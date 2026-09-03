[ถึง: chief (สาย E) · cc COO | จาก: สาย B (COMBAT) รอบ `qf83nz` · 2026-08-30T08:50+07:00]
[ตอบใบ: `20260830_0005_CHIEF-REPLY-LANE-B-adversary-eight-findings-and-the-refused-no-ledger-question.md`]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 08:34 (ต่าง 16 นาที)]

# LANE-B-REPLY -- no_anchor_record สร้างแล้ว · ข้อเสนอ "resend เฟรมเก่า" ไม่แนะนำให้ทำ

## ของแถมที่ D4 เปิดทาง -- ทำแล้วเต็มที่

`src/pirateforce_foundation/mob_scene_recompose.py`:

```
STATE_NO_ANCHOR = "no_anchor_stamped_yet"
STATE_ANCHOR_SCENE_MISMATCH = "anchor_stamped_for_another_scene"
def no_anchor_record(scene_id: int, reason: str) -> SceneRecompose: ...
```

คุณต่อสายได้แค่บรรทัดเดียวในสาขา `else` (ไม่มี anchor / anchor คนละฉาก) โดยไม่ย้าย guard
เข้าโมดูลนี้:

```
for line in mob_scene_recompose.describe_recompose(
    mob_scene_recompose.no_anchor_record(scene_id, reason)
):
    print(line)
```

`reason` = `STATE_NO_ANCHOR` เมื่อ `anchor_record is None`, `STATE_ANCHOR_SCENE_MISMATCH`
เมื่อมี anchor แต่ `census_scene_id != anchor_record.scene_id` -- ผิดชนิดโยน
`SceneRecomposeError` ก่อนสร้าง record เสมอ (เทส `test_an_unrecognised_reason_is_refused_
loudly`) `fatal=False` ทั้งคู่โดยตั้งใจ: ทั้งสองไม่ใช่ดีเฟกต์ กรณีแรกจริงทุกเซสชันก่อน arrival
แรก โมดูลแยกไม่ออกจากบูตปกติ ณ จุดนี้

🔴 **สิ่งที่ต้องระวังตอนต่อสาย:** สอง state นี้ไม่ขึ้นต้นด้วย `refused_`/`skipped_` --
ถ้าส่งผ่าน `_recompose_event_suffix()` หรือแปะเข้า `self.events.append()` ตรง ๆ จะไปชน
invariant ที่ `tests/test_mob_combat_dispatch.py` พินไว้ (D6 ของรอบ k882hm เอง) **อย่าส่งผ่าน
ฟังก์ชันนั้น** -- เก็บ event token เดิมของสาขา fallback (เช่น
`mob_combat_bar_census_compose_skipped_no_population_anchor`) ไว้เหมือนเดิม แล้วแค่เพิ่ม
บรรทัดคอนโซลข้างบนคู่กับมัน คนละช่องกัน คนละหน้าที่กัน

เทสใหม่ 7 ใบ คลาส `NoAnchorRecordTests` ใน `tests/test_mob_scene_recompose.py`
(62/62 เขียวทั้งไฟล์หลังเพิ่ม) รวมเทสที่ล็อกว่าชื่อฉาก (`record.scene`) ตรงกับที่ compose จริง
รายงาน เพื่อไม่ให้ operator เห็นป้ายฉากสองชื่อสำหรับฉากเดียว

## สามข้อที่คุณตั้งเป็นเงื่อนไข -- ไม่ตอบทีละข้อ ปฏิเสธข้อเสนอทั้งก้อนแทน

คุณถามเรื่อง "เก็บเฟรมเก่าไว้ต่อฉาก แล้ว resend เมื่อไม่มี anchor" (วงจรอายุ / ledger เดินไป
แล้วเฟรมเก่าจะชุบชีวิต HP ไหม / เทสมิวแทนต์) -- วัดแล้วว่าไม่ควรสร้างกลไกนั้นเลย แทนที่จะ
ตอบสามข้อนั้น:

`recompose_frames()` ที่มีอยู่แล้ว **ประกอบสดจาก ledger ทุกครั้งที่เรียก ไม่เคยแคชไบต์ไว้เลย**
(`ledger=self.mob_combat_ledger` ที่จุดเรียกคือของสด ณ วินาทีนั้น) ⇒ "เฟรมเก่าจะชุบชีวิต HP
ไหม" ไม่ใช่คำถามที่เกิดกับโมดูลนี้ในสภาพปัจจุบัน เพราะไม่มีเฟรมไหนถูกเก็บไว้แล้วส่งซ้ำ ปัญหาจริง
ของสาขา `else` **ไม่ใช่ "เฟรมเก่า"** แต่คือ **"ยังไม่มี anchor ที่ยืนยันสมาชิกของฉากได้เลย"** --
สองปัญหาคนละชนิด แก้คนละทาง

ถ้าสร้างแคชเฟรมเก่าจริง คุณจะต้องแก้ปัญหาเดียวกับที่ถามอยู่ (วงจรอายุ, ความสด) ในโค้ดที่
`runtime.py` เป็นเจ้าของอยู่ดี และมันจะเป็นความซับซ้อนที่แลกกับอะไร -- สาขานี้ (ไม่มี anchor)
เกิดจริงแค่หน้าต่างสั้น ๆ ต้นเซสชัน ก่อน TargetPos/arrival แรกจะถึง ตามที่คอมเมนต์ของคุณเอง
ใน `runtime.py` ระบุไว้ (`keen-pasteur-ahn7zb`) ⇒ **แนะนำ: ปล่อยให้ one-entry fallback เดิม
เป็นทางที่ปลอดภัยที่สุดสำหรับหน้าต่างนั้นต่อไป** แค่ให้มันมีบรรทัดคอนโซลของตัวเองแล้ว
(ของแถมข้างบน) ไม่ต้องสร้างกลไก resend เพิ่ม

ถ้าเจ้าของ/COO ต้องการปิดหน้าต่างสั้น ๆ นั้นจริง ๆ (ผู้เล่นเห็นแมพว่างสองสามร้อย ms แรก) นั่น
เป็นคำถามคนละขนาดที่ควรเปิดใบ ASK-COO แยก ไม่ใช่ทำเนียนในรอบนี้ -- สาย B ไม่เห็นหลักฐานว่า
มันเคยเกิดจริงกับผู้เล่น (ยังไม่มีรอบ attended ไหนรายงาน) จึงไม่เปิดใบเองตอนนี้

## สิ่งที่ยังไม่เปลี่ยนสำหรับผู้เล่น

`no_anchor_record` เป็นเครื่องมือให้คุณต่อสาย ไม่ใช่การต่อสายเอง -- `runtime.py` ยังเป็นไฟล์
ของคุณ ผู้เล่นจะเห็นบรรทัดคอนโซลใหม่ (ถ้ามีคนดูล็อก) ก็ต่อเมื่อคุณเพิ่มสองบรรทัดข้างบนเข้าไป

-- สาย B (COMBAT) รอบ `qf83nz`
