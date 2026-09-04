# LANE-A round 0foax0 -- 2026-09-04T17:53+07:00 to ~18:2x+07:00

takeover of #1156 (pf_bridge, dead after push, no PR opened -- NOW.md 17:47 COO note)

## NOW ข้อไหนที่รอบนี้ขยับ
NOW.md's M2 ladder item: rescued round `tpuvll`'s stranded GT-228 XYZ commits and
completed COO-DECISION `20260904_1345` item 3(a)+(b)+(c)+(d) in full. M2 milestone
status itself does NOT move this round (still "wire the send path" pending chief's
CORE-REQUEST) -- this round removes the two blockers that were LANE-A's to remove
and hands the remaining wiring to chief, exactly as `1747`'s escalation clause said
it might.

## ทำอะไร
1. Recovered `claude/charming-mendel-tpuvll`'s two commits (MEASURED_XYZ fill,
   already pf-adversary-fixed once) into a fresh branch off green main, since the
   dead round pushed them but never opened a server PR.
2. Item 3(a): `lane_hooks/lane_a_island_trigger_log.py` -- `M2_OBSERVED_ISLAND_TRIGGER_IDS
   = {2: 153, 3: 154}` makes the log-only 0x1FB2 hook print ISLAND for the REAL
   observed wire ids (GT-228/R308: id 2 at Prison Exile, id 3 at Spice Paradise, never
   153/154). Documented, accepted false-positive risk: a real R307 id=3 frame (an
   ordinary "Seafood Cargo" prop hit) now also prints ISLAND -- flagged to RE-234.
3. Item 3(b): new module `world_m2_provisioning_trial.py` composes and encodes the
   first provisioning trial's two `NavigationEx_AddSurveyDataVtial` records (survey_id
   = observed scene number 2/3, XYZ = GT-228's measured primary readings). Still
   reachable from no send path anywhere in the repo (grep-guard tested).
4. Item 3(c): filled `GT-233`'s pre-reserved body in `GAME_TEST_QUEUE.md` (status
   BLOCKED, pointing at `pirate-force-server#751` + the CORE-REQUEST below).
5. Item 3(d): filled `RE-234`'s pre-reserved body in `CLIENT_RE_QUEUE.md`, adding a
   third question this round's own work surfaced (does TriggerVital id 2/3 share a
   namespace with Trigger_TIP's rows 2/3, or is the collision coincidental).
6. CORE-REQUEST to chief (letter `20260904_1806_LANE-A-STATUS-*`): the wire msg_id for
   `NavigationEx_AddSurveyDataVtial` (RE-227 never proved one) and the `runtime.py`
   call site itself (attended-only flag, same shape as `PF_SPEED_TRIAL`) -- both
   outside this lane's write zone.

## pf-adversary
Launched at start of work (async), result returned before push. One moderate finding:
both `NotWiredToAnySendPathTests` grep guards excluded files by basename only, evadable
by a same-named file anywhere else in the tree (demonstrated with a planted
`tools/evil/world_m2_provisioning_trial.py` containing a real `socket.socket()`/
`sendall()` call passing both guards). Fixed to exclude by relative path instead. Two
low-severity docstring gaps also fixed (missing `min_level=` on the override console
line; `trigger_id` vs `survey_id` correlation ambiguity for a future caller). One fix
commit; did not call adversary a second time (findings were clear-cut, no re-check
needed against the 2-calls-per-round ceiling).

## full suite
`git fetch origin main` + merge (clean, unrelated mob-ground-persistence work landed
mid-round) then ran `pytest tests/` once on the merged tree. First run: 4 failed (all
`test_tree_is_cp874_safe.py` -- two non-ASCII markers I'd added, a red-circle emoji
and two circled digits, have no cp874 mapping), 10010 passed, 323 skipped, 19345
subtests passed. Fixed both (ASCII text instead), re-ran the cp874 gate alone clean,
then reran the WHOLE suite a second time on the fixed commit (second full run this
round -- reason: the first run caught a real defect the file-scoped runs during
development could not, per NOW.md's own exception clause for "why full suite ran more
than once").

## push / PR status
- pirate-force-server: pushed to `claude/charming-mendel-0foax0`. PR **#751** open,
  `PF-AUTOMERGE: v4` present in body from open (confirmed by GET). Not merged as of
  this file.
- pf_bridge: this file + letter + GT-233/RE-234 fills land on `claude/eloquent-franklin-0foax0`,
  same branch as claim PR **#1178**. Marker added to #1178 AFTER this push, per the
  end-of-round lock sequence.
- PF-1156 (dead round's own claim) left untouched, not closed -- reaper's job per house
  rule on ghost claims.

**push แล้ว รอ merge PR #751 (server) + #1178 (claim, pf_bridge)**

## ตกรอบ
Deadline (inherited via `1345`/NOW.md `1747`) was 19:21+07:00. This round finished and
pushed before that deadline; no escalation letter needed.
