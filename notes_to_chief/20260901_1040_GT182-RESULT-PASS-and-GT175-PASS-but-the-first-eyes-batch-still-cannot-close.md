# GT-182 [PASS] · GT-175 [PASS] · the rest of the first-eyes batch is UNGRADED

TO: chief (one addressee)
FROM: ka1-A (attended session; Panya drove every keystroke herself)
WHEN: 2026-09-01 ~10:40 +07:00 (approximate)
BOOT: jobs 1403 hold+resolve / 1404 boot / 1405 stop-recorder / 1406 teardown / 1407 release
BOOT_COMMIT 3ce8ab1682f82b783be0ba9b9fa596fc032e9ab8 · HEAD at acquisition
8346ee8060cc3316c7275d7fa2927e781c4432ae · flagless · run DB
run_gt182_20260901_094056.sqlite3 · capture `capture_gt182_20260901_094056`
NO VIDEO this round - the owner asked for none mid-round; job 1405 stopped ffmpeg and deleted
the file. Everything below is wire + her screenshots.

## GT-182 [PASS] - all three claims, on the FIRST warp of a login

client-observable: `/warp 3` with no coordinates, typed in the ordinary chat box mid-session.
Screen changed to Spice Paradise Island with no relog. Landed at X:-21,215 Y:16,907, standing
on ground, walkable immediately (no floating, no structure trap - F-2 from GT-172 does not
reproduce on the no-coords form). Creatures were on screen **before she moved**.

wire:
    LANE_GM_CHAT_WARP_CROSS_SCENE_NO_COORDS_TELEPORT_VITAL (73 bytes)
    WORLD_POP_HANDOFF scene=3 kind=census actors=62 wire=62 pc=11485B frame=11498B
      reapply_ms=3000 slot=after_teleport reason=scene_3_repopulated_from_bg0003_roster
    WORLD_CENSUS_BG0003 assembled=62/72 shippable=62 bodies=ok
      anchor=(-21215.000,16907.000,-830.000) source=bg0003_full_roster
      shortfall=identity_unresolved=10 unresolved=10
    [G>] WORLD_CENSUS_LANE_SCENE3_INITIAL_62 (11498 bytes)
    [G>] WORLD_CENSUS_LANE_SCENE3_REAPPLY_62 (11498 bytes)

The anchor equals the destination's pinned spawn, not the departure coordinates. **F-1 from
GT-172 is closed for this path** (GM-045 + GM-047 did it).

## GT-175 [PASS] - scene 3 first eyes

She named, on screen, from the 62: Sand dragon x3, Columbus, Spice Merchant Reyna, then
Wizards and Plato while walking. Census shortfall is 10 unresolved identities out of 72 -
that is a separate, already-known ticket, not a GT-175 failure.

## The rest of the batch: DO NOT GRADE

GT-171 / 173 / 174 / 166 / 187 stay `[PENDING]`. She reached scenes 5, 6, 7, 8, 9, 10, 11, 14
and 1 and every one was empty, **but that observation cannot answer a first-eyes ticket**:
letter 20260901_1035 measures the cause as a once-per-connection latch
(`runtime.py:7572 world_census_sent`) that silences every census after the first of a login.
The rosters are all registered in `ROSTER_COMPOSERS`. An empty screen here is the latch, not
the scene. Grading any of them FAIL now would write a lie into the matrix - it is the same
trap as the GT-172 round's warn, one door further along.

Same reason GT-146 and the mob-hit tickets stay out: PANYA-ORDER 20260901_0215 is still in
force and P-1/P-2 are not done.

## Two client-side findings that need their own tickets

**(C-1) "13 seconds no data" banner while the server is answering every frame.**
She walked for a while and the client raised a lost-connection banner. Console for that
window: 284 inbound frames, 277 `[HB>] exact empty RuntimeRes v4` replies, zero errors, zero
tracebacks, socket never closed. Hypothesis, UNPROVEN and to be written as a hypothesis:
the client does not count an *empty* RuntimeRes as data for its own liveness timer. If that is
right, the fix is a non-empty heartbeat, and it is an RE question first (what does the frozen
v141 put in that reply?), not a runtime edit.

**(C-2) After the banner the client kept walking and kept selecting NPCs, and warps stopped
taking effect visually** - but the wire shows the frames still arriving and still being
answered. Whether C-2 is a second bug or just C-1 plus the census latch is not measured.

## Teardown (job 1406) - clean

ports free (listeners 0), GameClient 0, ffmpeg 0, stopped markers 1, traceback markers 0,
stderr small, INTEGRITY ok, FK_ROWS 0, OPEN_SESSIONS 0, MAX_LEASE 14.
canonical UNCHANGED: 4FF37060D3A2E876A41A479A348E062557D6C2FA2FF355548FAF81830A548454
before and after. Run DB moved as expected (throwaway).

**One thing to look at in the DB AFTER:** the stored row is
`('Arena01', scene 3, 24243.0, 2579.4, 3787.0)` - she ENDED the session in scene 1 after
`/warp 1`, and scene 3's row is the pre-round value, unchanged. So a live cross-scene warp
still does not move the durable position (consistent with GT-172 F-3, now seen from the other
side). Not a defect by itself - `_checkpoint_exact_target` is gated on purpose - but somebody
should say out loud whether that is the intended rule, because it means a warp is never
recoverable across a crash.

## NONCLAIMS

- No claim about whether a SECOND census in one connection renders. Never measured; the latch
  has always prevented it.
- No claim about scene 14 / bg4001 or scene 997 specifically; they were reached and empty,
  same latch, no separate evidence.
- `/warp 12`, `13`, `15`, `17` were REFUSED by design (`scene_has_no_login_entry`) - correct
  behaviour, not a finding.
- `/warp 126` and one `/warp 3` were STAGED for next login rather than sent live (markerless
  rule) - correct behaviour, not a finding.
