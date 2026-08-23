#!/usr/bin/env python3
"""pf_lua_api_census.py - census of the game-server API surface called by the
client's own Lua scripts.

Input : gamedata/lua/**/*.lua   (decoded by pf_decode_lua_npc.py)
Output: gamedata/PF_GAMEDATA_LUA_API.tsv

Independent re-derivation: this does NOT read pf_decode_lua_npc.py's census.
It re-counts from the decoded sources so the two can be compared adversarially.

Method notes (honest limits are printed by --report):
  * Files are decoded as latin-1 on purpose: identifiers and punctuation are
    ASCII, and latin-1 never fails, so byte offsets stay exact.  Thai strings
    inside the sources will look garbled here; this tool does not read them.
  * Comments and string literals are masked before matching, so a call name
    inside a comment or a quoted string is not counted.
  * Arguments are split at top-level commas only (parens/brackets/braces and
    quotes are tracked), so nested calls count as one argument.
"""
import argparse, collections, csv, json, re, sys
from pathlib import Path

CALL = re.compile(r"(?<![A-Za-z0-9_.])([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\s*\(")
STDLIB = {"string", "table", "math", "os", "io", "coroutine", "debug", "package"}


def mask(src: str) -> str:
    """Blank out comments and string literals, preserving length and newlines."""
    out = list(src)
    i, n = 0, len(src)
    def blank(a, b):
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "
    while i < n:
        c = src[i]
        if c == "-" and src.startswith("--", i):
            j = i + 2
            m = re.match(r"\[(=*)\[", src[j:])
            if m:
                close = "]" + m.group(1) + "]"
                e = src.find(close, j)
                e = n if e < 0 else e + len(close)
            else:
                e = src.find("\n", j)
                e = n if e < 0 else e
            blank(i, e); i = e; continue
        if c in "\"'":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            j = min(j + 1, n)
            blank(i, j); i = j; continue
        m = re.match(r"\[(=*)\[", src[i:])
        if m:
            close = "]" + m.group(1) + "]"
            e = src.find(close, i)
            e = n if e < 0 else e + len(close)
            blank(i, e); i = e; continue
        i += 1
    return "".join(out)


def split_args(src: str, open_paren: int):
    """Return (arg_strings, end_index) for the call whose '(' is at open_paren."""
    depth, i, n = 0, open_paren, len(src)
    start, args = open_paren + 1, []
    while i < n:
        c = src[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                seg = src[start:i].strip()
                if seg or args:
                    args.append(seg)
                return args, i
        elif c == "," and depth == 1:
            args.append(src[start:i].strip()); start = i + 1
        i += 1
    return None, None


NUM = re.compile(r"^-?(?:0[xX][0-9a-fA-F]+|\d+\.?\d*|\.\d+)$")


def classify(arg: str) -> str:
    a = arg.strip()
    if not a:
        return "empty"
    if NUM.match(a):
        return "num"
    if a[:1] in "\"'":
        return "str"
    if a in ("true", "false"):
        return "bool"
    if a == "nil":
        return "nil"
    if "(" in a:
        return "call"
    if re.match(r"^[A-Za-z_][A-Za-z0-9_.]*$", a):
        return "var"
    return "expr"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--report", action="store_true")
    ns = ap.parse_args()

    root = Path(ns.root)
    lua_dir = root / "gamedata" / "lua"
    if not lua_dir.is_dir():
        print("REFUSED: %s not found" % lua_dir); return 3
    files = sorted(lua_dir.rglob("*.lua"))
    if not files:
        print("REFUSED: no .lua under %s" % lua_dir); return 3

    calls = collections.Counter()
    arity = collections.defaultdict(collections.Counter)
    shapes = collections.defaultdict(collections.Counter)
    seen_in = collections.defaultdict(set)
    unbalanced = 0

    for f in files:
        raw = f.read_bytes().decode("latin-1")
        src = mask(raw)
        for m in CALL.finditer(src):
            ns_name, meth = m.group(1), m.group(2)
            if ns_name in STDLIB:
                continue
            name = "%s.%s" % (ns_name, meth)
            args, end = split_args(src, m.end() - 1)
            if args is None:
                unbalanced += 1
                continue
            real = [raw[m.end():end].strip()] if False else None
            calls[name] += 1
            arity[name][len(args)] += 1
            shapes[name]["|".join(classify(a) for a in args)] += 1
            seen_in[name].add(str(f.relative_to(lua_dir)).replace("\\", "/"))

    out = Path(ns.out) if ns.out else root / "gamedata" / "PF_GAMEDATA_LUA_API.tsv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["api", "namespace", "method", "call_count", "file_count",
                    "arity_min", "arity_max", "arity_mode", "arg_shape_top",
                    "arg_shape_top_count", "distinct_arg_shapes", "example_files"])
        for name in sorted(calls, key=lambda k: (-calls[k], k)):
            a = arity[name]
            top_shape, top_n = shapes[name].most_common(1)[0]
            ex = sorted(seen_in[name])[:3]
            w.writerow([name, name.split(".")[0], name.split(".")[1], calls[name],
                        len(seen_in[name]), min(a), max(a),
                        a.most_common(1)[0][0], top_shape, top_n,
                        len(shapes[name]), ";".join(ex)])

    ns_tot = collections.Counter()
    for k, v in calls.items():
        ns_tot[k.split(".")[0]] += v
    print("files            %d" % len(files))
    print("distinct api     %d" % len(calls))
    print("total call sites %d" % sum(calls.values()))
    print("unbalanced skip  %d" % unbalanced)
    print("namespaces       %s" % ", ".join("%s=%d" % kv for kv in ns_tot.most_common()))
    print("wrote            %s" % out)
    if ns.report:
        for name, c in calls.most_common(15):
            a = arity[name]
            print("  %-32s %6d  arity %d-%d  top %s" %
                  (name, c, min(a), max(a), shapes[name].most_common(1)[0][0][:40]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
