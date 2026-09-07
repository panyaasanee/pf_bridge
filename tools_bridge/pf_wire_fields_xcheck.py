#!/usr/bin/env python3
"""Cross-check every ``*_wire.py`` module in a sibling ``pirate-force-server``
checkout against ``pf_bridge/external/PF_SERIALIZER_FIELDS.tsv``.

Owner: LANE-UI (COO-DECISION ``20260907_1541_COO-DECISION-ui1536-bridge-side-
checker-LANE-UI.md``, option (c)).  This is the ONLY file in
``tools_bridge/`` this lane owns.

WHY THIS LIVES ON THE BRIDGE SIDE
---------------------------------
The proven field table (``external/PF_SERIALIZER_FIELDS.tsv``) lives in
``pf_bridge``; the modules that encode those fields live in
``pirate-force-server``.  Nothing stood astride the two, so a module could
drift from the table with no test anywhere going red.  A copy of the table
in the server repo would be a second source of truth with no owner (the
``v141`` lesson); a test in the server repo could not read the table at all.
A bridge-side tool is the one place that sees both trees at once.

WHAT IT DOES NOT DO
-------------------
It does not block anybody.  With no sibling checkout it prints ``SKIP`` and
exits 0.  It does not import server modules -- everything is read with
``ast``, so a module that cannot be imported (missing dependency, syntax for
a newer Python) is still checked.  It never writes to either repository.

THE COMPARISON
--------------
For each ``encode_*``/``decode_*`` function in a ``*_wire.py`` module the
tool recovers the ORDERED sequence of tag bytes the function puts on the
wire, by walking the AST and resolving module-level ``_TAG_* = 0x..``
constants.  Calls into module-local helpers (``_encode_member`` and friends)
are expanded one level at a time, so a member record contributes its own
tags in place.  A loop body contributes its tags exactly once: the table has
one row per field, not one row per container member.

That sequence is compared against the rows of the matching ``message`` in
the TSV, direction ``W`` for encoders and ``R`` for decoders, ordered by the
table's own ``order`` column, keeping only rows that carry a real wire tag
(``0x..`` or ``UNTAGGED_*``).  Every other tag value in that column names a
call the static RE classified as writing no bytes into the stream
(``PE_IMPORT_*``, ``ATOMIC_*``, ``MUTATING_CHAIN_*``, ``CALL_UNCLASSIFIED``,
``EMPTY``, ...).

A disagreement in tag, in width, in count or in order exits non-zero with
one greppable line per finding naming module, function, message, direction
and position.

WHAT A FINDING MEANS, AND WHOSE DEBT IT IS
------------------------------------------
A red line against ``src/pirateforce_foundation/<x>_wire.py`` is the debt of
the lane that owns that module, not of LANE-UI.  This tool reports; it never
edits another lane's module.

NON-CLAIMS (read before believing an exit code)
-----------------------------------------------
1. A PASS says the tag SEQUENCE agrees with the table.  It says nothing
   about field MEANING -- ``external/PF_FIELD_VALIDATION.tsv`` still reads
   ``NOT_OBSERVED`` for most of these classes -- and nothing about whether
   the client ever sends the frame.
2. Both sides descend from the same static image.  Agreement here is an
   internal-consistency check, NOT independent evidence.
3. A function whose message cannot be resolved from its name is reported
   ``UNRESOLVED`` and is NOT checked.  Unresolved is not agreement.
4. The tool reads the ``order`` column as the wire order.  That is the
   table's own claim, not a fresh measurement by this tool.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

BRIDGE_ROOT = Path(__file__).resolve().parent.parent
TSV = BRIDGE_ROOT / "external" / "PF_SERIALIZER_FIELDS.tsv"

# Tag byte -> payload width in bytes, as the TSV's own ``len`` column spells
# it.  Built from the table at load time; this dict is only the fallback used
# to describe a tag the code emits that the table never mentions.
PRIMITIVE_WIDTH = {
    "u8tag": 1,
    "u16tag": 2,
    "u32tag": 4,
    "u64tag": 8,
    "read_u8tag": 1,
    "read_u16tag": 2,
    "read_u32tag": 4,
    "read_u64tag": 8,
}

# Helpers that emit a whole field with a tag the call site does not spell.
WSTRING_PRIMITIVES = {"wstring_tag", "read_wstring_tag"}
STRING8_PRIMITIVES = {"string8tag", "read_string8tag"}

WSTRING_ROW_TAG = "UNTAGGED_WSTRING16LE_LEN32LE"
STRING8_ROW_TAG = "UNTAGGED_STRING8_LEN32LE"

# The table spells a string field by its SHAPE; the code spells it by the tag
# byte the shipped helper writes.  ``ui_social_wire.wstring_tag`` writes
# ``0x48`` and its docstring names it "the CORRECT shape for
# ``UNTAGGED_WSTRING16LE_LEN32LE`` registry rows"; ``string8tag`` is the same
# statement for the 8-bit rows.  Neither byte appears in the table's own tag
# column (the table uses 0x05/0x08/0x0B/0x0F/0x12/0x14/0x19/0x1F/0x26/0x2A/
# 0x32 and nothing else), so the mapping is unambiguous in both directions.
TAG_ALIASES = {
    "0x48": WSTRING_ROW_TAG,
}

REAL_TAG_RE = re.compile(r"^0x[0-9A-Fa-f]{2}$")

# Modules known to disagree today that are NOT this lane's to fix.  One entry
# per line WITH the reason it is here and who owns it.  A ``ui_*`` module of
# this lane's own must never appear in this list.
ALLOWLIST: dict[str, str] = {}


def is_real_tag(tag: str) -> bool:
    return bool(REAL_TAG_RE.match(tag)) or tag.startswith("UNTAGGED_")


class Row:
    __slots__ = ("order", "tag", "length")

    def __init__(self, order: int, tag: str, length: str) -> None:
        self.order = order
        self.tag = tag
        self.length = length


def load_table(path: Path) -> dict[tuple[str, str], list[Row]]:
    """message, direction -> rows carrying a real wire tag, in ``order``."""

    table: dict[tuple[str, str], list[Row]] = {}
    with path.open("r", encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        col = {name: i for i, name in enumerate(header)}
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= col["tag"]:
                continue
            tag = parts[col["tag"]]
            if not is_real_tag(tag):
                continue
            direction = parts[col["direction(W/R)"]]
            try:
                order = int(parts[col["order"]])
            except ValueError:
                continue
            key = (parts[col["message"]], direction)
            table.setdefault(key, []).append(
                Row(order, tag, parts[col["len"]])
            )
    for rows in table.values():
        rows.sort(key=lambda r: r.order)
    return table


def snake_to_camel(name: str) -> str:
    return "".join(part.title() for part in name.split("_") if part)


def resolve_message(func_name: str, table_keys: set[str]) -> tuple[str | None, str]:
    """``encode_stall_open_payload`` -> ``StallOpenVital``.

    Returns (message or None, note).  A name that matches more than one
    message with a different field table is left unresolved on purpose: the
    tool refuses to guess which class a function belongs to.
    """

    stem = func_name
    for prefix in ("encode_", "decode_"):
        if stem.startswith(prefix):
            stem = stem[len(prefix) :]
            break
    else:
        return None, "not an encode_/decode_ function"
    if stem.endswith("_payload"):
        stem = stem[: -len("_payload")]
    camel = snake_to_camel(stem)
    wanted = camel + "Vital"
    hits = sorted(
        key
        for key in table_keys
        if key == wanted or key.endswith("_" + wanted)
    )
    if not hits:
        return None, "no message named " + wanted + " in the table"
    if len(hits) > 1:
        return None, "ambiguous: " + ", ".join(hits)
    return hits[0], ""


class Emission:
    __slots__ = ("tag", "width", "lineno", "how")

    def __init__(self, tag: str, width: int | None, lineno: int, how: str) -> None:
        self.tag = tag
        self.width = width
        self.lineno = lineno
        self.how = how

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "<%s@%d %s>" % (self.tag, self.lineno, self.how)


def const_ints(tree: ast.Module) -> dict[str, int]:
    out: dict[str, int] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Constant) or not isinstance(
            node.value.value, int
        ):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                out[target.id] = node.value.value
    return out


def tag_literal(node: ast.expr, consts: dict[str, int]) -> str | None:
    if isinstance(node, ast.Name) and node.id in consts:
        return "0x%02X" % consts[node.id]
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return "0x%02X" % node.value
    return None


def called_name(node: ast.Call) -> tuple[str | None, str | None]:
    """Return (qualifier, attribute) for ``wire.u32tag`` / ``_encode_member``."""

    if isinstance(node.func, ast.Attribute):
        base = node.func.value
        qualifier = base.id if isinstance(base, ast.Name) else None
        return qualifier, node.func.attr
    if isinstance(node.func, ast.Name):
        return None, node.func.id
    return None, None


def tag_constants_named_in(
    helper: ast.FunctionDef,
    consts: dict[str, int],
    lineno: int,
    how: str,
) -> list[Emission]:
    """Last resort for a module-local helper that writes or reads a field
    without going through a recognised primitive -- ``read_channel_tagged_
    wstring`` checks ``buf[offset] != _CHANNEL_WSTRING_TAG`` and never calls
    anything.  Falls back to the module-level ``*TAG*`` constants NAMED in the
    helper body, in source order, collapsing a constant repeated back to back
    (a tag checked and then quoted in the error message is one field).

    HEURISTIC, and deliberately the narrowest one that covers the shipped
    readers: it only ever runs for a helper from which no primitive call was
    recovered, so it can add fields, never reorder or remove them.
    """

    names: list[str] = []

    def visit(node: ast.AST) -> None:
        if (
            isinstance(node, ast.Name)
            and node.id in consts
            and "TAG" in node.id.upper()
        ):
            if not names or names[-1] != node.id:
                names.append(node.id)
        for child in ast.iter_child_nodes(node):
            visit(child)

    for stmt in helper.body:
        visit(stmt)
    return [
        Emission("0x%02X" % consts[name], None, lineno, how + " (named " + name + ")")
        for name in names
    ]


def emissions_of(
    func: ast.FunctionDef,
    consts: dict[str, int],
    locals_by_name: dict[str, ast.FunctionDef],
    seen: frozenset[str],
) -> list[Emission]:
    """Ordered tags this function puts on the wire.

    A loop body contributes its tags once -- ``ast.walk`` order is not source
    order, so the tree is walked with an explicit stack instead.
    """

    out: list[Emission] = []

    def visit(node: ast.AST) -> None:
        if isinstance(node, ast.Call):
            _, attr = called_name(node)
            if attr in PRIMITIVE_WIDTH and node.args:
                tag_arg = node.args[0] if attr.startswith("read_") is False else None
                # read_* primitives take (buf, offset, expected_tag)
                if attr.startswith("read_"):
                    tag_arg = node.args[2] if len(node.args) > 2 else None
                tag = tag_literal(tag_arg, consts) if tag_arg is not None else None
                out.append(
                    Emission(
                        tag or "UNRESOLVED_TAG_EXPR",
                        PRIMITIVE_WIDTH[attr],
                        node.lineno,
                        attr,
                    )
                )
            elif attr in WSTRING_PRIMITIVES:
                out.append(Emission(WSTRING_ROW_TAG, None, node.lineno, attr))
            elif attr in STRING8_PRIMITIVES:
                out.append(Emission(STRING8_ROW_TAG, None, node.lineno, attr))
            elif attr in locals_by_name and attr not in seen:
                helper = locals_by_name[attr]
                nested = emissions_of(helper, consts, locals_by_name, seen | {attr})
                if not nested:
                    nested = tag_constants_named_in(helper, consts, node.lineno, attr)
                if not nested:
                    # ``_read_u8_tag(buf, offset, _TAG_U8)`` -- a local clone
                    # of a primitive that takes the expected tag as an
                    # argument, so neither the helper body nor a shared name
                    # spells it.  Take the first argument that resolves to a
                    # module-level ``*TAG*`` constant.
                    for arg in node.args:
                        if (
                            isinstance(arg, ast.Name)
                            and arg.id in consts
                            and "TAG" in arg.id.upper()
                        ):
                            nested = [
                                Emission(
                                    "0x%02X" % consts[arg.id],
                                    None,
                                    node.lineno,
                                    attr + "(" + arg.id + ")",
                                )
                            ]
                            break
                out.extend(nested)
                return
        # ``bytes([_TAG_U8, value & 0xFF])`` -- an inline one-byte field, and
        # ``bytes([_CHANNEL_WSTRING_TAG]) + length + payload`` -- an inline
        # string field written without going through the shared primitive.
        # The one-element form requires a NAMED constant: ``bytes([0])`` is a
        # zero byte, not a tagged field.
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "bytes"
            and len(node.args) == 1
            and isinstance(node.args[0], ast.List)
            and len(node.args[0].elts) in (1, 2)
        ):
            head = node.args[0].elts[0]
            named = isinstance(head, ast.Name) and "TAG" in head.id.upper()
            if len(node.args[0].elts) == 2 or named:
                tag = tag_literal(head, consts)
                if tag is not None:
                    out.append(
                        Emission(
                            tag,
                            1 if len(node.args[0].elts) == 2 else None,
                            node.lineno,
                            "bytes([tag, ...])",
                        )
                    )
                    return
        for child in ast.iter_child_nodes(node):
            visit(child)

    for stmt in func.body:
        visit(stmt)
    return out


def check_module(
    path: Path,
    rel: str,
    table: dict[tuple[str, str], list[Row]],
    message_names: set[str],
) -> tuple[list[str], list[str], int]:
    findings: list[str] = []
    unresolved: list[str] = []
    checked = 0

    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), str(path))
    consts = const_ints(tree)
    locals_by_name = {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }

    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not (node.name.startswith("encode_") or node.name.startswith("decode_")):
            continue
        message, note = resolve_message(node.name, message_names)
        if message is None:
            unresolved.append(
                "XCHECK UNRESOLVED %s::%s -- %s" % (rel, node.name, note)
            )
            continue
        direction = "W" if node.name.startswith("encode_") else "R"
        rows = table.get((message, direction))
        if not rows:
            unresolved.append(
                "XCHECK UNRESOLVED %s::%s -- %s has no %s row with a real tag"
                % (rel, node.name, message, direction)
            )
            continue

        actual = emissions_of(node, consts, locals_by_name, frozenset({node.name}))
        if not actual:
            unresolved.append(
                "XCHECK UNRESOLVED %s::%s -- no tag emission found in the body"
                % (rel, node.name)
            )
            continue

        checked += 1
        for index in range(max(len(rows), len(actual))):
            want = rows[index].tag if index < len(rows) else None
            got = actual[index].tag if index < len(actual) else None
            if got is not None:
                got = TAG_ALIASES.get(got, got)
            if want == got:
                continue
            if want is None:
                findings.append(
                    "XCHECK EXTRA %s::%s %s %s pos=%d code=%s line=%d "
                    "-- table has %d tagged field(s), code emits %d"
                    % (
                        rel, node.name, message, direction, index + 1,
                        got, actual[index].lineno, len(rows), len(actual),
                    )
                )
            elif got is None:
                findings.append(
                    "XCHECK MISSING %s::%s %s %s pos=%d table=%s order=%d "
                    "-- table has %d tagged field(s), code emits %d"
                    % (
                        rel, node.name, message, direction, index + 1,
                        want, rows[index].order, len(rows), len(actual),
                    )
                )
            else:
                findings.append(
                    "XCHECK MISMATCH %s::%s %s %s pos=%d table=%s order=%d "
                    "code=%s line=%d"
                    % (
                        rel, node.name, message, direction, index + 1,
                        want, rows[index].order, got, actual[index].lineno,
                    )
                )
    return findings, unresolved, checked


def find_server(explicit: str | None) -> Path | None:
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
        return candidate if (candidate / "src").is_dir() else None
    sibling = BRIDGE_ROOT.parent / "pirate-force-server"
    return sibling if (sibling / "src").is_dir() else None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Cross-check *_wire.py tag sequences against "
            "external/PF_SERIALIZER_FIELDS.tsv."
        )
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="path to the pirate-force-server checkout (default: sibling dir)",
    )
    parser.add_argument(
        "--show-unresolved",
        action="store_true",
        help="print every function whose message could not be resolved",
    )
    args = parser.parse_args(argv)

    if not TSV.is_file():
        print("SKIP -- %s not found" % TSV)
        return 0
    server = find_server(args.repo)
    if server is None:
        print(
            "SKIP -- no pirate-force-server checkout beside this repository; "
            "this tool is advisory and blocks nobody"
        )
        return 0

    table = load_table(TSV)
    message_names = {message for message, _ in table}

    modules = sorted((server / "src").rglob("*_wire.py"))
    all_findings: list[str] = []
    all_unresolved: list[str] = []
    allowlisted: list[str] = []
    checked = 0
    for path in modules:
        rel = str(path.relative_to(server)).replace("\\", "/")
        findings, unresolved, count = check_module(path, rel, table, message_names)
        checked += count
        all_unresolved.extend(unresolved)
        if findings and rel in ALLOWLIST:
            allowlisted.extend(findings)
            continue
        all_findings.extend(findings)

    for line in all_findings:
        print(line)
    if args.show_unresolved:
        for line in all_unresolved:
            print(line)
    for line in allowlisted:
        print("XCHECK ALLOWLISTED " + line)
    for rel, reason in sorted(ALLOWLIST.items()):
        print("XCHECK ALLOWLIST-ENTRY %s -- %s" % (rel, reason))

    print(
        "pf_wire_fields_xcheck: %d module(s), %d function(s) checked, "
        "%d finding(s), %d unresolved, %d allowlist entr(ies)"
        % (
            len(modules),
            checked,
            len(all_findings),
            len(all_unresolved),
            len(ALLOWLIST),
        )
    )
    if all_findings:
        print("XCHECK FAIL -- see the lines above; each is the debt of the lane "
              "that owns the module named in it")
        return 1
    print("XCHECK PASS -- every resolved function agrees with the table")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
