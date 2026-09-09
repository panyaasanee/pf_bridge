งานเป้าหมายยืน A1 — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B; cc LANE-K, COO, chief
FROM: Codex RE/static · 2026-09-09T15:13:37+07:00
RESULT: DONE — A1 red-bit reset receiver and exact predicates closed

## คำตอบเพิ่มของ A1

[MEASURED][IMAGE][PROVEN_EXACT] จุด `0x00444241` และ `0x00444252` **ไม่ได้เรียก vslot `+0x3C/+0x40` บนมอนใน ESI**. ทั้งสองครั้งโหลด `ECX=[0x01032EC4]`; singleton นี้ถูก publish จาก constructor ของ `CMyActor` ตัวเดียวกับที่ติดตั้ง vtable `0x00F0D7A8`. ดังนั้น slot ที่ใช้จริงคือ `0x00454A70` และ `0x00454AC0` ของ **local player**, ไม่ใช่ `0x0043BD70/0x0043BDA0` ของ CNetNPC.

[MEASURED][IMAGE][PROVEN_EXACT] ภายใน tail ที่ A1 ปิดไว้แล้ว (`n_OFFESIVE=0`, `CNetNPC+0x70 & 0x100` ตั้ง):

- local-player vslot `+0x3C` คืน true เมื่อ `ActorAttr+0x58` เป็น float ที่ ordered และ `<=0`, `CMyActor+0x348` ไม่เป็น null และ current-value field ที่เลือกเป็นศูนย์
- local-player vslot `+0x40` คืน true เมื่อ field เดิมเป็น float ที่ ordered และ `>0` พร้อม gate และ current-value zero เดียวกัน
- `CMyActor+0x358==0` เลือก `ActorAttr+0x44`; ถ้าไม่เป็นศูนย์เลือก `ActorAttr+0x1A8`. นี่คือคู่ current-value ที่ผล A4 `20260909_0022` พิสูจน์แยกไว้แล้ว
- เพราะ predicate สองตัวแบ่งช่วง `<=0` กับ `>0`, union ของมันครอบคลุมค่า timer แบบ ordered ทุกค่า. เมื่อ current-value ที่ถูกเลือกเป็นศูนย์ selector ไป `0x00444267`, ล้าง `CNetNPC+0x70 bit 0x100` และไม่ส่ง style ใหม่ใน invocation นั้น
- ถ้า current-value ไม่เป็นศูนย์, `ActorAttr` ขาด, หรือ timer เป็น NaN ทั้งสอง predicate false และ tail ยังเลือก style 61. เมื่อบิตว่าง tail เลือก style 62 โดยไม่เรียกสอง predicate นี้

[MEASURED][IMAGE][PROVEN_EXACT] ผลเชิงออกแบบที่แคบ: **ไม่พบ timeout/disengage reset ใน tail นี้**. reset ที่พิสูจน์ได้ผูกกับ current-value zero ของ local player; การตีมอนแล้วหยุดตีขณะผู้เล่นยังมีค่า current มากกว่าศูนย์ไม่เข้า clear branch นี้จากหลักฐานที่ตรวจ.

นี่ทำให้ถ้อยคำ “local vslot” ในผล A1 เดิมชัดเจนขึ้น. ถ้าถูกอ่านว่าเป็น slot ของ CNetNPC จะเป็นการผูก receiver ผิดคลาส. ผลเดิมเรื่อง hit ตั้งบิตบน target actor และ updater เรียก selector บนมอนตัวเดิมยังคงเดิม.

## หลักฐานจากอิมเมจ

อิมเมจ `GameClient.local.bin` ขนาด 14,759,424 ไบต์ SHA-256 ก่อน/หลัง:
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

ทุกช่วงเป็น `[start,end)`:

| หลักฐาน | VA | File offset | SHA-256 |
|---|---|---|---|
| selector bit/receiver/reset | 00444238–0044426F | 00043638–0004366F | 49970f4caad61334da19883a5ced6d80e50e00954d197c0bee138e33ba2d324b |
| CMyActor vslot +0x3C predicate | 00454A70–00454AB5 | 00053E70–00053EB5 | 2bd6b2b22189b8e8f5284cfa2aad2febeb5acd8f96ec8810cb409a8eab481cac |
| CMyActor vslot +0x40 predicate | 00454AC0–00454B0A | 00053EC0–00053F0A | f8b07b3c88a3ba2b155ef136d746f4c30cde8f79d2ab747fc516eaeb7428b3e7 |
| CMyActor vtable incl. +0x3C/+0x40/+0x74 | 00F0D7A8–00F0D828 | 00B0BBA8–00B0BC28 | c92508ad7f2b0eb8f98d2f8960f85a9ba8f79eac289e77c2a75f61cf9b664c59 |
| constructor this/vtable/singleton publish | 0044C9B5–0044CB83 | 0004BDB5–0004BF83 | 884734793e33b40918a45de400ecfbfaf3b91a7ad2b332dc4734b690454e6da2 |
| float32 zero constant | 00F0989C–00F098A0 | 00B07C9C–00B07CA0 | df3f619804a92fdb4057192dc43dd748ea778adc52bc498ce80524c014b81119 |

Exact vtable bindings: `0x00F0D7E4 -> 0x00454A70`, `0x00F0D7E8 -> 0x00454AC0`, `0x00F0D81C -> 0x0044C630`; getter `0x0044C630` returns `[CMyActor+0x348]`. Constructor pins are `0x0044C9B5 ESI=ECX`, `0x0044C9C5 [ESI]=0x00F0D7A8`, and `0x0044CB7D [0x01032EC4]=ESI`.

Field keys in this exact consumer: `CNetNPC@0x70.4#W:b0x100` (local reset store), `CMyActor@0x358.1#R`, `ActorAttr@0x58.4#R`, `ActorAttr@0x44.4#R`, `ActorAttr@0x1A8.4#R`. ไม่มี field เหล่านี้ถูกประกาศเป็น direct FontStyleID wire field.

## การตรวจซ้ำ

Verifier stdlib-only: `pf_bridge/staged/standing_a1_reset_verify.py` SHA-256 `00d629c6f3de8580915a66f4f47e4e607e90520ed8f6a166c146270bcee386fc`.

Log: `pf_bridge/staged/standing_a1_reset_verify.log` SHA-256 `2e6ba095e6ef85b46f17bd66c3762b9f267a153148e222cc8c59d683502e0a50`.

ผล: `PASS spans=6 span_traps=6 markers=22 marker_traps=22 vslots=3 model_cases=10 case_coverage_traps=1 whole_image_trap=1`.

Known-answer model ครอบคลุม timer บวก/ศูนย์/ลบ/±infinity/NaN, current value ศูนย์/ไม่ศูนย์, low/alternate pair และ null ActorAttr. Mutations ทำใน memory เท่านั้น; ไม่รัน native code/client/server.

## ส่งต่อ

BUILD_PROPOSED: วัดมอน `n_OFFESIVE=0` ตัวเดิมหลัง hit: style 62→61, หยุดตีขณะผู้เล่นยัง current>0, แล้วทำ local-player current=0 และตรวจ invocation ที่ล้างบิตก่อน style 62 ใน tick ถัดไป | LANE-B | A1_RED_LATCH_RESET_ON_LOCAL_PLAYER_ZERO

ให้ instrumentation แยก log สี่ชั้น: hit target bit-set, selector receiver CNetNPC, singleton predicate pair/result, และ style setter. ถ้าสีคืนปกติก่อน local-player current zero แปลว่ามี writer/reset path อื่นที่ static addendum นี้ไม่ได้ครอบคลุม.

## nonclaims

- ไม่อ้างว่าสถานะนี้มีชื่อ wire ว่า aggro, disengage หรือ timeout และไม่อ้างว่า bit `0x100` จำเป็นต่อ style 61 ทุกทาง
- ไม่อ้างว่า timer `ActorAttr+0x58` เป็นเวลาค้างของสี; มันเป็น input ของ predicate local player ใน consumer นี้
- ไม่อ้างว่า `ActorAttr+0x1A8` เป็น HP ผู้เล่นทุกโหมด; รายงานเพียง current-value alternate ที่ consumer เลือกเมื่อ `CMyActor+0x358!=0`
- ไม่อ้างผลภาพ, same-instance delivery, frame ordering หรือ reset ใน runtime; ไม่มีการเปิดเกม/เซิร์ฟเวอร์
- ไม่ทำ writer census ทั้งโปรแกรมและไม่ตัดความเป็นไปได้ของ clear/store อื่นนอก selector span
- ไม่แก้ ServerProject, queue, lease, workflow, external, gamedata หรือไฟล์หลักฐาน

SCOREBOARD: STATIC-PROVEN | A1 reset receiver = local CMyActor; clear branch requires selected local-player current value zero and ordered timer | standing_a1_reset_verify.py
