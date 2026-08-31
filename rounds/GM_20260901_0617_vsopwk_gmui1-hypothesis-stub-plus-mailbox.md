# รอบ `vsopwk` -- 2026-09-01T06:17+07:00

## หนึ่งบรรทัด

Lock เปิดถูกลำดับก่อนแตะโค้ด (แก้เบี่ยงของรอบก่อน), บริโภคจดหมายค้างสี่ฉบับ, เพิ่ม hypothesis
stub ที่ห้า (`GM_PLUGIN_MODEL_KEY_SUSPECT`) เข้า `gm/bt_gm_probe.py` จากข้อมูล Codex เรื่อง
GameMaster.dll loader, ยืนยัน GM-A merge แล้ว, GM-B ยังบล็อกถูกต้อง

## round-lock

`list_pull_requests(state=open)` ทั้งสอง repo ก่อนเริ่ม: ไม่มี `[LANE-GM]` ค้าง (มีแต่
`[LANE-A]` #445 draft ของสายอื่น ไม่แตะ) เปิด lock เอง: empty commit
`round claim: gm-20260901-0617` ทั้งสอง repo แล้วเปิด draft PR (`pf_bridge` #673,
`pirate-force-server` #446) **ก่อน** แตะไฟล์ใด ๆ — แก้เบี่ยงโปรโตคอลที่รอบก่อน (`jd4jqp`)
บันทึกไว้ว่าตัวเองทำผิดลำดับ

## กล่องจดหมาย

สี่ใบบริโภครอบนี้ (รายละเอียดเต็มในจดหมาย STATUS):
1. `20260901_0444_COO-DECISION-attr-wire-raw-block-proceed-path0-defer-1-vs-2.md` — ตอบ ask
   เก่าที่ premise ถูกแซงไปแล้ว ไม่มีผลใหม่
2. `20260901_0254`/`0321`/`0344` CODEX-CORRECTION (GameMaster.dll/GMUI) — chief บริโภคในเขต
   ของ chief ไปแล้ว แต่ LANE-GM ยังไม่เคยบริโภคเอง — บริโภครอบนี้ **ใช้จริง** ไม่ใช่แค่อ่าน (ดู
   หัวข้อ P-3 ด้านล่าง)

ทั้งสี่ใบ append สตับบริโภคของสายนี้ต่อท้ายของเดิม (ไม่ลบ ไม่ทับ) `0444_COO-DECISION` ก็อปปี้
เข้า `consumed/` เพิ่ม (สามใบ CODEX ถูกก็อปโดย chief ไปแล้ว)

## GM-A -- ยืนยัน merge แล้ว

`pirate-force-server#440` merged `2026-08-31T21:57:48Z` (`04:57+07:00` 1 ก.ย.) — `GT-182` ไม่มี
อะไรบล็อกฝั่งนี้แล้ว (หัวคิวไม่ใช่เขตเขียนของสายนี้ ไม่แก้)

## P-3 -- hypothesis stub ที่ห้า (ไม่ใช่การแก้ wire)

ใบ `0344` (authoritative แทนที่ draft ที่ถอนแล้ว) พบว่า loader `GameMaster.dll` อ่าน slot
`+0x04` เป็นชื่อฐาน GUI model — คลัง `.model` ไม่มี `GMUI_BASIC.model` เลย แต่ `GMUI.project`
ประกาศ `GMUI_1` ที่มี child `GMUI_BASIC` เพิ่ม `GM_PLUGIN_MODEL_KEY_SUSPECT` เข้า
`gm/bt_gm_probe.py`'s `SUSPECT_STUBS` (3 -> 4) คำพูดยกจากใบตรง ๆ (`L"GMUI_1"` = PROPOSED
compatible binding ไม่ใช่ค่าคืนจริงพิสูจน์แล้ว) — ไม่มี wire variant ใหม่ เพราะเป็นคำถามชื่อ
รีซอร์สฝั่งไคลเอนต์ล้วน ไม่มี vital ใดแปรผลนี้ได้

**ค้นแล้ว: ไม่เจอ** — `pf_bridge/external/pf_rederive_gm_plugin_gate.py`,
`PF_GM_PLUGIN_GATE.tsv`, `PF_GM_PLUGIN_GATE.md` ไม่มีใน clone สดของรอบนี้ (ตรวจ `ls` ตรง ๆ)
ตรงกับที่ใบ 0344 ระบุเองว่า local-only/git-ignored ยังไม่ได้ packaging stub สร้างจากข้อความใน
ใบเท่านั้น

## เทสที่พิสูจน์

`tests/test_gm_bt_gm_probe.py` แก้ตาม (28 เทส, 2 ใหม่ pin คำเดิมของใบกันดริฟท์) สวีตเต็ม
`pytest tests/` = 6156 passed, 323 skipped, 0 failed เขียว(cloud sanity)
`tools/verify_hypothesis_ledger.py` PASS entries=47, `tools/verify_functional_coverage.py`
PASS domains=8 ไม่มี drift

## GM-B -- ยังบล็อกถูกต้อง

`RE-172` ตอบลบแล้ว ใบถามเจ้าของ `2327` ยังไม่มีคำตอบ เข้าเงื่อนไข (ข) การกระทำย้อนกลับไม่ได้
ไม่มี backup — ไม่เดาทางเอง ไม่แตะ `gm/attr_wire.py`

## pf-adversary -- ไม่มีทูลในสภาพแวดล้อมนี้

ตรวจซ้ำด้วย ToolSearch — ไม่มี Agent/Task ให้เรียก แทนที่ด้วยรีวิวตนเอง 4 ข้อก่อน commit
(รายละเอียดในจดหมาย STATUS) `[สมมติของสาย GM - รอ COO ยืนยัน]` ว่าเพียงพอสำหรับการเปลี่ยน
เอกสาร/hypothesis ที่ไม่แตะ wire

## ที่ไม่ทำในรอบนี้ (เจตนา)

- ไม่แตะ `gm/attr_wire.py`/GM-B (ล็อกเดิม รอเจ้าของ)
- ไม่แก้หัวคิว `GAME_TEST_QUEUE.md` (ไม่ใช่เขตเขียนของสายนี้ แค่บันทึกสถานะ merge ในจดหมาย)
- ไม่เพิ่ม wire variant สำหรับ suspect ที่ห้า (ไม่ใช่สิ่งที่ vital payload แปรผลได้)
- ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
  `scenarios/world_*.json`/`scenarios/combat_*.json`

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — เอกสาร/hypothesis stub บวกเก็บกวาดกล่องจดหมายล้วน ไม่มี wire ใหม่ ไม่มี chat command
ใหม่

## nonclaims

1. `GM_PLUGIN_MODEL_KEY_SUSPECT` ไม่ตอบ/ไม่หักล้างสี่ suspect เดิมของ RE-164
2. ไม่อ้างว่าไฟล์ artifact สามไฟล์เข้าไม่ถึงถาวร — แค่ clone สดของรอบนี้ไม่มี
3. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json` ไม่ประกาศ milestone ใด ๆ (ยังพักตามคำสั่ง `0215`)
4. ไม่ลบประวัติ — สตับบริโภคทั้งสี่ใบ append ต่อท้าย ไม่ทับของเดิม
5. GM-B ไม่มีความคืบหน้า — รอเจ้าของเคาะทาง 1/2 เหมือนเดิม

## PR

`pf_bridge` #673, `pirate-force-server` #446

— สาย GM รอบ `vsopwk`
