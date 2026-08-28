# R210 (session 03d46t) — CORE-REQUEST-027: player login name moved from ActorAttr guild slot to BasicAttr name slot

## บริบท (v6.4 preamble ระบุเป็นจุดแก้เดียวของ prompt เวอร์ชันนี้)
`PANYA-DECISION 20260828_0125` (การทดลอง live-client ของเจ้าของเอง, 266 คำสั่ง / 2 ชม. 20 นาที)
วินิจฉัยว่าเซิร์ฟเวอร์ (สืบทอดมาจากผู้เขียน V1-V141) ส่งชื่อตัวละครลงช่อง **ActorAttr bit
`0x01000000` @ `+0x164`** ซึ่งจริง ๆ คือช่อง **ชื่อกิลด์** (`LABEL_GUILD`) ไม่ใช่ช่องชื่อตัวละคร —
ตัวละครที่เพิ่งสร้างไม่ควรมีกิลด์ติดมาด้วยอยู่แล้ว เจ้าของสั่งย้ายชื่อไปช่อง **BasicAttr bit
`0x0001` @ `+0x28`** (wstring) ซึ่งเป็นช่องที่ NPC/mob/object ทุกตัวในโค้ดนี้ใช้อยู่แล้วสำหรับชื่อของ
ตัวเอง (`BASIC_BIT_NAME` ใน `mob_death.py` / `npc_wire.py` / `remote_player_hypothesis.py` /
`hostile_hp_link_hypothesis.py`) — เหลือแค่เส้นทาง login จริงของผู้เล่นเองที่ยังไม่ได้ต่อ

R209 (รอบก่อนหน้า) วิเคราะห์ประเด็นนี้แล้ว **ตัดสินใจไม่สร้าง** เพราะตอนนั้นยังไม่รู้ mapping จริง
(`CHIEF-ASK-COO 0759`), COO ยืนตาม (`COO-DECISION 0845` "ไม่สร้าง skeleton เปล่า รอข้อมูลจริง") และ
สั่งชัดว่า: "chief: ออกแบบจุดเสียบจริงพร้อมฟิลด์แรกในรอบเดียว เมื่อมีทั้งสองใบ" — ใบ `0125` (mapping
จริงจาก probe) มีอยู่แล้ว และใบเดียวกันตอบคำถาม x1/x37 ที่ COO ขอ RE runner ยืนยัน โดยตรงจากการสังเกต
จอจริงของเจ้าของเอง (ไม่ใช่แค่ทฤษฎี) — chief ตัดสินว่านี่เพียงพอที่จะไม่ใช่ "เดาโครง" อีกต่อไป

## สิ่งที่แก้ (เฉพาะ `pirate-force-server`)
ไฟล์เดียว: `src/pirateforce_foundation/player_wire.py`, ฟังก์ชันเดียว:
`_make_actor_attr_with_name_and_class` (เอกสารตัวเองระบุว่านี่คือ "เส้นทาง login จริง" เรียกผ่าน
`legacy_bridge.py`'s `LegacyProjector.start_game`) — **ไม่แตะ** `_make_actor_attr_with_name` /
`make_actor_attr_with_name` / `make_actor_attr_with_basic_faction` (baseline แช่แข็ง NAME-002 ที่
สายอื่น crosscheck byte ปักหมุดไว้ ตามที่ docstring เดิมสั่งไว้ชัดเจน)

1. `basic_mask` เพิ่ม bit `0x0001` และ `name_wire` (wstr-tag) ย้ายไปอยู่ทันทีหลัง header ของ mask
   BasicAttr (bit ต่ำสุดมาก่อน ตรงกับลำดับ ascending-mask-bit ที่โค้ดฐานนี้ใช้ทุกที่ รวมถึง
   `npc_wire.py`'s `make_npc_attr_with_basic_faction`)
2. `ActorAttr` mask literal จาก `0x01000801` → `0x00000801` (ตัด bit `0x01000000` ทิ้ง — ไม่ส่งช่อง
   ชื่อกิลด์เลยสำหรับตัวละครใหม่ ถูกต้องเพราะไม่มีกิลด์)
3. เอา `+ name_wire` ที่ท้าย return ออก (เพราะย้ายไปอยู่ตำแหน่งใหม่แล้ว ไม่ใช่ซ้ำ/หาย)
4. ความยาวเฟรมรวมไม่เปลี่ยน (string เดียวกัน ย้ายตำแหน่ง ไม่ได้เพิ่ม/ลด)

## เทสที่แก้ตาม (byte layout เปลี่ยนจริง ไม่ใช่ regression)
- `tests/test_player_wire_probe_base1.py` — คำนวณ offset ใหม่ (ใช้ `len(wstr_tag(NAME))` แทนเลข
  ฮาร์ดโค้ด กัน brittle), mask ทั้งสองฝั่งแก้ตรง
- `tests/test_player_name.py` — `expected_prefix` แก้ mask `0x034E`→`0x034F`, ActorAttr
  `0x01000801`→`0x00000801`, ย้ายตำแหน่ง `name_wire`
- `tests/golden/foundation_v1.json`, `tests/golden/item_lifecycle_v1.json` — **เฉพาะ**
  `start_pc`/`start_frame`/`merged_start_pc`/`merged_start_frame` sha256 เปลี่ยน (คำนวณใหม่จากการรัน
  โค้ดจริง ไม่ใช่เดา) — คีย์อื่นในไฟล์เดียวกัน (`actor_wire`/`create_pc`/`list_pc`/
  `merge_response_*`) **ไม่เปลี่ยนเลย** เพราะมาจากเส้นทาง template V141 แช่แข็งคนละเส้นทาง ยืนยันด้วย
  diff ของ pytest ก่อนแก้ (เห็นว่ามีแค่ 2 คีย์ต่างในแต่ละไฟล์)
- comment ใน `player_wire.py` เดิมพลาดพูดถึงชื่อไฟล์ `field_mobs.py` ตรง ๆ ซึ่งไปชน tripwire ของ
  `tests/test_field_mobs.py` (สแกน substring `"field_mobs"` ทั้ง src/ เพื่อจับใครมาแตะโมดูลนั้นโดยไม่
  รู้ตัว) — แก้ถ้อยคำให้พ้น substring แล้ว ไม่ใช่การเลี่ยง tripwire แต่เป็นการเขียน comment ให้ไม่ชน
  โดยไม่จำเป็น (player_wire.py ไม่เคย import/เรียก field_mobs จริง)

## หลักฐาน headless
- สวีตเต็ม (`python3.11 -m pytest -q` หลังติดตั้ง `capstone`/`pefile` ในแซนด์บ็อกซ์รอบนี้เอง):
  **3750 passed, 327 skipped, 0 failed** — เขียว(cloud sanity)
- `tools/pf_pytest_precondition_census.py --report <ผลรัน>`: **PASS** — ทุก skip ถูกประกาศและปักหมุด
  ไว้แล้ว ไม่มี skip ใหม่ที่ไม่มีเหตุผล
- `tools/verify_hypothesis_ledger.py`: **PASS entries=47** — ไม่มี ledger drift
- `pf-adversary` รีวิวก่อน commit ตามกฎหัวข้อ 10 (ผลแนบท้ายรอบนี้เมื่อกลับมา)

## หลักฐานเก่าขัดแย้ง (พบโดย pf-adversary, แก้แล้ว)
เอกสาร Grade A/B เก่า (`CHARACTER-NAME-001/002`, ลงวันที่ 2026-08-16) ใน `docs/COMMAND_HANDOFF.md` /
`STATUS.md` / `docs/EXPERIMENT_LEDGER.md` / `docs/FUNCTIONAL_COVERAGE.json` อ้างตรงข้ามกับ
`PANYA-DECISION 0125` แบบเป๊ะ (รวมบรรทัดสั่งห้ามใช้ `BasicAttr +0x28` ตรง ๆ) — รายละเอียดเหตุผลที่เชื่อ
ใบ `0125` มากกว่า (ไม่ใช่ถอยกลับ) อยู่ใน `notes_to_chief/20260828_0921_CHIEF-ASK-COO-character-name-
evidence-conflict-found-by-adversary-resolved-not-blocking.md` — สรุปสั้น: เอกสาร 2026-08-19/20 อีกใบ
(`PF_CHUNK2_Q1_ACTORATTR_MASK_FINDINGS`) ขัดกับเอกสาร 08-16 เองอยู่แล้วโดยไม่มีใครคืนดี, การสังเกตจอเดิม
ไม่มี negative control, เจ้าของวินิจฉัยเองว่าเป็นบั๊กตกทอด เติม annotation แก้ไม่ลบทั้ง 4 ไฟล์ — ดัน
ไฟล์รวมของ PR รอบนี้จาก 7 เป็น 11 ไฟล์ เกินเพดาน ~6 ไฟล์ตามปกติ แต่เป็นเรื่องเดียวกัน (การันตีความ
ปลอดภัยของ diff เดียวกันที่ adversary เพิ่งรีวิว ไม่ใช่งานแยก) — เหตุผลตามกฎ §7 ข้อยกเว้น

## nonclaims
- ไม่ได้พิสูจน์บนจอจริง (attended) — เปิด `GT-122` ให้ผู้เทสยืนยัน (ผ่าน `pf-queue-author`)
- ไม่ได้แตะ "probe base 1" ส่วนที่เหลือ (HP/MP ตาม `STANDARD_STATUS`, STR/CON/DEX/INT/PER) — ยังไม่มี
  แหล่งค่าที่ commit ในเรโปนี้ตามที่ `player_wire.py`'s module docstring บันทึกไว้แต่เดิม (คนละประเด็น
  กับตำแหน่งชื่อ)
- ไม่ได้อัปเดตตาราง CORE-REQUEST registry ใน `CHIEF_CONTINUATION.md` (ตารางนั้น stale ตั้งแต่ R177 —
  หนี้เดิม ไม่ใช่ของรอบนี้ ไม่แตะเพราะเสี่ยงทำให้ดูเหมือนแถวเก่าถูกตรวจสอบใหม่ทั้งที่ไม่ใช่)

## ต่อ
- COO/สาย: CORE-REQUEST-027 landed, PR รอ merge — ดู CHIEF-REPLY แยก
- ผู้เทส: `GT-122` เปิดใหม่ รอ merge ก่อนบูตได้ (ด่าน 0 จะ BLOCKED จนกว่าจะ merge)
