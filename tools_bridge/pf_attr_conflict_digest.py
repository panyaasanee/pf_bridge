#!/usr/bin/env python3
"""pf_attr_conflict_digest.py -- ASCII only, cp874-safe console.

Two Codex attr tables are too big to travel through pf_git_sync.ps1
(SIZE_LIMIT_BYTES = 2 MB):

    external/PF_ATTR_CONFLICTS.tsv   ~3.4 MB
    external/PF_ATTR_UNRESOLVED.tsv  ~2.3 MB

They stay on the bridge disk.  This script derives the small decision-grade
tables that DO travel, into

    notes_to_chief/reference_codex_attr/

Nothing here re-derives or reinterprets Codex's claims.  It only counts rows
and slices them, so every output line is traceable to a row in the source
file by conflict_key / unresolved_key.

Run from the pf_bridge folder:  python tools_bridge\pf_attr_conflict_digest.py
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.dirname(HERE)
EXT = os.path.join(BRIDGE, "external")
OUT = os.path.join(BRIDGE, "notes_to_chief", "reference_codex_attr")

CONFLICTS = os.path.join(EXT, "PF_ATTR_CONFLICTS.tsv")
UNRESOLVED = os.path.join(EXT, "PF_ATTR_UNRESOLVED.tsv")

# ---------------------------------------------------------------------------
# Why the mirror below exists
# ---------------------------------------------------------------------------
# pf_git_sync.ps1 has two scans.  ALLOWLIST (notes_to_chief, evidence_screens,
# rounds, tools_bridge) is scanned with --untracked-files=all, so a brand new
# file there travels on the next round with no git step at all.  SHARED_TRACKED
# (which is where external/ lives) is scanned with --untracked-files=no, so a
# file there travels only once it is ALREADY in the git index.
#
# .gitignore was widened on 2026-08-31 so the attr deliverables MAY be tracked,
# but nothing has staged them yet, so today they still cannot leave the bridge
# from external/.  Copying them under notes_to_chief/ is the same route ka1-A
# used for reference_adhoc_probe/ on 2026-08-28 and it needs no git write.
#
# Only files under the 2 MB sync cap are listed.  Delta tables against a prior
# generation are left out on purpose: high churn, low value to a lane that
# just wants to encode a field correctly.
MIRROR = [
    "PF_ATTR_FOR_SERVER.md",
    "PF_ATTR_SEMANTIC_REPORT.md",
    "PF_ATTR_FIELD_SEMANTICS.md",
    "PF_ATTR_FIELD_SEMANTICS.tsv",
    "PF_ATTR_CLASS_CENSUS.md",
    "PF_ATTR_CLASS_CENSUS.tsv",
    "PF_ATTR_RUNTIME_FIELDS.tsv",
    "PF_ATTR_UI_BINDINGS.tsv",
    "PF_ATTR_DATA_BINDINGS.tsv",
    "PF_ATTR_INHERITANCE.tsv",
    "PF_ATTR_COMPUTED_SEMANTICS.tsv",
    "PF_ATTR_CONTAINER_SEMANTICS.tsv",
    "PF_ATTR_FIELD_VALIDATION_DELTA.md",
    "PF_ATTR_FIELD_VALIDATION_DELTA.tsv",
    "PF_ATTR_REMAINING_CODEC_CENSUS.md",
    "PF_ATTR_REMAINING_CODEC_CENSUS.tsv",
    "PF_ATTR_GENERATION_MANIFEST.json",
    "PF_ATTR_PROBE_REQUESTS.tsv",
    "PF_ATTR_QUARANTINE.tsv",
    "PF_ERRATUM_TWO_IMAGES.md",
    "PF_A2_ACTOR_CODEC_CORRECTION.tsv",
    "PF_A2_BASIC_CODEC_CORRECTION.tsv",
    "PF_A2_ATTR_SEMANTIC_DELTA.md",
]
SIZE_CAP = 2 * 1024 * 1024

# Classes the running server actually encodes today.  A conflict outside this
# set cannot break the live wire, so it is a documentation question, not a
# release blocker.
WIRED_CLASS_PREFIXES = ("ActorAttr", "BasicAttr")


def read_tsv(path):
    if not os.path.exists(path):
        print("MISSING: " + path)
        return [], []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        rdr = csv.reader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
        rows = list(rdr)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def family_of(kind):
    """Collapse conflict_kind into the policy family that decides it.

    Each family is ONE question for the COO, not one question per row.
    """
    if "NON_WIRE" in kind:
        return "A_NON_WIRE_ROW"
    if "GATE" in kind or "MASK_STORAGE" in kind:
        return "B_MASK_GATE"
    if "DIRECTION" in kind:
        return "C_DIRECTION_DUP"
    if "LAYOUT" in kind or "SEMANTICS" in kind:
        return "D_LAYOUT"
    return "E_OTHER"


def write_tsv(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_NONE,
                       escapechar="\\", lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    print("wrote %-44s %5d row(s)  %8d bytes"
          % (name, len(rows), os.path.getsize(path)))


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    chdr, crows = read_tsv(CONFLICTS)
    if not chdr:
        return 2
    ci = dict((n, i) for i, n in enumerate(chdr))

    def cell(row, name):
        i = ci.get(name, -1)
        return row[i] if 0 <= i < len(row) else ""

    # ---- 1. buckets: kind x status, plus the family that decides it --------
    buckets = {}
    for r in crows:
        kind = cell(r, "conflict_kind")
        status = cell(r, "resolution_status")
        key = (family_of(kind), kind, status)
        buckets[key] = buckets.get(key, 0) + 1
    brows = []
    for (fam, kind, status), n in sorted(buckets.items(),
                                         key=lambda kv: (-kv[1], kv[0])):
        decides = "CODEX_ALREADY_RESOLVED" if status.startswith("CORRECTED") \
            or status.startswith("REFUTED") else "NEEDS_COO_RULING"
        brows.append([fam, kind, status, str(n), decides])
    write_tsv("PF_ATTR_CONFLICTS_BUCKETS.tsv",
              ["policy_family", "conflict_kind", "resolution_status",
               "row_count", "who_decides"], brows)

    # ---- 2. the slice that can break the LIVE wire ------------------------
    keep = ["conflict_key", "field_key", "conflict_kind", "frozen_claim",
            "rederived_claim", "rederived_evidence_key",
            "rederived_evidence_artifact", "resolution_status"]
    wired = []
    for r in crows:
        fk = cell(r, "field_key")
        if not fk.startswith(WIRED_CLASS_PREFIXES):
            continue
        if not cell(r, "resolution_status").startswith("OPEN"):
            continue
        wired.append([cell(r, k) for k in keep])
    wired.sort(key=lambda x: x[1])
    write_tsv("PF_ATTR_CONFLICTS_OPEN_WIRED.tsv", keep, wired)

    # ---- 3. headline counts ----------------------------------------------
    total = len(crows)
    open_n = sum(1 for r in crows
                 if cell(r, "resolution_status").startswith("OPEN"))
    fam_open = {}
    for r in crows:
        if not cell(r, "resolution_status").startswith("OPEN"):
            continue
        f = family_of(cell(r, "conflict_kind"))
        fam_open[f] = fam_open.get(f, 0) + 1

    uhdr, urows = read_tsv(UNRESOLVED)
    ubuckets = {}
    if uhdr:
        ui = dict((n, i) for i, n in enumerate(uhdr))
        for r in urows:
            def uc(name):
                i = ui.get(name, -1)
                return r[i] if 0 <= i < len(r) else ""
            # 'blocker' is long free text, so it is reduced to its first
            # clause only.  Bucketing on the raw field produced one row per
            # source row and no digest at all.
            blocker = uc("blocker").split(";")[0].split(":")[0].strip()[:60]
            cls = uc("class") or uc("applies_to_class")
            key = (uc("unresolved_kind"), cls, uc("scope_status"), blocker)
            ubuckets[key] = ubuckets.get(key, 0) + 1
        urows_out = [[k, c, sc, b, str(n)] for (k, c, sc, b), n in
                     sorted(ubuckets.items(), key=lambda kv: -kv[1])]
        write_tsv("PF_ATTR_UNRESOLVED_BUCKETS.tsv",
                  ["unresolved_kind", "class", "scope_status",
                   "blocker_head", "row_count"], urows_out)

    # ---- 4. mirror the attr deliverables onto the travelling route --------
    copied, skipped = [], []
    for name in MIRROR:
        src = os.path.join(EXT, name)
        if not os.path.exists(src):
            skipped.append((name, "missing in external/"))
            continue
        n = os.path.getsize(src)
        if n > SIZE_CAP:
            skipped.append((name, "%d bytes over the 2 MB sync cap" % n))
            continue
        with open(src, "rb") as fi:
            data = fi.read()
        dst = os.path.join(OUT, name)
        old = None
        if os.path.exists(dst):
            with open(dst, "rb") as fo:
                old = fo.read()
        if old == data:
            continue
        with open(dst, "wb") as fo:
            fo.write(data)
        copied.append((name, n))
    print("")
    print("mirrored %d changed file(s) into notes_to_chief/reference_codex_attr/"
          % len(copied))
    for name, n in copied:
        print("  + %-42s %8d bytes" % (name, n))
    for name, why in skipped:
        print("  - %-42s %s" % (name, why))

    lines = []
    lines.append("PF_ATTR conflict digest")
    lines.append("generated by tools_bridge/pf_attr_conflict_digest.py")
    lines.append("")
    lines.append("conflict rows total          : %d" % total)
    lines.append("already resolved by Codex    : %d" % (total - open_n))
    lines.append("still OPEN, need a ruling    : %d" % open_n)
    lines.append("")
    lines.append("OPEN rows by policy family (one ruling clears the family):")
    for f, n in sorted(fam_open.items(), key=lambda kv: -kv[1]):
        lines.append("  %-18s %5d" % (f, n))
    lines.append("")
    lines.append("OPEN rows on classes the live server encodes today "
                 "(%s) : %d" % ("/".join(WIRED_CLASS_PREFIXES), len(wired)))
    lines.append("")
    lines.append("full tables stay on the bridge disk only, they exceed the")
    lines.append("2 MB sync cap:")
    lines.append("  external/PF_ATTR_CONFLICTS.tsv")
    lines.append("  external/PF_ATTR_UNRESOLVED.tsv")
    txt = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "PF_ATTR_CONFLICTS_HEADLINE.txt"), "w",
              encoding="ascii") as fh:
        fh.write(txt)
    print("")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
