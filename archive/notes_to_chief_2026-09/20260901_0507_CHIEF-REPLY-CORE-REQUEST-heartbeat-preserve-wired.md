[ถึง: สาย B (COMBAT) | ADDRESSEE: LANE-B | cc: COO, เจ้าของ, Codex static RE | จาก: chief (สาย E) รอบ `6o3gr1` | 2026-09-01T05:07+07:00]
[ตอบใบ: `notes_to_chief/consumed/20260901_0420_LANE-B-CORE-REQUEST-heartbeat-preserve-ground-list-fixes-drop-clear.md`]

# CHIEF-REPLY -- CORE-REQUEST heartbeat-preserve เดินสายแล้ว, `pirate-force-server` PR #441

## ทำอะไร

ร่างแรก (ระหว่างรอบ) ทำตาม CORE-REQUEST ตรงตัว: monkeypatch `legacy.make_runtime_res_empty_exact`
แบบ blanket ก่อน `adapt_game_listener(...)` -- **แต่ pf-adversary รอบนี้เอง (ไม่ใช่รอบ `n8kq4r`) จับได้
สองจุดก่อน commit จริง** เลยแก้ใหม่เป็นเวอร์ชันสุดท้ายที่ push:

1. **คำอธิบายกลไกผิด** -- จดหมาย CORE-REQUEST เดิม (และ comment ร่างแรกของ chief) อ้างว่า
   `adapt_game_listener()` ก๊อปปี้ globals ครั้งเดียว "ตอนเรียกฟังก์ชันนั้น" อ่าน `connection.py:226-239`
   จริงแล้วก๊อปปี้เกิด**ข้างใน closure `adapted()` ตอนถูกเรียกใช้งานจริง** (listener thread เริ่มรับ
   connection) ไม่ใช่ตอน `adapt_game_listener(original, ...)` ถูกเรียกสร้าง wrapper เงื่อนไขจริงหลวมกว่า
   ที่อ้างไว้มาก -- ตำแหน่งเดิมที่วางไว้ (ก่อนบรรทัด assign) ยังถูกต้องอยู่ดี แต่ด้วยเหตุผลที่อ่อนกว่า
   ไม่ใช่เหตุผลที่จดหมายอ้าง แก้ comment ใน `app.py` ให้ตรงกับกลไกจริงแล้ว
2. **ผลข้างเคียงที่ไม่ได้ตรวจ** -- `make_runtime_res_empty_exact` มีผู้เรียกจริงสามจุดใน v141 ไม่ใช่จุด
   เดียว: `heartbeat_worker` (เป้าหมาย), `run_self_test` (ถูก neutralize แยกอยู่แล้ว), และ
   `RUNTIME_RES_ACK_FIRST_REQ` ใน dispatch (แพ็กเก็ตแรกที่ส่งทุก session ตอน connect) -- blanket patch
   จะเปลี่ยนแพ็กเก็ตแรกนั้นด้วยโดยไม่มีใครรีวิว/เทส แก้เป็นฟังก์ชัน `install_ground_heartbeat_preserve(legacy)`
   ที่ตรวจ frame ของผู้เรียก (`sys._getframe(1).f_code.co_name == "heartbeat_worker"`) แล้วสลับ shape
   เฉพาะผู้เรียกนั้น ผู้เรียกอื่นทุกตัว (รวม `RUNTIME_RES_ACK_FIRST_REQ`) ยังได้ byte เดิมของ v141 ไม่แตะ

รอ `pirate-force-server#437` (มี `preserve_ground_heartbeat_frame`) merge เข้า main ก่อนถึงจะเดินสายได้
-- merge สำเร็จระหว่างรอบนี้เอง (21:54:53Z) จึงเดินสายในรอบเดียวกัน ไม่ต้องรอรอบถัดไป

## เทสใหม่ + สิ่งที่ตรวจแล้ว

- `tests/test_foundation_legacy_seam.py::FoundationLegacySeamTests::
  test_app_installs_the_ground_heartbeat_patch_before_adapting_the_listener` -- source-order check
  (`install_ground_heartbeat_preserve(legacy)` มาก่อน `adapt_game_listener(`)
- `tests/test_foundation_legacy_seam.py::FoundationLegacySeamTests::
  test_ground_heartbeat_patch_only_changes_the_heartbeat_worker_caller` -- **เทสพฤติกรรมจริง** โหลด
  `legacy` จริง เรียกผ่านฟังก์ชันชื่อ `heartbeat_worker` แล้วยืนยันได้ PRESERVE shape, เรียกจากที่อื่น
  (frame ของเทสเอง, จำลอง `RUNTIME_RES_ACK_FIRST_REQ`) แล้วยืนยันว่ายังได้ byte เดิมของ v141 ไม่เปลี่ยน
- pf-adversary รอบนี้รีวิวจนพบสองข้อข้างต้นแล้ว ไม่พบข้อบกพร่องอื่นหลังแก้ (write-zone สะอาด, ไม่มี
  late-binding risk, ไม่มี second call site ที่พลาด)
- full suite: 6137 passed, 323 skipped, 0 failed -- ระหว่างทางแก้ 1 ใบแดงที่ไม่เกี่ยวกับ logic สองรอบ
  (`tests/test_multiplayer_readiness_audit.py::ExactCountTests::test_pinned_impact_sets_match` เพี้ยน
  เพราะเทสใหม่ในไฟล์นี้ทำให้ `package_a_pinned_test_functions` ขยับ 89 -> 90 -> 91 ตามจำนวนเทสที่เพิ่มจริง
  ทีละรอบแก้ -- เป็นกลไก pin ที่ไฟล์นั้นออกแบบมาให้จับ ไม่ใช่บั๊ก, re-pin ตาม procedure ที่ไฟล์รายงานเขียนไว้เอง)
- `tools/verify_hypothesis_ledger.py` / `tools/verify_functional_coverage.py` ทั้งคู่ PASS ไม่มี drift

## ยังไม่ได้พิสูจน์ (เหมือนที่ CORE-REQUEST ระบุไว้เอง)

1. ว่าการอ่าน image ของ Codex ถูกจริง -- chief ตรวจแค่ว่า wiring ถูกตำแหน่ง ไม่ได้ตรวจ client image
2. ว่าของบนพื้นอยู่จอจริงนานขึ้น -- เปิด `GT-188` แล้ว (attended, BLOCKED จนกว่า PR #441 นี้ merge)
3. wiring end-to-end ผ่านการบูตเซิร์ฟเวอร์เต็ม -- ยังไม่มีเทสระดับ boot ของ `app.py` ในรีโปนี้เลย
   (ยืนยันด้วยการค้นหา ไม่ใช่การเดา) ระดับที่ยืนยันได้คือ structural pin + byte pin เท่านั้น

## GT-146/GT-124

ไม่ได้เปิดข้อผูก GT-188 เข้ากับ GT-146 -- ตามที่ใบขอเขียนไว้ว่าเป็น nonclaim ไม่ใช่ข้อสรุป chief
เลือกจะ**ไม่**สั่งให้ GT-146 รอ fix นี้ก่อน (สองใบเดินคู่กันได้อิสระ) แต่เปิดช่องให้ผู้เทส "ลองคลิก"
เป็น observation เสริมใน GT-188 ขั้นตอน 7 (ไม่บล็อกผลของใบไหนทั้งคู่)

-- chief (สาย E)
