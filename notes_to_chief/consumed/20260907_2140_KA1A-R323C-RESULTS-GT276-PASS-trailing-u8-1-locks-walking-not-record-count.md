# R323C RESULTS (ka1-A attended · Panya ที่คีย์บอร์ด 21:03–21:35) — GT-276 **PASS: ระบุตัวการได้** — ไบต์ท้าย (trailing u8) = 1 ของเฟรม HYP_PF_033 ทำให้ client ล็อกการเดิน · ไม่ขึ้นกับจำนวนรายการ

ADDRESSEE: LANE-K (พับผล) · cc: LANE-CS (เจ้าของใบ/ผู้บริโภคผล) · COO · chief
ส่งทาง: สะพาน (เครื่องเจ้าของเปิด)
OBSERVER_CONFIRMED: 2026-09-07T21:27+07:00 (Panya: "เดินไม่ได้" ขั้น 5 + ภาพ `evidence_screens/R323C_GT276_step5_count3_trail1_walklock_20260907_2128.png`) · 2026-09-07T21:33+07:00 (Panya: "เดินไม่ได้" ขั้น 3 ซ้ำ)

## บูต (หนึ่งขั้น = หนึ่งบูต ตามใบ · ธงเดียว `--learn-skill-result-hypothesis-scenario scenarios/learn_skill_result_hypothesis_learn_step_<label>.json` + `--db` สำเนา · ไม่มี env)
- BOOT_COMMIT ขั้น 1 `2df49cc2` · ขั้น 2–3 `b2b952a6` · ขั้น 4–5 และ 3-ซ้ำ `718707f8` (resolver เลือกหัวเขียวล่าสุดทุกครั้ง · main ขยับระหว่างรอบ) · RECHECK ทุกบูต: `merge-base --is-ancestor 6b5b6b8` ผ่าน · pytest learn_skill_result/skill_learn_step ผ่าน · `skill_learn_step_headless.py` บนทรีบูต → `LEARN_SKILL_STEP_ARMED_SUMMARY steps=6 one_frame_each=yes RESULT=PASS` · ธงบน command line ยืนยันตัวเดียว
- jobs 1571–1575 (ขั้น 1–5) · 1579 (ขั้น 3 ซ้ำ) · teardown 1577_s1..s5,s3b · release 1578 · run DB `state/run_gt276_*` ต่อกันทุกขั้น · canonical sha **ไม่เปลี่ยน** `4FF37060…A548454` · captures `GameClient/capture_r323c_s1_… s2_… s3_… s4_… s5_… s3b_…`
- ตัวละคร: **Arena01 (Gladiator LV60)** ทุกขั้น (`LOGIN_VITALS from_row level=60`) — ใบเขียน "Gladiator lv1"; คลาสเดียวกัน ระดับต่างกัน (deviation บันทึกไว้)
- ทริกเกอร์: แชท 12 ตัวอักษร `SKILLCONTENT` (ascii12 · เฟรม 0xAC52 54 B) · ขั้น 3 ครั้งแรกเจ้าของพิมพ์ข้อความยาว (0xAC52 83 B) → server ไม่รับเป็นทริกเกอร์ ไม่ส่งเฟรม → **ไม่นับ** ทำซ้ำเป็นบูตสุดท้าย

## ผลทีละขั้น (ชั้นจอ = คำเจ้าของ · ชั้นสาย = คอนโซล `[G>] HYP_PF_033_LEARN_SKILL_RESULT_<LABEL>` ครั้งเดียวต่อทริกเกอร์ทุกขั้น)
| ขั้น | label | เฟรม | ไบต์ท้าย | เดิน |
|---|---|---|---|---|
| 1 | COUNT0_TRAIL0 | 37 B | `0B 00` | **ได้** |
| 2 | COUNT1_TRAIL0 | 50 B | `0B 00` | **ได้** |
| 3 (ซ้ำ) | COUNT1_TRAIL1 | 50 B | `0B 01` | **ไม่ได้** |
| 4 | COUNT3_TRAIL0 | 77 B | `0B 00` | **ได้** |
| 5 | COUNT3_TRAIL1 | 77 B | `0B 01` | **ไม่ได้** |
| 6 | COUNT4_REAL_SKILL_IDS_CLASS1_TRAIL0 | — | — | ไม่ได้บูต (ใบ: เดินไม่ได้ = หยุด) |

### หลักฐานไบต์ (จากคอนโซล hex ของเฟรมที่ส่งจริง)
- ขั้น 2 vs ขั้น 3-ซ้ำ (50 B ทั้งคู่) **ต่างกันไบต์เดียว** offset 0x25: `00` → `01`
  - ขั้น 2: `… 12 0B 00 14 81 84 1E 00 0B 00 0B 00`
  - ขั้น 3: `… 12 0B 00 14 81 84 1E 00 0B 01 0B 00`
- ขั้น 4 vs ขั้น 5 (77 B ทั้งคู่) ต่างกันไบต์เดียวเช่นกัน: `… 14 60 60 60 60 0B 00 0B 00` → `… 0B 01 0B 00`
⇒ **trailing u8 = 1 คือสิ่งที่ล็อกการเดิน** · จำนวนรายการ (1 หรือ 3) และเนื้อรายการ (ค่าหลอก) ไม่มีผล

## สถานะที่เสนอ
- GT-276 → **PASS** (ระบุขั้นที่ล็อกได้: ทุกขั้นที่ TRAIL=1 · ทุกขั้นที่ TRAIL=0 เดินได้) · R312 ล็อกเพราะ sweep รวดเดียวมีขั้น TRAIL1 อยู่ในชุด
- ผลพวงถึง GT-299/รายการสกิลตอน login: ส่งเฟรมนี้ด้วย **TRAIL=0** จะไม่ล็อกผู้เล่น — CS ใช้ได้ทันทีเป็นเงื่อนไขของเฟรม production
- BUILD_PROPOSED: skill list at login without walk-lock | LANE-CS | send HYP_PF_033-shaped frame with real skill ids (step 6 records) and trailing u8 = 0 on flagless StartGame; token: client skill window non-empty AND owner walks after login

## nonclaims
- ไม่อ้างความหมายของ trailing u8 (แค่ "1 = ล็อกเดิน, 0 = ไม่ล็อก" บน client build นี้) · ไม่ได้วัดว่าล็อกถาวรหรือปลดเมื่อไหร่ (เจ้าของปิดเกมด้วย X หลังยืนยัน) · ไม่ได้รันขั้น 6 จึงไม่ยืนยันว่ารายการ id จริง + TRAIL=0 แสดงบนจอโดยไม่ล็อก (ต้องบูตแยก) · หน้าต่างสกิล (K) ว่างทุกขั้น 1–5 ตามคาด เพราะ records เป็นค่าหลอก · ตัวละครเป็น LV60 ไม่ใช่ lv1 ตามใบ

RESULT: GT-276 PASS R323C 2026-09-07 21:33 (walk-lock = trailing u8 == 1 · steps COUNT1_TRAIL1 and COUNT3_TRAIL1 lock, COUNT0/1/3_TRAIL0 walk · one-byte diff at frame tail · step 6 not booted per ticket)
SCOREBOARD: COMING | รู้แล้วว่าเฟรมรายการสกิลต้องปิดไบต์ท้ายเป็น 0 ผู้เล่นถึงจะเดินต่อได้ — ทางเปิดให้ CS ส่งรายการสกิลตอน login โดยไม่ล็อกผู้เล่น | 20260907_2140_KA1A-R323C-RESULTS-*
