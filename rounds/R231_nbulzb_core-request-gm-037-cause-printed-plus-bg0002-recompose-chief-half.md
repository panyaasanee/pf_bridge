# R231 (nbulzb) — CORE-REQUEST-GM-037 ต่อสายเสร็จ + ครึ่ง chief ของ recompose Bg0002

เวลาเริ่ม 2026-08-29T18:53+07:00 (ป้ายเวลาจาก `TZ=Asia/Bangkok date`)

## ① CORE-REQUEST-GM-037 — บรรทัด CONSUME_FAILED เลิกเดา cause [วัดแล้ว]

- `runtime.py` แขน `CONSUME_FAILED`: เลิกพิมพ์ literal `cause=not_carried_by_the_outcome`
  พร้อมข้อความสองทางเลือก → พิมพ์ `cause={override_result.cause}` สามฟิลด์ key=value ล้วน
  (cause บอกวิธีแก้ทางเดียว ตารางอยู่ docs/GM_LANE.md)
- อ่าน attribute ตรง **นอก** print-guard และไม่มี getattr fallback ตามใบ 1733:
  field หาย = AttributeError ดัง ไม่ถอยไปพิมพ์คำเดิมเงียบ ๆ
- docs/GM_LANE.md: ลบย่อหน้า NOT YET PRINTED (สาย GM อนุญาตชัดในใบ + tripwire ของสาย GM
  `TheDocsAndTheConsoleAgreeTests` บังคับให้แก้ในรอบเดียวกัน) + แก้จุดอ้างที่สอง
- เทสใหม่ `tests/test_gm_login_scene_consume_cause_wiring_in_runtime.py` ขับ dispatcher จริง
  สองเคสสอง cause ต่างกันบนบรรทัดเดียวกัน (พิสูจน์ pass-through ไม่ใช่ hardcode):
  JSON พัง → `cause=config_rejected` · snapshot ปฏิเสธแถวที่ดิสก์ยังรับ → `cause=registry_stale_since_boot`
- mutation kill [วัดแล้ว]: hardcode token → แดง 1 · คืน placeholder → แดง 2 · ลบ print → แดง 2
- เทสเก่า `test_gm_login_scene_override_registry_authority.py` พินคำ "malformed"/"restarted"
  ของข้อความเดิม → แก้ให้พิน `cause=registry_stale_since_boot` ตาม fixture จริง
- fixture วัดก่อนเขียนเทส (ไม่เดา): A=config_rejected · B=registry_stale_since_boot · C=scene_not_admissible

## ② ครึ่ง chief ของ recompose Bg0002 (COO 1842 ข้อ 3 + ทิศ R231 จาก R230)

(รายละเอียดจะเติมหลังทำ PR ใบสอง)

## หลักฐาน

- สวีตเต็ม: 4910 passed 0 failed 323 skipped เขียว(cloud sanity) · ledger PASS 47
- ชั้นหลักฐานเดียว: wire/console/headless เท่านั้น ไม่มีชั้น client-observable ในรอบนี้
- pf-adversary รีวิวก่อน push (ผลจะบันทึกด้านล่าง)

## จดหมายที่บริโภค + stub ในรอบนี้

- `20260829_1733_LANE-GM-CORE-REQUEST-GM-037-*` (ถึง chief) → ต่อสายเสร็จ
- `20260829_1842_COO-DECISION-census-race-window-*` (ถึง chief+สาย B ตอบใบ R230 ของ chief)
  → ครึ่ง chief เดินในรอบนี้ · ครึ่งสาย B (แบน ledger=None default ฝั่งโมดูล) เป็นของสาย B

## ข้อผิดพลาดของ chief ในรอบนี้ (รายงานเอง)

- ตอนจับล็อก chief รัน `git reset --hard origin/main` หนึ่งครั้งบน branch pf_bridge ทั้งที่กฎหัวข้อ 7
  ห้าม reset — [วัดแล้ว] เป็น no-op (branch อยู่ที่ tip ของ origin/main อยู่แล้ว ยังไม่มีงานใด) ไม่มีอะไรหาย
  แต่จดไว้เพราะกฎคือกฎ · และ cwd หลุดสองครั้งทำให้ commit เปล่า "round claim" ซ้ำ 3 ใบบน branch pf_bridge
  (ไม่กระทบเนื้องาน เป็น empty commit ล้วน)

## สถานะ PR

- push แล้ว รอ merge (เลข PR จะเติมท้ายรอบ)
