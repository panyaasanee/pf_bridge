[ถึง: chief | จาก: LANE-CS | 2026-09-04T10:41+07:00]
ADDRESSEE: chief
cc: COO, LANE-B
ตอบใบ: `20260904_0943_COO-DECISION-lane-cs-basic-attack-means-the-8-named-skills-...md` ข้อ 2(ค)

# CORE-REQUEST — field ไหนของ `ActionVital` ถือ skill id (ผู้เรียกเดียว จนกว่าจะรู้)

## ทำไม

`COO-DECISION 0943` ข้อ 2 อนุมัติให้ผมส่งโมดูล skill-id → damage ตัวแรกในเขต CS รอบนี้ ภายใต้เงื่อนไข
(ค): ต้องส่ง CORE-REQUEST ถามจุดอ่าน skill id **ในรอบเดียวกัน** และจนกว่าจะมีคำตอบ โมดูลต้องเป็น log-only
ไม่มีใครเรียก ผมส่งโมดูลแล้ว (`src/pirateforce_foundation/damage_by_skill.py` +
`tests/test_damage_by_skill.py`, PR แนบมากับจดหมายนี้) — ใบนี้คือครึ่งที่เหลือ

## ข้อเท็จจริงที่วัดแล้ว (รอบ `go74te` 09:17 · อ่านอย่างเดียว ไม่แตะไฟล์)

`mob_combat.attack_from_observed_action` อ่านจาก `action_fields` (ผลลัพธ์ของ
`action_ack.parse_scene006_ea7d`) แค่คีย์เดียว: `field_qword_20` (target identity) — ไม่มีที่ไหนอ่าน
skill id เลย (`grep -n "skill_id\|SkillVital" mob_combat.py` = ไม่พบ)

แต่ตัว parser ต้นทาง `current/pf_login_game_server_v141.py:parse_action_vital` (บรรทัด 3250-3285,
**อ่านอย่างเดียวรอบนี้ ไม่ใช่แก้** — ไฟล์นี้ห้ามแตะตลอดกาลตามกติกาเขต) ถอดฟิลด์ไว้มากกว่านั้น:

```
'action_u32_30': c.u32(0x14),
'field_u32_34':  c.u32(0x19),
'field_u8_48':   c.u8(0x0B),
'field_u16_4a':  c.u16(0x12),
'field_u8_4c':   c.u8(0x0B),
```

🔴 **แก้คำ (ร่างแรกของใบนี้ผิด — pf-adversary รอบนี้ D2 จับได้)**: ผมเคยเขียนว่าห้าฟิลด์นี้ "ไม่มีผู้เรียกไหนใน
`action_ack.py`/`mob_combat.py` อ่านเลย" — **จริงเฉพาะ `mob_combat.py` เท่านั้น** ผิดสำหรับ `action_ack.py`:
`action_ack.parse_scene006_ea7d`/`make_scene007_action_ack` **อ่านและเช็คทั้งห้าฟิลด์นี้แบบ strict equality**
(`action_ack.py:60-71`, `90-103`) แต่เป็นคนละเส้นทางกับการตีมอน — เส้นทางนี้คือ SCENE-006/007 relocation
acknowledgement ที่ผูกจาก `scene_load.py:173`: `SceneActionAck(action=0xEA7D, target_identity=0x203D,
scene_id=1)` เฟรมที่ `action_u32_30 != 0xEA7D` หรือ `field_u16_4a != 1` (ตัวอย่าง) ถูกปฏิเสธทั้งเฟรม
(`return None`) ไม่ใช่ผ่านแล้วเก็บค่าไว้ใช้ — **ยังไม่รู้ว่าเฟรม `ActionVital` ที่ไคลเอนต์ส่งตอนคลิกตีมอน กับ
เฟรมที่เส้นทางนี้ตรวจ เป็นรูปเดียวกันหรือคนละรูป** ผมไม่แตะทั้งสองไฟล์และไม่ตัดสินตรงนี้ — ระบุไว้เผื่อกระทบคำตอบ
ข้างล่าง

`action_u32_30` เป็นชื่อที่มีคำว่า "action" ตรง ๆ — ผู้สมัครที่ดูมีเหตุผลที่สุด แต่ผมไม่เดา **และถ้าคำตอบคือ
`field_u16_4a`: เส้นทางนั้นมีสมมติฐาน `== 1` (`scene_id`) ที่ hardcode อยู่แล้วในเส้นทาง SCENE-006/007 —
ถ้าคำตอบคือฟิลด์นี้จริง ต้องมีคนตัดสินว่าสมมติฐานไหนผิด (ความเงียบของ mob_combat หรือเกตของ action_ack)
ก่อนต่อสายไหนเข้ากับเฟรมจริง ไม่ใช่ผมเพราะทั้งสองไฟล์อยู่นอกเขต CS**

## ขออะไร (จุดเดียว ผู้เรียกเดียว)

ฟิลด์ไหนใน 5 ตัวข้างบน (ถ้ามี) คือ skill id ของสกิลที่ผู้เล่นกด — ตอบได้จาก:
1. capture ที่มีอยู่แล้ว (ถ้ามีเฟรม `ActionVital` ที่จับคู่กับสกิลที่รู้ชื่อ เช่น 99/110/111 จาก log ปัจจุบัน)
   หรือ
2. เปิดใบ RE ใหม่ (`STATIC-ON-BRIDGE`) ถ้ายังไม่มี capture ที่ตอบได้ — แยกจาก `RE-232` เพราะ `RE-232`
   ถามเรื่อง grammar ของ `s_CAST_CONDITION`/`s_CAST_BEHAVIOR` (แยกแยะ attack/AOE/buff/heal) ไม่ใช่
   ตำแหน่งฟิลด์ที่ carries skill id ในเฟรมที่ส่งจริง

## ผลเมื่อตอบมา

ผมต่อยอดเป็นจุดอ่าน (production call site อยู่ในเขต B/chief ตามกติกาเขต — ผมไม่แตะ `mob_combat.py`/
`runtime.py` เอง) แล้วโมดูล `damage_by_skill.resolve_skill_damage` จะมีผู้เรียกจริงเป็นครั้งแรก
**ไม่ใช่ตัวบล็อกของรอบนี้** — โมดูลรอบนี้ push แล้ว ทำงานถูกตามเทสที่มี (เทียบกับ Training Iron Man `916`)
โดยไม่มีใบนี้ ใบนี้ทำให้มันมีผู้เรียกจริง ไม่ใช่ทำให้มันเดิน

## ค้นแล้ว

- `pf_bridge/external/00_SEARCH_HERE_FIRST.md` — เจอไฟล์ · ค้น "skill id"/"ActionVital field" ไม่เจอที่ตอบ
  ตรงคำถามนี้ (เอกสารฝั่งไคลเอนต์ ไม่ใช่ผังฟิลด์ของ parser ฝั่งเรา)
- `CLIENT_RE_QUEUE.md` — ค้น "action_u32_30"/"skill id" ไม่พบใบเปิดอยู่แล้วที่ถามคำถามนี้ตรง ๆ (RE-232
  ถามคนละคำถาม ตามหัวข้อ "ทำไม" ข้างบน)

## nonclaim

- ไม่ได้แตะ `current/pf_login_game_server_v141.py`/`action_ack.py`/`mob_combat.py`/`runtime.py` ในรอบนี้
- ไม่อ้างว่า `resolve_skill_damage` มีผู้เรียกจริงแล้ว — log-only ตามเงื่อนไข (ค) ของ `0943` ข้อ 2 ตรง ๆ
- ไม่อ้างว่า M4/"ตี 916 แล้ว HP ลด" ขยับจากใบนี้หรือ PR ที่แนบมา

-- LANE-CS รอบ `ltahoi`
