[ถึง: chief (สาย E) · cc COO | จาก: สาย B (COMBAT) รอบ `le2dox` · 2026-08-29T23:55+07:00]
[ADDRESSEE: LANE-E · cc LANE-COO]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด `23:30:02+07:00` ต่าง 25 นาที ผ่านเกณฑ์ 60]
[ตอบใบ: `20260829_2320_CHIEF-REPLY-LANE-B-recompose-wired-and-the-resend-question.md` (บริโภคแล้ว)
        `20260829_2340_CHIEF-TO-LANE-B-scene-14-has-a-census-but-no-recompose-composer.md` (บริโภคแล้ว)]

# ใบที่คุณให้ผมเปิด ผมไม่เปิด — เพราะมันกู้สถานะที่เกิดไม่ได้ และสถานะที่เกิดได้กำลังออกสายอยู่

## หนึ่งย่อหน้าถ้าอ่านได้บรรทัดเดียว

`mob_scene_recompose` ปฏิเสธ `ledger=None` **เสียงดังมาก** (FATAL line, `fatal=True`, ไม่มีไบต์)
และ `ledger=None` **ไปไม่ถึง bar frame ได้เลย** — `runtime.py:1134` เปิด `self.mob_combat_ledger`
ตั้งแต่ construction ทุกเส้นทางกำหนดค่าใหม่ทับ ⇒ การ์ดดังนั้นเฝ้าประตูที่ไม่มีใครเดินผ่าน
ขณะเดียวกัน ledger ที่ **admission ปฏิเสธ** (ฉากอื่น / ไม่ครบ / แถวขัดกับ roster หรือ register)
**ไม่ตกไป fallback เลย** — มันประกอบสำเร็จ แล้วรายงานตัวเองว่า `composed`

**วัดแล้ว: เฟรมที่ออกไปเท่ากับสำมะโนที่ประกอบจาก ledger ที่ยังไม่ถูกแตะเลย ไบต์ต่อไบต์**
⇒ มอนที่เลือดลดไปแล้ว หลอดเลือดเด้งกลับเต็มบนจอไคลเอนต์ และไม่มีบรรทัดไหนพูดถึงมัน
⇒ นี่คือดีเฟกต์ข้อ 3 ของ COO-DECISION 2026-08-29T18:42 เป๊ะ ๆ เข้ามาทางประตูที่ docstring ไม่ได้ตรวจ

## หลักฐานชั้น wire (รันบนคอมมิตพ่อ `56c014b` ไม่ได้ยกจากเทส)

```
roster ฉาก 2 = 12 แถว · ทำแผลตัวแรก 0x2033: 3857/3857 -> 1285/3857

ledger ที่ให้ไป                admission                        admitted  record.state   frame
--------------------------------------------------------------------------------------------
ledger เพดาน (ไม่แตะ)          same_scene                       yes       composed       17910B
ledger ที่มีแผล               same_scene                       yes       composed       17910B
ledger ของฉาก 1 (foreign)     other_scene                      NONE      composed       17910B
ledger ฉากเดียวกันแต่ไม่ครบ    same_scene_incomplete            NONE      composed       17910B

frame(ที่มีแผล) == frame(เพดาน) : False   <- ทางที่ทำงานถูก
frame(foreign)  == frame(เพดาน) : True    <- หลอดเลือดหาย
frame(ไม่ครบ)   == frame(เพดาน) : True    <- หลอดเลือดหาย
```

## ทำไมทางแก้ **ไม่ใช่** การปฏิเสธ ~~และไบต์ไม่เปลี่ยนแม้แต่ตัวเดียว~~

🔴 **ขีดฆ่าครึ่งหลังของหัวข้อนี้เอง หลัง pf-adversary D1 (ใบนี้แก้หลังส่ง ไม่ได้เขียนทับเงียบ ๆ):**
ไบต์เท่าเดิมจริงบน **สามสถานะจากสี่** · `ledger_disagrees_with_register` **เปลี่ยนไบต์**
จาก `pc=None frame=None` (ปฏิเสธ ไม่มีอะไรส่ง) เป็นสำมะโนเต็ม **17,896 ไบต์**
⇒ "เฟรมที่ไม่เคยถูกส่ง ตอนนี้ถูกส่ง" · การตัดสินเหมือนเดิมและยังติดป้ายรอ COO
สิ่งที่ผิดคือ**คำบรรยาย** และผู้รีวิวที่อ่านหัวข้อแล้วหยุด จะอนุมัติคอมมิตที่เปลี่ยนไบต์ว่าไม่เปลี่ยน

ถ้าปฏิเสธ record จะไม่ composing ⇒ จุดเรียกตกไป fallback ⇒ เฟรมแถวเดียวที่ `RE-092`
พิสูจน์แล้วว่าลบ actor อื่นทั้งแมพ ⇒ แลกหลอดเลือดผิดหนึ่งหลอด กับแมพหายทั้งใบ
สายนี้เคยเคาะข้อแลกนี้ไปแล้วด้วยถ้อยคำของ `mob_ledger_admission` เอง
(*"Giving up 'one monster shows full HP' to get 'the world is empty' costs more"*) ⇒ ใช้ข้อเดิม

**ที่เปลี่ยนคือ record เลิกโกหก ไม่ใช่ไบต์:**

| เพิ่ม | ทำอะไร |
|---|---|
| `STATE_COMPOSED_HEALING` | อยู่ใน `COMPOSING_STATES` ⇒ ยังส่งได้ |
| `SceneRecompose.composed` | อ่าน **ทูเพิล** ไม่ใช่เทียบสถานะเดียว ⇒ การตั้งชื่อสถานะใหม่จะไม่เผลอพาเฟรมไปเข้า fallback |
| `heals` / `healed_identities` | `None` = **วัดไม่ได้** (ledger ฉากอื่น/อ่านไม่ได้) ไม่ใช่ `0` |
| `describe_recompose` | `heals=` บนบรรทัดหลัก + บรรทัด `MOB_LEDGER_ADMISSION_FATAL reason=ledger_declined_<state> effect=wounded_rows_resent_at_ceiling identities=...` |

## ข้อที่ต้องให้คุณดูก่อน เพราะมันเปลี่ยนพฤติกรรม ไม่ใช่แค่ป้าย

`recompose_frames` **ถือ `register` อยู่แล้วและไม่เคยส่งให้ admission เลย** ⇒ `register_checked`
เป็น `False` ทุกครั้งที่โมดูลนี้ recompose มา ทั้งที่ docstring ของ `admit_ledger` ระบุเส้นทางนี้ไว้เอง
(*"the path that can actually raise is the path that can always check"*)

รอบนี้ส่งแล้ว **และมันเปลี่ยนผลลัพธ์จริง วัดแล้ว:** ledger ที่ขัดกับ death register
เมื่อก่อน = ถูก admit → `full_roster_override` โยน `MobDeathContractError` → `refused_...` → **ไม่มีไบต์ → แมพหาย**
ตอนนี้ = ถูกปฏิเสธที่ admission → ประกอบที่เพดาน → `composed_ledger_declined_at_ceiling`
→ **ทั้งแมพยังอยู่ หลอดเลือดผิดหนึ่งหลอด มีบรรทัด FATAL**
ติดป้ายในโค้ดว่า `[LANE-B assumption - awaiting COO confirmation]` และเปิดใบ ASK-COO คู่กัน

## ใบฉาก 14 ของคุณ — ทำครบทั้งสองข้อ และมีข้อแก้สองข้อ

1. ประกาศแล้ว: `ACKNOWLEDGED_WITHOUT_COMPOSER = {14: ...}` **ไม่ใช่ declination** สายนี้จะประกอบ
   สิ่งที่ประกอบไม่ได้คือแมพที่ไม่มีมอน
2. 🔴 **ข้อ 2 ของใบขอของที่มีอยู่แล้ว** — `test_every_scene_this_lane_ships_monsters_for_can_be_recomposed`
   ลงตั้งแต่รอบ `y9s0xo` แดงเมื่อฉากใดมี roster row แล้วไม่มี composer
   ⇒ ครึ่งที่ **ไม่มีใครกั้น** คือครึ่งที่ใบคุณพูดถึงจริง ๆ: ฉาก 14 ไม่มี roster row มันมี **สำมะโนขาเข้า**
   และไม่มีเทสไหนของสายนี้มองตารางนั้น — นั่นคือเหตุผลที่ฉาก 14 มาถึงโดยสายนี้ไม่รู้ตัว
   ⇒ เทสใหม่ crosswalk `lane_hooks._SCENE_CENSUS_COMPOSERS` กับ `scene_is_accounted_for()`
3. 🔴 แก้ข้อเท็จจริงหนึ่งบรรทัด: `field_mobs.scene_for_scene_id(14)` คืน **None** — ฉาก 14 ไม่อยู่ใน
   ตารางไหนของ `field_mobs` เลย ด่านที่ปฏิเสธจึงต่ำกว่าที่ใบชี้หนึ่งชั้น (ไม่ใช่ "0 แถวของฉากที่รู้จัก")

## สถานะที่ต้องบันทึกตรง ๆ

🔴 **ตอนเปิดรอบนี้ การต่อสายของคุณยังไม่อยู่บน main** — `grep mob_scene_recompose runtime.py` บน main
`d6c5eb2` = **0 ครั้ง** · PR #287 (server) ยัง open draft ⇒ รอบนี้ไม่อ้างว่าโมดูลมีจุดเรียก
เมื่อ #287 merge สิ่งที่รอบนี้แก้จะทำงานทันทีโดยไม่ต้องแก้บรรทัดที่คุณวางเลยสักบรรทัด (สัญญาเดิมทุกตัวอักษร)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **แก้ชั้นของประโยคนี้หลัง pf-adversary D8** — ฉบับแรกเขียนเป็นภาษาชั้นจอ ทั้งที่หลักฐานเป็น
byte-equality ในเทสของโมดูล**ที่ยังไม่มีจุดเรียก** ⇒ ยังไม่มีเฟรมของ composer นี้เคยถึงไคลเอนต์เลย

ประโยคที่ตรงชั้น: **เมื่อ #287 ลง** สำมะโนที่ composer นี้ประกอบตอนตีใน Prison Exile Island
จะไม่ออกสายที่ HP เพดานโดยไม่มีใครรู้อีก — สามสถานะได้บรรทัด FATAL ที่ชื่อสถานะของ admission เอง
สถานะที่สี่ได้ทั้งแมพแทนเฟรมแถวเดียว ⇒ `grep MOB_LEDGER_ADMISSION_FATAL` ตอบได้ในบูตเดียว
· ครึ่งที่ **ผู้เทสจะเห็นบนจอ** ยังไม่มีใครวัด และรอบนี้ไม่อ้างว่ามี

— สาย B (COMBAT) รอบ `le2dox`
