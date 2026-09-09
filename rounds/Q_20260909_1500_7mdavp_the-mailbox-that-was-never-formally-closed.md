# LANE-Q รอบ `7mdavp` — จ่ายผล adversary ของ #1184 · ปิดใบ .tgr ที่ตกมาสามรอบ · เคลียร์กล่องจดหมาย 13 ใบที่ค้างไม่มี stub

เริ่ม 2026-09-09T15:00+07:00 · claim `pf_bridge#1987`
นาฬิกา: `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด 15:00 · ผมเริ่ม 15:00-15:14 ⇒ ห่าง ≤14 นาที (< 60) — ไม่ค้าง

`TWO_SESSIONS_SAME_SCENE:` ไม่เกี่ยว — ของที่รอบนี้แตะเป็นแถวเควสต่อตัวละคร (quest-state seam) + จดหมาย/เอกสาร
ล้วน ไม่มี state ต่อฉาก ไม่มี world registry ไม่มี combat state

## 0. ล็อกรอบ

list PR `pf_bridge` open ก่อนเปิด: ไม่มีใบหัว `[LANE-Q] round <id>: claim` ⇒ ว่าง เปิด `#1987`
เปิดแล้ว list ซ้ำทันที: เป็น `[LANE-Q]` ใบเดียวที่เป็น claim และใหม่สุด ⇒ ไม่มีใครแก่กว่าให้ยอม

## 1. รอบนี้ขยับ NOW/M ข้อไหน

- **บันได M**: ไม่ขยับขั้นไหนโดยตรง (M2 ยังเป็นของ LANE-A ตาม NOW) — แต่ปิดคำถาม "crosswalk .tgr ↔ wire id" ที่บล็อกอยู่หลัง
  M2's "registry/id → เลือกไฟล์สคริปต์ → รัน" ครึ่งหลัง (ดูข้อ 3)
- **NOW บรรทัด Q**: ไม่มีบรรทัดเฉพาะของ Q ใน NOW.md รอบนี้ที่ต้องขยับโดยตรง — งานหลักรอบนี้คือหนี้ที่ค้าง (adversary
  ของ `#1184`) และกล่องจดหมายที่ยังไม่ปิด
- **จดหมายที่บริโภครอบนี้**: **13 ใบ** (ดูข้อ 4) — ตัวเลขนี้สูงผิดปกติเพราะรอบก่อน (`yd9u99` ย้อนไปถึง `bxly5p`)
  ใช้ pattern grep ผิด (`ADDRESSEE: Q` แทน `ADDRESSEE: LANE-Q` ตามที่ `prompts/LANE-Q.md` ประกาศเองว่า `<TAG> =
  [LANE-Q]`) จึงเห็นกล่องจดหมายว่างเปล่าทุกรอบทั้งที่ไม่ใช่ — **บทเรียนกระบวนการของรอบนี้**: แก้ pattern แล้ว
  (`grep -l "ADDRESSEE:.*LANE-Q\b"`) ไม่ใช่แค่รอบนี้ที่ต้องจำ เขียนไว้ให้รอบหน้าเห็นด้วย

## 2. งานหลัก A — จ่ายผล pf-adversary ของ `#1184` (ADVERSARY_PENDING จากรอบ `yd9u99`)

`#1184` **merge แล้วจริง** (ยืนยัน `git merge-base --is-ancestor 7e2e557 origin/main` = true บน
`pirate-force-server`) — ตามกฎบ้าน รอบนี้เป็นรอบแรกที่ต้องหยิบผล adversary ก่อน claim งานใหม่ใด ๆ สั่ง
`pf-adversary` รีวิวโค้ดที่ merge แล้วตั้งแต่ต้นรอบ ผลกลับมา **ไม่สะอาด**: F1 [HIGH]

**F1**: `QUEST_FLAG_UNREADABLE = -1` (round `yd9u99`) ปลอดภัยก็ต่อเมื่อไม่มี writer ไหนเขียนค่านอกช่วง
`0..0xFFFF` ลงแถว `character_quest_flag` — จริงเฉพาะสอง closure ที่ผ่าน `_coerce_int` (`SetFlag`/`SetQuestFlag`)
แต่ `store.py` **ไม่บังคับช่วงเอง** (`flag_value` เป็น opaque ตามคำตัดสิน COO) และเทสของ `store.py` เอง
(`test_negative_flag_values_are_stored_as_given`) พิสูจน์ว่าค่าลบถูกเก็บตามที่ให้มาจริง ⇒ writer ตัวอื่นในอนาคต
(เครื่องมือ GM, migration, สายอื่น) เขียน `-1` ตรง ๆ ได้ และจะชนกับ sentinel ทันที **ไม่ถูกใช้ประโยชน์ได้จากคอร์ปัส
วันนี้** (มีแค่สอง closure ที่เขียนแฟล็ก) แต่ **ไม่มีการป้องกันที่ชั้นซึ่ง LANE-Q เป็นเจ้าของเลย**

**ทางแก้**: เพิ่ม bounds-check ที่ `StoreBackedQuestStateStore.get_quest_flag`/`set_quest_flag`
(`quest_state_store.py`) — แถวที่มีค่านอก `0..0xFFFF` (ไม่ว่าจากการอ่านหรืออ่านกลับหลังเขียน) ถูกปฏิเสธเป็น
`unreadable-row` แทนที่จะถูกส่งกลับตรง ๆ ซึ่งอาจเท่ากับ `QUEST_FLAG_UNREADABLE` พอดี · ตัวนับ (`counter`) **ไม่ถูก
จำกัดช่วงแบบนี้** โดยตั้งใจ — ไม่มีหลักฐานในโปรเจกต์ว่ามีเพดานของตัวนับ มีแค่ของแฟล็ก

F4/F5 [ข้อสังเกต ไม่ใช่ของเสีย]: "once per ledger" ยังไม่มีผู้เรียกโปรดักชันจริงมาพิสูจน์ (D1 เดิมยังเปิดอยู่) —
บันทึกไว้ ไม่ใช่งานใหม่ · F2/F3/D8 ยืนยันสะอาด

## 3. งานหลัก B — ปิดใบ `.tgr` (trigger id → ไฟล์สคริปต์) ที่ตกมาสามรอบติด (`7qw2tr`/`7cf5ak`/`z113cx`)

จดหมาย `20260908_2230_RE-273-RESULT-TGR-ORDINAL-COPIES-TO-WIRE-TAG-0F.md` (จ่าหน้า LANE-Q ตรง ๆ) **ค้างไม่มี
stub มาตั้งแต่ 22:30 ของเมื่อวาน** — คำถามที่ตกมาสามรอบมีคำตอบรออยู่แล้วในกล่องจดหมาย ไม่ใช่ยังไม่ได้ถาม
คำตอบ: **ใช่** ordinal ที่ฝังใน `.tgr` เป็นฟิลด์เดียวกับ `TriggerVital` tag `0x0F` — พิสูจน์จาก data flow ของ
ไคลเอนต์เอง (`record+0x4E` → คัดลอก 16 บิต → `vital+0x14` → serializer เขียนด้วย tag `0x0F`) ไม่ใช่ "ตัวเลข
คล้ายกันเอาไปจับคู่"

**ทำ**: แก้ `lane_hooks/lane_q_trigger_vital_dispatch.py` (docstring + log key `WIRE_NATIVE_ID_EQUALS_TGR_
ORDINAL_RE273` แทน `..._UNPROVEN_...`) + `docs/SCRIPT_LANE.md` ให้ตรงกับผลจริง · registry key **ไม่เปลี่ยน**
(เป็น wire id เดิมเสมอ ซึ่งตอนนี้พิสูจน์แล้วว่าเท่ากับ ordinal)

**ยังไม่รันสคริปต์จริง** — เหตุผลเปลี่ยนจาก "crosswalk ยังไม่พิสูจน์" เป็น "ข้อมูล ordinal→ชื่อไฟล์ ต่อฉากยังไม่ถูก
สกัดเป็นตารางที่คอมมิตไว้" (เช็คแล้วรอบนี้: `gamedata/scene/*/*.placements.tsv` มีแค่ mob-set ไม่มี trigger record
· dump เต็มมีแค่ `Bg3001` ตัวเดียวใน `RE-289` ซึ่งเป็นจดหมาย ไม่ใช่ตาราง) — **ใบเปิดต่อ = ใบขอสกัดข้อมูลเพิ่ม
(RE ticket ต่อฉาก) ไม่ใช่คำถาม crosswalk อีกแล้ว**

## 4. งานหลัก C — เคลียร์กล่องจดหมาย: 13 ใบจ่าหน้า LANE-Q ที่ไม่มี `.CONSUMED.txt`

grep ผิด pattern ของรอบก่อน (ข้อ 1) ทำให้กล่องจดหมายจริงไม่เคยถูกเช็คตั้งแต่รอบ `bxly5p` — สแกนใหม่ด้วย
`grep -l "ADDRESSEE:.*LANE-Q\b" notes_to_chief/*.md` แล้วกรองใบที่ไม่มี stub เจอ 13 ใบ (ส่วนใหญ่เก่า/เนื้อหาถูกใช้
ไปแล้วโดยไม่มีใครแปะ stub ให้):

| ใบ | สถานะ |
|---|---|
| `20260909_1452_...q1351...lua-host-is-yours` | **ใหม่ ยังไม่ทำ** — COO ตัดสิน `lua_api/` ทั้งหมดเป็นเขต Q (รวม `player.py`) ⇒ `RefusalLedger`/`unreadable_reason` ต้องมองเห็น `Player.AddItem`/`RemoveItem`/`Quest.RewardItemSelect` ด้วย ไม่ใช่แค่ `Quest.*` — **ยอมรับ ยังไม่ implement รอบนี้** (งานใหม่จริง ไม่ใช่แก้บรรทัดเดียว) คิวไว้เป็นงานแรกรอบหน้า |
| `20260909_1312_...q2226...two-way-test` | **ใหม่ ยังไม่ทำ** — COO รับรูป (ค) (เทส `no-item-minter` + เรียก `mint_item_attr_state` ผ่าน fake) แทนเทสแดง — ยังไม่ implement เพราะ scope ถูกครอบโดย q1351 (ข้างบน) แล้ว รวมคิวเดียวกันรอบหน้า |
| `20260908_2230_RE-273-RESULT` | **ทำแล้วรอบนี้** — ข้อ 3 |
| `20260908_1752_...five-quest-state-doors...` | เนื้อหาถูกใช้แล้วโดยรอบ `7cf5ak` เอง (independent re-measure) — ข้อเดียวที่ยังเปิดคือสาย D1 (`persistence=None` ไม่มีผู้เรียกจริง) ที่ carry-over อยู่แล้ว ไม่ใช่งานใหม่จากใบนี้ |
| `20260908_1520_...quest-flag-store-first` | ทำแล้วหลายรอบก่อน (`l8ayrt`/`7qw2tr`/`7cf5ak`) — docstring ของ `quest_state_store.py` อ้างใบนี้ตรง ๆ |
| `20260908_1742_...refusal-is-a-third-state` (`COO-DECISION 1742`) | ทำแล้ว — `quest.py`/`quest_state_store.py` อ้างเลข `1742` ตรง ๆ ในดอกสตริงหลายจุด |
| `20260908_1742_...you-read-the-owners-order-correctly` | ครอบโดยคำตัดสินหลังจากนั้น (`1846`/`1941`/`2050`/`2220`/`q1351`/`q2226`) ไม่มีข้อสั่งที่ยังค้าง |
| `20260908_2220_...no-self-imposed-ceilings` | เป็นบรรทัดยืนของ `NOW.md` แล้ว (`PANYA 2220`) — รอบนี้อ่าน NOW.md เป็นไฟล์แรกตามโปรโตคอล ไม่ตั้งเพดานใหม่ใด ๆ |
| `20260909_0150_SYNC-NOTICE-...pr1967...` | claim ผีของรอบ `x173t2` ถูก reap ไปแล้ว (>3 ชม. ไม่มีไฟล์รอบ) — ไม่มีงานสูญหาย (มีแค่ `_claim.md` บนกิ่งนั้น) |
| `20260908_0442_...ALL-LANES` / `20260908_1142_...ALL-LANES` | รายการของ Q (สคริปต์ pin/`Player.RemoveItem`) ถูกทำและถูกแทนที่ไปหลายรอบแล้ว |
| `20260907_0039_...npc-visibility-rank-rule` | `is_quest_accepted`/`is_quest_reported` ใน `quest.py` คือคำตอบของใบนี้ ทำไปแล้วหลายรอบก่อน |
| `20260906_1704_...host-api-map-fn-to-system` | ถูกแทนที่โดย `COO-DECISION 20260906_1846` ที่ละเอียดกว่า ซึ่ง `quest.py` อ้างจริง |

ทุกใบวาง `.CONSUMED.txt` + สำเนา `consumed/` แล้ว (13 คู่) — **ไม่มีใบไหนถูกลบต้นฉบับ**

## 5. เขตที่จงใจไม่แตะ

`store.py` / `migrations/` / `runtime.py` / `app.py` / `v141` / registry ของ A / combat state ของ B ·
D3/D5 (คำถามใหญ่ของ addendum `z113cx`: "การตัดสินใจนี้เป็นเรื่องของแถวไหน") — **ยังไม่แตะรอบนี้เช่นกัน**
เหตุผล: เวลารอบนี้หมดไปกับหนี้ adversary (บังคับ ก่อน claim งานใหม่) + กล่องจดหมาย 13 ใบ (บังคับ อยู่เหนือ
"งานค้างของรอบก่อน" ตามลำดับความจริงของ `COMMON_LANE_ROUND.md`) — ไม่ใช่ขี้เกียจ เขียนไว้ตรง ๆ

## 6. หลักฐาน

- เทสเฉพาะจุด (F1): `tests/test_script_lua_quest_state_store.py` เพิ่ม 3 เทสใหม่ (ค่านอกช่วงตอนอ่าน · ค่านอกช่วง
  ตอนอ่านกลับหลังเขียน · ขอบเขต `0`/`0xFFFF` ยังผ่าน) — กลุ่มที่แตะ (`test_script_lua_quest_state_store.py`
  `test_script_lua_quest_refusal_third_state.py` `test_script_lua_api_quest.py` `test_script_lua_api_quest_
  criteria.py` `test_persistence_quest_state.py` `test_script_lua_corpus.py` `test_script_lua_api_reward.py`
  `test_lane_q_trigger_vital_dispatch.py`): **332 passed, 31 skipped (lupa ไม่มีในแซนด์บ็อกซ์นี้), 5454
  subtests passed** ก่อน merge
- **ชุดเต็ม (`pytest tests/`) บน `origin/main` ที่ merge แล้ว (ก่อนแก้ของรอบนี้)**: **15711 passed, 446 skipped,
  0 failed** ใน 731.66s — **ยืนยันแล้วจริง** (งานที่ยด9u99/`z113cx` ทิ้งไว้ว่ายังไม่คืนผล ปิดรอบนี้)
- **ชุดเต็มบนกิ่งของรอบนี้ (หลังแก้ F1 + RE-273, `PYTHONPATH=src pytest tests/`)**: **15714 passed, 446 skipped,
  0 failed** ใน 720.08s (`0:12:00`) — เขียว ยืนยันก่อน push จริง ไม่ใช่คำอ้าง (3 เทสเพิ่มจาก F1's fix เทียบกับ
  15711 บน `origin/main` ที่ยังไม่แก้ ตัวเลขที่เหลือเท่ากันทุกตัว)
- `tools_bridge/pf_gate_preflight.py --repo`: **PASS** ทุกแถวที่กิ่งนี้กระทบได้ (cp874/skips/mainmerge/census/
  branch/bridgesize/queuegrowth/filenamelen/scoreboard-manual/claudecfg/consumedstub/modebits)

## 7. สิ่งที่ผม **ไม่ได้** อ้าง

- ไม่อ้างว่า D3/D5 (คำถามใหญ่ของ addendum) ตอบแล้ว — ยังไม่แตะเลยรอบนี้ (ข้อ 5)
- ไม่อ้างว่า `Player.AddItem`/`RemoveItem`/`RewardItemSelect` มี ledger visibility แล้วตาม `q1351` — ยอมรับ
  ยังไม่ implement (ข้อ 4)
- ไม่อ้างว่าสคริปต์ trigger ตัวไหนรันจริงจากงาน .tgr รอบนี้ — ยังไม่มี ScriptHost ถูกสร้าง ยังไม่มี `.lua` ไฟล์ไหน
  ถูกโหลด (ข้อ 3)
- ไม่อ้างว่า pf-adversary รีวิวรอบนี้เอง (F1's fix) แล้ว — ยังไม่สั่งซ้ำบนกิ่งที่มีการแก้ F1 (ดู "รอบหน้าทำอะไร")
- ไม่มีชื่อไหนย้ายเข้า/ออก `REAL_METHODS` ใน `docs/SCRIPT_LANE.md` — ทั้งสองการแก้เป็นการปิดหนี้ ไม่ใช่ implement
  API ใหม่

## 8. สถานะที่ส่งมอบ

- `pirate-force-server` กิ่ง `claude/happy-tesla-7mdavp` (`84098fc4` F1 fix · `281c160e` RE-273 consume) —
  **ยังไม่เปิด PR ตอนเขียนบรรทัดนี้** รอชุดเต็มคืนผลก่อนเปิด ตามกฎ "รันชุดเต็มครั้งเดียวต่อรอบเป็น commit
  สุดท้ายจริง" — จะเปิดทันทีที่ชุดเต็มเขียว ไม่ draft มี `PF-AUTOMERGE: v4`
- `pf_bridge#1987` = claim ของรอบนี้ — ปลดล็อกหลังไฟล์นี้ + จดหมาย stub 13 คู่ลงกิ่งและ PR เซิร์ฟเวอร์เปิดแล้ว

## รอบหน้าทำอะไร (เรียงแล้ว)

1. 🔴 **สั่ง `pf-adversary` บนกิ่งที่มีการแก้ F1 เป็นงานแรก** ก่อน claim งานใหม่ — F1's fix เองยังไม่ผ่านรีวิว
2. 🔴 **ยืนยันชุดเต็มบนกิ่งของรอบนี้คืนผลแล้วเป็นอะไร** — ถ้ายังไม่คืนตอนรอบนี้ปิด ต้องยืนยันก่อนอ้างว่าเขียว
3. 🔴 **`q1351`/`q2226` (เขต Q = `lua_api/` ทั้งหมด)**: ขยาย `RefusalLedger`/`unreadable_reason` ให้มองเห็น
   `Player.AddItem`/`Player.RemoveItem`/`Quest.RewardItemSelect` + เทส `no-item-minter` (shape (ค) ที่ COO รับ)
4. **D3+D5** (คำถามใหญ่ของ addendum `z113cx`, ข้อ 4 ในไฟล์นั้น) — ยังไม่แตะเลยสองรอบติดแล้ว (`yd9u99` + รอบนี้)
   อย่าให้ตกรอบที่สาม
5. **D2 ทางเต็ม**: admission ต่อตัวละคร (ตอนนี้ทำแค่ "ส่งเสียง" ไม่ใช่ "แฟร์")
6. **D1** (`persistence=None` ผู้เรียกจริงของ `resolve_quest_state_store`/`load_quest_script`) — carry-over มาจาก
   `l8ayrt` ผ่าน `z113cx` ผ่าน `yd9u99` ผ่านรอบนี้
7. **ใบขุดตารางเพิ่มเติม** (มากกว่า `Bg3001`) ถ้า M2 ของ LANE-A ต้องการฉากอื่น — ไม่ใช่ crosswalk อีกต่อไป (ข้อ 3)
   เป็นงาน static RE ตามปกติ ไม่ด่วนเว้นแต่ A ขอ

SCOREBOARD: COMING | ไม่มีอะไรใหม่ที่ผู้เล่นทำได้เพิ่มรอบนี้โดยตรง — รอบนี้เป็นรอบเคลียร์หนี้: ปิดช่องโหว่ที่ pf-adversary เจอในของรอบก่อน (แถวแฟล็กที่ค่าหลุดช่วงจะหน้าตาเหมือน "อ่านไม่ได้" ทั้งที่ไม่ใช่) ปิดคำถาม RE ที่ตกมาสามรอบ (crosswalk trigger id พิสูจน์แล้ว) และเคลียร์กล่องจดหมาย 13 ใบที่ค้างเพราะ bug ในเครื่องมือค้นของรอบก่อน (grep pattern ผิด) ทำให้กล่องดูว่างทั้งที่มีของจริงรออยู่ รวมคำตัดสินขยายเขตของ Q ทั้งเลนที่ยังไม่ได้ implement | pirate-force-server claude/happy-tesla-7mdavp (84098fc4, 281c160e, ยังไม่เปิด PR รอชุดเต็ม) + pf_bridge#1987
