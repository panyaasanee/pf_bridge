"""LANE-B: can a mob_death contract refusal leave the live dispatch?

COO-DECISION 2026-09-07T15:41+07:00 item 5 (``pf_bridge`` notes_to_chief/
20260907_1541_COO-DECISION-b1520-hold-the-flip-measure-the-raise-LANE-B.md)
asks for a headless token proving whether killing a monster outside
``widen-death-scope-bg0002`` unwinds out of the listener thread.

``tests/test_mob_death_refusal_does_not_unwind_dispatch.py`` (round
tv8k4c, commit cef9875) answers that question for the roster kill site by
driving the real dispatcher.  This tool answers the OTHER half the letter
implies and that no dynamic test can reach in one run: of every production
call into a ``mob_death`` function that can raise
``MobDeathContractError``, which ones are not inside a handler for it, and
where a handler re-raises.  Static, so it covers the call sites no boot
happens to walk.

Prints one token per line, ASCII only, so a round file can quote it and a
later round can re-derive it:

    python3 tools/pf_mob_death_contract_unwind_static.py <repo root>

    MOB_DEATH_CONTRACT_CALLSITES total=N unguarded=M
    MOB_DEATH_CONTRACT_UNGUARDED <file>:<line>:<function>   (M lines)
    MOB_DEATH_CONTRACT_RERAISE count=K <file>:<line> ...

An unguarded line is NOT by itself a defect: it may sit behind a caller
that guards, or behind a condition that makes the raise unreachable (the
``runtime.py`` ``describe_death`` row is guarded by ``if death_step is not
None`` five lines above it, and ``describe_death`` raises only on a
mistyped step).  It is a list of places a reader must check by hand, which
is the thing the letter says was never measured.
"""
import ast
import pathlib
import sys


SRC = pathlib.Path(sys.argv[1]) / "src" / "pirateforce_foundation"

RAISERS = {
    "kill", "fire_mob_death_hook", "ruling_for", "death_frames",
    "dying_frames", "dead_frames", "corpse_npc_attr", "repopulation_frames",
    "repopulation_entries", "live_roster", "describe_death",
    "hostile_census_frames", "roster_override_coverage", "record_of",
    "with_death", "basic_mask_of", "death_actor_entry",
    "ruling_registered_at", "commit_death_and_prepare_hook", "commit_death",
}

def handler_names(h):
    if h.type is None:
        return ["<bare>"]
    t = h.type
    nodes = t.elts if isinstance(t, ast.Tuple) else [t]
    return [getattr(n, "id", getattr(n, "attr", None)) for n in nodes]

total = 0
unguarded = []
reraise = []
for path in sorted(SRC.rglob("*.py")):
    if path.name == "mob_death.py":
        continue
    tree = ast.parse(path.read_text(errors="replace"))
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if not isinstance(f, ast.Attribute) or f.attr not in RAISERS:
            continue
        if not (isinstance(f.value, ast.Name) and f.value.id == "mob_death"):
            continue
        total += 1
        cur, caught = node, None
        while cur in parents:
            par = parents[cur]
            if isinstance(par, ast.Try) and any(
                    cur is s or cur in ast.walk(s) for s in par.body):
                names = [n for h in par.handlers for n in handler_names(h)]
                if any(n in ("MobDeathContractError", "ValueError",
                             "Exception", "BaseException", "<bare>")
                       for n in names):
                    caught = names
                    break
            cur = par
        if caught is None:
            unguarded.append("%s:%d:%s" % (path.name, node.lineno, f.attr))

for path in sorted(SRC.rglob("*.py")):
    tree = ast.parse(path.read_text(errors="replace"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Try):
            continue
        for h in node.handlers:
            if "MobDeathContractError" not in handler_names(h):
                continue
            for sub in ast.walk(h):
                if isinstance(sub, ast.Raise):
                    reraise.append("%s:%d" % (path.name, sub.lineno))

print("MOB_DEATH_CONTRACT_CALLSITES total=%d unguarded=%d" % (
    total, len(unguarded)))
for row in unguarded:
    print("MOB_DEATH_CONTRACT_UNGUARDED %s" % row)
print("MOB_DEATH_CONTRACT_RERAISE count=%d %s" % (
    len(reraise), " ".join(reraise)))
