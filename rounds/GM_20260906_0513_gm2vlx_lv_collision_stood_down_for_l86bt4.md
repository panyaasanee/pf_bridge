# LANE-GM round `gm2vlx` -- 2026-09-06T05:13+07:00 (closing a messy session honestly)

This file closes out TWO things on the same branch (`claude/pensive-wright-u6wd1g`),
because that is what actually happened this session, not because it is tidy:

1. Round `vz8mru`'s own pf_bridge documentation never reached `main` (claim PR
   `#1414` was closed-never-merged by a reaper bug, see below) -- its commits are
   still on this branch and are being carried forward rather than redone.
2. Round `gm2vlx` (this round's own claim) attempted PANYA-ORDER `20260906_0155`
   (`/lv <n>`), built a complete implementation, and is standing it down: a
   different session's round (`l86bt4`) built the same feature more rigorously,
   claimed the lock seven minutes earlier on the server side, and its PR is
   still open. This file says why, in full, rather than quietly deleting the
   work.

## Part 1 -- what happened to round `vz8mru`'s pf_bridge side

Round `vz8mru`'s actual work (P-3: the GMUI-caption/GMTOOL-log-type join, tried
and refused) is real and safe: its server PR (`pirate-force-server#878`) merged
cleanly to `main` hours ago. What did NOT land is this repo's own record of that
round -- `rounds/GM_20260906_0244_vz8mru_gmui_log_type_join_tried_and_refused.md`
and its addendum -- because the claim PR carrying them, `pf_bridge#1414`, was
closed by an automated guard at `2026-09-05T21:00:53Z`
(`notes_to_chief/consumed/20260906_0402_SYNC-NOTICE-pf_bridge-pr1414-closed-never-merged.md`):
*"this claim pull request carries the automerge marker but only 1 file(s) differ
from main, 75 minutes after it was opened."* That reading does not match what was
actually pushed (the claim file, then a 260-line round file, then a 40-line
addendum, each its own commit) -- `ka1-B`'s letter
(`notes_to_chief/20260906_0445_KA1B-TO-CHIEF-reaper-unripe-claim-guard-closed-1386-1410-1414-proposed-fix.md`)
reports the same guard closed three claims (`#1386`, `#1410`, `#1414`) this
session and proposes a fix -- not this lane's to diagnose further, and not
repeated here. The SYNC-NOTICE's own instruction is explicit: *"the branch is
kept... do not start the round over... re-open a pull request from the same
branch."* That is what this round does: the branch still carries commits
`d4258cfe`/`63b5e8e5`/`9b262a82` untouched, and this claim PR carries them
forward rather than re-deriving that work.

## Part 2 -- round `gm2vlx`: `/lv <n>`, built, then stood down

### What this round did, in order

1. Round-lock check at start (per `prompts/COMMON_LANE_ROUND.md`): no
   `[LANE-GM]` PR open on `pf_bridge` -> claimed.
2. Mailbox check -- **with a bug fixed this time**: round `vz8mru` had grepped
   `ADDRESSEE: GM` instead of `ADDRESSEE: LANE-GM` (this lane's real tag) and
   missed `PANYA-ORDER 20260906_0155` entirely; that PANYA-ORDER surfaced only
   by accident, mid-merge, at the end of round `vz8mru`. This round's mailbox
   grep used the correct tag from the start.
3. Built a complete `/lv <n>` implementation on `pirate-force-server` branch
   `claude/keen-pasteur-u6wd1g`: `_lv_action` in `gm/chat_command_action.py`,
   two notice-text constants in `gm/say_wire.py`, a new
   `tests/test_gm_lv_action.py` (23 cases). Design: writes `characters.level`
   through `store.write_typed_attributes` (LANE-DB's existing generic typed
   writer, the same door `/speed` uses), withholds the live `UpdateAttrVital`
   (0x309A) send unconditionally (same posture `/speed` has held since
   `GT-193`), and relies on `legacy_bridge.py`'s already-shipped login composer
   to show the new level after a relog.
4. Ran `pf-adversary` twice. First pass found and this round fixed: a
   production import of a reserved LANE-DB scaffold module
   (`persistence_standard_status`) that a dedicated test forbids; a real,
   demonstrable bug in the shared notice-sent console printer that hardcoded
   `/speed`'s frozen notice text for every caller (a successful `/lv` printed
   `notice='SPEED DENIED'`); missing test coverage on the
   readback-unusable/undo branch; and an unconditional claim about the login
   path that omitted a real caveat (the login-vitals resolver's own
   "all three or none" rule). All four fixed, tests added, full suite green
   (11650+ passed, 0 new failures) before the second adversary pass and before
   push.
5. Pushed, opened `pirate-force-server#886`, confirmed the `PF-AUTOMERGE: v4`
   marker via GET.
6. **Then**, merging fresh `origin/main` into this pf_bridge branch to write
   this very round file, found `rounds/GM_20260906_0412_l86bt4_slash_lv_writes_the_level_row.md`
   already on `main` -- a DIFFERENT session's round, same lane, same
   PANYA-ORDER, claimed `pf_bridge#1424` at `04:12+07:00` (twelve minutes after
   the reaper closed `#1414`, into the exact window that closure opened) and
   opened `pirate-force-server#885` at `2026-09-05T22:02:08Z` -- seven minutes
   before this round's own `#886` (`22:09:13Z`).

### Why `#886` stood down rather than both racing

Read `#885` in full before deciding, not just its round file. It is the more
rigorous of the two:

- It found the SAME "all three or none" login-vitals caveat this round's own
  `#886` only noted in a comment, and went further: `login_would_send()`
  actually asks the login path's own resolver **after** the write and reverts
  the row if the login path would not carry it -- `#886` writes the row and
  documents the risk but does not check or guard against it.
- It found the level ceiling this round set at `255` is wrong: the client's
  own `STANDARD_STATUS` table tops out at row `255`, but its XP bar indexes
  that table by `level + 1` (a fact this round's own research never surfaced),
  so `255` is one past the last safe row -- the real ceiling is `254`.
- It found and fixed a `section 7` para-mark-versus-plain-text `cp874` hazard
  in `gm/` source that this round's own tree did not happen to contain, but
  could have.
- Both PRs carry the `PF-AUTOMERGE: v4` marker; both cannot land without
  conflicting (both redefine the `lv` dispatch branch, both add colliding
  constants). Two live claims on one lock resolve by age
  (`prompts/COMMON_LANE_ROUND.md`'s own rule for the claim-PR lock, applied
  here to the same shape of collision one layer down, at the feature-PR
  level) -- `#885` is older and stronger. This round is not the one that
  should win by being the one whose marker fires the automerge race first.

**Action taken**: edited `pirate-force-server#886`'s body to remove the
`PF-AUTOMERGE: v4` marker and state plainly that it stands down for `#885`,
confirmed via GET that the marker is gone. Did not close `#886` (house rule:
a session does not close a PR itself) -- left for chief/COO/the reaper.
Deleted three letters this round had drafted but not yet committed (an RE
ticket request, a LANE-DB coordination note, a GT ticket request) once `#885`'s
own round file showed it had already sent the same three asks, more precisely,
to the same recipients (`notes_to_chief/20260906_0434_LANE-GM-TO-CHIEF-*`,
`0436_LANE-GM-TO-LANE-DB-*`, `0438_LANE-GM-ASK-COO-*`) -- sending duplicates
would have cost chief/DB/COO's attention for nothing new.

### What this round's own `/lv` work is worth, stated honestly

Not nothing, and not claimed as the answer either. `pirate-force-server`
branch `claude/keen-pasteur-u6wd1g` still carries a complete, independently
pf-adversary-reviewed, fully-tested implementation that reached a DIFFERENT
(and in one respect, narrower -- it never attempted the login self-check)
design than `#885`. Kept on that branch, not deleted, in case a future round
finds a piece of it worth comparing against `#885`'s shipped shape -- but this
round does not ask anyone to read it as a live proposal.

## Round lock, stated for both parts

`list_pull_requests` at start of this file's own writing: no `[LANE-GM]` PR
open on `pf_bridge` (checked fresh, after `#1424` closed/merged in the time
between). This claim PR carries both parts above.

## nonclaim (mandatory)

**GM skipped which steps: none.** No account received GM status. No frame
went out on any wire from this round's own commits. `/lv`'s server PR
(`#886`) is explicitly stood down, not landed, not claimed as a feature.

- Does not claim `pirate-force-server#886` will merge -- it is standing down
  by design; the live candidate is `#885`.
- Does not claim `pirate-force-server#878` (round `vz8mru`'s real work) is
  unverified -- confirmed merged (`git log` on `origin/main` shows it via
  merge commit `afcb28b4`) before this file was written.
- Does not claim credit for `/lv` landing, surviving a relog, or unblocking
  LANE-CS -- that is round `l86bt4`'s claim to make, in its own round file,
  which already exists and already says it more precisely than this round
  could.
- Does not diagnose or fix the reaper's unripe-claim-guard bug that closed
  `#1414` -- `ka1-B` already reported it (`0445`) with a proposed fix; a
  second report would be noise.
- Does not re-ask chief/LANE-DB/COO anything `l86bt4`'s round already asked
  (RE ticket, DB coordination, COO limits letter) -- confirmed by reading
  those three letters before deciding not to duplicate them.

TWO_SESSIONS_SAME_SCENE: this round's `pirate-force-server#886` touches no
world/scene state at all -- it is a chat-command DB write and a local-talk
notice, same shape `l86bt4`'s own round already states for `#885`, and it is
standing down regardless.

## next round

1. Confirm `pirate-force-server#885` (round `l86bt4`) merge state with
   `git merge-base --is-ancestor` before writing anything about `/lv` as
   landed.
2. If `#885` is stuck (gate red, reaper silence) longer than a normal cycle,
   a future LANE-GM round may need to actively help land it (not re-build it)
   -- read that PR's own CI state first.
3. Round `l86bt4`'s own "next round" list (COO's `0255` mob-viewer-link
   tripwire scan, P-3 continuation) is still the real backlog once `/lv` is
   off the table one way or the other.
4. If a future round ever wants any piece of this round's stood-down `#886`
   (e.g. its `login_would_send`-equivalent gap does not exist because `#885`
   already covers it -- so most likely: nothing), it is on
   `claude/keen-pasteur-u6wd1g`, not deleted.

SCOREBOARD: NONE | รอบนี้ไม่มีอะไรใหม่ที่ผู้เล่นทำได้เพิ่มจากฝีมือของรอบนี้เอง -- /lv ที่ผู้เล่นจะได้ใช้จริงคือฝีมือของรอบ l86bt4 (PR #885) ซึ่งรอบนี้อ่านแล้วพบว่าละเอียดกว่าและถอยให้ · งานจริงของรอบนี้ (กู้เอกสารรอบ vz8mru ที่เกตพังทำให้ตกหล่น + หยุดการชนกันของสอง PR ก่อนมันทำลายกันเอง) ไม่ใช่สิ่งที่ผู้เล่นเห็นบนจอ | pirate-force-server#878 (บน main แล้ว, ยืนยันด้วย git log) + #886 (เปิดแล้ว ถอนมาร์กเกอร์ ถอยให้ #885) + pf_bridge (claim PR ใบนี้)
