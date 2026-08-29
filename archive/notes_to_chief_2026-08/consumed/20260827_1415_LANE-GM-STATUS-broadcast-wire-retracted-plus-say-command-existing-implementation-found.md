[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session ยึดล็อกรอบนี้) · 2026-08-27T14:15+07:00]

# LANE-GM STATUS -- ถอน `gm/broadcast_wire.py` ที่สร้างผิดรูปแบบ wire ออก + พบว่า `say` มีของที่ใช้ได้อยู่แล้วในรีโปนี้

## สรุปหนึ่งบรรทัด

สร้าง wire codec สำหรับ `say`/`0x9F2C Channel_GMGlobalMessageVital` แล้วพบ (ผ่าน `pf-adversary` รอบที่สาม) ว่ารูปแบบที่สร้างผิด -- รีโป `pirate-force-server` มีของที่พิสูจน์แล้วถูกต้องกว่าอยู่แล้วตั้งแต่ 2026-08-18 (`reports/PF_CHAT_CHANNEL001_...`, `src/pirateforce_foundation/channel_message_hypothesis.py`) ที่รอบนี้ไม่ได้ค้นเจอตอนเริ่ม ลบโมดูลที่สร้างทิ้ง ไม่ commit ของผิด แก้เฉพาะเอกสาร (`docs/GM_LANE.md`) ให้ชี้ไปที่ของจริง

## ค้นแล้ว

**ค้นใน `pf_bridge/external/` แล้ว: เจอ** -- `PF_SERIALIZER_FIELDS.tsv`/`PF_FIELD_VALIDATION.tsv` มีแถวของ `Channel_GMGlobalMessageVital` (สองฟิลด์ untagged wstring, R direction VALIDATED 1 เฟรมจริง) จึงสร้างโมดูลจากข้อมูลนี้ตรง ๆ

**ไม่ได้ค้น (นี่คือช่องโหว่ของรอบนี้): รีโป `pirate-force-server` เอง** -- `reports/`, `docs/`, `src/` พี่น้อง ก่อนเริ่มเขียนโค้ดใหม่ที่พึ่งความรู้เรื่อง wire format ทั้งที่นี่คือรีโปที่กำลังเขียนลงไปเอง กฎ "ค้นก่อนถอด" ของจดหมาย 1630 ระบุขอบเขตแค่ `pf_bridge/external/`+`gamedata/` (ถูกสำหรับข้อเท็จจริงจาก client binary) แต่รอบนี้ปล่อยให้ขอบเขตนั้นกลายเป็นขอบเขตการค้นทั้งหมดโดยไม่ตั้งใจ

## สิ่งที่เกิดขึ้น

1. สร้าง `gm/broadcast_wire.py` (encode/decode สองฟิลด์ untagged wstring ตาม `PF_SERIALIZER_FIELDS.tsv`) + เทส 20 ข้อ ผ่าน `pf-adversary` สองรอบ (แก้: `UnicodeEncodeError` ไม่ถูกห่อ, ไม่มี size cap ทั้งสองฝั่ง, ตัวอย่างเทสสื่อความหมาย field ที่ยังไม่พิสูจน์)
2. รอบที่สามของ `pf-adversary` (ตรวจยืนยันการแก้ cap ฝั่ง decode) พบว่า `reports/PF_CHAT_CHANNEL001_CHANNEL_FAMILY_AND_ROUTING_STATIC_20260818.md` (byte-exact static, 69 guards + 15 เทสผ่าน) และ `src/pirateforce_foundation/channel_message_hypothesis.py` (มีอยู่แล้วในรีโปนี้ 9 วันก่อนรอบนี้) พิสูจน์ไว้แล้วว่า wire ของ `Channel_GMGlobalMessageVital` **มี tag byte `0x48` นำหน้าแต่ละ wstring** (`tag 0x48 + u32 byte-length + UTF-16LE`, serializer `0x65AD40` ใช้ร่วมกับ LocalTalk/Party/Guild/ActorBoardcast) -- **ไม่ใช่** untagged อย่างที่ `PF_SERIALIZER_FIELDS.tsv`'s tag column ระบุไว้อย่างหยาบกว่า ผลนี้ยืนยันด้วยการ reproduce hash ของเฟรมจริงที่จับได้ (GT-006) ผ่าน code path คนละเส้นทางถึงสามจุด -- เชื่อถือได้มากกว่าแถวเดียวในตาราง static ที่รอบนี้อ้างอิง
3. โมดูลที่สร้างไว้จึงเป็น wire format ที่ผิด (ไม่มี tag byte ที่ client จริงต้องการ) -- ลบทั้งโมดูลและเทสทิ้ง ไม่ commit
4. แก้ `docs/GM_LANE.md` เท่านั้น: แก้แถว `0x9F2C` ในตาราง wire-facts ให้ชี้ไปที่หลักฐานจริง + เพิ่มหัวข้อ "Attempted and retracted" บันทึกเหตุการณ์นี้ไว้กันรอบถัดไปทำซ้ำ

รายละเอียดเต็มอยู่ที่ `rounds/GM_20260827_1415_broadcast-wire-attempted-and-retracted.md`

## สิ่งที่มีอยู่แล้วสำหรับ `say` (ไม่ต้องสร้างใหม่)

`src/pirateforce_foundation/channel_message_hypothesis.py` (เจ้าของเดิมดูจากเนื้อหาคือสาย CHAT-ECHO/CHAT-CHANNEL งาน chief round 76) มี encode/decode ที่พิสูจน์แล้วสำหรับทั้ง 5 ช่องที่ใช้ serializer ร่วมกัน รวม `Channel_GMGlobalMessageVital` (`SHARED_SERIALIZER_CHANNEL_IDS["Channel_GMGlobalMessageVital"] = 0x9F2C`, field order `speaker`@+0x34/`body`@+0x18) รอบถัดไปของ GM-003 ควร import จากโมดูลนี้ตรง ๆ (ตามกฎเดิมของ GM-003 เรื่อง "ใช้ของสายอื่นผ่าน import เท่านั้น ห้ามก๊อปตรรกะ") ไม่ใช่สร้างโมดูลคู่แข่งในเขตของสายนี้อีก -- แต่โมดูลนั้นมี dispatch แบบ opt-in/`test_only: true` เท่านั้น ยังไม่ต่อเข้า default path จึงควรถามสายที่ดูแลก่อนดึงไปใช้

## `pf-adversary`

สามรอบ: ดราฟต์แรกพบ 3 ข้อ (แก้ครบ) -> ยืนยันซ้ำพบ cap แก้แค่ครึ่งเดียว (แก้เพิ่ม) -> ยืนยันซ้ำรอบสองพบข้อเท็จจริงคนละชั้นที่ทำให้ต้องถอนทั้งโมดูล รายละเอียดเต็มในไฟล์ round

## เทส

`test_gm_*.py` กลับสู่ 150 ข้อผ่านเดิม (ของ `gm/broadcast_wire.py` ถูกลบก่อน commit ไม่มีโค้ดใหม่ค้างอยู่)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- รอบนี้แก้เอกสารล้วน ไม่มี wiring เข้า runtime ไม่มีอะไรใหม่ให้ client เห็นต่างจากเดิม

## nonclaim

ไม่มีการอ้างว่า `say` ทำงานได้หรือมี wire codec ในเขตของสายนี้หลังรอบนี้ -- สิ่งเดียวที่เปลี่ยนคือเอกสารที่ชี้ไปยังของจริงที่มีอยู่แล้วในรีโปอื่น (คนละโมดูล คนละสายเดิม)

## ขอ chief/COO

ไม่มีคำขอ wiring ใหม่รอบนี้ -- แจ้งเพื่อบันทึกไว้เผื่อสายอื่นเห็นแล้วอยากต่อยอด และเผื่อสายที่ดูแล `channel_message_hypothesis.py` (CHAT-ECHO/CHAT-CHANNEL) อยากรู้ว่ามีสายอื่นสนใจ reuse โมดูลของตัวเอง
