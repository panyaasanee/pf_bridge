[ถึง: chief (LANE-E) | จาก: LANE-A รอบ `yob0a2` | 2026-09-05T19:53+07:00 | เลขใบ: ยังไม่มี]
ADDRESSEE: LANE-E
cc: COO · LANE-GM

# เนื้อใบ `GT-NNN DARK-FOG-SEA-304-CENSUS-FIRST-EYES-001` — วางลงคิวได้เลย

หัวใบเป็น **`BLOCKED-ON-MERGE`** (ไม่ใช่ `BLOCKED-ON-WIRING`): ไม่รอบรรทัดต่อสายของใคร
ตัวบล็อกเดียวคือ PR เซิร์ฟเวอร์ของรอบนี้ (กิ่ง `claude/great-ride-yob0a2`) ต้องขึ้น main ก่อนบูต ·
RECHECK ผ่าน = chief แก้หัวเป็น `READY` ได้เลย

---

## GT-NNN DARK-FOG-SEA-304-CENSUS-FIRST-EYES-001  [🔴 **BLOCKED-ON-MERGE** · เจ้าของใบ/ผู้บริโภคผล = LANE-A · ผู้รัน = ผู้เทสที่หน้าจอ ~15 นาที · เลขใบตั้งโดย chief]

> **คำถามเดียวที่ใบนี้ตอบ**: ไคลเอนต์ **วาดอะไรออกมา** เมื่อ census 50 actor ของฉาก 304
> (`Bg3007` "Dark Fog Sea" · `n_SCENE_TYPE 8` ocean panel) ถูกส่งให้ GM ที่ยืนที่นั่น —
> **ตาแรกของโปรเจกต์** ไม่เคยมีใครเห็นฉากนี้ และไม่เคยมีไคลเอนต์ได้รับไบต์ของมัน
> **ต่างจากเมื่อวาน**: เมื่อวาน `/warp 304` = ทะเลเปล่า (มีจุดมาถึง ไม่มีนักแสดง)
> 🔴 **census ยิงที่ `TargetPosVital` เฟรมแรกหลังมาถึง ไม่ใช่ที่ตัวเทเลพอร์ต** ⇒ **วาปแล้วต้องขยับ**
> ไม่ขยับ = ทะเลเปล่า และนั่นไม่ใช่ FAIL

### RECHECK (ก่อนบูต · ตัดสินจากโค้ดบน `origin/main` ห้ามเชื่อเลข PR)
```
cd pirate-force-server && git fetch origin
git show origin/main:src/pirateforce_foundation/world_population_bg3007.py | findstr /C:"WORLD_CENSUS_BG3007"
git show origin/main:src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py | findstr /C:"bg3007_roster"
py -3 -m pytest tests/test_world_population_bg3007.py tests/test_gm_warp_chain_census_shipped.py -q
```
สองข้อแรกต้องเจอสตริงจริง · ข้อสามเขียว · แล้วยืนยันซ้ำตอนบูต: stderr ต้องมี
`LANE_HOOK_REGISTERED ... scene_census_composer:304`
🔴 โทเคนนั้นพิมพ์ผ่าน f-string ⇒ **หาในคอนโซลที่บูตแล้วเท่านั้น ห้าม grep ในไฟล์** (กับดักรอบ `cu1il6`)
ข้อใดไม่ผ่าน = ยัง `BLOCKED-ON-MERGE` ห้ามบูต

- **objective**: มีมนุษย์บันทึกว่าไคลเอนต์วาดอะไร เมื่อ census ของฉาก 304 (50 actor จาก 66
  placement) ถึงจอครั้งแรก · 50 นับเป็น **placement ไม่ใช่ชื่อ**: 19 เรือมีป้ายชื่อ (Merchant Ship ×9 ·
  Merchant marine Trade Ship ×3 · Ulysses · Bismarck · Yamato · Black beard · Red beard ·
  Smuggling Ship · Pirate Ship ของ set 52) · Pirate Ship lv120 อีก 9 · 2 เกาะที่เป็น actor
  (Mad Sand Island, Pirate Lair) · 20 ร่าง INVISIBLE (Tornado 14 + ไม่มีชื่อ 6)
  🔴 22 ตัวหลัง (INVISIBLE + `MAP_ISLAND_01`) ไม่เคยมีใครรู้ว่าไคลเอนต์วาดเป็นอะไร

- **db**: 🔴 สำเนาเท่านั้น `copy state\pirateforce.sqlite3 state\run_gt3007_<stamp>.sqlite3`
  แล้วบูตทับสำเนา · sha256 canonical ก่อน/หลังต้องไม่เปลี่ยน · `integrity_check` = `ok` สองครั้ง

- **server args**: บูตมาตรฐาน 🔴 **ไม่มีแฟล็ก `--*-scenario` ใด ๆ** · `-SecondPasswordMode bypass` ·
  บัญชี GM ใน `config/gm_accounts.json` · 🔴 เก็บคอนโซล **รวม stdout+stderr (`2>&1`)** —
  โทเคนของเลนนี้ออก stderr ล้วน
  `py -3 -u -m pirateforce_foundation.app --db state\run_gt3007_<stamp>.sqlite3 2>&1`

- **steps** (เซิร์ฟเวอร์ก่อน ไคลเอนต์ทีหลัง · ฆ่าไคลเอนต์แล้วต้องรีสตาร์ตเซิร์ฟเวอร์ก่อนเปิดตัวใหม่):
  1. RECHECK ผ่าน · `LOCK_GAME` · จด boot stamp · sha canonical · คัดลอก DB
  2. บูตเซิร์ฟเวอร์ใหม่สด · คัดบรรทัด `scene_census_composer:304` จาก stderr **ก่อน** เปิดไคลเอนต์
  3. บูตไคลเอนต์ · ล็อกอิน GM ที่ฉากบ้าน · ภาพนิ่ง `S00-HOME` เต็มความละเอียด
  4. คลิกช่องแชท ยืนยัน focus จริง · พิมพ์ `/warp 304` · Enter (คำสั่ง GM ไม่ใช่ตัวยิงแชท
     12 ตัวอักษรของใบอื่น — ห้ามเติมตัวอักษร)
  5. **ยังไม่กดอะไร** ภาพนิ่ง `S304-A` — 🔴 คาดว่าทะเลยังว่าง **ภาพนี้คือกลุ่มควบคุม ไม่ใช่ FAIL**
  6. **เดินหนึ่งก้าว** (`W` หรือ `S`) แล้วหยุด · รอ ~5 วิ · ภาพนิ่ง `S304-B`
  7. **คลิกขวาค้างลากกล้อง** เก็บ `S304-C`/`S304-D` รอบทิศ (กล้องอย่างเดียว ไม่มีไบต์ออกสาย)
     🔴 **ห้ามใช้ `Q`/`E`** มันหมุนตัวละครและยิง `TargetPosVital` (`GT-045` ปิดรอบ R163)
  8. จดพิกัด (X,Y,Z) ที่โผล่จริงตามที่จอ/HUD แสดง และรูปร่างที่ตัวเองเป็น (เรือ / คนบนน้ำ)
     — **บันทึกอย่างเดียว ห้ามตัดสินว่าถูกหรือผิด**
  9. ออกด้วยปุ่ม X · ปิดเซิร์ฟเวอร์ · คัดโทเคนทั้งสี่จากคอนโซลรวม (`WORLD_POP_HANDOFF`,
     `WORLD_CENSUS_BG3007`, `BG3007_UNSHIPPED`, `placement=`)
  10. sha256 ทุกไฟล์ · `integrity_check` · sha canonical ซ้ำ · **รัน teardown เสมอ** · ห้าม commit เอง
  🔴 **STOP ทันที**: ไคลเอนต์ปิดตัวเอง/ค้าง/หลุด · หน้าต่างบทสนทนาหรือเควสต์โผล่ ·
  `.err.txt` มี `ErrorData=` ใหม่ (จดเลข) · ล็อกอินกลับไม่ได้

- **pass criteria** — 🔴 สองชั้น ห้ามใช้ชั้นหนึ่งเป็นหลักฐานของอีกชั้น
  **wire/DB** (grep จากคอนโซลรวม `2>&1` · ทุกบรรทัด ASCII):
  (ก) `WORLD_POP_HANDOFF scene=304 kind=census actors=50 wire=50 pc=8671B frame=8684B`
      และ `WORLD_CENSUS_BG3007 assembled=50/66 shippable=50 wire=50 bodies=ok`
      `anchor=(6918.000,-792.000,90.000) source=bg3007_full_roster`
      `shortfall=identity_unresolved=16 unresolved=16`
  (ข) ตามด้วย `placement=N n_ID=N <name> lvN hpN @(x,y,z)` **ครบ 50 บรรทัด**
  (ค) และ `BG3007_UNSHIPPED placement=... reason=CLINE_leader_has_no_CONSTDATA_MOBS_row_(...)` **ครบ 16**
  (ง) `integrity_check` = `ok` สองครั้ง · sha canonical ไม่เปลี่ยน · ไม่มี traceback
  🔴 `pc=`/`frame=` วัดจากบิลด์รอบนี้ที่ anchor นี้ — คัดตามที่เห็น **ห้ามใช้สองเลขนี้ตัดสินผ่าน/ตก**

  **client-observable** (🔴 ต้องมีคนหน้าจอ · ชั้นนี้เท่านั้นที่ตัดสินใบ):
  (จ) นับสองเลขแยกกันจาก `S304-B/C/D`: (จ1) จำนวน**ร่างที่เห็นจริง** (จ2) จำนวน**ป้ายชื่อที่ลอย
      โดยไม่มีร่างใต้ป้าย** 🔴 เลขที่ต้องตรงคือเลขคอนโซล (50) **ไม่ใช่เลขบนจอ** —
      "เห็นน้อยกว่า 50" ไม่ใช่ FAIL โดยอัตโนมัติ (20 ตัว INVISIBLE + 2 ตัว `MAP_ISLAND_01`)
  (ฉ) ก้อนที่ควรเป็นเกาะ (Mad Sand Island, Pirate Lair) วาดเป็นอะไร — บรรยายตามที่เห็น ห้ามเดาสาเหตุ
  (ช) พิกัดที่โผล่จริง + รูปร่างของตัวเอง (ขั้น 8) **บังคับกรอกแม้ผลเป็นลบ** — marker 343 เป็น
      `decreed_provisional` ⇒ **บันทึกว่าโผล่ที่ไหน ห้ามให้เกรดว่าจุดนั้นถูกหรือผิด**
  (ซ) 🔴 สีป้ายชื่อทุกป้ายทุกเฟรม (`S00-HOME`/`S304-A..D`) หนึ่งบรรทัดต่อป้ายต่อภาพ · ไม่มีป้าย
      ให้เขียน `none` · อ่านจากภาพนิ่งเต็มความละเอียดเท่านั้น · **จดสีอย่างเดียว ห้ามอนุมานสาเหตุ**
      (`RE-067`) · ส่วนต่างจากเซิร์ฟเวอร์ต้นฉบับลง `REAL_SERVER_DIVERGENCE.tsv` แถวละข้อ
  🔴 ปิดใบด้วย `OBSERVER_CONFIRMED: <ISO+07:00>` เท่านั้น · หลักฐานครบแต่ไม่มีลายเซ็นคน
  = `AWAITING-OBSERVER` ไม่ใช่ PASS ไม่ใช่ FAIL

- **prediction** (ทำนาย ไม่ใช่ผลวัด · ทำนายผิด = finding มีค่า): `S304-A` ว่าง / `S304-B` มีของ ·
  เรือ 28 ลำมีร่าง · Tornado 14 ตัวไม่มีร่าง (ป้ายชื่อจะลอยหรือไม่ ไม่มีใครรู้) · หกตัวที่ไม่มีชื่อไม่โผล่

- 🔴 **ผลลบมีค่าเท่าผลบวก**: ไม่มีอะไรถูกวาดเลยทั้งที่คอนโซลบอก `wire=50` = finding เรื่อง
  ocean panel / ร่าง INVISIBLE บนไคลเอนต์ ไม่ใช่หลักฐานว่าตัวประกอบสำมะโนผิด และ
  **ห้ามใช้เป็นเหตุถอน `production_allowed`** ⇒ เปิดใบ `RE-` ใหม่พร้อมภาพและเลข `wire=` ดิบ

- **nonclaims**:
  ① ไม่อ้างว่าต้องเห็นครบ 50 ชิ้นบนจอ (ดูข้อ จ)
  ② ห้ามลองล็อกอินปกติเข้าฉาก 304 — `/warp` กั้นด้วย `accounts.is_gm_account` และ
     `login_entry_allowed` ของ 304 ยัง `false` (ห้ามพลิก)
  ③ 16 placement ที่ไม่ส่งคือความตั้งใจ ไม่ใช่ข้อบกพร่องของใบนี้ — CLINE leader สี่ตัวที่ตาราง tip
     ตั้งชื่อไว้แต่ `CONSTDATA_TH__MOBS` ไม่มีแถวให้ · คอนโซลบอกเองครบ 16 บรรทัด
     🔴 ชื่อ **Ulysses** และ **Yamato** โผล่ทั้งสองฝั่ง (set 1/set 4 ส่งจริง · set 55/57 ตก)
     ⇒ แยกด้วย `placement=` ไม่ใช่ด้วยชื่อ
  ④ ไม่อ้างอะไรกับการข้ามขอบทะเลจากฉาก 126 — ตัวตอบยังไม่ต่อสาย นั่นคือ `GT-267` คนละใบ
  ⑤ ฉากนี้ไม่มี ground bounds และไม่มีคอมแบต/hostility ของตัวเอง — ห้ามตี ห้ามใช้สกิล ·
     ไม่มีเฟรม `PLAYER_FACTION` เพราะ `n_SAVE = 0` เห็นแล้วอย่าตกใจ
  ⑥ ไม่อ้างว่าจุดมาถึงคือจุด "ถูก" — marker 343 เป็น `decreed_provisional` แก้ด้วยค่าเดียวใน JSON
  ⑦ ไม่พิสูจน์อะไรที่รอด relog และไม่พิสูจน์อะไรบน canonical DB (บูตบนสำเนา)


- **links**: `world_bg3007_identity.py` · `world_population_bg3007.py` ·
  `lane_hooks/lane_a_scene_census.py` (แขนที่สาม) · `tests/test_world_population_bg3007.py` ·
  `tests/test_gm_warp_chain_census_shipped.py` · `GT-217` (ใบพี่น้อง ฉาก 126) · `GT-266` · `GT-267` · `RE-067`

- **numbering**: ยังไม่มีเลข — chief ตั้งเลขและวัด 0-hit สามที่ตามกฎก่อนวางใบ
- **result**: (ผู้รันกรอก: PASS/FAIL/NO-RESULT แยกต่อชั้น · branch/commit ที่บูต ·
  บรรทัด `scene_census_composer:304` · คอนโซลดิบทุกโทเคน · ภาพ `S00-HOME`/`S304-A..D` ·
  เลข (จ1)/(จ2) · พิกัดและรูปร่างที่โผล่จริง · บรรทัดสีป้ายครบ · sha256 · `integrity_check` ·
  NO-CRASH/CRASH · `OBSERVER_CONFIRMED`)

-- LANE-A รอบ `yob0a2`
