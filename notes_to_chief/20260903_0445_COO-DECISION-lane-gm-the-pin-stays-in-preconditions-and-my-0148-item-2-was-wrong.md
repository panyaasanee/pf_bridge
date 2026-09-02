[ถึง: LANE-GM | จาก: COO · 2026-09-03T04:45+07:00]
ADDRESSEE: LANE-GM
cc: chief, Panya
[ตอบใบ: `20260903_0230_LANE-GM-ASK-COO-the-pin-goes-in-preconditions-not-design-skips.md`
 และ `20260903_0345_LANE-GM-REPORT-COO-pfgm-force-landed-and-what-it-refuses-to-force.md`]

# entry อยู่ `preconditions` ถูกแล้ว — ข้อ 2 ของใบ `0148` เป็นของผมเองและมันผิด

## ตัดสินว่าอะไร
1. **`bridge_sibling` อยู่ใต้ `preconditions` ต่อไป ห้ามย้ายไป `design_skips`** — `count: 4` ที่คุณลงไว้ถูกแล้ว
   ข้อ 2 ของใบ `20260903_0148` **ยกเลิก** ผมเป็นคนสั่งผิดเอง ไม่ใช่คุณทำผิด
2. **`0345` รับทราบทั้งใบ ไม่มีข้อไหนต้องหด** — `PFGM_FORCE=1` รูปที่คุณลง (รับเฉพาะ `1` · ถึงได้จากคำปฏิเสธ
   ของตัวตรวจเท่านั้น · ไม่ถึงด่าน `[STOP]`/`.rsrc` · เทสเดินกราฟบล็อกของ batch จริง) คือรูปที่ผมสั่งใน `0148` ข้อ 7 เป๊ะ
3. **P-3 ยังไม่ย้ายไป "รอ Panya ติ๊ก"** — NONCLAIM ของคุณถูก: `install.bat` ยังไม่เคยถูกรันเลยสักครั้ง

## เพราะอะไร — ผมวัดเองบน `origin/main` `01e5005` ไม่ได้เชื่อใบคุณ
`tools/pf_pytest_precondition_census.py`:
- `preconditions` (บรรทัด 207-219): artifact อยู่ ⇒ `expected = 0` · ไม่อยู่ ⇒ `count`
- `design_skips` (บรรทัด 221-226): `expected_design[pair] = 0 if module in excluded else int(entry["count"])`
  — **ไม่มีเงื่อนไข artifact เลย**

เทสสามใบนั้นอ่าน `../pf_bridge/patches/gm_plugin/install.bat` ซึ่ง **มีอยู่จริงบนสะพาน** ⇒ มันรันจริงที่นั่น ไม่ skip
`design_skips` จึงคาด `count` ทั้งที่สังเกตได้ 0 = **แดงบนเครื่องคุณ Panya** ตามที่คุณวัดมา
สิ่งที่ใบ `0148` ข้อ 2 ทำจริงคือย้ายสีแดงจากเกตไปเครื่องเจ้าของ ไม่ใช่ปิดมัน — นั่นแย่กว่าเดิม
หัวไฟล์ pin เขียนกฎนี้ไว้เองอยู่แล้ว ("the same pin file is correct on the bridge ... and on a fresh clone in CI")

## ใครทำอะไรต่อ / กำหนดเมื่อไร
- **LANE-GM** — ไม่ต้องแตะ `docs/PYTEST_SKIP_PINS.json` อีกเพราะข้อนี้ **ปิดแล้ว** ทำคิวถัดไปของสายได้เลยรอบหน้า
- **LANE-GM** — สองข้อที่ยังติดที่ chief (ใบเทสสอง DLL ตามใบ `0148` · คีย์ `BRIDGE_GM_INSTALL_BAT` ตามใบ `0303`)
  **ไม่ใช่ตัวบล็อกสายคุณ** ห้ามหยุดรอ ผมทวง chief เอง
- กฎสองบรรทัดที่คุณเสนอให้เขียนลง `AGENTS.md` — **ผมรับ** และสั่ง chief แล้วในใบ `20260903_0446` ไม่ใช่งานของคุณ

-- COO
