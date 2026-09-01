[ถึง: chief (สาย E) | cc: COO, Panya, สาย B, สาย GM, สาย RE, ผู้เทสทุกกะ | จาก: LANE-A (WORLD) รอบ `02k3w5` · 2026-08-29T01:46+07:00]
[ADDRESSEE: CHIEF]
[ตอบ/ต่อยอดจาก: `20260829_0018_KA3A-GT122-PASS-GT102-PARTIAL-GT104-BLOCKED-mobs-answer-as-npc.md` ข้อ ②]

# LANE-A CORE-REQUEST — **เจอตัวที่ทำให้หน้าต่างของ Columbus พูดเป็น Sebastian แล้ว มันอยู่ในทรีเรา ไม่ใช่ที่ไคลเอนต์** · ขอแก้ 3 บรรทัดในไฟล์แช่แข็ง

## หนึ่งประโยค

`make_v98_conversation_face_state` (`current/pf_login_game_server_v141.py:1088-1096`) ยัง resolve ตัวตน
จากตารางเก่า `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS` ⇒ **ทุกครั้งที่ผู้เล่นคลิก NPC มันส่งเฟรมที่ตีตรา
actor `0x2002` ใหม่เป็น MOBS `2` (Sebastian ผู้คุมเกาะคุก) ทับตัวตนที่สำมะโนตอนล็อกอินส่งไว้ถูกแล้ว (MOBS `156` Columbus)**

## หลักฐาน (สองชั้น ชั้นบนมาก่อน)

**client-observable** — เจ้าของ 2026-08-29T00:17+07:00 (`OBSERVER_CONFIRMED`, บูตไร้แฟล็ก
`BOOT_COMMIT 3baf65de`): คลิก Columbus → หน้าต่าง QUEST หัวข้อ **`Sebastian`** เนื้อ "Prison Exile Island
ข้าคือผู้คุม..." **เสียงพากย์เป็นเสียง Sebastian** · แต่แผงเป้าข้าง ๆ อ่านว่า **`Columbus`**
⇒ สองเฟรมในบูตเดียวกันพูดคนละคนเรื่องตัวเดียวกัน นี่คือ signature ของฝั่งเซิร์ฟเวอร์ ไม่ใช่ของไคลเอนต์

**ตาราง/ซอร์ส** (สาย RE static รอบนี้ ทุกข้อมีบรรทัดที่มา):
- `TEXTDATA_TH__MOBS_TIP.tsv` บรรทัด 3: `n_ID=2` `s_NAME=Sebastian` `s_TITLE=Warden`
  `s_NPC_CHATS` = `<text>[52300002]</text> ข้าคือผู้คุมของที่นี่...` · `52300002` → `SCENE_NAME_TIP` บรรทัด 3 =
  ` Prison Exile Island ` ⇒ **ประกอบกลับได้เป็นสตริงที่เจ้าของเห็นทุกตัวอักษร**
- `CONSTDATA_TH__MOBS.tsv` บรรทัด 3: `n_ID=2` `s_NPC_VOICE=20;21` · บรรทัด 153: `n_ID=156` (Columbus)
  `s_NPC_VOICE=93;94;95` ⇒ **เสียงที่ต่างกันที่เจ้าของได้ยิน ตรงกับตารางคนละแถว**
- `v141:1325` แถวของ placement 1 คือ `(1, 2, ..., 'M010_001_000_N', 'Sebastian')`
- `v141:1094` แตกแถวเป็น `_, template_id, px, py, pz, preset, _` — **ฟิลด์ที่ 7 (ชื่อ) ถูกทิ้งด้วย `_`**
- `v141:1096` `make_npc_attr(template_id, aid, 1, 0, preset)` — พารามิเตอร์ที่ 1 คือ **MOBS/template u16 ที่ `+0x78`**
  (docstring ของ `make_npc_attr` เอง `v141:1145-1146`) ⇒ **เลข Mob-Set ถูกส่งในช่องที่ต้องเป็น MOBS n_ID**
- ควบคุมกลับ: `CLINE[(n_CLINE_TYPE=1, n_CREATURE_TYPE=2)]` = แถว `1001` `n_LEADER_BK1=156`
  ⇒ **placement 1 คือ Columbus จริง** · `COLUMBUS_PLACEMENT_INDEX = 1` ของสาย A ถูกอยู่แล้ว
- เลข `2` เป็น **ทั้ง** เลข Mob-Set ที่ถูกต้อง **และ** MOBS n_ID ของ Sebastian ⇒ บั๊กนี้ไม่โผล่เป็นเลขผิด
  แต่โผล่เป็น **คนผิด** ซึ่งคือสิ่งที่เจ้าของเห็น

## ขอให้แก้อะไร (บรรทัดเดียวในทางความหมาย สามบรรทัดในทางโค้ด)

ที่ `v141:1094-1096` — resolve เลข Mob-Set ผ่าน `world_port_royal_identity.resolve()` แล้วส่งค่าที่ resolve ได้:

```
identity = world_port_royal_identity.resolve(template_id)      # เพิ่ม (import แบบ lazy ในฟังก์ชัน)
attrs = [(NPC_ATTR, make_npc_attr(identity.mobs_n_id, aid, 1, 0,
                                  identity.outfit, basic_name=identity.name))]
```

**นี่คือ call เดียวกับที่ `world_population._entry` (`src/pirateforce_foundation/world_population.py:376-417`)
ทำอยู่แล้ว** ไม่ใช่ทางใหม่ · ถ้า `resolve()` คืน `None` (ตัวที่สำมะโนไม่ส่งอยู่แล้ว) **ห้าม fallback เป็นเลข Mob-Set**
— นั่นคือบั๊กเดิม — ให้คงพฤติกรรมเดิมเฉพาะตัวนั้นแล้วพิมพ์ token บอกชื่อ index ออกคอนโซล

## ทำไมสาย A ไม่แก้เอง

`current/pf_login_game_server_v141.py` เป็นไฟล์แช่แข็ง: `AGENTS.md` บรรทัด 130 บังคับว่ามันต้อง "clean"
ตอน commit และ `legacy_bridge.py` บรรทัดแรกเขียนว่า "frozen V141 serializers" · ประวัติยืนยัน: ไฟล์นี้
ถูกเพิ่มครั้งเดียว 8,014 บรรทัด (PR #159, 27 ส.ค.) และ **ไม่เคยถูกแก้อีกเลย**
⇒ นอกเขตเขียนของสาย A · **[สมมติของสาย A - รอ COO ยืนยัน]** ว่าไฟล์นี้เป็นของ chief ถ้าผิด บอกมา สาย A แก้เองรอบหน้าได้ทันที

## สาย A ทำอะไรไปแล้วในรอบนี้ เพื่อให้คุณแก้แล้วจบในรอบเดียว

`tests/test_face_frame_identity_contradiction.py` (ลงในรอบนี้ เขียวแล้ว 5 ข้อ) — พินความขัดแย้งไว้ทั้งก้อน
พร้อม**เทสตรวจรับของการแก้**: `test_the_fixed_face_frame_must_ship_the_census_identity`
🔴 **เมื่อคุณแก้แล้ว เทส `test_face_frame_ships_the_set_number_while_census_ships_the_mobs_id` จะแดง —
นั่นคือสัญญาณว่าแก้สำเร็จ** ข้อความ assert บอกตรง ๆ ให้ลบคลาสนั้นทิ้ง ไม่ใช่ให้ย้อนโค้ด

## ของแถมที่อาจได้ฟรีในการแก้เดียวกัน (ยังไม่วัด อย่านับเป็นข้ออ้าง)

`v141:1094` ทิ้งฟิลด์ชื่อ ⇒ ทุกคลิกส่ง population ทั้งชุดด้วย `basic_name=""` และ BasicAttr บิต `0x0001`
คือเส้นที่ `0x51F920` ก๊อปลง `LABEL_NAME` ⇒ **น่าจะเป็นสาเหตุเดียวกับ finding "ป้ายชื่อหายหลังขยับ" (④.2)**
[สมมติของสาย A - ยังไม่วัด] · ถ้าจริง แก้จุดเดียวได้สองเรื่อง

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน (ถ้าใบนี้ลง)

คลิก Columbus แล้ว **หน้าต่างขึ้นชื่อ Columbus พูดบทของ Columbus ด้วยเสียงของ Columbus** แทนที่จะเป็น
ผู้คุมจากเกาะคุกที่อยู่คนละเกาะ · และป้ายชื่อ NPC ทั่วเมืองน่าจะไม่หายหลังคลิก
**ตัวปิด: `GT-102` ใบเดิม ไม่ต้องเปิดใบใหม่**
