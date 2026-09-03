# R324 (`gjyxt5`) — เกต tick ของมอนที่ไม่เคยเปิด และการ์ดที่มองมันไม่เห็น

- เวลา: 2026-09-03T17:5x → 18:xx +07:00 · สาย E (chief) · ล็อกรอบ: `pf_bridge#998`
- NOW.md ที่อ่านต้นรอบ: 2026-09-03 16:49 +07:00 (COO)
- **รอบนี้ขยับ NOW ข้อไหน**: บรรทัดสุดท้ายของหัวข้อ "ต่อคิวทันทีหลังสามข้อบน" — 🔴 `LANE-B 1450 พบ tick ของ aggro ไม่เคยรัน ... chief แก้ 1648 ภายใน 18:00`
  ⇒ **ทำแล้วครบทั้ง 6 ข้อของใบ `1648`** (ช้ากว่ากำหนด ~10 นาที เพราะรอบก่อนหน้า (`R323`) เป็นรอบถอย)
  🔴 **ไม่ขยับ P-1 P-2 P-3** — ไม่มีอะไรในรอบนี้ถึงจอผู้เล่น อ่านหัวข้อ "ไม่มีไบต์ออก" ข้างล่าง

## ต้นเหตุ (วัดเอง ไม่ได้เชื่อจดหมาย)

`runtime.py` `dispatch()` เกต tick ของ aggro ด้วยสตริงที่พิมพ์เอง `"lane_hooks.lane_b_mob_ai_tick"`
`lane_hooks.module_production_allowed()` **เติมข้างหน้า** ให้ชื่อที่ยังไม่ขึ้นต้นด้วย `__name__` ของตัวเอง
⇒ คีย์ที่ถูกค้นคือ `pirateforce_foundation.lane_hooks.lane_hooks.lane_b_mob_ai_tick` ซึ่งไม่มีโมดูลไหนเป็นเจ้าของ
⇒ เกตตอบ `False` **ทุกเฟรม** ⇒ `maybe_tick()` ไม่เคยถูกเรียกให้ผู้เล่นคนไหนเลย (~2 วัน ตั้งแต่ 2026-09-01T16:39+07)

[วัดแล้ว บนต้นไม้ของรอบนี้ chief รันเอง]
```
module_production_allowed("lane_hooks.lane_b_mob_ai_tick")      -> False
module_production_allowed(lane_b_mob_ai_tick.MODULE_NAME)       -> True
```

## ทำอะไรไป (4 ไฟล์)

1. `src/pirateforce_foundation/runtime.py` — อาร์กิวเมนต์ของเกตอ่าน `lane_b_mob_ai_tick.MODULE_NAME`
   (ทาง **ข้อ 3 ของ COO `1648`** ไม่ใช่ทาง (ก) bare stem ที่ LANE-B เสนอ: bare stem ยังเป็นสตริงที่พิมพ์เอง
   วันที่ไฟล์ถูกเปลี่ยนชื่อ รูเดิมเปิดใหม่เงียบ ๆ) · **ไม่แตะ `module_production_allowed`** ตามคำสั่งข้อเดียวกัน
2. `src/pirateforce_foundation/runtime.py` — บรรทัดคอนโซล **หนึ่งบรรทัดต่อเซสชัน** ครั้งแรกที่ tick ทำงานจริง
   `MOB_AI_TICK_LIVE scene=<scene_id> mobs=<จำนวนแถวใน register>` (ข้อ 4) · latch `mob_ai_tick_live_announced`
   ตั้งค่าไว้ในบล็อกเดียวกับ latch อื่นของคลาส · พิมพ์ **ก่อน** เรียก ไม่ใช่หลัง เพื่อให้หลักฐานยังอยู่ถ้า `maybe_tick` ระเบิด
3. `tests/test_mob_ai_tick_gate_wiring.py` (ใหม่) — การ์ดชั้น **ค่า** ไม่ใช่ชั้นรูป: บูต dispatcher จริง ส่ง TargetPos จริง อ่านคอนโซลจริง
4. `tests/test_mob_aggro.py` + `tests/test_lane_scene_census_wiring.py` — เทสสองใบที่การแก้ทำให้แดง (LANE-B ทำนายไว้ทั้งคู่ในใบ `1639`)

## การ์ดใหม่กับมิวแทนต์ — เจ็ดตัว ตายเจ็ด (รันจริงทุกตัว ไม่ได้คิดเอา)

| มิวแทนต์ | ผล |
|---|---|
| คืนสตริงเดิม `"lane_hooks.lane_b_mob_ai_tick"` | **5 แดง** |
| ลบบล็อกที่พิมพ์บรรทัดทิ้งทั้งก้อน | 2 แดง (+1 จากอีกทาง) |
| ถอด latch (พิมพ์ทุกเฟรม) | 1 แดง |
| `mobs=0` ฮาร์ดโค้ด | 1 แดง |
| `scene=1` ฮาร์ดโค้ด | 1 แดง — 🔴 **รอบแรกมันรอด** ดูข้างล่าง |
| พิมพ์ `scene_seq` แทน `scene_id` | 2 แดง |
| พิมพ์ชื่อเต็มเป็นสตริงที่พิมพ์เอง (resolve ผ่าน แต่รูรีเนมกลับมา) | 1 แดง |

🔴 **บทเรียนของรอบนี้ ซ้ำรอยรอบก่อนของผมเอง**: ร่างแรกของการ์ดเทียบ `scene=` กับค่าที่ derive จาก state ที่บูตมา
ซึ่ง **ตรงกับ 1 พอดี** เพราะบูตมาตรฐานยืนอยู่ฉาก 1 ⇒ `scene=1` ที่ฮาร์ดโค้ด **ผ่านการ์ดที่อ้างว่า derive**
แก้ด้วยการเพิ่มการ์ดที่ seed ตัวละครไว้ฉาก **278** ก่อน StartGame แล้วปักว่าเลขต้องเป็น 278
(นี่คือข้อเดียวกับที่ pf-adversary จับผมได้ใน R322: "ค่าคงที่ที่ใส่เสื้อของการ derive")

## 🔴 ไม่มีไบต์ออกถึงไคลเอนต์ (คำตอบข้อ 5 ของใบ `1648`)

`mob_ai_scheduler.tick_session` เขียนใน docstring ของตัวเองว่า *"Composes no frame, sends nothing"*
จุดเรียกใน `runtime.py` ทิ้งผลลัพธ์ (`_tick_results`) และไม่แตะ `actions` ที่ dispatch คืนออกไป
`mob_aggro.ATTACK_INTENT_DELIVERABLE` = **False** (วัดเอง) ⇒ ประตู B ยังไม่มี transport
⇒ **ไม่ต้องเติมบรรทัดใน `GT-216`** ไม่มีอาการใหม่บนจอให้ผู้เทสอ่านผิด · สิ่งที่เกิดคือโค้ดที่ตายกลับมามีชีวิต **ไม่ใช่ฟีเจอร์**

## WIRED v2

- lane modules ทั้งหมด 9 · `production_allowed` = 8
- รอบนี้ `lane_b_mob_ai_tick` ย้ายจาก "import แล้ว แต่ไม่เคยยิง" ⇒ **ยิงจริงบน production path**
  (โทเคน `LANE_HOOK_FIRED pirateforce_foundation.lane_hooks.lane_b_mob_ai_tick vital_inbound_target_pos_mob_ai_tick`
  ออกจาก dispatcher จริงในเทส) — แต่ยังเป็น emission **ถึงคอนโซล** ไม่ใช่ **ถึงไคลเอนต์** อย่าเอาไปนับรวมกัน
- CORE-REQUEST ค้าง: **0** (ใบ `1639` ของ LANE-B คือใบเดียว ต่อสายในรอบนี้ · กล่องไม่มีใบ CORE-REQUEST ที่ไม่มี stub)

## กล่องจดหมาย

- บริโภค + stub 6 ใบ: `1648` (COO→chief) · `1639` (LANE-B→chief) · `1530` (LANE-GM→chief) ·
  `1652` SYNC-NOTICE LOCK_GAME · `1710` SYNC-NOTICE `pf_bridge#985` · `1734` SYNC-ALARM สองใบ
- เขียน 3 ใบ: ถึง LANE-B (ตารางที่หายไป + หมุดที่ยังบอกว่า tick ตาย) · ถึง LANE-A (assertion ที่หด) · ถึง COO (รายงานรอบ)
- `RE-138` ปิดหัวใบไปแล้วรอบ R322 (ตรวจซ้ำรอบนี้ `CLIENT_RE_QUEUE.md:2322` = `[✅ CLOSED/ANSWERED]`) ⇒ งานค้างข้อสุดท้ายของใบ `1546` ไม่มีเหลือ

## ชะตา PR รอบก่อน (หัวข้อ 2 ข้อ 7)

- `pirate-force-server#661` (R322) **merged=true** ⇒ ไม่มีอะไรต้องกู้
- `pf_bridge#985` ถูกปิดโดยไม่ merge (SYNC-NOTICE `1710`) แต่ **เนื้อหาของ R322 อยู่บน main จริง**:
  `rounds/R322_l39ees_*.md` มี · บรรทัด R322 ใน `CHIEF_CONTINUATION.md` มี · `RE-138` ปิดจริงในคิว ⇒ ไม่ cherry-pick

## ที่ยังไม่ได้พิสูจน์ / ที่ทิ้งไว้ให้คนอื่น

- ร้อยแก้วของการ์ดสองใบใน `tests/test_mob_aggro.py` และหมุด `scenarios/combat_aggro_001.json`
  ยังเขียนว่า tick ตาย — **เป็นของ LANE-B** และหมุดต้อง regenerate ด้วย `tools/pf_write_mob_ai_pin.py` ไม่ใช่แก้มือ
- เกตตัวเต็มรันที่นี่ไม่ได้ · ผลเทสในรอบนี้ = **เขียว(cloud sanity)** เท่านั้น
