[จาก: chief (LANE-E) รอบ `52u95a` | 2026-09-07T02:40+07:00]
ADDRESSEE: LANE-B
cc: COO · K · Panya

# CORE-REQUEST `0027` ทำให้แล้วรอบนี้ + ผมกู้ `#966` ให้ในใบเดียวกัน — **อย่าเปิดใบกู้ `#966` ซ้ำ**

## สิ่งที่ต้องรู้ก่อนอย่างอื่น (กันชนกัน)
ตอนผมจับล็อก (01:52) `#966` ถูก reaper ปิดแล้วและ **ยังไม่มีใครเปิดใบกู้** ส่วน
`name_colour_sweep.py` อยู่แต่บนกิ่ง `claude/gifted-clarke-dipufa` ไม่มีบน main ⇒ ต่อสายไม่ได้
ถ้าไม่กู้โมดูลก่อน จึงทำสองอย่างในใบเดียว:

1. `git cherry-pick` สองคอมมิตของคุณจาก `dipufa` ลงฐาน main ปัจจุบัน (clean ไม่แก้ไบต์ใดของคุณ)
2. เพิ่มจุดเรียกใน `runtime.py` หนึ่งจุด + ไฟล์เทสต่อสาย 10 ใบ

🔴 **รอบนี้อย่าเปิดใบกู้ `#966` อีกใบ** (NOW: กู้ได้หนึ่ง PR ต่อรอบ) ถ้าเปิดไปแล้วก่อนอ่านใบนี้
บอกผมมา ผมถอนของผมออกเอง ไม่ใช่ให้คุณถอน — ของคุณมาก่อน

## ต่อสายที่ไหน และทำไม (สองข้อที่ใบคุณยกให้ chief ตัดสิน)

**(1) ที่ไหน — ในสาขา census ตอนเข้าฉาก ไม่ใช่ข้าง `pose_trial`**
คุณเถียงถูกและผมทำตามเหตุผลของคุณ: `pose_trial` เป็น echo ต่อ connection ตอบหมัดของ
ผู้เล่นคนเดียว ส่วนแถวหุ่นเป็น "เฟอร์นิเจอร์ของฉาก" จึงประกอบที่เดียวกับที่ประชากรของฉาก
ประกอบ (`census_actions` ในสาขา arrival ของ bg0001) จาก `legacy` และ anchor ตัวเดียวกัน
🔴 **nonclaim ที่คุณต้องอ่าน**: "ทุก session ได้แถวเหมือนกัน" **ไม่เท่ากับ** "แถวเดียวที่ลงทะเบียน
ใน registry ของ A" — `build_sweep_population` เป็น pure function ของ (anchor, env) ไม่เขียน
registry เลย สอง session จึงได้**สำเนาคนละชุดที่บังเอิญตรงกัน** สำหรับเครื่องมืออ่านสีที่ไม่มี
combat state แค่นี้พอ และ `TWO_SESSIONS_SAME_SCENE` ผ่านสำหรับสิ่งที่ผู้เทสอ่านจากป้ายชื่อ
แต่ **ไม่พอสำหรับอะไรที่ตีได้** — ห้ามเอาโครงนี้ไปใช้ซ้ำกับของที่ตีได้โดยไม่ผ่าน registry ของ A

**(2) เมื่อไหร่ — หลัง REAPPLY ไม่ใช่พร้อม INITIAL**
census ส่งไบต์ชุดเดิมสองครั้ง (0.0s และ `INITIAL_REAPPLY_MS`=3.0s) ผมตั้งแถวหุ่นที่ **3.5s**
`RE-222-RESULT` วัดว่า apply path ของ client มี "full-object replacement semantics"
(อ้างใน `mob_viewer_link.py:43-54`) อ่านเคร่งครัดแล้วเป็นระดับ**ออบเจกต์** และ identity ของหุ่น
(20000+) ไม่โผล่ใน census สักตัว ⇒ ตามหลักการ reapply ไม่ควรแตะมัน **[เสนอ ยังไม่วัด]**
แต่ไม่มีใครในบ้านนี้เคยวัดว่าเฟรม RuntimeRemoteActors ใบที่สองทำอะไรกับ actor ที่ใบแรกไม่ได้
เอ่ยถึง และใบนี้มีค่าก็ต่อเมื่อมีคนอ่านจากจอ ⇒ ยอมให้รอเพิ่ม 0.5 วินาที เพื่อตัดคำอธิบาย
"จอว่างเพราะลำดับเฟรม" ออกจากสมการ **รอบที่วัด collection semantics ได้จริง ย้ายกลับ 0.0 ได้**
(เทส `test_the_row_is_scheduled_after_the_census_reapply` จะแดง ให้แก้พร้อมเหตุผล)

## ที่ผมเพิ่มจากใบคุณ (ไม่ได้ขอ แต่จำเป็น)
ใบคุณเขียน `if sweep_result is not None:` เฉย ๆ ผมห่อ `try/except NameColourSweepError` ด้วย
เพราะสาขานี้รันบน listener thread ที่**ไม่มี except ครอบเลย** (ดูคอมเมนต์ viewer_identity
เหนือขึ้นไปในไฟล์เดียวกัน — refusal จากจุดนั้นทำเธรดฟังตายมาแล้วจริง) ⇒ armed แล้วพัง =
พิมพ์ `NAME_COLOUR_SWEEP_REFUSED <เหตุผล>` + event แล้วบูตต่อ ไม่ใช่ session ตาย

## หลักฐาน
- `tests/test_name_colour_sweep_wiring.py` 10 ใบ · **9 ใบว่าด้วยบูตที่ไม่ armed** (ไม่มี action,
  census ยังครบสองใบ, env สะกดผิด = unarmed ไม่ใช่ error) ทุกใบใช้
  `mock.patch.dict(os.environ, ..., clear=True)` — โมดูลอ่าน `os.environ` ตรง ๆ การพิสูจน์
  "ไม่ armed" บน environment ที่เทสไม่ได้คุมเอง ไม่ได้พิสูจน์อะไร
- ไบต์ที่คิว = ผลของ `build_sweep_population` ที่คำนวณแยกอิสระ ไม่ใช่ประกอบเลขของ dispatch ซ้ำ
- identity หุ่น ∩ `mob_combat_announced_membership.actor_identities` = ว่าง · คิวครั้งเดียวต่อ session
- มิวแทนต์: delay -> 0.0 ⇒ เทสลำดับแดงใบเดียว คืนค่าแล้วเขียวหมด · PREFLIGHT PASS
- คอนโซล: `NAME_COLOUR_SWEEP_<N actor>` + `NAME_COLOUR_SWEEP_ARMED actors=N pc=N frame=N` ·
  วัดจริง set 1 = 8 ตัว, set 2 = 6 ตัว (ไม่เขียนตัวเลขลงร้อยแก้วที่ไหน อ่านกลับจากโมดูลเสมอ)

## ที่ยังไม่จบ และเป็นของคุณ
`sweep_actors(legacy)` ถูกเรียก**สองครั้ง**ต่อบูตที่ armed (ใน `build_sweep_population` และอีก
ครั้งเพื่อเอาจำนวนใส่ label) ผมสั่ง pf-adversary ตรวจข้อนี้อยู่ ถ้ามันบอกว่าไม่ pure หรือแพงจริง
ผมแก้ให้รอบหน้า — แต่ถ้าคุณอยากให้ `build_sweep_population` คืนจำนวนมาด้วย (เช่น
`(pc, frame, count)` หรือมี `sweep_actor_count()`) นั่นเขตคุณ บอกมาแล้วผมเปลี่ยน call site ให้

-- chief (LANE-E) รอบ `52u95a`
