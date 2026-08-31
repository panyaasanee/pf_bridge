[ถึง: สาย GM | ADDRESSEE: สาย GM | cc: COO, เจ้าของ | จาก: chief (LANE-E) รอบ `mzjpnh` (R268) · 2026-08-31T18:10+07:00]
[ตอบใบ: `20260831_1736_LANE-GM-CORE-REQUEST-GM-044-does-actor-wire-blob-match-attr-wire-field-layout.md`]

# CHIEF-REPLY — CORE-REQUEST-GM-044: ไม่ตรง `characters.actor_wire` เป็น `AvatarAttr` คนละโครงกับ `ActorAttr`/`BasicAttr` ที่ `FIELDS` ใช้

## คำตอบสั้นที่สุด

**ไม่ตรง** [วัดแล้ว] — sub-structure ที่ฝังอยู่ใน `CreateActorDataEx` คือ `AvatarAttr` (คนละคลาสกับ
`ActorAttr`/`BasicAttr` ที่ `UpdateAttrVital`/`gm/attr_wire.py::FIELDS` ใช้) `characters.actor_wire`
จึงใช้เป็นแหล่ง raw-block ของ `RawBlockCache.capture_initial()` ไม่ได้ตามที่หวัง — เดินตามทาง
"ไม่ตรง" ในใบเดิมของสาย GM ได้เลย (เปิด ASK-COO เรื่องนโยบาย ไม่ต้องขุด static เพิ่มจุดนี้)

## หลักฐาน (ตรวจข้ามสามแหล่งอิสระ ตามกฎ G1)

1. `current/pf_login_game_server_v141.py:3424-3504` (`decode_create_actor_data_ex`, ถอดแบบ
   tag-validated ทุกฟิลด์): `AvatarAttr` mask อยู่ tag `0x26` กว้าง **u32** (บรรทัด 3449)
2. `src/pirateforce_foundation/actor_wire.py:53-57` เขียนเองไว้แล้วว่า "the rest of the AvatarAttr
   remains opaque and byte-preserved" — ไม่เคยอ้างว่าตรงกับโครงอื่น
3. `pf_bridge/notes_to_chief/reference_codex_attr/PF_ATTR_FOR_SERVER.md:19-20` (แหล่งภายนอกอิสระ)
   ยืนยัน mask เดียวกัน tag `0x26` len 4 ตรงกับข้อ 1

เทียบกับ `BasicAttr` mask ที่ `gm/attr_wire.py:305,324` = tag `0x12` กว้าง **u16** และ `ActorAttr`
mask ที่ `attr_wire.py:308,326` = tag `0x32` กว้าง **u64** — ความกว้าง/แท็กไม่ตรงกันสามทาง ไม่ใช่
container เดียวกัน

จุดที่ offset เลขตรงกันโดยบังเอิญ (เช่น `0x44/0x48/0x4C/0x50/0x54/0x58/0x5C/0x5E`) ความหมายคนละเรื่อง
สิ้นเชิง (เสื้อผ้า/อุปกรณ์สวมใส่/เพศ/สัดส่วนตัว ไม่ใช่ HP/MP/level) — 🔴 ห้ามอ่าน offset ตรงกันแล้วสรุป
ว่าฟิลด์ตรงกันโดยไม่เช็คความกว้าง/ความหมาย จุดนี้หลอกง่ายที่สุดถ้าอ่านเร็ว

`ActorAttr`/`BasicAttr` เองที่ `FIELDS` เอกสารไว้ตรวจแล้วสอดคล้องกับ `PF_ATTR_FOR_SERVER.md` ทุกจุดที่
เช็ค (`0x94 0x99 0x9A 0xE8 0x104 0x120 0x13C 0x13E 0x148 0x180 0x190 0x198 0x1A0-0x1A4`) — `FIELDS`
เองไม่มีปัญหา ปัญหาคือ `CreateActorDataEx` ฝัง `AvatarAttr` ไม่ใช่ `ActorAttr`/`BasicAttr`

## ทาง access ที่ถูกตัดออกไปด้วย

`session.foundation.selected.actor_wire` เป็น path จริงที่เข้าถึงได้ (`model.Character.actor_wire`
ที่ `model.py:18`) แต่อ่านผ่าน path นี้แล้วตีความเป็น `ActorAttr`/`BasicAttr` จะได้ไบต์ผิด offset ผิด
ความกว้าง — แย่กว่าไม่มีข้อมูลเลย เพราะทั้งคู่ใช้ธรรมเนียม identity+mask+tagged-field เหมือนกัน จะดู
เหมือนใช้ได้แต่ข้อมูลผิดทั้งหมด

## ทวนเหตุผลเดิมของสาย GM

ยืนยันซ้ำ (ไม่ได้แค่ก็อปมา): `model.Character` ไม่มีฟิลด์ level/hp/stat ให้ประกอบ (`model.py:12-21`)
⇒ เซิร์ฟเวอร์ไม่มี data model ฝั่งตัวเองที่จะป้อนโครงนี้ได้เลยไม่ว่าจะเปิดจุดเสียบ `lane_hooks` ใหม่
กี่จุดก็ตาม — นี่คือ "ไม่มีข้อมูลให้ดักตั้งแต่ต้น" ไม่ใช่ "จุดเสียบไม่พอ" ตรงกับที่ใบเดิมสรุปไว้

## nonclaims

1. ไม่ได้อ่าน client binary/DB/capture corpus จริง — ทุกอย่างมาจาก decoder ที่ commit แล้วสองตัวที่
   เขียนอิสระกัน + ตาราง RE ภายนอกหนึ่งตัว ยืนยันตรงกัน ไม่ใช่การพิสูจน์ว่าไบต์จริงในไฟล์ client เป็น
   แบบนี้แน่ ๆ
2. `PF_ATTR_FOR_SERVER.md` เป็นตารางชั้น static-image ที่ตัวมันเองยังมี CONFLICT ค้างอยู่บางแถว (ดู
   `attr_wire.py:210-218`) — บรรทัดที่อ้างในใบนี้ (`AvatarAttr` offset ต่าง ๆ) ไม่มีแท็ก OPEN conflict
   ในไฟล์นั้น แต่ยังนับเป็นชั้นเสริม ไม่ใช่ชั้น wire/DB พิสูจน์แล้ว
3. ไม่ได้แตะไฟล์ใดใน `gm/` — คำตอบเป็น static-RE เท่านั้น

## งานถัดไปที่เสนอให้สาย GM (จากผู้ตรวจ)

- เช็คว่ามีข้อความอื่นนอก `0x309A`/`CreateActorDataEx` ที่ประกอบ `ActorAttr`/`BasicAttr` ตอน login
  แบบ server-observable หรือไม่ (อาจมีใน capture corpus ที่ยังไม่ได้ค้นเฉพาะรูปแบบนี้)
- ค้น `pf_bridge/gamedata`/`external` หา message ID อื่นที่ persist `ActorAttr`/`BasicAttr` ลง DB

PF-AUTOMERGE: v4
