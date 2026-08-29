[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session ยึดล็อกรอบนี้) · 2026-08-27T04:38+07:00]

# LANE-GM STATUS — พับผล RE-089/090/091 เข้าโค้ด/เอกสาร + wire codec ใหม่สำหรับ GM-003 warp

## สรุปหนึ่งบรรทัด

`RE-090` (TeleportVital/ForcePos/CWarpResult field layout, PASS/DONE) ยังไม่เคยถูกพับเข้าโค้ดของสายนี้แม้ chief จะปิดหัวใบใน `CLIENT_RE_QUEUE.md` ไปแล้วตั้งแต่รอบ `kdx85r` — รอบนี้สร้าง `gm/teleport_wire.py` ที่ implement layout นั้นจริง พร้อมแก้ `gm/state_wire.py`/`docs/GM_LANE.md` ให้ตรงกับผล `RE-089` (หักล้าง `bm_gm.tga`) และ `RE-091` (chat trigger เป็น dedicated GM UI ไม่ใช่ prefix)

## ค้นแล้ว

**ค้นใน `notes_to_chief/` แล้ว: เจอ** — อ่านทั้งสามใบ `RE-089`/`RE-090`/`RE-091` เต็มฉบับ (ไม่ได้พึ่งแค่บรรทัดสรุปใน `CLIENT_RE_QUEUE.md`) · **ค้น `external/PF_FIELD_VALIDATION.tsv` แล้ว: เจอ** ตรวจตัวเลข frame count ของทั้งสี่ข้อความเองก่อนอ้างในโค้ด (ForcePos/CWarpResult = 0 จริง, TeleportVital = 132 candidate frame ต่อทิศ `A2_STATIC_OPEN`) — พบว่า docstring ร่างแรกของตัวเองเขียนผิด (อ้างว่าศูนย์ทั้งสาม) แก้ก่อนส่งใบนี้

## สิ่งที่สร้าง (`pirate-force-server`, เขตเขียนของสายนี้)

- `gm/teleport_wire.py` (ใหม่) — encode/decode `ForcePos`/`CWarpResult`/`TeleportVital` ตาม RE-090
- `gm/state_wire.py` docstring แก้ตาม RE-089 (ไม่แก้พฤติกรรม)
- `docs/GM_LANE.md` แก้ครบ (wire-facts table, ปิดหัวข้อ RE-open เป็น RE-closed, เพิ่มหัวข้อ modules delivered รอบนี้)
- `tests/test_gm_teleport_wire.py` (29 เทส)

`test_gm_*.py` ทั้งชุด: 129 เทสผ่านหมด รายละเอียดเต็มอยู่ที่ `rounds/GM_20260827_0438_teleport-wire-codec-re090-fold-in-plus-re089-docstring-fix.md`

## `pf-adversary`

สองรอบ (สร้าง → พบ 7 ข้อจริง [1 HIGH, 1 MEDIUM-HIGH, 2 MEDIUM, 2 LOW-MEDIUM, 2 LOW] → แก้ครบ → ยืนยันซ้ำ → พบเศษตกค้าง 1 จุด [เอกสารขัดแย้งกันเองสองที่เรื่องจำนวนเฟรมของ `TeleportVital`] → แก้แล้ว) รายละเอียดทุกข้ออยู่ใน rounds file

## 🔴 ข้อสังเกตสำคัญที่สุดของรอบนี้ (ไม่ใช่บั๊ก แต่เป็นความเสี่ยงที่ยังไม่ปิด)

ลำดับฟิลด์ของ `TeleportTarget` (object ย่อยของ `TeleportVital`) implement ตามลำดับที่ RE-090 **เขียนไว้ในข้อความ** (`scene_id, scene_seq, field_0x10, field_0x11, vec3`) ไม่ใช่ ascending object-offset — เหตุผลคือ RE-090 เองพิสูจน์ไว้แล้วว่าลำดับสตรีมจริงไม่ใช่ ascending offset เสมอ (ตัวอย่างสองจุดในใบเดียวกัน) จึงเชื่อถือลำดับที่เขียนไว้มากกว่าลำดับ offset แต่ **ยังไม่เคยตรวจกับเฟรมจริง** — `PF_FIELD_VALIDATION.tsv` มี 132 candidate frame ของ `TeleportVital` ที่ `A2_STATIC_OPEN` (candidate-matched ยังไม่ parse-confirmed) รอบ RE ถัดไปน่าจะรัน codec นี้กับ 132 เฟรมนั้นเพื่อปิดคำถามนี้ให้เด็ดขาดก่อนเอาไปใช้กับ client จริง — ไม่ใช่ RE-request ใหม่ (ไม่มีอะไรให้ถอดเพิ่ม แค่ต้อง cross-check ของที่มีอยู่แล้ว) เขียนไว้ตรงนี้เผื่อรอบ RE ถัดไปเห็นแล้วหยิบทำได้เลย

## ยังไม่ทำ (ตั้งใจ)

`warp` ยังไม่ execute — ต้องมี inbound dispatch ของ `0x51E9` ใน `runtime.py` ที่ไม่เคยมีมาก่อนเลย บวกจุดตัดสินใจเรื่อง authorization gate ก่อน execute ที่ใหญ่กว่าจดหมาย `CORE-REQUEST` บรรทัดเดียว เสนอเป็นรอบถัดไปที่ตั้งใจทำเฉพาะเรื่องนี้ ไม่รีบยื่นจดหมายที่ยังไม่คิดจุด wiring ให้ชัดพอ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ยังไม่มี — รอบนี้เป็นโค้ด/เอกสารฝั่งเซิร์ฟเวอร์ล้วน ไม่มี wiring เข้า runtime

## nonclaim

ไม่มีการอ้างว่าไบต์ที่ `gm/teleport_wire.py` สร้างได้จะถูก client จริงยอมรับ — field ส่วนใหญ่ยัง NOT proven semantics และลำดับฟิลด์ `TeleportTarget` ยังไม่ยืนยันกับเฟรมจริงตามที่เขียนไว้ข้างบน ไม่มีการ execute หรือส่ง frame ใด ๆ จริงในรอบนี้
