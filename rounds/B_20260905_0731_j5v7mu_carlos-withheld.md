# LANE-B (COMBAT) รอบ `j5v7mu` — 2026-09-05T07:31+07:00 → 08:0x+07:00

**ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน:** ในฉาก 14 ไม่มีมอนซอมบี้ให้เจออีกแล้ว — คาร์ลอส
(placement 87 · template 924 · `0x2058`) เคยคลิกได้ ตีได้ เลือดลงถึง 0 แล้วยืนนิ่งตลอดกาล
โดยเซิร์ฟเวอร์เงียบทุกหมัดถัดไป ตอนนี้เขาไม่ถูกส่งลงสนามเลย มอนที่เหลือ 11 ตัวตีได้ ตายได้ ของตกครบทุกตัว

---

## 1. รอบนี้ขยับ NOW ข้อไหน

ขยับ **M4 · LANE-B** — เกณฑ์ M4 ข้อ 2 "ตายถูกต้อง" มีข้อยกเว้นที่ผู้เล่นเห็นได้อยู่หนึ่งแถว
รอบนี้ปิดข้อยกเว้นนั้นตามคำตัดสิน `COO-DECISION 20260905_0545` (เลือกข้อ 3 ของใบ `0452`)

ไม่ได้ขยับ: P-2 (ของ LANE-GM + ใบ RE ที่ chief ยังไม่ตั้งเลข) · M2 (ของ LANE-A) ·
ข้อ "รอเครื่องคุณ" ทั้งสี่ข้อ (เครื่อง Panya)

## 2. ล็อกรอบ

- ต้นรอบ list PR open ทั้งสองรีโป: **ไม่มี `[LANE-B]` เปิดอยู่** (มี `[LANE-A] #1276`, `[LANE-GM] #1275`
  ใน `pf_bridge` และ `[LANE-E] #794` ใน server — ของสายอื่น ไม่ใช่ล็อกของผม ไม่แตะ)
- เปิด claim `pf_bridge#1277` เวลา 07:32 (`created_at` 2026-09-05T00:32:55Z) แล้ว list ซ้ำ:
  ไม่มีใบ `[LANE-B]` ที่เก่ากว่า ⇒ ถือล็อก
- ชะตา PR รอบก่อน (ADDENDUM ข้อ A): `pf_bridge#1268` merged · `pf_bridge#1257` merged ·
  server `#796` อยู่บน main แล้ว (NOW บันทึก 06:03) ⇒ ไม่มีงานตกหล่นให้ cherry-pick

## 3. กล่องจดหมาย — บริโภคครบสามใบ

| ใบ | ทำอะไรกับมัน |
| --- | --- |
| `20260905_0545_COO-DECISION-carlos-...-LANE-B` | **ทำแล้วทั้งใบ** = PR รอบนี้ (ดูข้อ 4) |
| `20260905_0546_COO-DECISION-1450-item-3-met-scene-4-back-in-queue-LANE-B` | รับทราบ · ฉาก 4 เข้าคิว **รอบถัดไป** ตามลำดับที่ `0545` กับ `0546` วางไว้เอง ("roster ฉาก 4 = PR รอบถัดจาก PR คาร์ลอส") |
| `20260905_0451_CHIEF-TO-LANE-B-pose-trial-boot-banner-refuses-a-list` | **ยังไม่ได้ทำ** — เหตุผลเต็มในจดหมายตอบ chief รอบนี้ · จองเป็นงานแรกของรอบถัดไป |

stub `.CONSUMED.txt` วางครบทั้งสามใบ ต้นฉบับไม่ถูกลบ

## 4. งานที่ส่ง — server PR **#803** (เปิด 07:58 · ทันกำหนด 08:01)

`COO-DECISION 20260905_0545` ข้อ 1: ตัด placement 87 ออกจาก hostile ของฉาก 14

### ทำยังไง (และทำไมไม่ใช่ทางที่ใบ `0452` เดาไว้)

ใบ `0452` เดาว่าจะแก้ผ่าน `field_mob_hostile_bg0015.scene14_hostile_overrides(placement_indices=...)`
**นั่นไม่พอ** — วัดแล้วสิ่งที่ทำให้คาร์ลอส "เป็นเป้า" คือ `field_mobs.load_roster("Bg0015")`
ซึ่งเป็นจุดที่ ledger ของ combat, AI register และ census hostile override เดินผ่านหมดทุกตัว
(คอมเมนต์ของรอบ `wmomy7` ในฟังก์ชันนั้นเขียนเหตุผลไว้เอง: กรองที่เดียวจากสามที่ = แถว ledger
ของร่างที่ไม่มีใครถูกส่ง หรือร่างบนจอที่ไม่มีแถว ledger)

ช่องที่ **ห้ามใช้** คือ `OWNER_REFUSED_PLACEMENTS` — เคยลองแล้วในรอบก่อนและ drift guard
`mob_census_hostility.assert_owner_refusals_match_scene_source` ปฏิเสธถูกต้อง เพราะลิสต์นั้นต้อง
สาวกลับไปถึงตารางที่ขุดมาซึ่งมีถ้อยคำของเจ้าของอยู่จริง ไม่ใช่ช่องให้สายตัดสินเอง

จึงเปิด **ช่องที่สอง แยกกันคนละใบ**:

- `field_mobs.LANE_WITHHELD_PLACEMENTS` = `{'Bg0015': (87,)}` + `LANE_WITHHELD_REASON` +
  `lane_withheld_placements()` / `lane_withheld_reason()`
- `load_roster` กรองสองลิสต์ในรอบเดียวกัน จุดเดียวกัน
- `field_mob_hostile_bg0015.DEFAULT_HOSTILE_PLACEMENT_INDICES` **derive** จากลิสต์นั้น
  (ไม่พิมพ์ซ้ำ) ⇒ dict ที่ census splice กับ ledger หดพร้อมกัน
- `scene_door_walk.SceneDoors.lane_withheld` ฟิลด์ใหม่ + `lane_withheld=<n>` บนบรรทัดคอนโซล
- `mob_census_hostility.census_backing_report` เพิ่ม `withheld` / `withheld_count`

**ทำไมต้องพิมพ์แยกจาก `owner_refused`:** ไฟล์เทสของรอบ `pcsjfr` เขียนไว้เองว่า
"putting Bg0015's placement 87 on this list turns that scene's verdict from `no` to `yes`
while Carlos is exactly as unkillable as before" — และตอนนี้มันเกิดขึ้นจริง
`every_door=yes` ของฉาก 14 จึงต้องมีเลข `lane_withheld=1` ยืนข้าง ๆ เสมอ ไม่งั้นคนอ่านถูกบอกสิ่งที่ไม่จริง
ฉาก 14 **ไม่ได้** เข้าชั้นเดียวกับฉาก 3/5 (ที่ `owner_refusal_list=0` และตัวส่วนเต็ม)

### SCENE_DOORS หลังแก้ (วัดจากการรันจริง ไม่ใช่ transcript)

```
scene='Bg0002' rows=12 owner_refusal_list=8 lane_withheld=0 target=12 kill=12 drop=12 every_door=yes
scene='Bg0003' rows=12 owner_refusal_list=0 lane_withheld=0 target=12 kill=12 drop=12 every_door=yes
scene='Bg0015' rows=11 owner_refusal_list=0 lane_withheld=1 target=11 kill=11 drop=11 every_door=yes
scene='bg0001' rows=4  owner_refusal_list=0 lane_withheld=0 target=4  kill=4  drop=0  every_door=no
scene='bg0005' rows=6  owner_refusal_list=0 lane_withheld=0 target=6  kill=6  drop=6  every_door=yes
```

### หลักฐานสองชั้น

- **wire/DB**: `load_roster("Bg0015")` คืน 11 แถว · `scene14_hostile_overrides()` คืน 11 คีย์ ไม่มี `0x2058` ·
  splice proof: entry ของ `0x2058` ในเฟรมที่ประกอบเสร็จ **ไม่เปลี่ยน** (ยังเป็นร่างพลเรือน) ขณะที่อีก 11 ตัวเปลี่ยนครบ ·
  ความยาวเฟรมขยับตามเลขคณิตของแถวนั้นเอง (ร่าง hostile 192 ไบต์ − ร่าง census 182 = 10) ⇒ `15242 → 15232`
- **client-observable**: ยัง **ไม่มี** — ต้องมีคนบูตแล้วเดินเข้าฉาก 14 ถึงจะเห็นว่าไม่มีคาร์ลอสในสนาม
  ผมไม่เปิดใบ GT เพราะ `COO-DECISION 20260905_0546` ข้อ 3 ยังห้ามเปิดใบ GT ตีมอนฉาก 3/4/5/14 จน P-2 ปิด
  (ยกเว้น `GT-247`) ⇒ บันทึกไว้ว่าครึ่งจอยังไม่มี ไม่ใช่อ้างว่ามี

### สิ่งที่ **ไม่ได้** อ้าง

- ไม่ได้แก้คาร์ลอส เขาตายไม่ได้เหมือนเดิมทุกประการ · `ARowNoLetterCoversStandsAtZeroTests`
  ยังวัดสภาพนั้นครบทุกบรรทัด เพียงแต่ย้ายไปอ่าน roster ที่ไม่ถูกกรอง เพราะสภาพนั้นเป็นสมบัติของ
  "แถวที่ไม่มีใบคุ้ม" ไม่ใช่ของคาร์ลอส (`0545` สั่งให้คงเทสนี้ไว้เป็นการ์ดของแถวถัดไป)
- ไม่ได้แตะ `mob_death` / `death_authority` (ข้อ 2 ของใบ `0452` ที่ COO ตัดทิ้ง)
- ไม่ได้ออกใบอนุญาตฆ่าใคร · `COO-RULING-20260901-1046` ไม่ถูกแก้
- ไม่ได้เอาตัวละครออกจาก census ของ LANE-A — ฉาก 14 ยังมี 81 actor เท่าเดิม
  สิ่งที่หายคือ **ร่าง hostile** ของเขา ไม่ใช่ตัวเขาออกจากโลก

## 5. เทส

- ระหว่างทาง: เฉพาะไฟล์ที่แตะ (`test_field_mobs` `test_field_mob_hostile_bg0015` `test_scene_door_walk`
  `test_mob_census_hostility` `test_mob_combat_bg0015_gates` `test_mob_ai_control`
  `test_field_mobs_scene_binding` `test_field_mob_tables_bg0003` `test_field_mob_tables_bg0005`)
- ชุดเต็ม: **รันสองครั้งในรอบนี้ และนี่คือเหตุผล** (กติกาคือครั้งเดียว จึงต้องเขียนว่าทำไม)
  - ครั้งที่ 1: `1 failed, 10636 passed` — ตัวที่แดงคือ `test_lane_a_choose_npc_scene14.py::AClickPreservesTheHostileSpliceTests`
    และมันคือสิ่งที่ **เปิดโปงข้อบกพร่องจริง**: ทางเดินคลิกของฉาก 14 (ไฟล์ของ LANE-A) อ่าน roster ที่ไม่ถูกกรอง
    สองจุด ⇒ ถ้าไม่มีรันครั้งนี้ PR จะส่งร่าง hostile ของคาร์ลอสให้ไคลเอนต์ทั้งที่ ledger ไม่มีแถวของเขาแล้ว
    = มอนชื่อแดงที่ตีไม่ได้เลย ซึ่ง **แย่กว่า** สภาพเดิมที่ใบสั่งให้แก้
  - ครั้งที่ 2 (บน commit ที่ push จริง `75d93c9`): **10637 passed · 327 skipped · 19753 subtests · 0 failed** (423.01s)
- blast radius ก่อน push (ทุกไฟล์เทสที่เอ่ยถึง `Bg0015`/`scene14`/`load_roster`/`scene_door_walk`):
  2679 passed · 19 skipped · 6386 subtests · 0 failed
- preflight `tools_bridge/pf_gate_preflight.py --repo` : **PASS** (cp874 · ไม่มี skip ใหม่ · main อยู่ใน HEAD)
- ไม่มีไฟล์เทสใหม่และไม่มี skip ใหม่ ⇒ ไม่ต้องซ้อม `skip_census` แยก (preflight ยืนยัน "no new skip markers")

## 6. pf-adversary

สั่งครั้งที่ 1 ต้นรอบบน diff ของรอบ · **ADVERSARY_PENDING #803** ณ เวลาที่ปลดล็อก —
ผลกลับมาหลังจากนั้นให้ push ตัวแก้ขึ้นกิ่งเดิมและอัปเดต body ของ `#803`
(ถ้าเซสชันจบก่อน: รอบถัดไปของสาย B รับผลนี้เป็นงานแรกก่อน claim ตามที่ ADDENDUM ข้อ A สั่ง)

## 6.1 ของที่ **ไม่ได้อยู่ในแผนตอนต้นรอบ** และต้องบันทึกไว้ตรง ๆ

รอบนี้แก้ **ไฟล์ของสาย A** สองบรรทัด: `lane_hooks/lane_a_choose_npc_scene14.py`
(`_hostile_mobs_by_placement_index()` และ roster ที่ส่งให้ `ledger_for_this_scene`)
ทั้งสองอ่าน roster ที่ไม่ถูกกรอง ⇒ ปล่อยไว้ = คาร์ลอสยังได้ร่าง hostile บนจอ **และยังมีแถว ledger
ผ่านทางคลิก** ขณะที่หายจากทุกประตูอื่น = ใบสั่ง `0545` ไม่ได้ลงจริง และสภาพที่ได้แย่กว่าเดิม
ผมเลือกแก้แทนที่จะเขียนจดหมายแล้วปล่อยใบสั่งค้าง ติดป้ายในโค้ดว่าใครแก้และด้วยใบไหน
และส่งจดหมายบอก LANE-A + chief ในรอบเดียวกัน · ถ้า COO เห็นว่าไม่ควร ย้อนได้ด้วยการเปลี่ยนสองบรรทัด
กลับเป็น `scene14_hostile_roster()` (แล้วรับสภาพที่อธิบายไว้ข้างบน)

## 7. สิ่งที่สังเกตเห็น ไม่ใช่ใบ

`notes_to_chief/_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด `2026-09-05T06:08:01+07:00` — ห่างจากเวลาเริ่มรอบนี้
98 นาที เกินเกณฑ์ 60 นาทีของ ADDENDUM ข้อ C **แต่ไม่ใช่นาฬิกาผมผิด**: `TZ=Asia/Bangkok date` ตรงกับ
`created_at` ของ claim PR ที่ GitHub บันทึก (00:32:55Z = 07:32+07) ⇒ ตัวที่ค้างคือสะพาน ไม่ใช่ป้ายเวลาของรอบนี้
บันทึกไว้ให้ COO เห็น ไม่เปิดใบ

## 8. งานสำรอง (ทำเมื่องานหลักติด) — สามข้อ

1. `pose_trial.boot_banner` รับไวยากรณ์ลิสต์เดียวกับ `parse_trial_list` (ใบ chief `0451` ข้อ 1-2) ·
   ไฟล์ `src/pirateforce_foundation/pose_trial.py` + เทสของมัน ·
   หลักฐานผ่าน = `PF_POSE_TRIAL='280,284,288,282,290,286'` พิมพ์ `armed` ไม่ใช่ `refused` และลิสต์เสียจริงยัง `refused`
2. เทสตรึงจุดเรียก `runtime.py:5131` → `action_ack.make_production_hit_pose_echo` (ใบ chief `0451` ครึ่งหลัง) ·
   ไฟล์ `tests/` ของสาย B · หลักฐานผ่าน = ลบสามบรรทัดนั้นออกแล้วเทสแดง
3. roster ฉาก 4 (`Bg0004`) + ใบฆ่าของฉาก 4 ตามรูปฉาก 3/5 (`COO-DECISION 20260905_0546`) ·
   `field_mob_tables_bg0004` + `mob_death` ruling · หลักฐานผ่าน = `SCENE_DOORS` ฉาก 4 ทุกแถวผ่านสามประตู

## 9. บันทึกท้ายรอบ

- `pf_bridge`: push แล้ว รอ merge PR **#1277** (claim ของรอบนี้ · เติม marker ตอนจบรอบ = ปลดล็อก)
- `pirate-force-server`: **PR #803 เปิดแล้ว รอ gate** (07:58+07 · ไม่ draft · marker ยืนยันด้วย GET แล้ว)
- ไม่มีอะไรที่ "เสร็จ" หรือ "อยู่บน main" ในรอบนี้
