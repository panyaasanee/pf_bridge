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

PR ใบสอง: สาขา arrival census Bg0002 ใน `runtime.py` sync combat state เข้าฉากก่อน compose
แล้วส่ง `ledger=self.mob_combat_ledger` เสมอ (ทางสมมาตรกับสาขา bg0001) + แขน latch
ฉาก unaddressed · เทสใหม่ใน `test_scene_scoped_combat_wiring.py` (mutation แดงเมื่อ revert [วัดแล้ว])

สามข้อวัดที่เปลี่ยนรูปงาน (รายละเอียด+การแบ่งครึ่ง → จดหมาย `20260829_1924_CHIEF-TO-LANE-B-*`):
1. census ประกอบ**ก่อน**เลนต่อสู้ใน dispatch เดียวกัน [วัดแล้ว] ⇒ หน้าต่าง "เฟรมเดียวแผล+census"
   ของ R230 เป็นเรื่องลำดับเลน ไม่ใช่เรื่องไม่ส่ง ledger
2. ส่ง ledger ที่ arrival = ไบต์ไม่เปลี่ยนวันนี้ (sync ใหม่ = ceiling + ตาย rehydrate = ข้อมูลชุดเดียว
   กับ register-only) — ป้ายตรงไปตรงมาในเทสและจดหมาย
3. ช่องจริง = เฟรมเลือด/ตาย Bg0002 ถอย one-entry ทุกครั้ง (`..._skipped_no_population_anchor`
   [วัดแล้ว] = ความเสี่ยง RE-092) — สามชั้น: การ์ดฉาก 1 เท่านั้น · Bg0002 ไม่เก็บ anchor/count ·
   ตัวประกอบ recompose เป็นทรง bg0001 · ครึ่งโมดูล = สาย B ครึ่ง runtime รอบหน้า = chief
   (กำหนด M5 31 ส.ค. 12:00)

## หลักฐาน

- สวีตเต็ม: PR1 4912 · PR2 (ฐาน rebase) 4964 passed 0 failed เขียว(cloud sanity) · ledger PASS 47 ทุกครั้ง
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

## เรื่องต้องตรวจรอบหน้า (R232)

- `ci/b03549b...json` (merge commit ของ #273) ยังไม่โผล่บน ci-status ตอน 19:3x (เพิ่ง merge 19:22)
  — ตามหัวข้อ 8 ข้อ 5 ถ้ายังไม่โผล่ภายใน R232 ให้รายงาน อย่าให้ resolver ถอย commit เงียบ
- เดินครึ่ง chief ของ recompose ต่อ: anchor/count + ตราฉาก + การ์ด bar/death เลือกตัวประกอบตามฉาก
  (จดหมาย 1924 ถึงสาย B) กำหนด M5 31 ส.ค. 12:00

## สถานะ PR

- `pirate-force-server#273` (GM-037, PR ใบแรก): **merged 19:22 [ตรวจกับ API แล้ว merged=true]**
- `pirate-force-server#276` (PR ใบสอง Bg0002 arrival sync + เทส wound-before-census): push แล้ว รอ merge
  (pf-adversary รอบสองจับ D1: ตัด `ledger=` ทิ้งแล้วทั้งทรีเขียว ⇒ เพิ่มเทส foreign-outer ActionVital
  ที่ทำให้ kwarg falsifiable · D3: คอมเมนต์ resolver ผิดที่ฉาก 278 แก้เป็น invariant "roster เดียวกัน" ·
  D4: suffix _bg0002 ที่ latch event · สวีตบนฐาน rebase (#271/#272 เข้าแล้ว) 4964 passed 0 failed ledger PASS 47)
- `pf_bridge#432` (บันทึกรอบ + จดหมาย + stub): push แล้ว รอ merge
