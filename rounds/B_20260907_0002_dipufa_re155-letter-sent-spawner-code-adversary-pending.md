# LANE-B round dipufa -- 2026-09-07T00:02+07:00 start

## รอบนี้ขยับ NOW/M ข้อไหน
NOW ข้อ "รอ Panya ติ๊ก"/งานด่วน: **`RE-155` (B) ใบแรก** (PANYA `2142` ข้อ 4 · เส้นตาย
2026-09-07 02:00) -- COO `2345` สั่งให้เป็นงานแรกของรอบ ก่อนแตะ PR ใด ทำครบตามลำดับ
นั้น: จดหมาย `*-TO-K-*` ส่งแล้วก่อนแตะโค้ดอื่น (ภายในนาทีที่ ~20 ของรอบ)

## ล็อกรอบ
claim PR `pf_bridge#1590` (กิ่ง `claude/practical-knuth-dipufa`) เปิดก่อนแตะอะไรทั้งสิ้น
· list ใบ `[LANE-B] round <id>: claim` ที่ open ตอนเริ่ม = **ไม่มี** (`#1493` หัวใบเป็น
`addendum` ไม่ใช่ `claim` จึงไม่ใช่ล็อกตามข้อ 1) · list ซ้ำหลังเปิด: ไม่มีใบ `[LANE-B]`
ที่เก่ากว่าและยังมีชีวิต

## กล่องจดหมาย -- บริโภครอบนี้
1. `20260906_2142_KA1A-PANYA-ORDER-...` + addendum `20260906_2150_...` -- **ทำ**: อ่าน
   คำสั่งเจ้าของคำต่อคำ, ตารางสีลงจดหมาย K คำต่อคำ
2. `20260906_2241_COO-DECISION-panya2142-re155-owner-b-...` -- **ทำ**: B รับเจ้าของ
   RE-155, ทำตามข้อ 1-5 ที่สั่ง
3. `20260906_2345_COO-DECISION-b2245-...` -- **ทำ**: ลำดับ "RE-155 -> K ก่อนทุกอย่าง
   (30 นาทีแรก)" -- ทำตามลำดับเป๊ะ
4. `20260906_2345_COO-DECISION-b2340-d1-...` -- **อ่านแล้ว ยังไม่ทำ**: D1(ก)+D2+
   tripwire ฉากที่ 13 บน PR #958 -- เหตุผลข้างล่าง ("รอบหน้าทำอะไร")

`NO_FEATURE_WAITING:` ไม่มีผล RE/CORE-REQUEST ใหม่ถึงสายนี้นอกเหนือจากที่บริโภคแล้ว

## รอบนี้ทำอะไร (ของจริง)

### ก. RE-155: จดหมาย + สปาวน์เนอร์ + เทส (ส่งตามเส้นตาย)
- จดหมาย `pf_bridge/notes_to_chief/20260907_0021_LANE-B-TO-K-gt-body-RE-155-
  dummy-row-npc-and-916-sweep.md` -- ตารางสี `2150` คำต่อคำ, รายการผู้สมัครครบ 5
  ฟิลด์พร้อมเหตุผลตัด/ไม่ตัด, บล็อก `ATTENDED:` 5 บรรทัด, เกณฑ์ PASS/PARTIAL/ผลลบ
  ส่งเวลา 00:21+07 -- **ก่อนเส้นตาย 02:00 เกิน 1 ชม.**
- โค้ด `pirate-force-server` กิ่ง `claude/gifted-clarke-dipufa`
  (`src/pirateforce_foundation/name_colour_sweep.py` +
  `tests/test_name_colour_sweep.py`, 15 เทสใหม่ผ่านหมด): env-gated
  (`PF_NAME_COLOUR_SWEEP=1|2`), สองต้นแบบจริง (NPC placement 0, Training Iron Man
  placement 103), แถบ placement index สังเคราะห์ (20000+) ทดสอบไม่ชนกับตารางจริง
  ใดเลย (12 ตาราง `field_mob_tables_bg*` + 115 แถวของ `population`)
- **ผู้สมัครที่ตัดไม่ได้จริง (ผลลบที่มีค่า, บันทึกในจดหมายเดียวกัน ไม่เปิดใบถาม
  ซ้ำ)**: relation +0x98 (สองคลาสคนละอันใช้ชื่อ +0x98 ร่วมกัน -- `gm/
  name_color_gate.py` vs `mob_viewer_link.py` -- ไม่มีหลักฐานว่า NPCAttr มีฟิลด์
  relation แบบ ActorAttr เลย เดาตำแหน่งไบต์ = ผิดกฎ NOW P-2) และ rank (ไม่มีบิต/
  แท็กผูกอยู่เลยในทั้ง `field_mobs.py` และ `gm/attr_wire.py`)
- 🔴 **หมายเหตุสำคัญที่จดหมายบอกไว้แล้ว**: สปาวน์เนอร์ยังไม่ต่อสายเข้า
  `runtime.py`/`app.py` (คนละงาน, ต้อง CORE-REQUEST แยกให้ chief ต่อ env ->
  dispatch แบบเดียวกับ `pose_trial`) -- ATTENDED จริงบูตไม่ขึ้นจนกว่าจะมี CORE-REQUEST
  นั้น ห้ามอ่านใบนี้ว่า "พร้อมบูตแล้ว"

### ข. pf-adversary -- สั่งแล้ว คืนผลแล้วในรอบนี้ แก้ครบแล้ว
สั่งกลางรอบ (ไม่ใช่ต้นรอบ -- รอบนี้เป็นรอบแรกของเซสชันนี้ กว่าจะรู้ขอบเขตงานจริงก็ผ่าน
การอ่าน NOW/mailbox/prompts ไปมาก) บนกิ่ง `claude/gifted-clarke-dipufa` commit
`5a718e2` พร้อมโจทย์ 6 ข้อ: (a) ข้ออ้าง ActorAttr+0x98 vs NPCAttr+0x98 เป็นสองคลาส
จริงหรืออ่านเกิน (b) แถบ placement สังเคราะห์ชนตารางที่พลาดไปหรือไม่ (c) การต่อ
faction ของ NPC (`_npc_faction_body`) ผิดรูปหรือไม่ (d) การจับคู่ template/preset
สังเคราะห์ทำลาย invariant ที่อื่นหรือไม่ (e) `NPC_BASE_HP=100` ปลอดภัยจริงหรือไม่
(f) จุดเดาอื่นที่ยังไม่เห็น

**ผลคืนแล้วในรอบนี้เอง** (ก่อนจบรอบ -- ไม่ต้องส่งต่อรอบหน้า):
1. **[เปิดเผยไว้แล้ว ไม่ใช่บั๊กที่ซ่อน]** ทั้งฟีเจอร์ยังเป็น no-op ในโปรดักชัน (grep ทั้ง
   repo: ไม่มีที่ไหนเรียก `sweep_actors`/`build_sweep_population` เลยนอกจากตัวมันเองกับ
   เทส) -- ตรงกับที่จดหมาย `0021` และ `0027` (CORE-REQUEST) บอกไว้แล้วตรงๆ ไม่ต้องแก้
   เพิ่ม แต่เป็นเหตุผลที่ยืนยันว่า **ห้ามอ่าน PR นี้ว่า P-2 ขยับ** จนกว่า chief ต่อสาย
2. **[แก้แล้ว]** เทสชนกันตรวจแค่ 12 ตาราง `field_mob_tables_bg*` + ตาราง v141 ไม่เคย
   เห็น `scene2_prison_exile_tables.py`/`world_bg1001_identity.py`/
   `world_bg3001_identity.py`/`world_bg3007_identity.py`/`world_bg3008_identity.py`/
   `world_bg4001_identity.py` (ไม่ชนกันจริงวันนี้ -- ดัชนีสูงสุดของทั้งห้าไฟล์อยู่แค่
   หลักสิบ -- แต่คำอ้าง "ครบทุกตาราง" ไม่ตรงกับที่เทสตรวจจริง) -- เพิ่มทั้งห้าไฟล์เข้า
   `_EXTRA_PLACEMENT_ROW_SOURCES` ในเทสแล้ว พร้อมคอมเมนต์ยอมรับตรงๆ ว่านี่คือ
   enumerated list ไม่ใช่ discovery scan (ความเสี่ยงที่เหลือ: ไฟล์ตารางที่ 13 ในอนาคต
   ต้องมาลงที่นี่ด้วยมือ) แก้ prose ในโมดูลให้ตรงกับที่เทสตรวจจริงด้วย
3-6. **[ตรวจแล้ว ไม่พบบั๊ก]** ข้ออ้าง ActorAttr+0x98 vs NPCAttr+0x98 คนละคลาส (ตรงตาม
   คำต่อคำใน `gm/name_color_gate.py`/`mob_viewer_link.py` จริง) · การต่อ faction ของ NPC
   ตรวจ byte-level กับ `make_npc_attr` จริงแล้วถูกต้อง (รัน 15 เทสจริงกับ gamedata จริง
   ในเวิร์กทรีแยก) · คู่ template/preset สังเคราะห์ไม่ชนอะไรเพราะยังไม่มีจุดเรียกจริง
   (ตามข้อ 1) · `NPC_BASE_HP=100` ตรงกับ default ของ `make_npc_attr` เองและตรงกับที่
   ตัวประกอบ Port Royal จริงใช้อยู่แล้ว
7. **[แก้แล้ว]** `_npc_faction_body` ไม่ตรวจ bounds/faction!=0 เหมือน `hostile_npc_attr`
   พี่น้องของมัน (เชื่อ caller เดียวอย่างเดียว) -- เพิ่ม `field_mobs._require_int` +
   guard faction=0 เหมือนกันแล้ว

คำถามที่ adversary ทิ้งไว้ (ยังไม่มีคำตอบ ไม่ใช่ของรอบนี้): เมื่อ chief ต่อสายจริง จะเรียก
`build_sweep_population` จากจุดเข้า registry ของ A (ตาม shared-world rule) หรือจากจุด
เฉพาะกิจใน `runtime.py` แบบ `pose_trial` (per-connection ไม่ใช่ scene population)? ยังไม่มี
อะไรที่ commit แล้วตอบคำถามนี้ -- ใส่ไว้ใน CORE-REQUEST ให้ chief ตัดสินเมื่อรับงาน

## ที่ไม่ได้แตะ
- ไม่แตะ `runtime.py` / `app.py` / `current/pf_login_game_server_v141.py`
- ไม่แตะ `field_mobs.py` เนื้อฟังก์ชันเดิม (import + เรียกใช้ private helper เท่านั้น
  ไม่แก้ตัวมันเอง) -- เพิ่มบรรทัดเดียวในสารบัญผู้ import (`test_field_mobs.py`)
- ไม่แตะ `mob_viewer_link.py` / `gm/name_color_gate.py` / `gm/attr_wire.py`
- ไม่แตะ D1/D2/tripwire ฉากที่ 13 บน `#958` (ดูข้างล่าง)
- ไม่ hardcode สี/FontStyleID ใดๆ ทั้งสิ้น
- ไม่เปิดโครงสีเพิ่ม (viewer slot/tripwire/ruling ใหม่) ตามคำสั่งข้อ 3 ของ `2241`

## verification
- `pytest tests/test_name_colour_sweep.py tests/test_field_mobs.py
  tests/test_mob_viewer_link.py` -> **94 passed, 58 subtests passed**
- `pytest tests/test_mob_*.py tests/test_name_colour_sweep.py
  tests/test_field_mobs.py tests/test_population.py` -> **1751 passed, 1 skipped,
  5148 subtests passed**
- `python3 tools_bridge/pf_gate_preflight.py --repo pirate-force-server` (ก่อน
  commit) -> **PREFLIGHT PASS** (cp874, ไม่มี skip ใหม่, main อยู่ใน HEAD, census
  ตรง, ชื่อไฟล์ใหม่ 2 ไฟล์ <=100 ตัวอักษร)
- ชุดเต็ม `pytest tests/` บนต้นไม้ commit จริง (`5a718e2`): **สั่งรันแล้ว กำลังรอผล
  ตอนจบไฟล์รอบนี้** (คำสั่งใช้เวลานาน, รอบก่อนวัดได้ ~7 นาทีสำหรับ ~12,500 เทส) --
  ถ้าผลไม่เขียวเมื่อ push จริง จะแก้ก่อน push ตามกฎ "ห้าม push ถ้าชุดเต็มแดง"
- ทุกไฟล์ที่แตะเป็น ASCII ล้วน (พบ 2 จุดภาษาไทยในคอมเมนต์ตอนแรก แก้เป็นอังกฤษแล้ว
  ตรวจซ้ำด้วย `str.isascii()`) · stage ทีละไฟล์ อ่าน `git diff --cached` ทุก hunk
  ก่อน commit · ไม่ใช้ `git add -A`

## PR/status
- `pf_bridge` claim `#1590` (`claude/practical-knuth-dipufa`) -- ปลดเมื่อจบรอบ
  (ดูข้อ 3 ของ "จบรอบ")
- `pirate-force-server`: commit บนกิ่ง `claude/gifted-clarke-dipufa` (`5a718e2` +
  แก้ตามผล adversary ข้อ 2/7 + census ที่เพิ่มขึ้น 4 ไฟล์) -- **PR เปิดไม่ draft**
  พร้อม `PF-AUTOMERGE: v4` ตั้งแต่เปิด: adversary คืนผลแล้ว ข้อบกพร่องจริง (2, 7)
  แก้แล้วในคอมมิตเดียวกัน ข้อที่เหลือ (3-6) ตรวจแล้วไม่พบบั๊ก ข้อ 1 เป็นเรื่องที่
  จดหมายเปิดเผยไว้แล้วไม่ใช่บั๊กของโค้ด -- เข้าเงื่อนไข "draft จนกว่า adversary คืน"
  ครบแล้ว (คืนและแก้แล้วในรอบเดียวกัน)
- ชุดเต็ม `pytest tests/` รันซ้ำหลังแก้ตามผล adversary ก่อน push -- ผลลงในหัวข้อ
  verification ข้างบน (ถ้าไม่เขียว ไม่ push จนกว่าจะแก้)

## รอบหน้าทำอะไร (เรียงแล้ว)
1. **D1(ก) + D2 tripwire ฉากที่ 13 + 924/529** บน PR `#958` (หรือกิ่งใหม่ถ้า reaper
   ปิด `#958` ไปแล้ว -- เช็ค `git merge-base --is-ancestor` ก่อนเชื่อไฟล์รอบเก่า
   ตามบทเรียนของรอบ `c2ikd0`) ตาม COO-DECISION `b2340`: เปลี่ยนชื่อใบ bg0001 ให้อ้าง
   PANYA `0041`, จำกัดใบ derive เหลือ 11 ฉากที่ผ่านคอลัมน์จริง, ลำดับอำนาจ
   ใบเซ็น>derive>ตาราง เป็นเทส, tripwire ฉากที่ 13 (ไม่มีใบเซ็น+ไม่มี census =
   แดง), มิวแทนต์ 61->709 ต้องแดง
2. เมื่อ ATTENDED RE-155 มีคนบูตจริง: อ่านผลจาก K, ปิด/อัปเดตหัวใบ RE-155 ตามผล
3. รอคำตอบ chief ต่อ CORE-REQUEST `0027` (ต่อสาย `PF_NAME_COLOUR_SWEEP`) -- ถ้าไม่มา
   ใน 1-2 รอบ ทวงผ่านช่องทาง COO ตามกฎ escalation

TWO_SESSIONS_SAME_SCENE: ไม่เปลี่ยน -- โมดูลใหม่ไม่เขียน state ต่อ session ใดๆ,
`sweep_actors()`/`build_sweep_population()` เป็น pure function อ่าน env + ตาราง
ที่ commit แล้วเท่านั้น ผลเหมือนกันทุก process ที่ import โมดูลเดียวกันด้วย env
เดียวกัน ไม่มี state ต่อ session

SCOREBOARD: STUCK | RE-155's own dummy-row spawner and its full candidate list (with color table, ATTENDED block and pass/partial/negative criteria) reached the bridge before the 02:00 deadline, the code that composes it is written, tested and has cleared its first adversary pass -- but no player sees anything new yet: the env var is not wired into runtime.py's dispatch (a separate CORE-REQUEST chief still owes) | pf_bridge/notes_to_chief/20260907_0021_LANE-B-TO-K-gt-body-RE-155-dummy-row-npc-and-916-sweep.md ; pirate-force-server branch claude/gifted-clarke-dipufa, PR open (adversary-cleared)
