#!/usr/bin/env python3
"""Build the bounded IMAGE-only static type-info class map.

This does not select a serializer schema.  It proves the distinct class identity
behind the two ItemAttr and two VitalData registry candidates.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import os
import re
import secrets
import shutil
import struct
import sys
from dataclasses import dataclass
from pathlib import Path


IMAGE_SHA = "9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623"
IMAGE_SIZE = 14_759_424
EXTRACTOR_SHA = "0bb792bb6b0561e11592ab7f8c93c65cd1e0fba0210e2a6bf40c9e5a8579112e"
REGISTRY_SHA = "27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d"
A2_SHA = "1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334"
NAME_IAT = 0x00C3B7AC
NAME_IMPORT = "?_name_internal_method@type_info@@QBEPBDPAU__type_info_node@@@Z"
CONSTRUCT_START, CONSTRUCT_END = 0x0088F2E0, 0x0088F307
CONSTRUCT_SHA = "a0835228ee17015e5baaafd8ad82b0e9f91f3410509ee73acfa430d029988596"
WALK_START, WALK_END = 0x0088F2B0, 0x0088F2D1
WALK_SHA = "00076eb0d61b7763ba58709f657437f455e6c6a2e3da83b3005bef0b847a61e9"


class BuildError(RuntimeError):
    pass


@dataclass(frozen=True)
class Expected:
    registry_name: str
    class_name: str
    decorated_name: str
    identity_kind: str
    vtable_va: int
    vtable_off: int
    registry_getter_va: int
    getter_pointer_off: int
    descriptor_getter_va: int
    descriptor_getter_target_va: int
    descriptor_va: int
    descriptor_refs: int
    type_descriptor_va: int
    type_descriptor_off: int
    name_off: int
    init_start: int
    init_end: int
    init_off: int
    init_sha: str
    base_chain: str


EXPECTED = (
    Expected("ItemAttr", "ItemAttr", ".?AVItemAttr@@", "EXACT_REGISTRY_CLASS",
             0x00F0EBB0, 0x00B0CFB0, 0x0046B4A0, 0x00B0CFC0,
             0x0046B3C0, 0x0046B3C0, 0x010335B4, 5,
             0x0101E6C0, 0x00C1BEC0, 0x00C1BEC8,
             0x00BD9900, 0x00BD9937, 0x007D8D00,
             "b3f455d619390db121fe5ebb67d3757ef6b3629d8c2a8964b13e1753ccf9971c",
             "ItemAttr"),
    Expected("ItemAttr", "StallItem", ".?AVStallItem@@", "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER",
             0x00F4A188, 0x00B48588, 0x0046B4A0, 0x00B48598,
             0x00766BE0, 0x00766BE0, 0x0108AEBC, 4,
             0x0101E590, 0x00C1BD90, 0x00C1BD98,
             0x00C0E260, 0x00C0E297, 0x0080D660,
             "8247c9aa2311c3aa741c92fbaf2c2083d7b140a96674aa44f820cec521c4201f",
             "StallItem->ItemAttr"),
    Expected("VitalData", "VitalData", ".?AVVitalData@@", "EXACT_REGISTRY_CLASS",
             0x00F0B930, 0x00B09D30, 0x004277C0, 0x00B09D40,
             0x004277B0, 0x005F33E0, 0x010823A8, 5,
             0x0101B16C, 0x00C1896C, 0x00C18974,
             0x00BF0150, 0x00BF0187, 0x007EF550,
             "1d86e643cbe74d5387d89d221c1eae6a36aa32a5bdd8616caac6de02a4dcf75b",
             "VitalData"),
    Expected("VitalData", "Channel_MessageVtial", ".?AVChannel_MessageVtial@@", "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER",
             0x00F375FC, 0x00B359FC, 0x004277C0, 0x00B35A0C,
             0x00657D10, 0x0065A930, 0x01084430, 7,
             0x01026100, 0x00C23900, 0x00C23908,
             0x00BF7570, 0x00BF75A6, 0x007F6970,
             "e0584b98c2097959d533c78402d0946af6e9b37711f151b4288ec1f4a5bef497",
             "Channel_MessageVtial->Channel_BasicVtial->ClonableVital->VitalData"),
)


HEADER = [
    "classmap_key", "registry_name", "class_name", "decorated_name",
    "identity_kind", "vtable_va", "vtable_file_off", "registry_getter_va",
    "getter_pointer_file_off", "descriptor_getter_va",
    "descriptor_getter_target_va", "descriptor_va", "descriptor_file_off",
    "descriptor_reference_count", "type_descriptor_va",
    "type_descriptor_file_off", "class_name_file_off", "initializer_start",
    "initializer_end", "initializer_file_off", "initializer_span_sha256",
    "base_descriptor_chain", "source",
]

# Independent, complete output oracle.  It is deliberately not assembled from
# EXPECTED: changing an in-memory semantic label must not be able to validate
# itself.  Every generated dictionary is compared field-for-field to this list.
EXPECTED_ROW_LINES = (
    "9ebe88d0ba94a645ac1911ab2b2f92cb81cb6f66fc792d20a522a17eed19a8f3\tItemAttr\tItemAttr\t.?AVItemAttr@@\tEXACT_REGISTRY_CLASS\t0x00F0EBB0\t0x00B0CFB0\t0x0046B4A0\t0x00B0CFC0\t0x0046B3C0\t0x0046B3C0\t0x010335B4\tUNMAPPED_BSS\t5\t0x0101E6C0\t0x00C1BEC0\t0x00C1BEC8\t0x00BD9900\t0x00BD9937\t0x007D8D00\tb3f455d619390db121fe5ebb67d3757ef6b3629d8c2a8964b13e1753ccf9971c\tItemAttr\tIMAGE",
    "b332bf2f220694fd18c771e91d309c762810ac5501df8cb435b4c3af0dd22b1c\tItemAttr\tStallItem\t.?AVStallItem@@\tPOLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER\t0x00F4A188\t0x00B48588\t0x0046B4A0\t0x00B48598\t0x00766BE0\t0x00766BE0\t0x0108AEBC\tUNMAPPED_BSS\t4\t0x0101E590\t0x00C1BD90\t0x00C1BD98\t0x00C0E260\t0x00C0E297\t0x0080D660\t8247c9aa2311c3aa741c92fbaf2c2083d7b140a96674aa44f820cec521c4201f\tStallItem->ItemAttr\tIMAGE",
    "1e2fa1c3e6d65207ee64ab8c02a6c60a88b460bec9f84dae68150a311621a26e\tVitalData\tVitalData\t.?AVVitalData@@\tEXACT_REGISTRY_CLASS\t0x00F0B930\t0x00B09D30\t0x004277C0\t0x00B09D40\t0x004277B0\t0x005F33E0\t0x010823A8\tUNMAPPED_BSS\t5\t0x0101B16C\t0x00C1896C\t0x00C18974\t0x00BF0150\t0x00BF0187\t0x007EF550\t1d86e643cbe74d5387d89d221c1eae6a36aa32a5bdd8616caac6de02a4dcf75b\tVitalData\tIMAGE",
    "8dad95be6029d9a5c448bb84bccd9c06d6e588e1fd993f85d9e82cacdc06fd2e\tVitalData\tChannel_MessageVtial\t.?AVChannel_MessageVtial@@\tPOLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER\t0x00F375FC\t0x00B359FC\t0x004277C0\t0x00B35A0C\t0x00657D10\t0x0065A930\t0x01084430\tUNMAPPED_BSS\t7\t0x01026100\t0x00C23900\t0x00C23908\t0x00BF7570\t0x00BF75A6\t0x007F6970\te0584b98c2097959d533c78402d0946af6e9b37711f151b4288ec1f4a5bef497\tChannel_MessageVtial->Channel_BasicVtial->ClonableVital->VitalData\tIMAGE",
)


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fmt(value: int) -> str:
    return "0x%08X" % value


def cstring(data: bytes, off: int) -> str:
    end = data.find(b"\0", off, off + 256)
    if end < 0:
        raise BuildError("unterminated TypeDescriptor name")
    try:
        return data[off:end].decode("ascii")
    except UnicodeDecodeError as exc:
        raise BuildError("non-ASCII TypeDescriptor name") from exc


def undecorate_class_name(decorated: str) -> str:
    match = re.fullmatch(r"\.\?AV([A-Za-z_][A-Za-z0-9_]*)@@", decorated)
    if match is None:
        raise BuildError("unsupported/non-exact TypeDescriptor class name")
    return match.group(1)


def rel32_target(site: int, raw: bytes) -> int:
    return (site + 5 + struct.unpack("<i", raw[1:5])[0]) & 0xFFFFFFFF


def load_extractor(path: Path):
    if sha_file(path) != EXTRACTOR_SHA:
        raise BuildError("pf_extract_protocol.py hash mismatch")
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("pf_static_classmap_extract", path)
    if spec is None or spec.loader is None:
        raise BuildError("cannot load pinned extractor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def strict_rows(path: Path, expected_sha: str) -> list[dict[str, str]]:
    if sha_file(path) != expected_sha:
        raise BuildError(path.name + " hash mismatch")
    text = path.read_text(encoding="utf-8")
    reader = csv.DictReader(io.StringIO(text), dialect="excel-tab")
    if (reader.fieldnames is None or any(not field for field in reader.fieldnames)
            or len(reader.fieldnames) != len(set(reader.fieldnames))):
        raise BuildError(path.name + " invalid header")
    rows = []
    seen = set()
    for row in reader:
        if (None in row or set(row) != set(reader.fieldnames)
                or any(value is None for value in row.values())):
            raise BuildError(path.name + " malformed row")
        fingerprint = tuple(row[field] for field in reader.fieldnames)
        if fingerprint in seen:
            raise BuildError(path.name + " duplicate complete row")
        seen.add(fingerprint)
        rows.append(row)
    return rows


def descriptor_from_getter(data: bytes, image, getter_va: int) -> int:
    off = image.va_range_to_off(getter_va, 6)
    if off is None:
        raise BuildError("descriptor getter is unmapped")
    raw = data[off:off + 6]
    if raw[0] == 0xE9:
        getter_va = rel32_target(getter_va, raw[:5])
        off = image.va_range_to_off(getter_va, 6)
        if off is None:
            raise BuildError("descriptor getter thunk target is unmapped")
        raw = data[off:off + 6]
    if len(raw) != 6 or raw[0] != 0xB8 or raw[5] != 0xC3:
        raise BuildError("descriptor getter is not exact mov-eax/ret")
    return struct.unpack_from("<I", raw, 1)[0]


def validate_complete_row_oracle(rows: list[dict[str, str]]) -> None:
    oracle = [dict(zip(HEADER, line.split("\t"), strict=True))
              for line in EXPECTED_ROW_LINES]
    if len(rows) != len(oracle):
        raise BuildError("complete class-map row count oracle mismatch")
    for index, (row, expected) in enumerate(zip(rows, oracle, strict=True)):
        if set(row) != set(HEADER) or row != expected:
            changed = sorted(key for key in set(row) | set(expected)
                             if row.get(key) != expected.get(key))
            raise BuildError("complete class-map row oracle mismatch at %d: %s"
                             % (index + 1, ",".join(changed)))


def run_semantic_mutation_regressions(rows: list[dict[str, str]]) -> None:
    cases = (
        {"class_name": "BogusClass"},
        {"identity_kind": "EXACT_REGISTRY_CLASS"},
        {"base_descriptor_chain": "BogusClass"},
        {"class_name": "BogusClass", "identity_kind": "EXACT_REGISTRY_CLASS",
         "base_descriptor_chain": "BogusClass"},
    )
    for mutation in cases:
        altered = [dict(row) for row in rows]
        altered[1].update(mutation)
        try:
            validate_complete_row_oracle(altered)
        except BuildError:
            continue
        raise BuildError("semantic mutation regression was accepted")


def derive_base_chains(data: bytes, image,
                       class_by_descriptor: dict[int, str]) -> dict[str, str]:
    # StallItem descriptor getter returns the ItemAttr descriptor.
    stall_parent = descriptor_from_getter(data, image, 0x0046B3C0)
    if stall_parent != 0x010335B4:
        raise BuildError("StallItem -> ItemAttr descriptor link changed")
    # Channel_BasicVtial initializer takes ClonableVital as its base.
    basic = image.va_range_to_off(0x00BF74F0, 0x37)
    if basic is None:
        raise BuildError("Channel_BasicVtial initializer unmapped")
    basic_bytes = data[basic:basic + 0x37]
    if not all(struct.pack("<I", value) in basic_bytes for value in
               (0x010260B8, 0x01084448, NAME_IAT)):
        raise BuildError("Channel_BasicVtial initializer proof changed")
    if basic_bytes[0x11] != 0xE8:
        raise BuildError("Channel_BasicVtial base getter changed")
    basic_base_getter = rel32_target(0x00BF7501, basic_bytes[0x11:0x16])
    if basic_base_getter != 0x005F33F0:
        raise BuildError("Channel_BasicVtial base getter changed")
    # ClonableVital initializer takes VitalData as its base.
    clone = image.va_range_to_off(0x00BF0190, 0x37)
    if clone is None:
        raise BuildError("ClonableVital initializer unmapped")
    clone_bytes = data[clone:clone + 0x37]
    if not all(struct.pack("<I", value) in clone_bytes for value in
               (0x010255C8, 0x0108239C, 0x010823A8, NAME_IAT)):
        raise BuildError("ClonableVital -> VitalData descriptor link changed")
    basic_type_off = image.va_range_to_off(0x010260B8, 9)
    clone_type_off = image.va_range_to_off(0x010255C8, 9)
    if basic_type_off is None or clone_type_off is None:
        raise BuildError("ancestor TypeDescriptor is unmapped")
    basic_name = undecorate_class_name(cstring(data, basic_type_off + 8))
    clone_name = undecorate_class_name(cstring(data, clone_type_off + 8))
    basic_parent = descriptor_from_getter(data, image, basic_base_getter)
    if basic_parent != 0x0108239C:
        raise BuildError("Channel_BasicVtial -> ClonableVital link changed")
    # The exact ClonableVital initializer embeds its VitalData base descriptor.
    if struct.pack("<I", 0x010823A8) not in clone_bytes:
        raise BuildError("ClonableVital -> VitalData link changed")
    item_name = class_by_descriptor.get(stall_parent)
    vital_name = class_by_descriptor.get(0x010823A8)
    if item_name is None or vital_name is None:
        raise BuildError("base descriptor is outside exact four-row identity map")
    return {
        "StallItem": "StallItem->" + item_name,
        "Channel_MessageVtial": "Channel_MessageVtial->" + basic_name
        + "->" + clone_name + "->" + vital_name,
    }


def build(base: Path, image_path: Path) -> tuple[bytes, bytes, str]:
    extractor_path = base / "pf_extract_protocol.py"
    registry_path = base / "PF_PROTOCOL_REGISTRY.tsv"
    a2_path = base / "PF_A2_SERIALIZER_SLOT34_DELTA.tsv"
    module = load_extractor(extractor_path)
    if image_path.stat().st_size != IMAGE_SIZE or sha_file(image_path) != IMAGE_SHA:
        raise BuildError("pinned image mismatch")
    image = module.Image(image_path)
    data = image.data
    registry_rows = module.scan_registry(image)
    if len(registry_rows) != 519:
        raise BuildError("registry census changed")
    by_name = {row.name: row for row in registry_rows}
    if set(name for name in ("ItemAttr", "VitalData") if name in by_name) != {"ItemAttr", "VitalData"}:
        raise BuildError("target registry rows missing")
    saved_registry = strict_rows(registry_path, REGISTRY_SHA)
    saved_by_name = {row["name"]: row for row in saved_registry}
    for name in ("ItemAttr", "VitalData"):
        row = by_name[name]
        saved = saved_by_name.get(name)
        if saved is None or saved["getter_va"] != fmt(row.getter_va) or saved["source"] != "IMAGE":
            raise BuildError("saved registry target mismatch: " + name)

    candidates: dict[str, list[tuple[int, int]]] = {"ItemAttr": [], "VitalData": []}
    wanted = {by_name[name].getter_va: name for name in candidates}
    for pointer_off in range(16, len(data) - 15, 4):
        getter = struct.unpack_from("<I", data, pointer_off)[0]
        name = wanted.get(getter)
        if name is None or struct.unpack_from("<I", data, pointer_off - 8)[0] != 0x00401B20:
            continue
        vtable_off = pointer_off - 16
        vtable_va = image.off_to_va(vtable_off)
        if vtable_va is not None and image.va_range_to_off(vtable_va, 0x20) == vtable_off:
            candidates[name].append((vtable_va, pointer_off))
    expected_candidates = {
        "ItemAttr": [(0x00F0EBB0, 0x00B0CFC0), (0x00F4A188, 0x00B48598)],
        "VitalData": [(0x00F0B930, 0x00B09D40), (0x00F375FC, 0x00B35A0C)],
    }
    if candidates != expected_candidates:
        raise BuildError("complete two-candidate getter/marker census changed")

    symbol = image.imports_by_iat.get(NAME_IAT)
    if symbol is None or (symbol.dll, symbol.name) != ("MSVCR90.dll", NAME_IMPORT):
        raise BuildError("type_info name import changed")
    for start, end, expected_hash in (
        (CONSTRUCT_START, CONSTRUCT_END, CONSTRUCT_SHA),
        (WALK_START, WALK_END, WALK_SHA),
    ):
        off = image.va_range_to_off(start, end - start)
        if off is None or sha_bytes(data[off:off + end - start]) != expected_hash:
            raise BuildError("descriptor helper proof span changed")

    derived_identity: dict[int, tuple[str, str]] = {}
    for item in EXPECTED:
        if image.va_range_to_off(item.type_descriptor_va, 9) != item.type_descriptor_off:
            raise BuildError("TypeDescriptor mapping changed")
        decorated_name = cstring(data, item.name_off)
        derived_identity[item.descriptor_va] = (
            undecorate_class_name(decorated_name), decorated_name
        )
    class_by_descriptor = {
        descriptor: identity[0] for descriptor, identity in derived_identity.items()
    }
    derived_chains = derive_base_chains(data, image, class_by_descriptor)

    output_rows: list[dict[str, str]] = []
    for item in EXPECTED:
        class_name, decorated_name = derived_identity[item.descriptor_va]
        identity_kind = ("EXACT_REGISTRY_CLASS" if class_name == item.registry_name
                         else "POLYMORPHIC_DERIVED_SHARING_REGISTRY_GETTER")
        base_chain = derived_chains.get(class_name, class_name)
        if image.va_to_off(item.descriptor_va) is not None:
            raise BuildError("runtime descriptor unexpectedly raw-backed")
        if item.descriptor_va < 0x0102BE00:
            raise BuildError("runtime descriptor is not in measured .data BSS tail")
        if image.va_range_to_off(item.vtable_va, 0x20) != item.vtable_off:
            raise BuildError("vtable mapping changed: " + item.class_name)
        if struct.unpack_from("<I", data, item.getter_pointer_off)[0] != item.registry_getter_va:
            raise BuildError("registry getter pointer changed: " + item.class_name)
        if struct.unpack_from("<I", data, item.vtable_off)[0] != item.descriptor_getter_va:
            raise BuildError("slot0 descriptor getter changed: " + item.class_name)
        getter_off = image.va_range_to_off(item.descriptor_getter_va, 5)
        if getter_off is None:
            raise BuildError("descriptor getter unmapped")
        getter = data[getter_off:getter_off + 6]
        if getter[0] == 0xE9:
            target = rel32_target(item.descriptor_getter_va, getter[:5])
            target_off = image.va_range_to_off(target, 6)
            if target != item.descriptor_getter_target_va or target_off is None:
                raise BuildError("descriptor getter thunk target changed")
            getter = data[target_off:target_off + 6]
        elif item.descriptor_getter_target_va != item.descriptor_getter_va:
            raise BuildError("expected descriptor getter thunk missing")
        if getter != b"\xB8" + struct.pack("<I", item.descriptor_va) + b"\xC3":
            raise BuildError("descriptor getter body changed: " + item.class_name)
        if data.count(struct.pack("<I", item.descriptor_va)) != item.descriptor_refs:
            raise BuildError("descriptor reference census changed: " + item.class_name)
        if image.va_range_to_off(item.init_start, item.init_end - item.init_start) != item.init_off:
            raise BuildError("initializer mapping changed")
        init_bytes = data[item.init_off:item.init_off + item.init_end - item.init_start]
        if sha_bytes(init_bytes) != item.init_sha or b"\xFF\x15" + struct.pack("<I", NAME_IAT) not in init_bytes:
            raise BuildError("initializer proof changed: " + item.class_name)
        if struct.pack("<I", item.type_descriptor_va) not in init_bytes or struct.pack("<I", item.descriptor_va) not in init_bytes:
            raise BuildError("initializer identity operands changed")
        values = [item.registry_name, class_name, decorated_name,
                  identity_kind, fmt(item.vtable_va), fmt(item.descriptor_va),
                  fmt(item.type_descriptor_va), base_chain, "IMAGE"]
        key = sha_bytes("\t".join(values).encode("utf-8"))
        values_by_field = [
            key, item.registry_name, class_name, decorated_name, identity_kind,
            fmt(item.vtable_va), fmt(item.vtable_off), fmt(item.registry_getter_va),
            fmt(item.getter_pointer_off), fmt(item.descriptor_getter_va),
            fmt(item.descriptor_getter_target_va), fmt(item.descriptor_va),
            "UNMAPPED_BSS", str(item.descriptor_refs), fmt(item.type_descriptor_va),
            fmt(item.type_descriptor_off), fmt(item.name_off), fmt(item.init_start),
            fmt(item.init_end), fmt(item.init_off), item.init_sha, base_chain, "IMAGE",
        ]
        output_rows.append(dict(zip(HEADER, values_by_field, strict=True)))
    validate_complete_row_oracle(output_rows)
    run_semantic_mutation_regressions(output_rows)
    if (len({row["classmap_key"] for row in output_rows}) != 4
            or len({row["vtable_va"] for row in output_rows}) != 4
            or len({row["descriptor_va"] for row in output_rows}) != 4):
        raise BuildError("duplicate class-map row/key/physical identity")

    a2_rows = strict_rows(a2_path, A2_SHA)
    base_refs = [row for row in a2_rows if row["message"] == "ItemAttr" and row["schema_variant"] == "VTABLE_0x00F0EBB0" and row["action"] == "ADD_AMBIGUOUS_CANDIDATE_ROW"]
    if len(base_refs) != 26 or any(row["source"] != "IMAGE" for row in base_refs):
        raise BuildError("existing exact ItemAttr candidate reference census changed")
    for other in base.glob("*.tsv"):
        if other.name == "PF_STATIC_TYPE_INFO_CLASSMAP.tsv":
            continue
        first = other.open("r", encoding="utf-8-sig", errors="strict").readline().rstrip("\r\n").split("\t")
        if "classmap_key" in first:
            raise BuildError("duplicate class-map namespace in " + other.name)

    out = io.StringIO(newline="")
    writer = csv.writer(out, dialect="excel-tab", lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows([row[field] for field in HEADER] for row in output_rows)
    tsv = out.getvalue().encode("utf-8")
    md = ("# Static type_info class map (IMAGE)\n\n"
          "## [MEASURED][IMAGE] Controls\n\n"
          "Pinned image SHA-256: `%s`. Rows: **4**.\n\n"
          "The complete aligned getter/marker census still has two candidates for `ItemAttr` and two for `VitalData`. "
          "Slot 0 descriptor getters plus the pinned MSVCR90 `type_info::_name_internal_method` import and exact static-initializer/RTTI edges identify the four static class identities shown in the TSV.\n\n"
          "## [MEASURED][IMAGE] Descriptor backing\n\n"
          "The descriptor-storage VAs are in the unbacked `.data` BSS tail (raw-backed end VA `0x0102BE00`), so every `descriptor_file_off` is `UNMAPPED_BSS`. "
          "No descriptor bytes were read or hashed. Backed MSVC TypeDescriptor names are separate IMAGE evidence.\n\n"
          "## [MEASURED][IMAGE] Interpretation guard\n\n"
          "`StallItem` shares the `ItemAttr` registry getter, and `Channel_MessageVtial` shares the `VitalData` registry getter. This establishes static class-hierarchy and registry-getter sharing only; it does **not** imply a runtime observation and does **not** justify collapsing or merging their serializer schemas. "
          "The base links are `StallItem -> ItemAttr` and `Channel_MessageVtial -> Channel_BasicVtial -> ClonableVital -> VitalData`.\n\n"
          "## [MEASURED][IMAGE] Delta accounting\n\n"
          "- Newly decoded A2 rows: **0**.\n"
          "- Existing exact `ItemAttr` candidate references (`VTABLE_0x00F0EBB0`): **26**.\n"
          "- Physical duplicate class-map rows: **0**.\n"
          "- Priority-1 closures: **0**.\n"
          "- Evidence source: **IMAGE** only. No DUMP, CAPTURE, or DATA evidence is mixed into these rows.\n\n"
          "This is an identity artifact only; it does not select a canonical ItemAttr schema and does not change A2/status/manifest/index files.\n" % IMAGE_SHA.upper()).encode("utf-8")
    return tsv, md, image.sha256


def write_sync(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def publish(base: Path, products: dict[str, bytes]) -> None:
    lock = base / ".PF_STATIC_TYPE_INFO_CLASSMAP_PUBLISH.lock"
    txn = base / (".PF_STATIC_TYPE_INFO_CLASSMAP_TXN.%d" % os.getpid())
    token = ("pid=%d nonce=%s\n" % (os.getpid(), secrets.token_hex(16))).encode("ascii")
    fd = None
    acquired = False
    txn_created = False
    committed = False
    recovery_required = False
    installed: list[tuple[Path, Path | None]] = []
    try:
        binary_flag = getattr(os, "O_BINARY", 0)
        fd = os.open(
            str(lock), os.O_WRONLY | os.O_CREAT | os.O_EXCL | binary_flag, 0o600
        )
        acquired = True
        if os.write(fd, token) != len(token):
            raise BuildError("short publish-lock token write")
        os.fsync(fd)
        os.close(fd)
        fd = None
        txn.mkdir()
        txn_created = True
        staged = {}
        for name, data in products.items():
            staged[name] = txn / (name + ".new")
            write_sync(staged[name], data)
        plan = "\n".join(
            "%s\texisted=%s\tsha256=%s" %
            (name, "YES" if (base / name).exists() else "NO", sha_bytes(data))
            for name, data in products.items()
        ).encode("ascii") + b"\n"
        write_sync(txn / "publish.journal", plan)
        for name in products:
            target = base / name
            backup = txn / (name + ".old") if target.exists() else None
            # The durable journal and rollback entry both exist before the first
            # destructive rename for this target.
            installed.append((target, backup))
            if backup is not None:
                os.replace(target, backup)
            os.replace(staged[name], target)
        for name, data in products.items():
            if (base / name).read_bytes() != data:
                raise BuildError("post-publish readback mismatch")
        committed = True
        shutil.rmtree(txn)
    except BaseException as exc:
        if not committed:
            failures = []
            for target, backup in reversed(installed):
                try:
                    if target.exists():
                        target.unlink()
                    if backup is not None and backup.exists():
                        os.replace(backup, target)
                except BaseException as rollback_exc:
                    failures.append("%s: %s" % (target.name, rollback_exc))
            if failures:
                recovery_required = True
                raise BuildError(
                    "publish rollback failed; lock/transaction retained: "
                    + "; ".join(failures)
                ) from exc
            if txn_created and txn.exists():
                try:
                    shutil.rmtree(txn)
                except BaseException as cleanup_exc:
                    recovery_required = True
                    raise BuildError(
                        "rollback completed but transaction cleanup failed; "
                        "lock/transaction retained"
                    ) from cleanup_exc
        else:
            # Outputs passed exact readback; never attempt a partial rollback
            # after commit merely because cleanup was interrupted.
            recovery_required = True
        raise
    finally:
        if fd is not None:
            os.close(fd)
        if acquired and not recovery_required:
            try:
                if lock.read_bytes() != token:
                    raise BuildError("publish-lock ownership token changed")
                lock.unlink()
            except FileNotFoundError as exc:
                raise BuildError("owned publish lock disappeared") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--audit-only", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    base = Path(__file__).resolve().parent
    image_path = (args.image or (base.parents[1] / "GameClient" / "GameClient.local.bin")).resolve()
    before = sha_file(image_path)
    print("image_sha256_before=" + before)
    tsv, md, measured = build(base, image_path)
    products = {"PF_STATIC_TYPE_INFO_CLASSMAP.tsv": tsv, "PF_STATIC_TYPE_INFO_CLASSMAP.md": md}
    if args.check:
        for name, data in products.items():
            path = base / name
            if not path.is_file() or path.read_bytes() != data:
                raise BuildError(name + " is missing or not byte-exact")
    elif not args.audit_only:
        publish(base, products)
    after = sha_file(image_path)
    if after != before or after != measured or after != IMAGE_SHA:
        raise BuildError("image changed during build")
    print("image_sha256_after=" + after)
    print("ok rows=4 candidate_groups=2 physical_duplicates=0 new_a2_rows=0 p1_closures=0 mode=" + ("check" if args.check else "audit" if args.audit_only else "publish"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildError, OSError, csv.Error, ValueError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
