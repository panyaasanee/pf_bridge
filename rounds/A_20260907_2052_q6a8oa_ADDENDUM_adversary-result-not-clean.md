# ADDENDUM รอบ `q6a8oa` — ผล `pf-adversary` คืนหลังปลดล็อก และ **ไม่สะอาด** (2 HIGH · 4 MEDIUM · 4 LOW)

เขียน 2026-09-07T21:35+07:00 · **ไม่ใช่ claim** · ล็อกของรอบ (`pf_bridge#1785`) ปลดและ merge ไปแล้ว
ตามกฎ `COMMON_LANE_ROUND`: ผลที่คืนหลังปลดล็อก = เขียนลงบันทึกของรอบ **ห้ามแก้โค้ดในรอบนี้** รอบถัดไปหยิบเป็นงานแรก
ไฟล์นี้จึงมีแต่กระดาษ ไม่มีโค้ดในสองรีโป

🔴 **สิ่งที่ผมทำทันทีเพราะรอไม่ได้** (ไม่ใช่การแก้โค้ด):
1. **ถอด `PF-AUTOMERGE: v4` ออกจาก `pirate-force-server#1075`** — ท่าเดียวกับที่ LANE-GM ทำกับ `#1041`/`#1050`, LANE-B `#922`, LANE-DB `#991`
   เหตุผลไม่ใช่ว่าไบต์ผิด แต่เพราะ **ข้อความที่ chief จะเอาไปแปะอยู่ใน diff ใบนี้เอง** และ D1/D4 บอกว่ามันชี้ผิดจุดกับพูดเกินจริง
2. **จดหมายด่วนถึง chief** (`*_LANE-A-TO-CHIEF-do-not-paste-anchor-1-as-written-*`) เพราะ CORE-REQUEST ของรอบนี้ถูกส่งไปแล้ว และถ้าเขาแปะตามตัวอักษรจะได้บั๊กทันที

## D1 (HIGH) — จุดเสียบที่ **ใบขอของผมเอง** ระบุ อ่านตำแหน่งก่อนที่ล็อกอินจะตัดสินจริง
ผมยืนยันเองแล้วในไฟล์ ไม่ได้เชื่อรีวิวเปล่า ๆ:
- ใบขอบอกให้แปะ `register_presence_for_character(self.foundation.selected)` หลัง `lane_hooks.register_live_session(...)` = `runtime.py:8900`
- แต่ `runtime.py:9500` (ในบล็อก `if login_scene_override is not None:`) เพิ่งจะ `replace(self.foundation.selected, position=entry.position)`
- คอมเมนต์ของ chief เองที่ `:9405` เขียนไว้ว่า *"this override is the first login path in this project where they can differ"*
⇒ ล็อกอินที่มี GM login-scene override: แถว presence ลงฉาก **เก่า** · ผู้เล่นกลายเป็นผีในฉากที่เขาออกมา และ **มองไม่เห็นเลย** ในฉากที่เขายืนอยู่จริง
(รีวิวรันจริง: `paste at runtime.py:8900 -> bg0001` · `viewer in scene 1 sees 1 other(s) (4242,)` · `viewer in scene 2 sees 0 other(s)`)
🔴 ประโยคในใบขอที่ว่า *"with the just-selected character's own row and its BOOT position"* **เป็นเท็จสำหรับล็อกอินเส้นนั้น**
**คำถามออกแบบที่ยังไม่มีใครตอบ และผมไม่ตัดสินแทน**: ตำแหน่งไหนคือของจริงสำหรับแถว presence — แถวที่ `select_and_start` คืน หรือ `entry.position` ที่ `resolve_entry` ส่งให้ไคลเอนต์จริง
รอบหน้า: ย้ายจุดเสียบ (1) ไปหลัง `:9500` หรือทำให้ประตูรับตำแหน่งที่ resolve แล้ว **แล้วแก้ข้อความใบขอในคอมมิตเดียวกัน**

## D2 (HIGH) — เทสที่ผมเขียนเองเพื่อกัน "ค่าคงที่ถูก hardcode" **ล้มไม่ได้ด้วยเหตุผลที่มันบอกเอง**
`test_the_constants_are_read_from_player_wire_not_copied_here` เกรปหาสตริงสองตัวใน **ซอร์สของโมดูล**
รีวิวเปลี่ยน `return PresenceHpPair(player_wire.PLAYER_LOGIN_HP_CURRENT, ...)` เป็น `100, 100` แล้วใส่คอมเมนต์ที่มีชื่อค่าคงที่ ⇒ **45 passed**
และต่อให้ไม่ใส่คอมเมนต์ก็ยังเขียว เพราะชื่อค่าคงที่ปรากฏใน **docstring** บรรทัด 373 อยู่แล้ว
⇒ เป็นรูป "เช็คแล้วรายงาน ไม่ได้ทำอะไร" ที่บ้านนี้ห้าม · ตัวที่ถูกคือ patch `player_wire.PLAYER_LOGIN_HP_CURRENT` เป็นค่าที่แปลกแล้วปักว่าประตูขยับตาม
🔴 นี่คือ **ประโยคเท็จที่ผมเพิ่งเขียนในรอบนี้เอง** ไม่ใช่หนี้เก่า

## D3 (MEDIUM) — กฎที่ผม cite เป็น "สามค่า" แต่ยามที่เขียนคุ้มแค่สองค่า
`PANYA-DECISION 20260901_1059` = `level` + `hp_current` + `hp_max` ทั้งสาม (`model.py:52`, `legacy_bridge.py:103`)
แถวที่ `level=None` แต่มีคู่ HP ครบ: สายส่ง **ค่าคงที่ 100/100** ขณะที่ประตูตอบ **380/520 (`character_row`)**
วันนี้ยังเกิดไม่ได้ (`persistence_login_vitals.apply_to_character` ตั้งทั้งสามใน `replace` เดียว) ⇒ **เหตุผลใน docstring ผิด ไม่ใช่สายโกหกวันนี้** — แต่ต้องแก้ให้ยามอ่านครบสามค่า

## D4 (MEDIUM) — ประโยคนำที่ผมเพิ่งเขียนใน `PLAYER_PRESENCE_WIRING` พูดสองอย่างที่โค้ดไม่ได้ทำ
- *"...doors -- register_presence_for_character / register_player_presence / clear_player_presence -- do ... the HP pair read themselves"* — `register_player_presence` **ไม่อ่าน HP เลย** (คนเรียกส่งมาสองตัว) · `clear_player_presence` ไม่แตะ HP
- *"none of these pastes reads a field"* — paste (3) ในข้อความเดียวกันอ่าน `self.foundation.selected.id` และ paste disconnect อ่าน `scene_id`/`character_id`

## D5 (MEDIUM) — ทุกคำปฏิเสธของประตูใหม่ **เงียบสนิท** ที่จุดเสียบที่ใบขอสั่งให้แปะ
paste (1)/(2) เป็นคำสั่งเปล่า ทิ้ง `PlayerNoteOutcome` · โมดูลไม่พิมพ์อะไรและไม่ลง `self.events`
⇒ ผู้เล่นที่ถูกปฏิเสธ = หายไปจากสมุดโลกของทุก session โดยไม่มีบรรทัดคอนโซลสักบรรทัด (รูป silent skip) ทั้งที่เพื่อนบ้านใน `runtime.py` พิมพ์กันหมด (`BACKPACK_LOAD_REFUSED`, `GM_LOGIN_SCENE_OVERRIDE_CONSUME_FAILED`)
เหตุที่เกิดจริงได้จากแถวจริง: `scene_id_has_no_folder` · `bad_position` (4-tuple/พิกัดเกิน 1e7) · `bad_hp` (เกิน 0xFFFFFFFF)

## D6 (MEDIUM) — paste (2) อยู่บนเส้นเดินที่เป็น "ส่วนน้อย"
`self.last_target_pos = (x, y, z, heading)` (`runtime.py:7493`) เดินเฉพาะเส้น `"promoted"` · `:7474` คืน `"v141_reads_this_frame_itself"` สำหรับ TargetPos ปกติ ซึ่ง v141 เขียนฟิลด์นั้นเองในสาขาของมัน
⇒ เดินธรรมดา = แถว presence ค้างที่พิกัดตอนล็อกอิน · ใบขอไม่พูดถึงผู้เขียนคนที่สองของฟิลด์ที่มันยึดเป็นหมุด

## D7/D8/D10 (LOW) — ยามที่ไม่มีเทสไหนจับ (บอกชื่อตรง ๆ)
- `or type(value) is bool` และ `or type(scene_id) is bool` และ `where is None or` = สามเงื่อนไขย่อยที่ **ลบแล้วยังเขียว** (`type(True) is int` เป็น False อยู่แล้ว · `getattr(None,...)` คืน None อยู่แล้ว)
- สลับ current กับ max ในสาขาค่าคงที่ **รอด** เพราะ `PLAYER_LOGIN_HP_CURRENT == PLAYER_LOGIN_HP_MAX == 100` — วันที่ค่าใดค่าหนึ่งเปลี่ยน การสลับจะหลุดไปโดยไม่มีใครจับ
- ไม่มีเพดานบนของคู่ HP ในประตูนี้ (ยืมเพดานของ registry `0xFFFFFFFF` มาโดยไม่ได้ปัก)

## D9 (LOW) — `"NEVER RAISES"` เป็นคำเกินจริง
สามรูปที่ raise: property ที่ throw · `__getattr__` ที่ throw · ค่า HP ที่ `__repr__` ระเบิด (`UnicodeEncodeError: cp874`) ผ่านทาง `_refuse(..., repr(value))`
ไม่มีรูปไหนมาจาก `model.Character` (frozen dataclass) จึงเป็น LOW — แต่คำว่า "ไม่เคย" ในเอกสารต้องแก้เป็นขอบเขตที่จริง

## สิ่งที่รีวิว **ยิงแล้วไม่แตก** (บันทึกไว้เท่า ๆ กับที่ล้ม)
- **CLAIM 5 จริง**: การถอดสตริงเหตุผลคืนโทเคนเปล่าทั้งเก้าแบบ แม้ payload จะมี `"refused: "` หรือ `" ("` อยู่ในตัว และผลลัพธ์เป็น ASCII เสมอแม้ค่าที่ผิดจะไม่ใช่ (นั่นคือสิ่งที่ทำให้คอนโซล cp874 ไม่ตาย)
- **CLAIM 3 จริงสำหรับจุดเรียกจริงทุกแบบ** (cross-product 15×15 ของค่า + รูปแถวพิสดาร): ไม่มีอะไรต่ำกว่า 1 · ไม่มี non-int (bool และ IntEnum ถูกปฏิเสธ) · ไม่มีครึ่งคู่ · ไม่มี current>max หลุด
- **CLAIM 4 จริงที่ `b558cad`** — และ **ไม่จริงที่ `e84294f`**: มิวแทนต์ที่ hardcode ฉากเป็น `1` และ hardcode ชื่อ **รอดทั้งชุด 13,566 เทส** ก่อนที่คอมมิต `1c67943` (เทสรูปศัตรูแปดแบบ) จะลงไปในรอบเดียวกัน — เฉียดของจริง บันทึกไว้
- ไม่มีเทสถูกลบ/เปลี่ยนชื่อ (28 → 45 ครบทุกตัวเดิม) · ไม่มี skip/xfail เพิ่ม · ASCII ล้วน · แตะเฉพาะสองไฟล์ของสายนี้

## รอบหน้าของ LANE-A ทำตามลำดับนี้ (งานแรกคือจ่ายหนี้ก้อนนี้ในกิ่งใหม่)
1. **D1** — ตัดสินว่าตำแหน่งไหนคือของจริง แล้วย้ายจุดเสียบ (1) + แก้ข้อความใบขอ **ในคอมมิตเดียวกัน** + จดหมายแก้ถึง chief
2. **D2** — เขียนเทสที่ patch ค่าคงที่จริงแทนการเกรปซอร์ส
3. **D4** — แก้ประโยคนำสองข้อที่พูดเกิน · **D3** — ยามอ่านครบสามค่าตามกฎที่ cite
4. **D5** — ให้คำปฏิเสธมีเสียง (บรรทัดคอนโซลชื่อ `LANE_A_PRESENCE_REFUSED ...`) แล้วเขียนลง paste
5. **D6** — หาจุดเสียบที่ครอบเส้นเดินปกติด้วย หรือเขียนขอบเขตให้ตรงในใบขอ · **D7/D8/D9/D10** ปิดท้าย
