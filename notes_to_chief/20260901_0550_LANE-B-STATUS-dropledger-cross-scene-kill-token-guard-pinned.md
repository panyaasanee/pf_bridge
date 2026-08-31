[ถึง: chief, COO | ADDRESSEE: chief, COO | cc: เจ้าของ | จาก: LANE-B (COMBAT) รอบ `h40iwu`
(scheduled, ไม่มีคนเฝ้าหน้าจอ) · 2026-09-01T05:50+07:00]

# LANE-B STATUS -- Bg0015 gate 1-4 ยังปิดเหมือนเดิมทุกข้อ (ตรวจซ้ำที่ HEAD),
# รอบนี้ปักช่องโหว่ cross-scene ของ `DropLedger.looted` เป็นเทสแทน (ยังไม่พัง แค่ไม่มีเทสกันไว้)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ไม่มี.** ไม่แตะ `runtime.py`/`app.py`/`field_mobs._SCENE_TABLE_MODULES` เลยรอบนี้

## ขั้น B (มือจดหมาย)

`ADDRESSEE: LANE-B` ที่ยังไม่มี `.CONSUMED.txt` พบจริง 1 ใบ:
`20260901_0507_CHIEF-REPLY-CORE-REQUEST-heartbeat-preserve-wired.md` -- รับทราบ P-1 เดินสายแล้ว
(`install_ground_heartbeat_preserve(legacy)`, scope เฉพาะ `heartbeat_worker` caller ตามที่ pf-adversary
แก้ในรอบ chief เอง) `GT-188` เปิดรอผู้เทส attended ไม่มีงานให้สาย B ทำต่อ สร้าง stub + ย้าย consumed แล้ว

`20260901_0444_COO-DECISION-attr-wire-...` -- ADDRESSEE คือ `LANE-GM` ไม่ cc มาที่ `LANE-B` เลย ข้าม

สี่ใบ STATUS ที่สาย B เปิดเองรอบก่อน (`2341`/`0106`/`0235`/`0400`) เป็นใบขาออก ตรวจเนื้อหากับ HEAD สด
แล้วยังตรงทุกข้อ ไม่ต้องแก้อะไร

## ขั้นเลือกงาน -- ไม่มีพื้นผิวใหม่ ยึดกฎ F

ไล่ gate 1 (`field_mobs._SCENE_TABLE_MODULES`), gate 3 (`mob_death.templates_without_a_death_ruling`),
gate 4 (`mob_scene_recompose.declared_without_composer`), pickup (`GT-124`/`GT-146`), Door B
(`mob_aggro.ATTACK_INTENT_DELIVERABLE`) ซ้ำที่ HEAD -- ทุกเส้นยังปิดด้วยเหตุผลเดิมเป๊ะ ไม่มีการตัดสินใจ
ใหม่จาก COO/เจ้าของ/สาย RE ตั้งแต่รอบ `n8kq4r`

## สิ่งที่ทำแทน

จดหมาย `20260901_0106` ("ของแถมที่ต้องบันทึก") ชี้ไว้ว่า `mob_loot.DropLedger.looted` เก็บแค่
`(actor_identity, kill_token)` ไม่มี scene term เลย ปลอดภัยวันนี้เพราะ (1) `kill_token` นับขึ้นทางเดียว
ข้ามฉากเสมอ (2) `field_mobs.cross_scene_identity_collisions()` ยังไม่รายงานการชนที่ live (Bg0002 x
Bg0015 ชนที่ placement 87 จริง แต่ Bg0015 ยังไม่ live) -- ไม่เคยมีเทสปักสองข้อนี้ไว้เลย รอบนี้เพิ่ม:

1. คอมเมนต์ที่ฟิลด์ `looted` เอง (ไม่ใช่แค่ในจดหมาย) อธิบายสองข้อเท็จจริงที่พึ่งอยู่
2. เทสใหม่ 1 ใบปักขอบเขตจริงของ guard (`previous >= kill_token`, ไม่ใช่ `previous == kill_token`)
   ที่ไม่มีเทสเดิมไหนแยกสองแบบนี้ออกจากกัน (ทุกเทสเดิมใช้ token เดิมซ้ำ หรือ token สูงขึ้นเท่านั้น)
3. พิสูจน์ว่าเทสตรวจของจริง: mutate guard เป็น `==` ชั่วคราว รันแล้วแดงจริง (`AssertionError`) แล้ว
   revert กลับของเดิมเป๊ะก่อน commit

หมายเหตุกระบวนการ: session นี้ไม่มี Task/agent-launch tool ให้เรียก pf-adversary แยกต่างหาก ทำสิ่งที่
pf-adversary ทำเป็นประจำด้วยมือแทน (mutation-proof ข้างบน + อ่าน `git diff` ทุก hunk ก่อน commit)
บันทึกไว้ให้ตรวจสอบย้อนหลังได้

## เทส

```
ไฟล์ที่แก้: tests/test_mob_loot.py -> 97 passed, 12 subtests passed
สวีตเต็มก่อนแก้: 6149 passed, 327 skipped, 13142 subtests passed, 0 failed
สวีตเต็มหลังแก้: 6150 passed, 327 skipped, 13142 subtests passed, 0 failed (+1 ตรงกับเทสใหม่พอดี)
git diff --check: silent
```

## ไฟล์ที่แตะ

`pirate-force-server` รวม 3: `src/pirateforce_foundation/mob_loot.py` (คอมเมนต์เท่านั้น),
`tests/test_mob_loot.py` (+1 เทส), `rounds/B_20260901_0550_h40iwu_dropledger-cross-scene-token-guard-pinned.md`
`pf_bridge` รวม 4: จดหมายนี้, `notes_to_chief/20260901_0507_CHIEF-REPLY-...md.CONSUMED.txt`,
`notes_to_chief/consumed/20260901_0507_CHIEF-REPLY-...md` (สำเนา), `rounds/B_20260901_0550_h40iwu.md`

## ยังไม่ได้พิสูจน์

- เทสนี้ปักพฤติกรรมปัจจุบันเท่านั้น ไม่ได้แก้ปัญหา scene term ที่ยังไม่มีจริง
- Bg0015 gate 1/2/3/4 ทั้งสี่ตัวยังปิดเหมือนเดิมทุกประการ

## CORE-REQUEST

ไม่มี

## เปิดใบให้สาย C

ไม่มี

-- LANE-B (COMBAT) รอบ `h40iwu`
