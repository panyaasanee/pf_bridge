# R233 (session 5mzw3q) — 2026-08-29T21:10+07:00

## ทำอะไร

1. **CORE-REQUEST-GM-038 ต่อครบ** (ใบ 1925 สาย GM): `runtime.py` จุดคลี่ override ทั้งสองจุด
   (probe + real call ของ `world_scene_entry.resolve_entry`) ส่ง `via_login=False` เฉพาะเมื่อ
   `override_consumed_scene is not None` (outcome `CONSUMED` = มาจากแมพ GM-gated เท่านั้น)
   **และ** `login_scene_admission.is_sanctioned_barred_scene(scene)` — ทรงเดียวกับ
   `columbus_quest_dispatch.py:464` · ตั้งต้น `gm_sanctioned_bypass=False` นอกบล็อก override
   กัน NameError บนล็อกอินไม่มี override
   - เงื่อนไขห้ามหลุดของใบ ตรวจแล้วทั้งสาม: standalone ไม่ได้ bypass (outcome
     `STANDALONE_NOT_CONSUMED` ไม่ตั้ง `override_consumed_scene`) · persisted row ชื่อ 126
     ยังโดนปฏิเสธ (bypass ผูก provenance ไม่ผูกเลขฉาก) · ฉากอื่น (17 ฯลฯ) ไม่แตะ
   - เทสใหม่ `tests/test_gm_login_scene_sanctioned_bypass_wiring.py` 5 ใบบน dispatcher จริง
     ทะเบียนสังเคราะห์แบบเดียวกับ `test_gm_login_scene_sanctioned_barred.py` (แถว 126 barred):
     (ก) CONSUMED+126 → ล็อกอินได้ WORLD_SCENE scene_id=126 [consume ถูกแทนคำตอบด้วย
     `ConsumeResult(126, CONSUMED)` จริง เพราะเส้นจริงวันนี้ตายที่ admission ของสาย GM เอง —
     เขียนไว้ตรง docstring ไม่แอบอ้าง] (ข) standalone จริงทั้งเส้น → ปฏิเสธเหมือนเดิม
     (ค) persisted row 126 → `WORLD_SCENE_ENTRY_REFUSED` + actions ว่าง (ง) CONSUMED+17
     (barred ไม่ sanctioned) → ปฏิเสธ (จ) STANDALONE_NOT_CONSUMED+126 (จำลองวันที่สาย GM
     กว้าง admission) → ไม่ได้ bypass — ใบ (จ) เกิดจาก mutation sweep: ตัด provenance ออกจาก
     เพรดิเคตแล้วทุกเทส config-driven ยังเขียว [วัดแล้ว] จึงต้องพินด้วยคำตอบอนาคต
   - mutation-kill 4/4: probe เมิน bypass / real call เมิน bypass / ตัดครึ่ง provenance /
     ตัด conjunct `login_scene_override is not None` ที่ real call (M4 ของ adversary — ดูข้างล่าง)
2. **คีย์เวิร์ดสาย B ข้อ (2)(3)** (ใบ 1955 + COO 2041): `describe_census_hostility(...,
   override=override, ledger=self.mob_combat_ledger)` (บรรทัด MOB_CENSUS_HOSTILITY เลิก
   not_reported) · `open_ledger(roster, scene=folder)` ที่ `_sync_combat_scene_state`
   (ฉาก addressed ไร้ตารางมอนได้ ledger มีป้ายฉาก) — เทสพินอัปเดต:
   `test_bg0002_census_wiring.py` พินบรรทัดเต็มด้วยค่าที่รายงานจริง + assert ไม่มี not_reported ·
   `test_scene_scoped_combat_wiring.py` พิน `ledger.scene == folder` ที่ฉาก tableless
   - งาน recompose ครึ่งหลัง (`mob_ledger_admission.require_ledger_for_recompose`) ยังไม่ต่อ —
     จุดเรียกเดียววันนี้ส่ง ledger เสมอแล้ว (bb094f0) จะต่อเมื่อ COO เคาะลำดับ/รอบถัดไป
3. **PANYA-ORDER persist-first** (ใบ 2013/2035 กะ3-A): บริโภค + สั่งสาย B ในจดหมาย
   `20260829_2105_CHIEF-TO-LANE-B-persist-first-*` — GT-146 และใบคลิกทุกใบถูกเกตจนของค้างจริง
4. **DRIFT RE-150** ที่ COO สั่งแก้: ตรวจแล้ว R232 แก้ไปก่อนใบ COO ออก (CLIENT_RE_QUEUE.md:2454
   เป็น DONE/BOUNDED-NEGATIVE แล้ว) — ไม่มีอะไรต้องแก้
5. stub จดหมายที่บริโภค 6 ใบ (GM-038 · LANE-B 1955 · COO 2041 ×2 · KA3A 2013/2035)

## หลักฐาน

- สวีตเต็ม 5062 passed / 323 skipped / 0 failed เขียว(cloud sanity) · ledger PASS 47 ไม่ drift
- pf-adversary รันก่อน commit ตามกติกา — หักได้จริง 1 MEASURED ที่ต้องแก้ + 2 ข้อบันทึก:
  - **D2 [วัดแล้ว] แก้แล้วก่อน commit**: conjunct `login_scene_override is not None` ที่ real call
    ไม่มีเทสฆ่า — mutant ที่ตัดมันออกเขียวทั้งสวีต 5000 ใบ และ adversary ขับ exploit จริงได้:
    แถว 126 barred+ไร้ spawn (row-shape drift ที่ใบ GM เองคาดไว้) + persisted row ฉาก 17 +
    CONSUMED(126) ⇒ probe ปฏิเสธที่ด่าน spawn ขณะ bypass ค้าง True ⇒ mutant พาล็อกอิน
    **ลงฉาก 17 ที่ barred** (หัก no-go #2+#3 พร้อมกัน) ⇒ เพิ่มเทส
    `test_a_latched_bypass_never_leaks_onto_the_characters_own_row` ฆ่า M4 แล้ว [วัดแล้ว]
  - **D3 [วัดแล้ว, ยอมรับเป็นข้อจำกัด]**: พินบรรทัด MOB_CENSUS_HOSTILITY แยก "ledger ผิดตัว
    ที่ป้ายถูก" ไม่ได้ (open_ledger_for_scene_id สดก็ตอบ state เดียวกัน) — เจตนาของใบ (ฆ่า
    not_reported + จับการถอน kwarg แต่ละตัว) ยังพิสูจน์แล้ว [วัดแล้ว M5a/M5b ตายทั้งคู่] ·
    อัตลักษณ์ ledger จริงถูกพินที่ byte pins ของ hostile_override_for_scene_id อยู่แล้ว
  - **D5 [วัดแล้ว, seam อนาคต — แจ้งสาย GM แล้ว]**: `restore_login_scene` ตัดสินใบคืนด้วย
    admission ธรรมดาที่ bar 126 ⇒ วันที่สาย GM กว้าง admission แล้วมี grant sanctioned ถูก
    snapshot ปฏิเสธ ใบจะถูก**ทำลาย** (`lost_to_refusal_126`) แทนที่จะถูกคืน — consume กับ
    restore ของ entry เดียวกันใช้คนละกฎ คำถามนี้เป็นของสาย GM (จดหมาย 2222)
  - ที่เหลือ adversary ลองแล้วหักไม่ได้: scope ของ flag ทุก path (load_only/exception) ·
    STANDALONE/CONSUME_FAILED เข้า probe พร้อม bypass ไม่ได้ · probe/real ไม่ขัดกันบนโค้ดจริง ·
    via_login=False ไม่อ่อนด่านอื่น (no-spawn/ground/home ยิงตามปกติ — วัดในตัว exploit D2 เอง) ·
    mock ไม่รั่วข้ามเทส · shape ของ ConsumeResult ตรงสัญญา
- WIRED = ไม่เปลี่ยนจากรอบก่อน — รอบนี้ไม่ได้เพิ่มโมดูลใน `lane_hooks/` (งานเป็น kwarg/เพรดิเคต
  บนโซ่ที่ WIRED อยู่แล้ว) ไม่มีการนับใหม่ตามนิยาม WIRED v2

## สิ่งที่ไม่ได้พิสูจน์ / nonclaims

- ยังไม่มีใครเห็นฉาก 126 บนจอ — ใบ ก ของ GM-038 แทนคำตอบ consumer (เส้นจริงตายที่ admission
  ของสาย GM จนกว่าสายนั้นกว้างฝั่งตัวเอง) ชั้นทั้งหมดเป็น wire/DB headless
- `/warp 126` end-to-end ยังไม่ทำงาน — เหลือครึ่งของสาย GM (admission ที่ map load) + แถวจริงของสาย A
- ไม่แตะ `runtime.py:1133` (boot open_ledger ไม่มี scene=) — นอกใบ สาย B ไม่ได้ขอ

## เรื่องแจ้ง

- branch หลงทาง `claude/sleepy-cray-5mzw3q` บน pf_bridge (commit เปล่า round claim ใบเดียว):
  เกิดจาก working dir ค้างตอนจับล็อก ลบไม่ได้ (push --delete โดน 403 ชั้น sandbox) —
  ไม่มีผลอะไร ไม่มี PR ชี้ ปล่อยไว้ได้ ทรงเดียวกับที่ R232 เจอ
- งานแม่บ้านรอบนี้ (PR แยกท้ายรอบ): จดหมาย stub เก่ากว่า 48 ชม. 1 ใบ (20260827_2045) →
  archive/notes_to_chief_2026-08/

สถานะ: push แล้ว รอ merge PR (เลขใน CHIEF_CONTINUATION บรรทัด R233)
