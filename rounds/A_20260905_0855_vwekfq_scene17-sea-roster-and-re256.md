# LANE-A รอบ `vwekfq` — roster ฉาก 17 (ทะเล) + RE-256 ปลด layout ของ GT-233

- รหัสรอบ: `vwekfq` (กิ่ง `claude/eloquent-franklin-vwekfq` / `claude/charming-mendel-vwekfq`)
- เริ่ม: 2026-09-05T08:55+07:00 · ไฟล์รอบ: 2026-09-05T10:28+07:00
- claim: `pf_bridge#1288` (เปิด 08:55 · ไม่ draft · marker เติมตอนจบรอบ)
- server: `pirate-force-server#810` (เปิด 10:08 · ไม่ draft · marker ตั้งแต่เปิด · verified ด้วย GET สองครั้ง)

## 0. NOW ข้อไหนขยับ

อ่าน `NOW.md` เป็นไฟล์แรกของรอบ (08:55 · ตรวจล่าสุด 08:53 โดย COO)

- **ขยับ**: `0848` A: "roster ฉาก 17 (ทะเล) อนุมัติ = งานหลัก 09:21" — เป็นเป้าอนุมัติของบันได M3
  ("สนามมีมอนสเตอร์") ไม่ใช่หัวข้อ "รอเครื่องคุณ" ของ M2 เอง (M2 เองยังรอ `RE-256` ตอนต้นรอบ)
  รอบนี้ส่งงานตามเงื่อนไขสี่ข้อของ `0848` ครบ (ดูข้อ 2)
- **ขยับทางอ้อม**: `RE-256` (ตอนต้นรอบ M2 ยังรอผลนี้อยู่) มาถึงกลางรอบ (10:07) — บริโภคในรอบเดียวกัน
  ปลดเฉพาะ **layout/version gate** ของ `GT-233` ไม่ใช่ตัวบูตจริง (ยังต้อง attended)
- **ไม่ขยับ**: บันได M2 เอง ("ออกจากเมืองได้") ยังไม่ปิด — เกณฑ์คือจอ ไม่ใช่โค้ด

## 1. ต้นรอบ ตามลำดับที่กติกาบังคับ

1. อ่าน `NOW.md` เป็นไฟล์แรก ✅
2. **ล็อกรอบ**: list PR open ทั้งสองรีโปที่หัวขึ้นต้น `[LANE-A]` → ไม่มีเลย
   (`pf_bridge` เปิด `#1287` GM claim / `#1285` B claim · `pirate-force-server` เปิด `#806` chief/E · `#807` DB
   — สายอื่น ไม่แตะ) ⇒ ตัดกิ่งจาก main · commit `rounds/A_20260905_0855_vwekfq_claim.md` · push · เปิด `#1288`
   ไม่ draft · body ไม่มี marker · list ซ้ำทันทีหลังเปิด: ไม่มี `[LANE-A]` ใบที่เก่ากว่า ⇒ ล็อกเป็นของรอบนี้
3. **ชะตา PR รอบก่อน (ADDENDUM ข้อ A)** วัดจาก API: `pf_bridge#1276` (round `nmn123`) `merged=true`
   `merged_at 2026-09-05T01:25:46Z` · server ของรอบนั้น `pirate-force-server#805` `merged=true`
   (main HEAD ตอนโคลนคือ `884a9816` = merge ของ `#805` พอดี) ⇒ ไม่มีอะไรหายจาก main ไม่ต้อง cherry-pick
4. **กล่องจดหมาย (ADDENDUM ข้อ B)** ใบ `ADDRESSEE: LANE-A` ที่ยังไม่มี stub ตอนต้นรอบ: `0848` (งานหลัก)
   ระหว่างรอบมีใบใหม่เข้ามาสองใบ (main ขยับระหว่างทาง): `0905` (LANE-B แจ้งข้อมูล ไม่มีธุระให้ A ทำ)
   และ `1007` (ผล `RE-256`) — ทั้งสามบริโภคครบรอบนี้ (stub + สำเนา `consumed/`)

## 2. งานหลัก — roster ฉาก 17 (Bg1001) ตามเงื่อนไขสี่ข้อของ `COO-DECISION 0848`

มอบให้ pf-builder subagent ทำในสองสายงานคู่ขนาน (เขียนโค้ด+เทส) ควบคุมโดยรอบนี้ (ตรวจ diff/รันเทส/สั่ง push)

### 2a. ข้อมูลที่วัด

`CONSTDATA_TH__INSTANCE.tsv` แถว 109/122/124 (`n_SCENE_ID=17`) ชื่อ type 801 (min level **25**)
814 (70) 816 (70) — ทั้งสามชนเลข resolve 7/8 กับ `Bg1001.placements.tsv` (8 แถว: set 3 คือ instance
ที่สองของ set 2 ที่ป้ายผิด แก้ด้วยคอลัมน์เครื่อง `template_ids` ไม่ใช่ป้าย ตามบรรทัดฐาน
`world_bg0004_identity`) · leader ที่ resolve: 2880/2881/2883/2884 (set 6 ไม่มีแถว `CLINE` ในทั้งสามชนิด
ที่ชน ⇒ ปล่อยไม่ resolve แทนการเดา)

### 2b. เงื่อนไขสี่ข้อ — ทำอะไรตรงไหน

(ก) **[PROPOSED] ไม่ใช่ [MEASURED]**: `CLINE_BLOCKS` ใน `world_m2_sea_destination.py` ขยายด้วย
    type 801/814/816 (dense 5 key/5 แถวทั้งสาม) ติดป้าย `PROPOSED_CLINE_TYPES` + `is_cline_block_proposed()`
    ไม่มี control แบบ 56==56 ของฉาก 126 ⇒ ไม่มีที่ไหนเขียนคำว่า "measured" สำหรับฉากนี้
(ข) **ชั้นเลเวลต่ำสุด**: ใช้ type 801 (min level 25) ไม่ใช่ 814/816 (70) — ตรงข้ามข้อบกพร่อง D8
    ของร่างก่อนหน้า (max ข้ามชั้น) · มีเทสปักทิศทางนี้โดยเฉพาะ + `_self_check` รันไทม์
(ค) **actor/census เท่านั้น**: `world_bg1001_identity.py` (ใหม่, crosswalk) + `world_population_bg1001.py`
    (ใหม่, composer) รูปแบบเดียวกับ `world_bg3001_identity`/`world_population_bg3001` — ไม่มี hostile
    flag ไม่มี faction bit ไม่เปิดใบ GT ตีมอน (P-2 ยังไม่ปิด)
(ง) **เทสปักไบต์เกาะ 2/3**: `test_lane_a_scene17_roster_does_not_touch_gt233.py` — hash ไบต์ output ของ
    `encode_trial_records` (trigger_id 153/154), census เกาะ Atlantis, และไบต์ crossing-handoff ฉาก 17 เอง
    ก่อนรอบนี้ทั้งหมด แล้วยืนยันซ้ำหลังโมดูลใหม่ import — ไม่ได้ทำให้ไคลเอนต์ปิดตัว เพราะ **ไม่ได้ส่งอะไรใหม่
    ไปไคลเอนต์เลย** (ดูข้อ 2c ว่าทำไม)

`GT-159` ยืนยันไม่แตะ (`git diff` ต่อ `GAME_TEST_QUEUE.md`/`GT-159` ว่างเปล่า)

### 2c. สิ่งที่จงใจไม่ทำ — จุดตัดสินใจความปลอดภัยที่สำคัญที่สุดของรอบ

`runtime.py` (ไฟล์ chief) จุดข้าม Columbus crossing (`crossing_handoff_dispatched=True`, ~บรรทัด 6183-6197
บน main ที่ merge แล้ว) ส่งสิ่งที่ `crossing_handoff()` ประกอบให้โดยไม่มีเงื่อนไข บนสมมติฐานที่คอมเมนต์ตัวเอง
เขียนไว้ว่าฉากนี้ประกอบ `CLEAR` เปล่าเสมอ ถ้ารอบนี้ลงทะเบียน `ROSTER_COMPOSERS["bg1001_roster"]` จะพลิก
สมมติฐานนั้นให้ส่งลูกเรือ 7 คนที่ไม่เคยผ่าน attended test ไปหาไคลเอนต์จริงทันทีในการข้ามครั้งถัดไป — เป็นการ
ตัดสินใจเรื่องความปลอดภัยของ `runtime.py` ไม่ใช่คำถามโค้ด ⇒ **ไม่ลงทะเบียนเอง** `world_population_handoff.
PENDING_CROSSING_SAFETY_REVIEW` บันทึกเหตุผลเต็ม · crossing ยังคงไบต์เดิม (พิสูจน์ด้วยเทสข้อ (ง))

**CORE-REQUEST ถึง chief** (ฝากใน PR body ของ `#810` แล้ว): ทบทวนจุดเรียก Columbus crossing ว่าจะเปิด
`ROSTER_COMPOSERS["bg1001_roster"]` เมื่อไหร่/อย่างไร

### 2d. สิ่งที่ยังไม่ตัดสิน (ตั้งใจ)

- CLINE type 801 คือชนิดที่ถูกจริงหรือแค่ tie-break ที่สมเหตุสมผลที่สุด (ไม่มี control ตัดสิน)
- ไคลเอนต์จริงเรนเดอร์ 7 ตัวนี้ได้โดยไม่มีปัญหาไหม — ไม่มีใครยืนในฉาก 17 พร้อม actor มาก่อนในโปรเจกต์นี้
- ไม่มีใบ ChooseNPC click-responder สำหรับฉากนี้ (ตั้งใจ — ฉากนี้คือปลายทาง Columbus quest เอง
  ซึ่งเป็นโซนชนแบบเดียวกับที่ `lane_a_choose_npc_roster_scenes.py` เคยเตือนไว้ และ actor ยังไม่ถูกส่งจริง)

## 3. งานที่สอง (มาถึงกลางรอบ) — `RE-256` ปลด layout/version gate ของ `GT-233`

จดหมาย `20260905_1007_RE-256-RESULT...md` มาถึง 10:07 ระหว่างกำลังปิดรอบ (ตอบใบที่ M2 รอมาตั้งแต่ต้นรอบ
ในชื่อเดิม `RE-0430`) — บริโภคในรอบเดียวกันตาม COO `2142` ไม่ปิดด้วย "ใบเดิมเสนอไว้แล้ว"

ผลวัด (static, บนเครื่อง RE runner): ไบต์นำหลัง vital header ของ `NavigationEx_AddSurveyDataVtial` คือ
**boolean presence ของ pointer** (`0B 01` เมื่อมีหนึ่ง record ตามหลัง, `0B 00`/ไม่มีเมื่อไม่มี) **ไม่ใช่จำนวน
record** · `vital_version` คงที่ **0** แบบ exact equality · ห้ามใส่ record count เพิ่มเด็ดขาด

### สิ่งที่แก้

- `world_m2_provisioning_trial.encode_trial_records`: ดีฟอลต์ `outer_leading_byte` จาก `None` →
  `navigationex_survey_record.OUTER_PRESENCE_PRESENT` (=1) — จุดเรียกจริงจุดเดียวของ GT-233
  (`runtime.py` เรียกโดยไม่ override พารามิเตอร์นี้อยู่แล้ว ⇒ ถึง production โดยไม่ต้องแตะ `runtime.py`)
- `encode_add_survey_data_outer` (คอมโพสเซอร์ทั่วไป): คงดีฟอลต์ `None` ไว้ตั้งใจ (เป็น primitive ใช้ซ้ำได้
  หลายที่ `None` ยังเป็นทางเลือกจริงเช่นจำลองการจับภาพเดิมของ R313)
- doc comment ทั้งสองไฟล์ที่เคยเขียนว่าไบต์นี้ "ไม่มีค่าที่วัดสำหรับคลาสนี้" แก้ให้ชี้ `RE-256` ตรง ๆ
- `test_lane_a_scene17_roster_does_not_touch_gt233.py`: hash ที่ปักไว้ **re-derive จากโค้ดที่แก้แล้วจริง**
  (รันแล้วอ่านค่าออกมา ไม่ใช่เดา) เพราะ `RE-256` เปลี่ยนไบต์นำจริงตามที่ควรเป็น — เทสยังพิสูจน์เป้าหมายเดิม
  (ฉาก 17 ไม่ทำให้ไบต์นี้ขยับต่ออีก) แค่ baseline ใหม่ถูกต้องกว่าเดิม

### เสนอบรรทัดสถานะ `GT-233` (ไม่แก้หัวใบเอง ไม่ใช่ใบที่ตัวเองเปิด)

```
LAYOUT/VERSION GATE CLEARED BY RE-256 (outer presence=1, vital_version=0, no record-count byte)
— READY FOR ATTENDED RUN; msg-id control and on-screen window still unverified.
```

### ยังไม่ตัดสิน (attended เท่านั้น ตาม nonclaims ของ `RE-256` เอง)

เฟรมที่แก้แล้วเปิดหน้าต่างรายงานกัปตันจริงไหม · msg-id (`0xC4AF`) control แยกอิสระ · ผลต่อ M2 โดยรวม

## 4. จดหมายอื่นที่รับทราบ

`20260905_0905_LANE-B-TO-LANE-A...md` — B ขีดฆ่าประโยคผิดในไฟล์ของ A (`lane_a_choose_npc_scene14.py`)
ให้แล้วใน `#808` · B ไม่แตะ `lane_a_click_hp.py` (หนี้เดิม ไม่มีใครสั่งแก้ บันทึกไว้เป็นหนี้ของ A ไม่ใช่งาน
ของรอบนี้ ไม่บล็อกใคร) · รับกติกา shipped-vs-mined ของฉาก 14 ไว้ใช้ถ้าจำเป็นในอนาคต — ไม่มีธุระตรงกับ
ฉาก 17

## 5. เทส

- ระหว่างทำงาน: รันเฉพาะไฟล์ที่เกี่ยว (`test_world_bg1001_identity.py` `test_world_population_bg1001.py`
  `test_lane_a_scene17_roster_does_not_touch_gt233.py` `test_world_m2_sea_destination.py`
  `test_navigationex_survey_record.py` `test_world_m2_provisioning_trial.py` `test_m2_survey_trial.py`
  และไฟล์ co-maintenance ที่ tripwire บังคับ) — เขียวทุกครั้ง
- 🔴 **ชุดเต็มรันสองครั้งรอบนี้** (ปกติครั้งเดียว) — เหตุผล: รันครั้งแรกหลังงานหลัก (roster ฉาก 17) เสร็จ
  บน commit ที่ merge `origin/main` แล้ว (`987edc55`) ได้ **10781 passed / 323 skipped / 19909 subtests /
  0 failed** (512.37s) ก่อน push · ระหว่างนั้นจดหมาย `RE-256` มาถึงและถูกบริโภคเป็นงานที่สองในรอบเดียวกัน
  (เปลี่ยนไบต์จริงในโค้ด production) ⇒ ต้องรันชุดเต็มอีกครั้งบน commit สุดท้ายจริงก่อน push ตามกติกา
  "ต้องเป็น commit สุดท้ายจริง ๆ" ได้ **10782 passed / 323 skipped / 19909 subtests / 0 failed** (514.44s)
  — ค่าที่ใช้ตัดสินคือรอบที่สอง (main ไม่ขยับอีกระหว่างสองรอบนี้ ตรวจด้วย `git fetch origin main` ซ้ำ)
- pf-adversary: ไม่มี subagent แยกให้เรียกในรอบนี้ — ทำรีวิวมือแทน (join ตรวจซ้ำด้วยมือ, ทิศทางชั้นเลเวล
  ปักด้วยเทสเฉพาะ, ไบต์เกาะ 2/3 ปักด้วยเทสข้อ (ง), ป้าย `[PROPOSED]` ตรวจทุกจุดที่เขียน "measured",
  ยืนยัน `GT-159` ไม่ถูกแตะ) — บันทึกไว้ตรง ๆ ว่าไม่ใช่ automated adversary pass

## 6. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีอะไรเปลี่ยนบนจอ — ขึ้นเรือแล้วดาดฟ้ายังว่างเหมือนเดิม (จงใจ ตามข้อ 2c) และ `GT-233` ยังไม่มีใครบูตซ้ำ
(ต้อง attended) แต่สิ่งที่พร้อมจริงตอนนี้: ลูกเรือ 7 คนของฉาก 17 ถูกสร้าง/ทดสอบแล้วรอการตัดสินใจเรื่อง
`runtime.py` หนึ่งจุด และเฟรมของ `GT-233` ที่จะบูตครั้งต่อไปมี layout ที่ `RE-256` วัดแล้วแทนของเดิม

## 7. สถานะท้ายรอบ

push แล้ว รอ merge `pirate-force-server#810` (เปิดแล้ว ไม่ draft marker ตั้งแต่เปิด ยืนยันด้วย GET สองครั้ง
สถานะตอนนี้ = "open, waiting on the gate") · claim `pf_bridge#1288` push งานครบแล้ว เติม marker ตอนจบ
ไฟล์นี้ · ไม่รอ gate ไม่รอ merge ก่อนปิดรอบ ตามหัวข้อล็อกรอบ

QUEUE_TRIAGE: ไม่ได้กวาดคิว attended ทั้งชุดรอบนี้ (ไม่ใช่รอบของ chief) — เสนอบรรทัดสถานะ `GT-233`
ให้ผู้ดูแลคิวเติมตามข้อ 3 เท่านั้น
