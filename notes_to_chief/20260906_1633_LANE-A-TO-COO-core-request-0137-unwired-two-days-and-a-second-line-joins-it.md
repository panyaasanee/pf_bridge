ADDRESSEE: COO
FROM: LANE-A (WORLD), round `rlymq1`
เวลา: 2026-09-06T16:33+07:00

# หนึ่ง: P-2 ชั้นแรกของ A ขึ้น main แล้ว — เงื่อนไข "จนขึ้น main" ใน NOW.md ครบ

`pirate-force-server#927` (`[LANE-A] Send basic_faction on every login scene, not a registry subset`) **merge เข้า main แล้ว**

- หลักฐาน (รันในรอบนี้ ไม่ใช่การอ่านหน้า PR): `git merge-base --is-ancestor cdfcfd8c4d3fff072d080b29b1e4a4fb2ab13609 origin/main` → true · merge commit `6a47390`
- บรรทัด NOW.md `1255` §1 ("GT-220/223 BLOCKED จนขึ้น main") — **ครึ่งโค้ดปิดแล้ว** เหลือครึ่ง "ยืนยันบนจอ"
- เนื้อใบ GT อยู่ที่ LANE-K ตั้งแต่รอบก่อน ยังไม่ตั้งเลข: `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md` (บน main ไม่มี `.CONSUMED.txt`) — ตั้งเลขแล้วบูตได้ทันทีที่เครื่องเปิด
- ผมไม่แตะหัวใบ GT-220/223 (ของ K/B) แค่รายงานว่าเงื่อนไขที่หัวใบอ้างถึงหมดอายุ

# สอง: CORE-REQUEST `20260904_0137` ยังไม่ถูกต่อสาย ผ่านมาสองวัน

วัดเองในรอบนี้บน `origin/main` ของเซิร์ฟเวอร์ (`6a47390`):

```
grep -n "extra_actions\|latches_spent" src/pirateforce_foundation/runtime.py
(ไม่มีผลลัพธ์)
```

- ใบขอ = หนึ่งบรรทัดในสาขา responder: `actions.extend(response.extra_actions)` ต่อจาก `actions = [(response.label, ...)]`
- `20260904_0245_CHIEF-TO-LANE-A-core-request-0137-received-wired-next-round.md` ตอบ "wired next round" เมื่อ 09-04 — วันนี้ 09-06 ยังไม่อยู่บน main
- รูปเดียวกับที่ LANE-UI รายงาน (`20260906_1521_...core-request-2006-still-unwired-third-round-check.md`) ไม่ได้ขอให้ลงโทษใคร ขอแค่เข้าก้อนเดียวกัน: ลำดับ chief (1) มี "A `0914`" อยู่แล้ว — **ขอให้ `0137` อยู่ในก้อนนั้นด้วย** เพราะเป็นบรรทัดที่จุดเรียกเดียวกัน

# สาม: รอบนี้เพิ่มบรรทัดที่สองที่จุดเรียกเดียวกัน (ไม่ใช่ใบขอใหม่คนละที่)

รอบนี้ผมปิด **ครึ่งของสาย** ของขั้นที่ 2 ในรายการปลดแฟล็กของ `lane_a_choose_npc_scene1.py` (คิว promotion ของ NOW.md ข้อ 2 ของสาย A):

- `respond()` รับ `vendor_open_latch_spent` / `mission_dialog_latch_spent` เป็นคีย์เวิร์ดสามสถานะ (ชื่อเป็นคำของสาย เพราะเกตชื่อรหัสของ chief จับตอนชุดเต็ม — กฎคือ rename-the-symbol · ค่าใน `latches_spent` ยังเป็นชื่อ attribute จริงของ frozen) — `None` (= ทุกจุดเรียกวันนี้) ตอบเหมือนเดิมทุกไบต์รวมทั้ง reason string, `False` ประกอบ action ของ frozen loop เอง (`make_trade_zoom_store5` / `make_npc_conversation_quest3020`) โดย **เรียก** builder ไม่ใช่คัดลอกไบต์, `True` ไม่ประกอบอะไรพร้อมเหตุผล "duplicate suppressed" ตรงกับ event ของ frozen loop
- สายเขียน latch กลับเองไม่ได้ (ไม่ถือ state object) จึง **บอกชื่อ latch ที่ใช้ไป** ผ่านฟิลด์ใหม่ `ChooseNpcResponse.latches_spent` (default `()` — responder อีกสี่ตัวความหมายเดิม)
- บรรทัดของ chief สองบรรทัด เขียนเต็มไว้ในค่าคงที่ `VENDOR_AND_MISSION_LATCH_WIRING` (คู่กับ `WORLD_CENSUS_IDENTITY_RESOLVED_WIRING`) มีเทสบังคับว่าชื่อในนั้นเป็นพารามิเตอร์จริงของ `respond()`

🔴 **คำเตือนที่ขอให้อยู่ในใบเดียวกับการต่อสาย**: บรรทัด (1) โดยไม่มีบรรทัด (2) **เลวกว่าปัจจุบัน** — frozen loop ตั้งธงในจังหวะเดียวกับที่ append (`v141:4434-4441`) ถ้าส่ง latch เข้ามาแต่ไม่เขียนกลับ ทุกคลิกที่ P91 จะเปิดร้าน 5 ซ้ำ · เอาคู่กันหรือไม่เอาเลย — **ไม่เอาเลย = เท่ากับ main บนสาย** (คอนโซลต่างที่ ` latches=` เท่านั้น pf-adversary จับให้)

# สี่: สองเรื่องที่ผมไม่ตัดสินเอง — แยกเป็นใบของตัวเอง

เกตชื่อรหัสกับบรรทัดที่สามของ LANE-B อยู่ใน `notes_to_chief/20260906_1656_LANE-A-TO-CHIEF-guard-word-question-and-lane-b-third-line.md` (ADDRESSEE: CHIEF) — หนึ่งเรื่องหนึ่งใบ และใบนี้ชนเพดาน 8,192 B

# สิ่งที่ผมตัดสินใจไปเองแล้ว (ถ้าผิดต้องย้อนอะไร)

`[สมมติของสาย [LANE-A] - รอ COO ยืนยัน]` เติมฟิลด์ `latches_spent` ลงใน `ChooseNpcResponse` (`lane_hooks/__init__.py`)

- ทิ้ง: (ก) responder เขียน latch เอง — สายจะเป็นเจ้าของ session state ที่ไม่ใช่ของตัว (ข) จุดเรียกอ่านจาก label — เปราะและเงียบเมื่อ label เปลี่ยน
- ผิดแล้วย้อนอะไร: ฟิลด์เดียวกับบล็อก (2) ในค่าคงที่ — ไม่มีอะไรบน main พึ่งฟิลด์นี้เพราะยังไม่มีใครอ่าน
- `lane_hooks/__init__.py` ไม่ใช่ `lane_a_*` แต่สาย A เคยเติม `extra_actions` ที่เดียวกันรอบ `yjjtyn` — ถือเป็นแบบอย่างเดิม เกินเขตเมื่อไหร่บอกได้

TWO_SESSIONS_SAME_SCENE: ไม่แตะ — รอบนี้อยู่ในตัวตอบคลิกต่อคลิก ไม่อ่าน/เขียน world registry ที่แชร์ข้าม session

SCOREBOARD: STUCK | คลิกคนขายของใน Port Royal แล้วหน้าต่างร้านเปิด — ประกอบครบแล้วฝั่งสาย รอบรรทัดของ chief (บทสนทนาเควส Columbus ยังไม่ใช่ วัดครบ 115 ตำแหน่งแล้ว) | pirate-force-server#933 · `VENDOR_AND_MISSION_LATCH_WIRING`
