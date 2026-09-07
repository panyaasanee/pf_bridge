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

Exactly four things are compared, and each has its own line prefix:

``XCHECK MISMATCH``  position i holds a different tag on each side (tag,
                     and therefore also order -- a swap shows up as two
                     mismatched positions).
``XCHECK MISSING``   the table has a tagged field at position i and the code
                     emits nothing there (count).
``XCHECK EXTRA``     the code emits at position i and the table has no row
                     there (count).
``XCHECK WIDTH``     same tag on both sides, different payload width.  Only
                     compared when BOTH sides are known: the table's ``len``
                     column is a plain integer AND the emission came from a
                     fixed-width primitive.  ``4+N_bytes`` (every string
                     row) and a variable-width helper are silent, not
                     agreeing.  ``N/A`` and ``0`` sit only on rows
                     ``is_real_tag`` already dropped, so they never arrive.

Any of the four exits non-zero with one greppable line per finding naming
module, function, message, direction and position.

WHAT HAPPENS WHEN THIS TOOL DOES NOT UNDERSTAND THE CODE
--------------------------------------------------------
It says so, and the function is counted as ``UNRESOLVED`` -- it is never
compared, and it never contributes to a PASS.  There is no fallback that
fills in a field the code does not demonstrably emit.  Until 2026-09-07 there
were two (a helper's fields guessed from the ``*TAG*`` constants its body
happened to name, and from the arguments at its call site); both could only
ADD emissions, so both turned "this tool cannot see" into "PASS", and on this
tree they were buying agreement for six functions.  COO-DECISION
``20260907_1744``: an honest red is worth more than a green that was bought.
The ``UNRESOLVED`` lines carry a machine-greppable reason:

``NO-ROW``                 the table has no row for that message+direction.
``ROWS-BUT-NO-WIRE-TAG``   the table HAS rows for it and every one of them
                           carries a non-wire tag (``AppraisalStopVital`` is
                           two ``EMPTY`` rows).  This is a different fact
                           from ``NO-ROW`` and used to be reported as it.
``OPAQUE-BODY``            a module-local helper, a recursive helper, or a
                           tag expression this tool cannot resolve.
``NO-EMISSION``            the body yielded no tag at all.

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
5. Only MODULE-LOCAL helpers are expanded.  A call into a helper defined in
   another module is invisible: it contributes no emission and raises no
   ``OPAQUE-BODY``.  This is common, not hypothetical -- 78 of the 151
   compared functions call ``require_exhausted``, which lives in
   ``ui_social_wire.py``, and the tool assumes every such call writes nothing.
   ``require_exhausted`` happens to write nothing; the tool cannot know that,
   and it would make the same assumption about a helper that writes a field.
   A hole, not a proof.
6. The comparison is over the tag COLUMN.  Two fields that carry the same tag
   byte can swap places with nothing to see: ``StallOpenVital`` W really does
   have three ``0x0F`` rows.  ``--self-test``'s reorder mutant does not cover
   that shape.
7. There is no notion of reachability.  A field written under ``if False:`` or
   under a runtime flag is credited as emitted.
8. ``is_real_tag`` keeps 3191 of the table's 6931 data rows.  A PASS is
   agreement with the rows this tool deems wire-bearing, not with the table.
9. ``--self-test`` measures this tool against mutants of a real module.  It
   says nothing about whether the table is right, and every mutant in the
   bank is by construction a shape this tool can already express -- so
   ``SELFTEST PASS`` is not evidence about the shapes listed in 5-7.
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

# Per-module count of functions this tool actually COMPARED, measured on
# 2026-09-07 (round ``0bzq9y``).  Regenerate with ``--emit-pin``.
#
# WHY THIS EXISTS: without it the tool has three outcomes and only one of them
# is visible.  A finding is red.  An ``UNRESOLVED`` is green-and-printed.  A
# function that silently leaves the tool's universe -- ``def`` turned
# ``async def``, a module renamed off ``*_wire.py``, an annotation added to a
# tag constant -- was green and printed NOWHERE, and ``XCHECK PASS -- every
# resolved function agrees with the table`` was still the last line.  Deleting
# one character from the module glob took the compared set to zero and printed
# a PASS.  This pin makes "this tool now understands LESS of the tree than it
# did" a red, per module, so the line names who lost what.
#
# A DELIBERATE drop (a module removed, a function renamed on purpose) is closed
# by regenerating the pin in the same commit that earns it -- not by deleting
# the pin.
COVERAGE_PIN: dict[str, int] = {
    "src/pirateforce_foundation/actor_wire.py": 0,
    "src/pirateforce_foundation/gm/activity_cheat_code_wire.py": 0,
    "src/pirateforce_foundation/gm/attr_wire.py": 0,
    "src/pirateforce_foundation/gm/cheat_wire.py": 0,
    "src/pirateforce_foundation/gm/command_wire.py": 0,
    "src/pirateforce_foundation/gm/forbid_to_talk_wire.py": 0,
    "src/pirateforce_foundation/gm/say_wire.py": 0,
    "src/pirateforce_foundation/gm/speed_wire.py": 0,
    "src/pirateforce_foundation/gm/state_wire.py": 0,
    "src/pirateforce_foundation/gm/teleport_wire.py": 0,
    "src/pirateforce_foundation/npc_wire.py": 0,
    "src/pirateforce_foundation/player_wire.py": 0,
    "src/pirateforce_foundation/ui_activity_wire.py": 14,
    "src/pirateforce_foundation/ui_buildingcrystal_wire.py": 20,
    "src/pirateforce_foundation/ui_channel_wire.py": 9,
    "src/pirateforce_foundation/ui_collectionobj_wire.py": 8,
    "src/pirateforce_foundation/ui_community_social_wire.py": 32,
    "src/pirateforce_foundation/ui_dyeing_appraisal_relive_wire.py": 6,
    "src/pirateforce_foundation/ui_express_wire.py": 6,
    "src/pirateforce_foundation/ui_friend_wire.py": 4,
    "src/pirateforce_foundation/ui_gathering_wire.py": 4,
    "src/pirateforce_foundation/ui_mail_wire.py": 6,
    "src/pirateforce_foundation/ui_party_wire.py": 4,
    "src/pirateforce_foundation/ui_pets_wire.py": 20,
    "src/pirateforce_foundation/ui_social_wire.py": 0,
    "src/pirateforce_foundation/ui_stall_wire.py": 6,
    "src/pirateforce_foundation/ui_tracepath_wire.py": 0,
    "src/pirateforce_foundation/ui_trade_wire.py": 2,
    "src/pirateforce_foundation/ui_treasurehunt_wire.py": 4,
    "src/pirateforce_foundation/ui_winemaking_wire.py": 6,
}


def is_real_tag(tag: str) -> bool:
    return bool(REAL_TAG_RE.match(tag)) or tag.startswith("UNTAGGED_")


class Row:
    __slots__ = ("order", "tag", "length")

    def __init__(self, order: int, tag: str, length: str) -> None:
        self.order = order
        self.tag = tag
        self.length = length


def load_table(path: Path) -> tuple[
    dict[tuple[str, str], list[Row]], dict[tuple[str, str], list[str]]
]:
    """Return (tagged, present).

    ``tagged``  -- (message, direction) -> rows carrying a real wire tag, in
                   ``order``.  These are the rows the comparison uses.
    ``present`` -- (message, direction) -> the tag value of EVERY row in the
                   table, tagged or not.

    Two distinct facts are needed downstream and they used to be conflated
    (COO-DECISION ``20260907_1744``): a message the table never mentions is
    not the same thing as a message the table DOES carry rows for whose every
    row is a non-wire tag (``EMPTY``, ``PE_IMPORT_*``, ...).  ``AppraisalStop
    Vital`` is the second kind, and reporting it as the first is a false
    verdict about the table.
    """

    tagged: dict[tuple[str, str], list[Row]] = {}
    present: dict[tuple[str, str], list[str]] = {}
    with path.open("r", encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        col = {name: i for i, name in enumerate(header)}
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= col["tag"]:
                continue
            tag = parts[col["tag"]]
            direction = parts[col["direction(W/R)"]]
            key = (parts[col["message"]], direction)
            present.setdefault(key, []).append(tag)
            if not is_real_tag(tag):
                continue
            try:
                order = int(parts[col["order"]])
            except ValueError:
                continue
            tagged.setdefault(key, []).append(
                Row(order, tag, parts[col["len"]])
            )
    for rows in tagged.values():
        rows.sort(key=lambda r: r.order)
    return tagged, present


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
        # ``_TAG_U32 = 0x14`` and ``_TAG_U32: int = 0x14`` are the same
        # constant.  Reading only the first shape meant one added annotation
        # dropped every field of six functions with the run still green.
        if isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value = node.value
        elif isinstance(node, ast.Assign):
            targets = node.targets
            value = node.value
        else:
            continue
        if not isinstance(value, ast.Constant) or not isinstance(value.value, int):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                out[target.id] = value.value
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


def emissions_of(
    func: ast.FunctionDef,
    consts: dict[str, int],
    locals_by_name: dict[str, ast.FunctionDef],
    seen: frozenset[str],
    opaque: list[str],
) -> list[Emission]:
    """Ordered tags this function puts on the wire.

    A loop body contributes its tags once -- ``ast.walk`` order is not source
    order, so the tree is walked with an explicit stack instead.

    ``opaque`` collects, in source order, every place where this tool did not
    understand what the code does.  A non-empty ``opaque`` means the recovered
    sequence is INCOMPLETE, so the caller must report the function
    ``UNRESOLVED`` instead of comparing it.  Nothing in here may invent an
    emission the code does not demonstrably make (COO-DECISION
    ``20260907_1744``: a fallback that fills in a field the code never wrote is
    the mechanism that manufactures a green run).
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
                if tag is None:
                    opaque.append(
                        "%s() at line %d is passed a tag expression this tool "
                        "cannot resolve to a module-level constant"
                        % (attr, node.lineno)
                    )
                else:
                    out.append(
                        Emission(
                            tag,
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
                nested = emissions_of(
                    helper, consts, locals_by_name, seen | {attr}, opaque
                )
                if not nested:
                    # The helper writes or reads SOMETHING -- it is called from
                    # an encoder/decoder body -- but no recognised primitive
                    # was recovered from it.  Guessing its fields from the
                    # ``*TAG*`` constants its body happens to name, or from the
                    # arguments of the call, is what this round removed: both
                    # could only ADD fields, so they turned "this tool cannot
                    # see" into "PASS".
                    opaque.append(
                        "module-local helper %s() called at line %d emits no "
                        "tag this tool can recover" % (attr, node.lineno)
                    )
                out.extend(nested)
                return
            elif attr in locals_by_name:
                # Recursive call: the guard stops the recursion, and stopping
                # silently would drop whatever the second level writes.
                opaque.append(
                    "module-local helper %s() recurses at line %d and is not "
                    "expanded a second time" % (attr, node.lineno)
                )
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
    present: dict[tuple[str, str], list[str]],
    message_names: set[str],
) -> tuple[list[str], list[str], int]:
    findings: list[str] = []
    unresolved: list[str] = []
    checked = 0

    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), str(path))
    consts = const_ints(tree)
    locals_by_name = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
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
            every = present.get((message, direction))
            if not every:
                unresolved.append(
                    "XCHECK UNRESOLVED %s::%s -- NO-ROW: %s has no %s row in "
                    "the table at all" % (rel, node.name, message, direction)
                )
            else:
                kinds = ", ".join(sorted(set(every)))
                unresolved.append(
                    "XCHECK UNRESOLVED %s::%s -- ROWS-BUT-NO-WIRE-TAG: %s has "
                    "%d %s row(s) in the table, none carrying a wire tag "
                    "(tag values present: %s)"
                    % (rel, node.name, message, len(every), direction, kinds)
                )
            continue

        opaque: list[str] = []
        actual = emissions_of(
            node, consts, locals_by_name, frozenset({node.name}), opaque
        )
        if opaque:
            unresolved.append(
                "XCHECK UNRESOLVED %s::%s -- OPAQUE-BODY: %s"
                % (rel, node.name, "; ".join(opaque))
            )
            continue
        if not actual:
            unresolved.append(
                "XCHECK UNRESOLVED %s::%s -- NO-EMISSION: no tag emission "
                "found in the body" % (rel, node.name)
            )
            continue

        checked += 1
        for index in range(max(len(rows), len(actual))):
            want = rows[index].tag if index < len(rows) else None
            got = actual[index].tag if index < len(actual) else None
            if got is not None and index < len(actual):
                # The alias translates the SHAPE the table spells into the byte
                # the shipped string helper writes.  Applied blindly it also
                # runs backwards: ``u8tag(0x48, x)`` -- one tagged byte -- would
                # be rewritten into ``UNTAGGED_WSTRING16LE_LEN32LE`` and match a
                # length-prefixed UTF-16LE row, with the width check silent
                # because that row's ``len`` is ``4+N_bytes``.  A fixed-width
                # primitive has a known width; a string helper does not.  Only
                # the second may be aliased.
                if actual[index].width is None:
                    got = TAG_ALIASES.get(got, got)
            if want == got:
                # Same tag, different payload width.  ``Row.length`` is the
                # table's ``len`` column; ``Emission.width`` is known only for
                # the fixed-width primitives (u8/u16/u32/u64 tag) and for an
                # inline ``bytes([tag, value])``.  Both sides must be known
                # before this says anything -- an unknown width is not a
                # disagreement.
                if index < len(actual):
                    table_len = rows[index].length
                    code_width = actual[index].width
                    if (
                        code_width is not None
                        and table_len.isdigit()
                        and int(table_len) != code_width
                    ):
                        findings.append(
                            "XCHECK WIDTH %s::%s %s %s pos=%d tag=%s "
                            "table_len=%s code_width=%d line=%d"
                            % (
                                rel, node.name, message, direction, index + 1,
                                want, table_len, code_width,
                                actual[index].lineno,
                            )
                        )
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


# ---------------------------------------------------------------------------
# --self-test: this tool, measured against mutants of REAL modules
# ---------------------------------------------------------------------------
# COO-DECISION ``20260907_1744``: the mutant bank lives inside the tool, not in
# a new test file with a new owner.  Six mutants, and the fifth is the one that
# matters -- a module this tool cannot see through must come out as a COUNTED
# ``UNRESOLVED``, never as a ``PASS``.
#
# Subjects are chosen from the real tree, never synthesised, and deliberately
# from more than one module: this lane has twice shipped a fixture monoculture
# (every synthetic file named ``ui_*``, short, single-name, single-file) and
# twice had it found for it.  A subject must already agree with the table, or
# a surviving mutant would be unattributable.

MUTANTS = (
    "reorder",
    "retag",
    "drop-field",
    "add-field",
    "opaque-helper",
    "narrow-width",
    "alias-launder",
)

OPAQUE_HELPER_NAME = "_pfxc_selftest_opaque"


def _stmt_emissions(
    stmt: ast.stmt,
    consts: dict[str, int],
    locals_by_name: dict[str, ast.FunctionDef],
) -> tuple[tuple[str, ...], bool]:
    """(tags this single statement emits, whether it was fully understood)."""

    holder = ast.FunctionDef(
        name="_pfxc_probe",
        args=ast.arguments(
            posonlyargs=[], args=[], vararg=None, kwonlyargs=[],
            kw_defaults=[], kwarg=None, defaults=[],
        ),
        body=[stmt],
        decorator_list=[],
        returns=None,
        type_comment=None,
    )
    if hasattr(ast, "TypeAlias"):  # py3.12+ carries type_params
        holder.type_params = []
    opaque: list[str] = []
    got = emissions_of(
        holder, consts, locals_by_name, frozenset({"_pfxc_probe"}), opaque
    )
    return tuple(e.tag for e in got), not opaque


class Subject:
    """One real encoder/decoder this self-test mutates."""

    __slots__ = (
        "rel", "tree", "func", "consts", "locals_by_name", "positions",
        "baseline_checked",
    )

    def __init__(
        self, rel, tree, func, consts, locals_by_name, positions,
        baseline_checked,
    ):
        self.rel = rel
        self.tree = tree
        self.func = func
        self.consts = consts
        self.locals_by_name = locals_by_name
        self.positions = positions  # [(stmt index, tags emitted)]
        self.baseline_checked = baseline_checked


def _pick_subjects(
    server: Path,
    table: dict[tuple[str, str], list[Row]],
    present: dict[tuple[str, str], list[str]],
    message_names: set[str],
    wanted: int = 5,
) -> list[Subject]:
    """One candidate per module, then a deliberately UNLIKE set of them.

    Taking the first ``wanted`` in path order hands back three ``ui_*`` files
    in the same flat directory -- the fixture monoculture this lane has been
    caught with twice.  So candidates are scored for unlikeness (subpackage
    vs top level, ``ui_`` prefix vs not, encoder vs decoder) and the set is
    grown greedily from the ones that share the fewest traits.
    """

    candidates: list[Subject] = []
    for path in sorted((server / "src").rglob("*_wire.py")):
        rel = str(path.relative_to(server)).replace("\\", "/")
        findings, _unresolved, module_checked = check_module(
            path, rel, table, present, message_names
        )
        if findings:
            continue  # a subject must already agree, or a mutant is deniable
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), str(path))
        consts = const_ints(tree)
        locals_by_name = {
            n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)
        }
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if not (
                node.name.startswith("encode_") or node.name.startswith("decode_")
            ):
                continue
            message, _note = resolve_message(node.name, message_names)
            if message is None:
                continue
            direction = "W" if node.name.startswith("encode_") else "R"
            rows = table.get((message, direction))
            if not rows or len(rows) < 3:
                continue
            opaque: list[str] = []
            emitted = emissions_of(
                node, consts, locals_by_name, frozenset({node.name}), opaque
            )
            if opaque or len(emitted) < 3:
                continue
            positions = []
            for index, stmt in enumerate(node.body):
                tags, clean = _stmt_emissions(stmt, consts, locals_by_name)
                if tags and clean:
                    positions.append((index, tags))
            if len({tags for _i, tags in positions}) < 2:
                continue  # cannot build a reorder that changes the sequence
            candidates.append(
                Subject(
                    rel, tree, node, consts, locals_by_name, positions,
                    module_checked,
                )
            )
            break
    return _spread(candidates, wanted)


def _traits(subject: Subject) -> tuple[str, ...]:
    name = subject.rel.rsplit("/", 1)[-1]
    return (
        "dir=" + subject.rel.rsplit("/", 1)[0],
        "prefix=" + ("ui_" if name.startswith("ui_") else "other"),
        "dir_depth=%d" % subject.rel.count("/"),
        "kind=" + ("encode" if subject.func.name.startswith("encode_") else "decode"),
        "width_known=%s"
        % bool(_first_primitive_call(subject.func, subject.consts, True)),
    )


def _spread(candidates: list[Subject], wanted: int) -> list[Subject]:
    chosen: list[Subject] = []
    pool = list(candidates)
    while pool and len(chosen) < wanted:
        taken = [t for c in chosen for t in _traits(c)]
        pool.sort(key=lambda c: sum(t in taken for t in _traits(c)))
        chosen.append(pool.pop(0))
    return chosen


def _mutate(subject: Subject, kind: str) -> ast.Module | None:
    """A deep copy of the subject's module with one mutation applied."""

    import copy

    tree = copy.deepcopy(subject.tree)
    func = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == subject.func.name
    )
    first = subject.positions[0][0]
    other = next(
        (i for i, tags in subject.positions if tags != subject.positions[0][1]),
        None,
    )
    last = subject.positions[-1][0]

    if kind == "reorder":
        if other is None:
            return None
        func.body[first], func.body[other] = func.body[other], func.body[first]
    elif kind == "drop-field":
        del func.body[last]
    elif kind == "add-field":
        func.body.insert(first + 1, copy.deepcopy(func.body[first]))
    elif kind == "retag":
        call = _first_primitive_call(func, subject.consts)
        if call is None:
            return None
        node, arg_index = call
        node.args[arg_index] = ast.Constant(value=0x7F)
    elif kind == "narrow-width":
        call = _first_primitive_call(func, subject.consts, fixed_width_only=True)
        if call is None:
            return None
        node, _arg_index = call
        name = node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id
        swapped = {"u32tag": "u16tag", "u16tag": "u32tag",
                   "u64tag": "u32tag", "u8tag": "u16tag"}
        swapped.update({"read_" + k: "read_" + v for k, v in list(swapped.items())})
        if name not in swapped:
            return None
        if isinstance(node.func, ast.Attribute):
            node.func.attr = swapped[name]
        else:
            node.func.id = swapped[name]
    elif kind == "alias-launder":
        # The one mutant that produced a byte-identical PASS after D1/D2/D3:
        # a length-prefixed UTF-16LE string rewritten as the single tagged
        # byte TAG_ALIASES translates, with the width check silent because
        # that row's ``len`` is ``4+N_bytes``.
        call = _first_string_primitive_call(func)
        if call is None:
            return None
        if isinstance(call.func, ast.Attribute):
            call.func.attr = "u8tag"
        else:
            call.func.id = "u8tag"
        call.args.insert(0, ast.Constant(value=0x48))
    elif kind == "opaque-helper":
        helper = ast.parse(
            "def %s(buf, offset):\n"
            "    while offset < len(buf):\n"
            "        offset += 1\n"
            "    return offset\n" % OPAQUE_HELPER_NAME
        ).body[0]
        tree.body.insert(0, helper)
        func.body.insert(
            first,
            ast.parse("%s(b'', 0)" % OPAQUE_HELPER_NAME).body[0],
        )
    else:  # pragma: no cover - guarded by MUTANTS
        raise ValueError(kind)
    return ast.fix_missing_locations(tree)


def _first_string_primitive_call(func: ast.FunctionDef) -> ast.Call | None:
    for node in ast.walk(func):
        if isinstance(node, ast.Call):
            _q, attr = called_name(node)
            if attr in WSTRING_PRIMITIVES:
                return node
    return None


def _first_primitive_call(
    func: ast.FunctionDef,
    consts: dict[str, int],
    fixed_width_only: bool = False,
) -> tuple[ast.Call, int] | None:
    """First recognised primitive call, and which argument holds its tag."""

    for node in ast.walk(func):
        if not isinstance(node, ast.Call):
            continue
        _q, attr = called_name(node)
        if attr not in PRIMITIVE_WIDTH:
            continue
        arg_index = 2 if attr.startswith("read_") else 0
        if len(node.args) <= arg_index:
            continue
        if tag_literal(node.args[arg_index], consts) is None:
            continue
        if fixed_width_only and PRIMITIVE_WIDTH[attr] is None:
            continue
        return node, arg_index
    return None


def run_self_test(
    server: Path,
    table: dict[tuple[str, str], list[Row]],
    present: dict[tuple[str, str], list[str]],
    message_names: set[str],
) -> int:
    import tempfile

    subjects = _pick_subjects(server, table, present, message_names)
    if not subjects:
        print("SELFTEST FAIL -- no clean subject with 3+ tagged fields found")
        return 1
    if len({s.rel for s in subjects}) < 2:
        print(
            "SELFTEST FAIL -- only %d module(s) available as subjects; a "
            "single-module mutant bank is a fixture monoculture"
            % len({s.rel for s in subjects})
        )
        return 1

    shared = sorted(set.intersection(*[set(_traits(s)) for s in subjects]))
    if shared:
        print(
            "SELFTEST NARROW -- every subject shares: %s." % ", ".join(shared)
        )
        print(
            "SELFTEST NARROW-CAUSE -- this is THIS BANK'S filter, not a "
            "property of the tree.  The reorder mutant swaps two top-level "
            "statements, so a subject needs two of them emitting different "
            "tags; every decoder on the tree does all its reads inside one "
            "statement and is rejected here, which is why no decoder and "
            "nothing under gm/ is ever mutated.  A statement-granularity "
            "reorder is the wrong strategy for that shape and replacing it is "
            "the first job of the next round of this lane."
        )

    survivors: list[str] = []
    exercised: set[str] = set()
    ran = 0
    skipped: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for subject in subjects:
            for kind in MUTANTS:
                mutated = _mutate(subject, kind)
                if mutated is None:
                    skipped.append("%s::%s %s" % (subject.rel, subject.func.name, kind))
                    continue
                target = root / subject.rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(ast.unparse(mutated), encoding="utf-8")
                findings, unresolved, checked = check_module(
                    target, subject.rel, table, present, message_names
                )
                ran += 1
                exercised.add(kind)
                caught, why = _mutant_caught(
                    kind, subject, findings, unresolved, checked
                )
                print(
                    "SELFTEST %-13s %-58s %s"
                    % (kind, subject.rel + "::" + subject.func.name,
                       "caught" if caught else "SURVIVED -- " + why)
                )
                if not caught:
                    survivors.append(
                        "%s %s::%s (%s)"
                        % (kind, subject.rel, subject.func.name, why)
                    )
    for line in skipped:
        print("SELFTEST SKIPPED %s -- mutation does not apply to this subject" % line)
    print(
        "pf_wire_fields_xcheck --self-test: %d subject(s), %d mutant(s) run, "
        "%d survivor(s), %d not applicable"
        % (len(subjects), ran, len(survivors), len(skipped))
    )
    never_run = [k for k in MUTANTS if k not in exercised]
    if never_run:
        print(
            "SELFTEST FAIL -- mutant(s) %s applied to no subject at all; a "
            "mutant that never runs pins nothing" % ", ".join(never_run)
        )
        return 1
    if survivors:
        for line in survivors:
            print("SELFTEST SURVIVOR " + line)
        print("SELFTEST FAIL -- a mutant this tool must catch went unreported")
        return 1
    print("SELFTEST PASS -- every mutant was caught, and the blind one was "
          "counted UNRESOLVED rather than passed")
    return 0


def _mutant_caught(
    kind: str,
    subject: Subject,
    findings: list[str],
    unresolved: list[str],
    checked: int,
) -> tuple[bool, str]:
    tail = "::" + subject.func.name + " "
    mine = [line for line in unresolved if tail in line]
    if kind == "opaque-helper":
        # The whole point: blind must NOT be silent, and must NOT be checked.
        if findings:
            return False, "reported a field disagreement instead of UNRESOLVED"
        if not any("OPAQUE-BODY" in line for line in mine):
            return False, "no counted UNRESOLVED for the blinded function"
        if checked != subject.baseline_checked - 1:
            return False, (
                "module checked %d function(s), expected %d -- the blinded "
                "function was still compared"
                % (checked, subject.baseline_checked - 1)
            )
        return True, ""
    if kind == "alias-launder":
        if not findings:
            return False, (
                "a tagged byte was accepted as a length-prefixed string -- "
                "TAG_ALIASES ran backwards"
            )
        return True, ""
    if kind == "narrow-width":
        if not any(line.startswith("XCHECK WIDTH") for line in findings):
            return False, "no XCHECK WIDTH line"
        return True, ""
    if not findings:
        return False, "no finding at all"
    return True, ""


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
        "--emit-pin",
        action="store_true",
        help="print a fresh COVERAGE_PIN literal for this tree and exit",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "mutate real modules and require this tool to catch every mutant; "
            "exits non-zero if any survives"
        ),
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
        if args.self_test:
            # A self-test that cannot obtain a subject has measured NOTHING.
            # Reporting that as success is the exact failure the mode exists to
            # stop, and a bridge-only checkout is the shape this tool says it
            # expects, so this is the common case, not the corner.
            print(
                "SELFTEST FAIL -- no pirate-force-server checkout to build "
                "mutants from; zero mutants ran, which is not a pass"
            )
            return 1
        print(
            "SKIP -- no pirate-force-server checkout beside this repository; "
            "this tool is advisory and blocks nobody"
        )
        return 0

    table, present = load_table(TSV)
    # Every message the table mentions, not only those with a tagged row: a
    # message whose rows are all ``EMPTY`` is IN the table, and saying "no
    # message named X" about it is a false statement about the table.
    message_names = {message for message, _ in present}

    if args.self_test:
        return run_self_test(server, table, present, message_names)

    modules = sorted((server / "src").rglob("*_wire.py"))
    all_findings: list[str] = []
    all_unresolved: list[str] = []
    allowlisted: list[str] = []
    checked = 0
    per_module: dict[str, int] = {}
    for path in modules:
        rel = str(path.relative_to(server)).replace("\\", "/")
        findings, unresolved, count = check_module(
            path, rel, table, present, message_names
        )
        checked += count
        per_module[rel] = count
        all_unresolved.extend(unresolved)
        if findings and rel in ALLOWLIST:
            allowlisted.extend(findings)
            continue
        all_findings.extend(findings)

    if args.emit_pin:
        print("COVERAGE_PIN: dict[str, int] = {")
        for rel in sorted(per_module):
            print('    "%s": %d,' % (rel, per_module[rel]))
        print("}")
        return 0

    regressed = []
    for rel in sorted(COVERAGE_PIN):
        was = COVERAGE_PIN[rel]
        now = per_module.get(rel)
        if now is None:
            regressed.append(
                "XCHECK COVERAGE-LOST %s -- pinned at %d compared function(s), "
                "the module is not in the run at all now (renamed off "
                "*_wire.py, moved, or deleted)" % (rel, was)
            )
        elif now < was:
            regressed.append(
                "XCHECK COVERAGE-DROP %s -- pinned at %d compared function(s), "
                "now %d; this tool understands less of this module than it did"
                % (rel, was, now)
            )
    for rel in sorted(set(per_module) - set(COVERAGE_PIN)):
        print(
            "XCHECK UNPINNED %s -- %d compared function(s), not in COVERAGE_PIN "
            "(informational; regenerate the pin with --emit-pin)"
            % (rel, per_module[rel])
        )
    for line in regressed:
        print(line)

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
    if regressed:
        print(
            "XCHECK FAIL -- no field disagreement, but coverage went backwards "
            "in %d module(s) above. A deliberate drop is closed by regenerating "
            "COVERAGE_PIN (--emit-pin) in the commit that earns it."
            % len(regressed)
        )
        return 1
    print(
        "XCHECK PASS -- every COMPARED function agrees with the table and no "
        "pinned module lost coverage; %d function(s) were not compared at all "
        "(--show-unresolved names them): unresolved is not agreement."
        % len(all_unresolved)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
