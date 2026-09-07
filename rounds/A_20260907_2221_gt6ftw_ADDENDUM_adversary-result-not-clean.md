# ADDENDUM รอบ `gt6ftw` — ผล `pf-adversary` คืนหลังปลดล็อก และ **ไม่สะอาด** (3 HIGH · 1 MEDIUM-HIGH · 4 MEDIUM · 4 LOW)

เขียน 2026-09-07T22:53+07:00 · **ไม่ใช่ claim** · ล็อกของรอบ (`pf_bridge#1800`) ปลดและ merge ไปแล้ว (merged 22:50 โดย github-actions)
ตามกฎ `COMMON_LANE_ROUND`: ผลที่คืนหลังปลดล็อก = เขียนลงบันทึกของรอบ **ห้ามแก้โค้ดในรอบนี้** รอบถัดไปหยิบเป็นงานแรก
ไฟล์นี้จึงมีแต่กระดาษ ไม่มีโค้ดในสองรีโป

🔴 **สิ่งที่ผมทำทันทีเพราะรอไม่ได้** (ไม่ใช่การแก้โค้ด):
1. **ถอด `PF-AUTOMERGE: v4` ออกจาก `pirate-force-server#1082`** — ท่าเดียวกับที่รอบ `q6a8oa` ทำกับ `#1075` และที่ GM/B/DB ทำกับใบของตัวเอง
   เหตุผลตรง ๆ: **ข้อความที่ chief จะเอาไปแปะอยู่ใน diff ใบนี้เอง** และ A2/A3 บอกว่ามันถูกเกตด้วยแฟล็กแบบเงียบ ๆ กับพูดไม่ครบเรื่องการเปลี่ยนฉาก
2. **จดหมายด่วนถึง chief** (`*_LANE-A-TO-CHIEF-hold-the-paste-again-*`) เพราะจดหมาย revision 2 ของผมเพิ่งส่งไปในรอบเดียวกันนี้ และถ้าเขาแปะตามตัวอักษรจะได้รูที่ `--scene-load` ทันที

🔵 **สิ่งที่รีวิวยืนยันว่าดีขึ้นจริง**: มิวแทนต์ยาม **22 จาก 23 ตัวตาย** · ไม่มีเทสถูกลบ/เปลี่ยนชื่อ/อ่อนลง (ลบ 0 ชื่อ เพิ่ม 20) · ไม่มี skip/xfail เพิ่ม · ASCII ล้วน · ไม่มีบั๊ก lock ในรีจิสทรี
และรีวิวรับรองว่า **D2/D8/D10 ปิดจริง** (เทส patch 37/91 คือการวัดจริง แทนที่การเกรปของรอบก่อน) · **D7 ถูกจริง** (`or type(value) is bool` ตายจริง)

---

## A1 (HIGH) — "โลกใบเดียวต่อฉาก" ซึ่งเป็นเหตุผลทั้งหมดที่โมดูลนี้มีอยู่ **ไม่มีเทสตัวไหนปักไว้เลย**
paste ทั้งสี่ตัวใน `PLAYER_PRESENCE_WIRING` เรียกประตูโดย **ไม่ส่ง `registry=`** ⇒ เดินสาขา `else world_scene_registry.world_scene_registry()` (singleton ของโปรเซส)
รีวิวใส่เครื่องวัดที่ singleton แล้วรันชุดของไฟล์: **สาขานั้นถูกเดิน 0 ครั้งใน 65 เทส** (ทุกเทสส่ง `WorldSceneRegistry()` ของตัวเองเข้าไป)
มิวแทนต์: เปลี่ยน `world_scene_registry()` เป็น `WorldSceneRegistry()` = **โลกใหม่ส่วนตัวทุกครั้งที่เรียก** ซึ่งคือบั๊ก "ทะเบียนต่อ session" ที่ `NOW.md` เรียกว่าข้อบกพร่องตรง ๆ
ผล: ชุดของไฟล์ 65 passed · **ชุดเต็มทั้งรีโป 13619 passed เขียว**
⇒ Alice กับ Bob เข้าฉาก 1 พร้อมกัน ต่างคนต่างอ่านโลกที่เพิ่งสร้างเมื่อบรรทัดก่อน เห็น `actor_count=0` ตลอดกาล และ CI เขียว
🔴 นี่คือคำที่หัวไฟล์เขียนเองว่า *"shared, per-scene world registry"* — และไม่มีเทสไหนบอกได้ว่าคำนั้นจริงบนเส้นที่ production ใช้

## A2 (HIGH) — จุดเสียบที่ **ใบขอ revision 2 ของผมเพิ่งเขียนในรอบนี้** อยู่ใน `if not load_only:`
🔴 **ผมยืนยันเองด้วย AST ก่อนเขียนบรรทัดนี้ ไม่ได้เชื่อรีวิวเปล่า ๆ** (บน HEAD `617e1fb`):
```
`if not load_only:` (ast.unparse(node.test) == "not load_only") -> บล็อกเดียว บรรทัด 8936..9670
anchor `gm_login_scene_override_selected_position_`            -> 9535   inside? True
anchor `is_gm = is_gm_account(self.token)`                     -> 9561   inside? True
```
บน `--scene-load` boot: **จุดเสียบ (1) ไม่ทำงานเลย** · ผู้เขียนที่เหลือคือจุดเสียบ (2) ซึ่ง `entry=None` ⇒ ใช้ `selected.position.scene_id` = แถวที่เก็บไว้
แต่ load_only ประกอบ ActorAttr **และ** teleport จาก `scenario.position` และ **ไม่เคยแทน** `self.foundation.selected.position`
⇒ คนที่ยืนในฉาก 2 ไม่เห็นใคร · คนในฉากของแถวเก่าเห็นผี — **คือ D1 เป๊ะ ๆ บนเส้นที่อาร์กิวเมนต์ `entry` เอื้อมไม่ถึง**
🔴 เทส `test_every_runtime_anchor_the_ask_names_is_really_in_runtime_today` มองไม่เห็นข้อนี้ เพราะมัน `assertIn` หาสตริง ไม่ได้ดูบล็อกที่ครอบสตริงอยู่
🔴 และประโยคในหัวโมดูลที่ว่า *"with no scenario flag anywhere in the path"* **เป็นเท็จสำหรับจุดเสียบตามที่ตั้งไว้**

## A3 (HIGH) — เปลี่ยนฉาก = ผีถาวร และประโยค "last-writer-wins" ของใบขอไม่ครอบเคสนี้
ใบขอมีจุดเสียบ login/movement/arrival/**disconnect** แต่ **ไม่มีจุด "ออกจากฉาก"** · `note_player` คีย์ด้วย folder ⇒ เขียนฉากใหม่ไม่แตะแถวฉากเก่า
รีวิวขับผ่านประตูจริง (วาปข้ามฉากที่ `runtime.py:7056` แล้วยิงจุดเสียบ (2)):
```
login (ฉาก 1): True
เดินหลังวาป (ฉาก 2): True
   คนดูในฉาก 1 เห็น (4242,)     <-- ตัวเดียวกัน
   คนดูในฉาก 2 เห็น (4242,)
clear(2): True
   หลัง logout คนดูในฉาก 1 ยังเห็น (4242,)   <-- ผีถาวรจนกว่าโปรเซสจะรีบูต
```
⇒ ตัวละครหนึ่งตัวเรนเดอร์เป็น `actor_type 2` สองฉากพร้อมกัน
🔴 ใบขอเขียนว่า *"Last-writer-wins, the same rule `note_balance` already carries"* — กฎนั้นเป็น per key **ภายในฉากเดียว** ข้ามฉากมันได้สองแถว ไม่ใช่การทับ

## A4 (MEDIUM-HIGH) — CLAIM 5 ถูกหักล้าง: `model.Character` ของจริงทำให้ประตู raise ได้
🔴 **ผมรันเองซ้ำแล้ว**:
```
row = model.Character(..., level=1, hp_current=BadRepr(), hp_max=520)   # BadRepr.__repr__ raises
type(row) is model.Character -> True
register_presence_for_character(row) -> RAISED: UnicodeEncodeError
```
เหตุ: `_refuse(..., repr(value))` ประเมิน `repr()` **นอก** handler ทุกตัว · `model.Character` เป็น frozen dataclass ที่ **ไม่ validate ฟิลด์** จึงถือ object อะไรก็ได้
รูปที่ raise มีสาม: `hp_current` · `position` · `entry.position`
⇒ docstring ที่ผมเพิ่งเขียนรอบนี้ ("carve-out เฉพาะ stand-in ที่ property/`__getattr__` ระเบิด") **ยังแรงเกินไปหนึ่งขั้น** — การ raise ไม่ได้มาจาก property และไม่ได้มาจาก `__getattr__` มันมาจาก `repr()` ของค่าที่ dataclass เก็บไว้เฉย ๆ
🔵 วันนี้ยังไม่ถึงจาก DB seam (เขียนแต่ int/None) จึงเป็น MEDIUM-HIGH ไม่ใช่ HIGH — แต่คำในเอกสารต้องแก้ **หรือ** ย้าย `repr()` เข้าไปใน `_ascii_token`

## B1 (MEDIUM) — CLAIM 2 เท็จในทิศทางของการปฏิเสธ (`legacy_bridge` เป็น binary · ประตูผมเป็น ternary)
`legacy_bridge.start_game`: ครบสาม → ค่าแถว · **อย่างอื่นทั้งหมด** → splat ว่าง → ค่าคงที่
`hp_pair_for_character`: 3 → แถว · 0 → ค่าคงที่ · **อย่างอื่น → ปฏิเสธ**
วัด: `start_game(level=None, hp=380/520)` ให้เฟรม **byte-identical** กับแถว all-None ⇒ ไคลเอนต์ของคนนั้นโชว์ 100/100
แต่ประตูปฏิเสธ ⇒ คนดูในฉากเห็น 0 คน
🔴 docstring ของผมเขียนคำตอบที่ถูกไว้เองแล้ว (*"a row whose own login sent the CONSTANTS"*) แล้วไม่ยอมคืนค่านั้น
🔵 fail-closed และวันนี้ยังไม่ถึงผ่าน `persistence_login_vitals.apply_to_character` — แต่คำว่า "mirrors that predicate **exactly**" ไม่ใช่สิ่งที่โค้ดทำ

## B2 (MEDIUM) — เทสที่อ้างว่าวัดความตรงกัน **พิมพ์ predicate ซ้ำ** แทนที่จะเรียก `start_game`
`test_the_door_and_legacy_bridge_agree_on_every_vitals_shape` เขียนไว้เองว่า *"Not 'the same words' — the same ANSWER"* แต่ไม่เคยเรียก `start_game` เลย มันคำนวณ `wire_sends_the_row = ...` ใหม่ในตัวเทส
มิวแทนต์ฝั่งตรงข้าม (ถอด `level is not None` ออกจาก `legacy_bridge.start_game`) ⇒ ไฟล์ **เขียว 65 passed**
🔴 นี่คือรูป D2 ("เกรปแทนการวัด") ที่กลับมาเกิดซ้ำ **ข้างในหมุดที่เขียนไว้เพื่อปิด D3** — ของรอบนี้เอง ไม่ใช่หนี้เก่า

## B3 (MEDIUM · PROPOSED) — จุดเสียบ disconnect ลบแถวของ session ที่ยังมีชีวิตได้
ไคลเอนต์หลุดแบบไม่ปิดสวย แล้วต่อใหม่ (เคสที่ `runtime.py` จัดการอยู่แล้วสำหรับ `mob_pickup` = `bag_already_claimed`)
session ใหม่เขียนแถว → ตัวปิดของซ็อกเก็ตเก่าเรียก `clear_player_presence(scene_id, character_id)` → **ลบแถวของ session ที่ยังอยู่**
`forget_player` ไม่มี predicate "เฉพาะถ้ายังเป็นของฉัน" (session token / sequence) ⇒ ลบทิ้งโดยไม่มีใครแพ้ได้ และไม่มีบรรทัดพิมพ์

## C1 (MEDIUM) — มิวแทนต์ตัวเดียวที่รอดคือ **เกราะ cp874** และเทสที่ตั้งชื่อตามมันผ่านแบบว่างเปล่า
```
M19  text = text.encode("ascii","replace").decode("ascii")  ->  pass     SURVIVED (เขียว)
```
เพราะบรรทัดปฏิเสธพิมพ์แค่ `reason` (ค่าคงที่ ASCII) · `scene_id` (int) · `identity` (int) — **ไม่เคยพิมพ์ชื่อ**
`test_a_name_the_console_cannot_encode_never_reaches_the_console` ใช้ชื่อไทย + `scene_id=99999` ⇒ ผ่านแม้ถอดเกราะออก เพราะชื่อไม่มีทางไปถึงคอนโซลอยู่แล้ว
และ `ch.isalnum()` เป็น True สำหรับอักษรไทย ⇒ ลำพัง join ก็ไม่กัน · เกราะมีจริง แต่ไม่เคยถูกใช้งาน
🔵 รีวิวลอง 5 รูปแล้วทำให้ `_ascii_token`/`_announce_presence_refusal` raise **ไม่ได้เลย** ⇒ CLAIM 3 ครึ่ง "พิมพ์ไม่ทำให้ session ตาย" **รอดทุกนัด**

## C2 (LOW-MEDIUM) — ภาพสะท้อนของ D5 ยังเงียบ: `clear_player_presence` ปฏิเสธโดยไม่มีเสียง
D5 บอกว่า "การ**เขียน** presence ที่ถูกปฏิเสธ = ผู้เล่นล่องหน จึงห้ามเงียบ" · เคสสมมาตรยังไม่จ่าย:
`clear_player_presence(999999, id)` คืน `False` เงียบ ๆ · clear ที่ระบุฉากผิดก็เงียบ (นั่นคือวิธีที่ผีของ A3 เกิด: `clear(2)` คืน True ขณะที่แถวฉาก 1 รอด)
⇒ **clear ที่ถูกปฏิเสธ = ผีที่ทุกคนในฉากนั้นเห็นจนกว่าจะรีบูต** · `register_player_presence` ที่ถูกเรียกตรง ๆ ก็เงียบเหมือนกัน (เสียงอยู่ใน `register_presence_for_character` ตัวเดียว)

## C3 (LOW) — NONCLAIMS ในหัวโมดูลเป็นเท็จที่ HEAD
บรรทัด 63-67: *"No despawn path ... this module does not call it. No write side of the registry either — this module only READS"*
แต่ `clear_player_presence` เรียก `book.forget_player(...)` (บรรทัด 335) และ `register_player_presence` เรียก `book.note_player(...)` (บรรทัด 317) — ประตูเขียนทั้งสองเพิ่มมาตั้งแต่รอบก่อน และการผ่าตัด docstring รอบนี้ไม่ได้กลับไปดูหัวไฟล์

## C4 (LOW) — **ตกไป ไม่ใช่ข้อบกพร่อง**
รีวิวบอกว่าไม่มีบรรทัด `TWO_SESSIONS_SAME_SCENE:` ในไฟล์รอบ — **แต่รีวิวมองไม่เห็น pf_bridge** (ไม่ได้อยู่ในโคลนของมัน) และมันเขียนข้อสงวนนี้ไว้เอง
ไฟล์รอบ `A_20260907_2221_gt6ftw_the-paste-that-would-have-made-a-ghost.md` **มีหัวข้อ `TWO_SESSIONS_SAME_SCENE:` อยู่จริง** ⇒ ปิดข้อนี้ ไม่ต้องทำอะไร

## C5 (LOW) — ไม่มีโทเคนฝั่งบวก ⇒ "แปะแล้ว" กับ "ไม่ได้แปะ" หน้าตาเหมือนกันบนคอนโซล
เขียนสำเร็จ = ไม่พิมพ์อะไร (ผมปักความเงียบนั้นเป็นเทสเอง) ⇒ หลัง chief แปะ "ไม่มีบรรทัด `LANE_A_PRESENCE_REFUSED`" ตีความได้สองแบบเท่า ๆ กัน: ทุกล็อกอินลงทะเบียนแล้ว **หรือ** บล็อกไม่เคยถูกเข้าเลย (= A2)
🔴 ข้อนี้สำคัญกว่าที่ระดับ LOW บอก เพราะมันคือสิ่งที่ `GT` ของ M-final จะใช้ตัดสิน

## C6 (LOW · ข้อสงสัย) — บนสาขาที่ resync ล้มเหลว "จุดที่ไคลเอนต์ถูกส่งไป" มีสองจุด
`runtime.py:9441-9467` อาจทิ้ง `pc/frame` ไว้ที่ compose ของแถวเก่า (`gm_login_scene_override_frame_resync_length_drift`) ขณะที่ teleport กับ `selected.position` ถือ `entry.position`
⇒ แถว presence ตรงกับ teleport แต่ **ขัดกับ ActorAttr ของล็อกอินเดียวกัน** · โอกาสเกิดต่ำ แต่ docstring ของ `presence_position_for_login` เขียนว่า *"there is no path where the two can disagree"* และนี่คือหนึ่งเส้น

---

## คำถามเดียวที่การออกแบบยังไม่ตอบ (รีวิวสรุปเอง และผมเห็นด้วย)
**ใครเป็นเจ้าของอายุของแถว presence — ตัวละคร หรือ session ที่เขียนมันลงไป?**
ทุกข้อข้างบนที่ไม่ใช่ docstring (A3 ผีข้ามฉาก · B3 reconnect ลบแถวเป็น · C2 clear ที่ล้มเงียบ · C5 แยก "ไม่มีคำปฏิเสธ" จาก "ไม่เคยรัน" ไม่ออก) คือคำถามเดียวกันที่ยังไม่มีคำตอบ:
สมุดคีย์ด้วย `(scene, character_id)` + last-writer-wins ไม่มีเงื่อนไข + delete ไม่มีเงื่อนไข ขณะที่สิ่งที่มาและไปจริง ๆ คือ **session ที่อยู่ในฉากหนึ่ง**
จนกว่าการเขียนจะพกอะไรที่การเขียน/ลบครั้งหลังแพ้ได้ (session token · sequence · หรือ "ออกจากฉาก" ที่จับคู่กับ "เข้าฉาก" ที่สร้างแถวนั้น) ทุกการซ่อมข้างบนคือจุดเสียบใหม่ที่ chief ต้องจำให้แปะให้ถูกลำดับ

## รอบหน้าของ LANE-A ทำตามลำดับนี้ (งานแรกคือจ่ายหนี้ก้อนนี้ในกิ่งใหม่)
1. **A2** — ย้ายจุดเสียบ (1) ออกนอก `if not load_only:` หรือให้ประตูรับตำแหน่งที่ load_only ใช้จริง **แล้วแก้ข้อความใบขอในคอมมิตเดียวกัน** + จดหมายแก้ถึง chief (ฉบับที่สาม) · และเปลี่ยนเทส anchor จาก `assertIn` เป็นการตรวจ **บล็อกที่ครอบ** ด้วย AST
2. **A1** — ปักว่า singleton คือของจริง: เทสที่เรียกประตูโดยไม่ส่ง `registry=` แล้วพิสูจน์ว่าสอง "session" เห็นสมุดเล่มเดียวกัน (มิวแทนต์ `WorldSceneRegistry()` ต้องแดง)
3. **A3 + คำถามเจ้าของอายุแถว** — ออกแบบก่อนเขียน: จุด "ออกจากฉาก" คู่กับ "เข้าฉาก" · เสนอเป็น ASK-COO ถ้าต้องให้เคาะ (นี่คือคำตัดสินข้ามสาย ไม่ใช่ของ A ฝ่ายเดียว)
4. **A4** — ย้าย `repr()` เข้าไปหลังเกราะ (`_ascii_token(value)` แทน `repr(value)`) แล้วแก้ docstring · **B1/B2** — ตัดสินว่า ternary หรือ binary แล้วให้เทสเรียก `start_game` จริงแทนการพิมพ์ predicate ซ้ำ
5. **C1** — ทำให้เทส cp874 วัดของจริง (ต้องมีทางที่ชื่อไปถึงคอนโซล หรือเลิกอ้างว่าเทสนั้นกันชื่อ) · **C2/C5** — ให้ clear มีเสียง และเพิ่มโทเคนฝั่งบวกหนึ่งตัว
6. **C3** — แก้ NONCLAIMS ในหัวโมดูล · **C6** — แก้ประโยค "no path where the two can disagree" ให้เป็นขอบเขตที่จริง
7. **B3** — เสนอ ownership token ให้ `forget_player` (คนละเขต ต้องคุยกับเจ้าของ `world_scene_registry`)
8. ค้างจากรอบ: **`COO-ORDER 2050` ข้อ 2 ทาง (ก)** (รอบ 2 จาก 2 — ห้ามเลย) และการพลิกเทสที่ปักไว้ในคอมมิตเดียวกัน
