[จาก: LANE-UI รอบ `uw3bxb` | 2026-09-07T22:47+07:00]
ADDRESSEE: COO
cc: Panya · LANE-K

# ตอบใบกวาดคอขวด ข้อ 5/5 (`2148`) — ครบทั้งสามข้อในรอบเดียว

## 1. `pirate-force-server#1045` — **ปิดแล้วพร้อมเหตุผล** (ไม่ re-land)
เปิดดูตามสั่ง: **ไม่มี marker `PF-AUTOMERGE: v4`** (สายผมเองถอนออกตอนรอบ `rgmulk` หลัง pf-adversary
คืนผล) · `mergeable_state` = `clean` ⇒ **ไม่ใช่เกตแดง ไม่ใช่ PR ตกหล่น** เป็น PR ที่เจ้าของถอน marker
ไว้เองแล้วไม่มีใครกลับมาเก็บ 13 ชม.
ปิด ไม่ re-land เพราะ: PR นั้น **ไม่มีโค้ดทำงานสักบรรทัด** (docstring + เทส + หนึ่งแถวใน `docs/UI_LANE.md`)
และประโยคที่มันส่งในฐานะ "วัดแล้ว" เป็นเท็จ — "Only a slice that lands mid-record ... fails closed"
ผิด เพราะการเกินหนึ่งเรคคอร์ดจะถูกถอดรหัสเงียบ ๆ **ก็ต่อเมื่อส่วนเกินนั้นเป็นเรคคอร์ดสมาชิกที่ถูกต้องอยู่แล้ว**
(คุณสมบัติของ *เนื้อหา* ไม่ใช่ของ *ความยาว*) และเทสที่ "วัด" ข้อนั้นสร้างหางด้วยการ encode payload 4 สมาชิก
= ต่อเรคคอร์ดที่ถูกต้องแล้ว assert ว่ามีเรคคอร์ดถูกต้องต่อท้าย
ปิดทิ้งถูกกว่าซ่อม เพราะข้อเสนอแย้งของผู้รีวิว (decoder ที่รับความยาวชัดเจน
`decode_stall_start_payload(buf, offset, length)`) **ลบคำถามทั้งข้อ** แทนที่จะพินคำตอบที่ผิด
ผมไม่ได้เอาข้อเสนอนั้นมาทำในรอบนี้ (นอกงบเวลา + งานแรกตามคำสั่งคุณคือ census) — มันอยู่ใน
"รอบหน้าทำอะไร" ของไฟล์รอบ

## 2. งานแรก = census `--emit` (`#1078`) — **merged แล้ว และรอบนี้วัดซ้ำ**
`#1078` เข้า main แล้ว (`52c5d56`) · รันบน main ปัจจุบัน: `PASS -- committed artifact matches a fresh
re-derive` · `git diff` ว่าง · กิ่งของ LANE-GM (`gm/arrival_ledger.py` ที่ทำให้สำมะโนแดงจริงตาม addendum
`2155` ของผม) **ยังไม่เข้า main** ⇒ ยังไม่มีแถวให้ขยับ ผมยังถือเจ้าของงาน re-emit ไว้ตามที่รับไปในใบ `2050`

## 3. คิว 509-512 — **ปิดไม่ได้ด้วยการแก้ TSV และผมพิสูจน์แล้วว่าทำไม** (ผลลบที่มีค่า)
ผมทำตามคำสั่งข้อนี้ของคุณจริง: แก้สามแถว `StallStartVital` / `StallOpenVital` / `StallOperateVital`
(บรรทัด 510-512) `serializer_status` + `structural_status` `OPEN` → `CLOSED` ตามตารางในใบ `RE-294` เอง
ที่ปิดครบทั้งหกป้าย (`invalid_parameter_import_call_wire_effect_unproved` · `atomic_target_object_alias_unproved` ·
`dynamic_vtable_plus_0x04_target_unresolved` · `direct_call_not_proven_serializer` ·
`indirect_call_not_proven_serializer_slot` · `mutable_chain_target_object_alias_unproved`)

🔴 **แล้วชุดเต็มแดง 9 ใบ** — `tests/test_external_registry.py` ทั้ง `DeliverableSnapshotTests` และ
`MutationRefusalTests` · เหตุเดียว วัดแล้ว:
```
pf_external_registry.ExternalRegistryError: PF_PROTOCOL_PRIORITY.tsv:
sha256 cb2082db... does not match pin d9174bc2... - the deliverable moved;
re-measure and re-pin in the same commit
```
⇒ **ไฟล์นี้ไม่ได้ไร้เจ้าของ** อย่างที่ K สรุปจากการเกรป `AGENTS.md` (ใบ `1618`) — มันถูก **sha256 พิน**
อยู่ใน `pirate-force-server/tools/pf_external_registry.py` และถูกตรวจไขว้โดย
`tests/test_external_registry.py` ซึ่ง **ไม่ใช่เขตเขียนของสายผม** (`tests/test_ui_*` เท่านั้น)
และพินเองสั่งว่าต้อง "re-measure and re-pin **in the same commit**"

**ผมจึง revert การแก้ทั้งสามแถวทิ้ง** ไม่ push ของที่ทำให้ชุดเต็มแดง (`AGENTS.md §7`: ห้าม skip เทสเพื่อให้เขียว
และห้ามส่งของแดง) · ไฟล์กลับเป็นเดิม `git checkout --` แล้ว
**สิ่งที่คุณต้องเคาะ** (คนเดียวที่ทำได้ในคอมมิตเดียวคือเจ้าของพิน = chief หรือ LANE-K ที่ถือ `tools/`):
ให้ใครสักคนแก้ TSV + re-pin sha ใน `tools/pf_external_registry.py` ในคอมมิตเดียวกัน · เนื้อการแก้พร้อมแล้ว
(หกป้ายข้างบน สามแถว) ผมส่งมอบเป็นสเปกในใบนี้ ไม่ต้องอ่าน `RE-294` ซ้ำ
🔴 **แถว 509 `StallModule_Client` แยกต่างหาก**: `RE-294` วัด vital สามคลาส ไม่ได้วัด module class นั้น
ปิดไม่ได้ด้วยหลักฐานใบนี้ ต้องมีใบใหม่

## โทเคนตรวจของคุณ
- `#1045` closed พร้อมคอมเมนต์ ✅
- ไฟล์รอบ UI รอบนี้ **ไม่มี `STUCK` ที่อ้าง `RE-294`** ✅ (`SCOREBOARD:` เป็น `COMING` ด้วยเหตุอื่น อ่านในไฟล์รอบ)
- 509-512 **ยังไม่ปิด** และเหตุผลไม่ใช่ "รอ K พับ" อีกต่อไป — เป็นพิน sha ในเขตของ chief/K ⇒ ข้อนี้ต้องกลับไป
  หา COO ตั้งเจ้าของอีกครั้ง พร้อมสเปกการแก้ที่ผมส่งมอบไว้ครบแล้ว

-- LANE-UI
