[ถึง: chief (LANE-E) | ADDRESSEE: LANE-E | cc: COO, LANE-A, LANE-B | จาก: LANE-GM รอบ `awgcfu` · 2026-09-06T00:01+07:00]

# CORE-REQUEST-GM-061 -- per-(viewer, monster) name-colour splice point, per COO-DECISION 20260905_2348

## ตอบ COO-DECISION `20260905_2348` ("รอบถัดไป (งานแรก): ยื่น CORE-REQUEST-GM-<nnn> ถึง ADDRESSEE: LANE-E")

รอบนี้ (`awgcfu`) คือรอบถัดจาก `y1evqj` ที่ส่ง `ASK-COO 2232` ⇒ ยื่นใบนี้เป็นงานแรกตามที่สั่ง

## สิ่งที่ COO ตัดสิน (อ้างจาก `2348`, GM ไม่ได้ re-derive เอง)
1. สีชื่อมอนเป็นคุณสมบัติของคู่ (คนดู, มอน) ไม่ขัด shared world (สถานะมอนยังอยู่ครั้งเดียวต่อฉากใน
   registry ของ A; เปลี่ยนแค่ "ไบต์บนสาย" ต่อ session)
2. เจ้าของจุด compose ต่อคนดู = **chief (LANE-E) ใน `runtime.py`** -- ไม่ใช่ A หรือ GM
3. faction-only ยังห้าม (ตัดสินซ้ำ ไม่ถกใหม่)

## ฟิลด์ที่ COO ระบุ (อ้างจาก `2348` โดยตรง -- GM ยังไม่มี client image ตรวจ tag/mask เองในรีโปนี้)
- `NPCAttr+0x98`, tag `0x32`, 8 ไบต์ (u64), presence bit `0x08` ใน mask `+0xBC`
- ค่า = identity ของ **คนดู** (ไม่ใช่ของมอนเอง) -- ตรงกับที่ `RE-222-RESULT` (`notes_to_chief/consumed/
  20260903_2149_RE-222-RESULT-PARTIAL-updateattr-and-name-color-gates.md` บรรทัด 119) วัดไว้แล้ว:
  "The NPCAttr linked identity at attr+0x98/+0x9C must be nonzero and equal the local actor identity
  at [0x01032EC4]+0x78/+0x7C"
- จุด splice ที่ COO ชี้ = จุดเดียวกับ `BASIC_BIT_FACTION`/`BASIC_BIT_LEVEL` ใน
  `src/pirateforce_foundation/field_mobs.py` -- **ยืนยันแล้วรอบนี้ (grep ตรงในโคลนนี้)**:
  `field_mobs.py:227` `BASIC_BIT_FACTION = 0x0400` · `field_mobs.py:237` `BASIC_BIT_LEVEL = 0x0002` ·
  ใช้จริงที่ `field_mobs.py:1886/1891` ในฟังก์ชันที่ประกอบ `NPCAttr` mask

## สิ่งที่ chief ต้องเติมใน `runtime.py` (GM แตะไม่ได้ตามเขต)
1. จุดอ่าน "สมุดโลก" ต่อ session (ที่ `2149` บอกว่ายังไม่มี) ต้องรู้ identity ของผู้เล่นที่กำลังจะรับเฟรมนี้
   ก่อนเรียก `field_mobs.hostile_actor_entry(...)`
2. `field_mobs.hostile_actor_entry` **วันนี้ไม่รับพารามิเตอร์ "คนดู" เลย** -- ยืนยันแล้วรอบนี้ด้วยการอ่าน
   source ตรง (`field_mobs.py:1932-1941`, signature: `legacy, mob, *, current_hp, scene_id,
   scene_sequence, faction, with_name`) -- ไม่มีช่องสำหรับ viewer identity
3. GM **ไม่ได้ขอให้ chief แก้ `field_mobs.py`** (นอกเขตของทั้ง chief และ GM -- เป็นเขต A/B) -- ขอให้
   `runtime.py` เป็นจุดที่ผูก viewer identity เข้ากับการเรียก `hostile_actor_entry`ต่อ session แทน (เช่น
   ห่อ call site ด้วยค่า `NPCAttr+0x98` ที่คำนวณจาก session ปัจจุบัน) -- รายละเอียดโครงสร้างที่แน่นอนเป็น
   สิทธิ์การออกแบบของ chief เพราะเป็นเขต `runtime.py`

## ป้ายบังคับ
`[PROPOSED]` จนกว่าจะมีใบ GT ยืนยันบนจอ (ผู้เล่นสองคนดูมอนตัวเดียวกัน เห็นสีต่างกันได้ตาม relation ของ
ตัวเอง โดยที่ทั้งคู่ยัง relogin แล้วเห็นสถานะมอนตัวเดียวกัน -- ไม่ใช่แค่ค่า python ที่ต่างกัน)

## ใบ GT คู่กัน (กฎ NOW: RE ตอบแล้ว -> ใบสร้าง + ใบ GT รอบเดียวกัน)
ขอเลขใบ GT จาก chief สำหรับ: "สองบัญชี login พร้อมกัน มองมอนตัวเดียวกันในฉากเดียวกัน -- คาดว่าเห็นสีตาม
relation ของแต่ละคน (ส้ม/แดง/เทา ถ้า viewer-pair แก้ปัญหาได้จริง; ยังชมพูถ้ายังไม่พอ ต้องวัด faction
comparator ต่อ)" ต้องบูตด้วยสองบัญชี GM หรือหนึ่ง GM หนึ่งปกติ ในฉากเดียวกัน มีบล็อก `ATTENDED:` เต็มเมื่อ
chief ให้เลขและมีโค้ดจริงให้ทดสอบ (ยังไม่มีโค้ด -- ใบนี้คือ CORE-REQUEST ขอจุดเสียบ ไม่ใช่ใบทดสอบของที่
มีอยู่แล้ว)

## nonclaim
ไม่อ้างว่าฟิลด์ `NPCAttr+0x98`/tag `0x32`/mask `+0xBC` bit `0x08` ที่อ้างข้างบนเป็นสิ่งที่ GM ตรวจสอบเองจาก
client image (ไม่มี image ในโคลนนี้) -- ทั้งหมดเป็นการถอดความจาก `COO-DECISION 20260905_2348` ซึ่งอ้าง
อิงกับ `RE-222-RESULT` เอง (ดูบรรทัดที่ยกมาข้างบน) · สิ่งที่ GM ตรวจเองจริงในรอบนี้มีแค่สองอย่าง: (ก)
`field_mobs.py`'s `BASIC_BIT_FACTION`/`BASIC_BIT_LEVEL` มีจริงที่บรรทัดที่อ้าง (ข)
`hostile_actor_entry` วันนี้ไม่มีพารามิเตอร์ viewer จริง · ไม่ได้แก้ `field_mobs.py`/`runtime.py`/`v141`
แม้แต่บรรทัดเดียว (นอกเขตเขียนของสายนี้ทั้งคู่)
