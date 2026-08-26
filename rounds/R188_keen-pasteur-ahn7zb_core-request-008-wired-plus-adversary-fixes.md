# R188 — chief cloud (`keen-pasteur-ahn7zb` / server: `optimistic-mccarthy-ahn7zb`)
2026-08-27 ~09:0x-11:3x (+07:00)

## งานหลักของรอบ: ต่อสาย `CORE-REQUEST-008` (v6.1 หัวข้อ 17 บังคับก่อนงานอื่น)

### สิ่งที่ทำ

1. **การ์ดกันรอบซ้อน**: ไม่มี `[LANE-E]`/`WIP round claim` PR เปิดค้างทั้งสอง repo (มีแค่ `[LANE-A]`/`[LANE-B]`
   ซึ่งไม่ใช่ล็อกของสาย E) ⇒ จับล็อกด้วย draft PR `pf_bridge#167`, `pirate-force-server#93`
2. **ยืนยันโครงพี่น้อง**: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง — ไม่หยุดงาน
3. **ต่อสาย `CORE-REQUEST-008` (สาย B)**: อ่านจดหมาย `20260827_1015_LANE-B-REPLY-*` — สาย B สร้างครึ่ง pure-logic
   เสร็จแล้ว (`mob_death.hostile_census_frames`, บน main แล้ว) เหลือ 3 จุดใน `runtime.py` ให้ chief ต่อสาย:
   `MOB_COMBAT_BAR` (`_dispatch_mob_combat` ~3833), `MOB_DEATH_DYING`/`MOB_DEATH_DEAD` (~3962) ต่อสายครบทั้งสาม
   จุดตามสเปคที่จดหมายเขียนไว้ (anchor/count จาก session state, `roster` จาก `field_mobs.load_roster()`,
   `register=self.mob_death_register` **หลัง** commit, `ledger=self.mob_combat_ledger`,
   `dead_timer=DYING_TIMER_SECONDS` เฉพาะเฟรม dying)
4. **เทสใหม่**: `tests/test_mob_combat_census_wiring.py` (7 เทส) — ขับ arrival census ก่อนแล้วค่อยโจมตี (ไม่มีไฟล์
   เทสไหนเดิมทำแบบนี้ — เทสเดิมทั้งหมดโจมตีก่อนมี census จึงชน fallback branch เสมอ ไม่เคยพิสูจน์ path จริง)
   ยืนยัน bar/dying/dead frame ตรงกับการเรียก `hostile_census_frames` อิสระ byte-exact + มี actor อื่นที่ไม่ใช่
   เป้าหมายอยู่ในเฟรมด้วย (พิสูจน์ไม่ใช่ one-entry อีกต่อไป)
5. **`pf-adversary` (บังคับก่อน commit)** พบสองข้อจริง แก้ทั้งคู่ในรอบเดียวกันก่อน push:
   - **[HIGH]** ไม่มี fail-closed guard รอบ `hostile_census_frames` (เวอร์ชันแรก) — exception จะฆ่า listener
     thread แทนที่จะแค่ส่งเฟรมผิด (หนักกว่าบั๊กเดิม) ⇒ ห่อ `try/except Exception` ตกไปที่ one-entry frame +
     event `*_census_compose_refused_<ExceptionType>`
   - **[MEDIUM]** ไม่มี scene guard — `population_refresh_anchor`/`world_census_actor_count` ถูกเซตแยกจากกันได้
     (arena harness) และไม่มีอะไรล้างตอนออกฉาก ⇒ เพิ่ม guard `scene_id == world_population.SCENE_ID` ก่อนเชื่อ
   - **[LOW-MEDIUM]** คอมเมนต์ "unreached today" เท็จ (เทสของผมเองพิสูจน์ว่าไปถึงได้จริง) ⇒ แก้คอมเมนต์
   เพิ่มอีก 3 เทส (compose exception ×2, scene mismatch ×1) รวมเป็น 7 เทสในไฟล์ — ทั้งหมดผ่าน
6. **หลักฐาน**: สวีตเต็ม เขียว(cloud sanity) `2432 passed, 8 skipped` (skip ตรงตาม
   `docs/PYTEST_SKIP_PINS.json` ทุกใบ มีเหตุผลกำกับ) · บูต headless ยืนยันคอนโซล
   `MOB_COMBAT_BAR_CENSUS_RECOMPOSE actor_count=115 target=0x201F` และ
   `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE actor_count=115 target=0x201F` พิมพ์จริง (ตามด่านคอนโซลของ COO 03:45)
   push `pirate-force-server@741ab5d`
7. **เปิด `RE-098`** ให้สาย C ตามที่ขอไว้ในใบ `20260827_1030_LANE-B-REPLY-PANYA-ORDER-*` (ข้อ 4 ที่สาย B ตอบไม่ได้
   ในเขตตัวเอง — parser definition payload 16 ไบต์ต่อ `.npc` เทียบ level/rank/spawn-rate)
8. **อัปเดตริเดอร์ `GT-084`/`RIDER-084-A`**: append บรรทัด "static/wire risk ปิดแล้ว, client-observable ยังเปิด"
   ไม่แก้ P1-P5/objective/pass-criteria เดิมแม้แต่ตัวอักษรเดียว
9. **เคลียร์กล่องจดหมาย**: consume 3 ใบ (`0920` ของ chief เอง, `1015`, `1030` จากสาย B) — สำเนาไป `consumed/` +
   วาง stub ตามธรรมเนียม `COO-DECISION 2146`

### WIRED

ไม่มีเลนใหม่เข้า `production_allowed` รอบนี้ — งานคือทำให้เลน `mob_combat`/`mob_death` ที่ต่อสายอยู่แล้ว
(ตั้งแต่ก่อนรอบนี้) ปลอดภัยขึ้น ไม่ใช่การต่อสายเลนใหม่ ⇒ ตัวเลข `WIRED v2` ไม่ขยับจากที่ R187 วัดไว้บางส่วน
(field_mobs/mob_death ยืนยันแล้ว) ยังค้างงานวัด `WIRED v2` ให้ครบทั้งกระดาน 10-13 เลนตามที่ R187 ทิ้งไว้ —
ไม่ใช่งานของรอบนี้ (ไม่มี CORE-REQUEST ใหม่จากสาย A รอบนี้ — สาย A ยืนยันเองใน `A_20260827_0428` ว่า
CORE-REQUEST-003/004 ต่อสายแล้วจริง ไม่มีของค้างให้ chief ทำ)

### nonclaims

ไม่ได้อ้างว่าไคลเอนต์จริงเรนเดอร์ถูก — ยังเป็นชั้น wire/DB เหมือนเดิม (`GT-084`/`RIDER-084-A` `OW1`-`OW3`
ยังต้องรอ attended) · ไม่ได้แตะ `mob_combat.py`/`mob_death.py` (เขตสาย B) · ไม่ได้วัด `WIRED v2` ใหม่ทั้งกระดาน
· ไม่ได้ไล่ backlog ผู้เทส/CHIEF_CONTINUATION.md ทั้งหมด (ไม่มีเวลาในรอบนี้ หลังภาระ CORE-REQUEST-008)

### BUILD_IMPACT

ปิดความเสี่ยงล้างเมืองทุกครั้งที่ต่อสู้ (world-wipe) ก่อน M3 (28 ส.ค. 12:00) และ M4 (29 ส.ค. 23:59) — ถ้าไม่แก้
Panya จะเจอบั๊กนี้เองตอนเทส attended จริงตามที่ `CHIEF-URGENT 09:20` เตือนไว้ ตอนนี้เฟรม combat/death compose
เข้า full census แล้วทั้งสามจุด พร้อม fail-closed ที่ arrival census เองก็ยังไม่มีครบ (จุด `full_roster_override`
ใน `else:` clause ของ arrival ยังไม่มี guard — พบโดย pf-adversary ระหว่างรีวิว ไม่ใช่ของรอบนี้ ไม่แก้ในรอบนี้
เพราะนอกขอบเขต `CORE-REQUEST-008` — ฝากเป็นข้อสังเกตสำหรับ CORE-REQUEST ถัดไป)

### ที่ยังค้าง

- วัด `WIRED v2` ให้ครบทั้งกระดาน (10-13 เลน) — R187 ทิ้งไว้ ยังไม่มีใครทำ
- arrival census's own `full_roster_override` call (ใน `else:` ของ `try/except`) ไม่มี guard เหมือนกัน — pf-adversary
  เจอระหว่างรีวิวรอบนี้ ไม่ใช่ scope ของ `CORE-REQUEST-008` แต่ควรเปิด CORE-REQUEST ใหม่แก้
- backlog ผู้เทส/CHIEF_CONTINUATION.md ไม่ได้ไล่รอบนี้

-> `notes_to_chief/20260827_1130_CHIEF-REPLY-CORE-REQUEST-008-wired-plus-two-adversary-findings-fixed.md`
