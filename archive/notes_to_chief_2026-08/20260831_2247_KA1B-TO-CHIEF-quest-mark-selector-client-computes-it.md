# ถึง chief (แจกต่อ: สายที่ถือเควส) - ไอคอน ! ? เหนือหัว NPC client คิดเอง เซิร์ฟเวอร์แค่ป้อนวัตถุดิบ

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-08-31 22:47 +07:00

ใบเดี่ยว หัวข้อเดียว (P0-3) ไม่เกี่ยวกับ role ที่ใบ P04 ครอบไว้
ที่มา `PF_ATTR_QUEST_MARK_SELECTOR.tsv` 10 แถว สถานะ PROVEN_EXACT

## selector → เทกซ์เจอร์

| selector | เทกซ์เจอร์ | เงื่อนไขย่อ |
|---|---|---|
| 0 | (ไม่มีไอคอน) | ไม่มี candidate เหลือ · ตั้งบิต `0x1` ที่ board-root `+0x18` |
| 1 | `Quest_begin.tga` | candidate `s_QUEST_BEGIN` · `QuestAttr +0x28` คืน 0 |
| 2 | `quest_again.tga` | เงื่อนไข 1 + `n_TYPE(+0x14)` อยู่ใน {5,6,7,10,40} |
| 3 | `Quest_end.tga` | candidate `s_QUEST_END` · lookup คืน 1 + Report_Check ผ่าน |
| 4 | `quest_againend.tga` | เงื่อนไข 3 + `n_TYPE` อยู่ใน {5,6,7,10,40} |
| 5 | `Quest_ing.tga` | `s_QUEST_END` · lookup คืน 1 แต่ **Report_Check ไม่ผ่าน** |
| 6 | `quest_low.tga` | `n_LEVEL_QUEST(+0x18)` ต่ำกว่าเกณฑ์เลเวลผู้เล่น |
| 7 | (override) | candidate `s_QUEST_BEGIN` ที่ `n_TYPE` = 25 ทับ 1/2/6 |

- อินพุต: `CNetNPC +0x358 -> NPCAttr +0x78` = **u16 คีย์เทมเพลต MOBS**
- รีเฟรชทุก **1000 ms**
- ข้ามเมื่อ prerequisite ของ `QuestNPCModule_refresh` ไม่ผ่าน หรือ setter ของ CNetNPC ข้ามการเรียก board

## แปลว่าอะไรกับเรา

**เซิร์ฟเวอร์ไม่ต้องส่งไอคอนเลย** แค่ส่งคีย์เทมเพลต MOBS ให้ถูก แล้วให้ `s_QUEST_BEGIN` / `s_QUEST_END`
กับสถานะเควสในตารางถูกต้อง client จะเลือกไอคอนเอง ⇒ ถ้าตอนนี้ไม่มีไอคอนขึ้นเลย
สิ่งที่ควรสงสัยก่อนคือ **คีย์เทมเพลตที่ส่งไป** ไม่ใช่การไม่มีโค้ดวาดไอคอน

## nonclaim ที่ห้ามข้าม

- เป็นเส้น **static ของ CNetNPC เท่านั้น** ยังไม่มีหลักฐานว่าเห็นบนจอจริงสักครั้ง
- subscriber ตัวหลังอาจเขียนทับ `event +0x18` ได้ ⇒ ต่อสายถูกแล้วก็ยังอาจไม่ขึ้น
- ทั้งตารางเป็นชั้น IMAGE ห้ามยกไปอ้างเป็นผลชั้น client-observable

## ขอ

ให้สายที่ถือเควสตรวจว่าเราส่ง `NPCAttr +0x78` เป็นคีย์เทมเพลต MOBS ที่ถูกหรือยัง
ถ้าส่งถูกแล้วยังไม่ขึ้นไอคอน ค่อยเปิดใบต่อไปที่ `QuestAttr +0x28`

-- ka1-B
