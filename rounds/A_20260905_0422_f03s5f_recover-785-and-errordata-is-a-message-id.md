# LANE-A รอบ `f03s5f` — กู้ `#785` ที่ตายกับเกต + `ErrorData=50351` คือเลข id ของคลาสเอง

- เริ่ม 2026-09-05T04:22+07:00 · claim PR `pf_bridge#1256`
- ล็อกรอบ: list PR open ทั้งสองรีโปต้นรอบ — ไม่มี `[LANE-A]` เปิดค้างเลย (มีแต่ `[LANE-DB] #1255`,
  `[LANE-GM] #1254` ใน bridge และ `[LANE-UI] #788`, `[LANE-B] #787` ในเซิร์ฟเวอร์ = ไม่ใช่ล็อกของสายนี้)
  ⇒ ตัดกิ่งจาก `main` สด commit ไฟล์ร่าง push เปิด claim `#1256` แล้ว list ซ้ำ ไม่มีใบสายเดียวกันเก่ากว่า ⇒ ถือล็อก

## รอบนี้ขยับ NOW ข้อไหน

**"รอเครื่องคุณ" ข้อ 4 (`GT-233` M2 provisioning trial)** — ขยับสองอย่าง:

1. งานของรอบก่อนที่ *หายไปจาก main* ถูกกู้กลับมาแล้ว (ดูหัวข้อถัดไป) — ก่อนหน้านี้ NOW เขียนว่า
   "A `#785` เปิด 03:26 รอเกต" ซึ่งไม่จริงตั้งแต่ 03:52: มันถูกปิดโดยไม่ merge
2. คำวินิจฉัยของ `GT-233` แคบลงจาก "layout ฟิลด์ผิด (เดา)" เป็น **"ผู้อ่านของคลาสนี้เองหยุด และที่เดียว
   ที่ยังไม่มีใครอ่านทีละฟิลด์คือ outer serializer `[0x00733570,0x00733614)`"** พร้อมใบ RE แคบที่ถามตรงนั้น

**ไม่ขยับ M2 ขั้นบนจอ** เพราะบูตซ้ำถูกห้ามตามหัวใบ `BLOCKED-ON-LAYOUT` (chief R347) และคำตอบที่ต้องใช้
ต่อไปอยู่ในไบนารีไคลเอนต์ ซึ่งโคลนคลาวด์ของสายนี้ไม่มี (`client_image ABSENT`) — จดหมาย `0435` ถึง COO

## 1. กู้ `#785` (ADDENDUM ข้อ A)

`SYNC-NOTICE 0400` แจ้งว่า server `#785` (`7caacd7`) **ปิดโดยไม่ merge** เพราะเกตแดง · อ่าน gate log แล้ว
ต้นเหตุ **ตัวเดียว วัดได้**:

- คอมเมนต์บรรทัดเดียวในไฟล์เทสของรอบนั้นสะกดชื่อไฟล์ไบนารีไคลเอนต์ตรง ๆ
- `.github/workflows/gate-windows.yml` (บรรทัด ~397) ตัด `tests/*.py` **ทุกไฟล์** ที่มีสตริงนั้นออกจากการเลือกเทส
- ⇒ จำนวนโมดูลที่ถูกซ่อน 49 ≠ หมุด 48 ใน `docs/PYTEST_SKIP_PINS.json` ⇒ `pytest_subset` **และ** `skip_census`
  แดงพร้อมกัน (`WindowsGateExclusionPinTests` สองตัว) ⇒ reaper ปิดใบ

🔴 **PR body ของ `#785` เขียนว่าเทสสองตัวนั้น "แดงอยู่แล้วบน main" — ผิด** ไฟล์เทสนั้นมีอยู่บน `main` ก่อนแล้ว
การ `git checkout origin/main -- .` จึงลบ *เนื้อ* ที่เพิ่งเติมออกไปด้วย ⇒ แดงหาย ⇒ อ่านผลกลับหัวเป็น "ไม่ใช่ของฉัน"
สิ่งที่จับได้จริงคือการซ้อมเกตสองช่องตาม `AGENTS.md` (worktree ไม่มี `pf_bridge` ข้าง ๆ + `excl.txt`) ซึ่งรอบก่อน **ไม่ได้ทำ**
รอบนี้ทำแล้ว (ดูหัวข้อเทส)

วิธีกู้: `cherry-pick 7caacd7` ขึ้นกิ่งของรอบนี้บน `origin/main` สด แล้วแก้ต้นเหตุบนกิ่งตัวเอง
(ไม่ push กิ่งของเซสชันอื่น) · ของในกิ่งเดิมไม่หาย

## 2. ของใหม่ของรอบนี้ — `ErrorData` คือเลข id ไม่ใช่รหัสข้อผิดพลาด

วัดจาก artifact ที่ commit แล้วล้วน ๆ:

- **50351 = `0xC4AF` = id ของ `NavigationEx_AddSurveyDataVtial` เอง**
- กฎนี้รีโปเราเขียนไว้แล้วสำหรับอีกเลข: `delete_actor_hypothesis.py:32` / `mob_loot.py:159`
  "28317 = `0x6E9D` = `GSCN_RunTimeProtocolRes` คือ id ของคลาสเอง" · และ `0x6E9D` คือ u16 ตัวแรก
  **ในเฟรมที่ R313 จับมาได้จริง** (เทสแกะจากไบต์ ไม่ใช่เทียบค่าคงที่สองตัว)

ผลสองข้อ:

1. `msg_id = 0xC4AF` **ถูกและครบสองชั้นแล้ว** (wire: เราส่งเลขนี้ · client-observable: ไคลเอนต์แปลงเป็น
   *ชื่อคลาส* บนจอเอง) ⇒ โมดูลเลิกปฏิเสธที่จะเขียนเลขนี้ลงไป (`NAVIGATIONEX_ADD_SURVEY_DATA_VITAL_ID`)
   แต่ `encode_add_survey_data_outer` **ยังไม่มี default ให้ `msg_id`** — เลขมีบ้านพร้อมหลักฐาน ≠ composer เลือกให้ผู้เรียก
2. ErrorData บอก *ที่* ที่ผู้อ่านหยุด ไม่ได้บอก *สาเหตุ* ⇒ ถ้อยคำ R313 ("คนละรหัสกับ 28317 ⇒ layout ฟิลด์ผิด")
   ไปทิศถูกแต่ด้วยเหตุผลที่ยังไม่ครบ · สิ่งที่พิสูจน์ได้คือ envelope ชั้นนอกผ่าน → dispatch เข้าคลาสนี้ →
   **ผู้อ่านของคลาสนี้เองหยุด** ซึ่งเป็นได้ทั้งเนื้อ record และ **โครงชั้นนอกของคลาส**

`read_failure_layer(legacy, error_data)` = กฎนี้ในรูปโค้ด (`OUTER_ENVELOPE` / `THIS_VITAL` / `SOMETHING_ELSE`)
ให้รอบ attended รอบหน้าอ่านเลขบนจอแล้วรู้ชั้นทันที ไม่ต้องคิดเลขฐานสิบหกหน้าจอ

**composer ไม่ถูกแตะเลยทั้งรอบ** — ไม่มีไบต์ไหนบนสายเปลี่ยน จนกว่าใบ RE จะตอบ

## 3. ใบ/จดหมายที่ออกรอบนี้

- `notes_to_chief/20260905_0430_LANE-A-RE-TICKET-addsurveydata-outer-serializer-field-by-field.md`
  (ขอเลขใบจาก chief · ผู้ทำ = RE runner สายเดียว · ถาม: มีตัวนับ record/header ก่อน record ตัวแรกไหม)
- `notes_to_chief/20260905_0435_LANE-A-ASK-COO-rtti-static-parser-needs-the-re-runner-not-the-cloud.md`
  (งาน "static parser จาก RTTI" ที่ `0251`/R347 สั่ง สายนี้ทำบนคลาวด์ไม่ได้ — ทำข้อ 2 แทนแล้วเดินต่อ ไม่หยุดรอ)
- บริโภคแล้ว: `20260905_0400_SYNC-NOTICE-*pr785*` (stub `.CONSUMED.txt` + สำเนาเข้า `consumed/`)
- ลง stub ย้อนหลังให้ใบ `ADDRESSEE: LANE-A` อีกสองใบที่ไม่มีใครวางไว้ (ระบุในไฟล์ stub ว่ารอบไหนบริโภคจริง
  และว่า stub ลงย้อนหลังโดยรอบนี้): `20260904_1331_KA1A-R308-RESULTS-*` (XYZ เกาะ 2/3 → `#753`)
  · `20260904_1401_CHIEF-TO-LANE-A-numbers-*` (เลข `GT-233` → เนื้อใบรอบ `0foax0`)
  ⇒ ตอนนี้ไม่มีใบ `ADDRESSEE: LANE-A` ใบไหนค้างโดยไม่มี stub

## 4. เทส

- ระหว่างทำงาน (เฉพาะไฟล์ที่แตะ): `tests/test_navigationex_survey_record.py test_world_scene_travel.py
  test_world_scene_liveness.py test_world_m2_arrival.py test_lane_a_choose_npc_roster_scenes.py
  test_m2_survey_trial.py test_world_m2_provisioning_trial.py` → 271 passed, 501 subtests
- ซ้อมเกตสองช่องตาม `AGENTS.md` (worktree แยก ไม่มี `pf_bridge` ข้าง ๆ · `excl.txt` = **48 โมดูล ตรงหมุดพอดี**
  = ต้นเหตุที่ฆ่า `#785` หายจริง) บนต้นไม้ที่ merge `origin/main` สด (`9a05531`) แล้ว:
  - `pytest_subset` **exit 0** — 9579 passed, 93 skipped, 17674 subtests, 368 วิ
  - `skip_census` **exit 0** — "every skip is declared, named and pinned · RESULT: PASS"
- ชุดเต็มรันครั้งเดียวต่อรอบ = การซ้อมช่อง `pytest_subset` ครั้งนี้ (ไม่ได้รันซ้ำ)

## 5. pf-adversary

สั่งต้นรอบพร้อมเริ่มงาน (หนึ่งครั้ง · ครบโควตา 1 ใน 2 ของรอบ) — **ผลยังไม่คืนตอนจบรอบ**
⇒ `ADVERSARY_PENDING server#793` ตามกติกา (`COO 0903_2345`): push ตามเดิม ห้ามถือล็อกรอ
และ **รอบถัดไปของสาย A หยิบผล adversary เป็นงานแรกก่อน claim**
ห้ามอ่านรอบนี้ว่า "ผ่าน adversary แล้ว" — ยังไม่ผ่าน ยังไม่มีผล

## งานสำรอง 3 ข้อ (ถ้ารอบหน้างานหลักติด)

1. ตอบใบ RE `0430` เมื่อผลกลับมา แล้วแก้ composer ตามคำตอบ (ถ้ามี header จริง) + ใบ GT พ่วงบูตเดียว
2. M2 ขั้นถัดไปที่ไม่พึ่ง identity: เส้นทางทะเล/เป็นเรือของฉาก 126 ตาม travel model ของเจ้าของ
   (`world_scene_travel.py` เป็นไฟล์ของสายนี้ · ฉาก 126 ยังค้าง "ตั๋วขากลับ" ตามเทสที่รอบก่อนปัก)
3. `arrival_order` `confidence=low` ให้เฉพาะบิลด์ attended และ production ต้องปฏิเสธ `matched_as=trial`
   (`COO-DECISION 20260904_2048` — ยังไม่ได้ปิดเป็นโค้ด)

## สถานะท้ายรอบ

- push แล้วทั้งสองรีโป · **รอ merge PR `pirate-force-server#793`** (เปิด 2026-09-05T05:00+07:00 ไม่ draft ·
  marker อยู่ใน body ยืนยันด้วย GET แล้ว) · สถานะจริง = **"เปิดแล้ว รอ gate"** ไม่ใช่ "เสร็จ" ไม่ใช่ "อยู่บน main"
- claim `pf_bridge#1256` เติม marker ตอนจบรอบนี้ = ปลดล็อก
- `ADVERSARY_PENDING server#793` (ดูข้อ 5)
- ของที่ยัง **ไม่** อยู่บน main และห้ามบันทึกว่าจ่ายแล้ว: ทุกอย่างในรอบนี้ · งานของ `#785` จะถือว่ากลับมาก็ต่อเมื่อ
  `#793` merge จริง (`git merge-base --is-ancestor` เท่านั้น ห้ามใช้ฟิลด์ `merged` ของ API)
