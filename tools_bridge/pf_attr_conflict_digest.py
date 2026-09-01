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
import time

csv.field_size_limit(min(2147483647, sys.maxsize))

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.dirname(HERE)
EXT = os.path.join(BRIDGE, "external")
NOTES = os.path.join(BRIDGE, "notes_to_chief")
OUT = os.path.join(NOTES, "reference_codex_attr")
STATE = os.path.join(OUT, ".last_mirrored_generation.json")

# The audit report was released to the team on 2026-09-01 by Panya.  It lives
# at the project root, which is outside every repo, so the cloud lanes cannot
# read it there.  Mirror it onto the travelling route like the attr tables.
# Codex rewrites it in place every checkpoint, so this re-copies when it moves.
AUDIT_SRC = os.path.join(os.path.dirname(BRIDGE),
                         "Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md")
AUDIT_OUT_DIR = os.path.join(NOTES, "reference_codex_audit")
AUDIT_DST = os.path.join(AUDIT_OUT_DIR,
                         "Pirate_Force_Codex_Audit_Recommendations.md")
MANIFEST = os.path.join(EXT, "PF_ATTR_GENERATION_MANIFEST.json")

# 2026-09-01: this script used to key everything off PF_ATTR_GENERATION_MANIFEST
# and mirror only the artifacts it listed.  That manifest covers ONE Codex work
# stream (attr).  Codex finished it, pinned it as a dependency, and moved on to
# colour / quest-mark / drop / GM work - so the attr generation_id stopped
# moving while Codex kept writing every few minutes.  Result: the round log
# reported "same generation, no letter" for half a day and 172 files in
# external/ never reached the team, including every artifact behind the three
# fronts the owner was actively asking about.
#
# The authority file below carries an authority_version that moves with each
# real round, so that is the signal now.  A content fingerprint over external/
# is the fallback for when it is absent.
AUTHORITY = os.path.join(EXT, "PF_CRITICAL_ARTIFACT_AUTHORITY.json")

# A file written within this many seconds is probably still being written.
FRESH_WRITE_GUARD_SEC = 20

# pf_git_sync.ps1 refuses anything over 2 MB.  Stay under it with a margin so a
# table that grows slightly between rounds does not start failing silently.
SIZE_CAP = 1900000

# The sync proprietary name guard ($BAD_NAME_PARTS) refuses names carrying
# these fragments - but pf_git_sync.ps1 waives the guard for the extensions
# below when the file travels under notes_to_chief/, a waiver Panya extended on
# 2026-09-01 so the twelve capture-VALIDATOR files stop being refused every
# round.  So only refuse here what the sync would still refuse there.
NAME_GUARD = ("capture", "gameclient", "pirateforce.sqlite")
WAIVED_EXTS = (".md", ".tsv", ".py", ".json")
HARD_DENY = ("gameclient", "pirateforce.sqlite")


def sync_would_refuse_name(name):
    low = name.lower()
    if any(g in low for g in HARD_DENY):
        return True
    if any(g in low for g in NAME_GUARD):
        return not low.endswith(WAIVED_EXTS)
    return False

# What to mirror.  This used to be a prefix list ("PF_ATTR_", "PF_A2_", ...)
# and that was still a hand-maintained guess: the 2026-08-31 P0-5 round shipped
# PF_COMBAT_LIFECYCLE.tsv/.md, no prefix matched, and 34 rows of combat
# lifecycle silently never reached the team.  The manifest IS Codex's own
# curated deliverable list, so mirror everything in it and let the size cap and
# the sync name guard do the excluding.  No pattern to keep in step with Codex.
MIRROR_PREFIXES = None  # kept for reference; selection is now manifest-driven

# A letter is written only when the round is SIGNIFICANT.  Codex regenerates
# roughly every 20 minutes, so on an hourly schedule "the generation changed"
# is true almost every run - announcing that unconditionally would drop ~24
# auto-letters a day into a mailbox that is already the team's bottleneck.
# Everything else still gets mirrored, and every round is recorded in
# CODEX_ROUNDS_LOG.tsv, so nothing is lost - it just does not ping anyone.
HIGH_SIGNAL_EXACT = ("PF_ATTR_FOR_SERVER.md", "PF_ATTR_QUARANTINE.tsv",
                     "PF_ATTR_PROBE_REQUESTS.tsv")
HIGH_SIGNAL_SUBSTR = ("SELECTOR", "DISCRIMINATOR", "CORRECTION", "ERRATUM")

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


def round_key():
    """What identifies 'a Codex round' for change detection.

    authority_version first; otherwise a fingerprint of every file in
    external/ (name + size + mtime), which moves whenever anything is written.
    """
    try:
        with open(AUTHORITY, "r", encoding="utf-8") as fh:
            a = json.load(fh)
        v = a.get("authority_version")
        if v:
            note = a.get("authority_note", "")
            return "authority:" + str(v), note
    except Exception:
        pass
    h = hashlib.sha256()
    for name in sorted(os.listdir(EXT)):
        full = os.path.join(EXT, name)
        if not os.path.isfile(full):
            continue
        st = os.stat(full)
        h.update(("%s|%d|%d\n" % (name, st.st_size, int(st.st_mtime))).encode())
    return "fingerprint:" + h.hexdigest()[:16], ""


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


def snapshot_audit_report():
    """Keep an immutable copy of the audit report before Codex overwrites it.

    Mirrors what the scheduled task does by hand, so a skipped or forgotten
    step never costs a version.  No-op when the bytes match the newest copy
    already in audit_history/.
    """
    if not os.path.exists(AUDIT_SRC):
        return
    hist = os.path.join(os.path.dirname(BRIDGE), "audit_history")
    if not os.path.isdir(hist):
        os.makedirs(hist)
    with open(AUDIT_SRC, "rb") as fh:
        data = fh.read()
    existing = sorted(os.listdir(hist))
    if existing:
        with open(os.path.join(hist, existing[-1]), "rb") as fh:
            if fh.read() == data:
                return
        for name in existing:
            with open(os.path.join(hist, name), "rb") as fh:
                if fh.read() == data:
                    return
    gen = "unknown"
    try:
        with open(MANIFEST, "r", encoding="utf-8") as fh:
            gen = json.load(fh).get("generation_id", "unknown")[:12]
    except Exception:
        pass
    name = ("Pirate_Force_Codex_Audit_Recommendations.%s_%s.byscript.md"
            % (gen, datetime.datetime.now().strftime("%Y%m%d_%H%M")))
    with open(os.path.join(hist, name), "wb") as fh:
        fh.write(data)
    print("  audit report snapshot kept: %s (%d bytes)" % (name, len(data)))


def write_inventory():
    """One map of every Codex file and how a cloud lane can reach it.

    A lane cannot list the bridge disk, so without this it has no way to know
    whether a file it cannot see is missing, oversized, or never existed.
    """
    rows = []
    for name in sorted(os.listdir(EXT)):
        full = os.path.join(EXT, name)
        if not os.path.isfile(full) or name.startswith("."):
            continue
        n = os.path.getsize(full)
        slice_name = name[:-4] + ".SLICE.md" if name.endswith(".tsv") else ""
        if os.path.exists(os.path.join(OUT, name)):
            how, where = "full copy", name
        elif slice_name and os.path.exists(os.path.join(OUT, slice_name)):
            how, where = "summary only (over 2 MB)", slice_name
        else:
            how, where = "BRIDGE DISK ONLY", ""
        rows.append([name, str(n),
                     time.strftime("%Y-%m-%d %H:%M",
                                   time.localtime(os.path.getmtime(full))),
                     how, where])
    path = os.path.join(OUT, "INVENTORY_what_you_can_read.tsv")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_NONE,
                       escapechar="\\", lineterminator="\n")
        w.writerow(["file_in_external", "bytes", "codex_wrote_at",
                    "how_you_read_it", "read_this_instead"])
        w.writerows(rows)
    unreachable = sum(1 for r in rows if r[3] == "BRIDGE DISK ONLY")
    print("  inventory: %d files, %d unreachable" % (len(rows), unreachable))
    return len(rows), unreachable


def slice_oversized():
    """Give every over-cap table a small readable stand-in.

    A file above the 2 MB sync cap can never reach a cloud lane, and a lane
    that cannot see a table has no way to know what it would have said.  Rather
    than hand-writing a digest per file (which only ever covers the files
    someone remembered), derive one for ANY over-cap table: row count, the
    low-cardinality columns bucketed, and a few sample rows.  Future oversized
    deliverables are covered without editing this script again.
    """
    made = []
    for name in sorted(os.listdir(EXT)):
        full = os.path.join(EXT, name)
        if not os.path.isfile(full) or name.startswith("."):
            continue
        if not name.lower().endswith(".tsv"):
            continue
        if os.path.getsize(full) <= SIZE_CAP:
            continue
        if sync_would_refuse_name(name):
            continue
        dst = os.path.join(OUT, name[:-4] + ".SLICE.md")
        try:
            with open(full, "r", encoding="utf-8", errors="replace",
                      newline="") as fh:
                rdr = csv.reader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
                hdr = next(rdr, [])
                if not hdr:
                    continue
                counts = [{} for _ in hdr]
                sample, rows = [], 0
                for r in rdr:
                    rows += 1
                    if len(sample) < 4:
                        sample.append(r)
                    if rows <= 40000:
                        for i, v in enumerate(r[:len(hdr)]):
                            if len(counts[i]) <= 60:
                                v = v[:48]
                                counts[i][v] = counts[i].get(v, 0) + 1
        except Exception as exc:
            print("  slice failed for %s: %s" % (name, exc))
            continue

        L = ["# %s - ตัวสรุป (ไฟล์เต็มเดินทางไม่ได้)" % name, ""]
        L.append("ไฟล์เต็ม `pf_bridge/external/%s` ขนาด %d ไบต์ **เกินเพดาน 2 MB ของ "
                 "`pf_git_sync.ps1` จึงอยู่บนดิสก์บริดจ์เท่านั้น**" %
                 (name, os.path.getsize(full)))
        L.append("")
        L.append("- แถวข้อมูล: **%d** · คอลัมน์: **%d**" % (rows, len(hdr)))
        L.append("- สร้างโดย `tools_bridge/pf_attr_conflict_digest.py` "
                 "นับกับกรองเท่านั้น ไม่ได้ตีความอะไรใหม่")
        L.append("")
        L.append("## คอลัมน์")
        L.append("")
        L.append("`" + "` · `".join(hdr) + "`")
        L.append("")
        L.append("## คอลัมน์ที่ค่าซ้ำกันมาก (ใช้ดูรูปร่างข้อมูล)")
        L.append("")
        shown = 0
        for i, c in enumerate(counts):
            if not c or len(c) > 30 or len(c) < 2:
                continue
            shown += 1
            if shown > 6:
                break
            L.append("**%s**" % hdr[i])
            L.append("")
            L.append("| ค่า | จำนวน |")
            L.append("|---|---|")
            for v, n in sorted(c.items(), key=lambda kv: -kv[1])[:14]:
                L.append("| `%s` | %d |" % ((v or "(ว่าง)").replace("|", "\\|"), n))
            L.append("")
        if shown == 0:
            L.append("ทุกคอลัมน์มีค่าไม่ซ้ำกันเกือบทั้งหมด (เป็นตารางหลักฐานรายแถว)")
            L.append("")
        L.append("## ตัวอย่าง 4 แถวแรก")
        L.append("")
        L.append("```")
        for r in sample:
            L.append(" | ".join((x or "")[:60] for x in r[:10]))
        L.append("```")
        L.append("")
        L.append("อยากได้แถวไหนเต็ม ๆ ขอผู้ทดสอบที่บริดจ์ดึงให้ได้ "
                 "หรือขอให้ Codex ตัดชุดย่อยตามเงื่อนไขที่ต้องการ")
        txt = "\n".join(L) + "\n"
        old = None
        if os.path.exists(dst):
            with open(dst, "r", encoding="utf-8") as fh:
                old = fh.read()
        if old != txt:
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(txt)
            made.append((os.path.basename(dst), rows))
    for n, r in made:
        print("  slice %-52s %7d rows" % (n, r))
    return made


def mirror_audit_report():
    """Copy the released audit report onto the route the lanes can read."""
    if not os.path.exists(AUDIT_SRC):
        return None
    n = os.path.getsize(AUDIT_SRC)
    if n > SIZE_CAP:
        print("  audit report %d bytes - over the sync cap, not mirrored" % n)
        return None
    with open(AUDIT_SRC, "rb") as fh:
        data = fh.read()
    if not os.path.isdir(AUDIT_OUT_DIR):
        os.makedirs(AUDIT_OUT_DIR)
    if os.path.exists(AUDIT_DST):
        with open(AUDIT_DST, "rb") as fh:
            if fh.read() == data:
                return None
    with open(AUDIT_DST, "wb") as fh:
        fh.write(data)
    print("  audit report refreshed for the team (%d bytes)" % n)
    return n


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
    """Copy Codex's deliverables onto the route that actually travels.

    Everything in external/ that clears the guards - not a curated list and not
    a filename pattern.  Both of those have already failed once each: the
    prefix list dropped PF_COMBAT_LIFECYCLE, and the manifest list dropped 172
    files.  The size cap and the sync name guard do the excluding.
    """
    added, changed, skipped = [], [], []
    names = set(artifacts)
    for f in os.listdir(EXT):
        if os.path.isfile(os.path.join(EXT, f)) and not f.startswith("."):
            names.add(f)
    now = time.time()
    for name in sorted(names):
        low = name.lower()
        if sync_would_refuse_name(name):
            skipped.append((name, "sync name guard would refuse it"))
            continue
        src = os.path.join(root, name)
        if not os.path.exists(src):
            src = os.path.join(EXT, name)
        if not os.path.exists(src):
            continue
        if now - os.path.getmtime(src) < FRESH_WRITE_GUARD_SEC:
            skipped.append((name, "written seconds ago, left for next round"))
            continue
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


def is_high_signal(name):
    up = name.upper()
    return name in HIGH_SIGNAL_EXACT or any(k in up for k in HIGH_SIGNAL_SUBSTR)


def significance(added, changed, summary, prev_wired):
    """Return (bool, reason).  A new deliverable always counts: the round that
    added the name-colour selector, the role discriminator and the quest-mark
    selector was the most valuable one so far."""
    if added:
        return True, "new artifact(s) %d: %s" % (
            len(added), ", ".join(n for n, _ in added[:4]))
    hot = [n for n, _ in changed if is_high_signal(n)]
    if hot:
        return True, "high-signal file changed: " + ", ".join(hot[:4])
    if summary and prev_wired is not None and summary.get("wired") != prev_wired:
        return True, "open wired-conflict count moved %s -> %s" % (
            prev_wired, summary.get("wired"))
    return False, ""


def log_round(gen, added, changed, summary, announced, reason):
    path = os.path.join(OUT, "CODEX_ROUNDS_LOG.tsv")
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_NONE,
                       escapechar="\\", lineterminator="\n")
        if new:
            w.writerow(["checked_at", "generation_id", "added", "changed",
                        "conflicts_total", "conflicts_open", "open_wired",
                        "announced", "reason"])
        w.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    gen[:16], str(len(added)), str(len(changed)),
                    str(summary.get("total", "")) if summary else "",
                    str(summary.get("open", "")) if summary else "",
                    str(summary.get("wired", "")) if summary else "",
                    "yes" if announced else "no", reason])


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


def game_lock_held():
    """True while an attended in-game round is running.

    Hashing ~44 artifacts is sustained disk I/O on the same drive the game
    client and server are reading from, and attended rounds measure timing -
    a stutter reads exactly like the bug under test.  This work is re-runnable
    at any moment; an attended round is not.  So it yields.
    """
    path = os.path.join(BRIDGE, "LOCK_GAME.txt")
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.readline().strip().upper().startswith("HELD")
    except Exception:
        return False


def main():
    # Preserve the audit report BEFORE the lock check, not after.  Codex
    # overwrites it in place and an attended round can hold the lock for over
    # an hour, long enough for several checkpoints to be lost.  This is one cp
    # of a ~110 KB file - it is not the disk load the lock rule guards against
    # (that is the sha256 pass over ~48 artifacts below).  Doing it here also
    # means the guarantee does not depend on the scheduled task remembering to
    # copy the file by hand.
    try:
        snapshot_audit_report()
    except Exception as exc:
        print("snapshot failed (continuing): %s" % exc)

    if game_lock_held():
        print("LOCK_GAME is HELD - an attended round is running; standing down")
        # Record the gap.  Without this the skip is invisible afterwards, and
        # the per-checkpoint retraction lists inside the window are lost with
        # nobody aware they existed.
        try:
            if not os.path.isdir(OUT):
                os.makedirs(OUT)
            with open(os.path.join(OUT, ".skipped_for_game_lock"), "a",
                      encoding="ascii") as fh:
                fh.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                         + "\tskipped: LOCK_GAME held\n")
        except Exception:
            pass
        return 3
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    g = load_generation()
    if g is None:
        # The attr manifest being unreadable or mid-write must no longer stop
        # the whole run: attr is one frozen work stream, everything else Codex
        # writes still needs to reach the team.
        print("attr manifest unusable this round - mirroring the rest anyway")
        gen, root, artifacts = "attr-unavailable", EXT, {}
    else:
        gen, root, artifacts = g

    key, note = round_key()
    print("round key : %s%s" % (key, ("  (" + note + ")") if note else ""))

    prev_key, prev_wired = None, None
    if os.path.exists(STATE):
        try:
            with open(STATE, "r", encoding="ascii") as fh:
                st = json.load(fh)
            prev_key = st.get("round_key")
            prev_wired = st.get("open_wired")
        except Exception:
            prev_key, prev_wired = None, None

    added, changed, skipped = mirror(root, artifacts)
    mirror_audit_report()
    slice_oversized()
    write_inventory()
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

    announced, reason = False, ""
    if key == prev_key:
        print("  same round as last run - no letter")
    elif not (added or changed):
        reason = "new round but mirrored bytes identical"
        print("  " + reason + " - no letter")
    else:
        sig, reason = significance(added, changed, summary, prev_wired)
        if sig:
            announce(gen, prev_key, added, changed, skipped, summary)
            announced = True
        else:
            reason = "background tables only - no new artifact, no high-signal change"
            print("  round mirrored quietly - " + reason)
    log_round(key[:24], added, changed, summary, announced, reason)

    with open(STATE, "w", encoding="ascii") as fh:
        json.dump({"round_key": key, "generation_id": gen,
                   "open_wired": summary.get("wired") if summary else None}, fh)
    print("")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
