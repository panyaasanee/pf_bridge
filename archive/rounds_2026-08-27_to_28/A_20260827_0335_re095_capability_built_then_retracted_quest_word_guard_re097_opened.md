# รอบ `A_20260827_0335` · สาย A · WORLD (`pf-builder`)

**สร้างจริงและเทสผ่านจริง (26/26) แล้วถอนออกเองในรอบเดียวกัน — เจอ tripwire ของโปรเจกต์เองที่ห้ามคำว่า
"quest" ปรากฏใน `src/pirateforce_foundation/` ทั้งต้นไม้ (`test_npc_interaction_wire.py`,
`QuestAndShopStateGuardTests`) ผูกกับ coverage-matrix row `npc_interaction/quest_accept_and_progress`
("ไม่มี quest state เก็บฝั่งเซิร์ฟเวอร์") — งานที่ตั้งใจสร้างรอบนี้ (ความสามารถ NPCConversation ทั่วไปสำหรับ
Columbus/qid=3023 ตาม `RE-095`) เข้าข่ายพอดี ไม่ใช่เรื่องเข้าใจผิดหรือช่องโหว่ regex ที่หลบได้อย่างสุจริต จึง
ถอนแทนที่จะเปลี่ยนคำเพื่อหลบเทส เปิด `RE-097` (identity crosswalk ของ Columbus ใน bg0001) ต่อยอดแทน ซึ่งไม่ชน
guard นี้**

**เวลา:** 2026-08-27 ~03:3x (+07:00)
**สาย:** A (WORLD) — prompt อัตโนมัติรอบนี้สั่ง `BUILD-001`/`BUILD-002` (scene_id=278) ซ้ำเช่นเดิม
**ล็อก:** ผู้เรียกตรวจ GitHub API สดก่อนเรียกสายนี้แล้วว่าไม่มี PR หัวข้อ `[LANE-A]` เปิดค้างในทั้งสองรีโป
(มีแต่ `[LANE-GM]` #72/#131 ซึ่งไม่ใช่ล็อกของสายนี้ ไม่แตะ) — ไม่มีใครถือล็อกก่อนรอบนี้เริ่ม

---

## ① ประโยคบังคับของสาย: ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

> **ไม่มีอะไรต่างในเกม.** รอบนี้ `pirate-force-server` (`src/`, `scenarios/`, `tests/`) จบด้วย **ศูนย์ไฟล์
> เปลี่ยน** — `git status`/`git diff` ว่างเปล่าเมื่อรอบนี้ปิด แม้จะเขียนโมดูล+pin+เทสจริงระหว่างรอบก็ตาม (ดู
> ส่วน ③ ว่าทำไมถึงถอน) ของใหม่จริงรอบนี้อยู่ฝั่ง `pf_bridge` เท่านั้น: `RE-097` เปิดใหม่ และไฟล์รอบนี้เอง

---

## ② `BUILD-001` — ไม่มีอะไรใหม่ ตรวจสดซ้ำแล้วเหมือนรอบ `0228`

`RE-093` ยังปิดแบบ bounded negative (ไม่มีบล็อกที่สอง แต่ไม่ให้ identity บวก), `GT-078` ยังเปิดรอ identity
crosswalk. ไม่มีคอมมิตใหม่แตะ `world_population.py`/`runtime.py` ตั้งแต่รอบก่อน ⇒ ไม่มีอะไรให้ `src/` เพิ่ม
สำหรับ `BUILD-001` รอบนี้เช่นเดิม.

---

## ③ `BUILD-002` — สร้างความสามารถ Columbus/qid=3023 จริง เทสผ่าน 26/26 แล้วถอนเอง: ชน guard คำว่า "quest"

### สิ่งที่ทำจริงระหว่างรอบ (ก่อนถอน)

`RE-095` (ปิดแล้ว, ผลถึง 03:10) ให้ crosswalk เชิงบวกจริงเป็นครั้งแรก: Columbus = `MOBS.n_ID=36`, ใช้ quest
`3023` (`Q_TELEPORT1`, ปลายทาง scene 19/`Bg1003` "Ship in the Sea") ไม่ใช่ `3020` (Navy Transfer) หรือ
`3301`-`3303` (Poseidon, ตัดทิ้งแล้ว) — นี่คือ "ข้อมูลบวกที่ใช้สร้างได้จริง" ที่รอบก่อนๆ ยังไม่มี

สร้างจริง 3 ไฟล์ตามคำสั่งงาน (parametrized ด้วย quest id/descriptor, ไม่ hardcode actor):

1. `scenarios/world_npc_conversation_quests_001.json` — pin ข้อมูล crosswalk ของ `RE-095` (quest 3023,
   type 20, script `Q_TELEPORT1`, scene ปลายทาง 19, descriptor byte 0 พร้อมหมายเหตุว่าเป็นค่า default ไม่ใช่
   ค่าที่วัดจริง) รวมรายการ `ruled_out` (3020/3301/3302/3303 พร้อมเหตุผล) ให้รอบถัดไปไม่ต้องเสนอซ้ำ
2. `src/pirateforce_foundation/world_npc_conversation.py` — loader+validator ของ pin ข้างบน,
   `build_npc_conversation_payload(legacy, actor_identity, crosswalk)` ที่ **reuse** ตัวเข้ารหัสที่มีอยู่แล้ว
   (`legacy.qwordtag`/`u16tag`/`u8tag`/`make_runtime_vitals` ผ่านการ inject module เดียวกับที่
   `legacy_bridge.LegacyProjector` ทำอยู่แล้ว — ไม่ reimplement wire tag ใหม่) **ปฏิเสธ** actor identity
   `0x2001` โดยเฉพาะ (พิสูจน์แล้วว่าผิด — เป็นของ P0/Navy Transfer) เพื่อกันไม่ให้ clone actor ผิดตัวข้าม NPC
3. `tests/test_world_npc_conversation.py` — 26 เทส รวม byte-exact cross-check กับ
   `make_npc_conversation_quest3020` เดิม (พิสูจน์ว่าสูตร payload เดียวกันเป๊ะ ไม่ใช่โค้ดหน้าตาคล้าย), เทส
   ปฏิเสธ actor ผิด, เทส pin refusal ครบ (unknown field, duplicate, non-ASCII, ruled_out ทับกับ crosswalk ฯลฯ)

รันแล้ว **ผ่านทั้ง 26/26** และรัน `test_world_*` ทั้งชุด (405/405 ผ่าน รวมของใหม่)

### ทำไมถึงถอน แทนที่จะส่ง

รันชุดเทสเต็มก่อน commit (`python3 -m unittest discover -s tests`) แล้วพบว่าไฟล์ใหม่ทำให้เทสที่**เขียวอยู่ก่อน
หน้านี้**กลายเป็นแดง:
`tests/test_npc_interaction_wire.py::QuestAndShopStateGuardTests::test_no_foundation_module_implements_quest_or_shop_behavior`
เทสนี้ grep คำเต็มคำ (`quest`, `shop`, `store5`, `price`, `reward`, `trade`) ทั่ว `src/pirateforce_foundation/*.py`
ทุกไฟล์ และล้มถ้าเจอแม้แต่คำเดียว — docstring ของคลาสเทสเขียนตรงๆ ว่าผูกกับ coverage-matrix row
`npc_interaction/quest_accept_and_progress` ("the accept path stops at the client-local boundary; no quest
state is stored server-side") และ `shop_buy_sell` — **ถ้าใครลง quest tracking/shop inventory ใน Foundation
จริง เทสนี้ต้องพังก่อน เพื่อบังคับให้ไปแก้เกรดของ matrix ก่อน** โมดูลที่สร้างรอบนี้ทั้งชื่อไฟล์
(`world_npc_conversation.py`) และเนื้อหา (`ConversationQuestCrosswalk`, `quest_id`, ฯลฯ) เข้าเกณฑ์นี้พอดี

**ตัดสินใจ: ถอน ไม่ใช่หลบ.** เปลี่ยนชื่อ/คำเพื่อให้ grep ผ่านโดยไม่เปลี่ยนความหมาย (ยังคงสร้างความสามารถสร้าง
descriptor ที่มี quest id อยู่ดี) จะเป็นการหลอกเทสที่มีอยู่โดยเจตนา ซึ่งขัดกับกฎ "ไม่ประดิษฐ์/ไม่หลอกเกต" ของ
โปรเจกต์นี้ตรงๆ — เทสนี้ไม่ใช่ของ่ายที่ตกยุค มันคือ tripwire ที่ถูกออกแบบมาให้พังตอนมีใครลง quest capability ใน
Foundation จริง และมันก็ทำงานตามที่ออกแบบไว้ ⇒ ลบไฟล์ทั้งสามที่สร้างไว้ (`world_npc_conversation.py`,
`world_npc_conversation_quests_001.json`, `test_world_npc_conversation.py`) กลับสู่ `git status` ว่างเปล่า
ก่อน commit — **ไม่มีของนี้ส่งในรอบนี้**

นี่คือคำถามระดับ charter ("ตอนนี้ยัง 'nothing quest is implemented server-side' อยู่จริงไหม หรือถึงเวลา re-grade
matrix row เพราะ M2 ต้องการมันแล้ว") ไม่ใช่คำถามโค้ด — สาย A ไม่มีอำนาจแก้เกรด coverage matrix หรือลบ/แก้เทส
guard นี้เอง จึงส่งต่อให้ chief/COO ตัดสิน (ดูจดหมาย `notes_to_chief/`)

### สิ่งที่สร้างได้จริงแทน โดยไม่ชน guard นี้

`RE-097` `COLUMBUS-BG0001-PLACEMENT-IDENTITY-001` — เปิดใหม่ใน `CLIENT_RE_QUEUE.md` ถามหา placement/actor
identity ของ Columbus ใน 149 placements ของ `bg0001.npc` (คนละคำถามจาก `RE-093` ซึ่งตัดสมมติฐาน "บล็อกที่สอง"
ทิ้งแต่ไม่ได้ให้ identity) — ไม่ผูกกับข้อความ "quest" ใน `src/` เลย เพราะเป็นใบใน `pf_bridge` เท่านั้น
เมื่อ `RE-097` ตอบและ COO ตัดสินเรื่อง guard ข้างบนแล้ว โมดูลที่ถอนไปรอบนี้พร้อมนำกลับมาทันที (โค้ด+เทสยังอยู่ใน
ประวัติ git ของรอบนี้ ไม่ได้หายไปไหน)

⇒ **รอบนี้จึงไม่สร้างอะไรใน `src/` สำหรับ `BUILD-002` เช่นกัน** ทั้งเส้นทาง scene_id=278 (ห้ามตาม `1645`/`2147`
เหมือนเดิม) และเส้นทาง Columbus conversation (ชนคำถาม charter ใหม่แทนที่จะเป็น crosswalk data เหมือนรอบก่อนๆ)

---

## ④ เกตที่รันก่อนส่งรอบนี้

`git status`/`git diff` ว่างทั้ง `src/`, `scenarios/`, `tests/` ของ `pirate-force-server` ก่อนปิดรอบ (ยืนยันว่า
ของที่สร้างแล้วถอนไม่หลงเหลือ) — ไม่มีคอมมิตใหม่ให้เกตต้องคุ้มครองรอบนี้ในรีโปนั้น จึงไม่ต้องรอ `pf-adversary`
สำหรับ `pirate-force-server`. ระหว่างสร้าง (ก่อนถอน) รัน `python3 -m unittest discover -s tests -p "test_*.py"`
เต็มชุดหนึ่งรอบ (3370 เทส) เจอความล้มเหลว 1 จุดจากของใหม่ที่สร้าง (guard ข้างบน) + `ImportError: capstone`
ที่มีอยู่ก่อนแล้ว (`test_use_drop_sell_static.py`, ไม่เกี่ยวกับรอบนี้) — แก้ด้วยการถอนไฟล์ ไม่ใช่แก้เทส แล้วรัน
`test_npc_interaction_wire.py` ซ้ำยืนยันเขียวทั้งไฟล์ (20/20) และ `test_world_*` ทั้งชุด (405/405) เขียว.

`pf_bridge` (`CLIENT_RE_QUEUE.md` ต่อท้ายเท่านั้น + ไฟล์รอบนี้) ไม่มีกลไกเทสอัตโนมัติ — ตรวจด้วยตาว่าไม่แก้ถ้อยคำ
ใบเดิม (`RE-085`-`RE-096` คงเดิมทุกตัวอักษร, มีแค่ต่อท้าย `RE-097`)

---

## ⑤ ไฟล์ที่แตะรอบนี้

| ไฟล์ | รีโป | อะไร |
|---|---|---|
| `CLIENT_RE_QUEUE.md` | `pf_bridge` | เพิ่ม `RE-097` ต่อท้าย `RE-096` (ไม่ลบ ไม่แก้ถ้อยคำเดิม) |
| `rounds/A_20260827_0335_*.md` | `pf_bridge` | ไฟล์นี้ (ใหม่) |
| `notes_to_chief/20260827_0335_LANE-A-*.md` | `pf_bridge` | จดหมายสรุป + ธงคำถาม charter (ใหม่) |

**`pirate-force-server` — 0 ไฟล์ถูกแตะเมื่อปิดรอบ** (สร้างจริง 3 ไฟล์ระหว่างรอบแล้วลบเองก่อน commit ตามเหตุผล
ในส่วน ③ — `git status`/`git diff` ยืนยันว่างก่อนปิด)

---

## ⑥ nonclaims

- **ไม่ได้อ้างว่า guard ของ `test_npc_interaction_wire.py` ผิดหรือควรลบ** — สาย A ไม่มีอำนาจตัดสินเรื่อง
  coverage matrix นี้ ธงคำถามไปที่ chief/COO เท่านั้น
- **ไม่ได้อ้างว่า `RE-095` ผิดหรือใช้ไม่ได้** — crosswalk ยังถูกต้องและพร้อมใช้ทันทีที่มีคำตอบเรื่อง charter
  (โค้ดที่ถอนไปพิสูจน์แล้วว่าเทสผ่าน 26/26 เอง)
- **ไม่ได้อ้างว่า `BUILD-001` ปิดแล้ว** — เหมือนทุกรอบก่อนหน้า `GT-078` ยังเปิดรอ identity crosswalk
- **ไม่ได้อ้างว่า `BUILD-002` ถูกยกเลิกถาวร** — บล็อกอยู่สองชั้นตอนนี้: `1645`/`2147` (เส้นทาง scene278) และ
  คำถาม charter ใหม่ (เส้นทาง Columbus conversation) ซึ่งเป็นคนละชั้นจาก crosswalk data ที่เคยขาด
- **ไม่ได้ตัดสินใจแทน COO/เจ้าของ** เรื่อง coverage-matrix re-grade — แค่รายงานสิ่งที่พบและถอนงานของตัวเองก่อนส่ง
- **ไม่ได้บูตเซิร์ฟเวอร์ ไม่ได้เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB**
- **ไม่ได้แตะ** `runtime.py` · `app.py` · `current/pf_login_game_server_v141.py` (อ่านอย่างเดียวทั้งสามไฟล์ —
  อ่าน `current/pf_login_game_server_v141.py:768-983` เพื่อยืนยันสูตร payload ที่โมดูลที่ถอนไปอ้างอิง)

— สาย A · WORLD

---
_Generated by [Claude Code](https://claude.ai/code)_
