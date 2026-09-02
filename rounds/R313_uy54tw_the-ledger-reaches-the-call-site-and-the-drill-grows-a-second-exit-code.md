# R313 · `uy54tw` · LANE-E (chief) · 2026-09-03T03:xx+07:00

**รอบนี้ขยับ NOW ข้อไหน:** `P-1` — บรรทัดเดียวที่ `COO-DECISION 20260903_0251` สั่งไว้เป็นงานแรกของ R313
(`mob_combat_ledger=` ที่จุดเรียก ChooseNPC `runtime.py:8800` + ลบคอมเมนต์ล้าสมัย + เทสผ่าน dispatcher จริง) **ทำครบ push แล้ว รอ merge**
และงานที่ 1 ของ `COO-DECISION 20260903_0149` (ปิดรูกติกาซ้อมเกต) ที่ R312 ไม่ได้ทำเพราะทั้งรอบหมดไปกับใบกู้ `main` แดง

**สิ่งที่ยังไม่ขยับ และเพราะอะไร:** `P-2` (สีชื่อมอน) ไม่แตะ — `NOW.md` ห้ามเปิด RE ใหม่จนมีผลจากเครื่องจริงและ P0-2 ขยับ ·
`COO 0054` (รวมตรรกะสามชื่อสองชุดให้เหลือชุดเดียว ชื่อ inline ชนะ) **ยังไม่ทำในรอบนี้** — เป็นใบแยกตามที่ `0054` เขียนเอง
และกฎขนาด PR หนึ่งเรื่องต่อใบบังคับให้ใบที่สองเปิดหลังใบแรก merge ⇒ **จองเป็นงานแรกของรอบหน้า** (รายละเอียดข้างล่าง)

---

## 1. `mob_combat_ledger` ถึงมือ responder แล้ว (`pirate-force-server`)

`runtime.py:8800` เดิมส่งอาร์กิวเมนต์หกตัวและมีคอมเมนต์ **35 บรรทัด** อธิบายว่าทำไมไม่ส่งตัวที่เจ็ด
คอมเมนต์นั้นบรรยายพฤติกรรม **ก่อน** `server#606` (การ์ดตายปฏิเสธทั้งคลิก) ว่าเป็นของปัจจุบัน ⇒ ใครมาอ่านก่อนตัดสินจะอ่านของเก่า

- ลง `mob_combat_ledger=getattr(self, "mob_combat_ledger", None)` แทน · คอมเมนต์เหลือ **8 บรรทัด** บอกสามอย่าง:
  ใบไหนปลด (`COO 0251` แทน `1945`) · ซากศพยังเงียบและใบของสาย A จะแก้ · ไฟล์เทสไหนหมุดมันไว้
- 🔴 **`getattr` ไม่ใช่ `self.mob_combat_ledger` ตรง ๆ ตามตัวอักษรของใบ `0251`** และนี่คือส่วนที่ผมเปลี่ยนเอง:
  ledger ถูกเปิดใน `try` ก้อนใหญ่ของ `__init__` (`runtime.py:1037-1401`) ⇒ เซสชันที่พลาดตรงนั้นจะไม่มีแอตทริบิวต์เลย
  และจุดเรียกนี้จะกลายเป็น `AttributeError` ทุกคลิกแทนที่จะประกอบที่เพดานเหมือนบูตที่ไม่มี ledger ·
  `runtime.py:5885` ใช้ `getattr` ที่ ledger ตัวเดียวกันด้วยเหตุผลเดียวกันอยู่แล้ว ⇒ ตามสำนวนของไฟล์ ไม่ใช่การประดิษฐ์ใหม่

### เทสที่พิสูจน์ว่าคีย์เวิร์ดอยู่ "ที่จุดเรียก" ไม่ใช่แค่ "responder รับได้"

ไฟล์ใหม่ `tests/test_choose_npc_call_site_ledger.py` (4 เทส) ยิงเฟรมจริงผ่าน `state.dispatch` ทั้งหมด — ไม่มีการยื่น ledger ด้วยมือ
(ไฟล์ของสาย A `tests/test_lane_a_click_after_a_kill.py` ยื่นด้วยมือ **โดยเจตนา** และเขียนไว้ใน docstring ว่าเพราะจุดเรียกยังไม่ส่ง)

| เทส | สิ่งที่ปัก |
| --- | --- |
| `..._still_puts_bytes_on_the_wire` | ฆ่ามอนหนึ่งตัวในฉาก 2 แล้วคลิกชาวเมือง ⇒ ได้ action `LANE_A_CHOOSE_NPC_SCENE2_FACE_P<n>` พร้อม pc และ frame ไม่ว่าง |
| `..._proves_the_session_ledger_reached_the_responder` | คอนโซลพิมพ์ `dead_at_ceiling=1` — เป็นไปได้ก็ต่อเมื่อ ledger **ที่รู้เรื่องการฆ่า** มาถึง |
| `..._corpse_is_refused_by_name_and_not_by_silence` | คลิกซากศพ ⇒ ไม่มี action แต่มี `_IDENTITY_REFUSED reason=clicked_body_is_dead_needs_a_mob_death_body placement=<n>` |
| `..._before_any_kill_is_answered_at_the_ceiling` | คอนโทรล: เซสชันที่ไม่มีการรบเลย ⇒ `dead_at_ceiling=0` ⇒ เทสข้างบนอ่าน "การฆ่า" ไม่ใช่ "มี ledger" |

**มิวแทนต์ [วัดแล้ว]:** ลบบรรทัด `mob_combat_ledger=` ออกจาก `runtime.py` ⇒ **2 failed 2 passed** (ตัวที่แดงคือสองตัวที่ต้องแดง)
คืนกลับ ⇒ **4 passed** · ก่อนรอบนี้ ไม่มีอะไรในรีโปเลยที่จะสังเกตการลบบรรทัดนี้ได้

### ตัวเลขที่เปลี่ยนบนคอนโซล และใบเทสที่ต้องรู้

วัดผ่าน dispatcher จริงในรอบนี้ คลิกชาวเมือง placement 0 ฉาก 2:

    ไม่ฆ่าอะไรเลย : ... visible=97 hostile=12 hp=ledger from_ledger=12 wounded=0 dead_at_ceiling=0
    ฆ่าหนึ่งตัว   : ... visible=97 hostile=12 hp=ledger from_ledger=11 wounded=0 dead_at_ceiling=1

⇒ `GT-214` ข้อ (ข) ปักไว้ว่า `hp=ceiling from_ledger=0` ⇒ **กลายเป็นสตริงเก่าทันทีที่ใบนี้ merge แม้ผู้เทสไม่ได้ฆ่าอะไร**
ใบนั้นเป็นของสาย A ผมแตะไม่ได้ ⇒ ส่งจดหมาย `20260903_0300_CHIEF-TO-LANE-A-gt214-token-line-changes-when-the-ledger-lands.md`
พร้อมสตริงใหม่ทั้งบรรทัด และเตือนว่า **ข้อ 10 (`S02-HP-AFTER`) เปลี่ยนคำทำนาย** ด้วย (แถบ HP อาจยังพร่อง = สิ่งที่ CORE-REQUEST ขอ ไม่ใช่ FAIL)
🔴 `hp=ledger from_ledger=12` **ยกเป็นหลักฐานว่า HP มาจาก ledger ไม่ได้** (`COO 1945` ข้อ 4.3) — ช่องที่ยกได้คือ `wounded=` เท่านั้น

## 2. รูของกติกาซ้อมเกตปิดแล้ว (`pf_bridge` · `AGENTS.md`)

`COO 0149` ข้อ 2: LANE-GM ซ้อมครบตามถ้อยคำเดิมแล้วยังตายที่ `#611` เพราะการซ้อมนั้นเป็น **pytest ไม่ใช่ census** — สอง exit code คนละตัว

- เงื่อนไขเปลี่ยนจาก "เพิ่มไฟล์เทสใหม่" เป็น **"เพิ่มไฟล์เทสใหม่ *หรือเพิ่ม skip ใหม่*"**
- ต้องได้ `exit 0` **ทั้งสองช่อง**: `pytest_subset` และ `skip_census` · บล็อกคำสั่งติดป้ายชื่อช่องให้ทั้งสองบรรทัด
  และเตือนสองอย่างที่ทำให้ซ้อมแล้วไม่เจอ: อ่าน `$?` ของทั้งสองบรรทัด และ `log.txt` ต้องมาจาก pytest ที่ใส่ `-rs`
- ทางแก้ที่อนุญาตมีสองทางเท่านั้น (precondition ใน `tests/pf_preconditions.py` หรือหมุดใน `docs/PYTEST_SKIP_PINS.json` → `design_skips`)
  · **ห้ามอ่อนตัว census ลง** ยกจากใบ `0149` ตรงตัว

**และรอบนี้เดินตามกติกาใหม่นั้นเอง** (รอบนี้เพิ่มไฟล์เทสใหม่หนึ่งไฟล์) — worktree แยก ไม่มี `pf_bridge` ข้าง ๆ:

    pytest_subset : 7218 passed, 74 skipped, 14273 subtests, 287.91s   exit 0
    skip_census   : "every skip is declared, named and pinned" RESULT: PASS   exit 0

## 3. งานคิวและกล่องจดหมาย

- `GT-215` (ใบของผมเอง) **`BLOCKED` → `🟢 READY`**: RECHECK ทั้งสองข้อผ่าน วัดเองบน `origin/main` `425150aa`
  (`new_character_vitals()` 5 hit ใน `store.py` · `tests/test_persistence_vitals_seed_007.py` 49 passed) — `server#595` merge ไปแล้ว
- `RE-169` (ใบของผมเอง) **ปิด** ตามที่ใบผลของ RE runner ขอ: `OpenCloseUI` มีแขนงปิดจริง ชื่อ UI ที่ `+0x14`,
  ไบต์ `+0x30` เป็นตัวสลับ (ค่าตั้งต้น `1` ⇒ คำสั่งปิดต้องส่งศูนย์), ชื่อเป้าหมายคือ `Quest_NPC_Conversation_New`/`Quest_NPC_Conversation`
  · 🔴 **numeric opcode ยัง `NOT_OBSERVED`** ⇒ ข้อห้ามต่อ production call site ยังยืนทุกตัวอักษร · handler คืน `AL=1` เสมอ = รับ dispatch ไม่ใช่ปิดสำเร็จ
- บริโภคจดหมาย 4 ใบพร้อม stub: `0149` · `0251` · `0152` (LANE-B ถอนบรรทัด `scene=` ของตัวเอง — ไม่มีอะไรให้ chief ต่อ) · `0204` (ผล RE-169)
  · ใบ `0210` สองใบเป็นของ LANE-A/LANE-DB · `0148` เป็นของ LANE-GM ⇒ ไม่ใช่ของผม ไม่ stub

## WIRED

`WIRED = 10/10` โมดูลเลนที่ `runtime.py`/`app.py` เห็น — ตัวเลขนี้ **ไม่ได้วัดใหม่ในรอบนี้** และตามนิยาม WIRED v2
มันคือจำนวน import ไม่ใช่จำนวน emission บน production path ⇒ ห้ามอ่านเป็นความคืบหน้า
สิ่งที่รอบนี้เพิ่ม **จริง** คือหนึ่งอาร์กิวเมนต์บน emission path ที่มีอยู่แล้ว (`scene_choose_npc_responder`)

## สิ่งที่ยังไม่พิสูจน์

- **ไม่มีอะไรบนจอ** ทั้งรอบเป็นชั้น wire/console บนคลาวด์ ไม่มี `OBSERVER_CONFIRMED` ไม่มีเฟรมจากเครื่องจริง
- เขียว(cloud sanity) และ เขียว(ซ้อมทรงเกต บน worktree ที่ไม่มี `pf_bridge`) **ไม่ใช่** เขียว(gate เต็ม บนสะพาน)
  คลาวด์คือ Linux + 3.11 เกตคือ Windows + 3.14.7 — R312 ทั้งรอบคือหลักฐานว่าสองเครื่องนี้ไม่เหมือนกัน
- ซากศพยัง **ไม่ตอบด้วย body** คลิกร่างที่ตายแล้วยังได้ศูนย์ไบต์ (มีชื่อ ไม่เงียบ) — ใบของสาย A
- ยังไม่ได้วัดว่าฉากอื่นที่ลงทะเบียน responder (1, 3, 14, roster islands) ได้ประโยชน์หรือเสียหายจาก ledger ที่ส่งไปด้วย
  นอกจากที่ pf-adversary ตรวจให้ในรอบนี้

## งานแรกของรอบหน้า (จองไว้)

`COO 0054`: ตรรกะสามชื่อมีสองชุดบน `main` — inline ที่ `runtime.py:7449-7488` (ชื่อที่ `GT-204` อ่าน:
`superseded_by_pickup` / `last_object_pickup` / `publication_refused`) กับ `mob_loot.boundary_stash_dropped_event`
(`BOUNDARY_STASH_*_EVENT` คนละคำ ยังไม่มีใครเรียก) ⇒ รวมเหลือชุดเดียว **ชื่อ inline ชนะ** เป็นใบแยกใบเล็ก
🔴 ค่าคงที่อยู่ใน `mob_loot.py` ซึ่งเป็นคำศัพท์ของสาย B ⇒ ก่อนแก้ต้องอ่านเทสของเลนนั้นและเขียนใบถึงเจ้าของการ์ดตาม `COO 0053` กฎ ข.

🔴 สถานะ: push แล้ว รอ merge — ยังไม่อยู่บน `main` จนกว่ารอบถัดไปวัดด้วย `git merge-base --is-ancestor`
