# GT-192 -- the `background` block, verbatim

ย้ายออกจาก `GAME_TEST_QUEUE.md` โดย chief รอบ `xkmzxr`/R306 ตามกฎหัวข้อ 11 (ใบเก็บคำถาม เกณฑ์ สถานะ ลิงก์ ·
ประวัติไปอยู่ที่อื่น) และเพราะใบยาวเกินเพดาน 12,000 อักขระของ `COO-DECISION 20260902_1648`
ไม่มีการลบเนื้อหา และไม่มีขั้นตอนความปลอดภัยข้อไหนถูกตัด — ที่ย้ายคือประวัติของบั๊กล้วน ๆ

- background (read before touching anything):
  - `20260901_1035_KA1A-ROOTCAUSE-*.md`: measured on a live capture (boot 1404,
    `run_gt182_20260901_094056.sqlite3`) that `self.world_census_sent` is a **once-per-TCP-
    connection** latch (`runtime.py:1155`, set at 7785/7996/8016/8122/8250/1384, never reset
    anywhere before this round's fix), so every warp after the session's first census-bearing
    scene arrival was silently dropped -- ten `/warp` chat commands in the owner's own GT-182
    session-2 capture produced exactly two censuses, both for the FIRST scene she landed
    census-eligible in. This is the exact bug this entry checks is now closed.
  - the fix that landed (`runtime.py:5459-5470`, inside `_gm_warp_resync_selected_scene`,
    the same method `CORE-REQUEST-GM-045`/`GM-047` already wired): on a confirmed cross-scene
    GM warp it now resets `world_census_sent`, `world_census_refused`, `last_target_pos`, and
    the sibling fields that describe the OLD scene's placement indices
    (`population_indices`, `world_census_indices`, `population_refresh_anchor`,
    `census_anchor_record`, `npc_idle_action_sent`). Resetting `last_target_pos` matters for
    the SAME reason `GT-182`'s own F-1 finding did: without it, the newly-unlatched census
    would compose the destination roster around the departure scene's stale coordinates.
  - what nobody has measured yet, per `1035`'s own nonclaim: "I did NOT prove the client
    would render a second census in the same session... **The round that lands this must be
    attended-tested before any first-eyes ticket is graded.**" This entry is that attended
    test. `1120`'s amendment does not change any of items 1-3 above; it only blocks item 4
    (scene-1 eager census), which this entry does not exercise.
