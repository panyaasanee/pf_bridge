# GM round 2026-08-27 ~13:3x-14:1x (+07:00) -- `say`/`Channel_GMGlobalMessageVital` wire codec attempted, found wrong, retracted

ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#175`, `pirate-force-server#101`) -- ตรวจ GitHub API ก่อนยึดล็อก: ไม่มี PR เปิดค้างเลยสักใบในทั้งสอง repo ตอนตรวจ (`list_pull_requests` state=open คืนค่าว่างทั้งคู่)

## ตรวจสถานะก่อนเริ่มงานจริง

ยืนยัน `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ขั้นแรกบังคับของทุกรอบ) · อ่านจดหมาย order 1630 ซ้ำ · อ่านรอบก่อนหน้าทั้งสองใบเต็มฉบับ (`20260827_0724` CORE-REQUEST-011, `20260827_0725` CORE-REQUEST-010) รวมถึง `docs/GM_LANE.md` เต็มไฟล์: ทั้ง CORE-REQUEST-010/011 ยังไม่ถูก chief ต่อสายเข้า `runtime.py` (grep `handle_gm_run_command_vital`/`make_warp_force_pos_frame` = ศูนย์ผลลัพธ์ในทั้ง `runtime.py`/`app.py`) และไม่มี CHIEF-REPLY หรือ RE ใหม่เจาะจงสายนี้เข้ามาตั้งแต่รอบก่อน (อ่านรายการจดหมายทั้งหมดตั้งแต่ `0438` ถึงปัจจุบัน)

## ตัดสินใจเลือกงานของรอบนี้

เนื่องจาก CORE-REQUEST-010/011 ยังไม่ถูกต่อสายและไม่มี RE ใหม่ รอบนี้เลือกสร้างสิ่งที่ยังไม่ถูกทำ: wire codec สำหรับ `say <ข้อความ>` (GM-003) ซึ่งตามจดหมาย 1630 ใช้ `0x9F2C Channel_GMGlobalMessageVital` -- ยังไม่มีใครในสายนี้แตะมาก่อน (`docs/GM_LANE.md` แถวเดิมเขียนว่า "field layout not yet pinned by this lane")

## สิ่งที่สร้าง แล้วถอนออก (ไม่ commit)

**ค้นแล้ว: เจอ (แต่ไม่พอ)** -- ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`gamedata/00_SEARCH_HERE_FIRST.md` ตามกฎ "ค้นก่อนถอด" แล้วเจอ `external/PF_SERIALIZER_FIELDS.tsv`/`PF_FIELD_VALIDATION.tsv` มีแถวของ `Channel_GMGlobalMessageVital` (สองฟิลด์ `UNTAGGED_WSTRING16LE_LEN32LE` ที่ +0x34/+0x18, R direction VALIDATED 1 เฟรมจริง) จึงสร้าง `gm/broadcast_wire.py` + `tests/test_gm_broadcast_wire.py` ตาม pattern เดียวกับ `gm/teleport_wire.py` ผ่าน `pf-adversary` สองรอบแรก (พบและแก้: `UnicodeEncodeError` ไม่ถูกห่อเป็น error ของโมดูล, ไม่มี size cap ทั้งฝั่ง encode/decode, ตัวอย่างในเทสสื่อความหมาย field ที่ยังไม่พิสูจน์) เทสผ่านครบ 20 ข้อ, สวีต `test_gm_*.py` 170 ข้อผ่านหมด

**รอบที่สามของ `pf-adversary` (ตรวจยืนยันการแก้ decode-cap) พบสิ่งที่ทำให้ต้องถอนทั้งโมดูล**: `reports/PF_CHAT_CHANNEL001_CHANNEL_FAMILY_AND_ROUTING_STATIC_20260818.md` (byte-exact static, 69 guards + 15 เทสผ่าน) และ `src/pirateforce_foundation/channel_message_hypothesis.py` ที่มีอยู่แล้วในรีโปนี้ตั้งแต่ 2026-08-18 (ก่อนรอบนี้ 9 วัน) พิสูจน์ไว้แล้วว่า `Channel_GMGlobalMessageVital` ใช้ serializer `0x65AD40` ร่วมกับอีก 4 ช่อง (LocalTalk/Party/Guild/ActorBoardcast) แบบ **มี tag byte `0x48` นำหน้าแต่ละ wstring** (`tag 0x48 + u32 byte-length + UTF-16LE`) -- **ไม่ใช่** untagged อย่างที่ `PF_SERIALIZER_FIELDS.tsv`'s "tag" คอลัมน์ระบุ (`UNTAGGED_WSTRING16LE_LEN32LE`) ผลของ CHAT-CHANNEL-001 ยืนยันซ้ำด้วยการ reproduce hash ของเฟรมจริงที่จับได้ (GT-006) ผ่าน code path คนละเส้นทางถึงสามจุด -- เชื่อถือได้มากกว่าแถวเดียวในตาราง static

โมดูล `gm/broadcast_wire.py` ที่สร้างไว้จึงเป็น **wire format ที่ผิด** (ไม่มี tag byte ที่ client จริงต้องการ) -- ถ้าถูกส่งจริงจะเป็นไบต์ที่ client ไม่ยอมรับ **ลบทั้งโมดูลและเทสทิ้ง ไม่ commit**

## แก้เอกสาร (สิ่งเดียวที่ push จริงรอบนี้)

- `docs/GM_LANE.md`: แก้แถว `0x9F2C` ในตาราง wire-facts ให้ชี้ไปที่หลักฐานจริง (`reports/PF_CHAT_CHANNEL001_...`, `channel_message_hypothesis.py`) แทนคำกล่าวอ้างเดิมที่ล้าสมัย ("field layout not yet pinned by this lane") และเพิ่มหัวข้อ "Attempted and retracted (broadcast-wire round)" บันทึกว่าเกิดอะไรขึ้น เพื่อไม่ให้รอบถัดไป (ของสายนี้หรือสายอื่น) ถอดรหัสข้อความนี้ซ้ำผิดอีก

## ต้นเหตุที่แท้จริง (บทเรียน ไม่ใช่ข้อแก้ตัว)

กฎ "ค้นก่อนถอด" ของสายนี้ (จดหมาย 1630) ระบุให้ค้นเฉพาะ `pf_bridge/external/` และ `pf_bridge/gamedata/` ก่อนถอดรหัสอะไรที่พึ่งข้อมูล client -- รอบนี้ทำตามนั้นตรง ๆ แต่ไม่ได้ค้น **รีโป `pirate-force-server` เองก่อน** (`reports/`, `docs/`, `src/` พี่น้อง) ทั้งที่นี่คือรีโปที่กำลังเขียนโค้ดลงไป กฎเดิมถูกสำหรับข้อเท็จจริงจาก client binary แต่ถูกตีความ (ผิด) ว่าเป็นขอบเขตการค้นทั้งหมด ทั้งที่คำตอบที่ถูกต้องกว่าซ่อนอยู่ในรีโปเดียวกันมา 9 วันแล้ว รอบถัดไปควรขยายกฎนี้ให้รวมการค้น `reports/`/`docs/`/`src/` ของ `pirate-force-server` เองด้วยก่อนเขียนโมดูลใหม่ที่พึ่งข้อมูล wire

## `pf-adversary`

สามรอบตามลำดับ:
1. ดราฟต์แรกของ `gm/broadcast_wire.py`: พบ 3 ข้อ (MEDIUM: `UnicodeEncodeError` ไม่ถูกห่อ, LOW/MEDIUM: ไม่มี size cap, LOW: ตัวอย่างเทสสื่อความหมาย field ที่ยังไม่พิสูจน์) -- แก้ครบ
2. ยืนยันซ้ำหลังแก้: (1)/(3) ปิดจริง, (2) แก้ครึ่งเดียว (cap มีแค่ฝั่ง encode ไม่มีฝั่ง decode) -- แก้เพิ่ม
3. ยืนยันซ้ำรอบสอง: cap ทั้งสองฝั่งปิดจริง ไม่มีช่องโหว่ใหม่ **แต่พบข้อเท็จจริงคนละชั้น**: docstring ที่อ้างว่า `Channel_GMGlobalMessageVital` เป็น "distinct class with its own serializer" ขัดกับหลักฐานที่มีอยู่แล้วในรีโปนี้เอง (ดูหัวข้อด้านบน) -- ผลคือถอนทั้งโมดูลแทนที่จะแก้แค่ประโยคนั้น เพราะ wire format ที่ใช้จริงผิดทั้งหมด ไม่ใช่แค่คำอธิบาย

## เทส

`docs/GM_LANE.md` เป็นการแก้เอกสารล้วน ไม่มีโค้ดใหม่ค้างในรอบนี้ -- `test_gm_*.py` กลับสู่ 150 ข้อผ่านเดิม (ของ `gm/broadcast_wire.py` ถูกลบพร้อมเทสของมันก่อน commit)

## push

`pirate-force-server@1686bf3` บน `claude/youthful-johnson-aue00g` (PR #101)

## จดหมาย

`notes_to_chief/20260827_1415_LANE-GM-STATUS-broadcast-wire-retracted-plus-say-command-existing-implementation-found.md`

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้เป็นการแก้เอกสารและถอนโค้ดที่ผิดออก ไม่มีอะไรใหม่ให้ client เห็นต่างจากเดิม ไม่มีการ execute หรือส่ง frame ใด ๆ

## nonclaim

ไม่มีการอ้างว่า `say` ทำงานได้ -- รอบนี้ไม่มีโค้ดใหม่เข้าสู่ `pirate-force-server` เลย มีแต่การแก้เอกสารและการลบโค้ดที่พิสูจน์แล้วว่าผิด

## ค้าง (ตั้งใจ ไม่บล็อก)

- CORE-REQUEST-010/011 รอ chief ต่อสายจริง -- ค้างจากหลายรอบก่อน ไม่ใช่ของใหม่รอบนี้
- `say` ยังไม่มี wire codec ในเขตเขียนของสายนี้ -- แต่ตอนนี้รู้แล้วว่าไม่ต้องสร้างใหม่: รอบถัดไปควร import จาก `channel_message_hypothesis.py` โดยตรง (ตามกฎ GM-003 เดิมเรื่องใช้ของสายอื่นผ่าน import เท่านั้น) และประสานกับสายที่ดูแลโมดูลนั้นก่อน เพราะ dispatch ของมันยังเป็น opt-in/`test_only: true` ไม่ใช่ default
- การ decode สองฟิลด์ wide-string ของ `GM_RunGMCommandVital` เป็นชื่อคำสั่ง/argument จริง ยังต้องรอ RE หรือ attended capture matrix -- ค้างจากหลายรอบก่อน ไม่ใช่ของใหม่
- `TeleportTarget` field-order ยังไม่เทียบกับ 132 candidate frame ที่ `A2_STATIC_OPEN` -- ค้างจากหลายรอบก่อน ไม่ใช่ของใหม่
