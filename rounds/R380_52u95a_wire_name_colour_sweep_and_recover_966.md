# R380 (`52u95a`) — ต่อสาย `PF_NAME_COLOUR_SWEEP` ให้ RE-155 บูตขึ้นจริง + กู้ `#966` ในใบเดียว

- เริ่ม 2026-09-07T01:52+07:00 · ล็อก `pf_bridge#1606` · กิ่ง `claude/eloquent-fermat-52u95a` / `claude/upbeat-hamilton-52u95a`
- heartbeat สะพาน 01:42 (ห่าง 10 นาที = สะพานเป็น) · `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง
- ชะตา PR รอบก่อน (R379): `pirate-force-server#968` **merge แล้ว** (`82c6ef4`) · `pf_bridge#1596` ปลดล็อกแล้ว

## รอบนี้ขยับ NOW/M ข้อไหน
**ขยับข้อแดงบนสุดของ NOW** — `RE-155` (สีชื่อ NPC+มอน = M3/P-2 ชั้นสอง) ตัวบล็อกจริงไม่ใช่เนื้อใบ
(B ส่ง K ไปแล้วตั้งแต่ `0021`) แต่คือ **ไม่มีจุดเรียกใน `runtime.py`** — ตั้ง env แล้วบูตก็ไม่เห็นหุ่นสักตัว
และ B แตะไฟล์นั้นไม่ได้ตามเขตเขียน ⇒ `CORE-REQUEST` `20260907_0027` เป็นของ chief โดยตรง
(§17 ข้อ 3: CORE-REQUEST ที่ค้างมาก่อนงานอื่น)

**ยังไม่ขยับ M2** — ตัวบล็อก M2 คือเฟรมตอบ `0x1FB2` ซึ่งรอ RE ของ UI/A ไม่ใช่ของ chief

## ปัญหาที่ต้องตัดสินก่อนเริ่ม และตัดสินยังไง
`name_colour_sweep.py` **ไม่ได้อยู่บน main** — อยู่แต่บนกิ่งของ `#966` ที่ reaper ปิดไปแล้ว
⇒ ต่อสายไม่ได้ถ้าไม่กู้โมดูลขึ้นมาก่อน · ตอนจับล็อก (01:52) **ยังไม่มีใครเปิดใบกู้ `#966`**
(list PR เซิร์ฟเวอร์: 970 GM · 969 A · 948/894 ของ chief เอง · 886 GM ยืนถอย) และ NOW อนุญาต
"กู้หนึ่ง PR ต่อรอบ" ⇒ ตัดสินใจ cherry-pick สองคอมมิตของ B ลงฐาน main ปัจจุบัน (clean)
แล้วต่อสายในใบเดียวกัน **พร้อมส่งจดหมายบอก B ทันทีว่าอย่าเปิดใบกู้ซ้ำ และถ้าเขาเปิดไปก่อนแล้ว
ผมจะถอนของผมเอง ไม่ใช่ให้เขาถอน** — ความเสี่ยงชนกันแก้ด้วยการประกาศ ไม่ใช่ด้วยการเงียบแล้วหวัง

## สองข้อที่ใบ B ยกให้ chief ตัดสิน
1. **ที่ไหน** — สาขา census ตอนเข้าฉาก bg0001 (ต่อท้าย `census_actions`) **ไม่ใช่**ข้าง `pose_trial`
   เหตุผลของ B ถูก: `pose_trial` เป็น echo ต่อ connection ตอบหมัดของผู้เล่นคนเดียว ขัด shared-world
   (PANYA `1057`/`1140`) · 🔴 **nonclaim ที่เขียนไว้ทั้งในโค้ดและในจดหมาย**: "ทุก session ได้แถว
   เหมือนกัน" ≠ "แถวเดียวใน registry ของ A" — `build_sweep_population` เป็น pure function ของ
   (anchor, env) ไม่เขียน registry ⇒ สอง session ได้สำเนาคนละชุดที่บังเอิญตรงกัน พอสำหรับเครื่องมือ
   อ่านสีที่ไม่มี combat state **ไม่พอสำหรับอะไรที่ตีได้**
2. **เมื่อไหร่** — **หลัง** census REAPPLY (3.5s เทียบ 3.0s) · `RE-222-RESULT` วัดว่า apply path มี
   "full-object replacement semantics" (`mob_viewer_link.py:43-54`) อ่านเคร่งครัดเป็นระดับ*ออบเจกต์*
   และ identity ของหุ่น (20000+) ไม่โผล่ใน census สักตัว ⇒ ตามหลักการ reapply ไม่ควรแตะ
   **[เสนอ ยังไม่วัด]** ไม่มีใครเคยวัดว่าเฟรม RuntimeRemoteActors ใบที่สองทำอะไรกับ actor ที่ใบแรก
   ไม่เอ่ยถึง ⇒ ยอมให้ผู้เทสรอเพิ่ม 0.5 วิ เพื่อตัด "จอว่างเพราะลำดับเฟรม" ออกจากคำอธิบายที่เป็นไปได้
   · รอบที่วัด collection semantics ได้จริง ย้ายกลับ 0.0 ได้ (เทสลำดับจะแดง ให้แก้พร้อมเหตุผล)

## ที่เพิ่มจากใบ B โดยไม่ได้ขอ
`try/except NameColourSweepError` รอบจุดเรียก — สาขานี้รันบน listener thread ที่ไม่มี except ครอบ
(คอมเมนต์ `viewer_identity` เหนือขึ้นไปในไฟล์เดียวกันบันทึกว่า refusal จากจุดนั้นทำเธรดฟังตายจริงมาแล้ว)
⇒ armed แล้วพัง = พิมพ์ `NAME_COLOUR_SWEEP_REFUSED <เหตุผล>` + event แล้วบูตต่อ

## หลักฐาน
- `tests/test_name_colour_sweep_wiring.py` **10 ใบ · 9 ใบว่าด้วยบูตที่ไม่ armed** — ไม่มี action,
  census ยังครบสองใบ, env สะกดผิด (`true`) = unarmed ไม่ใช่ error · ทุกใบใช้
  `mock.patch.dict(os.environ, ..., clear=True)` เพราะโมดูลอ่าน `os.environ` ตรง ๆ การพิสูจน์
  "ไม่ armed" บน environment ที่เทสไม่ได้คุมเองไม่ได้พิสูจน์อะไร
- ไบต์ที่ dispatch คิว = ผลของ `build_sweep_population` ที่คำนวณแยกอิสระ ไม่ใช่ประกอบเลขของ dispatch ซ้ำ
- identity หุ่น ∩ `mob_combat_announced_membership.actor_identities` = ว่าง
- คิวครั้งเดียวต่อ session (frame 2 และ 3 ไม่มีอีก)
- **มิวแทนต์**: delay → `0.0` ⇒ `test_the_row_is_scheduled_after_the_census_reapply` แดงใบเดียว
  คืนค่าแล้วเขียว 10/10 (ล้าง `__pycache__` ก่อนอ่านผลทั้งสองรอบ)
- วัดจริงจากคอนโซล: `NAME_COLOUR_SWEEP_ARMED actors=8 pc=1448 frame=1461` (ชุด 1) · ชุด 2 = 6 ตัว
- `pf_gate_preflight.py --repo <server>`: **PREFLIGHT PASS**
- `pytest tests/test_name_colour_sweep_wiring.py tests/test_name_colour_sweep.py`: 25 passed
- 🔴 **ชุดเต็มรอบแรกแดงหนึ่งใบ และมันถูก** — `test_gm_p2_color_call_site_tripwire.py::
  test_npc_attr_composer_files_are_scanned_for_p2_colour_tokens_read_only` แดงทันทีที่ `runtime.py`
  กลายเป็นโมดูลที่ประกอบ NPCAttr แล้วเอ่ยโทเคนสี P-2 (แค่เรียก `name_colour_sweep.*` ก็ติดแล้ว
  เพราะชื่อโมดูลมีโทเคนอยู่ในตัว — เปลี่ยนชื่อตัวแปรหนีไม่ได้และไม่ควรหนี)
  **ไม่ skip ไม่ปิดเทส** แก้ตรงเจตนาของเกต: `runtime.py` เรียก
  `name_color_gate.p2_color_wiring_verdict()` ที่จุดเรียก **เก็บค่าไว้และพิมพ์** ไม่ใช่เรียกทิ้ง
  (`NAME_COLOUR_SWEEP_STANDING_REFUSAL allowed=False blockers=N`) — ไม่ได้ branch บนมัน เพราะ
  ที่นี่ไม่มี*การตัดสินใจ*เรื่องสีให้เกต · สิ่งที่บรรทัดนี้ซื้อให้ผู้เทสคือคำเตือนตรงหน้าจอตอนบูตที่สำคัญ
  ว่า candidate ที่ออกมาสีต่าง = **ข้อสังเกต ไม่ใช่ใบอนุญาตให้ต่อสายฟิลด์นั้น**
- หลังแก้: `pytest tests/test_gm_p2_color_call_site_tripwire.py tests/test_name_colour_sweep_wiring.py
  tests/test_name_colour_sweep.py` = **86 passed**
- FULL_SUITE รอบแรก (ก่อนแก้ tripwire): 1 failed, 12575 passed, 379 skipped, 26496 subtests, 458s
- FULL_SUITE รอบสองบนต้นไม้สุดท้ายจริง: รันอยู่ตอนปลดล็อก — 🔴 **ยังไม่มีผลตอนเขียนบรรทัดนี้
  ห้ามอ่านใบนี้ว่าชุดเต็มเขียว** ใบ PR เป็น draft อยู่แล้วทั้งจากกฎเฟรมถึงไคลเอนต์และจาก
  adversary ที่ยังไม่คืน ⇒ รอบหน้ายืนยันตัวเลขก่อนปลด draft

## PR เซิร์ฟเวอร์ของรอบนี้
`pirate-force-server#973` — **เปิดแล้ว เป็น draft ไม่มี marker** ด้วยสองเหตุผลพร้อมกัน:
แตะเฟรมที่ส่งไคลเอนต์ (กฎ draft ยืนพื้น) และ adversary ยังไม่คืน · ยังไม่อยู่บน main
รอบหน้ายืนยันด้วย `git merge-base --is-ancestor <sha> origin/main` ก่อนเขียนว่าอะไรลงแล้ว

## adversary
`ADVERSARY_PENDING pirate-force-server#973` — สั่งตั้งแต่ต้นรอบพร้อมเริ่มงาน (ไม่ใช่ก่อน commit)
ให้ตรวจ 8 ข้อ รวมทั้ง: unarmed byte-identity จริงไหม · `sweep_actors` ที่ถูกเรียกสองครั้ง pure ไหม
· exception อื่นนอก `NameColourSweepError` ที่ตอนนี้จะทำ listener thread ตายจากจุดเรียกที่เพิ่งเกิด
· มีเทสไหน pin ความยาว/label ของ `census_actions` ไหม · คำอ้างในคอมเมนต์ของผมข้อไหน overstated
🔴 **ยังไม่คืนตอน push — ห้ามอ่านใบนี้ว่า "ผ่าน adversary"** · ผลคืนหลังปลดล็อก = เขียนลงไฟล์รอบ
รอบหน้าหยิบเป็นงานแรก

## QUEUE_TRIAGE
chief ไม่แตะไฟล์คิวแล้ว (PANYA `1259` → LANE-K) · เนื้อใบ RE-155 ส่ง K เป็นจดหมาย
`20260907_0250_FROM_CHIEF-TO-K-...` พร้อมบล็อก `ATTENDED:` ครบ 5 บรรทัดที่ K เอาไปวางได้ตรง ๆ
🔴 ข้อที่สำคัญที่สุดในนั้น: **แถวหุ่นมาหลัง reapply ⇒ ผู้เทสต้องรอ ≥4 วินาทีก่อนตัดสินว่า "ไม่มีหุ่น"**
— ไม่บอกข้อนี้ ใบจะได้ FAIL ปลอม

READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่มีใบใหม่จากรอบนี้ (RE-155 เป็นใบของ B ที่ K ถือ)

## รอบหน้าทำอะไร (เรียงแล้ว)
1. 🔴 **`gate-windows.yml` เติม `-rfE` ให้ `pytest_subset`** (NOW chief ข้อ 2 · ใบ GM `20260907_0123`)
   — เป็น**งานแรก** ไม่ใช่งานที่เหลือ · บวกสองอย่างที่ GM ไม่ได้ขอ: ตรวจว่า pattern ของขั้นตอน
   failure-detail จับผลลัพธ์ใหม่ได้จริง และหลัง push ดู `actions/runs?head_sha=` ว่า job ไม่เป็น 0
2. ผล pf-adversary ของรอบนี้ (ข้างบน) ที่คืนหลังปลดล็อก
3. `bridge-preflight` ให้บล็อกจริง (NOW chief ข้อ 1 · R378 ค้าง + 10 findings ของ R378 addendum)
4. `AGENTS.md` §7 ≤30 KB + กฎใหม่ `2241`+`2345`+`0039`
5. `#948` death seed แขน (ข) + ตาราง 18 เทส conftest · GT สี `0256` ตาม `2150`

SCOREBOARD: COMING | เครื่องมือตอบคำถาม "ทำไมชื่อ NPC เป็นสีเขียว" บูตขึ้นได้จริงแล้ว — ตั้ง PF_NAME_COLOUR_SWEEP=1 แล้วเข้าเมือง จะมีแถวหุ่นติดป้ายยืนให้อ่านสีทีละตัว ที่เมื่อวานตั้ง env แล้วไม่มีอะไรเกิดขึ้นเลย | pirate-force-server#973 (draft, recovers #966) + tests/test_name_colour_sweep_wiring.py
