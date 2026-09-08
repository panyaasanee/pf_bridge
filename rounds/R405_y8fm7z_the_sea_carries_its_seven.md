# R405 · `y8fm7z` · [LANE-E] — ทะเลพาลูกเรือของมันไปด้วย และกองทัพร้างจะไม่ยืนอยู่กลางน้ำอีก

เริ่ม 2026-09-08T18:22+07:00 · ล็อก `pf_bridge#1939` · กิ่ง `claude/loving-wozniak-y8fm7z` / `claude/great-franklin-y8fm7z`

## 0. รอบนี้ขยับ NOW ข้อไหน
`NOW.md` "งานด่วนตอนนี้ · chief": ลำดับคือ `0206`+ริด §0 (จ่ายแล้ว R403) → **Columbus/`bg1001_roster`** ← **รอบนี้** → `CORE-REQUEST 1553` → ครึ่งผู้เล่น R4 → `GM-058` → walk+หมุด 32→38
ขยับ **M2** ("ออกจากเมืองได้") ชิ้นสุดท้ายที่ผู้เล่นเห็นด้วยตา: ข้ามไปฉาก 17 แล้วทะเล**มีคนอยู่** ไม่ใช่ทะเลว่าง

## 1. ตรวจต้นรอบ
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 B) ✅
- ล็อกรอบ: list `pf_bridge` open PR — ไม่มีใบ `[LANE-E] round *: claim` ⇒ เปิด `#1939` แล้ว list ซ้ำ: `#1939` ใหม่สุด สายอื่นทั้งหมด ⇒ ล็อกเป็นของผม
- ชะตา PR รอบก่อน: `pirate-force-server#1157` (R404) **ยังเปิด รอเกต/รอ reaper** — ไม่ใช่ล็อกของรอบนี้ ไม่ถอย (`COMMON` ล็อกรอบ ข้อ 1)
- 🔴 **สะพานค้าง**: `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด `2026-09-08T16:08:01+07:00` ห่างจากเวลาที่วัด (18:22) **134 นาที** > 60 ⇒ ตรวจนาฬิกาตัวเองกับหลักฐานอิสระตามที่ `COMMON` สั่ง: `pf_bridge#1939` `created_at` = `2026-09-08T11:23:18Z` = **18:23 +07** ตรงกับนาฬิกาผม ⇒ **นาฬิกาไม่ผิด สะพานค้าง** — push ต่อตามกฎ ไม่หยุดรอบ
- ไม่มี `LOCK_*.txt` ใน `git status` ทั้งสองรีโป

## 2. CORE-REQUEST ที่ค้างของทุกสาย (ก่อนงานอื่น)
| ใบ | สาย | สถานะรอบนี้ |
|---|---|---|
| รอบ `vwekfq` — `bg1001_roster` ถูกกันออกจาก `ROSTER_COMPOSERS` รอ chief ตรวจ `runtime.py` | LANE-A | ✅ **ตอบแล้วด้วยโค้ดรอบนี้** (ข้อ 3) |
| `CORE-REQUEST-GM-058` ตัวตนต่อคอนเนกชัน | LANE-GM | รับใบ · COO (`1742`) วางไว้ **หลังครึ่งผู้เล่นของ R4** — ไม่แซง `PANYA 1420` · ตอบเป็นจดหมายรอบนี้ ไม่ใช่โค้ด |
| `_discover()` / `ui_dispatch.adopt_answerer` | LANE-UI | ❌ **ยังเสียบไม่ได้** — วัดเองรอบนี้บน `origin/main` (`48eaf82`): `grep -rn "adopt_answerer" src/` = **0 hit** ⇒ ฟังก์ชันยังไม่อยู่บน main · ตัวบทอยู่ในใบตอบ R404 แล้ว เสียบรอบแรกที่มันโผล่ |
| `CORE-REQUEST 1553` | — | คิวถัดไปของผม (ยังไม่แตะรอบนี้) |

WIRED = 287 ไฟล์ใน `src/pirateforce_foundation/` ที่เอ่ย `production_allowed` / 10 scenario ที่ `"production_allowed": true` — **[เสนอ]** ไม่ใช่ [วัดแล้ว] เพราะเป็น grep ไม่ใช่ emission census ตาม WIRED v2 · ตัวนับ emission จริง (`tools/pf_runtimeres_actor_entry_static.py`) ยังตาบอด 32/38 และเป็นคิวข้อ 5 ของผมเอง

## 3. งานหลัก — ตอบ CORE-REQUEST `vwekfq` ด้วยของที่วัดได้ ไม่ใช่ด้วยเหตุผล
`pirate-force-server` กิ่ง `claude/great-franklin-y8fm7z` คอมมิต `866182f`

### สิ่งที่ใบนั้นถาม
สาย A สร้างนักแสดง 7 ตัวของฉาก 17 เสร็จแล้ว (`world_bg1001_identity` / `world_population_bg1001`) และลงทะเบียนใน `world_scene_travel.CENSUS_SOURCES` แล้ว **แต่จงใจไม่ใส่** ลง `world_population_handoff.ROSTER_COMPOSERS` เพราะเชื่อว่า `runtime.py` จุดเรียก Columbus "ฮาร์ดโค้ด `crossing_handoff_dispatched=True` บนสมมติฐานว่าตะเข็บนี้ตอบ `KIND_CLEAR` เสมอ" — คำถามที่สาย A แก้เองไม่ได้เพราะไม่มีสิทธิ์เขียน `runtime.py`

### สิ่งที่ตรวจแล้ววัดได้ (headless บน encoder แช่แข็งจริง ที่ entry ของ Columbus จริง)
1. **จุดเรียกใน `runtime.py` เป็น generic อยู่แล้ว** — อ่าน `sends_a_frame` · `dispatch_slot` · `reapply_ms` · `membership_reset` · `kind` · `scene_id` **กลับออกมาจาก handoff** ไม่ฮาร์ดโค้ดสักตัว · `crossing_handoff_dispatched=True` เป็น**ฟิลด์ของบรรทัดคอนโซล** (`dispatched=YES`) ใน `columbus_quest_dispatch` ไม่ใช่คำยืนยันเรื่อง kind
   ```
   ก่อน:  clear  pc=  17B frame=  27B slot=before_teleport reapply=None actors=0
   หลัง:  census pc=1377B frame=1390B slot=after_teleport  reapply=3000 actors=7
   ```
   ประกอบสองครั้งต่อหนึ่งการข้าม (บรรทัดคอนโซลหนึ่ง · ไบต์ที่ runtime คิวอีกหนึ่ง) — **วัดว่าไบต์เท่ากันเป๊ะทั้ง `pc` และ `frame`** เพราะโรสเตอร์นี้อ่านตารางแช่แข็ง ไม่มีนาฬิกา ตัวนับ หรือ RNG
2. 🔴 **สิ่งที่ใบนั้นถูกจริง ๆ และไม่ใช่จุดเรียก**: การลงทะเบียน composer **ตัวใดก็ตาม** เปลี่ยน CLEAR ที่**การันตี** ของฉากนั้น ให้กลายเป็น `KIND_UNAVAILABLE` ที่**เป็นไปได้** · วัดโดยทำให้ builder `raise`:
   ```
   kind=unavailable sends_a_frame=False pc=0B
   ```
   UNAVAILABLE **ไม่ส่งเฟรมเลย** ⇒ ไคลเอนต์ถือนักแสดง 115 ตัวของท่าเรือยืนอยู่กลางทะเลเปิด — **แย่กว่าทะเลว่างที่มีอยู่วันนี้** และเป็นสภาพเดียวกับที่ docstring ของโมดูลบอกว่าตัวเองมีไว้เพื่อจบมัน
3. **ยังไม่มีใครเห็นบนจอ** — `GT-106` (attended 2026-08-27) เดินฉาก 17 แล้วพบว่า**ว่างเปล่าไม่มีนักแสดงเลย** นั่นคือทั้งหมดของบันทึก attended

### จึงส่งของสองชิ้นในใบเดียว (ชิ้นที่สองคือเหตุผลที่ชิ้นแรกปลอดภัย)
- `handoff_on_crossing` (เส้นทางเฟรม สัญญาว่า**ไม่ raise เด็ดขาด**) ตอนนี้ให้ฉากที่ **ตั้งชื่อได้** ตกไปที่ **CLEAR ของฉากนั้น** พร้อมเหตุผลที่ระบุความล้มเหลว แทนที่จะเป็น "ไม่มีเฟรมเลย" · ฉากที่ **อ่าน scene id ไม่ออก** ยังเป็น UNAVAILABLE เหมือนเดิม (ไม่มีฉากให้ประกอบ clear ให้) · composer ทุกตัวได้ตาข่ายนี้ ไม่ใช่แค่ bg1001
- `bg1001_roster` เข้า `ROSTER_COMPOSERS` · `PENDING_CROSSING_SAFETY_REVIEW` ว่างแต่**ไม่ลบตาราง** (เหตุผลเขียนไว้ที่ตาราง)

🔴 **ร่างแรกวางตาข่ายผิดที่แล้ววัดเจอ**: วางไว้ใน `handoff_for_arrival` (ทางที่เอกสารเขียนว่า STRICT) ⇒ กลืน `_require_pair` และ `encoder or reader drift` ของ `_roster_handoff` ไปด้วย — **เทสปฏิเสธสามใบใน `test_world_population_handoff` กลายเป็นเขียวที่ไม่ยืนยันอะไรเลย** ย้ายลงเส้นทางเฟรมซึ่ง "ไม่ raise" เป็นสัญญาอยู่แล้ว บันทึกไว้ในคอมเมนต์ตรงจุด

### หมุดที่ปลด (ปลด ไม่ใช่ลบ — เหตุผลอยู่ที่หมุด)
`test_world_population_handoff` · `test_world_m2_crossing_handoff` · `test_lane_a_scene17_roster_does_not_touch_gt233` · `test_world_population_bg1001` (โมดูลถูก seam import แล้ว = เท่ากับ composer พี่น้องทุกตัว) · `test_columbus_quest_dispatch_wiring` · `test_world_population_handoff_wiring`
`test_gm_warp_chain_census_shipped` — helper เลิกกรองด้วยตารางที่ว่างแล้ว หันไปถาม `lane_a_scene_census.scene_is_open_to_players` ซึ่งเป็น**ประตูของเส้นทางนั้นเอง**: ประตูล็อกอินของฉาก 17 ยัง**ปิด** ⇒ GM `/warp 17` ยัง**มาถึงทะเลว่างเหมือนเดิม` · สองตะเข็บ สองคำตอบ และใบนี้ไม่อ้างข้ามตะเข็บ

## 4. หลักฐานสองชั้น (ห้ามรวมข้ามชั้น)
- **wire/DB [วัดแล้ว]** — บูต headless เต็มรูปผ่าน `make_state_class` (เทส `test_columbus_quest_dispatch_wiring`): action list ของการข้ามจริงมี `WORLD_POP_HANDOFF_...` **หลัง** `CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE` พร้อม `_REAPPLY` ตามหลัง · frozen state `population_indices` = `(6, 1, 2, 3, 4, 0, 5)` (7 ตัว) anchor `(0.0, 0.0, 0.0)` · event `world_m2_crossing_handoff_census_scene_17` · คอนโซล:
  `WORLD_M2_CROSSING_HANDOFF scene=17 kind=census held=108 composed=YES dispatched=YES pc=1377B frame=1390B slot=after_teleport reason=scene_17_repopulated_from_bg1001_roster`
- **client-observable** — **ไม่มี ยังไม่มีใครเห็น** `GT-106` เดินฉาก 17 พบว่าว่าง เป็นบันทึกทั้งหมดที่มี ⇒ เนื้อใบ attended ส่งให้ LANE-K รอบนี้ **ไม่มี `OBSERVER_CONFIRMED` และห้ามเขียนว่ามี**
- **nonclaims**: (ก) ไม่อ้างว่าไคลเอนต์วาดนักแสดงเจ็ดตัวได้ (ข) ตาราง identity ของ A ติดป้าย `[PROPOSED]` ทั้งแผง (ไม่มี control ตกลงเรื่องชนิด CLINE) — รอบนี้ไม่แตะและไม่เลื่อนชั้นให้ (ค) ไม่อ้างว่า GM `/warp 17` เห็นอะไรเพิ่ม (ง) ไม่แตะ `login_entry_allowed` ของฉาก 17

## 5. TWO_SESSIONS_SAME_SCENE
ไม่มีฟิลด์ใหม่และไม่มีสถานะร่วมใหม่ · `_roster_handoff` เป็น pure composition จากตารางแช่แข็ง + anchor ที่ผู้เรียกส่งมา และ `membership_reset` ถูกเขียนลง frozen state **ของ connection ตัวเอง** (`self.population_indices` / `self.world_census_indices`) ⇒ ผู้เล่นสองคนที่ข้ามไปฉาก 17 พร้อมกันได้ไบต์ชุดเดียวกันคนละสำเนา ไม่มีใครเขียนทับ membership ของใคร · ตาข่าย CLEAR ก็เป็น per-call เช่นกัน · registry ของ LANE-A ไม่ถูกแตะรอบนี้

## 6. QUEUE_TRIAGE
`QUEUE_TRIAGE:` เพิ่มเนื้อใบใหม่หนึ่งใบ (ส่งให้ LANE-K ตั้งเลข — `NOW §11` ยกการตั้งเลขให้ K แล้ว) = **M2-SEA-CAST-ON-ARRIVAL** · ไม่ถอน ไม่ยกเลิกใบใด · ไม่ archive รอบนี้
`READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ:` ไม่มีใบใหม่ที่พร้อมบูตนอกลำดับของ `NOW` — ใบใหม่ของผมต้องต่อท้าย `GT-304` และ **ไม่แซง `GT-309`** เพราะบูตเดียวกันคือบูต M2 (เขียนไว้ในเนื้อใบแล้ว)
🔴 **ของค้างที่ผมไม่ได้ทำรอบนี้ และไม่เงียบ**: `GAME_TEST_QUEUE.md` = **989 KB** เกินเพดาน 300 KB ของ `NOW` อยู่มาก (preflight ผ่านเพราะเกตวัด**การโต** ต่อ PR ไม่ใช่ขนาดสัมบูรณ์) ⇒ งานแม่บ้าน `§17 ข้อ 9` เป็น **PR แยกใบเล็กของรอบหน้า** ไม่ยัดเข้าใบนี้

## 7. adversary
`ADVERSARY_PENDING pirate-force-server#<PR ของรอบนี้>` — สั่ง `pf-adversary` ตั้งแต่ต้นรอบพร้อมเริ่มงาน โจทย์คือ**หักล้าง**ข้อความว่า "จุดเรียก Columbus เป็น generic อยู่แล้ว จึงลงทะเบียน composer ได้เลย" ผลยังไม่คืนตอน push ⇒ push ตามกฎ · **ห้ามอ่านใบนี้ว่า "ผ่าน adversary"**
รอบถัดไปของ LANE-E: สั่ง adversary บนกิ่งนี้เป็นงานแรก แล้วจ่ายข้อที่เป็นของแพตช์นี้เอง

## 8. รอบหน้าทำอะไร
1. **งานแรก**: ผล `pf-adversary` ของกิ่ง `claude/great-franklin-y8fm7z` — จ่ายข้อที่เป็นของแพตช์นี้ในรอบเดียวกัน
2. เสียบ `_discover()` ของ CORE-REQUEST LANE-UI ทันทีที่ `ui_dispatch.adopt_answerer` อยู่บน main (ยืนยันด้วย `git merge-base --is-ancestor` ไม่เชื่อจดหมาย)
3. `CORE-REQUEST 1553` → ครึ่งผู้เล่นของ R4 → `GM-058` (ลำดับของ COO `1742` ห้ามสลับ)
4. งานแม่บ้าน `§17 ข้อ 9` เป็นใบเล็กแยก: `GAME_TEST_QUEUE.md` 989 KB
5. ของค้างจาก R404 ที่ยังไม่จ่าย: **D-G** ป้าย `..._QTY2_COMMITTED` ยังฮาร์ดโค้ด QTY2 · **D-F** สาขา `if not applied:` เข้าไม่ถึง · **D-D/D-I** เกต HYP-008 เป็น tautology + `runtime.py` รับกว้างกว่า `store.py` (ครึ่งหนึ่งอยู่เขต LANE-DB อยู่ในจดหมายถึงเขาแล้ว)
6. `tools/pf_runtimeres_actor_entry_static.py` walk ทั้งต้นไม้ + หมุด 32→38 คอมมิตเดียว (`1441` ข้อ 4)

SCOREBOARD: COMING | ข้ามทะเลไปเกาะแล้วทะเลมีเรือ/คนของมันเจ็ดตัว แทนที่จะเป็นน้ำเปล่า และถ้าประกอบไม่สำเร็จผู้เล่นได้แผนที่ว่างแทนกองทัพท่าเรือที่ยืนค้างกลางน้ำ | pirate-force-server กิ่ง `claude/great-franklin-y8fm7z` `866182f` (PR เปิดท้ายรอบ) + เนื้อใบ attended ส่ง LANE-K
