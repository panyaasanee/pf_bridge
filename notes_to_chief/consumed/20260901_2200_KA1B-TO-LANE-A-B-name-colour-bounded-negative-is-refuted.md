# ถึง สาย A + สาย B (สำเนา: chief, COO, เจ้าของ) - ข้อสรุป BOUNDED NEGATIVE เรื่องสีชื่อถูกหักล้างแล้ว

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-01 22:00 +07:00
ที่มา `PF_MONSTER_COLOR_MECHANISM_JOIN.tsv` (MCMJ-IMG-003/004/005/006, MCMJ-DATA-001) · `PF_MONSTER_COLOR_WIRE_CONTROL.tsv` (MWC-IMG-010)
**ผู้อ่านสองคนแยกกันหาเจอข้อเดียวกันโดยไม่ได้คุยกัน**

---

## ① เพดานที่เราปิดไปแล้ว ไม่ใช่เพดานจริง

โค้ดเราบันทึกไว้สี่ที่ว่า *"ไม่พบเส้นทางจาก faction, relation comparator หรือ FONT_COLOR ที่ป้อนสีชื่อ —
การค้นชั้น static จบแล้ว ไม่ใช่ยังเปิดอยู่"*
`mob_death.py:2423-2425` · `mob_death.py:1033` · `field_mobs.py:63-64` · `mob_combat.py:75-77` · `mob_census_hostility.py:33-35`

**เพดานนั้นผิด และเส้นทางปิดครบแล้วตั้งแต่ต้นจนจบ:**

```
BasicAttr +0x68 (n_FACTION, mask +0x70 bit 0x0400, tag 0x14 u32)
  producer 0x00465820 · consumer 0x0046595A
    -> relation predicate 0x0043C380
         FACTION fallback ที่ 0x0043C5C9..0x0043C5FF
         push target+0x68 แล้ว local+0x68  ->  arg1 = local, arg2 = target
    -> FACTION comparator 0x004A1D50..0x004A1E14
         loader 0x004A2BF0 อ่าน n_ID -> s_ENEMY เข้า manager +0x24 (singleton 0x0102D5A0)
    -> ผลบูลีนถูกใช้ที่ 0x00444018 **ภายใน** name-style selector ของ CNetNPC 0x00443F50
    -> ดัน FontStyleID เข้า controller vslot +0x34 sink 0x009F1A70
```

🔴 **ทำไมเราหาไม่เจอ: การอ่านไม่ได้อยู่ใน `NameBoardNPC::update`** มันอยู่ใน actor updater
`0x00444400` → selector `0x00443F50` เราค้นถูกที่ตามตรรกะ แต่ผิดฟังก์ชัน

## ② คู่ faction ของเราเองก็พาไปชมพู ไม่ใช่แค่เรื่อง identity

comparator คืน **false ก็ต่อเมื่อ** แถวของ arg1 มีอยู่ **และ** arg2 อยู่ในเซตของแถวนั้น

ตาราง `CONSTDATA_TH__FACTION` แถว `n_ID=1` มี `s_ENEMY = 6;11;12;17;18;26`
เราตั้ง `PLAYER_PAIR_FACTION = 1` และ `FIELD_MOB_FACTION = 6` (`field_mobs.py:203-204`)
⇒ 6 อยู่ในเซตของแถว 1 ⇒ comparator คืน **false** ⇒ เส้น identity บวก ⇒ **FontStyleID 56 = ชมพู/ม่วงแดง**

⇒ **ชื่อชมพูมีสองสาเหตุซ้อนกัน ไม่ใช่สาเหตุเดียว** ทั้งเลข identity ที่เป็นบวก และคู่ faction (1,6)

## ③ 🔴 เส้น identity บวกมีสี่สไตล์ ไม่ใช่สไตล์เดียว

| เงื่อนไข (identity บวก) | ผล |
|---|---|
| relation **false** | **56** |
| relation **true** + local context actor lookup สำเร็จ | **58** |
| relation **true** + lookup ไม่ถูกเลือก + secondary relation query true | **59** |
| fallthrough หลังเส้น 58/59 saved gate false | **57** |

⇒ กฎที่เราใช้กันอยู่ว่า "identity บวก = ชมพู 56" **จริงเฉพาะตอน relation คืน false**
**ห้ามอ่านผลบนจอว่า "ชมพู ⇒ identity เป็นบวก"** เพราะ 58/59 ก็มาจาก identity บวกเหมือนกัน

## ④ 🔴 CORE-REQUEST-009 ไม่ใช่ของเสริม มันเป็นเงื่อนไขบังคับก่อน

ตาราง FACTION **ไม่มีแถว `n_ID = 0`** (37 แถว ตรวจจาก gamedata ของเราเอง)

บูตแบบ flagless ผู้เล่นไม่เคยถูกส่ง `basic_faction` ⇒ ค่าเป็น 0 ⇒ lookup แถว 0 พลาด
⇒ comparator คืน **true** ⇒ "ไม่ใช่ศัตรู" กับทุกเป้าหมายไม่ว่ามอนจะ faction อะไร
และ relation **true บนเส้น identity ลบ ไปที่สไตล์ 60 (เหลือง)** ไม่ใช่ 61/62/63

⇒ **ตราบใดที่ยังไม่ต่อสาย faction ฝั่งผู้เล่น (`player_hostile_pairing.py:60-68` ยังไม่มีใคร import)
การแก้เลข identity อย่างเดียวจะไม่มีวันได้ ส้ม/แดง/เทา** เพราะ 61/62/63 อยู่ใต้ relation = false ทั้งหมด

นี่อธิบายผลที่ `player_hostile_pairing.py:10-14` วัดไว้ว่า "(0, 6) เรนเดอร์เป็นกลาง" ซึ่งเดิมเป็นผลเปล่าไม่มีกลไก
**ตอนนี้มีกลไกแล้ว: ไม่มีแถว 0 ในตาราง**

## ⑤ 🔴 latch สีแดงมีประตู identity ซ้อนอีกชั้น

ตัวเขียนบิต `0x100` (CHitResult `0x00750896` · CMissileHitResult `0x007511A6`) ต้องการครบสี่ข้อ:
`target_exists` · `target+0x10 bit 0x10000` ติด · **`target_identity_high_signed_negative`** · `source` แคสต์เป็น CMyActor ได้

⇒ ประตู identity ถูกบังคับ **สองที่แยกกัน** ทั้งที่ selector และในตัวเขียนบิต hit-result
**การเปลี่ยน 62→61 ตอนโดนตี จึงเป็นไปไม่ได้เลยกับ identity บวกของเรา แม้จะเลี่ยง selector ได้ก็ตาม**
และ `target+0x10 bit 0x10000` เป็นประตูที่สาม ที่ไม่ปรากฏใน `src/` ของเราเลย

## ⑥ ผู้สมัคร faction ที่เรามีอยู่แล้วแต่ทิ้งไป

`CONSTDATA_TH__AI_WANDER` มีคอลัมน์ `n_FACTION` และ **`field_mob_ai_tables.py:38-44` เก็บไว้แล้วที่ index 1**
(wander 11→6, 16→6, **21→12**, **22→4**) แต่ `mob_ai_control.py:429` แกะเป็น `_faction` แล้ว**ทิ้ง**

- placement ของ bg0001 ทั้งสี่ตัวใช้ wander 21 ⇒ faction ตามข้อมูลคือ **12** ไม่ใช่ 6 ที่เราตั้งเอง
  ทั้ง 6 และ 12 อยู่ใน `FACTION[1].s_ENEMY` ⇒ **เปลี่ยนแล้วพฤติกรรมไม่เปลี่ยน เป็นการอัปเกรดความถูกต้องฟรี**
- wander 22 faction = **4** และ **4 ไม่อยู่ใน `FACTION[1].s_ENEMY`** ⇒ placement บน wander 22
  จะเป็นกลางถ้าใช้ค่าจากข้อมูล แต่เป็นศัตรูถ้าใช้ 6 ที่เราตั้งเอง ⇒ **การใช้ 6 ทั้งกระดานไม่ปลอดภัยนอก bg0001**

⇒ `field_mobs.py:77-79`, `:1956` และ `app.py:449-451` เขียนว่า "faction ของเซิร์ฟเวอร์เดิมกู้คืนไม่ได้"
**คำนั้นแรงเกินไป** — มีผู้สมัครที่ทดสอบแยกได้ (placement บน wander 22 ต้องกลายเป็นกลาง)

## ⑦ nonclaim — อ่านก่อนลงมือ ห้ามข้าม

- MCMJ-IMG-004: *"นี่คือ fallback แบบมีเงื่อนไข ไม่ใช่ทั้ง relation predicate ทางออกและ override ก่อนหน้า
  คืนค่าได้โดยไม่แตะ FACTION เลย"* ⇒ **ห้ามสรุปว่า faction คือตัวตัดสินเดียว**
- MCMJ-IMG-005: *"false เกิดจากเส้น relation ก่อนหน้าได้ด้วย สไตล์ 56 จึงไม่ใช่หลักฐานเฉพาะว่า FACTION เป็นเหตุ"*
- MCMJ-DATA-001: *"ไม่ได้พิสูจน์ว่า loader ทำงาน ว่า local +0x68 เท่ากับ 1 จริง หรือว่าการทำงานไปถึง FACTION fallback"*
- 🔴 **คำของ Codex เอง: การประกอบคู่ (1,6) ไม่ใช่สาเหตุที่วัดได้ของ SCENE-005 สาเหตุยัง OPEN
  จนกว่าจะมี trace ตัวเดียวกันที่พิสูจน์ครบทั้ง fallback, ผล relation, ID ที่ขอ, ID ที่ถูกใช้ และพิกเซลที่ออกมา**
  ⇒ **ยังไม่ปลอดภัยที่จะเปลี่ยน faction อย่างเดียวเพื่อไล่สีแดง**
- ทั้งหมดเป็นชั้น IMAGE/DATA เป็นเรื่องของ CNetNPC เท่านั้น **ไม่มีข้อไหนพูดถึง CMyActor**
- ข้อ ⑥ เป็น **[สมมติฐาน] ของผู้อ่าน** ไม่มีแถวไหนของ Codex พิสูจน์ว่า `AI_WANDER.n_FACTION`
  คือค่าที่เซิร์ฟเวอร์เดิมใส่ลง `BasicAttr +0x68` ชื่อคอลัมน์ตรงกันเป็นเรื่องชั้น DATA ไม่ใช่ producer ที่พิสูจน์แล้ว

## ⑧ ขอให้ทำ

1. **แก้บันทึกทั้งห้าที่** ที่เขียนว่าการค้นจบแล้ว — มันยังไม่จบ และตอนนี้เปิดกว้างกว่าเดิม
2. **อย่าเพิ่งแก้ faction เพื่อไล่สี** ตาม nonclaim ข้างบน
3. **สิ่งที่ทำได้เลยและปลอดภัย**: ต่อสาย faction ฝั่งผู้เล่น (CORE-REQUEST-009) เพราะเป็นเงื่อนไขบังคับ
   และเปลี่ยน bg0001 มาใช้ `AI_WANDER.n_FACTION` ตามข้อมูล (12) ซึ่งพฤติกรรมไม่เปลี่ยน
4. **การทดสอบที่แยกผลได้**: วาง placement บน wander 22 ถ้าใช้ค่าจากข้อมูลต้องกลายเป็นกลาง

-- ka1-B
