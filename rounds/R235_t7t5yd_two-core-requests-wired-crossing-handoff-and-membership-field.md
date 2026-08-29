# R235 (t7t5yd) — 2026-08-30T01:1x (+07:00) — สาย E

[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 00:50 (ต่าง 22 นาที)]

## ทำอะไรไปบ้าง (pirate-force-server · 6 ไฟล์ · รอ merge PR #291)

1. **CORE-REQUEST 2246 (สาย B, COO เคาะ 23:42) ต่อสายแล้ว** — บล็อก MOB_LOOT ใน
   `runtime.py._dispatch_mob_combat` เป็นห้าบรรทัด `mob_drop_presence.sustain_a_kill`
   ตามสเปกคำต่อคำ: การ์ด `if drops:` ถอด · ลูป prune ลบทิ้งไม่แทนที่ · ไม่ใส่
   `prune_previous_kills` · import เพิ่มหนึ่งบรรทัด
   เทส wiring ใหม่ `tests/test_mob_drop_presence_wiring.py` 4 ใบ ขับ dispatcher จริง:
   คิลไม่ตกของยังพาของบนพื้นมาด้วย (พื้น pre-seed ด้วยคิล Bg0002 จริงผ่าน cell เพราะตาราง
   drop ของ bg0001 ว่างจริงตาม R221) · แถวที่เพิ่งประกาศยังอยู่ใน ledger · เส้นทางยิง
   console line + event เสมอ · mutation-kill 3/3 (การ์ดคืน = แดง 2 ใบ · prune คืน = แดง 1 ใบ)
   ⇒ ด่านบิลด์ของ `RIDER-149-A` (บรรทัด `MOB_DROP_PRESENCE`) จะผ่านทันทีที่ #291 merge

2. **COO-DECISION 2254 ต่อสายแล้ว** — `runtime.py` เรียก
   `world_population_handoff.handoff_on_crossing` ที่บล็อก crossing commit
   (หลัง `confirmed_fields()`): clear เข้าคิว**ก่อน** teleport · census เข้าคิว**หลัง** + reapply
   ตาม `dispatch_slot` ที่ handoff ประกาศเอง · action พินไบต์กับ compose อิสระ (adversary D1)
   · membership: **เฉพาะ census ข้ามกลับฉากบ้าน**เขียนสามฟิลด์ + ตรา recompose ครบชุด
   (adversary D6) · census ฉากอื่น (roster) ส่งเฟรมแต่ **withhold membership** + event ชื่อชัด
   เพราะ ChooseNPC ตัวเดียวในทรีพูดตาราง bg0001 = KeyError หลุด connection (adversary D2
   วัดแล้ว 16/81) → คำถามรากเป็น ASK-COO ใบ `20260830_0155` · unavailable = ทิ้ง membership
   ตามสัญญา seam · `world_census_identity_resolved` คงอยู่เฉพาะ census ฉากบ้าน
   ตรวจก่อนต่อ (คำเตือนสาย A ใบ 2305): `#285` merge แล้ว `ROSTER_COMPOSERS` บน main
   เหลือ bg0015 ใบเดียว ไม่มีฉาก 2
   เทส `tests/test_world_population_handoff_wiring.py` 4 ใบ ขับ dispatcher เดินเข้าประตูจริง
   (debug boot — ทางเดียวที่ประตูเปิดได้ เหตุผลเดียวกับเทส liveness) · mutation-kill 2/2
   (สลับ slot / ตัด membership write)
   guard test ใน `tests/test_world_population_bg0015.py` อัปเดตเป็นเซตสองผู้เรียก
   ตามที่คอมเมนต์ของมันสั่งไว้เอง (ผู้เรียกใหม่ต้องมีเหตุผลเป็นลายลักษณ์)
   🔴 ความจริงที่ต้องพูดตรง: ประตู travel gate บน production ยัง inert (debug-only)
   เส้น crossing จึง "ติดอาวุธ" รอวันประตูเปิด — ของที่ถึงผู้เล่นวันนี้สำหรับฉาก 14
   คือจุด lane census ตอน login ที่ต่อไว้ R232 ซึ่งเดินผ่าน seam เดียวกันอยู่แล้ว

3. **CORE-REQUEST 2321 (สาย A) ตอบทาง (ก)** — `SceneCensusResult` ได้ฟิลด์
   `membership: Any | None = None` (default ⇒ ตัวประกอบเดิมไม่หักทุกตัว) · call site
   coerce ในตาข่าย fail-closed แล้วเขียน `population_indices` /
   `population_refresh_anchor` / `world_census_indices` **สามฟิลด์พร้อมกัน** เมื่อไม่ None
   · membership รูปผิด = refuse census ทั้งใบ ไม่ half-write
   เทสใหม่ 3 ใบใน `tests/test_lane_scene_census_wiring.py`
   ⇒ สาย A แก้ตัวประกอบของตัวเองหนึ่งบรรทัดได้รอบถัดไป

## หลักฐาน
- สวีตเต็มหลังแก้ตาม adversary **5305 passed 0 failed** (323 skipped ตามพิน) เขียว(cloud sanity)
- `HYPOTHESIS_LEDGER PASS entries=47` (ขั้นบังคับข้อ 7 ก่อน commit)
- mutation-kill 9/9 · เทส wiring ใหม่ 14 ใบ ขับ dispatcher จริง
- ทุกบรรทัดที่เพิ่มใน src/tests เป็น ASCII ล้วน (ตรวจด้วย encode ไม่ใช่ตามตา)
- pf-adversary รีวิวก่อน commit: 7 ข้อ แก้ 5 (D1 D2 D3 D5x3 D6) ส่งต่อ 2 (D4 unmeasured ·
  D7 ของสาย B) — รายละเอียดในจดหมาย FROM_CHIEF_R235 และ ASK-COO 0155

## ที่ไม่ได้พิสูจน์
- ชั้น client-observable ทั้งหมด (G-OBS): ของค้างบนพื้น/ป้ายกลับมา = `RIDER-149-A` ·
  ประชากรตามการข้ามฉาก = ยังไม่มีใบ (ประตู production ยังปิด)
- "การส่งซ้ำวาดป้ายใหม่จริงไหม" ยัง unmeasured (`REEMISSION_REDRAWS_THE_LABEL=None`)

## งานถัดไปของ chief (กำหนดจาก COO 0046: ภายใน ~03:00)
จุดเสียบสาย B สามจุด (หลังคอมมิตการตี · หลังประกอบ bar/death frame · หลังคำขอเก็บของ)
+ ขยายทรง `census_composer` ให้ครอบ recompose — เหตุที่ไม่ลงรอบนี้: PR #291 ชนเพดาน
~6 ไฟล์แล้ว และ COO เคาะลำดับให้ 2246 ไปก่อนเอง (ใบ 0046)
