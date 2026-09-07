# R323 RESULTS (ka1-A attended · Panya ที่คีย์บอร์ด 19:37–20:20) — GT-288 ชุด 2 MEASURED ทั้งสองชั้น (สีชื่อไม่ขึ้นกับ actor_type/สกิน) · GT-299 BLOCKED-ON-PRECONDITION (รายการสกิลว่าง)

ADDRESSEE: LANE-K (พับผล) · cc: COO · LANE-B (เจ้าของ GT-288) · LANE-CS (เจ้าของ GT-299) · chief
ส่งทาง: สะพาน (เครื่องเจ้าของเปิด)
OBSERVER_CONFIRMED: 2026-09-07T19:46+07:00 (Panya: ภาพหน้าจอแถวหุ่น 6 ตัว + คำบรรยายทีละตัว) · 2026-09-07T20:15+07:00 (Panya: ภาพหน้าต่างสกิลว่างทั้งสองแท็บ)

## บูต
- **R323A (GT-288)** BOOT_COMMIT `57f1efac` (main ณ ตอนบูต `e08a9a65` · code_delta 7 · resolver เลือกหัวเขียวล่าสุด) · ทรีไร้ธง + env `PF_NAME_COLOUR_SWEEP=2` (ใบต้องการ) · RECHECK ก่อนบูตบนทรีบูต: `merge-base --is-ancestor 9d2d1c04` ผ่าน · pytest `test_name_colour_sweep*.py` 30 passed 16 skipped · `sweep_enabled(env=2)=True` · `ACTOR_TYPE_CANDIDATE=5` · `_row_xyz` ordinal 0 = −150 บน X · jobs 1560→(ยกเลิก)→1564/1565/1566 · run DB `state/run_gt288_20260907_193650.sqlite3` (ตัดจาก canonical) · capture `GameClient/capture_r323a_20260907_193650/`
- **R323B (GT-299)** BOOT_COMMIT `f8352ea3` (main `2df49cc2` · code_delta 3) · ธงเดียว `--learn-skill-request-hypothesis-scenario scenarios/learn_skill_request_hypothesis_decode_probe.json` + `--db` สำเนา · ไม่มี env · RECHECK: `merge-base --is-ancestor 11f937a3` ผ่าน · pytest learn_skill/skill_learn 184 passed · รัน `skill_learn_request_headless.py` บนทรีบูต → `LEARN_SKILL_REQUEST_ARMED_SUMMARY probes=3 decoded_no_reply=yes real_frame=refused no_db_write=yes RESULT=PASS` · jobs 1567(abort ก่อนบูต: needle ผิด)→1570/1568/1569 · run DB `run_gt299_20260907_195440` (ต่อจาก run_gt288) · capture `capture_r323b_20260907_195440/`
- canonical sha **ไม่เปลี่ยน** `4FF37060…A548454` ทั้งสองบูต · ปิดสะอาด listeners 0 · ตัวละครใหม่ (test · Gladiator LV1) อยู่เฉพาะใน run DB
- **เหตุการณ์ 19:31–19:33 (ความผิด ka1-A)**: บูตแรก 1560 ขึ้นปกติ แต่ ka1-A ต่อคิว teardown 1562 ไว้ใน inbox ขณะ client ยังเปิด → job บูตจบทันทีหลังเปิดเกม → bridge รัน teardown ต่อ → บรรทัดแรกของ teardown ฆ่า GameClient → เกมดับที่หน้าเลือกตัวละคร ไม่ได้วัดอะไร · ปล่อยล็อกแล้วบูตใหม่ 1564 · กติกา ka1-A: ห้ามวาง teardown ก่อนเจ้าของบอกว่าปิดเกมแล้ว

## GT-288 NAME-COLOUR-SWEEP-DUMMY-ROW-001 ชุด 2 — **MEASURED ทั้งสองชั้น**
### ชั้น wire (คอนโซล + game log)
- `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` (login บนบก) · `NAME_COLOUR_SWEEP_STANDING_REFUSAL allowed=False blockers=3` (ตามคาด ไม่ใช้ตัดสิน) · **`NAME_COLOUR_SWEEP_ARMED actors=6 census_actors=108 wire=114 pc=21502 frame=21516`** · `[G>] WORLD_CENSUS_INITIAL_108_SWEEP_6 (21516 bytes)` ×1 · `[G>] WORLD_CENSUS_REAPPLY_108_SWEEP_6` ×1 · ไม่มี collection ใบที่สอง (ตรง HEADLESS_PROOF ของ B ทุกตัวเลข)
### ชั้นจอ (Panya · หุ่นเรียง −X จากจุดเกิด ห่าง 150 · เธอไม่คลิก/ไม่ตี ตามใบ)
| # | ป้าย | เห็นตัว | ป้ายชื่อ | สี | ร่างกาย |
|---|---|---|---|---|---|
| 1 | N-BASE | ใช่ | ใช่ | **เขียว** | ปกติ (ทหารเรือ) |
| 2 | N-AT5 | ใช่ | ใช่ | **เขียว** | **ตัวเปลือย** (ชุดไม่ถูกใส่) |
| 3 | N-SKIN | ใช่ | ใช่ | **เขียว** | **โมเดลโหลดไม่ครบ ยืนเอียง ตัวขาด** |
| 4 | M-BASE | ใช่ | ใช่ | **ชมพู** | ปกติ (หุ่นซ้อม 916) |
| 5 | M-AT5 | ใช่ | ใช่ | **ชมพู** | **T-pose** (แอนิเมชันไม่ผูก) |
| 6 | M-SKIN | ใช่ | **ไม่มีป้าย** | — | ปกติ (โมเดล M010) |
### สิ่งที่ตารางบอก (ka1-A อ่าน · B ตีความต่อ)
- **หุ่นทั้ง 6 วาดขึ้นจอ** — client รับ `actor_type 5` และรับ recompose แบบเฟรมเดียวได้ (ตอบ nonclaim ของ B และคำถามใบ chief 0341)
- **สีชื่อไม่ขยับตาม actor_type (4→5) และไม่ขยับตามสกิน**: ต้นแบบ NPC เขียวทั้ง 3 · ต้นแบบมอน ชมพูทั้ง 2 ที่มีป้าย ⇒ ตัวตัดสินสีอยู่ใน**ฟิลด์ body ที่ต่างกันระหว่างต้นแบบ NPC (n_ID 1) กับต้นแบบมอน (916)** ไม่ใช่ actor_type/visual preset · ผู้สมัครที่เหลือ = ชุด 1 (faction 7/12/999) หรือฟิลด์อื่นใน NPCAttr ที่สองต้นแบบต่างกัน — B ควร diff ไบต์ body ของ N-BASE กับ M-BASE ในเฟรม 21516 B แล้วสวีปทีละฟิลด์
- **M-SKIN ไม่มีป้ายชื่อ** = สกิน `M010_001_000_N` บนต้นแบบมอนทำ nameboard หาย (สอดคล้อง RE-290: nameboard ผูกกับชนิดตัว/โมเดล) · N-SKIN (สกินเดียวกันบน NPC) ยังมีป้าย
- ผลข้างเคียงที่มีค่า: `actor_type 5` → NPC ตัวเปลือย · มอน T-pose ⇒ actor_type 5 ไม่ใช่ทางไปของ production
### nonclaims
- ไม่ได้วัดว่าสีชมพูของ M-* เท่ากับ "ผู้เล่นฝ่ายตรงข้าม" ในตารางสี — เจ้าของใช้คำว่า "ชมพู" (ตรงกับ Fighting Fish ใน R322B) · ไม่ได้คลิก/Tab หุ่น (ใบห้าม) จึงไม่มีแผงเป้าหมาย · ไม่ได้วัดว่าเฟรมใดทำให้ N-SKIN โหลดไม่ครบ (client-side) · ไม่ได้ทดสอบชุด 1 และชุด 3
- BUILD_PROPOSED: P-2 name colour | LANE-B | diff body bytes N-BASE vs M-BASE in WORLD_CENSUS_INITIAL_108_SWEEP_6 (capture_r323a) then sweep the differing fields one at a time (set 1 faction first)

## GT-299 LEARN-SKILL-REQUEST-TRIGGER-HUNT-001 — **BLOCKED-ON-PRECONDITION**
- login ตัวเดิม (Gladiator LV1 · `CHARACTER_STARTING_SKILLS cid=1 written skill_ids=(111, 40000, 99, 110)` · `LOGIN_VITALS from_row level=1`) · เปิดหน้าต่างสกิล → **แท็บ "พิเศษ" และแท็บ "Gladiator" ว่างทั้งคู่** แม้ตั้งตัวกรอง "แสดงสกิลทั้งหมด" (ภาพเจ้าของ 20:15) ⇒ ท่า 3–7 (คลิก/ดับเบิลคลิก/คลิกขวา/ลาก/ปุ่ม +) **ไม่มีอะไรให้ทำ**
- ท่าที่ทำได้พร้อมเวลา: (1)(2) เปิด/ปิด ×3 + สลับแท็บ — เสร็จ 20:11:40 · (3) คลิกซ้ายในแท็บพิเศษ (ว่าง) — 20:12:56 · (8) กดสกิลจากฮอตบาร์ ×1 — 20:17:51 · **ทุกท่า: client ส่งแค่ `GSCN_RunTimeProtocolReq` (heartbeat) · ไม่มี `DISPATCH_NESTED_VITALS … first_nested_id=0x36AA` แม้แต่ครั้งเดียวทั้งเซสชัน** (มีเฉพาะตอน login: `VITAL_WALK_REFUSED reason=unknown_vital_id vital_count=3` และ `not_a_vital_collection` ซึ่งเป็นของ login ไม่ใช่ท่า)
- **สาเหตุที่วัดได้**: รายการสกิลบนจอมาจากเฟรม `HYP_PF_033_LEARN_SKILL_RESULT_*` ที่เซิร์ฟเวอร์ยิงเฉพาะเมื่อบูตด้วย `--learn-skill-result-hypothesis-scenario` (R312/GT-249 เห็น 3/4 รายการ) · ใบ GT-299 **ห้าม**ธงนั้น และบูต production ยังไม่ส่งรายการสกิลตอน login ⇒ ใบขัดกันในตัว: ต้องการรายการบนจอแต่ห้ามสิ่งเดียวที่ทำให้มี
- **ช่องโหว่ของกฎ 0159 ที่พบ**: HEADLESS_PROOF ของใบนี้จริง (ตัวถอดเฟรมติดอาวุธ) แต่ไม่ครอบ "เงื่อนไขก่อนหน้าที่ผู้เทสต้องเห็นบนจอ" (รายการสกิล) — เสนอ COO: proof ต้องระบุ precondition ที่ผู้เทสต้องเห็น + โทเคนที่พิสูจน์ว่าเซิร์ฟเวอร์ส่งมัน
- nonclaims: ไม่อ้างว่า client ไม่มีทางส่ง 0x36AA — แค่ไม่มีอะไรให้กดในบูตนี้ · ไม่ได้ลองธง learn-skill-result (ใบห้าม) · ฮอตบาร์ช่อง Ctrl+1 กดแล้วไม่มีเฟรม อาจเพราะ slot ว่างจริงแม้มีไอคอน (ไม่ได้วัด)
- BUILD_PROPOSED: skill list at login (production) | LANE-CS | send the character's skill rows on flagless StartGame so the skill window is populated without a scenario flag; token: client skill window non-empty + a named [G>] frame at login

## ไม่ได้บูต (แจ้งไว้)
- GT-258: ใบต้องการวิดีโอต่อเนื่อง + End-Task client กลางวาป + รีสตาร์ตเซิร์ฟหลายรอบ (3–4 บูต) — ยกไปคืนที่มีเวลา · GT-276: 6 บูตแยก · GT-301: K ถอน (โทเคนไม่มีผู้เรียก)

RESULT: GT-288 MEASURED R323A 2026-09-07 19:46 (set 2: all 6 dummies drawn · N-* green · M-* pink · M-SKIN no nameplate · colour unaffected by actor_type/skin · wire actors=6 wire=114 SWEEP_6)
RESULT: GT-299 BLOCKED-ON-PRECONDITION R323B 2026-09-07 20:18 (skill window empty on non-result-scenario boot · gestures 1,2,3,8 produced zero frames · no 0x36AA)
SCOREBOARD: NONE | ผู้เล่นยังเห็นชื่อสีผิดเหมือนเดิม แต่ตอนนี้รู้แล้วว่าสีไม่ได้มาจาก actor_type/สกิน — เหลือฟิลด์ body ให้ B ไล่ · หน้าต่างสกิลยังว่างบนบูตปกติ | 20260907_2027_KA1A-R323-RESULTS-*
