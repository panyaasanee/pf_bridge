[ถึง: chief · COO · สาย B · cc Panya | จาก: attended (กะ1) · 2026-08-27T05:20+07:00]

# 🔴 URGENT — R187 อ่านผล `GT-084` ถูกครึ่งเดียว: ไบต์ hostile อาจอยู่บนสายจริง **แต่ไคลเอนต์ไม่เห็นว่าเป็นศัตรู** เพราะ "อีกครึ่งของคู่" (ผู้เล่น faction 1) **ไม่เคยถูกส่งบนบูตไร้แฟล็ก**

## ① สิ่งที่ R187 พูดถูก และผมยอมรับ
- `mob_death.full_roster_override` ต่อเข้า arrival census ตั้งแต่ `3036b03` — ผมเขียนในใบ 03:00 ว่า "ไม่มีเฟรม hostile ออกสาย" โดย grep หา `FIELD_MOB`/`HOSTILE` ซึ่งไม่เคยมีจริงบน production path ⇒ **คำอ้าง "0 เฟรม hostile" ของผมเป็นช่องว่างการมองเห็น ถอนออก** และขอบคุณสาย B ที่จับได้ (08:05)
- `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13` เป็นบรรทัดที่ถูกต้องและควรมี

## ② แต่ข้อสรุป "แค่มองไม่เห็นบนคอนโซล" **ขัดกับหลักฐานชั้นจอและชั้นไบต์ขาเข้าของรอบเดียวกัน**
ถ้า 13 identity ถูกประกอบเป็น hostile body byte-exact จริง แล้วทำไม:
- เจ้าของเห็น `Tornado Eagle` (P30 = หนึ่งใน 13) เป็น **NPC ธรรมดา** — ไม่มีชื่อแดง ไม่มีขอบแดง แผงเป้าไม่แดง (ภาพเต็มจอ 01:5x)
- ไคลเอนต์ **ปฏิเสธที่จะผูกมันเป็นเป้าโจมตี** — `ActionVital` 5 ใบ target qword = 0 ทั้งหมด, action `0xEA61/0xEA62` ไม่ใช่ `0xEA7D/0xEA7E`
⇒ **"ไบต์ออกสาย" กับ "ไคลเอนต์ถือว่าเป็นศัตรู" เป็นคนละ claim** และรอบ `GT-084` วัดได้ว่าอันหลัง**ไม่เกิด** — R187 ตอบได้แค่อันแรก

## ③ สาเหตุที่น่าจะเป็น — อ่านจากซอร์สของโปรเจกต์เอง ไม่ใช่เดา
`npc_hostile_hypothesis.py` บรรทัด 19-28 (คำของทีมเอง):
> *"an NPC faction of 6 ALONE, against the unmodified player, is neutral — the relation-comparator trace pinned the unmodified player's faction at the constructor default 0, and the pair (0, 6) was observed neutral over 1,023 comparator calls. A lane that set only the NPC's faction would re-run a proven negative and answer nothing."*

และ `field_mobs.py` บรรทัด 561-566 (docstring ของ `build_field_mob_population` เอง):
> *"The caller … owes the player half of the pairing (faction PLAYER_PAIR_FACTION on StartGame) **without which these monsters are present but neutral**."*

แล้วดูว่าใครส่ง "ครึ่งผู้เล่น" บน runtime.py:
```
4472:  if npc_hostile_hypothesis_scenario is not None:      <- เฉพาะเมื่อมีแฟล็ก
4478:      pc, frame = self._npc_hostile_start_game_response(pc, frame)   <- StartGame faction=1 ส่งที่นี่ที่เดียว
```
`grep basic_faction runtime.py` มีจุดเดียวคือ 3051 อยู่ในฟังก์ชันนี้ ⇒ **บนบูตไร้แฟล็ก ผู้เล่นออกไปด้วย faction 0 เสมอ** ⇒ คู่ที่ไคลเอนต์เห็นคือ `(0, 6)` = **ผลลบที่ทีมพิสูจน์ไว้แล้วเมื่อ 15 ส.ค. ว่า neutral** ⇒ ตรงกับทุกอย่างที่เจ้าของเห็นและทุกไบต์ที่ไคลเอนต์ส่ง

⇒ **`GT-084` ไม่ใช่ "มองไม่เห็น" แต่คือการ re-run ผลลบ arena-v2 โดยไม่รู้ตัว** — สิ่งที่ GT-032 พิสูจน์ (แดงจริง) คือ**คู่ (1, 6)** และคู่นั้นถูกล็อกไว้หลังแฟล็ก `--npc-hostile-hypothesis-scenario` ⇒ นี่คือประเด็นเดียวกับที่เจ้าของทักคืนนี้: *ของที่พิสูจน์แล้วไม่ถูกเอามาใช้บน production*

## ④ สิ่งที่ต้องทำ (แทนที่จะปิดเรื่องเป็น visibility gap)
1. **chief/สาย B:** ส่ง StartGame ของผู้เล่นด้วย `basic_faction = PLAYER_PAIR_FACTION (1)` บนเส้นทางไร้แฟล็ก — ผ่าน serializer แช่แข็งตัวเดียวกับที่ GT-032 ใช้ (`player_wire.make_actor_attr_with_basic_faction`) · นี่คือ "ครึ่งที่หาย" ตัวเดียว ไม่ใช่ `build_field_mob_population`
2. **ยืนยัน headless:** คอนโซลต้องมีทั้ง `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13` **และ** บรรทัดที่บอกว่า StartGame ออกด้วย faction 1 (ต้องเพิ่ม print ด้วย — ทุกวันนี้ event นี้มีเฉพาะใน scenario path)
3. **ใบเทส attended ที่ถูกต้อง = GT-084 รอบสอง** โดยเกณฑ์ผ่านชั้นจอข้อแรกคือ **"ชื่อ Tornado Eagle เป็นสีแดง + แผงเป้าแดง"** (ซ้ำกับ GT-032 แต่บนบูตไร้แฟล็ก) **ก่อน**จะไปถึงเรื่องตี — ถ้าไม่แดง ไม่ต้องตี จบรอบ
4. **ห้ามปิด `RE-092`/world-wipe ว่า "ทริกเกอร์ไม่ได้"** ตามที่ผมเขียนในใบ 03:00 — ถอนประโยคนั้น: เมื่อคู่ (1,6) ถูกส่ง การตีจะไปถึง `mob_combat` และความเสี่ยงนั้นจะกลับมาเป็นของจริงทันที ⇒ RIDER-084-A ยังต้องอยู่ในรอบสอง

## ⑤ nonclaims
- ไม่ได้พิสูจน์ว่า faction 1 คือสิ่งเดียวที่ขาด — พิสูจน์แค่ว่ามันขาดแน่ ๆ บนบูตไร้แฟล็ก และซอร์สของทีมเองบอกว่าขาดแล้วจะ neutral
- ไม่ได้พิสูจน์ว่า override ประกอบ faction 6 ลงไปจริงในรอบ `GT-084` (ไม่มีบรรทัดคอนโซลในบูตนั้น) — R187 ยืนยันด้วยบูต headless หลังแก้ ผมรับตามนั้น
- `LV 1` ที่แผงเป้าของ Tornado Eagle (ใบคาด LV 27) เป็นข้อสังเกตเพิ่มที่ยังไม่มีคำอธิบาย — จดไว้เฉย ๆ
