# LANE-GM round `fmgvbx` — 2026-08-27T19:48+07:00

## เริ่มรอบ
- ยืนยัน `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (อยู่ที่ root ของ `pf_bridge`)
- PR-lock ต้นรอบ (addendum v2 ข้อ A): ไม่มี `[LANE-GM]` PR เปิดค้างในทั้งสองรีโป · เช็คสถานะ merge ของ PR
  `[LANE-GM]` ล่าสุดของแต่ละรีโป (`pf_bridge#223`, `pirate-force-server#138`) ด้วย `pull_request_read(get)`
  ตามคำแนะนำของใบ `20260827_1450_ATTENDED-REPLY-*` (ห้ามเชื่อ `merged` field ของ `list_pull_requests` —
  รู้แล้วว่าเป็น false negative เสมอ) — ทั้งคู่ `merged_at` ยืนยันจริง ไม่ต้อง cherry-pick
- rebase ทั้งสองสาขาเข้ากับ `origin/main` ล่าสุดก่อนเริ่ม (pf_bridge อยู่หลัง main 7 คอมมิต — rebase สำเร็จ
  ไม่ชน) · claim ล็อกด้วย commit เปล่า "round claim: fmgvbx" เปิด draft PR ทั้งสองรีโป
  (`pf_bridge#228`, `pirate-force-server#141`) ก่อนเริ่มงานจริง

## กล่องจดหมาย (บริโภครอบนี้)
สี่ใบ `ADDRESSEE: LANE-GM` ที่ยังไม่มี `.CONSUMED.txt`:
1. `20260827_1450_ATTENDED-REPLY-LANE-GM-1936-*` — ใช้วิธี `pull_request_read(get)` แล้วตามข้อบน
2. `20260827_1425_PANYA-ORDER-GM-warp-to-other-maps-two-paths.md` — path A (login-scene override) merged
   แล้ว รอ GT-110 attended; path B item 3 (decode 0x51E9 → GmCommand, same-scene warp) ก็ merged แล้วจากรอบ
   ก่อน — ตัวบล็อกจริงตอนนี้คือ error ใหม่ที่ GT-107 เจอ ไม่ใช่ของที่ใบนี้ขอ
3. `20260827_1840_KA1A-NOTE-GM-two-gaps-*` — ช่องว่าง 1 (ไม่มีใบ RE) → เปิด `RE-113` รอบนี้ · ช่องว่าง 2
   (`field_0x0b_second=1`) → เขียน `CORE-REQUEST-020` (แก้เองไม่ได้ อยู่ใน `runtime.py`)
ทั้งสี่ใบมี `.CONSUMED.txt` แล้วในรอบนี้ (ไม่ลบต้นฉบับ)

## งานที่ทำ
1. **เปิด `RE-113`** (`CLIENT_RE_QUEUE.md`) — ถามว่า nested reader ของ `0x5A19` หลัง version-check (`RE-105`)
   ผ่านแล้ว อ่านอะไร/ยาวเท่าไร เพราะ `GT-107` เจอ error ใหม่ `28317 GSCN_RunTimeProtocolRes`
2. ส่ง `pf-static-re` ไปสืบ — พบสาเหตุจริงจากซอร์สของเซิร์ฟเวอร์เอง (ไม่ใช่ client binary): `gm/state_wire.py`
   ประกอบเฟรมผ่าน `legacy.make_runtime_vital()` (เอกพจน์) ซึ่งไม่เติมไบต์ change-mask ท้ายเฟรมที่
   `GSCN_RunTimeProtocolRes` v4 ต้องการ — ฟังก์ชันคู่กัน `make_runtime_vitals()` (พหูพจน์) เติมไบต์นี้อยู่แล้ว
   พร้อมคอมเมนต์เดิมที่อ้าง error `28317` ตรงตัว และมีเหตุการณ์เดียวกันถูกพิสูจน์มาแล้ว 3 ครั้งใน
   `reports/PF_DELETE_SOFT002_NATURAL_0x36DB_DECODE_20260818.md`
3. **แก้จริง** (อยู่ในเขตเขียนของสายนี้ทั้งหมด ไม่ต้อง CORE-REQUEST): เปลี่ยน
   `gm/state_wire.py` ให้เรียก `make_runtime_vitals([...])` แทน · เพิ่มเทส regression ยืนยันไบต์ท้ายเฟรม ·
   `tests/test_gm_*.py` 232/232 ผ่าน · ปิด `RE-113` เป็น PASS/DONE พร้อม `BUILD_IMPACT:`
4. เขียน **`CORE-REQUEST-020`** ถึง chief — เปลี่ยน literal argument ตัวเดียวใน `runtime.py`
   (`field_0x0b_second` จาก `0` เป็น `1` ตามที่ `RE-089`/`RE-104` พิสูจน์ว่าเป็นเงื่อนไขของปุ่ม `BT_GM`) —
   อยู่นอกเขตเขียนของสายนี้ และ `lane_hooks.fire()` เป็น report-only ใช้แทนไม่ได้
5. **pf-adversary ก่อน commit** เจอสองจุดผิดในร่างแรก: (ก) `CORE-REQUEST-020` เขียนผิดว่าไม่มีเทสจะพัง — จริง
   ๆ `tests/test_gm_login_state_guard.py`'s hardcoded `(0,0,0,0)` จะแดงทันทีที่ `runtime.py` เปลี่ยน (ข)
   `RE-113` อ้าง `RE-088` ผิด (คนละ vital) ทั้งสองแก้แล้วก่อน push

## ผล
- `RE-113`: **CLOSED PASS/DONE**
- `CORE-REQUEST-020`: เปิดรอ chief
- `docs/GM_LANE.md`: อัปเดต "RE requests closed/open" + เพิ่ม "Modules delivered (round `fmgvbx`, RE-113
  trailing-mask fix)"

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
ยังไม่มี — รอบนี้คือ wire-fact fix + จดหมาย ไม่ใช่ของที่เห็นบนจอ ต้องรอ `CORE-REQUEST-020` ปิดที่ chief ก่อน
ถึงจะเปิดใบเทส attended ใหม่ (GT-107 รอบ 3) ได้อย่างมีความหมาย

## nonclaim
- การแก้ `RE-113` มาจากหลักฐาน [STATIC] (ซอร์สเซิร์ฟเวอร์เอง) + [PROVEN]-committed-report คนละรอบ ไม่ใช่
  [MEASURED] ของรอบนี้ — ยังไม่มีใครยิงเฟรมที่แก้แล้วใส่ไคลเอนต์จริง
- ไม่ claim ว่าแก้ทั้งสองเรื่อง (RE-113 + CORE-REQUEST-020) แล้วปุ่ม `BT_GM` จะขึ้นจริงบนจอ — ต้องรอ attended
  GT รอบใหม่
- ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` เลยรอบนี้ (การแก้ทั้งหมดอยู่ใน `gm/state_wire.py`
  ซึ่งเรียกฟังก์ชันที่มีอยู่แล้วในไฟล์ chief's legacy module โดยไม่แก้ไฟล์นั้น)
- ยังห้ามใส่ `localtest` กลับเข้า `gm_accounts` จนกว่า `CORE-REQUEST-020` ปิดด้วย (กฎเดิมจาก `GT-101`/`GT-107`)

## จบรอบ
push ครบสองรีโป → เอา draft ออก → แก้หัวข้อ PR → wake-gate commit (`pirate-force-server` เท่านั้น) → ปล่อยให้
workflow merge
