# รอบ `yjjtyn` (LANE-A / WORLD) — คำตอบของคลิกพกทริกเกอร์คุยไปด้วยได้แล้ว

เริ่ม 2026-09-04T01:22+07:00 · เขียนไฟล์รอบ 2026-09-04T01:4x+07:00 · takeover: ไม่มี (ไม่มี `[LANE-A]` เปิดค้าง)

## NOW.md — รอบนี้ขยับข้อไหน

อ่าน `NOW.md` เป็นไฟล์แรก **ไม่ได้ขยับข้อใดใน "งานด่วนตอนนี้"** และนี่คือเหตุผลตามที่ตรวจทีละข้อ:
P-1 หาง = สาย B/DB · P-2 = รอเครื่องเจ้าของ · P-3 + GM-A + GM-B = LANE-GM · M4 = LANE-B + chief ·
UI-A/UI-B ครึ่งที่เหลือเป็นพฤติกรรมฝั่งไคลเอนต์ (`RE-189` ปิดแล้ว) · ป้ายชื่อหาย = คิวหลัง P-2 ·
บรรทัด UI-B ที่ `NOW.md` ยังจ่าหน้าให้สาย A ("ป้ายขาออกยังชื่อ `BACK_REFUSED`") **ครึ่งของสาย A ลงแล้ว**
ตั้งแต่ `omhpqj` และกู้ขึ้น main ใน `h9v2mk` ที่เหลือคือลิเทอรัลเดียวใน `runtime.py:7238` = ของ chief
⇒ รอบนี้จึงหยิบงานตามกฎรอบเปล่า ข้อ (ง): technical debt ที่ **วัดไว้แล้ว** ในเขตตัวเอง
รายงานทั้งสองข้อถึง COO แล้วในจดหมาย `20260904_0140`

## ต้นรอบ (ตามลำดับที่กติกาบังคับ)

1. `NOW.md` อ่านก่อนทุกอย่าง
2. ล็อกรอบ: list PR สถานะ open ทั้งสองรีโป — ไม่มี `[LANE-A]` เปิดอยู่ (`#1037` เป็นของ LANE-GM ไม่ใช่ล็อกของผม)
   ⇒ ตัดกิ่งจาก `main`, commit `rounds/A_20260904_0122_yjjtyn_claim.md`, เปิด `pf_bridge#1038` (ไม่ draft, **ไม่มี marker**)
   list ซ้ำหลังเปิด: ไม่มีใบ `[LANE-A]` ที่เก่ากว่า ⇒ ถือล็อก
3. ชะตา PR รอบก่อน (ADDENDUM ข้อ A): `pf_bridge#1032` **merged=true** · `pirate-force-server#687` **merged=true**
   ⇒ ไม่มีงานหายจาก main ไม่ต้อง cherry-pick
4. กล่องจดหมาย: ไม่มีใบ `ADDRESSEE: LANE-A` ที่ยังไม่มี stub · `PANYA-DECISION 20260904_0125` ที่เข้ามาระหว่างรอบ
   จ่าหน้า COO (cc chief/LANE-B) ไม่ใช่ของสายนี้ ไม่แตะ
5. `pf-adversary` สั่งตั้งแต่ต้นรอบพร้อมเริ่มงาน ตามกฎ COO `0903_2345`

## สิ่งที่ทำ

**ปัญหา (วัดไว้แล้วโดยรอบ `zqmosn` ไม่ใช่ของใหม่):** ประตูคลิก NPC ของฉาก 1 (พอร์ตรอยัล) ปิดอยู่
เพราะ responder ที่ยึดตระกูล vital ของฉากจะ **กลืนคำตอบทั้งก้อนของลูปแช่แข็ง** และ `ChooseNpcResponse`
พกได้คู่เดียว ⇒ เปิดประตูวันนั้น = NPC ทั้งเมืองคุยไม่ได้ + ร้านค้าไม่เปิด
รายการ 7 ข้อในดอกสตริงของโมดูลเขียนข้อ 1 ไว้ว่า "`ChooseNpcResponse` ต้องกลายเป็น collection"

**ทำข้อ 1 และครึ่งของข้อ 2:**

- `src/pirateforce_foundation/lane_hooks/__init__.py`
  `ChooseNpcResponse` เพิ่มฟิลด์ `extra_actions: tuple[tuple[str, bytes, bytes, float], ...] = ()`
  **ดีฟอลต์ว่างคือข้อโต้แย้งเรื่องความปลอดภัยทั้งหมด** — responder เดิมสี่ตัว (ฉาก 2, 14, สิบฉากโรสเตอร์)
  และจุดเรียกใน `runtime.py` วันนี้ ความหมายไม่เปลี่ยน · ย่อหน้าในดอกสตริงระบุชัดว่า **ยังไม่มีใครอ่านฟิลด์นี้**
  และห้ามอ่านการมีอยู่ของฟิลด์ว่า "แอ็กชันถูกส่งแล้ว"
- `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene1.py`
  `_conversation_extra()` ประกอบทริกเกอร์คุยของลูปแช่แข็ง โดย **เรียก `legacy.make_npc_conversation_empty`**
  ไม่ใช่ก๊อปไบต์ และคง **ป้ายเดิม** `V98_NPC_CONVERSATION_DEFAULT_P<idx>`
  (เหตุผล: `GAME_TEST_QUEUE.md` grep สตริงนี้อยู่ 4 ครั้ง — กฎ grep ใน `AGENTS.md`)
  · สามตำแหน่งได้ `()` พร้อมเหตุผลของตัวเอง: ตัวเควส (`V129_QUEST_ACTOR_INDEX`) และตัวจุดร้าน
  (`V112_SHOP_TRIGGER_INDEX`) เป็น **once-per-session** ในลูปแช่แข็ง และ `respond()` ไม่ได้รับแลตช์ใด ๆ
  · ตัวมอน (`V112_MONSTER_INDEX`) ลูปแช่แข็ง `continue` ทิ้งไปเลย
  · fail closed สองทาง: อ่านค่าคงที่ของ v141 ไม่ได้ ⇒ ประกอบ **น้อยลง** ไม่ใช่มากขึ้น · ตัวประกอบ raise ⇒
  เสียแค่ extra ไม่เสียคำตอบ · บรรทัดคอนโซลรายงาน `extra=<n> extra_reason=<หนึ่งในสี่>` ทุกคลิก
  · `production_allowed` ของฉาก 1 **ยังเป็น False** (ยังขาดร้านค้า + บรรทัดของ chief + ข้อ 3-7)
- `tests/test_lane_a_choose_npc_scene1.py`: คลาสใหม่ `TheTalkTriggerRidesAlongAsAnExtraActionTests`
  (6 เทส) รวม **เทสมิวแทนต์** ที่สลับตัวประกอบแช่แข็งแล้วไบต์ต้องเปลี่ยนตาม (พิสูจน์ว่า derive จริง)
  · เทสเดิม `test_one_response_carries_one_frame_which_is_the_whole_blocker` **ขีดฆ่าถ้อยคำ ไม่ลบ**
  และแก้ให้ตรงกับความจริงใหม่ (ยังคู่เดียว แต่ "คู่เดียว" ไม่ใช่ตัวบล็อกทั้งหมดอีกแล้ว)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

🔴 **ยังไม่มี และเขียนไว้ตรง ๆ ทั้งใน PR และในโค้ด** — ประตูฉาก 1 ยังปิด และยังไม่มีใครอ่าน `extra_actions`
สิ่งที่ขยับคือ **ราคาที่วัดไว้ของการเปิดประตู** ลดจากสองแอ็กชันที่หาย เหลือหนึ่ง (ร้านค้าของ P91)
วันที่ผู้เล่นเห็นจริงคือวันที่ (ก) chief ต่อบรรทัดเดียว (ข) แลตช์ร้านค้าเข้าถึง responder ได้
(ค) ข้อ 3-7 ครบ แล้วประตูเปิด — ตอนนั้นคลิก NPC ทั้งเมืองพอร์ตรอยัลจะได้คำตอบ รวมถึงตัวที่วันนี้เงียบ

## CORE-REQUEST ถึง chief

`notes_to_chief/20260904_0137_LANE-A-CORE-REQUEST-CHIEF-one-line-queues-extra-actions.md`
บรรทัดเดียว: `actions.extend(...)` ต่อท้าย `actions = [(response.label, ...)]` ในกิ่ง responder (`runtime.py:9678` โดยประมาณ)

## pf-adversary

🔴 **`ADVERSARY_PENDING pirate-force-server#691`** — สั่งต้นรอบพร้อมเริ่มงานตามกฎ COO `0903_2345`
แต่ผลยังไม่คืนตอน push ⇒ push ตามเดิม ไม่ถือล็อกรอ (กฎเดียวกันบังคับไว้)
**รอบถัดไปของสาย A ต้องหยิบผลนี้เป็นงานแรก ก่อน claim** · ห้ามเขียนที่ใดว่า "ผ่าน adversary"
คำถามที่สั่งให้โจมตี: ฟิลด์ใหม่ inert จริงกับผู้อ่านเดิมทุกตัวหรือไม่ · การประกอบ extra ตรงกับลูปแช่แข็ง
ทุกตำแหน่งหรือไม่ (P30 · ตัวจุดร้าน · ตัวเควส · multi-select) · ป้ายที่เลือกทำให้ grep ของคิวตกศูนย์หรือไม่
· มีอะไรเป็น regression กับฉากที่ประตูเปิดอยู่แล้ว (2, 14, 3-11, 126, 130) หรือไม่

## เทส

- ระหว่างทำ: `pytest tests/test_lane_a_choose_npc_scene1.py` (27 passed) ·
  `tests/test_lane_hooks.py` + responder ฉาก 2/14/โรสเตอร์ (153 passed) ·
  `pytest tests/ -k "choose_npc or lane_hooks or face_frame or npc_interaction"` (277 passed)
- ชุดเต็ม: รันครั้งเดียวรอบนี้ บนต้นไม้ที่ merge `origin/main` แล้ว (already up to date) และเป็น commit สุดท้ายจริง
  **9178 passed, 327 skipped, 17662 subtests, 0 failed** (391 วินาที)

## สถานะ PR (ตามจริง ห้ามเขียนว่าเสร็จ)

- `pirate-force-server#691`: **เปิดแล้ว ไม่ draft · marker `PF-AUTOMERGE: v4` ยืนยันด้วย GET แล้วสองครั้ง (ตอนเปิด และหลัง PATCH body) · รอ gate-windows**
- `pf_bridge#1038`: claim PR ของรอบนี้ — เติม `PF-AUTOMERGE: v4` หลังไฟล์รอบนี้ push = ปลดล็อก
  ไม่รอ gate ไม่รอ merge

## จดหมายของรอบนี้

- `notes_to_chief/20260904_0137_LANE-A-CORE-REQUEST-CHIEF-one-line-queues-extra-actions.md`
- `notes_to_chief/20260904_0140_LANE-A-REPORT-COO-the-collection-half-landed-and-lane-a-has-no-unblocked-now-item.md`
  (รวมข้อเสนอสองข้อให้ COO: บรรทัด UI-B ใน `NOW.md` ไม่ใช่ของสาย A แล้ว · และ `GT-076` มีหัวใบบล็อก
  ที่เหตุบล็อกหมดอายุแล้ว — ผมไม่แตะหัวใบเอง เพราะไมล์สโตนถูกพักและเวลา attended แพงที่สุด)
