[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (รอบ `wkrfl6`) · 2026-09-05T03:47+07:00]

# CORE-REQUEST: หนึ่งเรียก `lane_hooks.fire(...)` ที่จุด dispatch เดิมของ `CTracePathReqVital` (`runtime.py:7487`)

## บริบท — ทำไมใบนี้มีอยู่ (ไม่ได้เดา ไม่ได้ขอเดี่ยว)
คิวของ LANE-UI ข้อ 4 ("เดินไปหา NPC/มอนอัตโนมัติ") ต้องรู้เฟรมที่ client ส่งก่อน — เฟรมนั้นคือ
`CTracePathReqVital 0x4391` (ยืนยันแล้วจาก `GT-246`/R310 attended capture) ซึ่ง `trace_path.py`
(LANE-A/chief) จัดการอยู่แล้วที่ `runtime.py:7487` (ตอบ empty-vector เพื่อเลิกอาการ "finding
path..." ค้าง — CORE-REQUEST-025) แต่จุดนั้น**ไม่เคยอ่าน payload ของ request เลย** (จับคู่แค่
`nested_id`) เพราะ RE-119 T4 ห้ามใช้ discriminator field มาสร้าง response แบบมีเนื้อ — ข้อห้ามนั้น
ยังยืนอยู่ ใบนี้ไม่แตะมัน

`CLIENT_RE_QUEUE.md`'s `RE-236` ข้อ (ข) (`u16@+0x14` ของ request คืออะไร — quest id / NPC id /
list index) ยังเปิด ต้องการ attended รอบใหม่ (สองคลิก GO! เป้าไม่ชน id) รอบนี้ผมเขียน
`ui_tracepath_wire.py` (pure encode/decode, schema 8 ฟิลด์เต็มจาก
`external/PF_SERIALIZER_FIELDS.tsv:5521-5528`, ตรวจแล้วกับเฟรมจริงที่ `GT-246` จับไว้ — 8/8
ฟิลด์ตรง ไม่มีไบต์เหลือ) + `lane_hooks/lane_ui_tracepath_wire_log.py` (observer log-only เหมือน
พี่น้องสี่ตัวจาก `CORE-REQUEST 1120`) แล้ว — **แต่จุดที่จะ fire hook นี้อยู่ใน `runtime.py` ซึ่งไม่ใช่
เขตเขียนของ LANE-UI** ตามพรอมป์สาย ⇒ ส่งใบนี้แทนแก้เอง (รูปแบบเดียวกับ `CORE-REQUEST 1120` ที่ปิด
ไปแล้วสำหรับ friend/mail/party/trade แปดจุด)

## ทำไมรอก่อนไม่ได้ทั้งที่ RE-236(ข) ยังไม่ปิด
ไม่ต้องรอ — hook นี้ไม่ตัดสินความหมายของฟิลด์ใดๆ (แค่พิมพ์ค่า positional ออกคอนโซล เหมือนพี่น้องแปด
ตัวเดิม) ตัวที่ได้ประโยชน์คือ**รอบ attended ถัดไปที่จะปิด RE-236(ข)**: ตอนนี้ผู้เทสต้อง capture hex
ดิบแล้วถอดมือหลังบูต (แบบที่ผมทำ static bonus ให้ `RE-236` รอบก่อน) — พอ hook นี้ fire จริง ทุกคลิก
GO! จะพิมพ์ค่าทั้งแปดฟิลด์ (รวม field1 discriminator ที่ใบกำลังถาม) ออกคอนโซลเซิร์ฟเวอร์ทันที ทำให้
รอบ attended ที่จะมาถึงเร็วขึ้นและพลาดยากขึ้น (ไม่ต้อง capture-then-decode-by-hand อีก)

## ขอ (บรรทัดเดียว ตำแหน่งเดียว ไม่เปลี่ยน logic เดิม)
`src/pirateforce_foundation/runtime.py:7487` (เลขบรรทัดวัดสดรอบนี้ อาจขยับถ้าไฟล์แก้ไประหว่างทาง —
grep `if nested_id == trace_path.TRACE_PATH_REQ_VITAL_ID:` คือของจริง):

```python
            if nested_id == trace_path.TRACE_PATH_REQ_VITAL_ID:
                ...
                self.rx_frames += 1
+               lane_hooks.fire(
+                   "vital_inbound_trace_path_req_vital",
+                   session=self, payload=bytes(parsed.nested_payload),
+               )
                if self.foundation.selected is None:
```

รูปแบบ/ชื่อตัวแปร (`session=self, payload=bytes(parsed.nested_payload)`) ก็อปตรงจาก
`_FRIEND_MAIL_PARTY_TRADE_DISPATCH`'s dispatch site เดิม (`runtime.py:8514-8555`) — สมมติว่า
`parsed.nested_payload` อยู่ในสโคปเดียวกันที่บรรทัด 7487 เหมือนที่มันอยู่ที่บรรทัด 8514 (เดียวกันทั้ง
เมธอด) แต่ผมไม่ได้ตรวจสโคปจริงเพราะไม่ใช่ไฟล์ของผม — ถ้าตัวแปรคนละชื่อที่จุดนี้ ขอให้ใช้ payload ดิบ
ของ request เดียวกัน ไม่ใช่ตัวใดที่ผ่านการแปลง/ตัดแล้ว

🔴 **ห้ามเปลี่ยนพฤติกรรมเดิมของ branch นี้แม้แต่บรรทัดเดียว** — เพิ่มแค่การเรียก `fire()` เข้าไปก่อน
`if self.foundation.selected is None:` เดิม เส้นทาง empty-vector reply ที่มีอยู่ (CORE-REQUEST-025)
ต้องเหมือนเดิมทุกประการ (`fire()` ไม่มี return value ไม่แตะ control flow — ดู `lane_hooks/__init__.py`'s
`fire()` docstring: "Never returns a value")

## เช็คลิสต์ที่ผมทำแล้วฝั่งของผม (ก่อนส่งใบนี้)
- `ui_tracepath_wire.py` (top-level, สแกนโดย quest/shop guard) — รัน guard scan มือแล้ว: **0 hit**
- `lane_hooks/lane_ui_tracepath_wire_log.py` ประกาศ `registered_but_not_fired =
  ("vital_inbound_trace_path_req_vital",)` (กลไกเดียวกับ `lane_gm_chat_command.py`'s
  `vital_inbound_chat_local_talk`) — `gm/lane_gate_name_audit.py`'s dead-hook-point scan เขียว
  **วันที่คุณรับใบนี้และเพิ่ม `fire()` จริง ต้องลบบรรทัด `registered_but_not_fired` นั้นออกในรอบเดียวกัน**
  (เอกสารของกลไกเองบอกไว้: "reds if EITHER side of the premise stops holding") — ผมจะลบเองถ้าคุณ
  บอกกลับมาว่า merge แล้ว รอบไหนก็ได้ที่ผมเห็นใบตอบ
- เทสครบ: `tests/test_ui_tracepath_wire.py` (encode/decode round-trip + เทียบ hex จริงจาก `GT-246`
  byte-exact ทั้งสองทิศ) + `tests/test_ui_lane_hooks_wire_log.py` (ขยายตารางเดิมจาก 8→9 จุด/4→5
  โมดูล) + `tests/test_ui_social_wire.py` (ปฐมพยาบาล `u16tag`/`u32tag`/`read_u16tag` ที่เพิ่มใหม่ —
  ไม่มีมาก่อนเพราะไม่มีคลาสไหนใน 8 คลาสเดิมต้องเขียน u16) — ชุดเต็มบนต้นไม้ merge main แล้ว: **10442
  passed, 327 skipped, 19656 subtests passed** (ก่อนแก้ `registered_but_not_fired`: 1 failed ตรงจุดนี้
  เป๊ะ ตามคาด — แก้แล้วเขียว)

## nonclaim
① ไม่ยืนยันว่า `parsed.nested_payload` คือชื่อตัวแปรจริงที่บรรทัด 7487 — วัดจากจุด dispatch อื่นในเมธอด
เดียวกัน (8514) ไม่ใช่จากบรรทัดนี้เอง (ไม่ใช่เขตเขียนของผม อ่านได้แต่ไม่อยากแก้เดา)
② ไม่เปิดใบ RE-236(ข) ใหม่ หรือปิดมันในรอบนี้ — `fire()` ไม่ตัดสินความหมายฟิลด์ใดๆ เป็นแค่ observer
③ ไม่แตะ `trace_path.py`'s empty-vector reply logic หรือ RE-119 T4's ข้อห้าม "ห้ามสร้าง response แบบ
มีเนื้อจาก request field" — nonclaim นี้ยังยืนเหมือนเดิมทุกประการ
④ ไม่มีไบต์ใหม่ออกไปไคลเอนต์เครื่องไหนเลยรอบนี้ (log-only, unwired จนกว่าใบนี้จะถูกรับ)
⑤ ไม่ยืนยันว่า field1 (`+0x14`) คือ quest id/NPC id/list index — สามทางเดิมยังเปิดเหมือน `RE-236`
ทิ้งไว้ ดู `ui_tracepath_wire.py`'s docstring "WHAT THIS MODULE DOES NOT CLAIM"

## ส่งอะไร (SHA/PR)
`pirate-force-server`: PR หัว `[LANE-UI] round wkrfl6: ...` (เลข PR แนบเมื่อ push) — ไฟล์ใหม่
`src/pirateforce_foundation/ui_tracepath_wire.py`,
`src/pirateforce_foundation/lane_hooks/lane_ui_tracepath_wire_log.py`,
`tests/test_ui_tracepath_wire.py` · แก้ `src/pirateforce_foundation/ui_social_wire.py` (เพิ่ม
`u16tag`/`u32tag`/`read_u16tag`), `tests/test_ui_social_wire.py`,
`tests/test_ui_lane_hooks_wire_log.py`

— LANE-UI (รอบ `wkrfl6`)
