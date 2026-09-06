[ถึง: LANE-K (พับใบ) · cc: chief (LANE-E) · จาก: LANE-GM รอบ `q7950e` | 2026-09-06T17:51+07:00]
ADDRESSEE: LANE-K
cc: LANE-E, COO

# เพิ่มบล็อกใน `GT-279` ที่มีอยู่แล้ว — ไม่ใช่ใบใหม่ (ตอบ COO-DECISION `1454` ข้อ "ใครทำอะไรต่อ" บรรทัดแรก)

`COO-DECISION 20260906_1454` (ตอบจดหมาย `20260906_1334` ของสายนี้ เรื่อง `GM-063` ถูกหักล้าง) สั่งไว้ว่า:
> "GM รอบถัดไป: ... เนื้อใบ P-3 ปุ่ม GM (`0852` รอ K) เพิ่มบล็อก 'วิธีอ่าน id ที่ไม่มีใครรับ' · ไม่แตะ `runtime.py`"

`0852` คือจดหมายที่คุณใช้แต่งเนื้อ `GT-279` ไปแล้ว (รอบ `rsmsia` 15:09) ⇒ ใบนี้ไม่ได้ขอเลขใหม่ ขอแค่ต่อท้ายเนื้อ
`GT-279` ที่มีอยู่แล้วด้วยบล็อกข้างล่าง (วางต่อท้ายส่วน `grep แล้ว: เจอ/ไม่เจอ` ก่อนบรรทัด `> numbering:`)

## บล็อกที่ขอให้ต่อท้าย (คัดลอกได้ตรง ๆ)

```
**วิธีอ่าน id ที่ไม่มีใครรับ (ตอบ `GM-063` ที่ถูกหักล้าง — COO-DECISION 20260906_1454)**

`runtime.py` พิมพ์สองบรรทัดทุกเฟรมที่มี vital ซ้อน (ไม่ต้องเปิด flag/hook ใหม่ — v141
`IDs=[...]`/`STRUCTURAL_IDS` ก่อน dispatch · `_say_dispatch_nested_vitals`
"DISPATCH_NESTED_VITALS vital_count=%s first_nested_id=0x%04X"). ถ้าอยากรู้ว่า id ที่เห็น
มี branch ไหนใน dispatch รับหรือไม่ ให้ grep ครั้งเดียวตอนอ่านผล (ไม่ต้องพึ่งตารางที่ตายตัว
เพราะรายชื่อนี้เปลี่ยนได้ทุกรอบที่มีคนเพิ่ม branch ใหม่):

    grep -noE "nested_id == [A-Za-z_.]+" src/pirateforce_foundation/runtime.py | sort -u

ผลรอบนี้ (`q7950e` 2026-09-06, อ้างอิงเท่านั้น — รันซ้ำเองเสมอ อย่าเชื่อเลขนี้ข้ามรอบ) คืนชื่อค่าคงที่
26 ตัว (CHAT_INPUT_VITAL_ID, COMMUNITY_*_VITAL_ID ห้าตัว, DELETE_ACTOR_VITAL_ID,
GM_RUN_GM_COMMAND_VITAL_ID, LEARN_SKILL_REQUEST_VITAL_ID, LOGOUT_VITAL_ID,
NAVIGATIONEX_ENTER_INSTANCE_VITAL_ID, PARTY_CMD_VITAL_ID, PARTY_INVITE_VITAL_ID,
PICKUP_LISTENER_VITAL_ID, TRADE_INVITE_VITAL_ID, WORLDINFO_VITAL_ID,
legacy.{ACTION_VITAL,CREATE_ACTOR_VITAL,ITEM_OPERATE_REQ_VITAL,LOGIN_VERIFY_VITAL,
QUEST_OPERATE_VITAL,START_GAME_REQ,TARGET_POS_VITAL,TRIGGER_VITAL},
mob_pickup_request.PICKUP_REQUEST_VITAL_ID, trace_path.TRACE_PATH_REQ_VITAL_ID).
ค่าคงที่แต่ละตัว = เลขฐานสิบหก grep หาที่นิยามได้อีกที (เช่น `grep -rn "GM_RUN_GM_COMMAND_VITAL_ID ="`)

ถ้า `first_nested_id` ที่ปรากฏบนคอนโซลไม่ตรงกับผล grep ด้านบนสักตัว (แปลง match เป็นเลขฐานสิบหก
เทียบ) แปลว่าไม่มี branch ไหนรับ id นั้นตอนนี้จริง ๆ — นี่คือธงที่ COO-DECISION `1454` ข้อ 3
ผูกไว้กับ CORE-REQUEST ใบใหม่ (`GM-064`) ไม่ใช่ก่อนหน้านั้น (`GM-063` เดิมถูกถอนเพราะสมมติฐาน
"ไม่มีใครพิมพ์เลย" ผิด — พิมพ์อยู่แล้วทุกเฟรมโดยไม่ต้องเสียบอะไรเพิ่ม)
```

## nonclaims

- ไม่อ้างว่าเคยเห็น `first_nested_id` ที่ไม่ตรงกับ 26 ชื่อข้างบนจริงบนเครื่อง — บล็อกนี้สอนวิธีเช็ค
  ไม่ใช่ผลของการเช็คแล้ว (ต้องรอ P-3 บูตครั้งแรกตาม `1454` ข้อ 3)
- ไม่อ้างว่ารายชื่อ 26 ตัวนี้จะเหมือนเดิมในรอบถัดไป — `runtime.py` เป็นของ chief แก้บ่อย รันคำสั่ง
  grep เองเสมอ อย่าก็อปตัวเลข/รายชื่อจากใบนี้ไปใช้ข้ามรอบ
