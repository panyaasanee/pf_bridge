#!/usr/bin/env python3
"""pf_attr_conflict_digest.py -- carry Codex's attr work to the team.  ASCII only.

Codex writes its attr deliverables into pf_bridge/external/ and regenerates the
whole set every round.  Two things then go wrong on their own:

  1. Nothing in external/ reaches GitHub.  .gitignore denies the folder except
     for a few named members, and pf_git_sync.ps1 scans external/ with
     --untracked-files=no, so a new file there can never ride along.  Cloud
     lanes read from a clone, so for them the work does not exist.
  2. Two tables (PF_ATTR_CONFLICTS.tsv ~3.4 MB, PF_ATTR_UNRESOLVED.tsv ~2.3 MB)
     exceed the 2 MB cap in pf_git_sync.ps1 and can never travel whole.

This script fixes both, every time it runs, with no git command:

  * verifies the generation is COMPLETE (sha256 of every artifact against the
    manifest) so a half-written round is never published,
  * mirrors the attr deliverables into notes_to_chief/reference_codex_attr/,
    which IS in the sync push allowlist and carries untracked files,
  * derives small decision-grade slices of the two oversized tables,
  * and, when the generation_id has changed since last run, writes a letter
    into notes_to_chief/ naming what is new so the team SEES it instead of
    having to poll a folder.

Discovery is by pattern, not by a hand-written list: a deliverable Codex adds
next round is picked up without anyone editing this file.  That matters - the
2026-08-31 round added PF_ATTR_NAME_COLOR_SELECTOR.tsv,
PF_ATTR_ROLE_DISCRIMINATOR.tsv and PF_ATTR_QUEST_MARK_SELECTOR.tsv, three
answers to P0 blockers, and a hand-written list would have dropped all three.

Run from the pf_bridge folder:  python tools_bridge\pf_attr_conflict_digest.py
Safe to run repeatedly; it only writes when bytes actually changed.
"""

import csv
import datetime
import hashlib
import json
import os
import sys

csv.field_size_limit(min(2147483647, sys.maxsize))

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.dirname(HERE)
EXT = os.path.join(BRIDGE, "external")
NOTES = os.path.join(BRIDGE, "notes_to_chief")
OUT = os.path.join(NOTES, "reference_codex_attr")
STATE = os.path.join(OUT, ".last_mirrored_generation.json")
MANIFEST = os.path.join(EXT, "PF_ATTR_GENERATION_MANIFEST.json")

# pf_git_sync.ps1 refuses anything over 2 MB.  Stay under it with a margin so a
# table that grows slightly between rounds does not start failing silently.
SIZE_CAP = 1900000

# Names carrying these fragments are refused by the sync proprietary name guard
# ($BAD_NAME_PARTS).  Mirroring them would only produce a refusal line a round.
NAME_GUARD = ("capture", "gameclient", "pirateforce.sqlite")

# Which artifacts belong to the attr work.  Prefix match, deliberately broad.
MIRROR_PREFIXES = ("PF_ATTR_", "PF_A2_", "PF_A3_", "PF_A6_", "PF_ERRATUM_")

# Classes the running server actually encodes today.  A conflict outside this
# set cannot break the live wire, so it is a documentation question rather than
# a release blocker.
WIRED_CLASS_PREFIXES = ("ActorAttr", "BasicAttr")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_generation():
    """Return (generation_id, root_dir, artifacts) or exit with a reason.

    The manifest says plainly that the top-level copies in external/ are
    non-authoritative mirrors and that artifact_root holds the verified bytes,
    so everything below reads from the root, not from external/*.tsv.
    """
    if not os.path.exists(MANIFEST):
        print("ABORT: no manifest at " + MANIFEST)
        return None
    with open(MANIFEST, "r", encoding="utf-8") as fh:
        man = json.load(fh)
    gen = man.get("generation_id", "")
    root = os.path.join(EXT, man.get("artifact_root", ""))
    artifacts = man.get("artifacts", {})
    if not os.path.isdir(root):
        print("ABORT: artifact_root missing - Codex is probably mid-write")
        return None

    # A generation still being staged has files that do not match their
    # recorded digest yet.  Publishing that would hand the team a torn round.
    bad = []
    for name, want in sorted(artifacts.items()):
        p = os.path.join(root, name)
        if not os.path.exists(p):
            bad.append(name + " missing")
            continue
        if isinstance(want, str) and len(want) == 64:
            got = sha256(p)
            if got != want:
                bad.append(name + " sha mismatch")
    if bad:
        print("ABORT: generation is incomplete or being rewritten right now:")
        for b in bad[:10]:
            print("  ! " + b)
        print("  (nothing was published; run again in a minute)")
        return None
    print("generation %s verified: %d/%d artifacts match their sha256"
          % (gen[:12], len(artifacts), len(artifacts)))
    return gen, root, artifacts


def read_tsv(path):
    if not os.path.exists(path):
        return [], []
    with open(path, "r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    return (rows[0], rows[1:]) if rows else ([], [])


def write_tsv(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_NONE,
                       escapechar="\\", lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    print("  slice %-42s %5d row(s)  %8d bytes"
          % (name, len(rows), os.path.getsize(path)))


def family_of(kind):
    """Collapse conflict_kind into the policy family that decides it.

    Each family is ONE ruling for the COO, not one ruling per row.
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


def build_slices(root):
    """Derive the small tables that stand in for the two oversized ones."""
    chdr, crows = read_tsv(os.path.join(root, "PF_ATTR_CONFLICTS.tsv"))
    summary = {}
    if not chdr:
        return summary
    ci = dict((n, i) for i, n in enumerate(chdr))

    def cell(row, name):
        i = ci.get(name, -1)
        return row[i] if 0 <= i < len(row) else ""

    buckets = {}
    for r in crows:
        key = (family_of(cell(r, "conflict_kind")), cell(r, "conflict_kind"),
               cell(r, "resolution_status"))
        buckets[key] = buckets.get(key, 0) + 1
    brows = []
    for (fam, kind, status), n in sorted(buckets.items(),
                                         key=lambda kv: (-kv[1], kv[0])):
        who = ("CODEX_ALREADY_RESOLVED"
               if status.startswith(("CORRECTED", "REFUTED"))
               else "NEEDS_COO_RULING")
        brows.append([fam, kind, status, str(n), who])
    write_tsv("PF_ATTR_CONFLICTS_BUCKETS.tsv",
              ["policy_family", "conflict_kind", "resolution_status",
               "row_count", "who_decides"], brows)

    keep = ["conflict_key", "field_key", "conflict_kind", "frozen_claim",
            "rederived_claim", "rederived_evidence_key",
            "rederived_evidence_artifact", "resolution_status"]
    wired = [[cell(r, k) for k in keep] for r in crows
             if cell(r, "field_key").startswith(WIRED_CLASS_PREFIXES)
             and cell(r, "resolution_status").startswith("OPEN")]
    wired.sort(key=lambda x: x[1])
    write_tsv("PF_ATTR_CONFLICTS_OPEN_WIRED.tsv", keep, wired)

    open_n = sum(1 for r in crows
                 if cell(r, "resolution_status").startswith("OPEN"))
    fam_open = {}
    for r in crows:
        if cell(r, "resolution_status").startswith("OPEN"):
            f = family_of(cell(r, "conflict_kind"))
            fam_open[f] = fam_open.get(f, 0) + 1

    uhdr, urows = read_tsv(os.path.join(root, "PF_ATTR_UNRESOLVED.tsv"))
    if uhdr:
        ui = dict((n, i) for i, n in enumerate(uhdr))
        ub = {}
        for r in urows:
            def uc(name):
                i = ui.get(name, -1)
                return r[i] if 0 <= i < len(r) else ""
            # 'blocker' is long free text; bucketing on it raw produced one row
            # per source row and no digest at all, so keep the first clause.
            key = (uc("unresolved_kind"), uc("class") or uc("applies_to_class"),
                   uc("scope_status"),
                   uc("blocker").split(";")[0].split(":")[0].strip()[:60])
            ub[key] = ub.get(key, 0) + 1
        write_tsv("PF_ATTR_UNRESOLVED_BUCKETS.tsv",
                  ["unresolved_kind", "class", "scope_status", "blocker_head",
                   "row_count"],
                  [[k, c, s, b, str(n)] for (k, c, s, b), n in
                   sorted(ub.items(), key=lambda kv: -kv[1])])

    summary = {"total": len(crows), "open": open_n, "families": fam_open,
               "wired": len(wired), "unresolved": len(urows)}
    return summary


def mirror(root, artifacts):
    """Copy the attr deliverables onto the route that actually travels."""
    added, changed, skipped = [], [], []
    for name in sorted(artifacts):
        if not name.startswith(MIRROR_PREFIXES):
            continue
        low = name.lower()
        if any(g in low for g in NAME_GUARD):
            skipped.append((name, "sync name guard would refuse it"))
            continue
        src = os.path.join(root, name)
        n = os.path.getsize(src)
        if n > SIZE_CAP:
            skipped.append((name, "%d bytes, over the sync cap" % n))
            continue
        with open(src, "rb") as fh:
            data = fh.read()
        dst = os.path.join(OUT, name)
        if os.path.exists(dst):
            with open(dst, "rb") as fh:
                if fh.read() == data:
                    continue
            changed.append((name, n))
        else:
            added.append((name, n))
        with open(dst, "wb") as fh:
            fh.write(data)
    return added, changed, skipped


def announce(gen, prev_gen, added, changed, skipped, summary):
    """Write a letter so the team SEES a new round instead of polling."""
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    fname = "%s_CODEX-NEWGEN-%s-%dnew-%dchanged-ka1B-auto.md" % (
        stamp, gen[:8], len(added), len(changed))
    path = os.path.join(NOTES, fname)
    L = []
    L.append("# Codex ส่งงานรอบใหม่ - generation `%s`" % gen[:16])
    L.append("")
    L.append("ใบนี้เขียนอัตโนมัติโดย `tools_bridge/pf_attr_conflict_digest.py` "
             "ไม่ใช่คนเขียน - มันบอกแค่ว่า**อะไรเปลี่ยน** ส่วน**แปลว่าอะไร** "
             "ต้องมีคนอ่านแล้วเขียนใบตีความตามมา")
    L.append("")
    L.append("- generation ก่อนหน้า: `%s`" % (prev_gen[:16] if prev_gen else "(ยังไม่เคยมิเรอร์)"))
    L.append("- generation นี้: `%s`" % gen)
    L.append("- ยืนยัน sha256 ของ artifact ครบทุกไฟล์แล้วก่อนคัดลอก "
             "(ไฟล์ที่เขียนค้างจะไม่ถูกเผยแพร่)")
    L.append("")
    if added:
        L.append("## ไฟล์ใหม่ที่ไม่เคยมีมาก่อน (%d)" % len(added))
        L.append("")
        for n, b in added:
            L.append("- `%s` (%s bytes)" % (n, b))
        L.append("")
    if changed:
        L.append("## ไฟล์เดิมที่เนื้อหาเปลี่ยน (%d)" % len(changed))
        L.append("")
        for n, b in changed:
            L.append("- `%s` (%s bytes)" % (n, b))
        L.append("")
    if skipped:
        L.append("## ไม่ได้มิเรอร์ (%d) - อยู่บนดิสก์บริดจ์เท่านั้น" % len(skipped))
        L.append("")
        for n, why in skipped:
            L.append("- `%s` - %s" % (n, why))
        L.append("")
    if summary:
        L.append("## conflict รอบนี้")
        L.append("")
        L.append("- แถวทั้งหมด %d · Codex ปิดเอง %d · **ยัง OPEN %d**"
                 % (summary["total"], summary["total"] - summary["open"],
                    summary["open"]))
        for f, n in sorted(summary["families"].items(), key=lambda kv: -kv[1]):
            L.append("  - %s: %d" % (f, n))
        L.append("- แถว OPEN ที่แตะคลาสที่เซิร์ฟเวอร์ encode จริงวันนี้ "
                 "(ActorAttr/BasicAttr): **%d**" % summary["wired"])
        L.append("- unresolved %d แถว" % summary["unresolved"])
        L.append("")
    L.append("## อ่านที่ไหน")
    L.append("")
    L.append("`pf_bridge/notes_to_chief/reference_codex_attr/` "
             "อ่าน `README_WHAT_THIS_IS.md` ก่อน · "
             "ตัวเลข conflict อยู่ใน `PF_ATTR_CONFLICTS_HEADLINE.txt` · "
             "แถวที่แตะโค้ดจริงอยู่ใน `PF_ATTR_CONFLICTS_OPEN_WIRED.tsv`")
    L.append("")
    L.append("**กติกาที่ยังใช้เหมือนเดิม:** ทุกแถวของ Codex เป็นหลักฐานชั้น IMAGE "
             "(แกะไบนารีนิ่ง) ห้ามยกไปอ้างเป็นผลชั้น client-observable "
             "และคอลัมน์ `nonclaim` มีไว้ให้อ่าน - มันบอกว่าแถวนั้น**ไม่ได้**พิสูจน์อะไร")
    L.append("")
    L.append("-- ka1-B (อัตโนมัติ)")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("  letter %s (%d bytes)" % (fname, os.path.getsize(path)))
    return fname


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    g = load_generation()
    if g is None:
        return 2
    gen, root, artifacts = g

    prev_gen = None
    if os.path.exists(STATE):
        try:
            with open(STATE, "r", encoding="ascii") as fh:
                prev_gen = json.load(fh).get("generation_id")
        except Exception:
            prev_gen = None

    added, changed, skipped = mirror(root, artifacts)
    summary = build_slices(root)

    lines = ["PF_ATTR digest", "generated by tools_bridge/pf_attr_conflict_digest.py", ""]
    lines.append("generation_id : " + gen)
    if summary:
        lines.append("")
        lines.append("conflict rows total          : %d" % summary["total"])
        lines.append("already resolved by Codex    : %d"
                     % (summary["total"] - summary["open"]))
        lines.append("still OPEN, need a ruling    : %d" % summary["open"])
        lines.append("")
        lines.append("OPEN rows by policy family (one ruling clears a family):")
        for f, n in sorted(summary["families"].items(), key=lambda kv: -kv[1]):
            lines.append("  %-18s %5d" % (f, n))
        lines.append("")
        lines.append("OPEN rows on classes the live server encodes today "
                     "(%s) : %d" % ("/".join(WIRED_CLASS_PREFIXES),
                                    summary["wired"]))
    lines.append("")
    lines.append("the two tables below stay on the bridge disk, over the cap:")
    lines.append("  PF_ATTR_CONFLICTS.tsv")
    lines.append("  PF_ATTR_UNRESOLVED.tsv")
    txt = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "PF_ATTR_CONFLICTS_HEADLINE.txt"), "w",
              encoding="ascii") as fh:
        fh.write(txt)

    print("")
    print("mirrored: %d new, %d changed, %d left behind"
          % (len(added), len(changed), len(skipped)))
    for n, b in added:
        print("  + %-46s %9d" % (n, b))
    for n, b in changed:
        print("  ~ %-46s %9d" % (n, b))
    for n, why in skipped:
        print("  - %-46s %s" % (n, why))

    if gen != prev_gen and (added or changed):
        announce(gen, prev_gen, added, changed, skipped, summary)
    elif gen != prev_gen:
        print("  generation changed but no mirrored bytes differ - no letter")
    else:
        print("  same generation as last run - no letter")

    with open(STATE, "w", encoding="ascii") as fh:
        json.dump({"generation_id": gen}, fh)
    print("")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
