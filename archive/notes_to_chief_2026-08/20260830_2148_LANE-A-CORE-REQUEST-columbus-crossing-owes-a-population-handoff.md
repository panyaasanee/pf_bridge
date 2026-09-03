[ถึง: chief | ADDRESSEE: chief | cc: COO, เจ้าของ, สาย B, สาย GM | จาก: LANE-A (WORLD) รอบ `czoo9t` · 2026-08-30T21:48+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · อ้างอิง: `RE-162` Job 4, `GT-106` (PENDING), `COO-DECISION 20260829_2254`]

# LANE-A CORE-REQUEST — **ทั้งเมือง Port Royal ตามผู้เล่นออกทะเลไปด้วย** · เฟรมที่แก้เรื่องนี้ประกอบเสร็จแล้ว รอ `runtime.py` คิวมันเท่านั้น

## สรุปหนึ่งบรรทัด

การข้ามฉากเดียวที่ผู้เล่นทำเองได้บนบูตปกติ (คุย Columbus → แถว 3021 → ฉาก 17) **ส่งแค่
`TeleportVital` อย่างเดียว** ไม่มี population handoff ตามไป ผลคือ actor collection ของ Port Royal
ที่ไคลเอนต์ถืออยู่ตั้งแต่ login **ยังอยู่ครบ** หลังข้ามฉาก — สำมะโนที่ทรีนี้ประกอบให้ login คือ
**115 actor** (`world_population.census_count_for_dispatch() -> (115, 'full_census')`, วัดใหม่รอบนี้
ไม่ได้ยกมาจากจดหมายเก่า) ⇒ ผู้เล่นออกทะเลไปพร้อมคนทั้งเมืองยืนอยู่บนน้ำรอบตัว

## นี่ไม่ใช่ข้อสังเกตใหม่ของสาย A คนเดียว — สองแหล่งอิสระเจอรูเดียวกัน

1. **สาย A เอง** `columbus_quest_dispatch._emit_arrival_stowaways` พิมพ์ `WORLD_POP_STOWAWAYS`
   ตรงจังหวะนี้มาตั้งแต่รอบ `2pdf6j` — เป็น **รายงาน** ว่าใครยังถูกถืออยู่ ไม่เคยมีใครประกอบเฟรมที่ปิดรูนี้
2. **`RE-162` Job 4** (`notes_to_chief/20260830_1909_RE-162-RESULT-IN-SESSION-SCENE-CHANGE-WIRE-EXISTS-CLIENT-OBSERVABLE-UNPROVEN.md`)
   เขียนไว้เองเป็น negative finding: *"the Columbus in-session crossing sends the teleport frame
   alone ... nothing in this clone's committed source sends one."*

`world_population_handoff.handoff_on_crossing` — เลนที่สาย A สร้างไว้เพื่อจังหวะนี้พอดี — ถูกต่อสายใน
`runtime.py` **ที่เดียว** และที่นั่นคือเลน travel-gate (`runtime.py:7146`) ซึ่ง **ปิดโดย default ตามคำสั่ง
เจ้าของ** (`COO RULING 20260826`) ส่วนสาขา Columbus (`runtime.py:4971-5044`) ไม่เคยเรียกมันเลย

## สิ่งที่รอบนี้สร้างเสร็จแล้ว (อยู่ใน write zone ของสาย A ทั้งหมด ไม่แตะ `runtime.py`/`app.py`)

`src/pirateforce_foundation/world_m2_crossing_handoff.py` (ใหม่) ป้อน `SceneEntry` ที่ dispatch
ผลิตอยู่แล้ว เข้า seam ที่ ship อยู่แล้ว แล้วคืน `SceneHandoff` มาให้ครบ — kind / reason / bytes /
dispatch slot / membership reset **ไม่มีอะไรถูกคิดขึ้นใหม่ในไฟล์นี้เลย ทุกค่าเป็นคำตอบของ encoder เดิม**

วัดจริงสำหรับฉาก 17 วันนี้: `kind=clear`, `pc=17B`, `frame=27B`, `slot=before_teleport`,
`membership_reset.clears_everything = True` และ `frame == legacy.frame_pc(pc)` (พินไว้ในเทส)

บรรทัดคอนโซลที่ **บูตปกติพิมพ์ตั้งแต่วันนี้** ไม่ต้องมีแฟล็ก ไม่ต้องมี scenario:

```
WORLD_M2_CROSSING_HANDOFF scene=17 kind=clear held=115 composed=YES dispatched=NO
  pc=17B frame=27B slot=before_teleport
  reason=scene_17_left_empty_on_purpose_sea_scene_no_cline_type_mob_set_placements_unresolvable_gt078
```

## CORE-REQUEST (บรรทัดเดียว)

> `runtime.py` สาขา Columbus success (`:5028-5044`): เรียก `world_m2_crossing_handoff.crossing_handoff(legacy, entry)` คิว `handoff.pc/frame` **ก่อน** action teleport ตาม `handoff.dispatch_slot` แล้ว apply `handoff.membership_reset` และส่ง `crossing_handoff_dispatched=True` ที่ call ของ `dispatch_columbus_quest3021` ในการแก้ครั้งเดียวกัน

รูปเต็มของบล็อก (คัดลอกรูปแบบจากบล็อก crossing ที่ chief เขียนเองแล้วที่ `:7146-7255`
ไม่ได้คิดรูปใหม่):

```python
else:
    handoff = world_m2_crossing_handoff.crossing_handoff(legacy, entry)
    print(world_population_handoff.handoff_console_line(handoff))
    tp_pc, tp_frame = legacy.make_login_teleport(*entry.teleport_fields)
    crossing_actions = [(
        "CORE_REQUEST_014_COLUMBUS_Q3021_TELEPORT_SCENE17_ONCE",
        tp_pc, tp_frame, 0.0,
    )]
    if handoff.sends_a_frame:
        handoff_actions = [(handoff.label, handoff.pc, handoff.frame, 0.0)]
        if handoff.dispatch_slot == world_population_handoff.SLOT_BEFORE_TELEPORT:
            crossing_actions = handoff_actions + crossing_actions
        else:
            crossing_actions = crossing_actions + handoff_actions
    actions = actions + crossing_actions
    # ทั้งสองฟิลด์พร้อมกันเสมอ ตาม MembershipReset (ครึ่งเดียวคือบั๊ก)
    reset = handoff.membership_reset
    self.population_indices = reset.population_indices
    self.population_refresh_anchor = reset.population_refresh_anchor
    self.world_census_indices = reset.population_indices
    self.events.append("core_request_014_columbus_scene17_teleport_sent")
    self.events.append(f"world_m2_crossing_handoff_{handoff.kind}_scene_{handoff.scene_id}")
```

### สี่เรื่องที่ต้องอ่านก่อนต่อสาย ไม่ใช่รายละเอียดปลีกย่อย

1. **ลำดับสำคัญกว่าตัวเฟรม** clear เป็นของฉากที่ไคลเอนต์ยัง render อยู่ ⇒ ต้องอยู่ **ก่อน** teleport
   (`slot=before_teleport` เป็นคำตอบของ handoff เอง ไม่ใช่กติกาที่ต้องจำ) อย่า hardcode ลำดับ ให้อ่าน
   `handoff.dispatch_slot` เหมือนบล็อก `:7172-7183` ทำอยู่แล้ว
2. **`membership_reset` ต้องเอาไปทั้งคู่** ถ้าคิว clear แล้วปล่อย `population_indices` เดิมไว้
   `handoff_report` เขียนเตือนไว้เองที่ `:1048-1056`: **คลิก ChooseNPC ครั้งเดียวจะ recompose ทั้ง
   เมืองกลับเข้าไปในฉากใหม่** — คือกลับไปแย่กว่าเดิม ไม่ใช่เท่าเดิม
3. **`self.world_census_indices` ต้องรีเซ็ต *หลัง* dispatch คืนค่าแล้ว** ไม่ใช่ก่อน — บรรทัด
   `WORLD_POP_STOWAWAYS` และ `WORLD_M2_CROSSING_HANDOFF` ทั้งคู่อ่านค่านี้ผ่าน `held_indices` ถ้ารีเซ็ต
   ก่อน ทั้งสองบรรทัดจะรายงาน 0 ในรอบที่มันควรรายงาน 115 (นี่คือรูป `k882hm-D3` ที่บล็อก `:7203-7206`
   ของ chief เขียนกันไว้เองแล้ว)
4. **ประกอบสองครั้ง — ยอมรับและบอกไว้ตรงนี้ ไม่ได้ซ่อน** dispatch ประกอบครั้งหนึ่งเพื่อพิมพ์บรรทัด
   และบล็อกนี้ประกอบอีกครั้งเพื่อเอา bytes ทางเลือกที่ไม่ต้องประกอบสองครั้งคือเปลี่ยนรูป return ของ
   `dispatch_columbus_quest3021` ซึ่ง **จะพัง call site เดิมที่อ่าน `entry.teleport_fields`** จึงไม่ทำ
   สำหรับ clear 27 ไบต์ต้นทุนคือศูนย์ ถ้าวันหนึ่ง crossing ไปลงฉากที่มี roster จริง ให้รื้อจุดนี้ก่อน

### หมายเหตุ census ที่จะแดงตอน chief ต่อสาย (เตือนล่วงหน้า ไม่ใช่บั๊ก)

`tests/test_world_population_bg0015.py` สำมะโน call site ของ `handoff_on_crossing` ใต้ `src/`
และอนุญาต **หนึ่ง call ต่อหนึ่งไฟล์** รอบนี้อัปเดตให้เป็นสามไฟล์แล้ว (`lane_a_scene_census.py`,
`runtime.py`, `world_m2_crossing_handoff.py`) พร้อมเหตุผลเขียนไว้ในเทสเอง — บล็อกของ chief
**ไม่เพิ่ม call ใหม่** เพราะเรียกผ่าน `crossing_handoff` ไม่ใช่ `handoff_on_crossing` ตรง ๆ
ถ้า chief เลือกเรียก `handoff_on_crossing` ตรง ๆ ใน `runtime.py` แทน จะกลายเป็น call ที่สองในไฟล์
ที่ blessed แล้ว และเทสนั้นจะแดงโดยตั้งใจ — ให้แก้ที่โค้ด อย่าแก้ที่เทส

## สิ่งที่ยังไม่มีใครเห็น และใบนี้ไม่อ้าง

ยังไม่มีมนุษย์คนไหนเห็นไคลเอนต์ render ฉาก 17 เลย: `GT-106` ยัง `PENDING` และ `RE-162` ระบุว่า
in-session transition ยัง **client-observable UNPROVEN** ⇒ "ทะเลจะว่างหลังต่อสาย" คือสิ่งที่ **ไบต์บอก**
ไม่ใช่สิ่งที่ใครเห็น ใบนี้อ้างแค่อย่างแรก **ไม่ตั้งสถานะ PASS/FAIL ให้ใบไหนทั้งสิ้น (G-OBS)**

**ขอ chief เปิดใบเทส (attended) หนึ่งใบ** ต่อจาก `GT-106-R2`: เมื่อ clear มาถึงกลางเซสชันก่อน
teleport ไคลเอนต์ **ลบ actor ของฉากเก่าออกจริงหรือไม่** — คนละคำถามกับ `GT-106-R2` (นั่นถามว่า
ฉากปลายทาง render ไหม) ไม่เปิดเองเพราะใบ `GT` เป็นของ chief

— LANE-A (WORLD) รอบ `czoo9t`
