# ถึง chief (แจกต่อ: สายที่ถือ wire ทุกสาย) - แก้ตัวตนใน registry/vtable สามข้อ กระทบคำอธิบายในโค้ดเรา

จาก: ka1-B (ผู้ช่วย attended, กะ1) · 2026-09-01 21:17 +07:00
ที่มา `PF_SERIALIZER_SLOT34_CORRECTION.md` · `PF_STATIC_TYPE_INFO_CLASSMAP.md` · `PF_TARGETS_694790_6B3440_NONWIRE.md`

ทั้งสามข้อเป็นเรื่องเดียวกัน: **ตัวตนของช่อง/คลาสใน registry ที่เราอ้างไว้ในคอมเมนต์ ไม่ตรงกับที่แกะได้**
ไม่มีข้อไหนเป็นบั๊กที่ผู้เล่นเจอ แต่ทุกข้อทำให้เหตุผลที่เราเขียนไว้ในโค้ดผิด

---

## ① `0x0043BB80` ไม่ใช่ serializer ที่ใช้ร่วมกัน — คอมเมนต์เราบอกว่าใช่

V1 อ่านช่อง serializer จาก vtable **`+0x18`** ทั้ง 502 รายการ · การแบ่งตามความสามารถพิสูจน์ว่า
**56 แถวมี `NONE` ที่ `+0x18` และมี `R|W` ที่ `+0x34`**

`serializer_va = 0x0043BB80` โผล่บน **45 จาก 519 แถว** และทั้ง 45 แถวมี `old_slot_capabilities = NONE`
⇒ **มันไม่ใช่ stub ที่ใช้ร่วมกัน มันคือร่องรอยของการอ่านผิดช่อง ไม่มีความสามารถอ่านหรือเขียนบนสายเลย**

ตัว serializer จริงอยู่ที่ `+0x34` และ**แยกกันคนละตัว**:
`ActorAttr → 0x00466230` · `BasicAttr → 0x004656F0` · `DBAttribute → 0x00467790` ·
`CSkillAttr → 0x007520B0` · `MovementAttr → 0x004671C0` · `NPCAttr → 0x00466EB0` ·
`NPCAppearAttr → 0x00737FD0` · `BackpackAttr → 0x00469FA0`

**ขัดกับ:** `logout_hypothesis.py:296` เขียนว่า *"contrast serializer_va 0x0043BB80, shared by the whole Attr cohort"*
ข้อสรุปของใบนั้น (ว่า `handler_va 0x005F1190` ไม่ซ้ำใคร) **ยังยืน** แต่สิ่งที่มันยกมาเทียบเป็นโมฆะ และจำนวนคือ 45 ไม่ใช่ "ทั้ง cohort"

🟢 **ข่าวดี: สี่เลนของเราปักหมุด `+0x34` ตัวจริงไว้ตรงกับ Codex เป๊ะอยู่แล้ว** —
`stats_progression_hypothesis.py:189-191` และ `skill_attr_hypothesis.py:121` (อันหลังเขียน "vtable +0x34" ไว้ด้วย)
และเลนแชตไม่กระทบ: ไม่มีแถว `Channel*` และไม่มี `0x0065AD40` ใน delta เลย ⇒ `channel_message_hypothesis.py:29,150` ยังถูก

## ② เติมตัวตน `VitalData` ที่ registry เว้นว่างไว้ — พร้อมข้อห้ามหนึ่งข้อ

`PF_PROTOCOL_REGISTRY.tsv` บรรทัด 93 มี `VitalData` แต่ `vtable_va = UNKNOWN`, `serializer_va = UNKNOWN`

classmap เติมให้: **`VitalData` vtable `0x00F0B930`** (file off `0x00B09D30`) · registry getter `0x004277C0` ·
TypeDescriptor `0x0101B16C` · และ **`Channel_MessageVtial` vtable `0x00F375FC`** (file off `0x00B359FC`)
โซ่ฐาน: `Channel_MessageVtial → Channel_BasicVtial → ClonableVital → VitalData`

**เป็นประโยชน์กับ** `channel_message_hypothesis.py` ซึ่งประกอบ payload ของ Channel ในซอง VitalData
นี่เป็น vtable VA ตัวแรกของสองคลาสนี้ และเป็นครั้งแรกที่เรารู้ชื่อคลาสฐานสองตัวกลาง

🔴 **ข้อห้าม (nonclaim ตรงตัว):** การใช้ registry getter ร่วมกัน "พิสูจน์แค่ลำดับชั้นคลาสแบบ static และการใช้ getter ร่วมกัน
**ไม่ได้บอกอะไรเกี่ยวกับพฤติกรรมตอนรัน และไม่ใช่เหตุผลให้ยุบหรือรวม schema ของ serializer เข้าด้วยกัน**"
ข้อห้ามเดียวกันใช้กับ `StallItem → ItemAttr` · `serializer_identity_status` ของ VitalData ยังเป็น `UNKNOWN`

## ③ "generic VitalData collection reader" ของเรา จริง ๆ แล้วห้าข้อความใช้ร่วมกัน

ช่วง `[0x005F3E20,0x005F406D)` 589 ไบต์ เป็น serializer **ที่ใช้ร่วมกันของห้าข้อความพอดี**:
`GSCN_RunTimeProtocolReq` · `GSCN_RunTimeProtocolRes` · `GSCN_LoginProtocol` · `LSCN_Protocol` · `VitalProtocol`
คอนเทนเนอร์ลิสต์อยู่ที่ `owner+0x10` sentinel `owner+0x24`

helper สองตัวพิสูจน์แล้วว่า**ไม่ใช่เส้นบนสาย**: `0x006B3440` จองโหนดคงที่ 12 ไบต์ (`ret 12`) ·
`0x00694790` เติมเข้า `container+0x18` (`ret 4`) ทั้งคู่ไม่มี stream formal และไม่แตะ wire primitive `0x0089A600`/`0x0089A640`

**เกี่ยวกับ:** `gm/state_wire.py:50` · `gm/teleport_wire.py:89` · `damage_model_hypothesis.py:237`
ที่ปักช่วงนี้ไว้ว่าเป็น "generic VitalData collection reader" หลังกลไก version-byte ของ RE-105

⇒ คำว่า "generic" ตอนนี้**เป็นชื่อที่ชัดแล้ว: ห้าเจ้าของ ไม่ใช่เส้นเฉพาะ VitalData**
กลไกของ RE-105 จึงเป็นแบบ per-vital-instance จริง และ**ทำให้เจาะจงรายข้อความไม่ได้**

⚠️ ตัววิเคราะห์ของ Codex เอง **แก้ stream provenance ผ่านช่วงนี้ไม่ได้**
(`primitive_stream_provenance_unresolved expected=entry+0x4 observed=NONE`) ⇒ งานคอนเทนเนอร์ในนั้นปิดแล้ว
แต่**พฤติกรรมบนสายยังไม่ปิด** และทั้งห้าข้อความยังเป็น `OPEN`

---

## กติกา

ทั้งสามข้อเป็นชั้น **IMAGE** ล้วน เป็นเรื่องตัวตน/ช่อง ไม่ใช่ความหมายของค่า
ไม่มีข้อไหนเป็นหลักฐานตอนรันหรือบนจอ · ค่า `descriptor_file_off` ทั้งหมดเป็น `UNMAPPED_BSS` ⇒ ไม่มีการอ่านไบต์ descriptor
**สิ่งที่ควรทำคือแก้คอมเมนต์/เหตุผลในโค้ดให้ตรง ไม่ใช่แก้พฤติกรรม**

-- ka1-B
