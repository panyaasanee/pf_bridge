#!/usr/bin/env python3
"""Re-derive DATA-only controls for Pirate Force object-role investigation.

The program reads pinned GameClient DATA and derived table mirrors without
modifying them.  It publishes one TSV/Markdown pair plus a last-written pair
marker beside this script.  All output is ASCII and every TSV row is DATA-only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import lzma
import os
import struct
import sys
import uuid
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable


FORMAT = "PF_MONSTER_ROLE_DATA_CONTROLS_V1"
PAIR_FORMAT = "PF_MONSTER_ROLE_DATA_CONTROLS_PAIR_V1"
EXPECTED_ROW_COUNT = 21

HERE = Path(__file__).resolve().parent
PF_ROOT = HERE.parent.parent
TABLE_ROOT = HERE.parent / "gamedata" / "tables"

MOBS_PATH = TABLE_ROOT / "CONSTDATA_TH__MOBS.tsv"
AI_WANDER_PATH = TABLE_ROOT / "CONSTDATA_TH__AI_WANDER.tsv"
AI_COMBAT_PATH = TABLE_ROOT / "CONSTDATA_TH__AI_COMBAT.tsv"
AI_TACTIC_PATH = TABLE_ROOT / "CONSTDATA_TH__AI_TACTIC.tsv"
MOBS_TIP_PATH = TABLE_ROOT / "TEXTDATA_TH__MOBS_TIP.tsv"
CONSTDATA_PATH = PF_ROOT / "GameClient" / "Data" / "B_CONSTDATA_TH.pc_"
TEXTDATA_PATH = PF_ROOT / "GameClient" / "Data" / "B_TEXTDATA_TH.pc_"
PRIOR_ROLE_PATH = (
    HERE
    / ".pf_attr_generations"
    / "b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae"
    / "PF_ATTR_ROLE_DISCRIMINATOR.tsv"
)

TSV_PATH = HERE / "PF_MONSTER_ROLE_DATA_CONTROLS.tsv"
MD_PATH = HERE / "PF_MONSTER_ROLE_DATA_CONTROLS.md"
PAIR_PATH = HERE / "PF_MONSTER_ROLE_DATA_CONTROLS.pair.json"
LOCK_PATH = HERE / ".pf_monster_role_data_controls.lock"


INPUT_PINS: dict[Path, tuple[int, str]] = {
    MOBS_PATH: (
        749_302,
        "3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b",
    ),
    AI_WANDER_PATH: (
        2_313,
        "0b3f1eb8e67915c4be5758c734cae17c575ac2aa76cb989e13242cfb6ad01a23",
    ),
    AI_COMBAT_PATH: (
        79_483,
        "19cbc17fb124b5569dbe670fd793d22f00fec72645e6027348f09a6612d04a46",
    ),
    AI_TACTIC_PATH: (
        2_393,
        "ddcdf163795217d717b5cf25d696ed60d93b51244a8f451541d7eed555efc42a",
    ),
    MOBS_TIP_PATH: (
        239_200,
        "e25ac667c9029e07752fbfd5d13b548d2e62ea439936884f30187c0c553ce38f",
    ),
    CONSTDATA_PATH: (
        426_944,
        "496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8",
    ),
    TEXTDATA_PATH: (
        336_985,
        "56b4826ed437c3f30bd1937c580ca612c22655600b5fbeb781b64c767e74c467",
    ),
    PRIOR_ROLE_PATH: (
        42_626,
        "3e8d99dd9fd9c8717e27d3ec8d43e2599a6037fc366e58637aff3a5cc8d5ec73",
    ),
}

DECODED_PINS = {
    CONSTDATA_PATH: (
        8_443_000,
        "496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d",
    ),
    TEXTDATA_PATH: (
        3_548_508,
        "80c8ae29b8fcd8fa2ca132a85d0ac786105d006ac7ed401639455ad1a940a5b0",
    ),
}

DECODED_SPANS = {
    "MOBS": (
        CONSTDATA_PATH,
        0x0035AE0A,
        0x004A327E,
        "7abbecfdd78b4ec08f6371a700bbb936851e77f4916891f93c7f472c1af22390",
    ),
    "AI_WANDER": (
        CONSTDATA_PATH,
        0x00329A46,
        0x0032AA74,
        "0ee49521d6ab52af1d3fbc394844b088ff935fb33c285ed3b56713b8e3f26ff8",
    ),
    "AI_TACTIC": (
        CONSTDATA_PATH,
        0x0032AA74,
        0x0032BC36,
        "73b72fe4a45a47b638f5ea8772898ed6d227a6ec292a9e9c0c7eceb7bac27f31",
    ),
    "AI_COMBAT": (
        CONSTDATA_PATH,
        0x0032BC36,
        0x00351094,
        "6c7194a80bd5ced44540dd21a159d3139f93315745d5f6e2f9187c976dd0fa37",
    ),
    "MOBS_TIP": (
        TEXTDATA_PATH,
        0x001FEC7A,
        0x002431D6,
        "c57a550f96930fb739c16d702bee8a47b0b8d182bfc5d07b601b9a23382af20d",
    ),
}

MOBS_HEADER = (
    "n_ID", "s_NAME", "s_ID_MODEL_CLASS", "n_ID_MODEL", "n_ID_MAP",
    "s_PREDESCRIPT", "s_OUTFIT", "n_BOUNDARY", "n_HEIGHT", "n_LEVEL_MIN",
    "n_LEVEL_MAX", "n_RANK", "f_RATIO_EXP", "f_RATIO_SP", "s_PROPERTIES",
    "n_SPEED_WALK", "n_SPEED_RUN", "n_VEHICLE", "n_AI_WANDER",
    "n_AI_COMBAT", "n_AI_TACTIC", "s_SKILLS", "n_DEADMISSILE",
    "n_CONDITION", "n_SKIN_COLOR", "s_FX_SELECT", "n_WATER_DOWN",
    "s_FX_GORE", "n_INTIMATE", "n_CREDIT", "n_PVPSCORE", "n_MOB_APPEAR",
    "n_DROP_RANGE", "n_DROPS_EQUIPMENT", "n_DROPS_NORMAL",
    "n_DROPS_SPECIALLY", "n_DROP_FLOOR", "n_DROPS_QUEST",
    "s_QUEST_BEGIN", "s_QUEST_END", "n_CAPABILITY", "s_ICON", "s_LOCATION",
    "n_GM_SWITCH", "n_FITTINGROOM_DISTANCE", "n_FITTINGROOM_HEIGHT",
    "s_NPC_VOICE", "s_ROLE_GRAPHIC", "n_BROADCAST", "n_MOB_USAGE",
    "s_HK_VER", "s_TC_VER", "s_JP_VER", "s_TH_VER",
)
AI_WANDER_HEADER = ("n_ID", "s_WANDER", "n_FACTION", "n_OFFESIVE", "n_AGGRO")
AI_COMBAT_HEADER = ("n_ID", "s_CONDITOIN", "s_ACTION")
AI_TACTIC_HEADER = ("n_ID", "s_CREWID", "s_CONDITION", "s_ENEMY", "s_ALLY")
MOBS_TIP_HEADER = ("n_ID", "s_NAME", "s_TITLE", "s_NPC_CHATS")

EXPECTED_TABLE_SHAPES = {
    MOBS_PATH: (MOBS_HEADER, 3_210),
    AI_WANDER_PATH: (AI_WANDER_HEADER, 73),
    AI_COMBAT_PATH: (AI_COMBAT_HEADER, 276),
    AI_TACTIC_PATH: (AI_TACTIC_HEADER, 9),
    MOBS_TIP_PATH: (MOBS_TIP_HEADER, 3_139),
}

PRIOR_ROW_CLAIMS = {
    "MOBS_SCHEMA_CENSUS": "5de62fd8517fd720f520f4423e5c98f9571a04dced848f658060387db4ed7260",
    "MOBS_USAGE_VALUE_DOMAIN": "39168c0e09b7369589dd44991a4320091675e1664aa93ba57e2bc48b53a330e4",
    "MOBS_RANK_COMBAT_CROSS": "7f7621a88e675aff29253fbaa5459f5d6c96ea9dc7d9a8b573aa52bb7df84943",
    "MOBS_OFFESIVE_WEIGHTED_CROSS": "6be00acea321d43dcb58527da89b7752aa1ba965dba387a24c8bc3d1d6e419fd",
    "MOBS_CAPABILITY_QUEST_CROSS": "276b84804d8c700f3d99f3f3fe223e3ae3da17740b19a9dd7121beef75897c5d",
    "MOBS_USAGE1_RC_CLUSTER": "a093ef7ba1578d9165d188d797ccba3ab00aae64a082c44a223c56c7b2fe4a73",
    "MOBS_USAGE2_KQ_CLUSTER": "f5325cec52077563a172092c9605b4af77c083b180b1a388ba78704fc31a8b92",
    "MOBS_ID916_FINGERPRINT": "336e01a3e400c9d74ab7ee580f6853dfe9125a260b8610e2bb37981b6025d5d2",
    "MOBS_ID917_FINGERPRINT": "5289a5e0db3b67652c017601ac9bb61d2fad50ed1cf7dfa596c4f4f3123fe96b",
}

COLUMNS = (
    "control_id", "control_key", "row_kind", "axis", "subject",
    "measurement_label", "method", "control", "exact_observation",
    "measured_count", "semantic_status", "scope", "evidence_file",
    "evidence_file_size", "evidence_file_sha256", "evidence_locator",
    "support_files", "support_file_sizes", "support_file_sha256s",
    "evidence_key", "claim_sha256", "prior_artifact",
    "prior_artifact_size", "prior_artifact_sha256", "prior_row_id",
    "prior_row_key", "prior_row_claim_sha256", "relationship_to_prior",
    "supersedes_artifact", "supersedes_row_id", "supersedes_row_key",
    "supersedes_claim_digest", "corrected_field", "authority_precedence",
    "source", "nonclaim", "blocker", "required_next_evidence",
)

EXPECTED_IDS = (
    "CONSTDATA_INPUT_CHAIN",
    "TEXTDATA_INPUT_CHAIN",
    "AI_WANDER_LINK_INTEGRITY",
    "AI_COMBAT_LINK_INTEGRITY",
    "AI_TACTIC_LINK_INTEGRITY",
    "AI_COMBAT_TACTIC_COUPLING",
    "USAGE_RCO_FULL_MATRIX",
    "USAGE_U1_COUNTEREXAMPLES",
    "USAGE_U2_KQ_MIXED_TRAITS",
    "USAGE_U7_MIXED_TRAITS",
    "MOBS_TIP_NON_TOTAL_JOIN",
    "NPC_CHAT_MIXED_TRAITS",
    "NPC_VOICE_MIXED_TRAITS",
    "ROLE_GRAPHIC_MIXED_TRAITS",
    "LEXICAL_MONSTER_COUNTEREXAMPLES",
    "OFFENSIVE_AGGRO_POSITIVE_MATRIX",
    "ID916_LEXICAL_TRAINING_CORRECTION",
    "ID916_COARSE_TRAIT_COHORT",
    "ID917_MISSING_TIP_CONTROL",
    "NO_DATA_SIDE_NPCATTR_SCHEMA",
    "NO_VALIDATED_DATA_ROLE_LAW",
)

# Filled after the authored schema and fixed facts are reviewed.  It is a hash
# over all metric values, not over generated output, so label-only edits cannot
# silently move measured facts.
EXPECTED_METRICS_SHA256 = "d032c714a5eb9401744d6df02bccde34ad7705122e84b62f1115386413855435"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, code: str) -> None:
    if not condition:
        raise VerificationError(code)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_key(domain: str, *parts: Any) -> str:
    material = domain + "\0" + "\0".join(str(part) for part in parts)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def ids_text(values: Iterable[int]) -> str:
    return ",".join(str(value) for value in sorted(values))


def ids_hash(values: Iterable[int]) -> str:
    return sha256_bytes(ids_text(values).encode("ascii"))


def root_uri(path: Path) -> str:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(PF_ROOT.resolve())
    except ValueError as exc:
        raise VerificationError("input_outside_pf_root") from exc
    return "PF_ROOT://" + relative.as_posix()


def verify_input(path: Path) -> bytes:
    require(path in INPUT_PINS, "unregistered_input")
    expected_size, expected_hash = INPUT_PINS[path]
    data = path.read_bytes()
    require(len(data) == expected_size, "input_size_mismatch_" + path.name)
    require(sha256_bytes(data) == expected_hash, "input_hash_mismatch_" + path.name)
    return data


def decode_pcz(data: bytes) -> bytes:
    require(len(data) >= 13 and data[:4] == b"$pcz", "pcz_header_mismatch")
    expected_size = struct.unpack_from("<I", data, 4)[0]
    props = data[8:13]
    first = props[0]
    require(first < 9 * 5 * 5, "pcz_property_mismatch")
    lc = first % 9
    rest = first // 9
    lp = rest % 5
    pb = rest // 5
    dictionary = struct.unpack_from("<I", props, 1)[0]
    require(dictionary != 0, "pcz_dictionary_zero")
    decoder = lzma.LZMADecompressor(
        format=lzma.FORMAT_RAW,
        filters=[{
            "id": lzma.FILTER_LZMA1,
            "lc": lc,
            "lp": lp,
            "pb": pb,
            "dict_size": dictionary,
        }],
    )
    decoded = decoder.decompress(data[13:], max_length=expected_size + 1)
    require(len(decoded) == expected_size, "pcz_decoded_size_mismatch")
    return decoded


def verify_decoded_inputs(raw_inputs: dict[Path, bytes]) -> dict[Path, bytes]:
    decoded: dict[Path, bytes] = {}
    for path, (expected_size, expected_hash) in DECODED_PINS.items():
        payload = decode_pcz(raw_inputs[path])
        require(len(payload) == expected_size, "decoded_size_mismatch_" + path.name)
        require(sha256_bytes(payload) == expected_hash, "decoded_hash_mismatch_" + path.name)
        decoded[path] = payload
    for label, (path, start, end, expected_hash) in DECODED_SPANS.items():
        require(end <= len(decoded[path]), "decoded_span_bounds_" + label)
        require(
            sha256_bytes(decoded[path][start:end]) == expected_hash,
            "decoded_span_hash_mismatch_" + label,
        )
    return decoded


def parse_tsv(path: Path, raw: bytes) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError("tsv_utf8_mismatch_" + path.name) from exc
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    header = tuple(reader.fieldnames or ())
    rows = [dict(row) for row in reader]
    expected_header, expected_count = EXPECTED_TABLE_SHAPES[path]
    require(header == expected_header, "tsv_schema_mismatch_" + path.name)
    require(len(rows) == expected_count, "tsv_row_count_mismatch_" + path.name)
    require(
        all(set(row) == set(expected_header) for row in rows),
        "tsv_row_schema_mismatch_" + path.name,
    )
    return header, rows


def parse_prior(raw: bytes) -> tuple[tuple[str, ...], dict[str, dict[str, str]]]:
    text = raw.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    header = tuple(reader.fieldnames or ())
    required = {
        "discriminator_id", "discriminator_key", "claim_sha256",
        "exact_observation", "measured_count", "source",
    }
    require(required.issubset(header), "prior_role_schema_mismatch")
    rows = [dict(row) for row in reader]
    require(len(rows) == 28, "prior_role_row_count_mismatch")
    by_id = {row["discriminator_id"]: row for row in rows}
    require(len(by_id) == len(rows), "prior_role_duplicate_id")
    for row_id, claim_hash in PRIOR_ROW_CLAIMS.items():
        require(row_id in by_id, "prior_role_missing_" + row_id)
        row = by_id[row_id]
        require(row["claim_sha256"] == claim_hash, "prior_role_claim_mismatch_" + row_id)
        require(row["source"] == "DATA", "prior_role_source_mismatch_" + row_id)
        require(len(row["discriminator_key"]) == 64, "prior_role_key_mismatch_" + row_id)
    return header, by_id


def as_int(row: dict[str, str], field: str) -> int:
    value = row[field]
    try:
        result = int(value, 10)
    except ValueError as exc:
        raise VerificationError("integer_parse_mismatch_" + field) from exc
    require(str(result) == value, "integer_canonical_mismatch_" + field)
    return result


def present(value: str) -> bool:
    return value not in {"", "0"}


def unique_by_id(rows: list[dict[str, str]], label: str) -> dict[int, dict[str, str]]:
    result: dict[int, dict[str, str]] = {}
    for row in rows:
        row_id = as_int(row, "n_ID")
        require(row_id not in result, "duplicate_id_" + label)
        result[row_id] = row
    return result


def metric_fingerprint(metrics: dict[str, Any]) -> str:
    raw = json.dumps(metrics, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256_bytes(raw.encode("ascii"))


def compute_metrics(tables: dict[Path, list[dict[str, str]]]) -> dict[str, Any]:
    mobs = tables[MOBS_PATH]
    wander_rows = tables[AI_WANDER_PATH]
    combat_rows = tables[AI_COMBAT_PATH]
    tactic_rows = tables[AI_TACTIC_PATH]
    tip_rows = tables[MOBS_TIP_PATH]

    mobs_by_id = unique_by_id(mobs, "MOBS")
    wander_by_id = unique_by_id(wander_rows, "AI_WANDER")
    combat_by_id = unique_by_id(combat_rows, "AI_COMBAT")
    tactic_by_id = unique_by_id(tactic_rows, "AI_TACTIC")
    tip_by_id = unique_by_id(tip_rows, "MOBS_TIP")
    line_by_mob_id = {as_int(row, "n_ID"): index + 2 for index, row in enumerate(mobs)}
    line_by_tip_id = {as_int(row, "n_ID"): index + 2 for index, row in enumerate(tip_rows)}

    def rank(row: dict[str, str]) -> bool:
        return as_int(row, "n_RANK") > 0

    def combat(row: dict[str, str]) -> bool:
        return as_int(row, "n_AI_COMBAT") != 0

    def tactic(row: dict[str, str]) -> bool:
        return as_int(row, "n_AI_TACTIC") != 0

    def joined_wander(row: dict[str, str]) -> dict[str, str] | None:
        wander_id = as_int(row, "n_AI_WANDER")
        return None if wander_id == 0 else wander_by_id.get(wander_id)

    def offensive(row: dict[str, str]) -> bool:
        joined = joined_wander(row)
        return joined is not None and as_int(joined, "n_OFFESIVE") != 0

    def aggro_positive(row: dict[str, str]) -> bool:
        joined = joined_wander(row)
        return joined is not None and as_int(joined, "n_AGGRO") > 0

    def capability(row: dict[str, str]) -> bool:
        return as_int(row, "n_CAPABILITY") == 1

    def quest(row: dict[str, str]) -> bool:
        return present(row["s_QUEST_BEGIN"]) or present(row["s_QUEST_END"])

    def ordinary_drop(row: dict[str, str]) -> bool:
        return any(
            as_int(row, field) != 0
            for field in ("n_DROPS_EQUIPMENT", "n_DROPS_NORMAL", "n_DROPS_SPECIALLY")
        )

    def chat(row: dict[str, str]) -> bool:
        tip = tip_by_id.get(as_int(row, "n_ID"))
        return tip is not None and present(tip["s_NPC_CHATS"])

    def voice(row: dict[str, str]) -> bool:
        return present(row["s_NPC_VOICE"])

    def graphic(row: dict[str, str]) -> bool:
        return present(row["s_ROLE_GRAPHIC"])

    link_metrics: dict[str, Any] = {}
    for label, field, definitions in (
        ("W", "n_AI_WANDER", wander_by_id),
        ("C", "n_AI_COMBAT", combat_by_id),
        ("T", "n_AI_TACTIC", tactic_by_id),
    ):
        refs = [as_int(row, field) for row in mobs]
        nonzero = [value for value in refs if value != 0]
        distinct = sorted(set(nonzero))
        missing = sorted(set(distinct) - set(definitions))
        orphan = sorted(set(definitions) - set(distinct))
        link_metrics[label] = {
            "mobs_rows": len(mobs),
            "zero_refs": len(refs) - len(nonzero),
            "nonzero_refs": len(nonzero),
            "distinct_refs": len(distinct),
            "definition_rows": len(definitions),
            "duplicate_definition_ids": 0,
            "missing_refs": missing,
            "orphan_definitions": orphan,
        }

    coupling = Counter()
    for row in mobs:
        coupling[
            "W%dC%dT%d"
            % (
                as_int(row, "n_AI_WANDER") != 0,
                combat(row),
                tactic(row),
            )
        ] += 1
    coupling_mismatches = sum(combat(row) != tactic(row) for row in mobs)

    usage_rco: dict[str, dict[str, int]] = {}
    for usage in range(9):
        selected = [row for row in mobs if as_int(row, "n_MOB_USAGE") == usage]
        cells = Counter(
            "R%dC%dO%d" % (rank(row), combat(row), offensive(row))
            for row in selected
        )
        usage_rco[str(usage)] = {"total": len(selected), **dict(sorted(cells.items()))}

    usage1 = [row for row in mobs if as_int(row, "n_MOB_USAGE") == 1]
    all_rc = [row for row in mobs if rank(row) and combat(row)]
    usage1_non_rc = sorted(as_int(row, "n_ID") for row in usage1 if not (rank(row) and combat(row)))
    rc_outside_usage1 = [row for row in all_rc if as_int(row, "n_MOB_USAGE") != 1]
    rc_outside_by_usage = Counter(as_int(row, "n_MOB_USAGE") for row in rc_outside_usage1)

    usage2_kq = [
        row for row in mobs
        if as_int(row, "n_MOB_USAGE") == 2 and capability(row) and quest(row)
    ]
    usage2_rank_ids = sorted(as_int(row, "n_ID") for row in usage2_kq if rank(row))
    usage2_combat_ids = sorted(as_int(row, "n_ID") for row in usage2_kq if combat(row))
    usage2_offensive_ids = sorted(as_int(row, "n_ID") for row in usage2_kq if offensive(row))

    def usage_trait_metrics(usage: int) -> dict[str, int]:
        selected = [row for row in mobs if as_int(row, "n_MOB_USAGE") == usage]
        return {
            "total": len(selected),
            "R": sum(rank(row) for row in selected),
            "C": sum(combat(row) for row in selected),
            "O": sum(offensive(row) for row in selected),
            "K": sum(capability(row) for row in selected),
            "Q": sum(quest(row) for row in selected),
            "chat": sum(chat(row) for row in selected),
            "voice": sum(voice(row) for row in selected),
            "role_graphic": sum(graphic(row) for row in selected),
        }

    mob_ids = set(mobs_by_id)
    tip_ids = set(tip_by_id)
    joined_ids = sorted(mob_ids & tip_ids)
    missing_tip_ids = sorted(mob_ids - tip_ids)
    orphan_tip_ids = sorted(tip_ids - mob_ids)

    def mixed_trait_metrics(predicate: Any) -> dict[str, Any]:
        selected = [row for row in mobs if predicate(row)]
        usage_counts = Counter(as_int(row, "n_MOB_USAGE") for row in selected)
        result: dict[str, Any] = {
            "populated": len(selected),
            "R": sum(rank(row) for row in selected),
            "C": sum(combat(row) for row in selected),
            "O": sum(offensive(row) for row in selected),
            "K": sum(capability(row) for row in selected),
            "Q": sum(quest(row) for row in selected),
            "drops": sum(ordinary_drop(row) for row in selected),
            "usage": {str(key): usage_counts[key] for key in sorted(usage_counts)},
        }
        return result

    chat_metrics = mixed_trait_metrics(chat)
    chat_metrics["voice"] = sum(chat(row) and voice(row) for row in mobs)
    voice_metrics = mixed_trait_metrics(voice)
    voice_metrics["distinct_values"] = len({row["s_NPC_VOICE"] for row in mobs if voice(row)})
    graphic_metrics = mixed_trait_metrics(graphic)
    graphic_metrics["distinct_values"] = len({row["s_ROLE_GRAPHIC"] for row in mobs if graphic(row)})

    lexical_tip_ids = sorted(
        as_int(row, "n_ID")
        for row in tip_rows
        if "monster" in row["s_NAME"].casefold()
    )
    lexical_joined = sorted(set(lexical_tip_ids) & mob_ids)
    lexical_orphans = sorted(set(lexical_tip_ids) - mob_ids)
    lexical_usage = Counter(as_int(mobs_by_id[row_id], "n_MOB_USAGE") for row_id in lexical_joined)

    oa = Counter(
        "O%dA%d" % (offensive(row), aggro_positive(row))
        for row in mobs
    )
    o0_apos_ids = sorted(
        as_int(row, "n_ID")
        for row in mobs
        if not offensive(row) and aggro_positive(row)
    )

    row916 = mobs_by_id[916]
    tip916 = tip_by_id.get(916)
    row917 = mobs_by_id[917]
    require(tip916 is not None, "id916_tip_missing")
    coarse_cohort = sorted(
        as_int(row, "n_ID")
        for row in mobs
        if as_int(row, "n_MOB_USAGE") == 7
        and not rank(row)
        and not combat(row)
        and not tactic(row)
        and not capability(row)
        and not quest(row)
        and not ordinary_drop(row)
        and offensive(row)
    )
    cohort_tip_present = sorted(row_id for row_id in coarse_cohort if row_id in tip_by_id)
    cohort_tip_missing = sorted(row_id for row_id in coarse_cohort if row_id not in tip_by_id)

    properties_7174_count = sum(row["s_PROPERTIES"] == "7174" for row in mobs)
    properties_7175_count = sum(row["s_PROPERTIES"] == "7175" for row in mobs)
    name916_count = sum(row["s_NAME"] == row916["s_NAME"] for row in mobs)

    metrics: dict[str, Any] = {
        "links": link_metrics,
        "coupling": dict(sorted(coupling.items())),
        "coupling_mismatches": coupling_mismatches,
        "usage_rco": usage_rco,
        "usage1": {
            **usage_trait_metrics(1),
            "RC": sum(rank(row) and combat(row) for row in usage1),
            "non_RC_ids": usage1_non_rc,
            "RC_outside_U1": len(rc_outside_usage1),
            "RC_outside_by_usage": {
                str(key): rc_outside_by_usage[key] for key in sorted(rc_outside_by_usage)
            },
        },
        "usage2": {
            **usage_trait_metrics(2),
            "KQ": len(usage2_kq),
            "KQ_R_ids": usage2_rank_ids,
            "KQ_C_ids": usage2_combat_ids,
            "KQ_O_ids": usage2_offensive_ids,
        },
        "usage7": usage_trait_metrics(7),
        "tip_join": {
            "mobs": len(mob_ids),
            "tips": len(tip_ids),
            "overlap": len(joined_ids),
            "mobs_without_tip": len(missing_tip_ids),
            "tips_without_mobs": len(orphan_tip_ids),
            "mobs_without_tip_ids_sha256": ids_hash(missing_tip_ids),
            "tips_without_mobs_ids_sha256": ids_hash(orphan_tip_ids),
            "duplicate_mobs_ids": 0,
            "duplicate_tip_ids": 0,
        },
        "chat": chat_metrics,
        "voice": voice_metrics,
        "graphic": graphic_metrics,
        "lexical_monster": {
            "tip_name_hits": len(lexical_tip_ids),
            "joined": len(lexical_joined),
            "orphans": len(lexical_orphans),
            "tip_ids": lexical_tip_ids,
            "joined_ids": lexical_joined,
            "orphan_ids": lexical_orphans,
            "joined_R": sum(rank(mobs_by_id[row_id]) for row_id in lexical_joined),
            "joined_C": sum(combat(mobs_by_id[row_id]) for row_id in lexical_joined),
            "joined_O": sum(offensive(mobs_by_id[row_id]) for row_id in lexical_joined),
            "joined_K": sum(capability(mobs_by_id[row_id]) for row_id in lexical_joined),
            "joined_Q": sum(quest(mobs_by_id[row_id]) for row_id in lexical_joined),
            "joined_usage": {str(key): lexical_usage[key] for key in sorted(lexical_usage)},
        },
        "oa": {
            **dict(sorted(oa.items())),
            "O0A1_ids": o0_apos_ids,
        },
        "id916": {
            "mobs_line": line_by_mob_id[916],
            "tip_line": line_by_tip_id[916],
            "tip_label": tip916["s_NAME"],
            "tip_label_sha256": sha256_bytes(tip916["s_NAME"].encode("utf-8")),
            "mobs_name_sha256": sha256_bytes(row916["s_NAME"].encode("utf-8")),
            "mobs_name_occurrences": name916_count,
            "rank": as_int(row916, "n_RANK"),
            "wander": as_int(row916, "n_AI_WANDER"),
            "combat": as_int(row916, "n_AI_COMBAT"),
            "tactic": as_int(row916, "n_AI_TACTIC"),
            "usage": as_int(row916, "n_MOB_USAGE"),
            "capability": as_int(row916, "n_CAPABILITY"),
            "quest": int(quest(row916)),
            "drop": int(ordinary_drop(row916)),
            "faction": as_int(wander_by_id[as_int(row916, "n_AI_WANDER")], "n_FACTION"),
            "offensive": int(offensive(row916)),
            "aggro": as_int(wander_by_id[as_int(row916, "n_AI_WANDER")], "n_AGGRO"),
            "property7174_occurrences": properties_7174_count,
        },
        "cohort916": {
            "ids": coarse_cohort,
            "tip_present": len(cohort_tip_present),
            "tip_missing": len(cohort_tip_missing),
            "tip_missing_ids": cohort_tip_missing,
        },
        "id917": {
            "mobs_line": line_by_mob_id[917],
            "tip_present": 917 in tip_by_id,
            "mobs_name_sha256": sha256_bytes(row917["s_NAME"].encode("utf-8")),
            "rank": as_int(row917, "n_RANK"),
            "wander": as_int(row917, "n_AI_WANDER"),
            "combat": as_int(row917, "n_AI_COMBAT"),
            "tactic": as_int(row917, "n_AI_TACTIC"),
            "usage": as_int(row917, "n_MOB_USAGE"),
            "capability": as_int(row917, "n_CAPABILITY"),
            "quest": int(quest(row917)),
            "drop": int(ordinary_drop(row917)),
            "faction": as_int(wander_by_id[as_int(row917, "n_AI_WANDER")], "n_FACTION"),
            "offensive": int(offensive(row917)),
            "aggro": as_int(wander_by_id[as_int(row917, "n_AI_WANDER")], "n_AGGRO"),
            "property7175_occurrences": properties_7175_count,
        },
        "npcattr_schema": {
            "tables": 5,
            "header_cells": sum(len(shape[0]) for shape in EXPECTED_TABLE_SHAPES.values()),
            "npcattr_header_hits": sum(
                "npcattr" in column.casefold()
                for shape in EXPECTED_TABLE_SHAPES.values()
                for column in shape[0]
            ),
            "offset_width_direction_header_sets": sum(
                {"offset", "width", "direction"}.issubset(
                    {column.casefold() for column in shape[0]}
                )
                for shape in EXPECTED_TABLE_SHAPES.values()
            ),
        },
    }
    return metrics


def expected_metrics() -> dict[str, Any]:
    """Independent fixed census used to fail closed on input or logic drift."""
    return {
        "links": {
            "W": {
                "mobs_rows": 3210, "zero_refs": 17, "nonzero_refs": 3193,
                "distinct_refs": 61, "definition_rows": 73,
                "duplicate_definition_ids": 0, "missing_refs": [],
                "orphan_definitions": [7, 18, 19, 113, 118, 1002, 1003, 1004, 9000, 9001, 9903, 9904],
            },
            "C": {
                "mobs_rows": 3210, "zero_refs": 1326, "nonzero_refs": 1884,
                "distinct_refs": 184, "definition_rows": 276,
                "duplicate_definition_ids": 0, "missing_refs": [],
                "orphan_definitions": [
                    2, 9, 122, 126, 143, 154, 184, 213, 263, 265, 284, 285,
                    294, 305, 314, 334, 470, 500, 510, 520, 530, 540, 550,
                    1000, 1002, 1004, 1005, 1007, 1008, 1009, 1010, 1011,
                    1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1021,
                    1022, 1024, 1025, 1026, 1028, 1030, 1032, 1033, 1035,
                    1036, 1037, 1038, 1500, 1501, 1502, 1503, 1504, 1505,
                    1506, 1507, 1511, 1512, 1513, 1514, 1515, 1516, 1517,
                    1521, 1522, 1523, 1524, 1525, 1526, 1527, 1531, 1532,
                    1533, 1534, 1535, 1536, 1537, 1541, 1542, 1543, 1544,
                    1545, 1546, 1547, 9903, 9904, 9999,
                ],
            },
            "T": {
                "mobs_rows": 3210, "zero_refs": 1326, "nonzero_refs": 1884,
                "distinct_refs": 6, "definition_rows": 9,
                "duplicate_definition_ids": 0, "missing_refs": [],
                "orphan_definitions": [4, 100, 9903],
            },
        },
        "coupling": {"W0C0T0": 17, "W1C0T0": 1309, "W1C1T1": 1884},
        "coupling_mismatches": 0,
        "usage_rco": {
            "0": {"total": 180, "R0C0O0": 180},
            "1": {"total": 1545, "R0C0O0": 2, "R0C1O0": 1,
                  "R0C1O1": 5, "R1C0O0": 1, "R1C0O1": 3,
                  "R1C1O0": 246, "R1C1O1": 1287},
            "2": {"total": 832, "R0C0O0": 784, "R0C1O1": 14,
                  "R1C0O0": 18, "R1C1O0": 9, "R1C1O1": 7},
            "3": {"total": 2, "R1C1O1": 2},
            "4": {"total": 17, "R0C1O1": 6, "R1C1O1": 11},
            "5": {"total": 122, "R0C0O0": 93, "R0C1O1": 28,
                  "R1C1O1": 1},
            "6": {"total": 83, "R0C0O0": 71, "R0C0O1": 12},
            "7": {"total": 346, "R0C0O0": 127, "R0C0O1": 21,
                  "R0C1O1": 147, "R1C0O0": 6, "R1C0O1": 4,
                  "R1C1O0": 19, "R1C1O1": 22},
            "8": {"total": 83, "R0C0O0": 4, "R0C1O0": 1,
                  "R0C1O1": 10, "R1C1O0": 3, "R1C1O1": 65},
        },
        "usage1": {
            "total": 1545, "R": 1537, "C": 1539, "O": 1295, "K": 3,
            "Q": 2, "chat": 918, "voice": 1, "role_graphic": 8, "RC": 1533,
            "non_RC_ids": [642, 896, 933, 1017, 1924, 1925, 8039, 8041, 8163, 8180, 9043, 9044],
            "RC_outside_U1": 139,
            "RC_outside_by_usage": {"2": 16, "3": 2, "4": 11, "5": 1, "7": 41, "8": 68},
        },
        "usage2": {
            "total": 832, "R": 34, "C": 30, "O": 21, "K": 674,
            "Q": 691, "chat": 790, "voice": 652, "role_graphic": 212,
            "KQ": 670,
            "KQ_R_ids": [528, 529, 576, 586, 850, 1666, 1667, 1690, 1691, 1720, 1721, 3170],
            "KQ_C_ids": [157, 187, 191, 529, 573, 576, 586, 918, 1480, 1487],
            "KQ_O_ids": [157, 187, 191, 573, 586, 918, 1480, 1487],
        },
        "usage7": {
            "total": 346, "R": 51, "C": 188, "O": 194, "K": 75,
            "Q": 90, "chat": 72, "voice": 3, "role_graphic": 0,
        },
        "tip_join": {
            "mobs": 3210, "tips": 3139, "overlap": 2931,
            "mobs_without_tip": 279, "tips_without_mobs": 208,
            "mobs_without_tip_ids_sha256": "adb19bbea412aad0a7dba890493a501d3551016659876023fbd43f99e2b986e8",
            "tips_without_mobs_ids_sha256": "6d0fe47586801fdf6cfafc51e70fb63e21b50df60c2ea5ce45b6ee09ee55b02b",
            "duplicate_mobs_ids": 0, "duplicate_tip_ids": 0,
        },
        "chat": {
            "populated": 1844, "R": 990, "C": 1006, "O": 875, "K": 674,
            "Q": 707, "drops": 926,
            "usage": {"0": 4, "1": 918, "2": 790, "3": 2, "4": 13, "5": 13, "6": 23, "7": 72, "8": 9},
            "voice": 637,
        },
        "voice": {
            "populated": 666, "R": 26, "C": 32, "O": 23, "K": 544,
            "Q": 551, "drops": 1,
            "usage": {"1": 1, "2": 652, "4": 8, "7": 3, "8": 2},
            "distinct_values": 192,
        },
        "graphic": {
            "populated": 257, "R": 16, "C": 27, "O": 34, "K": 204,
            "Q": 200, "drops": 7,
            "usage": {"1": 8, "2": 212, "4": 8, "5": 15, "6": 13, "8": 1},
            "distinct_values": 30,
        },
        "lexical_monster": {
            "tip_name_hits": 15, "joined": 6, "orphans": 9,
            "tip_ids": [256, 541, 1611, 1612, 3059, 8028, 9501, 9502, 9503, 9504, 9505, 9506, 9507, 9508, 9509],
            "joined_ids": [256, 541, 1611, 1612, 3059, 8028],
            "orphan_ids": [9501, 9502, 9503, 9504, 9505, 9506, 9507, 9508, 9509],
            "joined_R": 4, "joined_C": 4, "joined_O": 4, "joined_K": 1,
            "joined_Q": 1, "joined_usage": {"1": 1, "2": 2, "7": 2, "8": 1},
        },
        "oa": {
            "O0A0": 1550, "O0A1": 15, "O1A1": 1645,
            "O0A1_ids": [917, 927, 1207, 1473, 1476, 1512, 1931, 1932, 2871, 3496, 8167, 8168, 8169, 8170, 8171],
        },
        "id916": {
            "mobs_line": 894, "tip_line": 913, "tip_label": "Training Iron Man",
            "tip_label_sha256": "25d822136e1c222df8398c4e4cf69c82a2906646860603c541d22f6126da15b5",
            "mobs_name_sha256": "7dc60f6834675000c6170f06ea40ee41d360998cc11ad819a09a8c3620554f25",
            "mobs_name_occurrences": 1, "rank": 0, "wander": 21, "combat": 0,
            "tactic": 0, "usage": 7, "capability": 0, "quest": 0, "drop": 0,
            "faction": 12, "offensive": 1, "aggro": 3000,
            "property7174_occurrences": 1,
        },
        "cohort916": {
            "ids": [872, 873, 916, 1112, 1113, 1135, 1136, 1204, 1209, 1773, 1929, 1933, 1934, 9012, 9027, 9028, 9029, 9030, 9031, 9034, 9036],
            "tip_present": 11, "tip_missing": 10,
            "tip_missing_ids": [872, 873, 1112, 1113, 1136, 1204, 1209, 1933, 1934, 9036],
        },
        "id917": {
            "mobs_line": 895, "tip_present": False,
            "mobs_name_sha256": "2120757a8e99bd922c88d0fdac05a88d6815c2a36c1384807d1ce315cacbb2ea", "rank": 0, "wander": 40,
            "combat": 0, "tactic": 0, "usage": 7, "capability": 0,
            "quest": 0, "drop": 0, "faction": 28, "offensive": 0,
            "aggro": 3000, "property7175_occurrences": 1,
        },
        "npcattr_schema": {
            "tables": 5, "header_cells": 71, "npcattr_header_hits": 0,
            "offset_width_direction_header_sets": 0,
        },
    }


def dict_text(values: dict[str, int], prefix: str = "") -> str:
    return ";".join(prefix + str(key) + "=" + str(values[key]) for key in sorted(values, key=lambda item: int(item) if str(item).isdigit() else str(item)))


def build_rows(
    metrics: dict[str, Any],
    prior_rows: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    prior_size, prior_hash = INPUT_PINS[PRIOR_ROLE_PATH]

    def prior_fields(row_ids: tuple[str, ...]) -> dict[str, str]:
        if not row_ids:
            return {
                "prior_artifact": "N/A", "prior_artifact_size": "N/A",
                "prior_artifact_sha256": "N/A", "prior_row_id": "N/A",
                "prior_row_key": "N/A", "prior_row_claim_sha256": "N/A",
            }
        ordered = tuple(sorted(row_ids))
        return {
            "prior_artifact": root_uri(PRIOR_ROLE_PATH),
            "prior_artifact_size": str(prior_size),
            "prior_artifact_sha256": prior_hash,
            "prior_row_id": ";".join(ordered),
            "prior_row_key": ";".join(prior_rows[row_id]["discriminator_key"] for row_id in ordered),
            "prior_row_claim_sha256": ";".join(prior_rows[row_id]["claim_sha256"] for row_id in ordered),
        }

    def add(
        control_id: str,
        row_kind: str,
        axis: str,
        subject: str,
        measurement_label: str,
        method: str,
        control: str,
        exact_observation: str,
        measured_count: str,
        semantic_status: str,
        scope: str,
        evidence: Path,
        locator: str,
        supports: tuple[Path, ...],
        prior_ids: tuple[str, ...],
        relationship: str,
        nonclaim: str,
        blocker: str,
        next_evidence: str,
        supersedes_row_id: str = "N/A",
        corrected_field: str = "N/A",
        authority_precedence: str = "N/A",
    ) -> None:
        evidence_size, evidence_hash = INPUT_PINS[evidence]
        support_paths = tuple(dict.fromkeys(supports))
        prior = prior_fields(prior_ids)
        if supersedes_row_id == "N/A":
            supersedes = {
                "supersedes_artifact": "N/A", "supersedes_row_id": "N/A",
                "supersedes_row_key": "N/A", "supersedes_claim_digest": "N/A",
            }
        else:
            old = prior_rows[supersedes_row_id]
            supersedes = {
                "supersedes_artifact": root_uri(PRIOR_ROLE_PATH),
                "supersedes_row_id": supersedes_row_id,
                "supersedes_row_key": old["discriminator_key"],
                "supersedes_claim_digest": old["claim_sha256"],
            }
        base = {
            "control_id": control_id,
            "row_kind": row_kind,
            "axis": axis,
            "subject": subject,
            "measurement_label": measurement_label,
            "method": method,
            "control": control,
            "exact_observation": exact_observation,
            "measured_count": measured_count,
            "semantic_status": semantic_status,
            "scope": scope,
            "evidence_file": root_uri(evidence),
            "evidence_file_size": str(evidence_size),
            "evidence_file_sha256": evidence_hash,
            "evidence_locator": locator,
            "support_files": ";".join(root_uri(path) for path in support_paths) or "N/A",
            "support_file_sizes": ";".join(str(INPUT_PINS[path][0]) for path in support_paths) or "N/A",
            "support_file_sha256s": ";".join(INPUT_PINS[path][1] for path in support_paths) or "N/A",
            **prior,
            "relationship_to_prior": relationship,
            **supersedes,
            "corrected_field": corrected_field,
            "authority_precedence": authority_precedence,
            "source": "DATA",
            "nonclaim": nonclaim,
            "blocker": blocker,
            "required_next_evidence": "PROPOSED: " + next_evidence,
        }
        evidence_key = stable_key(
            "PF_MONSTER_ROLE_DATA_EVIDENCE_V1",
            control_id, base["evidence_file"], base["evidence_file_sha256"],
            locator, base["support_files"], base["support_file_sha256s"],
            exact_observation, measured_count,
        )
        base["evidence_key"] = evidence_key
        claim_fields = (
            control_id, row_kind, axis, subject, measurement_label, method,
            control, exact_observation, measured_count, semantic_status, scope,
            prior["prior_row_id"], prior["prior_row_key"],
            relationship, supersedes["supersedes_row_id"], corrected_field,
            authority_precedence, nonclaim, blocker, base["required_next_evidence"],
        )
        base["claim_sha256"] = stable_key("PF_MONSTER_ROLE_DATA_CLAIM_V1", *claim_fields)
        base["control_key"] = stable_key(
            "PF_MONSTER_ROLE_DATA_ROW_V1", control_id, evidence_key, base["claim_sha256"]
        )
        rows.append({column: str(base[column]) for column in COLUMNS})

    const_supports = (CONSTDATA_PATH, MOBS_PATH, AI_WANDER_PATH, AI_COMBAT_PATH, AI_TACTIC_PATH)
    text_supports = (TEXTDATA_PATH, MOBS_TIP_PATH)
    joint_supports = const_supports + text_supports

    add(
        "CONSTDATA_INPUT_CHAIN", "DATA_INPUT_PIN", "input_integrity",
        "B_CONSTDATA_TH and four derived tables", "PACKED_DECODED_DERIVED_PIN",
        "Hash packed bytes, decode raw LZMA in memory, hash total payload and exact table spans, then hash derived TSV mirrors.",
        "All inputs are opened read-only; decoded bytes are never written.",
        "Packed size=426944 sha256=496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8;decoded size=8443000 sha256=496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d;MOBS,AI_WANDER,AI_COMBAT,AI_TACTIC span and derived-table hashes all match their fixed pins.",
        "packed_files=1;decoded_spans=4;derived_tables=4", "PROVEN_EXACT",
        "pinned_constdata_input_chain", CONSTDATA_PATH,
        "DECOMP spans MOBS=0x0035AE0A..0x004A327E;AI_WANDER=0x00329A46..0x0032AA74;AI_TACTIC=0x0032AA74..0x0032BC36;AI_COMBAT=0x0032BC36..0x00351094",
        const_supports[1:], (), "NEW_INPUT_CONTROL",
        "Input integrity does not assign gameplay meaning to any column.",
        "Input integrity alone does not validate an exact object-role law.",
        "Keep any consumer or runtime claim in a separately sourced artifact.",
    )
    add(
        "TEXTDATA_INPUT_CHAIN", "DATA_INPUT_PIN", "input_integrity",
        "B_TEXTDATA_TH and MOBS_TIP", "PACKED_DECODED_DERIVED_PIN",
        "Hash packed bytes, decode raw LZMA in memory, hash the total payload and MOBS_TIP span, then hash the derived TSV mirror.",
        "Text labels remain DATA labels and are not promoted to behavior.",
        "Packed size=336985 sha256=56b4826ed437c3f30bd1937c580ca612c22655600b5fbeb781b64c767e74c467;decoded size=3548508 sha256=80c8ae29b8fcd8fa2ca132a85d0ac786105d006ac7ed401639455ad1a940a5b0;MOBS_TIP span and derived-table hashes match their fixed pins.",
        "packed_files=1;decoded_spans=1;derived_tables=1", "PROVEN_EXACT",
        "pinned_textdata_input_chain", TEXTDATA_PATH,
        "DECOMP MOBS_TIP=0x001FEC7A..0x002431D6", text_supports[1:], (),
        "NEW_INPUT_CONTROL", "Text labels do not prove attackability or interaction policy.",
        "MOBS_TIP is not a total join with MOBS.",
        "Join by exact n_ID and retain both missing-side populations.",
    )

    for label, control_id, subject, evidence, prior_relationship in (
        ("W", "AI_WANDER_LINK_INTEGRITY", "MOBS.n_AI_WANDER to AI_WANDER.n_ID", AI_WANDER_PATH, "ADDITIVE_LINK_CENSUS"),
        ("C", "AI_COMBAT_LINK_INTEGRITY", "MOBS.n_AI_COMBAT to AI_COMBAT.n_ID", AI_COMBAT_PATH, "ADDITIVE_LINK_CENSUS"),
        ("T", "AI_TACTIC_LINK_INTEGRITY", "MOBS.n_AI_TACTIC to AI_TACTIC.n_ID", AI_TACTIC_PATH, "ADDITIVE_LINK_CENSUS"),
    ):
        values = metrics["links"][label]
        add(
            control_id, "DATA_JOIN_CONTROL", "AI_reference_integrity", subject,
            "FULL_LEFT_DOMAIN_REFERENCE_JOIN",
            "Parse all 3210 MOBS rows, retain zero references, resolve every nonzero exact ID, and count unused definitions separately.",
            "Zero-reference MOBS rows remain in the denominator; duplicate, missing, and orphan populations are independently counted.",
            "MOBS=%d;zero_refs=%d;nonzero_refs=%d;distinct_refs=%d;definition_rows=%d;duplicate_definition_ids=%d;missing_refs=%s;orphan_definition_ids=%s"
            % (
                values["mobs_rows"], values["zero_refs"], values["nonzero_refs"],
                values["distinct_refs"], values["definition_rows"],
                values["duplicate_definition_ids"], ids_text(values["missing_refs"]) or "NONE",
                ids_text(values["orphan_definitions"]) or "NONE",
            ),
            "population=3210;matched_nonzero=%d;missing_nonzero=%d;orphan_definitions=%d"
            % (values["nonzero_refs"], len(values["missing_refs"]), len(values["orphan_definitions"])),
            "PROVEN_EXACT", "complete_MOBS_left_domain", MOBS_PATH,
            "all MOBS rows;AI definition table all rows", (evidence, CONSTDATA_PATH),
            ("MOBS_SCHEMA_CENSUS",), prior_relationship,
            "Reference integrity does not name the gameplay meaning of an AI profile.",
            "No single joined ID is an exact NPC, monster, or training-object enum.",
            "Attach consumer evidence separately before assigning behavior semantics.",
        )

    coupling = metrics["coupling"]
    add(
        "AI_COMBAT_TACTIC_COUPLING", "DATA_MATRIX", "AI_reference_coupling",
        "MOBS W/C/T nonzero state", "FULL_3210_BINARY_MATRIX",
        "For every MOBS row, map each AI reference to zero/nonzero without dropping the 17 W=0 rows.",
        "Assert C and T nonzero states agree on all 3210 rows and publish every observed W/C/T cell.",
        "W0C0T0=%d;W1C0T0=%d;W1C1T1=%d;C_T_state_mismatches=%d"
        % (coupling["W0C0T0"], coupling["W1C0T0"], coupling["W1C1T1"], metrics["coupling_mismatches"]),
        "population=3210;observed_cells=3;mismatches=0", "PROVEN_EXACT",
        "complete_MOBS_binary_matrix", MOBS_PATH, "columns=n_AI_WANDER,n_AI_COMBAT,n_AI_TACTIC",
        (AI_WANDER_PATH, AI_COMBAT_PATH, AI_TACTIC_PATH, CONSTDATA_PATH),
        ("MOBS_SCHEMA_CENSUS",), "ADDITIVE_COUPLED_COUNT",
        "Binary co-occurrence does not prove that combat and tactic IDs have identical semantics.",
        "The table contains no role enum for the coupled state.",
        "Keep the coupling as reconstruction input, not a class label.",
    )

    rco_cell_keys = tuple(
        "R%dC%dO%d" % (rank_value, combat_value, offensive_value)
        for rank_value in (0, 1)
        for combat_value in (0, 1)
        for offensive_value in (0, 1)
    )
    matrix_text = "|".join(
        "U%s:%s" % (
            usage,
            ",".join(
                "%s=%d" % (cell_key, cells.get(cell_key, 0))
                for cell_key in rco_cell_keys
            ),
        )
        for usage, cells in metrics["usage_rco"].items()
    )
    add(
        "USAGE_RCO_FULL_MATRIX", "DATA_MATRIX", "usage_rank_combat_offensive",
        "MOBS.n_MOB_USAGE crossed with R/C/O", "FULL_USAGE_RCO_MATRIX",
        "Partition all MOBS rows by U=n_MOB_USAGE and exact R=(rank>0), C=(combat!=0), O=(joined offensive!=0) cells.",
        "All nine usage values and all zero cells are represented by a fixed complete-domain census.",
        matrix_text, "population=3210;usage_values=9;total_cells=72;nonzero_cells=33",
        "PROVEN_EXACT", "complete_MOBS_usage_domain", MOBS_PATH,
        "columns=n_MOB_USAGE,n_RANK,n_AI_COMBAT,n_AI_WANDER;AI_WANDER.n_OFFESIVE",
        (AI_WANDER_PATH, CONSTDATA_PATH),
        ("MOBS_USAGE_VALUE_DOMAIN", "MOBS_RANK_COMBAT_CROSS", "MOBS_OFFESIVE_WEIGHTED_CROSS"),
        "ADDITIVE_COMPLETE_MATRIX",
        "R, C, O, and U are measured traits; no cell name is a gameplay role.",
        "Every named role would still require an independent producer/consumer or runtime result.",
        "Use exact IDs and treat any selected reconstruction rule as a bounded hypothesis.",
    )

    u1 = metrics["usage1"]
    add(
        "USAGE_U1_COUNTEREXAMPLES", "DATA_COUNTEREXAMPLE_SET", "usage1_cluster_limits",
        "MOBS U=1", "EXACT_FALSE_POSITIVE_AND_FALSE_NEGATIVE_IDS",
        "Compare U=1 against the empirical R-and-C conjunction across the complete MOBS population.",
        "Publish all 12 U1 rows outside RC and the distribution of 139 RC rows outside U1.",
        "U1_total=1545;R=1537;C=1539;O=1295;K=3;Q=2;chat=918;voice=1;role_graphic=8;RC=1533;U1_non_RC_ids=%s;RC_outside_U1=139;RC_outside_by_U=%s"
        % (ids_text(u1["non_RC_ids"]), dict_text(u1["RC_outside_by_usage"], "U")),
        "counterexample_ids=12;missed_RC=139", "PROVEN_EXACT",
        "complete_MOBS_usage1_and_RC_comparator", MOBS_PATH,
        "all U1 rows plus all rank-positive/combat-nonzero rows",
        (AI_WANDER_PATH, MOBS_TIP_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_USAGE1_RC_CLUSTER",), "ADDITIVE_EXACT_COUNTEREXAMPLE_IDS",
        "RC is only a comparator, not ground-truth monster class.",
        "U1 and RC disagree in both directions.",
        "Do not implement U1 as an exact object-role law.",
    )

    u2 = metrics["usage2"]
    add(
        "USAGE_U2_KQ_MIXED_TRAITS", "DATA_COUNTEREXAMPLE_SET", "usage2_service_cluster_limits",
        "MOBS U=2 and KQ subset", "EXACT_MIXED_TRAIT_IDS",
        "Count U2 traits, then enumerate every R, C, and O row inside the exact U2+K+Q subset.",
        "No R/C/O row is discarded from the 670-row U2KQ denominator.",
        "U2_total=832;R=34;C=30;O=21;K=674;Q=691;chat=790;voice=652;role_graphic=212;U2KQ=670;KQ_R_ids=%s;KQ_C_ids=%s;KQ_O_ids=%s"
        % (ids_text(u2["KQ_R_ids"]), ids_text(u2["KQ_C_ids"]), ids_text(u2["KQ_O_ids"])),
        "U2KQ=670;R=12;C=10;O=8", "PROVEN_EXACT",
        "complete_MOBS_usage2_KQ_subset", MOBS_PATH,
        "columns=n_MOB_USAGE,n_CAPABILITY,quest vectors,n_RANK,n_AI_COMBAT,n_AI_WANDER",
        (AI_WANDER_PATH, MOBS_TIP_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_USAGE2_KQ_CLUSTER",), "ADDITIVE_EXACT_MIXED_IDS",
        "K and Q are DATA traits, not proved talkability or service admission.",
        "The U2KQ subset contains R, C, and O rows.",
        "Do not collapse the mixed subset into a universal NPC/service class.",
    )

    u7 = metrics["usage7"]
    add(
        "USAGE_U7_MIXED_TRAITS", "DATA_MATRIX", "usage7_mixed_population",
        "MOBS U=7", "COMPLETE_U7_TRAIT_COUNTS",
        "Count R, C, O, K, Q, chat, voice, and role-graphic traits over every U7 row.",
        "Use the full 346-row denominator and retain all seven observed R/C/O cells.",
        "U7_total=346;R=51;C=188;O=194;K=75;Q=90;chat=72;voice=3;role_graphic=0;RCO_cells=%s"
        % dict_text(metrics["usage_rco"]["7"]),
        "population=346;RCO_observed_cells=7", "PROVEN_EXACT",
        "complete_MOBS_usage7_population", MOBS_PATH,
        "all U7 rows;joined AI_WANDER and MOBS_TIP retained by left join",
        (AI_WANDER_PATH, MOBS_TIP_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_USAGE_VALUE_DOMAIN",), "ADDITIVE_U7_CONTROL",
        "U7 is a heterogeneous DATA population, not a training-object enum.",
        "No machine-readable role name accompanies U7.",
        "Use exact record evidence for any training-object behavior.",
    )

    join = metrics["tip_join"]
    add(
        "MOBS_TIP_NON_TOTAL_JOIN", "DATA_JOIN_CONTROL", "text_join_integrity",
        "MOBS and MOBS_TIP exact n_ID sets", "FULL_OUTER_ID_CENSUS",
        "Compare both complete unique-ID sets; count intersection and both one-sided populations.",
        "Use a full outer census so missing MOBS_TIP and orphan MOBS_TIP rows cannot disappear through an inner join.",
        "MOBS=3210;MOBS_TIP=3139;overlap=2931;MOBS_without_tip=279;MOBS_without_tip_ids_sha256=%s;TIP_without_MOBS=208;TIP_without_MOBS_ids_sha256=%s;duplicate_MOBS_ids=0;duplicate_TIP_ids=0"
        % (join["mobs_without_tip_ids_sha256"], join["tips_without_mobs_ids_sha256"]),
        "overlap=2931;left_only=279;right_only=208", "PROVEN_EXACT",
        "complete_MOBS_and_MOBS_TIP_id_domains", MOBS_PATH,
        "all n_ID values in both tables", (MOBS_TIP_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_SCHEMA_CENSUS",), "ADDITIVE_NON_TOTAL_JOIN",
        "Absence from MOBS_TIP does not prove invisibility, noninteraction, or a role.",
        "The two DATA tables are not a total one-to-one population.",
        "Keep exact missing-side controls in every text-dependent analysis.",
    )

    for key, control_id, subject, measurement, field_locator, relationship in (
        ("chat", "NPC_CHAT_MIXED_TRAITS", "joined MOBS_TIP.s_NPC_CHATS", "NONEMPTY_CHAT_LEFT_JOIN_CENSUS", "MOBS_TIP.s_NPC_CHATS", "NEW_MIXED_TRAIT_CONTROL"),
        ("voice", "NPC_VOICE_MIXED_TRAITS", "MOBS.s_NPC_VOICE", "NONEMPTY_VOICE_CENSUS", "MOBS.s_NPC_VOICE", "NEW_MIXED_TRAIT_CONTROL"),
        ("graphic", "ROLE_GRAPHIC_MIXED_TRAITS", "MOBS.s_ROLE_GRAPHIC", "NONEMPTY_ROLE_GRAPHIC_CENSUS", "MOBS.s_ROLE_GRAPHIC", "NEW_MIXED_TRAIT_CONTROL"),
    ):
        value = metrics[key]
        extra = ""
        if key == "chat":
            extra = ";voice=%d" % value["voice"]
        else:
            extra = ";distinct_values=%d" % value["distinct_values"]
        add(
            control_id, "DATA_MIXED_TRAIT_CONTROL", "presentation_or_text_trait", subject,
            measurement,
            "Select nonempty/nonzero values, retain the complete MOBS denominator, and cross the selected rows with independent R/C/O/K/Q/drop/usage traits.",
            "A populated text, voice, or graphic field is measured as presence only; raw non-ASCII values are never emitted.",
            "populated=%d;R=%d;C=%d;O=%d;K=%d;Q=%d;drops=%d;usage=%s%s"
            % (
                value["populated"], value["R"], value["C"], value["O"],
                value["K"], value["Q"], value["drops"],
                dict_text(value["usage"], "U"), extra,
            ),
            "population=%d;usage_values=%d" % (value["populated"], len(value["usage"])),
            "PROVEN_EXACT", "complete_nonempty_trait_population", MOBS_PATH,
            field_locator, (MOBS_TIP_PATH, AI_WANDER_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
            ("MOBS_SCHEMA_CENSUS",), relationship,
            "Presence does not define NPC, monster, talkability, hostility, or attackability.",
            "The selected population spans multiple independent trait combinations.",
            "Treat this field as its measured content/presentation axis only.",
        )

    lexical = metrics["lexical_monster"]
    add(
        "LEXICAL_MONSTER_COUNTEREXAMPLES", "DATA_LEXICAL_CONTROL", "lexical_role_noun",
        "case-insensitive monster substring in MOBS_TIP.s_NAME", "FULL_TIP_NAME_SUBSTRING_CENSUS",
        "Search every MOBS_TIP s_NAME value case-insensitively, then full-outer join exact IDs to MOBS and count independent traits.",
        "No raw names are emitted; only the ASCII search token, IDs, and counts are published.",
        "token=monster;TIP_name_hits=15;TIP_ids=%s;joined=6;joined_ids=%s;orphan=9;orphan_ids=%s;joined_R=4;joined_C=4;joined_O=4;joined_K=1;joined_Q=1;joined_usage=%s"
        % (
            ids_text(lexical["tip_ids"]), ids_text(lexical["joined_ids"]),
            ids_text(lexical["orphan_ids"]), dict_text(lexical["joined_usage"], "U"),
        ),
        "TIP_hits=15;joined=6;orphan=9;joined_usage_values=4", "PROVEN_LEXICAL_ONLY",
        "complete_MOBS_TIP_name_domain", MOBS_TIP_PATH,
        "column=s_NAME;casefold substring=monster", (MOBS_PATH, AI_WANDER_PATH, TEXTDATA_PATH, CONSTDATA_PATH),
        (), "NEW_LEXICAL_COUNTEREXAMPLE",
        "A name substring is not a machine-readable role enum.",
        "Lexical hits span U1, U2, U7, U8 and both joined/nonjoined populations.",
        "Require behavior evidence for every record before applying a gameplay role.",
    )

    oa = metrics["oa"]
    add(
        "OFFENSIVE_AGGRO_POSITIVE_MATRIX", "DATA_MATRIX", "offensive_aggro_relation",
        "MOBS-weighted AI_WANDER O/Apos", "FULL_3210_O_APOS_MATRIX",
        "Left join every MOBS row to AI_WANDER; treat W=0 as O0/A0; cross O=(offensive!=0) and Apos=(aggro>0).",
        "Retain the 15 O0/Apos exceptions and enumerate their exact IDs.",
        "O0A0=1550;O0Apos=15;O0Apos_ids=%s;O1Apos=1645;O1A0=0"
        % ids_text(oa["O0A1_ids"]),
        "population=3210;observed_cells=3;exception_ids=15", "PROVEN_EXACT",
        "complete_MOBS_weighted_wander_join", MOBS_PATH,
        "MOBS.n_AI_WANDER;AI_WANDER.n_OFFESIVE,n_AGGRO", (AI_WANDER_PATH, CONSTDATA_PATH),
        ("MOBS_OFFESIVE_WEIGHTED_CROSS",), "ADDITIVE_COMPLETE_O_APOS_MATRIX",
        "O implies positive aggro in this DATA census, but positive aggro does not imply O.",
        "Neither O nor Apos is proved attack admission or an object-role enum.",
        "Keep nameboard/presentation and action-admission evidence separate.",
    )

    id916 = metrics["id916"]
    add(
        "ID916_LEXICAL_TRAINING_CORRECTION", "DATA_CORRECTION", "lexical_identity",
        "MOBS and MOBS_TIP id 916", "EXACT_ID916_LEXICAL_JOIN",
        "Join exact id 916 across pinned MOBS, MOBS_TIP, and AI_WANDER; hash non-ASCII MOBS name and emit only the ASCII MOBS_TIP label.",
        "The correction is field-scoped to prior blocker wording; it does not rewrite the prior fingerprint or infer behavior.",
        "DATA contains lexical training labels for ID 916, but no machine-readable role enum or original attackability result. MOBS_line=894;MOBS_name_sha256=%s;MOBS_name_occurrences=1;MOBS_TIP_line=913;MOBS_TIP_label=Training Iron Man;label_sha256=%s;rank=0;wander=21;combat=0;tactic=0;U7;K0;Q0;drop0;faction=12;O1;aggro=3000;property7174_occurrences=1"
        % (id916["mobs_name_sha256"], id916["tip_label_sha256"]),
        "MOBS_records=1;MOBS_TIP_records=1;AI_WANDER_records=1", "PROVEN_LEXICAL_ONLY",
        "exact_id_916_join", MOBS_PATH,
        "MOBS derived_line=894;MOBS_TIP derived_line=913;AI_WANDER id=21",
        (MOBS_TIP_PATH, AI_WANDER_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_ID916_FINGERPRINT",), "FIELD_SCOPED_CORRECTION",
        "The ASCII label does not prove a dummy class, attackability, damage handling, or server policy.",
        "No machine-readable role enum or original interaction/attackability result is attached.",
        "Obtain exact behavior evidence for id 916 before implementing special handling.",
        supersedes_row_id="MOBS_ID916_FINGERPRINT",
        corrected_field="blocker",
        authority_precedence="FIELD_SCOPED_NEWER_DATA_EVIDENCE;CANONICAL_REPORT_AND_AUTHORITY_MUST_INDEX_THIS_PAIR;PRECEDENCE_APPLIES_TO_PRIOR_BLOCKER_ONLY",
    )

    cohort = metrics["cohort916"]
    add(
        "ID916_COARSE_TRAIT_COHORT", "DATA_COUNTEREXAMPLE_SET", "coarse_trait_nonuniqueness",
        "U7/R0/C0/T0/K0/Q0/drop0/O1 cohort", "EXACT_COARSE_TRAIT_COHORT",
        "Select the exact coarse tuple across all MOBS rows and publish every matching ID plus text-join coverage.",
        "The tuple deliberately excludes raw names and properties so its nonuniqueness is measurable.",
        "cohort_count=21;ids=%s;MOBS_TIP_present=11;MOBS_TIP_missing=10;missing_tip_ids=%s"
        % (ids_text(cohort["ids"]), ids_text(cohort["tip_missing_ids"])),
        "cohort=21;tip_present=11;tip_missing=10", "PROVEN_EXACT",
        "complete_MOBS_coarse_tuple_selection", MOBS_PATH,
        "all rows matching U7,R0,C0,T0,K0,Q0,drop0,O1",
        (AI_WANDER_PATH, MOBS_TIP_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_ID916_FINGERPRINT",), "ADDITIVE_NONUNIQUENESS_CONTROL",
        "Sharing the tuple does not prove shared behavior or role.",
        "ID 916 is one of 21 rows in this coarse DATA cohort.",
        "Use exact record identity and behavior evidence, not the tuple alone.",
    )

    id917 = metrics["id917"]
    add(
        "ID917_MISSING_TIP_CONTROL", "DATA_COUNTEREXAMPLE", "text_join_missing_control",
        "MOBS id 917", "EXACT_ID917_LEFT_ONLY_CONTROL",
        "Resolve exact MOBS id 917 and AI_WANDER id 40 while requiring absence from the complete MOBS_TIP ID set.",
        "The missing text row is retained rather than dropped from lexical analysis.",
        "MOBS_line=895;MOBS_name_sha256=%s;MOBS_TIP_records=0;rank=0;wander=40;combat=0;tactic=0;U7;K0;Q0;drop0;faction=28;O0;aggro=3000;property7175_occurrences=1"
        % id917["mobs_name_sha256"],
        "MOBS_records=1;MOBS_TIP_records=0;AI_WANDER_records=1", "PROVEN_EXACT",
        "exact_id_917_left_join", MOBS_PATH,
        "MOBS derived_line=895;MOBS_TIP complete-ID negative;AI_WANDER id=40",
        (MOBS_TIP_PATH, AI_WANDER_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_ID917_FINGERPRINT",), "ADDITIVE_MISSING_TIP_CONTROL",
        "Missing MOBS_TIP does not name the role or behavior of id 917.",
        "Positive aggro coexists with O0, and no text-row behavior inference is valid.",
        "Require exact behavior evidence if id 917 becomes implementation-relevant.",
    )

    schema = metrics["npcattr_schema"]
    add(
        "NO_DATA_SIDE_NPCATTR_SCHEMA", "DATA_BOUNDED_NEGATIVE", "schema_boundary",
        "five pinned role-input tables", "EXACT_HEADER_SCHEMA_CENSUS",
        "Validate every header cell in MOBS, AI_WANDER, AI_COMBAT, AI_TACTIC, and MOBS_TIP.",
        "The negative is bounded to the 71 explicit header cells in these five pinned tables and checks both NPCAttr naming and offset/width/direction schema columns.",
        "tables=5;header_cells=71;explicit_NPCAttr_header_hits=0;explicit_offset_width_direction_schema_header_sets=0",
        "tables=%d;header_cells=%d;negative_hits=0" % (schema["tables"], schema["header_cells"]),
        "BOUNDED_NEGATIVE", "five_pinned_DATA_table_headers", MOBS_PATH,
        "all header cells", (AI_WANDER_PATH, AI_COMBAT_PATH, AI_TACTIC_PATH, MOBS_TIP_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_SCHEMA_CENSUS",), "ADDITIVE_SCHEMA_BOUNDARY",
        "This header-only census does not exclude a schema encoded under neutral headers or in row values, is not a whole-GameClient search, and does not negate a separately proved serialized layout.",
        "No explicit NPCAttr or offset/width/direction schema header is present in these five pinned tables.",
        "Keep serialized NPCAttr layout evidence in its own source layer.",
    )

    add(
        "NO_VALIDATED_DATA_ROLE_LAW", "DATA_BOUNDED_CONCLUSION", "role_law_boundary",
        "audited DATA candidates", "AUDITED_ROLE_LAW_VALIDATION_STATUS",
        "Compare the complete usage/RCO matrix, U1/U2/U7 controls, text join, lexical hits, O/Apos matrix, and id916 cohort.",
        "Do not call a candidate validated without an independent original role or behavior oracle; none is present in these audited DATA inputs.",
        "U1_non_RC=12;RC_outside_U1=139;U2KQ_R=12;U2KQ_C=10;U2KQ_O=8;U7_RCO_cells=7;lexical_monster_joined_usage_values=4;O0Apos=15;id916_coarse_cohort=21",
        "audited_candidate_families=7;independent_role_oracles=0;validated_exact_role_laws=0", "NOT_VALIDATED",
        "pinned_DATA_candidate_set", MOBS_PATH,
        "controls=USAGE_RCO,U1,U2,U7,MOBS_TIP_lexical,O_Apos,id916_cohort",
        (AI_WANDER_PATH, AI_COMBAT_PATH, AI_TACTIC_PATH, MOBS_TIP_PATH, CONSTDATA_PATH, TEXTDATA_PATH),
        ("MOBS_USAGE1_RC_CLUSTER", "MOBS_USAGE2_KQ_CLUSTER", "MOBS_ID916_FINGERPRINT"),
        "ADDITIVE_COUNTEREXAMPLE_BOUNDARY",
        "This does not prove that any candidate is false, that no candidate is authoritative, or that no composite policy exists.",
        "No exact role law was identified or validated from the audited DATA candidates alone; DATA cannot decide which proxy, if any, is authoritative.",
        "Use client consumer/runtime evidence to close talk-versus-attack behavior.",
    )
    return rows


def validate_rows(rows: list[dict[str, str]], prior_rows: dict[str, dict[str, str]]) -> None:
    require(len(rows) == EXPECTED_ROW_COUNT, "output_row_count_mismatch")
    require(tuple(row["control_id"] for row in rows) == EXPECTED_IDS, "output_id_order_mismatch")
    require(all(tuple(row) == COLUMNS for row in rows), "output_schema_mismatch")
    require(len({row["control_id"] for row in rows}) == len(rows), "duplicate_control_id")
    require(len({row["control_key"] for row in rows}) == len(rows), "duplicate_control_key")
    require(len({row["evidence_key"] for row in rows}) == len(rows), "duplicate_evidence_key")
    require(len({row["claim_sha256"] for row in rows}) == len(rows), "duplicate_claim_sha256")
    require(all(row["source"] == "DATA" for row in rows), "mixed_source_row")
    require(all(all(value.isascii() for value in row.values()) for row in rows), "non_ascii_output_row")
    require(all(row["measurement_label"] and row["method"] and row["control"] for row in rows), "missing_measurement_method_control")
    require(all(row["required_next_evidence"].startswith("PROPOSED: ") for row in rows), "next_evidence_prefix_mismatch")
    prior_observations = {
        (row["exact_observation"], row["measured_count"])
        for row in prior_rows.values()
    }
    require(
        all((row["exact_observation"], row["measured_count"]) not in prior_observations for row in rows),
        "exact_duplicate_prior_claim",
    )
    correction = next(row for row in rows if row["control_id"] == "ID916_LEXICAL_TRAINING_CORRECTION")
    old = prior_rows["MOBS_ID916_FINGERPRINT"]
    require(correction["supersedes_artifact"] == root_uri(PRIOR_ROLE_PATH), "correction_supersedes_artifact")
    require(correction["supersedes_row_id"] == "MOBS_ID916_FINGERPRINT", "correction_supersedes_id")
    require(correction["supersedes_row_key"] == old["discriminator_key"], "correction_supersedes_key")
    require(correction["supersedes_claim_digest"] == old["claim_sha256"], "correction_supersedes_digest")
    require(correction["corrected_field"] == "blocker", "correction_field_scope")
    require(
        correction["exact_observation"].startswith(
            "DATA contains lexical training labels for ID 916, but no machine-readable role enum or original attackability result."
        ),
        "correction_exact_wording",
    )
    for row in rows:
        if row["prior_row_id"] != "N/A":
            ids = row["prior_row_id"].split(";")
            keys = row["prior_row_key"].split(";")
            claims = row["prior_row_claim_sha256"].split(";")
            require(len(ids) == len(keys) == len(claims), "prior_reference_arity")
            for row_id, key, claim in zip(ids, keys, claims):
                require(row_id in prior_rows, "prior_reference_missing")
                require(prior_rows[row_id]["source"] == "DATA", "prior_reference_mixed_source")
                require(prior_rows[row_id]["discriminator_key"] == key, "prior_reference_key")
                require(prior_rows[row_id]["claim_sha256"] == claim, "prior_reference_claim")


def render_tsv(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    data = buffer.getvalue().encode("ascii")
    return data


def render_md(rows: list[dict[str, str]], metrics: dict[str, Any], metrics_hash: str) -> bytes:
    lines = [
        "# PF Monster Role DATA Controls",
        "",
        "Status: CHECKPOINT / PROVISIONAL",
        "",
        "Source boundary: every TSV row is `source=DATA`. No IMAGE, DUMP, CAPTURE, server, or runtime fact is merged into a row.",
        "",
        "## Result",
        "",
        "- Published controls: %d DATA rows." % len(rows),
        "- Metrics fingerprint: `%s`." % metrics_hash,
        "- Bounded conclusion: no exact role law was identified or validated from the audited DATA candidates alone. These DATA controls cannot decide which proxy, if any, is authoritative.",
        "- No explicit NPCAttr or offset/width/direction schema header is present among the 71 header cells of the five pinned tables. This header-only result does not exclude schemas encoded under neutral headers or in row values.",
        "- DATA contains lexical training labels for ID 916, but no machine-readable role enum or original attackability result.",
        "- The exact ASCII MOBS_TIP label for id 916 is `Training Iron Man`. This corrects only the prior blocker text; it does not prove dummy behavior or attackability.",
        "- MOBS id 917 has no current MOBS_TIP row and remains an explicit missing-side control.",
        "",
        "## Input pins",
        "",
        "| Input | Size | SHA256 |",
        "|---|---:|---|",
    ]
    for path in sorted(INPUT_PINS, key=lambda item: root_uri(item)):
        size, digest = INPUT_PINS[path]
        lines.append("| `%s` | %d | `%s` |" % (root_uri(path), size, digest))
    lines.extend([
        "",
        "Packed DATA is decoded only in memory. Fixed decoded totals and the five exact table-span hashes are verified before any result is rendered.",
        "",
        "## Complete-domain safeguards",
        "",
        "- AI_WANDER: MOBS 3210; zero references 17; nonzero references 3193; all 3193 matched; duplicate definition IDs 0; unused definitions 12. The 17 zero-reference rows are never lost to an inner join.",
        "- AI_COMBAT: zero references 1326; nonzero references 1884; all matched; duplicate definition IDs 0; unused definitions 92.",
        "- AI_TACTIC: zero references 1326; nonzero references 1884; all matched; duplicate definition IDs 0; unused definitions 3.",
        "- Combat/tactic nonzero state agrees on all 3210 MOBS rows. This is a coupled count, not proof that the two IDs have the same meaning.",
        "- MOBS and MOBS_TIP are not a total join: overlap 2931, MOBS-only 279, MOBS_TIP-only 208.",
        "",
        "## Mixed-trait controls",
        "",
        "- U1 has 12 rows outside the empirical R+C comparator, while 139 R+C rows are outside U1.",
        "- U2+K+Q has 670 rows, including 12 rank-positive, 10 combat-nonzero, and 8 offensive rows.",
        "- U7 spans seven R/C/O cells and includes rank, combat, offensive, capability, quest, chat, and voice populations.",
        "- `s_ROLE_GRAPHIC` is populated on 257 rows: combat 27, offensive 34, capability 204, quest 200. It is not one role flag.",
        "- The case-insensitive ASCII token `monster` appears in 15 MOBS_TIP names, but only six have current MOBS rows; the joined six span U1/U2/U7/U8.",
        "- O/Apos is asymmetric: O0/Apos has 15 rows, O1/Apos 1645, and O1/A0 zero. Neither axis is proved attack admission.",
        "- The id 916 coarse tuple U7/R0/C0/T0/K0/Q0/drop0/O1 matches 21 IDs; lexical identity must not be generalized from that tuple.",
        "",
        "## Prior-reference and correction policy",
        "",
        "Existing `PF_ATTR_ROLE_DISCRIMINATOR.tsv` claims are not copied as new evidence. Applicable rows are referenced structurally by pinned artifact path, artifact SHA256, row id, row key, and claim digest.",
        "",
        "The id 916 correction includes `supersedes_artifact`, `supersedes_row_key`, `supersedes_claim_digest`, and `corrected_field=blocker`. Its authority precedence is field-scoped: the canonical report and authority index must cite this pair; no other prior field is superseded.",
        "",
        "## Rows",
        "",
        "| ID | Measurement | Status | Count |",
        "|---|---|---|---|",
    ])
    for row in rows:
        lines.append(
            "| `%s` | `%s` | `%s` | %s |"
            % (row["control_id"], row["measurement_label"], row["semantic_status"], row["measured_count"])
        )
    lines.extend([
        "",
        "## Nonclaims and next evidence",
        "",
        "These DATA controls do not decide talk versus attack, interaction admission, damage handling, death, loot issuance, or original-server policy. Those decisions require separately sourced client consumer or runtime evidence.",
        "",
        "Re-derive with `py -3 pf_rederive_monster_role_data_controls.py`; verify without writing with `--check`; run in-memory mutation guards with `--self-test`.",
        "",
    ])
    data = "\n".join(lines).encode("ascii")
    return data


def render_pair(tsv: bytes, md: bytes, metrics_hash: str) -> bytes:
    payload = {
        "format": PAIR_FORMAT,
        "publication_rule": "TSV and Markdown are valid together only when this last-written marker matches both hashes and sizes.",
        "metrics_sha256": metrics_hash,
        "row_count": EXPECTED_ROW_COUNT,
        "source_counts": {"DATA": EXPECTED_ROW_COUNT},
        "artifacts": {
            TSV_PATH.name: {"size": len(tsv), "sha256": sha256_bytes(tsv)},
            MD_PATH.name: {"size": len(md), "sha256": sha256_bytes(md)},
        },
        "pair_id": stable_key(
            "PF_MONSTER_ROLE_DATA_PAIR_V1", sha256_bytes(tsv), sha256_bytes(md), metrics_hash
        ),
    }
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("ascii")


@contextmanager
def exclusive_lock() -> Iterable[None]:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    fd = -1
    created = False
    try:
        try:
            fd = os.open(str(LOCK_PATH), flags, 0o600)
            created = True
        except FileExistsError as exc:
            raise VerificationError("publication_lock_exists") from exc
        except OSError as exc:
            raise VerificationError(
                "publication_lock_create_failed_errno_%s" % exc.errno
            ) from exc
        try:
            os.write(fd, ("pid=%d\n" % os.getpid()).encode("ascii"))
            os.fsync(fd)
            os.close(fd)
            fd = -1
        except OSError as exc:
            raise VerificationError(
                "publication_lock_initialize_failed_errno_%s" % exc.errno
            ) from exc
        yield
    finally:
        if fd >= 0:
            try:
                os.close(fd)
            except OSError:
                pass
        if created:
            try:
                LOCK_PATH.unlink()
            except FileNotFoundError:
                pass
            except OSError as exc:
                raise VerificationError(
                    "publication_lock_cleanup_failed_errno_%s" % exc.errno
                ) from exc


def publish(outputs: tuple[tuple[Path, bytes], ...]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for target, data in outputs:
            stage = target.with_name("." + target.name + "." + uuid.uuid4().hex + ".stage")
            with stage.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            staged.append((target, stage))
        # Marker is supplied last by the caller and is therefore the commit record.
        for target, stage in staged:
            os.replace(stage, target)
            with target.open("r+b") as handle:
                os.fsync(handle.fileno())
    finally:
        for _target, stage in staged:
            try:
                stage.unlink()
            except FileNotFoundError:
                pass


def check_outputs(outputs: tuple[tuple[Path, bytes], ...]) -> None:
    for path, expected in outputs:
        require(path.exists(), "missing_output_" + path.name)
        actual = path.read_bytes()
        require(actual == expected, "output_byte_mismatch_" + path.name)
    debris = list(HERE.glob(".PF_MONSTER_ROLE_DATA_CONTROLS*.stage"))
    require(not debris, "publication_stage_debris")


def self_test(
    metrics: dict[str, Any],
    rows: list[dict[str, str]],
    prior_rows: dict[str, dict[str, str]],
    raw_inputs: dict[Path, bytes],
) -> None:
    expected = expected_metrics()
    mutated_metrics = json.loads(json.dumps(metrics))
    mutated_metrics["links"]["W"]["zero_refs"] += 1
    require(mutated_metrics != expected, "selftest_metric_mutation_not_detected")

    mutated_raw = bytearray(raw_inputs[MOBS_PATH])
    mutated_raw[-1] ^= 1
    require(sha256_bytes(bytes(mutated_raw)) != INPUT_PINS[MOBS_PATH][1], "selftest_input_hash_mutation_not_detected")

    mutation_cases: list[list[dict[str, str]]] = []
    source_mutation = [dict(row) for row in rows]
    source_mutation[0]["source"] = "IMAGE"
    mutation_cases.append(source_mutation)
    ascii_mutation = [dict(row) for row in rows]
    ascii_mutation[0]["control"] += "\u0e01"
    mutation_cases.append(ascii_mutation)
    duplicate_key = [dict(row) for row in rows]
    duplicate_key[1]["evidence_key"] = duplicate_key[0]["evidence_key"]
    mutation_cases.append(duplicate_key)
    broken_reference = [dict(row) for row in rows]
    broken_reference[2]["prior_row_key"] = "0" * 64
    mutation_cases.append(broken_reference)
    broken_correction = [dict(row) for row in rows]
    index = EXPECTED_IDS.index("ID916_LEXICAL_TRAINING_CORRECTION")
    broken_correction[index]["corrected_field"] = "exact_observation"
    mutation_cases.append(broken_correction)
    for number, candidate in enumerate(mutation_cases, 1):
        try:
            validate_rows(candidate, prior_rows)
        except VerificationError:
            continue
        raise VerificationError("selftest_row_mutation_not_detected_%d" % number)


def derive() -> tuple[
    dict[Path, bytes], dict[str, Any], list[dict[str, str]], bytes, bytes, bytes,
    dict[str, dict[str, str]], str,
]:
    raw_inputs = {path: verify_input(path) for path in INPUT_PINS}
    verify_decoded_inputs(raw_inputs)
    tables: dict[Path, list[dict[str, str]]] = {}
    for path in EXPECTED_TABLE_SHAPES:
        _header, table_rows = parse_tsv(path, raw_inputs[path])
        tables[path] = table_rows
    _prior_header, prior_rows = parse_prior(raw_inputs[PRIOR_ROLE_PATH])
    metrics = compute_metrics(tables)
    expected = expected_metrics()
    require(metrics == expected, "metrics_fixed_census_mismatch_actual_" + metric_fingerprint(metrics))
    metrics_hash = metric_fingerprint(metrics)
    require(metrics_hash == EXPECTED_METRICS_SHA256, "metrics_hash_mismatch_actual_" + metrics_hash)
    rows = build_rows(metrics, prior_rows)
    validate_rows(rows, prior_rows)
    tsv = render_tsv(rows)
    md = render_md(rows, metrics, metrics_hash)
    pair = render_pair(tsv, md, metrics_hash)
    require(tsv.isascii() and md.isascii() and pair.isascii(), "non_ascii_rendered_output")
    return raw_inputs, metrics, rows, tsv, md, pair, prior_rows, metrics_hash


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="ascii", errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Re-derive DATA-only monster-role controls.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="Verify published bytes without writing.")
    modes.add_argument("--self-test", action="store_true", help="Run in-memory mutation guards without publishing.")
    args = parser.parse_args(argv)

    try:
        raw_inputs, metrics, rows, tsv, md, pair, prior_rows, metrics_hash = derive()
        outputs = ((TSV_PATH, tsv), (MD_PATH, md), (PAIR_PATH, pair))
        if args.self_test:
            self_test(metrics, rows, prior_rows, raw_inputs)
            success = "PASS self-test rows=%d source=DATA metrics=%s" % (
                len(rows), metrics_hash
            )
        elif args.check:
            check_outputs(outputs)
            success = "PASS check rows=%d source=DATA pair=%s" % (
                len(rows), json.loads(pair)["pair_id"]
            )
        else:
            with exclusive_lock():
                publish(outputs)
                check_outputs(outputs)
            success = "PASS publish rows=%d source=DATA pair=%s" % (
                len(rows), json.loads(pair)["pair_id"]
            )
        print(success)
        return 0
    except VerificationError as exc:
        print("FAIL " + str(exc))
        return 1
    except OSError as exc:
        print("FAIL os_error_errno_%s" % exc.errno)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
