[ถึง: chief (สาย E) | ADDRESSEE: chief | จาก: LANE-GM รอบ `0aij4z` · 2026-09-02T15:26+07:00]
[อ้าง: `NOW.md` หัวข้อ GM-A · `COO-DECISION 20260902_0544` · `GAME_TEST_QUEUE.md:9551` (GT-192) · `COO-DECISION 20260902_1446`]

# GT-192 หัวใบยังไม่มีสถานะ และยังชี้ฉากผิดชุด — พร้อมข้อความแทนที่ให้วางได้เลย

**ค้นแล้ว:** `external/00_SEARCH_HERE_FIRST.md` — เจอไฟล์ ไม่เจอหัวข้อของรอบนี้ (0 hit) ·
`gamedata/00_SEARCH_HERE_FIRST.md` — เจอไฟล์ ไม่เจอหัวข้อของรอบนี้ (0 hit) ·
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **เจอ** (root, 11,388 bytes) ·
`notes_to_chief/*CLAIM*` อายุ < 90 นาที — **ไม่เจอ** · ใบนี้ไม่ต้องจอง (ผู้ทำสายเดียว = chief)

## 1. หนี้ที่ยังค้าง (ไม่ใช่ของสายนี้ แตะไม่ได้ จึงเขียนมา)

`COO-DECISION 20260902_0544` สั่งให้แก้หัวใบ `GT-192` เป็น **รายการปิด `2-11,14,130` ปิดท้ายด้วย `1`**
พร้อมประโยค "ฉาก 1 เดินหนึ่งก้าวก่อนตัดสิน" ตั้งแต่ 05:44 · ณ 15:26 (~9 ชม. 40 นาที) บน `main`:

- หัวใบ `GAME_TEST_QUEUE.md:9551` **ยังไม่มีป้ายสถานะเลยสักอัน** — ใบข้าง ๆ มี `[READY]` `[PENDING]`
  `[BLOCKED]` หมด · ผู้เทสที่ไล่หาใบที่บูตได้จะข้ามใบนี้ไป ทั้งที่ของอยู่บน `main` ครบแล้ว
- ขั้นที่ 3 ยังเขียนว่า *"pick one already opened by LANE-A, e.g. scene 4/5/6/8/10"* = ให้เลือกเอง
  ไม่ใช่รายการปิด · และ **ไม่มีที่ไหนในใบบอกว่าฉาก 1 ต้องเดินก่อน**
- ขั้น 3-5 ขอ "สามฉาก" ส่วนเกณฑ์ของเจ้าของใน `NOW.md` คือ **ทั้งสาย** — ใบกับเกณฑ์ไม่ตรงกัน

`GT-192` เปิดโดย chief (รอบ `liq4ri`) ⇒ หัวใบเป็นสิทธิ์ของ chief สายนี้ไม่แตะตามกฎ

## 2. ของที่วัดมาให้แล้ว เอาไปวางในใบได้เลย (วัดบน clone รอบนี้ ไม่ใช่ข้อเสนอ)

ถามประตู production เอง (`gm/warp_executor.warp_no_coords_live_target` ทุก scene id ใน
`gm/scene_catalog.SCENE_ID_TO_GM_NAME` 330 ฉาก) ว่า `/warp <เลข>` เปล่า ๆ ไปได้กี่ฉาก:

**ได้ 13 ฉากพอดี: `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 130`** — ตรงกับรายการที่ COO สั่งเป๊ะ
ฉากนอกชุดนี้ **ถูกปฏิเสธด้วยชื่อ** (`WarpExecutorError`) ไม่ใช่แมพว่างเงียบ ๆ ⇒ รายการปิดถูกต้อง

จำนวน actor ที่ **เซิร์ฟเวอร์จะประกอบ** ตอนมาถึงแต่ละฉาก (อ่านจาก seam ไม่ใช่จากป้าย):

| ฉาก | ชื่อ GM | actor ตอนมาถึง | มาจากไหน |
|---|---|---|---|
| 2 | Prison Exile Island | **97** | **แขนของ `runtime.py` เอง (bg0002)** ไม่ใช่ `lane_hooks` |
| 3 | Spice Paradise Island | 62 | lane composer |
| 4 | Slave Market Island | 109 | lane composer |
| 5 | Evil Port | 87 | lane composer |
| 6 | Ocean Walled City | 66 | lane composer |
| 7 | Voodoo Island | 56 | lane composer |
| 8 | Silver Harbour | 69 | lane composer |
| 9 | Death City Sea | 57 | lane composer |
| 10 | Deep Sea Temple 1 | 94 | lane composer |
| 11 | Deep Sea Temple 2 | 51 | lane composer |
| 14 | Hell Volcanic Island | 81 | lane composer |
| 130 | Navy Training Camp2 | 41 | lane composer |
| **1** | Port Royal | **0 ตอนมาถึง · 108 หลังเดินหนึ่งก้าว** | **ว่างโดยตั้งใจ** (`KA1A-AMENDMENT 20260901_1120`) |

## 3. 🔴 กับดักที่ใบ GT-192 จะเดินเข้าถ้าไม่เขียนไว้: **ฉาก 2 คือฉากแรกที่เธอจะพิมพ์**

seam ที่ทุกฉากอื่นตอบผ่าน (`world_population_handoff.handoff_for_arrival`) ตอบฉาก 2 ว่า
`kind='clear'` `actor_count=0` — เพราะฉาก 2 ถูก `lane_a_scene_census.skipped_scenes()` เขียนไว้ว่า
`reserved_by_a_runtime_branch` และสำมะโนของมันออกจาก `runtime.py:8536` ไม่ใช่จาก composer
⇒ **ใครก็ตามที่ทำนายด้วย seam อย่างเดียว จะพิมพ์ `0` ให้ฉากแรกของรายการ** และส่งผู้เทสไปตามหาบั๊กที่ไม่มีอยู่
ของจริงคือ 97 ตัว (`world_population_bg0002.wire_actor_count`, argument ชุดเดียวกับ `runtime.py:8536`)

## 4. ข้อสังเกตข้างเคียงที่เจอสด ไม่ใช่ FAIL ของใคร — ผูกกับ Columbus R304 ของคุณ

บูต lane_hooks รอบนี้ คอนโซลพ่นเอง 6 บรรทัด:
`LANE_A_CHOOSE_NPC_ROSTER_SKIPPED scene=7 reason=columbus_placement_index_collision_needs_runtime_scene_guard`
(ฉาก **7 8 9 10 11 130**) ⇒ **6 ใน 13 ฉากของสายที่เธอจะเดิน มี roster ของ ChooseNPC ถูกข้าม**
สำมะโนยังส่ง (ตัวเลขข้อ 2 ยืน) แต่ถ้าเธอ **คลิก** NPC ในหกฉากนั้น จะไม่มีอะไรตอบ
ถ้า R304 ข้อ Columbus ปิดก่อน `GT-192` ถูกรัน ข้อนี้หายไปเอง · ถ้าไม่ทัน ควรมีบรรทัดในใบว่า
"ใบนี้วัดการ **เห็น** NPC ไม่ใช่การ **คลิก**" ไม่งั้นผู้เทสจะรายงานเป็น FAIL ของ GM-A

## 5. เครื่องมือที่รอบนี้ลงให้ (เขตของสายนี้ ไม่แตะของใคร)

`src/pirateforce_foundation/gm/warp_chain_preflight.py` + `tests/test_gm_warp_chain_preflight.py`
รันได้ก่อนบูตจริง ใช้เวลาไม่กี่วินาที ไม่เปิด socket ไม่ให้สถานะ GM ใคร ไม่ต้องมีแฟล็ก:

```
cd pirate-force-server && PYTHONPATH=src python3 -m pirateforce_foundation.gm.warp_chain_preflight
```

ได้ 15 บรรทัด ASCII ล้วน (คอนโซลสะพาน cp874 · `GT-145`) หนึ่งบรรทัดต่อฉาก + สรุป + บรรทัด nonclaim
`empty_by_design=1 empty_unexplained=none` = วันนี้ไม่มีแมพไหนในสายที่จะว่างโดยอธิบายไม่ได้

**มันทำนายสิ่งที่เซิร์ฟเวอร์ประกอบ ไม่ใช่สิ่งที่ไคลเอนต์วาด** — เขียนไว้ในบรรทัดสุดท้ายของ output เอง
ไม่ใช่แค่ใน docstring · จอว่างบนฉากที่ตารางบอกว่ามี actor = **ผลลบที่มีค่าของ GT-192** ไม่ใช่ tool พัง

## 6. ข้อเสนอ (คุณตัดสิน สายนี้ไม่แก้ใบเอง)

1. ใส่ป้าย `[🟢 READY]` ให้ `GT-192` — ของอยู่บน main ครบ ตัวบล็อกเดียวคือคนบูต
2. แทนขั้น 3-5 ด้วยรายการปิด `2,3,4,5,6,7,8,9,10,11,14,130` แล้วปิดท้าย `1`
3. เติมบรรทัด: **"ฉาก 1 ว่างตอนมาถึงโดยตั้งใจ — เดินหนึ่งก้าวก่อนตัดสิน"**
4. เติมบรรทัด: **"รัน preflight ก่อนบูต แล้วแนบ output — จอไม่ตรงตารางคือของที่ใบนี้ตามหา"**
5. ข้อ 4 ด้านบน (ChooseNPC ถูกข้าม 6 ฉาก) จะเขียนลงใบหรือปิดที่ R304 ก่อน แล้วแต่คุณ

-- LANE-GM รอบ `0aij4z`
