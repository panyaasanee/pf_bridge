# รอบ GM `szmgeh` — 2026-08-31T09:27+07:00

## บริบท

ต้นรอบ: ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo (round-lock ว่าง; `pirate-force-server#363` เป็น
`[LANE-B]` draft ไม่ใช่ล็อกของสายนี้ ไม่แตะ) รอบก่อน (`1q7nxu`) ทั้งสอง PR (`pf_bridge#578`,
`pirate-force-server#370`) `merged=true` ยืนยันด้วย `pull_request_read` แล้ว ไม่มีงานหาย ไม่ต้อง
cherry-pick อะไร ทั้งสองสาขาของตัวเองสะอาด ไม่มีงานค้าง (`git log`/`git status` ตรวจก่อน reset) จึง
`reset --hard origin/main` ทั้งคู่แล้วยึดล็อกด้วย empty commit "round claim: szmgeh" เปิด draft
`pf_bridge#581` / `pirate-force-server#373`

## กล่องจดหมาย (ลำดับงานข้อ 1)

grep `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt` คู่ พบสองใบ:

1. `20260831_0828_KA1A-DELIVERY-adhoc-probe-reference-now-inside-the-repo-per-owner-order.md` --
   ยืนยัน `reference_adhoc_probe/` เข้า repo แล้ว (อ่านอย่างเดียว) และ `gm/attr_wire.py` ยัง shelve
   ตาม `COO-DECISION 0350` เหมือนเดิม (ทั้งสองเงื่อนไข: ไม่มี version-confirmation constant ของ
   `UpdateAttrVital`, ตาราง `characters` ไม่มีคอลัมน์ level/hp/class ยังจริง) -- ไม่มีการกระทำเพิ่ม
   บริโภคแล้ว (stub + สำเนาไป `consumed/`)
2. `20260831_0901_GT164-RESULT-bounded-negative-on-suspect-2-plus-field-0x0b-second-is-the-button-visibility-switch.md`
   -- กะ1-A คลิก `BT_GM` จริงครบ 14/14 variant: **ไม่มีตัวไหนเปิด `GMUI_BASIC`** (bounded negative ต่อ
   `RE-164` ข้อ 2) ผลข้างเคียงที่ใหญ่กว่า objective เดิม: `field_0x0b_second` ยืนยันแบบ attended เป็น
   ครั้งแรกว่าเป็นสวิตช์การมองเห็นปุ่ม `BT_GM` **กลางเซสชัน** (ไม่ต้อง relog) 14/14 ไม่มีข้อยกเว้น --
   ฟิลด์นี้รู้จักอยู่แล้วจาก `RE-089`/`RE-104`/`CORE-REQUEST-020` ว่าคุมการมองเห็นตอน login เท่านั้น
   นี่คือมิติใหม่ (mid-session) ไม่ใช่ field ใหม่

ไม่พบ CORE-REQUEST/CHIEF-REPLY ใหม่ที่อ้างเลข GM-0xx ของสายนี้ที่ยังไม่บริโภครอบนี้ (`CORE-REQUEST-GM-043`
ถูกตัดสินและ consume ไปแล้วรอบก่อนหน้า) `GAME_TEST_QUEUE.md` ข้อที่เป็นของสาย GM คือ `GT-164` เอง ตรงกับ
จดหมายข้อ 2 พอดี — ไม่มีใบ GT อื่นของสาย GM ค้างอ่าน

## งานที่ทำ (หน่วยงานจริงหนึ่งหน่วยของรอบนี้)

หน่วยงานที่เลือก: **บริโภคผล `GT-164` เต็มรูปแบบ** -- ปิดหัวใบในคิวทั้งสอง + codify ความรู้ใหม่ที่ discovery
ให้เป็นเครื่องมือ (ไม่ใช่แค่บันทึกคำตอบ) เพื่อเร่งการทดสอบรอบถัดไปตามหลักการข้อ 2 ของสายนี้

1. `pf_bridge/CLIENT_RE_QUEUE.md` RE-164: เติมชั้น attended ใต้ข้อ 2 (ไม่ลบของเดิม), แก้ tag หัวใบเป็น
   `[PARTIAL — #2 CLOSED STATIC+ATTENDED, #4 CLOSED STATIC, #1/#3 NEEDS-ATTENDED-CAPTURE]`, แก้บรรทัด
   pass-criteria ที่ค้างเขียนว่า `BLOCKED` (ล้าสมัยตั้งแต่รอบ `jz4don` ปลดล็อกไปแล้ว) ให้ตรงความจริง,
   เพิ่ม nonclaim ข้อ 6, เพิ่ม link ไปจดหมายผล
2. `pf_bridge/GAME_TEST_QUEUE.md` GT-164: ปิดหัวใบเป็น RESULT พร้อมสรุปผล, เก็บสถานะเดิมไว้อ่านประกอบ
   ใต้หัว "สถานะเดิม (ก่อนผลรอบ szmgeh)" (ไม่ลบ), แก้สัญญาผู้บริโภคว่าปิดแล้ว, เพิ่ม link
3. `pirate-force-server/src/pirateforce_foundation/gm/bt_gm_probe.py`: เพิ่ม `observed_button_visible()`
   (predicate บริสุทธิ์: `field_0x0b_second == 1`), `guaranteed_visible_variant_ids()`,
   `guaranteed_hidden_variant_ids()` -- ไม่มี field/เฟรม/ที่อยู่หน่วยความจำใหม่ อ้างอิงเฉพาะสิ่งที่พิสูจน์
   แล้ว (`GT-164`, `RE-089`, `RE-104`, `CORE-REQUEST-020`) พร้อม docstring nonclaim ชัดเจนว่า "มองเห็นได้"
   ไม่ใช่ "คลิกได้ผล" -- อัปเดต module docstring บอกว่า `GT-164` RESULT ลงแล้วด้วย
4. `pirate-force-server/tests/test_gm_bt_gm_probe.py`: เพิ่ม 12 เทสใหม่ (`ObservedButtonVisibilityTests`)
   ปักตารางการมองเห็นให้ตรงกับใบผล `GT-164` เป๊ะ (3 visible: `second-byte-1`/`both-bytes-1`/
   `all-fields-1`, 11 hidden) กัน drift ถ้ามีใครแก้ generator ในอนาคตโดยไม่รู้ตัว
5. `pirate-force-server/docs/GM_LANE.md`: เพิ่มรอบ `szmgeh` ต่อท้าย (ไม่ลบของเดิม)
6. บริโภคจดหมายทั้งสองใบ (stub `.md.CONSUMED.txt` + สำเนาไป `notes_to_chief/consumed/`)

## pf-adversary self-review

ไม่มี agent `pf-adversary` แยกในอิมเมจนี้ (เหมือนที่รอบ
`GM_20260830_1020_stale-stageable-count-refreshed-plus-gm040-v2.md` เคยบันทึกไว้แล้ว) ทำเป็น self-review
ตรวจทีละ hunk แทนตามธรรมเนียมเดิม: ตรวจ (1) overclaim -- ไม่มี ทุกคำอ้างอิงมีที่มา/เลขบรรทัด ไม่มีการ
อ้าง "ค้นพบใหม่" ทับของที่รู้อยู่แล้ว (แยกให้ชัดว่า field เดิม แค่มิติ mid-session ใหม่) (2) safety --
ไม่แตะ account/permission/GM-elevation logic ใด ๆ เป็น pure metadata เหนือ generator ที่มีอยู่แล้ว ไม่มี
call site ใหม่ (3) เขตเขียน -- แค่ `gm/bt_gm_probe.py` + `tests/test_gm_bt_gm_probe.py` (4) คุณภาพเทส --
ปักค่าตรงจากใบผลจริง ไม่เดา ไม่พบจุดต้องแก้ก่อน commit

## เขียว

`pytest tests/test_gm_bt_gm_probe.py -q` (`pirate-force-server` HEAD หลัง fetch/reset): 26 passed
เขียว(local run รอบนี้) · `pytest tests/test_gm_*.py -q`: 1089 passed, 500 subtests เขียว(local run
รอบนี้)

## nonclaim

1. `GT-164` ปิดแล้วตอบเฉพาะข้อ 2 ของ `RE-164` เท่านั้น -- ข้อ 1/3/4 ไม่ถูกแตะเพิ่มรอบนี้ ข้อ 1/3 ยังเปิด
   รอ attended capture หรือ static RE เพิ่มที่ไม่มีในอิมเมจของ clone นี้ ห้ามอ้างว่า `RE-164` ปิดครบ
2. "ปุ่มมองเห็นได้" ไม่ใช่ "คลิกได้ผล" -- พิสูจน์แล้วว่าแยกกัน (14/14 ที่มองเห็นได้ก็ยังคลิกไม่เปิดสักตัว)
   `observed_button_visible` บอกแค่การมองเห็น ไม่เคยอ้างเรื่องคลิก
3. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/`scenarios/world_*.json`/
   `scenarios/combat_*.json` เลยรอบนี้ ไม่ให้สถานะ GM กับบัญชีที่ไม่อยู่ใน `gm_accounts` ไม่มีการประกาศ
   milestone จากผลที่ได้ด้วย GM
4. warp ด้วย GM ไปเกาะแล้วเห็นเกาะ ไม่ใช่ M2 ผ่าน -- ไม่มีการอ้าง milestone ใด ๆ ในรอบนี้
5. ไม่มี client image/จอในสภาพแวดล้อมนี้เหมือนทุกรอบ -- โค้ดที่เพิ่มรอบนี้เป็นการ codify ผลที่กะ1-A
   สังเกตมาแล้วผ่านการเทสจริงของเขา ไม่ใช่การยิงเฟรมใหม่หรือสังเกตใหม่จากรอบนี้เอง

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ผู้เทสที่ไล่ `RE-164` ข้อ 1/3 ต่อ (connection-context / current-UI object-key) เรียก
`bt_gm_probe.guaranteed_visible_variant_ids()` เพื่อเลือก variant ที่รู้แล้วว่าปุ่ม `BT_GM` จะโชว์แน่ก่อน
เริ่มไล่ suspect ถัดไป แทนที่จะต้องเดาหรือเจอปุ่มหายกลางเซสชันโดยไม่รู้สาเหตุเหมือนก่อนหน้านี้

## PR

- `pf_bridge#581` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready + retitle)
- `pirate-force-server#373` (draft ต้นรอบ ปิดท้ายรอบนี้เป็น ready + retitle + wake-gate commit)

— สาย GM รอบ `szmgeh`
