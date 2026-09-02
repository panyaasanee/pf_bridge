# สาย B (COMBAT) รอบ `jysbar` — 2026-09-02T11:44+07:00

**NOW.md ข้อที่ขยับ: P-1** (ของดรอปต้องค้างอยู่บนพื้น) — ตามคำสั่ง `COO-DECISION 20260902_1044`
ข้อ 5 แล้วข้อ 3-4 · กำหนดของใบนั้นคือ "PR ก่อน 12:31 +07:00"

**สรุปหนึ่งบรรทัด:** carrier ตัวที่สอง (`make_runtime_remote_actors`) มี PRESERVE composer แล้ว
และเฟรม bar / dying / dead ของสายเอง เลิกล้างพื้นแล้ว — แต่บนเส้นทางหลัง arrival เฟรมสามใบนั้น
ถูก recompose เป็น census ทั้งฉาก 108 ตัว ซึ่งอยู่หลังรั้วที่ COO ตั้งไว้เอง จึง **ยังไม่แตะ**

---

## 1. ตอบข้อ 5 ของใบ 1044 ก่อนเขียนโค้ด: เฟรมสุดท้ายหลังของตกคือเฟรมไหน

วัดจาก dispatcher จริงของรีโป (`tests/test_mob_combat_dispatch.py` บูตไร้แฟล็ก ไม่มีซีนาริโอ)
ดัมป์ทุกเฟรมที่ออกจาก dispatch เดียวกัน พร้อม derived change mask ที่ประกอบจริง

### ตาราง ก — หมัดที่ฆ่า (ก่อนรอบนี้)

| ลำดับ | เฟรม | หน่วง | carrier | derived mask | พื้น |
|---|---|---|---|---|---|
| 1 | `MOB_COMBAT_ANNOUNCE` | 0.0 | vitals | `0B 08 12 00 00` | **รักษา** |
| 2 | `MOB_DEATH_DYING` | 0.0 | remote-actors | `0B 02` | ล้าง |
| 3 | `MOB_DEATH_DEAD` | **0.7** | remote-actors | `0B 02` | ล้าง |
| 4 | `MOB_LOOT_DROP` (ถ้ามีของ) | 0.0 `[PROPOSED]` | drop | บิต 0x08 ติด | ประกาศของ |

🔴 **แถวที่ 4 เป็น `[PROPOSED]` ไม่ใช่ `[MEASURED]`** (pf-adversary อันดับ 2): แถวควบคุมที่ฮาร์เนสนี้
ฆ่าไม่ดรอปของ — adversary ขับ 40 kill ได้ `{0: 40}` ⇒ หน่วง 0.0 ของเฟรมของตกอ่านจาก **call site
ที่เข้าคิว** (`mob_drop_presence.ACTION_LABEL` · `actions.append(("MOB_LOOT_DROP", loot_pc,
loot_frame, 0.0))`) ไม่ใช่จากการวัดในฮาร์เนส · สิ่งที่ **วัดแล้ว** คือสามแถวบน ⇒ **เฟรมสุดท้ายของ
หมัดที่ฆ่าคือ `MOB_DEATH_DEAD` ที่ 0.7 วินาที** และภายใต้ลำดับ `[PROPOSED]` ข้างบน มันมาหลัง
เฟรมของตกและล้างมันทิ้ง

### หลังจากนั้นมีอะไรอีก — คำตอบที่ใบ 1030 อยากได้

- heartbeat ~2 วิ: `preserve_ground_heartbeat_frame` — **บิต 0x08 ติดอยู่แล้ว** ตั้งแต่ `app.py`
  install ลง main (วัดรอบนี้: pc 17 ไบต์ `... 0B 00 0B 08 12 00 00`) ⇒ ไม่ล้าง
- census: `world_population.INITIAL_REAPPLY_MS = 3000` เป็น **การส่งซ้ำครั้งเดียวผูกกับ arrival**
  ไม่ใช่ cadence ที่ยิงตลอดเวลา

🔴 **คำตอบตรง ๆ ต่อข้อ 5: ไม่ใช่ census ที่ยิงตลอดเวลา** เฟรมที่ปิดท้ายลำดับคือ dead frame ของ
หมัดนั้นเอง แล้วจึงเป็น heartbeat ที่รักษาพื้นอยู่แล้ว ⇒ **การไล่ปิดทีละจุดแบบ `0646` ไปถึงปลายได้จริง**
ไม่ต้องกลับไปเปิดเรื่องรูปของ carrier เป็นใบแยกอย่างที่ใบ 1044 เผื่อไว้ · เฟรมที่เหลือที่ยังล้างพื้น
มีเท่าที่ COO ระบุไว้เป๊ะ: bar · dying · dead · กับ census ขาเข้า

### ตาราง ข — หลังรอบนี้ (เส้นทางที่สายเป็นเจ้าของ composer เอง)

| เฟรม | derived mask ก่อน | หลัง |
|---|---|---|
| `MOB_COMBAT_ANNOUNCE` | 0x08 (vitals tail) | เท่าเดิม |
| `MOB_COMBAT_BAR` | `0B 02` | **`0B 0A`** + `12 00 00` |
| `MOB_DEATH_DYING` | `0B 02` | **`0B 0A`** + `12 00 00` |
| `MOB_DEATH_DEAD` | `0B 02` | **`0B 0A`** + `12 00 00` |

---

## 2. ของที่สร้าง

**`mob_loot.preserve_ground_in_runtime_res_remote_actors(legacy, entries)`** — คู่แฝดของ
`preserve_ground_in_runtime_res_vitals` สำหรับ carrier ตัวที่สอง

รูปไม่เหมือนพี่มันและนั่นคือความยากทั้งหมด: ใน `make_runtime_vitals` derived mask เป็น**เรคคอร์ด
สุดท้าย** จึงต่อท้ายได้ · แต่ใน `make_runtime_remote_actors` mask อยู่ **ก่อน** คอลเลกชัน actor
(ออฟเซ็ต 12) ⇒ การรักษาพื้นต้องแก้ไบต์เดียวกลางลำ (`0x02` → `0x02|0x08`) แล้วต่อเรคคอร์ด
ground list (ว่าง) ท้ายสุด

การเทียบไบต์ตามใบ 1044 ข้อ 3 จึงเขียนตามรูปจริง ไม่ใช่ตามคำ:
- ขับ `legacy.make_runtime_remote_actors` จริง แล้วเทียบกับ re-derivation ของสายเอง ทั้งก้อน
- ผลลัพธ์ต้องเท่ากับของ v141 **ทุกไบต์** ทั้งฝั่งซ้ายและฝั่งขวาของ mask (`pc[:12] == composed[:12]`,
  `pc[14:len(composed)] == composed[14:]`) ไบต์ใหม่มีได้เฉพาะที่ท้าย
- เรคคอร์ด `12 00 00` ปักซ้ำกับ **ไบต์ที่ heartbeat ส่งจริงในโปรดักชัน** (`preserve_ground_heartbeat_pc`)
  ⇒ สองที่นี้เคลื่อนพร้อมกันเท่านั้น
- frame เทียบกับ `_frame_via_struct` ทั้งเส้น ไม่ใช่ magic+suffix (บทเรียน ewm6ff D5 — สำคัญกว่าที่นี่
  เพราะ census 108 ตัวคือ 20 KB ใกล้เพดาน 65534 ที่ตัวเช็คแบบ suffix เคยตัดสินผิด)
- ปฏิเสธชื่อใหม่ `actors_composer_moved` · entry ว่าง/ไม่ใช่ bytes ปฏิเสธโดยชื่อ (นับในช่อง count
  ⇒ stream tail ที่ไคลเอนต์ align ไม่ได้ = ErrorData=28317)

**`mob_combat.remote_actors_preserving_the_ground(legacy, entries, site)`** — fall back ตามใบ 0646
ข้อ 4 รูปเดียวกับตัว vitals: **ประกอบ fall back ก่อน พิมพ์ทีหลัง** ⇒ ถ้า carrier ล่มจริงจะ raise
ของตัวเองและ **ไม่พิมพ์โทเคนโกหก** · โทเคน `GROUND_ACTORS_PRESERVE_REFUSED` ASCII บรรทัดเดียว
มีเพดาน · คอนโซลเขียนไม่ได้ = เสีย "บรรทัด" ไม่เสีย "เฟรม"

**จุดที่เสียบ (เรียง bar → dying → dead ตามใบ 1044 ข้อ 4):** `mob_combat.bar_frames` และ
`mob_death.death_frames` (ตัวเดียวประกอบทั้ง dying และ dead — ต่างกันที่ timer ไม่ใช่ที่ carrier)

## 3. สิ่งที่ **ไม่** ทำ และเพราะอะไร (ตัดสินเองแล้วเดินต่อ ไม่ได้หยุดรอ)

🔴 วัดรอบนี้แล้วได้ข้อเท็จจริงที่ใบ 1044 ยังไม่มีตอนเขียน: **หลัง arrival จริง เฟรม bar/dying/dead
ไม่ใช่คอลเลกชันหนึ่งตัวของสายอีกต่อไป** — `runtime.py` recompose มันเป็น generation ทั้งฉาก
108 actor (~20 KB) ผ่าน `mob_scene_recompose.recompose_frames`
(คอนโซล: `MOB_COMBAT_BAR_CENSUS_RECOMPOSE actor_count=108`,
`MOB_DEATH_FRAMES_CENSUS_RECOMPOSE_DYING actor_count=108`)

รั้วของ COO ข้อ 4 เขียนด้วย**เหตุผล**ว่า "พังที่ census = NPC หายทั้งแมพ ใหญ่กว่า P-1"
เฟรมที่ recompose แล้วสามใบนั้นอยู่ฝั่งแมพของรั้วตามเหตุผลนั้นเป๊ะ ⇒ **รอบนี้ไม่แตะ**
และปักไว้ด้วยเทสว่ามันยังล้างพื้นอยู่ (`test_the_post_arrival_recompose_is_still_outside_this_opt_in`)
วันที่ใครขยาย opt-in เทสใบนั้นแดง แล้วต้องพูดออกมาว่าทำไม

⇒ **ผู้เล่นที่เข้าฉากตามปกติยังไม่เห็นอะไรต่างจากเมื่อวาน** และรอบนี้พูดแค่นั้น: ประตูที่เปิดคือ
composer ของ carrier มีแล้ว ผ่านเทสในฮาร์เนส dispatcher จริง เหลือ**คำอนุญาตเดียว**คือให้ข้ามรั้ว
ไปที่ census · จดหมายถึง COO เสนอทางปลดล็อกที่ถูกที่สุด: GT หนึ่งขั้นที่ดูว่าไคลเอนต์รับเฟรม
mask `0x0A` ได้ไหม (บูตไร้แฟล็ก ตีมอนหนึ่งครั้งก่อน arrival census ก็เห็นแล้ว)

## 4. สมมติที่ติดป้ายไว้ ยังไม่ได้วัด

`[สมมติของสาย B - รอ COO ยืนยัน]` เมื่อบิตติดทั้งสองตัว ไคลเอนต์อ่าน actor collection ก่อน
แล้วค่อย ground list (serializer เขียน +0x1C ก่อน +0x20) · **ที่วัดแล้วคือแต่ละฟิลด์เดี่ยว ๆ**:
actor collection เดี่ยวในทุก census ที่เซิร์ฟเวอร์นี้เคยส่ง และ ground list เดี่ยวใน heartbeat
โปรดักชัน · **สองอันพร้อมกันยังไม่เคยอยู่บนไวร์** ⇒ นี่คือเหตุผลที่ fall back มี และที่รั้ว census ยังอยู่

## 5. หลักฐาน

- `pytest tests -q` — ผลเต็มอยู่ใน body ของ PR (server)
- เทสใหม่: `TheOtherCarrierKeepsTheGroundToo` 10 ใบ (รวมเคส 108 entry, 0 entry, composer ที่ย้าย,
  mask ที่ย้าย, framer ที่เพี้ยน, entry ว่าง)
- เทส dispatcher จริง: `test_the_kill_burst_frame_by_frame_and_the_frame_that_ends_it`
  (ตาราง ก/ข ข้างบนเป็นเทส ไม่ใช่คำอ้างใน PR) และ
  `test_the_post_arrival_recompose_is_still_outside_this_opt_in`
- เทสเก่าที่ต้องแก้เพราะไบต์เปลี่ยนจริง (แก้ด้วยการวัด ไม่ใช่ด้วยการเขียนคำอ้าง):
  `test_mob_combat.py::test_the_bar_frame_is_a_one_entry_generation_open_risk_not_a_fix`
  (ขีดฆ่าบรรทัดเทียบเดิม เขียนเหตุผลข้าง ๆ · สิ่งที่ใบนั้นมีไว้ปัก — หนึ่ง entry ไม่ใช่ศูนย์ ไม่ใช่ทั้ง
  roster — ยังปักอยู่ครบ) และ `test_mob_combat_dispatch.py` ตาราง 9jrsei
- pf-adversary รอบ `jysbar` ก่อน commit

## 6. บริโภคกล่องจดหมาย

- `20260902_1044_COO-DECISION-p1-lane-b-order-*` (ถึงสาย B) — บริโภคแล้ว ทำตามข้อ 5 → 3 → 4
  วางสำเนาใน `consumed/` + stub

## 7. ต่อไป

1. removal publisher ตาม `COO 0253` (ลำดับข้อ 2 ของใบ 1044)
2. `bag_delta_pc` (ข้อ 3) — ยังปิดอยู่ตามใบ 0943 ข้อ 2
3. ถ้า COO ปลดรั้ว census (หรือ GT เห็นเฟรม `0x0A` ผ่าน): เสียบ composer เดียวกันที่
   `mob_scene_recompose` แล้ว P-1 จะเห็นผลบนจอครั้งแรก

---

## 8. pf-adversary รอบ `jysbar` — สิ่งที่ถูกหักล้างก่อน commit

รีวิวยิงมา 9 อันดับ **สองข้อเป็น disqualifying** แก้ทั้งหมดก่อน commit:

1. 🔴 **(อันดับ 1, disqualifying)** `MOB_COMBAT_NONCLAIMS` ยังมีประโยค
   "A PRESERVE composer for that carrier does not exist yet" **และมันถูก serialize ลง
   `scenarios/combat_first_hit_001.json` ที่รอบนี้ regenerate เอง** ⇒ ไฟล์เดียวกันมีทั้งเลข
   `bar_frame_bytes: 170` (พิสูจน์ว่า composer ต่อแล้ว) กับประโยคว่ายังไม่มี composer
   เทสพินเขียวเพราะมันถามแค่ว่า JSON ตรงกับโค้ดไหม ⇒ **รับรองประโยคเท็จแทนที่จะจับได้**
   แก้: ขีดฆ่าพร้อมเหตุผล + เพิ่ม nonclaim ใหม่เรื่องบิตสองตัว ทั้ง `MOB_COMBAT_NONCLAIMS`
   และ `MOB_DEATH_NONCLAIMS` (ของ death เดิม **ไม่มี** ข้อไหนพูดถึงพื้นเลย) + regenerate พินใหม่
2. 🔴 **(อันดับ 2, disqualifying)** เทสที่เขียนว่า "Measured" ว่า burst มีสี่เฟรมรวมเฟรมของตก
   **ไม่เคยเห็นเฟรมของตกเลย** — adversary ขับ 40 kill ในฮาร์เนสเดียวกัน ได้ `{0: 40}` (ไม่มี drop)
   ⇒ ประโยค "dead frame มาหลัง drop frame 0.7 วิ" เป็น `[PROPOSED]` อ่านจาก delay ที่ call site
   เข้าคิว ไม่ใช่ `[MEASURED]` · แก้ docstring ให้ตรงกับสิ่งที่วัดจริง (สามเฟรม) และติดป้ายให้ถูก
3. **(อันดับ 3)** wrapper `remote_actors_preserving_the_ground` **ไม่มีเทสเลยแม้แต่ใบเดียว**
   mutant รอด 10/20 รวมสองข้อที่พี่มัน (vitals) เคยเสียเลือดมาแล้ว: กลืน exception ของ fall back
   และพิมพ์ก่อนประกอบ fall back ⇒ เพิ่มเทส 7 ใบ (fall back คืนไบต์ v141 + โทเคน · composer ตาย
   ต้องไม่พิมพ์บรรทัดโกหก · console cp874 พัง = เสียบรรทัดไม่เสียเฟรม · generator ต้องไม่ถูกดูดจน
   fall back เหลือศูนย์ entry (= world wipe ตาม RE-092) · ชื่อ site ต้องเดินทางและต้องเป็นชื่อที่มีจริง)
4. **(อันดับ 3 ต่อ)** `GROUND_ACTORS_PRESERVE_SITE_DEATH` เขียนว่า `mob_death.death_frame`
   ซึ่ง **ไม่มีฟังก์ชันชื่อนั้น** ⇒ แก้เป็น `death_frames` + ปักด้วยเทสว่าชื่อ resolve ได้จริง
5. **(อันดับ 4)** คอมเมนต์ใน `mob_death.py` เขียนว่า "นี่คือเฟรมที่เอาของออกจากพื้นเป็นใบสุดท้าย"
   ⇒ **จริงเฉพาะเส้นทางก่อน arrival** ขีดฆ่าพร้อมเหตุผล
6. **(อันดับ 5)** tripwire ของรั้วครอบไม่ครบ: ครอบแค่ bar และแค่ scene 1 ⇒ เพิ่มเคส kill
   (dying/dead หลัง arrival) และเขียนช่องโหว่ scene 2 ไว้ในตัวเทสเอง ·
   `mob_diag_multi_object.dead_only_schedule` ถูก opt-in ไปด้วยโดยไม่ได้ตั้งใจ (เป็น control ของ
   RE-107) ⇒ เขียนบอกไว้ที่บล็อก opt-in
7. **(อันดับ 6)** cross-pin กับ heartbeat **ไม่ใช่หลักฐานอิสระ**: `12 00 00` เป็นการเข้ารหัสทั่วไป
   ของ "u16 = 0" เหมือนกับช่อง count ศูนย์เป๊ะ ⇒ แยกกันด้วย**ตำแหน่ง**เท่านั้น = สมมติเดิมพูดซ้ำ
   ⇒ แก้ถ้อยคำในคอมเมนต์ให้พูดตามนั้น
8. **(อันดับ 7)** เทสใหม่หนึ่งใบทำให้การเทียบไบต์สี่ข้อ "มีชีวิต": shim ที่ **รับ** mask 0x0A แล้วเขียน
   0x02 ผ่านการเทียบก้อนใหญ่แต่ต้องโดนจับที่สี่ข้อนี้
9. **(อันดับ 9)** คอมเมนต์อ้าง "ดูไฟล์รอบ" แต่รีโปเซิร์ฟเวอร์ **ไม่มี** `rounds/` ⇒ แก้ให้ระบุ path
   ฝั่ง pf_bridge ตรง ๆ

🔴 **คำถามที่ adversary ทิ้งไว้และรอบนี้ตอบไม่ได้ (ยกไปให้ COO ในจดหมาย):** ถ้าไคลเอนต์อ่าน
สองบิตสลับกัน มันจะได้เฟรมที่ **well-formed แต่ความหมายกลับหัว** ไม่มี ErrorData ไม่มี refusal
ไม่มีบรรทัดคอนโซล และเทสทุกใบในรีโปยังเขียว เพราะทุกใบเทียบไบต์กับไบต์ ⇒ fall back กัน
"composer ล่ม" ได้ แต่กัน "composer ถูกเข้าใจกลับหัว" ไม่ได้ ⇒ **ต้องมี GT หนึ่งขั้นก่อนขยายไปที่ census**
