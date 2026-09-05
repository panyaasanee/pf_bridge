# LANE-B รอบ `4m2kx7` — ขุด roster ฉาก 8 (Silver Harbour) เปิดตาราง AI ให้มัน แล้ว**ไม่**ลงทะเบียน

เริ่ม 2026-09-06T04:31+07:00 · สาย B · COMBAT
claim PR: **pf_bridge#1426**
PR เซิร์ฟเวอร์ของรอบนี้: **pirate-force-server#PENDING** (สถานะจริงเขียนตอนจบรอบด้านล่าง)

## รอบนี้ขยับ NOW ข้อไหน

- **M3 "สนามมีมอนสเตอร์"** — ขยับหนึ่งขั้นแต่ยังไม่ถึงจอ: ฉากที่ 7 ของโปรเจกต์
  (Bg0008 · Silver Harbour) มี roster มอนจริงจากตาราง MOBS แล้ว 9 แถว 7 เทมเพลต
  และ**ตัวบล็อกฝั่งเราปิดหมดแล้ว** เหลือลายเซ็นเดียวที่สายนี้เซ็นเองไม่ได้
- **ไม่ขยับ M4** — งาน M4 ของสายนี้ใน NOW.md ติด chief ทั้งแถว: caller
  `apply_hp_damage` รอ Door B · `DEATH_SEED_WIRING` รอ chief อ่าน (`2149`) ·
  `2242` รอ chief (เห็น `#883` LANE-E เปิดอยู่จริง กำลังทำ) ⇒ ไม่มีชิ้นไหนเริ่มได้
- **ไม่ขยับ P-2** — ครึ่งของสายนี้ส่งไปแล้ว (`#876` บน main ยืนยันรอบนี้ด้วย
  `git merge-base --is-ancestor e48d910 origin/main` = จริง) เหลือ chief เสียบ census
- **งานสำรองข้อแรก (ปลดแฟล็ก 1 ตัว) ทำไม่ได้**: `docs/PROMOTION_BACKLOG.md`
  **ยังไม่มีบน origin/main** (chief `2351` ยังไม่ส่ง) และ scenario ในเขต B ทั้ง 5 ใบ
  (`combat_aggro_001` `combat_death_001` `combat_first_hit_001` `combat_loot_001`
  `combat_pickup_001`) `production_allowed = True` อยู่แล้วทุกใบ — ไม่มีอะไรให้ปลด
  ⇒ ลงงานสำรองข้อถัดไปของไฟล์สาย (โค้ดก่อน กระดาษทีหลัง) ซึ่งคือแถวนี้

## ล็อกรอบ

- ต้นรอบ list PR เปิดใน pf_bridge: `#1425` LANE-A · `#1424` LANE-GM · `#1421` LANE-E ·
  `#1420` LANE-UI — **ไม่มี** `[LANE-B]`
- เปิด claim `pf_bridge#1426` จาก `claude/focused-ramanujan-4m2kx7` (ไม่ draft · body
  ไม่มีสตริง marker ตั้งแต่เปิด)
- list ซ้ำทันทีหลังเปิด: `#1426`(B ของเรา) `#1425` `#1424` `#1421` `#1420` — ไม่มี
  `[LANE-B]` ใบอื่น ⇒ ไม่แพ้ใคร ทำงานต่อ

## กล่องจดหมาย

`grep -l "ADDRESSEE: \[LANE-B\]" notes_to_chief/*.md` ที่ไม่มี `.CONSUMED.txt` คู่ = **ว่าง**
ไม่มีใบให้บริโภครอบนี้

## งานที่รอบก่อน (`iimx05`) ส่งต่อ — ทำครบทั้งสี่ข้อ

1. **ติดตาม `#879`** ⇒ **อยู่บน main แล้ว** ยืนยันด้วย
   `git merge-base --is-ancestor 5a13eaa origin/main` = จริง (PR แสดงเป็น closed/merged:false
   เพราะรวมผ่านคิว ไม่ใช่ปุ่ม merge) ไม่ต้องกู้ ไม่ต้อง cherry-pick
2. **แจ้ง COO ว่า NOW.md ข้อ "งานแรก" ของ M4·LANE-B ค้าง** ⇒ แจ้งซ้ำเป็นรอบที่สอง
   ในจดหมาย `0441` ท้ายใบ
3. **D1 ครึ่งที่ค้าง** ⇒ ยังทำไม่ได้ ตรวจซ้ำแล้ว P-2 ยังไม่ปิด (NOW.md `0348`)
4. **ยืนยันผู้เรียกใน `runtime.py` ผ่านยามไม่แคช** ⇒ ยังไม่มีผู้เรียก (ของ chief)

## สิ่งที่ทำ

### ฉาก 8 · Silver Harbour · 9 มอนชื่อจริง

`tools/pf_mine_scene_mob_roster.py --scene Bg0008` → `field_mob_tables_bg0008.py`
(255 บรรทัด GENERATED ห้ามแก้มือ) — 9 placement · 7 เทมเพลต · ชื่อจาก `MOBS_TIP` ·
HP จาก `STANDARD_MOB[n_LEVEL_MIN]` · identity ผ่าน crosswalk `cline` (RE-128)

เลือกฉากนี้เพราะเป็นช่องว่างที่ชัดที่สุด: LANE-A มี `world_population_bg0008` +
`world_bg0008_identity` ให้ฉากนี้อยู่แล้ว (A เปิดสำมะโนการมาถึงไว้) แต่ B ไม่มีมอนเลย
เหมือนกรณีฉาก 3 และ 5 ที่ไฟล์รอบเก่าเขียนไว้ว่า "roster คือครึ่งเดียวที่ขาด"

**คอนโทรลระดับแถวมีของจริง ไม่ใช่ความบังเอิญ**: `world_bg0008_identity.IDENTITIES`
ของสาย A ขุดฉากเดียวกันด้วยเครื่องมือคนละตัวเพื่องานคนละงาน — เทส
`test_every_shipped_row_agrees_with_lane_as_independently_mined_crosswalk`
บังคับให้ทั้ง 9 แถวลงที่ `MOBS.n_ID` และ**ชื่อ**เดียวกันทั้งสองฝั่ง เคียงด้วยเลข Mob-Set
ของไฟล์ฉากเอง (ความผิดพลาดที่เทสนี้มีไว้จับคือของ GT-078: แผนที่ใส่ชื่อของแผนที่อื่น)

### ตัวบล็อกที่สอง — ตาราง AI — ปิดแล้วในรอบนี้

**วัดก่อนแก้ ไม่ใช่ทำนายจากโค้ด**: ป้อน 9 แถวเข้า `mob_ai_control.open_register`
บนตารางเดิม → ปฏิเสธ `AI_COMBAT` **162/200/471** และ `AI_WANDER` **2**

นี่คือประตูที่ราคาแพงที่สุดกับผู้เล่น ไฟล์เทสของฉาก 5 บันทึกเหตุผลไว้แล้ว:
`runtime.py` เรียก `_sync_combat_scene_state` **เหนือ** `except` ทุกตัวใน
`_dispatch_mob_combat` ⇒ การตี**ครั้งแรก**ในฉากที่ AI ไม่ได้ขุด จะคลี่ listener thread
ทิ้งและล้างโลกของผู้เล่นทั้งใบ

แก้: เติม `field_mob_tables_bg0008` เข้า union ของ `tools/pf_mine_mob_ai_rows.py`
แล้ว regenerate `field_mob_ai_tables.py` → **+4 แถว (19 บรรทัด) ไม่มีแถวเดิมเปลี่ยนแม้แถวเดียว**
(ทำ**ก่อน**การลงทะเบียนโดยตั้งใจ เหมือนรอบ `n8kq4r` เคยทำให้ Bg0015 — เพราะครึ่งนี้
ไม่ได้ติดใคร ส่วนอีกครึ่งติดลายเซ็น)

### 🔴 สิ่งที่รอบนี้ **ไม่** ทำ และเป็นหัวใจของรอบ: ไม่ลงทะเบียนฉาก 8

`field_mobs._SCENE_TABLE_MODULES` **ไม่ถูกแตะ** — ไม่มีไบต์ใหม่ถึงผู้เล่นเลย

เหตุผลวัดมาแล้ว: **ไม่มีใบไหนใน `mob_death.WIDENING_RULINGS` ครอบคลุมเทมเพลตใด
ของฉาก 8 เลย** `mob_death.ruling_for` โยน `target_outside_the_sanctioned_scope`
ทั้ง 9 แถว (274 · 277 · 280 · 281 · 527 · 529 · 544)

ถ้าลงทะเบียนทั้งที่ไม่มีใบ = มอน 9 ตัวที่ผู้เล่นตีจนเลือด 0 แล้วโดนตอบด้วยความเงียบ
ตลอดไป ซึ่งคือผลลัพธ์ที่ `COO-DECISION 2026-09-05T05:45+07:00` ปฏิเสธไว้แล้วกับ Carlos
("NPC หายไปหนึ่งตัว ดีกว่าซอมบี้ยืนอยู่หนึ่งตัว")

**ทางที่ลองแล้วและใช้ไม่ได้** (ลองจริง ไม่ได้เดา): ลงทะเบียนแล้ว withhold ทั้ง 9 แถว
แบบเดียวกับ Carlos — `field_mobs.load_roster` ปฏิเสธเองโดยการออกแบบ:
`an empty roster must come from an empty table, not from a filter`
ช่อง `LANE_WITHHELD_PLACEMENTS` มีไว้สำหรับแถวใน**ฉากที่ชิปแล้ว** ไม่ใช่ทั้งฉาก
⇒ **ไม่ลงทะเบียน** คือสถานะเดียวที่ถูกต้อง และเทสยึดสองครึ่งนี้ไว้**ด้วยกัน**
(`test_scene_eight_stays_unregistered_while_no_letter_covers_it` — วันที่ทุกแถวมีใบ
เทสตัวเดียวกันนี้จะ**บังคับให้ลงทะเบียน** ไม่ใช่ต้องลบเทสทิ้งเพื่อเดินต่อ)

### การอ่าน predicate ที่ generator บังคับให้ทำก่อนชิป

ฉาก 8 predicate ไม่ตรงกัน: `ai_combat 9 · rank 10 · drops_normal 8 · rank_and_ai_combat 9`

- `rank 10` vs `9`: หนึ่ง placement มี rank แต่ไม่มี combat AI → ไม่ชิป (เหมือนทุกฉากพี่น้อง)
- `drops_normal 8` vs 9 แถวที่ชิป: **placement 69 "Nina" (MOBS 529)** ไม่มีตารางดรอปเลย
  สักช่อง และใส่ avatar ของ**ผู้เล่น** `P_FEMALE_003_002_NENA`
  ⇒ **รูปทรงเดียวกับ Carlos เป๊ะ ๆ** (Bg0015 p87 · MOBS 924 · `P_MALE_033_000_CARLOS`)
  ซึ่งถูก withhold อยู่วันนี้เพราะคำถามเนื้อหา "template 924 คืออะไร" ยังไม่มีคำตอบ
  ⇒ ถามคำถามเดียวกันเรื่อง 529 ไปพร้อมใบขออนุญาต แทนที่จะปล่อยขึ้นจอก่อนแล้วค่อยถาม
  (เทส `test_the_second_player_avatar_row_is_named` ยึดข้อเท็จจริงชุดนี้ไว้ รวมถึงยึดว่า
  Carlos ยัง withheld อยู่จริง — ถ้าบรรทัดฐานที่รอบนี้อ้างขยับ เทสจะแดง)

## จดหมายที่เขียน

`notes_to_chief/20260906_0441_LANE-B-ASK-COO-widen-death-scope-bg0008-silver-harbour-seven-templates.md`
(ADDRESSEE: COO) — ขอใบ `widen-death-scope-bg0008-seven-templates` ครอบ
`{274, 277, 280, 281, 527, 529, 544}` + คำถามเนื้อหาเรื่อง Nina สามทางเลือก
ตามกติกา "เขียนคำถาม แล้วเดินต่อ": **ไม่หยุดรอ** — ถ้าไม่มีคำตอบข้อ 2 รอบถัดไปที่ใบมาถึง
จะเดินทางที่ 2 (ชิป 8 ตัว · Nina เข้า withhold เคียง Carlos) เพราะย้อนถูกที่สุด
ติดป้าย `[สมมติของสาย [LANE-B] - รอ COO ยืนยัน]` ไว้ในใบแล้ว

## pf-adversary

`ADVERSARY_UNAVAILABLE: claude/nice-meitner-4m2kx7` — เซสชันนี้ไม่มี tool ให้เรียกจริง
(ค้นแล้ว รายการ agent ที่มีคือ claude / Explore / general-purpose / Plan / statusline-setup
/ claude-code-guide และ pf-* ที่ประกาศไว้แต่ไม่รับคำสั่งในรอบนี้)
⇒ self-review ตามกติกา:

- อ่านทุก hunk ใน `git diff --cached` ก่อน commit (5 ไฟล์)
- **ของที่ self-review จับได้จริงในรอบนี้ สามอย่าง เขียนไว้ไม่ปิดบัง**:
  1. ร่างแรกของเทส regenerate เทียบ **stdout** ของ generator กับไฟล์บนดิสก์ → แดง
     เพราะ generator พิมพ์รายงาน withdrawn 14 บรรทัดลง stdout ปนกับตัวโมดูล
     แก้เป็นเขียนผ่าน `--out` ลงไดเรกทอรีชั่วคราวแล้วเทียบเนื้อไฟล์
  2. ร่างแรกใช้ `unittest.skipUnless(BRIDGE_GAMEDATA is not None, ...)` ซึ่ง**ไม่เคย skip**
     เพราะ `BRIDGE_GAMEDATA` เป็นอ็อบเจกต์ `Precondition` ไม่ใช่ path (จริงเสมอ)
     แก้เป็น `@BRIDGE_GAMEDATA.skip_unless_present()` ระดับคลาสตามแบบไฟล์พี่น้อง
     — ถ้าไม่จับ เกต Windows ที่ไม่มี pf_bridge จะแดง
  3. การเติม union ทำให้ pin สองตัวใน `tests/test_mob_ai_control.py` แดง (extras และ
     รายการ `AI_WANDER_ROWS`) — **นี่คือเทสที่ทำงานถูกต้อง** ไม่ใช่เทสที่ต้องข้าม
     แก้ pin ให้รับสภาพ "ฉากขุดแล้วแต่ยังไม่ลงทะเบียน" โดย**อนุมานจากโมดูล roster เอง**
     ไม่ใช่พิมพ์เลขซ้ำ (defect ที่รอบ `am1fw8` เคยบันทึกว่าทำให้ pin ค้างมาทั้งฉาก)
- ไม่มีเทสไหนถูก skip/disable เพื่อให้เขียว

## เทส

- ไฟล์ใหม่เดี่ยว: `pytest tests/test_field_mob_tables_bg0008.py -q` → **11 passed**
- ร่วมกับพี่น้อง: `test_mob_ai_control.py` + ไฟล์ใหม่ → **70 passed, 53 subtests**
- กลุ่ม mob_ai / field_mobs / mob_death ทั้งหมด → **472 passed, 777 subtests**
  (ก่อนแก้ pin: 2 failed — บันทึกไว้ข้างบน)
- **ชุดเต็มบนต้นไม้สุดท้าย** (`git merge origin/main` = Already up to date ก่อนรัน):
  ผลอยู่ท้ายไฟล์นี้
- `pf_gate_preflight.py --repo /home/user/pirate-force-server`: **PREFLIGHT PASS**

## TWO_SESSIONS_SAME_SCENE

รอบนี้ไม่เพิ่ม state ต่อ session แม้แต่ตัวเดียว: `field_mob_tables_bg0008.py` เป็น
ตารางค่าคงที่ล้วน (ไม่ import อะไรเลย) · `field_mob_ai_tables.py` เหมือนกัน ·
`_parse_hostile_placements` เป็นฟังก์ชันบริสุทธิ์อ่านโมดูลตาราง คืนอ็อบเจกต์ใหม่ทุกคอล
เทสตัวเดียวที่แตะรีจิสทรี (`test_a_full_withhold_is_not_an_alternative...`) คืนค่าเดิมใน
`finally` และ assert ซ้ำหลังคืนว่าฉากไม่อยู่ในรีจิสทรีแล้ว

## NO_FEATURE_WAITING

ไม่มีผล RE/GT ใบไหนของสายนี้ที่ตอบแล้วและยังไม่ถูกใช้ในรอบนี้ — กล่องจดหมายว่าง

## หนี้ที่ยังค้าง ไม่ใช่ของรอบนี้ให้ปิด

- D1 ครึ่งที่ค้าง (`first_in_the_world`) — ยังติด NOW.md ที่ห้ามใบเทสตีมอนจน P-2 ปิด
- `0014`/`0015` (`DEATH_SEED_WIRING`) รอ chief
- ข้อความค้างใน NOW.md เรื่อง `1246`(ค) — แจ้ง COO รอบที่สองแล้ว

## รอบหน้าทำอะไร

1. **ใบ COO เรื่องฉาก 8 มาถึงหรือยัง** — มาแล้วให้ทำเป็นงานแรก: เติมใบเข้า
   `mob_death.WIDENING_RULINGS` + ลงทะเบียน `field_mob_tables_bg0008` ใน
   `_SCENE_TABLE_MODULES` (**หนึ่งบรรทัด**) + Nina ตามคำตอบข้อ 2 (ไม่ตอบ = ทาง 2)
   ⇒ นั่นคือรอบที่ SCOREBOARD เป็น COMING จริง และ M3 ได้สนามที่เจ็ด
2. ยืนยัน `#PENDING` (PR ของรอบนี้) ขึ้น main ด้วย `git merge-base --is-ancestor`
3. ฉากถัดไปที่ A มี census แต่ B ไม่มีมอน: `bg0006` `Bg0007` `Bg0009` `Bg0010` `Bg0011`
   — ทำได้ทันทีแบบเดียวกัน แต่**ออกใบขออนุญาตล่วงหน้าพร้อมกันทีเดียว**จะดีกว่า
   ออกทีละฉากทุกรอบ (ข้อเสนอนี้อยู่ในจดหมาย `0441` ให้ COO พิจารณา)
4. เมื่อ P-2 ปิด: D1 ครึ่งที่ค้าง

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็น และรอบนี้พูดตรง ๆ ว่าทำไม** — ฉาก 8 ยังไม่ลงทะเบียน เพราะลงทะเบียนวันนี้
แปลว่าใส่มอน 9 ตัวที่ตีจนเลือดหมดแล้วยืนเฉยตลอดกาลให้ผู้เล่น ซึ่งแย่กว่าสนามว่าง
สิ่งที่รอบนี้ทำคือ ทำให้ระยะห่างระหว่างผู้เล่นกับ "มอนชื่อจริง 9 ตัวใน Silver Harbour"
เหลือ **ลายเซ็นเดียวจาก COO + หนึ่งบรรทัดโค้ด** จากเดิมที่ต้องขุดตาราง ขุด AI
หาคอนโทรล และค้นว่าอะไรกันบ้าง

SCOREBOARD: STUCK | ฉากที่ 7 (Silver Harbour) มี roster มอนจริง 9 ตัวจากตาราง MOBS และตาราง AI เปิดรับมันแล้ว แต่ผู้เล่นยังไม่เห็นเพราะยังไม่มีใบอนุญาตให้มอนพวกนี้ตายได้ ลงทะเบียนวันนี้ = ซอมบี้ 9 ตัว จึงถือไว้และขอใบแทน | pirate-force-server#PENDING · pf_bridge#1426 · notes_to_chief/20260906_0441_LANE-B-ASK-COO-widen-death-scope-bg0008-silver-harbour-seven-templates.md
