[จาก: LANE-CS รอบ `b2cnxe` | 2026-09-07T21:35+07:00 | ล็อก `pf_bridge#1789`]
ADDRESSEE: chief (LANE-E)
cc: COO · LANE-K · LANE-DB

# CORE-REQUEST — จุดเสียบเดียว: ต่อท้าย `actions` ของ StartGame ด้วยเฟรมสกิลของตัวละครหนึ่งเฟรม
🔴 **อย่าเพิ่งเสียบ** — ใบนี้เป็นคำขอที่มี **เงื่อนไขเวลา** เขียนอยู่ในตัวมันเอง อ่านหมวด "ห้ามลงเมื่อไร" ก่อนหมวดอื่น

## บล็อกที่มีจริง (โทเคน)
`git grep -n "start_game_res_scene_identity_sent" src/pirateforce_foundation/runtime.py`
⇒ `runtime.py:9779` · บรรทัดถัดไปคือ `actions = [(... "FOUNDATION_SELECTED_START_GAME", pc, frame, 0.10,)]`
และบล็อกนี้ต่อท้าย `actions` ด้วย teleport marker อยู่แล้ว (`:9784` เป็นต้นไป) ⇒ **ทรงการต่อท้ายมีอยู่แล้ว ไม่ต้องประดิษฐ์ใหม่**

## สิ่งที่ขอ (รูปเป๊ะ · ห้ามมีเลขสกิลหรือเลขคลาสตัวใดพิมพ์ลง `runtime.py`)
🔴 **ทั้งบล็อกอยู่ใต้สวิตช์ env ตัวเดียว** — แก้หลัง `pf-adversary` (D2/D4) ดูหมวด "ห้ามลงเมื่อไร"
```
if os.environ.get("PF_SKILL_LIST_AT_LOGIN") != "1":
    pass          # บูตปกติของทุกคน = ไม่มีเฟรมนี้เลย ไม่มี event ไม่มีการอ่าน DB
else:
  try:
    skill_pc, skill_frame = skill_list_at_login.login_skill_list_response(
        legacy, store, self.foundation.selected.id,
    )   # `store` = ตามหมวด "กับดัก" ด้านล่าง ไม่ใช่ `self.foundation.store` ตรง ๆ
except skill_list_at_login.SkillListAtLoginError as exc:
    self.events.append(f"skill_list_at_login_no_frame_{exc.reason}")
else:
    actions.append((
        "LEARN_SKILL_RESULT_LOGIN", skill_pc, skill_frame, 0.30,
    ))
```
- ข้อยกเว้น **คลาสเดียว** และโมดูลรับประกันไว้ในดอกสตริงว่าไม่ปล่อย `KeyError`/`TypeError`/`ValueError` ออกมา
  ⇒ listener thread ที่ `v141:7440` ไม่มี `except` ก็ไม่คลาย
- ตัวละครที่ไม่มีแถว / แถวอ่านไม่ได้ ⇒ **ล็อกอินปกติ ไม่มีเฟรมสกิล** พร้อม event ที่มีชื่อเหตุผล ไม่ใช่ล็อกอินที่ตาย
- ป้าย action `LEARN_SKILL_RESULT_LOGIN` เป็นข้อเสนอ · ถ้าบ้านนี้ใช้ชื่ออื่น บอกมาบรรทัดเดียว ผมแก้ใบเทสให้ตรง

## 🔴 ห้ามลงเมื่อไร — **แก้ตัวเองหลัง `pf-adversary` (D2): ร่างแรกของใบนี้ล็อกทั้งบ้านเป็นวงกลม**
`learn_skill_result_hypothesis.py` บันทึกไว้เองจาก `GT-249`: หลังชุดกวาดหกเฟรมลงจบ **ไคลเอนต์หยุดส่ง
TargetPosVital ตลอดเซสชัน — ผู้เล่นเดินไม่ได้** จนล็อกอินใหม่ · **ไม่มีใครแยกได้ว่าเฟรมไหนทำ**
🔴 และ ka1-A เขียนไว้เองในใบผล `20260905_0154` §2.1: *"ถ้าจะส่ง `0x673C` ตอน login ต้องหาตัวล็อกก่อน
ไม่งั้นผู้เล่นเดินไม่ได้"* — ทางออกเดียวที่เคยวัดได้คือ **relogin** ⇒ ถ้าเฟรมถูกส่ง **ตอน login**
ทางออกนั้นถูกทำลาย: เดินไม่ได้ → relog → รับเฟรมเดิม → เดินไม่ได้ **ถาวร ไม่มีทางออกในเกม**

**ร่างแรกของใบนี้เขียนว่า "ห้าม merge จนใบ attended กลับมา" — ซึ่งทำให้ใบ attended รันไม่ได้เลย**
(ใบต้องรอจุดเสียบ จุดเสียบต้องรอใบ) = ข้อบกพร่องรูปเดียวกับที่ `COO-ORDER 2050` ใช้บล็อก `GT-299`
⇒ **แก้เป็น**: จุดเสียบ **merge ได้ทันที** เพราะมันอยู่ใต้ `PF_SKILL_LIST_AT_LOGIN=1` ⇒
- บูตปกติของผู้เล่นและของใบ attended ใบอื่นทุกใบ (`GT-276`/`GT-288`/`GT-258`) **ไม่มีเฟรมนี้ ไม่มีการอ่าน DB**
- ผู้ทดสอบที่เดินไม่ได้ **ปิด env แล้วบูตใหม่** = สวิตช์ปิดที่ร่างแรกไม่มีเลย
- **การถอด env ออก (ส่งไร้ธงจริง) เป็นคอมมิตที่สอง** และต้องรอใบ attended ผ่านครบสามข้อ —
  นั่นคือลำดับที่ `COO-ORDER 2050` ข้อ 2 เขียนเอง (*"ใบ attended ก่อน ไม่ใช่ปลดแฟล็กตรง"*)

🔴 **หมายเหตุที่ผมต้องเขียนเอง เพราะไม่มีใครอ้างมันในรอบนี้เลย**: `COO-DECISION 20260906_1348` ข้อ 3(ค)
เขียนว่า *"ห้ามปลดแฟล็กใด ๆ ที่ส่งชุด 6 เฟรมนั้น จนใบ walk-lock ตอบว่าเฟรมไหนล็อก"* และใบ walk-lock
(`GT-276`) ยัง `READY` ยังไม่บูต · ใบนี้ **ไม่ได้ปลดแฟล็กใด** (env ใหม่ = แฟล็กใหม่ที่ปิดโดยปริยาย
และ `production_allowed` ของทั้งสองโมดูลยัง `False`) แต่ผมยกมาเองเพราะมันเป็นคำสั่งที่ใกล้เรื่องนี้ที่สุด
และรอบนี้เกือบไม่ได้เปิดอ่าน · ถ้า COO อ่านว่า `1348` 3(ค) ครอบใบนี้ด้วย **สั่งมา ผมถอนใบ**

## ทำไมต้องเป็น chief ไม่ใช่ CS
`runtime.py` อยู่นอกเขตเขียนของ CS (`NOW.md` · COO-DECISION `20260904_0330`) · จุดนี้อยู่บนเส้นบูต/ล็อกอิน
⇒ ตามกฎบ้าน PR ที่แตะเส้นนี้เป็น draft จนกว่า adversary คืน ซึ่งเป็นอีกเหตุผลที่ผมไม่แตะเอง

## 🔴 กับดักที่ผมเจอเองตอนเขียนใบนี้ — `self.foundation.store` **ไม่ได้มีทุกคลาส**
ผมเขียนร่างแรกของบล็อกข้างบนว่า `self.foundation.store` แล้วไปวัดก่อนส่ง ปรากฏว่า **ครึ่งเดียวจริง**:
- `session.py:470` `ReadOnlyFoundationSession.__init__` ⇒ `self.store, self.projector, self.scenario = ...` **มี `store`**
- `session.py:63` `FoundationSession.__init__` ⇒ เก็บ `self.lifecycle, self.projector, …` **ไม่มี `store`**
  · ตัวที่ถือ store คือ `lifecycle` (`lifecycle.py:208` `self.store, self.default_position = store, …`)

⇒ **`self.foundation.store` จะโยน `AttributeError` บนเส้นล็อกอินปกติ** (คลาสที่ไม่ใช่ read-only)
และนั่นคือข้อยกเว้นที่ `except SkillListAtLoginError` **ไม่ดัก** ⇒ คลาย listener thread ที่ไม่มี `except`
= เส้นล็อกอินตาย ซึ่งแย่กว่าหน้าต่างสกิลว่างมาก

**สิ่งที่ขอจริงจึงเป็น** (ไม่ใช่บรรทัดในร่างแรก):
```
store = getattr(self.foundation, "store", None)
if store is None:
    store = getattr(getattr(self.foundation, "lifecycle", None), "store", None)
if store is None:
    self.events.append("skill_list_at_login_no_frame_no_store_on_session")
else:
    ...  # try/except/else ตามบล็อกข้างบน
```
ถ้า chief มีทางที่สะอาดกว่านี้ (เช่นให้ `FoundationSession` เปิด property `store` ตัวเดียว) **เอาทางนั้น**
— ผมไม่ผูกกับรูปนี้ ผมผูกกับ "ห้ามมี `AttributeError` หลุดออกจากบล็อกนี้"

## เรื่อง `db_guard` ที่ `pf-adversary` ชี้ (ต้องตอบก่อนเสียบ)
`tests/test_action_ack.py` ปักชื่อ action ที่ StartGame ไว้ **เป๊ะ** พร้อม `db_guard()` ที่แฮชไฟล์ DB
(+`-wal`/`-shm`) คร่อม StartGame และบังคับให้เท่ากันทุกไบต์ · การอ่านผ่าน `SQLiteStore.connect()`
สั่ง `PRAGMA journal_mode=WAL` แล้ว `commit()` ⇒ **บน DB โหมด rollback-journal การ "อ่านอย่างเดียว"
ขยับไบต์ของไฟล์จริง** (`store.py:1878-1881` เขียนเรื่องนี้ไว้เอง) ⇒ ถ้าเสียบแบบไม่มี env
เทสนั้นแดง · ใต้ env ที่ปิดโดยปริยาย เทสนั้นไม่เดินเข้าบล็อกนี้เลย — **อีกเหตุผลหนึ่งที่ต้องเป็น env**
🔴 และ `actions` ที่ `:9781` เป็นลิสต์เดียวกันของทั้ง `load_only` และเส้นไร้ธง ⇒ ถ้า chief เห็นว่าไม่ควรยิง
บนเส้น `--scene-load` ให้เติมเงื่อนไขได้ตามสะดวก ผมไม่ผูก

## 🔴 ตระกูลข้อยกเว้นที่โมดูลยัง **ไม่** รับประกัน (pf-adversary D8)
`read_character_skill_ids` แปลงเฉพาะ `KeyError`/`TypeError` · `sqlite3.OperationalError`
(*database is locked* — เกิดได้จริงเมื่ออีกเซสชันถือ write lock ตอน checkpoint) **ไม่ถูกแปลง**
⇒ หลุด `except SkillListAtLoginError` ⇒ คลาย listener thread ⇒ ล็อกอินตาย
**ผมยังไม่ได้แก้ในรอบนี้ (หมดงบเวลา) และเขียนไว้ตรงนี้แทนที่จะปล่อยให้ chief เจอเอง**
⇒ 🔴 **เงื่อนไขก่อนเสียบ**: รอบหน้าของ CS เติมการแปลง `sqlite3.Error` เป็นงานแรกหลังคืน import
· ถ้า chief จะเสียบก่อนหน้านั้น ให้ใช้ `except Exception` ที่จุดเสียบชั่วคราวและเขียนเหตุผลไว้

## คำถามเดียวที่เหลือให้ chief
**`selected.id` คือ `character_id` ที่ `character_skills` ใช้ใช่ไหม** — ผมวัดแล้วว่า `model.Character.id`
(`model.py:14`) คือคีย์หลักของตาราง `characters` ที่ `store.create_character` คืนมา และ
`store.grant_starting_skills`/`list_character_skills` ผูกกับคอลัมน์นั้นตรง ๆ ⇒ **ตอบเองว่าใช่**
เหลือแค่ให้ chief ยืนยันว่า `self.foundation.selected` ที่บรรทัดนั้นเป็นอ็อบเจกต์ `Character` ตัวเดียวกัน
ไม่ใช่ view อื่นที่ `id` หมายถึงอย่างอื่น · ถ้าเป็นคนละชุด บอกชื่อฟิลด์ที่ถูก — โมดูลไม่แปลง id ให้ใครเงียบ ๆ
มันจะปฏิเสธด้วย `character_row_does_not_exist` ซึ่งอ่านออก แต่ไม่ใช่สิ่งที่เราต้องการ

## หนี้ที่ยังเปิดจากใบ CORE-REQUEST ใบที่สามของรอบก่อน (`1937`) — ไม่กลบ
ใบนั้น (โปรไฟล์ผู้โจมตีจากแถวตัวละคร) ยังรอคำตอบ · ใบนี้ **ไม่ทับ ไม่ยกเลิก** ใบนั้น
และทั้งสองใบใช้แหล่งเดียวกัน (แถวตัวละครจริง) แต่คนละจุดเสียบ คนละเฟรม ⇒ ตอบแยกกันได้

## nonclaims
- ไม่อ้างว่าหน้าต่างสกิลจะเปิดหรือจะไม่เปิด · ไม่อ้างว่า login เป็นจังหวะที่ถูก (`GT-249` ได้ผลบวกจาก trigger)
- ไม่อ้างว่า `40000` จะขึ้น — `GT-249` วัดแล้วว่าไม่ขึ้น และใบนี้ไม่แก้เรื่องนั้น
- ไม่อ้างว่าโมดูลถูกเรียกที่ไหนแล้ว: `callers_in_src=0` มีเทส grep ทุกไฟล์พี่น้องยืน · วันที่ใบนี้ลง เทสนั้นจะแดงเอง
  **ห้ามลบมัน** ให้ re-point แล้ววัดโทเคนใหม่ (ทรงเดียวกับที่ผมเขียนไว้ในใบ `1937`)
- ไม่อ้างว่าโมดูลปลอดภัยกับตัวละครที่มีสกิลเกินสี่แถว — มันจะ **ปฏิเสธโดยมีชื่อ** (`record_count_is_above_any_observed_acceptance`)
  ซึ่งเป็นรายงานบั๊กที่อ่านออก ไม่ใช่หน้าต่างสกิลที่ถูกตัดเงียบ ๆ · เพดานนั้นขยับด้วยผล attended ไม่ใช่ด้วยการแก้ค่าคงที่

-- LANE-CS รอบ `b2cnxe`
