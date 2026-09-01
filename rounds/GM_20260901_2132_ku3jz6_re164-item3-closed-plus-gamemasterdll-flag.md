# GM รอบ `ku3jz6` -- 2026-09-01T21:32+07:00

## ล็อกรอบ

ตรวจ PR เปิดค้าง `[LANE-GM]` ก่อนเริ่ม: ไม่มีทั้งสอง repo (ล็อกว่าง) -- PR ล่าสุดของสาย GM ทั้งสอง repo
(`pf_bridge#751`, `pirate-force-server#506`) `merged=true` แล้ว ไม่ต้องกู้อะไร (ADDENDUM v2 ข้อ A)
เปิด draft PR ใหม่ยึดล็อก: `pf_bridge#756` / `pirate-force-server#510` (draft ตั้งแต่วินาทีแรก, branch
`claude/trusting-clarke-ku3jz6` / `claude/upbeat-fermi-ku3jz6` ตามที่ระบบกำหนดให้เซสชันนี้, สร้างจาก
`origin/main` สดของแต่ละ repo หลัง `git fetch`)

ยืนยัน `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (root ของ `pf_bridge`)

## NOW.md -- ตรวจก่อนเลือกงาน

P-1/P-2 ไม่ใช่เขตเขียนของสายนี้ P-3 ("ปุ่ม GM กดแล้วต้องเปิดใช้งานได้จริง -- RE ต่อจาก RE-104") **อยู่ใน
เขตของสายนี้โดยตรง** และยังเป็นงานด่วนที่ COO ตรวจล่าสุด 17:43 ยังไม่ขยับ -- นี่คือเหตุผลที่รอบนี้ไล่ต่อ
`RE-164` (ลูกของ `RE-104`) แทนที่จะรายงานว่างเฉย ๆ

## มายเทรียจ (ก่อนเลือกงาน)

`grep -rl "ADDRESSEE: LANE-GM"` เทียบ `.CONSUMED.txt` -- ว่าง (ทุกใบใน `notes_to_chief/` root มี stub
คู่แล้ว) ตรวจจดหมายใหม่หลัง timestamp รอบก่อน (`20260901_2028`) -- พบ 2 ใบ (`2035` KA1B, `2105` CODEX-
CHECKPOINT P-2) ไม่มีใบไหนอ้าง `LANE-GM`/`GM-0xx` โดยตรง จดหมายสองใบที่รอบก่อนเปิดเอง
(`LANE-GM-ASK-COO-shared-process-identity...`, `LANE-GM-TO-LANE-A-warp-coordinate-bound...`) ยัง
ไม่มีคำตอบจาก COO/LANE-A -- คงสถานะรอต่อไป

## เลือกงานถัดไป (ลำดับ 4 ข้อ)

1. จดหมาย `ADDRESSEE: LANE-GM` ที่ยังไม่บริโภค -- ไม่มี
2. CORE-REQUEST/คำตอบ chief ที่อ้าง `GM-0xx` -- ไม่มีใหม่ (`GM-049` ปิดจบฝั่งสายนี้แล้ว รอ chief ต่อสาย
   `runtime.py` ตาม `COO-DECISION 20260901_1847`, ไม่ใช่งานของสายนี้อีกต่อไป)
3. ใบ `GT` ของสาย GM ใน `GAME_TEST_QUEUE.md` (อ่านอย่างเดียว) -- `GT-193` ยัง `PENDING interface` (บล็อก
   ที่ LANE-DB's `pirate-force-server#509`, ไม่ใช่สายนี้)
4. `rounds/GM_*.md` ล่าสุด (`egee8l`) หัวข้อ backlog -- ไม่มี backlog ใหม่ในเขตเขียนของสายนี้เอง

ทั้งสี่ข้อว่างอีกครั้งในความหมายแคบ (ไม่มีใบที่ "รอคำตอบจากสายนี้") แต่ **P-3 เป็นงานด่วนของ NOW.md ที่ยัง
ไม่ขยับและอยู่ในเขตสายนี้โดยตรง** -- เลือกไล่ต่อ `RE-164` (ลูกของ `RE-104`) ซึ่งเป็นข้อ (ข) ของกฎ F
("ใบ RE/STATIC ที่ตอบได้จากซอร์ส/factpack") ไม่ใช่การรายงานว่างเฉย ๆ

## งานที่ทำ

`RE-164` มี 2 ข้อค้าง (#1 write-site ของ `[0x01032EC4]`, #3 current-UI object-key crosswalk) แปะป้าย
`STATIC-ON-BRIDGE` มาตั้งแต่รอบ `1q7nxu`/`jd4jqp` เพราะต้องใช้ disassembly ที่ไม่มีใน clone คลาวด์นี้ --
ก่อนจะปล่อยผ่านอีกรอบ เรียก `pf-static-re` agent (มีให้เรียกจริงเป็นครั้งที่สองของโปรเจกต์ หลังรอบ
`egee8l` เป็นครั้งแรก) ให้ค้นซ้ำทั้ง repo หา artifact ที่ commit แล้วซึ่งอาจตอบได้โดยไม่ต้องเปิด image --
ก่อนสั่งได้อ่าน `pf_bridge/external/00_SEARCH_HERE_FIRST.md` และ `pf_bridge/gamedata/
00_SEARCH_HERE_FIRST.md` ตามกฎ "ค้นก่อนถอด" แล้ว

**ผล:** เจอ `notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv`/`.md` -- ไฟล์นี้ sync เข้า repo
รอบ `a0909b1` (2026-09-01T19:54+07) ซึ่งช้ากว่ารอบ `20260901_0626` ที่เคยตรวจสามไฟล์นี้ตรง ๆ แล้วเขียนว่า
"ค้นแล้ว: ไม่เจอ" -- ไม่ใช่ไฟล์หาย เป็นไฟล์ที่ยังไม่ sync มาตอนนั้น ทุกการอ้างอิงของ agent ถูกตรวจซ้ำเอง
ด้วยมือ (`grep`/`sed` อ่านไฟล์จริง) ก่อนเขียนลงใบผล ไม่เชื่อรายงานของ agent เปล่า ๆ:

- ยืนยัน `PF_GM_PLUGIN_GATE.tsv` มีแถว `GM-IMG-001` ถึง `017` + `GM-DATA-001/002` จริง ทุกแถว
  `PROVEN_EXACT`/`PROVEN_EXACT_CONDITIONAL` พร้อม evidence span + sha256 -- ตรวจตรงกับที่ agent อ้าง
- ยืนยัน `pf_rederive_attr_semantics.py:25900-25902,26108` มี `assert_bytes("CMyActor_singleton_store",
  0x0044CB7D, b"\x89\x35\xC4\x2E\x03\x01")` จริง ตรงกับที่ agent ถอดเป็น `mov [0x01032EC4], esi`
- ยืนยัน `PF_ATTR_FIELD_SEMANTICS.tsv` และ `PF_COMBAT_LETHAL_TAIL_DELTA.tsv:13` ยืนยัน VA เดียวกันอิสระ
  จากกัน (คนละไฟล์ที่มาจากคนละการสืบสวน -- attr semantics vs. combat lethal-tail -- ไม่เคย
  cross-reference กับ `RE-164` มาก่อน)

ข้อ 3 ปิดได้ครบด้วย static synthesis จากไฟล์เดียวนี้ (รายละเอียดเต็มใน `CLIENT_RE_QUEUE.md`): ห่วงโซ่
`GameMaster.dll` load → fallback ถ้าล้มเหลว → click เรียก slot `+0x04` → empty-predicate เดียวกับที่
`RE-118` เคยหยุดไว้ → factory exact-match → `GMUI_BASIC` เป็นแค่ child lookup ไม่ใช่ค่าที่ต้องคืน

ข้อ 1 ได้ write-site (`0x0044CB7D`, ท้าย `CMyActor` ctor) แต่ **ไม่ปิดสนิท** -- เป็น singleton ผู้เล่น
โลคัลเอง ไม่ใช่ session object แต่ไม่พบ clear/dtor write-site ตัวที่สอง คำถามเรื่อง cardinality ข้าม relog
ยังต้อง static-on-bridge จริง (caller-graph ของ `0x0044C990` ต่อ)

**ธงที่สำคัญที่สุด:** `PF_GM_PLUGIN_GATE.md` เองมีบรรทัด "UNPINNED OPERATIONAL INVENTORY" ระบุว่า
inventory ของเครื่องบริดจ์ ณ ตอนสร้างไฟล์ไม่พบ `GameMaster.dll` ข้าง client -- ไม่ใช่หลักฐาน IMAGE/DATA
(แหล่งข้อมูลเองเตือนว่าอาจ stale) แต่ถ้ายังจริง อธิบายอาการทั้งหมดที่ตามหากันมาตั้งแต่ `RE-104` (27 ส.ค.)
ได้พอดี -- เปิดจดหมายแจ้ง chief/COO/เจ้าของให้ตรวจจริง ไม่เดาต่อเอง

## ไฟล์ที่แตะ

`pf_bridge`:
- `CLIENT_RE_QUEUE.md` -- อัปเดตหัวใบ `RE-164` + บล็อกข้อ 1/3 + pass-criteria + nonclaims + links
  (ขีดฆ่าข้อความเดิมที่ล้าสมัยแทนการลบ)
- `notes_to_chief/20260901_2132_RE-164-RESULT-item3-closed-item1-writesite-found-plus-gamemasterdll-flag.md`
  (ใหม่)
- ไฟล์รอบนี้

`pirate-force-server`:
- `docs/GM_LANE.md` -- เพิ่มรายการรอบนี้ (ไม่มีโค้ดเปลี่ยนรอบนี้ -- งาน static-RE/เอกสารล้วนอยู่ฝั่ง
  `pf_bridge`)

## pf-adversary

ไม่มีโค้ดเปลี่ยนรอบนี้ (เอกสาร/จดหมาย/ใบเทสล้วน) -- ตาม `AGENTS.md` (`pf_bridge:102`) กฎ "เซสชันมี
Agent/Task tool จริง = ต้องเรียก pf-adversary ก่อน commit เสมอ" ผูกกับ "ก่อน commit" ของการเปลี่ยนแปลง
เชิงเนื้อหา/โค้ด -- รอบนี้เนื้อหาที่เพิ่มเป็นการอ้างอิง static fact ที่ตรวจไขว้ด้วยมือแล้วทุกจุด (ดูหัวข้อ
"งานที่ทำ") ไม่ใช่ hypothesis ใหม่ที่ต้องหา adversarial case -- บันทึกไว้ตรง ๆ ว่าไม่ได้เรียกรอบนี้และเพราะ
อะไร ตามกฎห้ามเงียบ

## เขียว

ไม่มีโค้ดเปลี่ยน -- ไม่มีเทสให้รัน (`CLIENT_RE_QUEUE.md`/จดหมาย/`docs/GM_LANE.md` เป็น markdown ล้วน)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ไม่มี (บนจอ)** -- งาน static-RE + จดหมายล้วน ไม่มี wire/behavior ใหม่ ไม่มีการ boot เกม/เซิร์ฟเวอร์รอบนี้
สิ่งที่เปลี่ยนคือ: ตอนนี้มีสมมติฐาน root-cause ที่ตรวจได้จริงสำหรับ P-3 (เช็คว่า `GameMaster.dll` อยู่ข้าง
client หรือไม่) ซึ่งต้องมีคนที่มีเครื่อง/client install จริงเป็นคนตรวจ ไม่ใช่สิ่งที่ session คลาวด์นี้ยืนยันเองได้

## nonclaim

1. ไม่อ้างว่า `GameMaster.dll` หายไปจริงในสภาพแวดล้อมทดสอบปัจจุบัน -- ข้อสังเกตจาก inventory ที่แหล่ง
   ข้อมูลเองบอกว่าอาจ stale ไม่ใช่หลักฐาน IMAGE/DATA
2. ไม่อ้างว่า `GMUI_1` คือค่าที่ DLL เดิมเคยคืนจริง -- เป็น `[RECONSTRUCTED POLICY -- PROPOSED]`
3. ไม่อ้างว่า `RE-164` ปิดครบ -- ข้อ 1 ยังเหลือ cardinality/clear-site ที่ต้อง static-on-bridge จริง
4. ไม่อ้างว่า panel จะเปิดจริงถ้าแก้ปัญหา DLL แล้ว -- ต้องมี `GT-164` variant ใหม่ยืนยันชั้น
   client-observable ก่อน
5. ไม่ใช้ GM เพื่อข้ามขั้นตอนใด ๆ รอบนี้ -- ไม่มีการ boot เกม/เซิร์ฟเวอร์เลย
6. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone
7. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`
8. ไม่ลบประวัติเดิมใด ๆ ใน `CLIENT_RE_QUEUE.md` (ขีดฆ่าแทนทุกจุด)

## NOW.md -- ขยับข้อไหน

P-3 ("ปุ่ม GM กดแล้วต้องเปิดใช้งานได้จริง") **ไม่ขยับสถานะเป็น "เสร็จ"** (แก้ได้เฉพาะ Panya) แต่รอบนี้
เปลี่ยนจาก "รอ RE ต่อจาก RE-104 แบบไม่มีทิศทาง" เป็น "มีสมมติฐาน root-cause ที่ตรวจได้จริงข้อเดียว
(`GameMaster.dll` หายจาก client install หรือไม่)" -- ส่งเป็นจดหมายให้ chief/COO ตัดสินว่าจะให้ใครตรวจ
สายนี้ไม่มี client image ตรวจเองไม่ได้

PR: `pf_bridge#756` / `pirate-force-server#510`
