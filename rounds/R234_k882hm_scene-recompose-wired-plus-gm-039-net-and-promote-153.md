# R234 (k882hm) — recompose ตามฉากขึ้นสาย · เน็ต GM-039 ปิดรู · เปิดใบ PROMOTE ใบแรก

เวลา: 2026-08-29T23:1x–23:5x+07:00 (`TZ=Asia/Bangkok date`)
สาย: E (PLATFORM/chief) · ล็อกรอบ: `pf_bridge#454` · `pirate-force-server#287`

## ผลของรอบ (สามบรรทัด)

1. **CORE-REQUEST ของสาย B (ใบ 2055) ต่อสายครบทั้งสามข้อ** — การตีและการฆ่าใน `Bg0002` เลิกส่งเฟรมตัวเดียวที่ RE-092 พิสูจน์ว่าลบทั้งแมพ
2. **CORE-REQUEST-GM-039 (ใบ 2058) รับข้อเสนอหลัก** — `AttributeError` เข้าเน็ตของบล็อก consume ตอน login จุดเดียว เทรดผู้ฟังเกมไม่ตายอีกจากช่องนั้น
3. **เปิด `PROMOTE-153`** ใบแรกของท่อ promotion ตาม `PANYA-DIRECTIVE 2222` + `COO-DECISION 2246` (chat echo บนบูตปกติ)

## 1. recompose ตามฉาก — ครึ่งของ chief

สาย B ส่งโมดูล `mob_scene_recompose.py` มาแล้ว (ตัวประกอบต่อฉาก ฉาก 1 delegate ของเดิมแบบไบต์ต่อไบต์ ฉาก 2 เป็นของใหม่) ครึ่งที่ค้างคือ `runtime.py` ซึ่งเป็นไฟล์ของ chief ทำแล้วสี่จุด:

- **จุด arrival ฉาก 1** (`runtime.py` สาขา bg0001) — เก็บ `self.census_anchor_record = mob_scene_recompose.census_anchor(world_population.SCENE_ID, generation.anchor, generation.actor_count)` เพิ่มจากสองแอตทริบิวต์เปล่าที่มีอยู่ (ไม่ได้แทนที่ — ตัวเก่ายังมีผู้อ่านอื่น: arena harness, frozen fallback, click dispatch)
- **จุด arrival ฉาก 2** (สาขา bg0002) — ตราเดียวกันด้วย `scene_id` ของฉากนั้น 🔴 สาขานี้ **จงใจไม่เซ็ต** `population_refresh_anchor`/`world_census_actor_count` มาแต่เดิม (คอมเมนต์ของมันเองสงวนไว้ให้ semantics ของ bg0001) ⇒ ตราใหม่คือทางเข้าของฉาก 2 โดยไม่แตะของสงวน
- **จุด bar frame และ death frames** — การ์ด `census_scene_id == world_population.SCENE_ID` เปลี่ยนเป็น `== anchor_record.scene_id` แล้วเรียก `recompose_frames(...)` แทนการเรียก `hostile_census_frames` ตรง ๆ
- **บรรทัดคอนโซล** `describe_recompose(record)` พิมพ์ **นอก** `if` ทุกสถานะ ตามข้อ 3 ของใบ

การ์ด "ฉากปัจจุบันต้องตรงกับตราของ anchor" **เก็บไว้ ไม่ได้ถอด** — ตราบอกว่า anchor ถูกวัดที่ไหน ไม่ได้บอกว่าผู้เล่นยืนที่ไหนตอนนี้ · การตีหลังข้ามฉากที่สำมะโนขาเข้าปฏิเสธ ต้องตกไป fallback ไม่ใช่เอาแมพเก่ามาประกอบใส่แมพใหม่

**ข้อที่โมดูลตัดสินให้ไม่ได้ (สาย B ถามมาตรง ๆ):** `refused_no_ledger` วันนี้ยังตกไปเฟรมตัวเดียวเหมือนเดิม รอบนี้ยังไม่ทำ "เก็บ census ล่าสุดต่อฉากแล้วส่งซ้ำ" เพราะมันคือ session state ก้อนใหม่ + วงจรอายุใหม่ ควรเป็นใบของตัวเอง ไม่ใช่ของแถมในใบต่อสาย — ตอบไว้ในจดหมาย `FROM_CHIEF_R234`

## 2. GM-039 — เน็ตของบล็อก consume

สาย GM ขอจุดเดียว: `except (ValueError, OSError, TypeError)` ⇒ เพิ่ม `AttributeError` · รับ **ข้อเสนอหลัก** ไม่เอาทาง (ก) `except Exception` และไม่เอาทาง (ข) ปล่อยรูไว้

ราคาที่ชั่งแล้วและไม่ปิดบัง: ชื่อฟิลด์พิมพ์ผิดในบล็อกนั้นจะกลายเป็น "override หาย + หนึ่งแถวเหตุการณ์" แทนเทรซแบ็ก — รับได้เพราะ CI จับ typo แบบนั้นก่อนถึงบูต (สาย GM วัดเอง: `casue` ⇒ แดง 11 เทสใน 5 ไฟล์) ส่วนอาการเดิม (เทรดผู้ฟังเกมตายใต้โปรเซสที่ supervisor เห็นว่าแข็งแรง) **ไม่มีเทสไหนเห็นได้เลย**

เทสของสาย GM ที่พิน `assertRaises(AttributeError)` ถูกกลับด้านตามที่ใบขอ: `dispatch` ต้องคืนปกติ + แถว `gm_login_scene_override_lookup_failed_AttributeError` + ตัวละครยืนที่แถวของตัวเอง + ไม่มีบรรทัด CONSUME_FAILED ปลอม

## 3. หลักฐานของรอบ

- **mutation-kill 3/3 วัดจริง** (ไม่ใช่คำอ้าง): ① ถอน `AttributeError` ออกจาก except tuple ⇒ เทส GM แดง ② คืนการ์ดเก่า `== world_population.SCENE_ID` ที่ bar ⇒ เทสฉาก 2 แดง ③ ถอดตรา arrival ของ bg0002 ⇒ แดง 3 ใบ
- เทสใหม่ `tests/test_mob_scene_recompose_wiring.py` 4 ใบ (ตราทั้งสองฉาก · bar ฉาก 2 · death frames ฉาก 2) — เทียบไบต์กับผลของ `recompose_frames` ที่เรียกเอง และอ่านจำนวนตัวกลับจากเฮดเดอร์ของไบต์ที่ประกอบ ไม่ใช่จาก roster
- **สวีตเต็ม 5151 passed · 323 skipped · 8909 subtests · เขียว(cloud sanity)** · `HYPOTHESIS_LEDGER PASS entries=47`
- 🔴 ไม่ได้พิสูจน์: ไคลเอนต์วาดอะไรจากเฟรมที่ประกอบใหม่ (ชั้น client-observable ยังไม่มีลายเซ็น) · ฉาก 2 ยังไม่มีใครตีจริงบนจอ (`GT-132` ยังบล็อก)

## 4. PROMOTE-153

`PANYA-DIRECTIVE 2222` ข้อ 2 บังคับว่าความสำเร็จห้ามหายเงียบ · `COO-DECISION 2246` สั่งให้ chat echo เป็นใบแรก · เปิดแล้วใน `GAME_TEST_QUEUE.md` (สารบัญ + ใบเต็มท้ายไฟล์)

เหตุที่แชทใบ้ **วัดแล้วรอบนี้บน main**: เส้นทาง echo ทั้งสองเลนเป็น scenario-gated — `chat_input_hypothesis.py:207,:282` และ `channel_message_hypothesis.py:636,:744` ประกาศ `production_allowed: False` และ docstring ของเลนหลังเขียนเองว่า "There is no production path to any of this" ⇒ บูตปกติสาขา dispatch ไม่มีอยู่จริง ตรงกับหลักฐานสดของเจ้าของ (เฟรมแชทถึง server 20:00:18 ไม่มี echo กลับ)

## ต้องทำอะไรต่อ

- รอบหน้าของ chief: **directive ข้อ 1 + ข้อ 7** (แยกสวิตช์เลนทำงาน/เลนกีดกัน แล้วตัด v0.1) — เส้นตาย 30 ส.ค. 21:00 · เป็นตัวปลดของ PROMOTE-153 ทั้งใบ
- สาย B: ครึ่งที่เหลือของ recompose (เก็บ census ล่าสุดต่อฉาก) ถ้าจะทำ ต้องเปิดใบของตัวเอง


---

## 5. ภาคผนวก (เขียนหลัง `pf-adversary` กลับมา) — 8 ข้อ แก้ครบในรอบเดียวกัน

`pf-adversary` ใช้เวลา 41 นาที ทดลองใน worktree ของตัวเอง (ลบทิ้งแล้ว ไม่แตะเช็คเอาต์ของรอบ)

**หักไม่ได้ (วัดแล้ว):** ฉาก 1 ไบต์ต่อไบต์เท่าเดิมทั้ง 5 เคสรวม diag objects · `recompose_frames` ไม่มีทางโยนออกจาก dispatch · NaN/Inf ไปไม่ถึงด่าน anchor · recompose ฉาก 2 ไม่เปลี่ยนสมาชิก (97 เข้า 97 ออก ต่างไบต์แรกที่ 17388 = ตัวที่ถูกตี)

**หักได้ 8 ข้อ แก้แล้วทั้งหมด:**
- **D1** คอมเมนต์อ้างว่าเน็ต GM-039 ครอบ `is_gm_account` — ไม่จริง (คนละ try ห่าง 400 บรรทัด เน็ต `(ValueError, OSError)`) ⇒ แก้คอมเมนต์ ระบุว่ารูยังเปิด **ไม่แอบขยาย**
- **D2** "ความดังย้ายที่" — ไม่จริง `state.events` ไม่พิมพ์บนบูตปกติ ⇒ เพิ่มบรรทัด `GM_LOGIN_SCENE_OVERRIDE_LOOKUP_FAILED` + เทสพิน
- **D3** จุด commit สำมะโนที่ **สาม** (lane composer R232) ไม่ได้ตรา ⇒ ตราแล้ว
- **D4** `describe_recompose` ไม่ได้พิมพ์ทุกสถานะ (อยู่ในการ์ด) ⇒ เลิกอ้าง + ขอ record "ไม่มี anchor" จากสาย B
- **D5** 4 มิวแทนต์รอดสวีตเต็ม (objects · `and`→`or` · การ์ดฉากที่ death · ชื่อ event) ⇒ เทสใหม่ 4 ใบ ฆ่าได้ทั้งหมด **วัดจริงทีละตัว**
- **D6** สถานะนอก `refused_`/`skipped_` ผ่าน assertion ของ `test_mob_combat_dispatch.py` ขณะเฟรม world-wipe อยู่บนสาย ⇒ `_recompose_event_suffix()`
- **D7** ตัวเลข "11 เทสใน 5 ไฟล์" วัดใหม่ = 7 ไฟล์ ⇒ แก้
- **D8** print +1/ตี +2/ฆ่า ~20-30% ของสตรีมเดิม · `detail=str(error)[:200]` เป็นช่อง cp874 เดียวที่ยังไม่วัด ⇒ ฝากสาย B

**หลังแก้:** สวีตเต็ม **5178 passed · 323 skipped · 9010 subtests เขียว(cloud sanity)** · ledger PASS 47 · mutation-kill รวม **7 ตัว** · PR `pirate-force-server#287` (ไม่ draft แล้ว) · `pf_bridge#454`/`#456` **merged แล้ว**

**ยังไม่ตัดสิน:** `refused_no_ledger` ยัง fallback เป็นเฟรมตัวเดียว — คำถามกลับไปที่สาย B พร้อมสามเงื่อนไข (จดหมาย `20260830_0005`)
