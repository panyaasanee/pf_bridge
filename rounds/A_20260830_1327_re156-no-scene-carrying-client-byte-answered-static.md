# LANE-A round `re156-answer` (2026-08-30T13:27+07:00)

Opened 2026-08-30T13:27+07:00 (Bangkok). Heartbeat at round start:
`_BRIDGE_HEARTBEAT.txt` last line 2026-08-30T13:22, 5 minutes old (well
within the 60-minute rule). This is the round immediately after `qp7brn`'s
first empty round, so Rule F (no two empty rounds in a row without picking
up (a)/(b)/(c)/(d)) is live this round.

## Section A -- last round's PR

`qp7brn` was a documented zero-diff round (no PR opened, per its own record
`A_20260830_1226_qp7brn_no-build-all-fronts-blocked-on-attended-work.md`).
Nothing to merge-check for that round specifically. The round before it
(`n8fq3w`) was already confirmed merged by `qp7brn` itself
(`pirate-force-server#304`, `pf_bridge#482`, verified via `pull_request_read`
`get`, not the unreliable `list` `merged` field). Re-verified this round:
`git merge-base --is-ancestor` for the tips both rounds cite still holds on
current HEAD `e677f49`. Nothing to salvage.

## Section B -- mailbox

Read every file added to `notes_to_chief/` since `qp7brn` closed
(2026-08-30T12:26 through 13:22): all `ADDRESSEE:` header hits for `LANE-A`
already carry a `.CONSUMED.txt` stub. The one substantive item relevant to
this lane's own modules is `20260830_0817_COO-DECISION-door-reader-precedence
-not-ruled-yet-gate-0941-is-the-real-fix.md`, which answers this lane's own
`ASK-COO 20260830_0115` and requires **no further action from Lane A** (COO's
own words: "ไม่ต้องทำอะไรเพิ่มเรื่องนี้ ทำงานอื่นต่อ"). Confirmed the gate it
names (`scene_admission_gate.strip_frozen_legacy_population`, wired into
`runtime.py` same round as `TheOptInBootHazardTests`'s closure) is present at
HEAD (`grep -n "scene_admission_gate" src/pirateforce_foundation/runtime.py`
hits at lines 6645-6823) -- the D1 hazard `pf-adversary` found in round
`vvy6q7` is closed, not still open. Mailbox otherwise clean.

## Why `qp7brn`'s "no build" could not just repeat

Re-walked every item `qp7brn` listed as blocking, per this round's own
instructions (steps 1-6):

1. **`GT-134`** (Bg0015/scene-14 first-eyes) -- confirmed `[READY]`, and its
   remaining precondition ("must see merge sha of `pirate-force-server#290`
   on main") is now actually satisfied: `git merge-base --is-ancestor
   50f010a HEAD` returns true on current HEAD `e677f49`. Still genuinely
   needs a human in front of the client (`G-OBS`) -- nothing left for source
   work.
2. **`RE-155`** (NPC/mob name colour) -- still `NEEDS-ATTENDED-CAPTURE`,
   static ceiling hit three times over (`RE-067`/`RE-068`/`RE-109`). Nothing
   changed since `qp7brn` read it.
3. **M2** -- still paused by the owner directly.
4. **`scene_admission_gate`'s scene-confirmation gap** -- `qp7brn` recorded
   this as "a permanent measured protocol limitation, not an open task," but
   `COO-DECISION 20260830_0946` ITEM 2 explicitly opened it as a queue
   ticket, `RE-156 SCENE-IDENTITY-SIGNAL-001 [STATIC-ON-BRIDGE]`, with two
   pass criteria answerable purely from committed source (no attended
   session, no code change required by the ticket's own objective). `qp7brn`
   apparently read the *problem* but missed that a *ticket* already existed
   for it by the time it closed (the ticket was opened by chief round
   `hd6tac` at ~10:5x, before `qp7brn` opened at 12:23) -- worth flagging so
   this doesn't repeat: check `CLIENT_RE_QUEUE.md` for new `RE-*[STATIC-ON-
   BRIDGE]` tickets touching this lane's own modules every round, not only
   the ones already cited in the previous round's file.

Also re-checked `docs/FUNCTIONAL_COVERAGE.json` domains directly (not by
grepping message strings in `src/*.py`, per house rule): `npc_interaction`'s
`next_missing_behavior` is `quest_accept_and_progress` (already recorded
in-progress, blocked on two independent evidence gaps named in that row --
no new source work available there this round) and `movement`'s is
`remote_player_movement_projection` (not this lane's open thread today).
Neither produced a Rule-F(a)/(d) item beyond what `RE-156` already gave under
(b).

## What was built this round

**Not a code change.** `RE-156` is a `[STATIC-ON-BRIDGE]` ticket whose own
objective says explicitly "do not fix code in this ticket" -- it asks two
factual questions answerable from committed source.

🔴 **CORRECTION (pf-adversary, before commit): the first draft of this
round's `RE-156` answer had a CRITICAL false claim.** It asserted "0/14
`parse_*` functions carry a scene field, no client->server scene byte exists"
by grepping the literal word "scene" inside each `parse_*` function's own
body/docstring. That method has a structural blind spot: `parse_action_vital`
(`current/pf_login_game_server_v141.py:3250-3284`) never says "scene" in
itself, but one of its four "opaque tail fields," `field_u16_4a` (offset
`0x12`), is named and consumed as `scene_id` by a *different* already-shipped
module, `src/pirateforce_foundation/action_ack.py:8-11,63`
(`SceneActionAck.scene_id`, compared against `fields["field_u16_4a"]`). That
module is wired into live dispatch at `runtime.py:247,6483-6501` (unlike
`TeleportCheckVital`, which genuinely has 0 hits there) -- gated behind CLI
flag `--scene-load-scenario` (`app.py:98,287-288`), not the flagless default
path. Two real-client `runtime_pass` captures show *different* values that
match two different real scenes: `reports/PF_SCENE006_EA7D_ATTACK_COMMAND_
RUNTIME_PASS_20260815.md:21` (scene 2) and `reports/PF_SCENE007_PORT_ROYAL_
EA7D_ACTION_ACK_RUNTIME_PASS_20260816.md:13,27-28` (scene 1, Port Royal). The
first draft's own test-of-itself (grep "scene" per function body) could not
see this cross-file semantic naming, and reported the narrower question it
actually answered as the wider one the ticket asked. The full corrected
answer, with all citations, is in the (rewritten, not patched) result letter
`notes_to_chief/20260830_1327_RE-156-RESULT-no-scene-carrying-client-byte-
teleport-check-echo-is-the-nearest-proxy.md`.

**Corrected objective-1/2 answer:**

1. **Objective 1 (does any client->server byte carry a scene id) is now
   POSITIVE, not negative.** `ActionVital.field_u16_4a` is that byte, per the
   citations above.
2. **But it is not usable as a scene-identity signal today, for three
   independent reasons, each measured, none hypothetical:** (a) it is behind
   an opt-in flag, not the default boot path; (b) it belongs to the
   **combat** domain (`docs/FUNCTIONAL_COVERAGE.json`'s `combat` domain cites
   `action_ack.py` under `attack_command_producer`/`action_acknowledgement`),
   not the `world`/`travel` domain `RE-156` was actually asked about
   (`scene_admission_gate.py`/`world_travel_gate.py`), and the module itself
   is marked `# PF-HYPOTHESIS-LEDGER: HYP-PF-002 frozen` -- out of this
   lane's write zone and not this lane's call to unfreeze; (c) live-tracking
   is unverified: the two captures are two different sessions/boots, not one
   session that crossed scenes and was observed to change value, so the
   static evidence cannot separate "the client writes its live current
   scene" from "this value happens to be baked per test scenario and
   coincidentally matched each scenario's own scene." This is the open
   question `pf-adversary` named and nobody has run the experiment for.
3. `TeleportCheckVital` (0 hits in `runtime.py`, constant-value echo never
   proven to vary by scene) and `TargetPosVital`/`GetWorldInfoVital` (no
   scene field at all) still stand exactly as the first draft described --
   only the headline "nothing exists" claim is withdrawn, not those two
   paragraphs.

This closes `RE-156`'s wire/DB-layer pass criteria with a **positive,
bounded** answer (previously mis-closed as a negative one). The
client-observable live-tracking question is split into a new ticket,
`GT-158 ACTIONVITAL-FIELD-U16-4A-LIVE-SCENE-TRACKING-001`, opened this round
in `GAME_TEST_QUEUE.md` (per this lane's own rule: hit an unknown, open a
ticket, keep moving -- do not stop to research it here).

## nonclaims

1. Does not claim `field_u16_4a` is proven to live-track the client's current
   scene -- the two captures are two different sessions; hypothesis (A) live
   tracking vs (B) baked-per-scenario coincidence is undecided, and is
   `GT-158`'s whole job.
2. Does not claim this is usable as a scene-identity signal in production
   today -- it is behind `--scene-load-scenario`, not the default path.
3. Does not claim this lane (WORLD) has any right or plan to touch
   `action_ack.py` or its `runtime.py` dispatch -- combat domain, frozen
   hypothesis (`HYP-PF-002`), outside this lane's write zone. No CORE-REQUEST
   is made from this finding; see the CORE-REQUEST section below.
4. Does not withdraw the first draft's `TeleportCheckVital`/`TargetPosVital`/
   `GetWorldInfoVital` findings -- those were independently correct and
   stand; only the "therefore nothing exists" headline is corrected.
5. Zero diff under `src/ scenarios/ tools/ current/ tests/` in
   `pirate-force-server` this round, before and after the correction -- this
   was a read-only RE answer plus a queue-ticket write, not a code build.

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี -- รอบนี้ไม่ใช่การเปลี่ยนแปลงในเกม แต่เป็นการตอบคำถามพื้นฐานของโปรโตคอล
(`RE-156`) ที่ COO สั่งบันทึกไว้ ไม่มี PR ต่อ `pirate-force-server` รอบนี้
เพราะไม่มีอะไรให้ build ตามขอบเขตของใบนี้เอง (มันห้ามแก้โค้ดตรงๆ)

## Verification performed

- `git merge-base --is-ancestor 50f010a HEAD` (pirate-force-server) -- true,
  confirms `#290` (scene-14 door + D3) is on main.
- `grep -n "scene_admission_gate" src/pirateforce_foundation/runtime.py` --
  hits at 6645-6823, confirms round `vvy6q7`'s D1 gate is wired.
- `grep -c "teleport_check" src/pirateforce_foundation/runtime.py` -- `0`
  (still correct after the correction pass).
- Independently re-read `action_ack.py` in full, `runtime.py:240-6510`
  around the cited dispatch block, `app.py:90-100,280-295`, and both
  `PF_SCENE006`/`PF_SCENE007` reports in full (not just the quoted lines) to
  confirm `pf-adversary`'s finding before rewriting the letter -- confirmed
  independently, not taken on the adversary's word alone.
- `sha256sum` on all thirteen evidence files now cited across both letters
  (five from the first draft, re-verified unchanged; eight new for the
  correction: `action_ack.py`, `test_action_ack.py`, `app.py`, both
  `PF_SCENE00[67]` reports, `runtime.py`, `logout_hypothesis.py`,
  `world_travel_gate.py`, `scene_admission_gate.py`). All match what is
  quoted in the corrected result letter.
- `grep -n "GT-158\|RE-158"` on both queue files before appending -- 0 hits,
  confirms the number was free.
- Did not run the full `pirate-force-server` test suite this round: zero
  source files were touched (`git status --short` empty in
  `pirate-force-server` before, during and after both the original pass and
  the correction pass), so there is no new behaviour to regress-test.
  Confirmed via `git status --short` rather than assumed.

## Files touched this round

- `pf_bridge/rounds/A_20260830_1327_re156-no-scene-carrying-client-byte-answered-static.md` (this file, new, then revised in place for the correction)
- `pf_bridge/notes_to_chief/20260830_1327_RE-156-RESULT-no-scene-carrying-client-byte-teleport-check-echo-is-the-nearest-proxy.md` (new, then fully rewritten in place -- not patched -- after `pf-adversary`'s finding)
- `pf_bridge/notes_to_chief/20260830_1327_LANE-A-STATUS-re156-answered-still-waiting-on-gt134-re155.md` (new, then revised)
- `pf_bridge/GAME_TEST_QUEUE.md` (+58 lines per `git diff --numstat`, new ticket `GT-158`, appended at end of file; nothing else in the file touched)

Zero diff in `pirate-force-server` (`src/ scenarios/ tools/ current/ tests/`)
this round, before or after the correction. `CLIENT_RE_QUEUE.md` header for
`RE-156` is **not** edited by this round -- the ticket was opened by chief,
not by this lane, and this lane's write zone limits ticket-header edits to
tickets it owns/opened; the corrected result letter is handed to chief to
close per the project's own "opener closes" convention (matching how
`RE-150`/`RE-154` were closed by their openers from RE-runner result
letters). `GT-158` **is** written directly into `GAME_TEST_QUEUE.md` by this
round, because this lane is the one opening that ticket (matching the
precedent of `RE-155`, which round `lg1dvz` opened directly).

## CORE-REQUEST

none. The flag-gating discovery (`action_ack.py`'s scene-ack path is real,
wired, and reachable only behind `--scene-load-scenario`) is real and
matches this lane's own charter language about probes-behind-flags almost
exactly -- but the module is combat domain, frozen under `HYP-PF-002`, and
outside this lane's write zone, so this lane is not the one to request
flipping it default-on. Flagged for COO/chief in the paired STATUS letter to
route to whichever lane owns combat/`HYP-PF-002`, and gated on `GT-158`'s
live-tracking answer regardless -- flipping a frozen hypothesis to default-on
before knowing whether the value it would expose is even meaningful would be
the "fabricated row" this project's own rules forbid.

## Next round candidates

- `GT-158` needs an attended session; flag it the same way `RE-152`/`RE-149`
  were flagged, and note it is combat-domain, not exclusively this lane's to
  run.
- If a future `pf-adversary` pass finds this correction still incomplete
  (e.g. another undecoded/mis-scoped field), that is a new/amended finding,
  not a reason to distrust this letter's specific citations -- every claim
  in it was independently re-derived from source in this round, not copied
  from the adversary's report text.
- `GT-134` and `RE-155` remain the two attended-only threads from before;
  nothing new to add there this round.
