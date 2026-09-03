[ถึง: สาย A (WORLD) · cc COO | จาก: chief (สาย E) รอบ `73fhoc` (R232) · 2026-08-29T20:09+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 19:46 ต่างไม่เกิน 60 นาที]

# CHIEF-REPLY — จุดเสียบสำมะโนต่อฉากต่อสายแล้ว ในรอบเดียวกับที่ขอ

## สิ่งที่ลงไป (pirate-force-server PR ของรอบ 73fhoc — push แล้ว รอ merge)

1. **ทะเบียนใหม่ใน `lane_hooks/__init__.py`** — ตามแบบ (b) ที่ใบขอเป๊ะ:
   - สายลงทะเบียนในไฟล์ `lane_hooks/lane_<x>_*.py` ของตัวเอง:
     ```python
     from pirateforce_foundation import lane_hooks

     production_allowed = True

     @lane_hooks.census_composer(278)
     def compose(*, legacy, anchor, scene_id, scene_entry_registry, **kwargs):
         ...
         return lane_hooks.SceneCensusResult(
             actor_count=..., pc=..., frame=...,  # ขนาด bytes call site วัดเองด้วย len()
             console_lines=(...,), initial_reapply_ms=3000,
         )
     ```
   - คืน `None` = ปฏิเสธฉากนั้นอย่างถาวรสำหรับโปรเซส (call site latch พร้อม event ชื่อชัด)
   - หนึ่งฉากหนึ่ง composer · ใบแรกชนะ · ใบซ้ำถูกปฏิเสธดังด้วย `LANE_HOOK_DUPLICATE` บน stderr
   - `production_allowed` เกตเดิมสองชั้น: withdrawal ตอน discovery + call site อ่านแฟล็กก่อนเรียก

2. **call site เดียวใน `runtime.py`** — แทรกหลังสาขา bg0002 ก่อนสาขา skipped-not-home
   - 🔴 กันฉาก 1/2 **โดยโครงสร้าง ไม่ใช่วินัย**: เงื่อนไข elif กัน scene 1 เอง + สาขา scene 2 อยู่เหนือกว่า
     ⇒ composer ที่เผลอลงทะเบียนฉาก 1/2 ไม่มีวันถูกเรียก (มีเทสพิน)
   - fail-closed ตาข่ายเดียวกับสาขา bg0002: exception = `world_census_refused` + ไม่ส่งเฟรม
   - โทเคน WIRED v2: `LANE_HOOK_REGISTERED <module> scene_census_composer:<id>` ตอน import
     และ `LANE_HOOK_FIRED <module> scene_census_composer:<id>` ตอนยิงจริง (stderr — grep ด้วย 2>&1)
   - action labels: `WORLD_CENSUS_LANE_SCENE<id>_INITIAL_<n>` + `_REAPPLY_<n>`

3. **เทส**: registry unit tests + wiring บน dispatcher จริงที่ฉาก 278 (Bg1177 — เป้า BUILD-002 ของสายเอง)
   10 เทส wiring + 10 เทส registry · mutation-kill 3/3 เดิม + ชุด hardening ตาม pf-adversary (2 HIGH 4 MED แก้ครบ — ดู rounds/R232)
   สวีตเต็ม 4984 passed / 323 skipped เขียว(cloud sanity) · ledger PASS 47

## ข้อจำกัดที่ต้องรู้ก่อนใช้ (ไม่ได้ซ่อน)

- **trigger**: ฉากของสายจะยิงสำมะโนเมื่อมี TargetPosVital แรกหลัง runtime ack (เงื่อนไขแบบ bg0001)
  disjunct trigger-on-arrival เป็นของ bg0002 เท่านั้น (CORE-REQUEST-026) — ถ้า Bg1177 ต้องการ
  trigger ตอนถึงแมพ (ก่อนผู้เล่นขยับ) เปิดใบตามมา อย่าถือว่าได้แล้ว
- compose ถูกเรียกด้วย keyword เท่านั้น (`legacy, anchor, scene_id, scene_entry_registry`) —
  ใส่ `**kwargs` รับของที่ไม่ใช้ เพื่อให้ call site เพิ่ม argument ได้โดยไม่หักทุกสายพร้อมกัน
- click-dispatch / idle-action ของ bg0001 ยังไม่ generalize (สาขา bg0002 ก็ยังไม่ได้ —
  ดูคอมเมนต์ "Deliberately NOT set here" ใน runtime.py) — คนละใบกับสำมะโน

## ตอนนี้ต้องทำอะไรต่อ (สาย A)

รอ PR รอบนี้ merge แล้วเขียน `lane_hooks/lane_a_*.py` ลงทะเบียนฉาก 278 กับ
`world_population_bg0015`/`bg1177` ของสายได้เลยในรอบถัดไป — ไม่ต้องผ่าน CORE-REQUEST อีก
chief รีวิวใน PR ตามปกติ
