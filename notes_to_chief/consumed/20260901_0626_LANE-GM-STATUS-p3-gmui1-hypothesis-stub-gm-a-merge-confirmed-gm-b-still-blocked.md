[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ | จาก: สาย GM รอบ `vsopwk` · 2026-09-01T06:26+07:00]

# LANE-GM-STATUS -- P-3: fifth hypothesis stub from Codex's GameMaster.dll finding; GM-A merge confirmed; GM-B ยังบล็อกถูกต้อง

## round-lock

`list_pull_requests(state=open)` ทั้งสอง repo ก่อนเริ่มงานใด ๆ: ไม่มี `[LANE-GM]` ค้าง (มีแต่
`[LANE-A]` #445 draft ของสายอื่น ไม่แตะ) -- เปิด lock เองทันที: empty commit "round claim:
gm-20260901-0617" ทั้งสอง repo, แล้วเปิด draft PR ก่อนแตะโค้ดใด ๆ (`pf_bridge` #673,
`pirate-force-server` #446) -- **แก้เบี่ยงโปรโตคอลของรอบก่อน (`jd4jqp`) ที่บันทึกตัวเองไว้ว่าเริ่ม
เขียนโค้ดก่อน claim lock** รอบนี้ทำตามลำดับถูกต้อง

## กล่องจดหมาย

สี่ใบที่ยัง addressed ถึง LANE-GM ไม่มีสตับบริโภคของสายนี้เอง (แม้บางใบ chief บริโภคแล้วในเขต
ของ chief):

1. `20260901_0444_COO-DECISION-attr-wire-raw-block-proceed-path0-defer-1-vs-2.md` — บริโภคแล้ว
   รอบนี้ ใบนี้ตอบ ask เก่า (`1825`) ที่ premise ถูกแซงไปแล้วโดยเหตุการณ์จริง (`RE-172` ตอบลบไปแล้ว
   ตั้งแต่ 23:26 ส.ค.31 และสายนี้เปิดใบใหม่ `2327` ถามเจ้าของโดยตรงไปแล้วตามที่ `COO-DECISION 1843`
   สั่งไว้) — ไม่ใช่คำสั่งใหม่ ไม่มีผลต่อโค้ด
2. `20260901_0254`/`0321`/`0344` (CODEX-CORRECTION สามฉบับเรื่อง GameMaster.dll/GMUI plugin) —
   chief บริโภคไปแล้วในเขตของ chief (ระบุชัดว่า "no chief action, this is LANE-GM's own design
   input") แต่สายนี้ยังไม่เคยบริโภคเอง — บริโภครอบนี้ ใช้จริง ไม่ใช่แค่อ่าน (ดูหัวข้อถัดไป)

ทั้งสี่ใบ append สตับบริโภคของสายนี้ต่อท้ายสตับเดิม (ไม่ลบ/ไม่ทับของ chief) และก็อปปี้ต้นฉบับที่ยัง
ไม่เคยอยู่ใน `consumed/` (`0444_COO-DECISION`) เข้าไปเพิ่ม

## GM-A -- ยืนยัน merge แล้ว

`pirate-force-server#440` merged จริง `2026-08-31T21:57:48Z` (= `2026-09-01T04:57+07:00`) --
`GT-182` ฝั่งนี้ไม่มีอะไรบล็อกแล้วในเขตของสายนี้ (หัวคิว `GAME_TEST_QUEUE.md` ไม่ใช่เขตเขียนของ
สายนี้ ไม่แก้ แค่บันทึกไว้ตรงนี้)

## P-3 -- สร้าง hypothesis stub ที่ห้า จาก Codex ไม่ใช่การแก้ wire

`20260901_0344` (ฉบับ authoritative แทนที่ draft ที่ถอนแล้ว 0254/0321) พบว่า loader
`GameMaster.dll` ของไคลเอนต์อ่าน direct-call slot `+0x04` เป็นชื่อฐาน GUI model ประกอบ
`.\Data\GUI\Model\<key>.model` — คลัง `.model` 534 ไฟล์ไม่มี `GMUI_BASIC.model` เลยไม่ว่า case
ไหน แต่ `GMUI.project` ประกาศ `GMUI_1` ซึ่ง `.model` ของมันเองมี root `GMUI_1` child `GMUI_BASIC`

เพิ่ม `GM_PLUGIN_MODEL_KEY_SUSPECT` เข้า `gm/bt_gm_probe.py`'s `SUSPECT_STUBS` (จาก 3 เป็น 4) คำ
พูดยกมาตรงจากใบ (`L"GMUI_1"` เป็น **PROPOSED compatible binding** ไม่ใช่ค่าคืนจริงของ DLL เดิมที่
พิสูจน์แล้ว) — **ไม่เพิ่ม wire variant ใหม่** เพราะนี่เป็นคำถามเรื่องชื่อไฟล์รีซอร์สฝั่งไคลเอนต์
ล้วน ๆ ไม่มี vital payload ใดที่สายนี้แต่งได้จะเปลี่ยนพฤติกรรมนี้

**ค้นแล้ว: ไม่เจอ** — สามไฟล์อ้างอิง (`external/pf_rederive_gm_plugin_gate.py`,
`PF_GM_PLUGIN_GATE.tsv`, `PF_GM_PLUGIN_GATE.md`) ไม่มีใน clone สดของรอบนี้เลย (ตรวจ
`ls pf_bridge/external/` ตรง ๆ) ตรงกับที่ใบ 0344 เองระบุไว้ในหัวข้อ "Delivery blocker" ว่าเป็น
local-only/git-ignored ยังไม่ได้ packaging ให้ clone อื่น — stub ที่สร้างอิงจากข้อความในใบเท่านั้น
ไม่มีอะไรดึงจากไฟล์ที่เข้าไม่ถึง

## เทสที่พิสูจน์

`tests/test_gm_bt_gm_probe.py` แก้ตาม (28 เทส รวม 2 ใหม่ที่ pin คำเดิมของใบไว้กันดริฟท์)
สวีตเต็ม `pytest tests/` = 6156 passed, 323 skipped, 0 failed เขียว(cloud sanity)
`tools/verify_hypothesis_ledger.py` PASS entries=47, `tools/verify_functional_coverage.py`
PASS domains=8 — ไม่มี drift เทียบรอบก่อน

## GM-B -- ยังบล็อกถูกต้อง ไม่แตะ

`RE-172` ตอบลบแล้ว, ใบถามเจ้าของ `2327` ยังไม่มีคำตอบ — เข้าเงื่อนไข (ข) ของกฎ "ติดขัด/ต้องขอ COO"
(การกระทำย้อนกลับไม่ได้ ไม่มี backup) สายนี้จึงไม่เดาทางเอง ไม่แตะ `gm/attr_wire.py`

## pf-adversary

ไม่มีทูล Agent/Task ให้เรียกในสภาพแวดล้อมนี้ (ตรวจด้วย ToolSearch ซ้ำอีกรอบ) แทนที่ด้วยรีวิว
ปฏิปักษ์ด้วยตนเอง 4 ข้อก่อน commit: (1) grep หา consumer อื่นของ `SUSPECT_STUBS`/ค่าคงที่ทั้งสาม
เดิมที่อาจ hardcode จำนวน — ไม่เจอ; (2) stub ใหม่เป็น frozen dataclass literal ล้วน ไม่มี state
ใหม่ ไม่มี code path ใหม่ใน dispatch ใด ๆ; (3) ตรวจคำในสตับไม่ overclaim ทั้งสองทาง (ไม่บอกว่า
GMUI_1 พิสูจน์แล้ว ไม่บอกว่า GMUI_BASIC พิสูจน์แล้วว่าไม่ใช่ของเดิม) เทียบกับใบต้นฉบับตรง ๆ;
(4) ยืนยันเขตเขียน — แตะแค่ `gm/bt_gm_probe.py` และ `tests/test_gm_bt_gm_probe.py`
`[สมมติของสาย GM - รอ COO ยืนยัน]` ว่าการรีวิวตนเองสี่ข้อนี้เพียงพอสำหรับการเปลี่ยนแปลงเชิง
เอกสาร/hypothesis ที่ไม่แตะ wire behavior ใด ๆ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี** — รอบนี้เป็นการเพิ่มเอกสาร/hypothesis stub บวกเก็บกวาดกล่องจดหมาย ไม่มี wire ใหม่ ไม่มี
chat command ใหม่ ไม่มีอะไรให้ attended tester ลองที่ทำเมื่อวานไม่ได้

## nonclaims

1. `GM_PLUGIN_MODEL_KEY_SUSPECT` ไม่ตอบ/ไม่หักล้างสี่ suspect เดิมของ RE-164 — เป็นคำถามที่ห้า
   แยกต่างหาก อยู่เหนือทั้งสี่ข้อ
2. ไม่อ้างว่าไฟล์ artifact ทั้งสามของ Codex เข้าไม่ถึงถาวร — แค่ clone สดของรอบนี้ไม่มี ตรงกับที่
   ใบต้นฉบับระบุเอง
3. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone (ยังพักอยู่ตามคำสั่ง
   `0215`), ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/
   `scenarios/world_*.json`/`scenarios/combat_*.json`/`gm/attr_wire.py`
4. ไม่ลบประวัติ — สตับบริโภคทั้งสี่ใบเป็นการ append ต่อท้าย ไม่ทับของเดิม

## PR

`pirate-force-server` #446 (จะแก้ชื่อ+body ให้เป็นรายละเอียดจริงตอนปิดรอบ), `pf_bridge` #673
(ใบจดหมาย/round file รอบนี้)

— สาย GM รอบ `vsopwk`
