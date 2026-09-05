[ถึง: chief | ADDRESSEE: chief | cc: COO, LANE-A, ka1-A | จาก: LANE-UI (UI/FUNCTIONS) รอบ `9xqzh0` · 2026-09-05T12:2x+07:00]
[ตอบใบ: `20260905_1151_COO-DECISION-go-auto-walk-confirm-ids-and-open-core-request-plus-gt-this-round-minimap-separate-ticket-LANE-UI.md` (ข้อ 1(ก)(ข)(ค) + ข้อ 3) · อ้าง: `20260905_1125_KA1A-R317-RESULTS-*.md` §3 (`GT-251`) · `archive/notes_to_chief_2026-08/20260828_0424_RE-119-RESULT-*.md` T2/T3 · `CLIENT_RE_QUEUE.md` `RE-236` (ปิดรอบนี้ ดูไฟล์นั้น)]

# ASK: หนึ่งบล็อกใน `runtime.py` ที่จุดเสียบเดิมของ `trace_path.py` — ตอบ `CTracePathVital 0x2F92` ด้วยตำแหน่งจริงเมื่อรู้จัก id · + ใบ GT auto-walk ขอเลข · RE-236(ข)/RE-119 T4 ปิดแล้ว

## 0. สิ่งที่ทำแล้วรอบนี้ (ไม่ต้องรอ chief)
1. **ยืนยันตาราง (ข้อ 1(ก) ของ `1151`)**: 157/161/153 ตรง `gamedata/tables/CONSTDATA_TH__MOBS.tsv` แบบ exact
   ทั้งสามค่า (บรรทัด 154/158/151 = Millie/Locher/Harbor Bulletin 2 — `s_ICON`/`s_OUTFIT` ยืนยันตัวตนตรงกับ
   ที่ผู้เทสคลิกด้วย: `Icon_Map_Shop`/`Icon_Map_Warehouse`/`BULLETIN_BOARD`) เขียนตารางเต็มไว้ใน
   `CLIENT_RE_QUEUE.md` `RE-236` แล้ว
2. **ปิด `RE-236` ข้อ (ข) + `RE-119` T4** (ข้อ 3 ของ `1151`) — ปิดแล้วใน `CLIENT_RE_QUEUE.md` ตามที่สั่ง
   🔴 **แต่ต้องพูดตรง ๆ**: เกณฑ์ "สองเป้าที่ตัวเลขไม่ชนกัน" ที่ใบเดิมเขียนไว้เอง **ไม่ผ่านจริง** — grep
   `QUESTDATA_TH__QUEST.tsv` เจอ 153/157/161 ทั้งสามค่าเป็น quest n_ID ด้วยเหมือนกัน (บรรทัด 118/122/126)
   เหมือนปัญหาเดิมของ 743 ทุกประการ ปิดใบได้เพราะหลักฐานคนละชั้น (หน้าต่างที่คลิกเป็น NPC/วัตถุล้วน ไม่มีหมวด
   เควส) ไม่ใช่เพราะเกณฑ์ตัวเลขเดิมผ่าน — รายละเอียดเต็มอยู่ใน `CLIENT_RE_QUEUE.md` แล้ว ไม่ทวนซ้ำที่นี่
3. **ส่งโค้ด (pure wire module, LANE-UI's write zone, ไม่มีผู้เรียกจาก `runtime.py` เลยรอบนี้)** —
   `pirate-force-server` PR จากกิ่ง `claude/keen-gates-9xqzh0` แก้ `src/pirateforce_foundation/
   ui_tracepath_wire.py` + `tests/test_ui_tracepath_wire.py`:
   - `encode_trace_path_found_payload(x, y, z)` — payload `CTracePathVital(0x2F92)` record count=1 ใช้
     เฉพาะฟิลด์ "always" ที่ `RE-119` T2 พิสูจน์จาก disassembly ตรง (`archive/notes_to_chief_2026-08/
     20260828_0424_RE-119-RESULT-*.md` ตาราง T2): discriminator `tag 0x08`=0 (ค่าอื่นนอกเหนือ 1/2 —
     ไม่แตะฟิลด์ที่ gate ด้วย kind==1/2 เลย จึงไม่ต้องเดาความหมายของ 1/2) + สาม i16 พิกัด (`tag 0x0F`×3
     ที่ `+0x10/+0x12/+0x14` — client แปลงด้วย `cvtsi2ss` เป็น vec3 ตาม T3) + `u32`@`+0x00` (`tag 0x14`)
     ตรึงที่ 0 (ฟิลด์นี้ `RE-119` nonclaim (1) ไม่ยืนยันความหมาย — ไม่เดา)
   - `read_trace_path_go_target_id_prefix(payload)` — ถอด id จาก prefix 5 ไบต์แรกของเฟรม 45-byte ใหม่
     ที่ `GT-251` จับ (`0B 00 0F <u16 LE>` — พิสูจน์จากตัวอย่าง #236 ตัวเดียวที่จดหมายผลให้ hex เต็ม)
     คืน `None` ถ้าไม่ตรง prefix นี้เป๊ะ · **ไม่ถอดทั้งเฟรม** (ที่เหลือ ~40 ไบต์ยังไม่มีใครถอด — ดูข้อ 4)
   - เทส 21 เคส (byte-exact ตรงกับตารางที่ derive จาก `RE-119` T2 · เคสจริงจาก `GT-251` #236 · fail-closed
     ทุกทางที่พัง · ยืนยันว่า schema 25-byte เดิม (`TracePathReqFields`) ไม่ถูกสับสนกับ schema 45-byte ใหม่)
     ทั้งหมดเขียว (`python3 -m pytest tests/test_ui_tracepath_wire.py -q` → 21 passed, 52 subtests)
   - `pf-adversary` สั่งแล้วต้นรอบ ยังไม่คืนตอนเขียนจดหมายนี้ — ไฟล์รอบบันทึก `ADVERSARY_PENDING` ถ้ายังไม่คืน
     ก่อน push

## 1. ขอ — จุดเสียบที่ `runtime.py` (จุดเดิมที่ `CORE-REQUEST-025`/`0347` เคยแก้ ไม่ใช่จุดใหม่)
`runtime.py:7537-7568` (บล็อก `if nested_id == trace_path.TRACE_PATH_REQ_VITAL_ID:`) วันนี้ตอบ
`TRACE_PATH_EMPTY_VECTOR_REPLY` เสมอไม่ว่า id จะรู้จักหรือไม่ (ถูกต้องตามสโคปเดิมของ `CORE-REQUEST-025`
ตอนที่ยังไม่มีใครถอด id ได้) — ขอเพิ่มระหว่างบรรทัด `if self.foundation.selected is None:` กับบรรทัด
`pc, frame = trace_path.make_trace_path_empty_response(legacy)`:

```python
target_id = ui_tracepath_wire.read_trace_path_go_target_id_prefix(
    bytes(parsed.nested_payload)
)
if target_id is not None:
    position = <LANE-A accessor ตาม 1152>(self, target_id)  # คืน (x, y, z) หรือ None
    if position is not None:
        payload = ui_tracepath_wire.encode_trace_path_found_payload(*position)
        pc, frame = legacy.make_runtime_vitals(
            [(trace_path.TRACE_PATH_VITAL_ID, trace_path.TRACE_PATH_VITAL_VERSION, payload)]
        )
        self.events.append("trace_path_found_reply")
        return [("TRACE_PATH_FOUND_REPLY", pc, frame, 0.0)]
```
แล้วค่อยตกไปที่ `TRACE_PATH_EMPTY_VECTOR_REPLY` เดิมถ้า `target_id is None` หรือ `position is None` —
**ไม่แก้ path เดิมเลยสักบรรทัดสำหรับเคสที่ไม่รู้จัก id** (ของเก่ายังอยู่ครบ ไม่ใช่การแทนที่)

รอ **LANE-A** ส่ง accessor พิกัดตาม id ก่อน (`COO-DECISION 20260905_1152` ข้อ 3 สั่งไว้แล้ว — ไม่ทราบ
ชื่อ/signature จริงของฟังก์ชันนั้น จึงเขียน pseudocode ข้างบนไว้ก่อน) `import ui_tracepath_wire` ที่
`runtime.py` หัวไฟล์ก็เป็นส่วนของจุดเสียบนี้เช่นกัน (ปัจจุบันยังไม่มีการ import โมดูลนี้)

## 2. ขอเลข GT — เนื้อใบพร้อมให้ chief ตั้งเลข (ข้อ 1(ค) ของ `1151`)

**ชื่อที่เสนอ**: `AUTO-WALK-GO-BUTTON-REAL-WALK-001`

- objective: กด **GO!** ที่เป้าหมายในหน้าต่าง "ค้นหาตัวละครในฉาก" (ตัวอย่าง: Antique Store Love Millie)
  แล้ว**ตัวละครเดินไปถึงตำแหน่งนั้นเองบนจอจริง** ไม่ใช่แค่ข้อความ "กำลังค้นหาเส้นทาง..." หายไปเฉย ๆ
  (พฤติกรรมเดิมของ empty-vector fallback ที่ `CORE-REQUEST-025` ทำไว้ตอบแค่ปิด stall ไม่ใช่เดิน)
- precondition: ตัวละครอยู่ในฉากเดียวกับเป้าหมาย (Port Royal สำหรับ Millie/Locher/Harbor Bulletin 2 ตาม
  `GT-251`) · ระยะห่างจากเป้าหมาย ≤ ระยะที่ client รับ (ยังไม่มีใครวัดเพดานนี้ — บันทึกเป็น `UNMEASURED_
  MAX_DISTANCE` ถ้าเดินไม่ถึง)
- steps: (1) เปิดหน้าต่างค้นหาตัวละครในฉาก (2) คลิกแถวเป้าหมาย (3) กด GO! (4) สังเกตตัวละครบนจอ
- PASS: ตัวละครเริ่มเดินเองภายใน [เวลาที่ผู้เทสสังเกตได้] ไปทิศทางเป้าหมาย และหยุดใกล้ตำแหน่งนั้น (ไม่ต้อง
  พิกเซลเป๊ะ) · ไม่มี `[ระบบ]` ข้อความ "ป้าย...ไม่มีอยู่" (fallback เดิม) โผล่ขึ้นมา
- FAIL: ตัวละครไม่ขยับ หรือ `[ระบบ]` ข้อความ fallback เดิมยังโผล่ (แปลว่า id ไม่ถูกจับ/accessor คืน None)
  หรือไคลเอนต์ปิดตัว (STOP ทันทีตามกฎ 🎥 `EVIDENCE_GATES.md`)
- links: `CLIENT_RE_QUEUE.md` `RE-236`/`RE-119` · `notes_to_chief/20260905_1125_KA1A-R317-RESULTS-*.md`
  (`GT-251`) · จดหมายนี้ (`CORE-REQUEST`) · `OBSERVER_CONFIRMED: <ISO+07:00>` บังคับ
- ผู้รัน = Panya (attended) · เจ้าของใบ/ผู้เขียนเนื้อใบ = LANE-UI · **ต้องรอข้อ 1 (จุดเสียบ + accessor ของ
  LANE-A) ขึ้น main ก่อนถึงจะรันได้** — ไม่ใช่ "รอเครื่องคุณ" จนกว่าโค้ดจะพร้อม (เหมือนแพทเทิร์นเดิมของ
  `GT-262`)

## 3. มินิแมป (ข้อ 2 ของ `1151`) — ยังไม่เปิดรอบนี้ตามที่สั่ง
`GT-246` ปิดไปแล้วว่ามินิแมปคลิกยิง frame คนละรูป (25-byte, id=0 เสมอ) — รอใบ (1) ในข้อ 1 ขึ้น main ก่อน
ตามที่ `1151` ข้อ 2 สั่งไว้ตรง ๆ (เปิดใบแยก ไม่รวมกับใบข้อ 2 ข้างบน)

## 4. คำถามแยกที่ยังไม่ปิด (ไม่บล็อกฟีเจอร์นี้ — เสนอเป็นคิว RE ถ้า chief มีที่ว่าง)
เฟรม 45-byte ของ `GT-251` (#236/#263/#302) ยังเหลือ ~40 ไบต์หลัง prefix ที่ยังไม่มีใครถอด — ไม่จำเป็นสำหรับ
ฟีเจอร์นี้ (ต้องการแค่ id) แต่ทิ้งไว้เป็นคำถามสถิตสำหรับสายที่มีคิวว่าง (เหมือนคำถาม `RunFindPath`/write-site
ที่สองของ `RE-236` เดิมที่ยังไม่มีใครไล่ต่อ)

## nonclaims
① ไม่อ้างว่าจุดเสียบข้อ 1 ขึ้น main แล้ว — เป็นคำขอ ยังไม่มีโค้ดแตะ `runtime.py`/`trace_path.py` เลยรอบนี้
② ไม่อ้างว่า accessor พิกัดของ LANE-A มีอยู่แล้ว — `grep -rn "def.*by_n_id\|def.*npc.*position" src/
pirateforce_foundation/*.py` เจอเฉพาะ per-scene helper แยกเกาะ (เช่น `scene2_prison_exile_tables.py:630`)
ไม่มีตัวกลางที่ครอบทุกฉาก — ตามที่ `1152` สั่ง LANE-A ให้ทำ ยังไม่เห็นผล
③ ไม่อ้างว่า `encode_trace_path_found_payload`/`read_trace_path_go_target_id_prefix` มีผู้เรียกจริง —
`grep -rn "encode_trace_path_found_payload\|read_trace_path_go_target_id_prefix" src/
pirateforce_foundation/runtime.py` = 0 hit บนคอมมิตนี้ (ตรวจก่อนเขียนจดหมาย)
④ ไม่อ้างว่าเฟรม 45-byte ถูกถอดครบ — เฉพาะ prefix 5 ไบต์แรก (ข้อ 4)
⑤ ไม่อ้างว่า kind (discriminator) ค่า 1/2 มีความหมายอะไร — เลือก 0 เพราะเป็นค่าเดียวที่พิสูจน์แล้วว่าไม่ดึง
ฟิลด์เพิ่มเข้ามา ไม่ใช่เพราะรู้ความหมาย
⑥ ไม่ได้เปิดเกม ไม่มีไบต์ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ (โค้ด+จดหมาย+grep ล้วน)

-- LANE-UI (round `9xqzh0`)
