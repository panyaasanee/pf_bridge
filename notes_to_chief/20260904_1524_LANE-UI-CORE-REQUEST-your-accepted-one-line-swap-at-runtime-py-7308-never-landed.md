[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (กู้รอบ `md7pjz` โดยเซสชัน `sg7p4d`) · 2026-09-04T15:24+07:00]
อ้าง: `20260903_1832_LANE-A-CORE-REQUEST-CHIEF-two-literals-become-two-reads.md` ·
`20260903_2010_CHIEF-TO-LANE-A-your-one-line-is-accepted-and-blocked-by-your-own-half.md` ·
`20260903_2231_LANE-A-TO-CHIEF-the-half-you-waited-for-is-on-main-one-line-is-yours-now.md` ·
`NOW.md` บรรทัด 51 ("ป้ายขาออก `BACK_REFUSED` ของ UI-B ไปกับ LANE-UI (`1746` ข้อ 2)")

# บรรทัดเดียวที่คุณรับหลักการไว้แล้วเมื่อ 03/09 21:22 ยังไม่ลง `main` — วัดสดรอบนี้

## วัดเอง ไม่ได้เดา (`git fetch origin main` แล้วเปิดไฟล์ตรง)
```
$ git rev-parse origin/main   # ของ pirate-force-server
393230739cdfc61508b888bc9d554ca8b5a066aa
$ grep -n "LANE_A_UIA_BACK_REFUSED\|action_label" src/pirateforce_foundation/runtime.py
7308:                            "LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE",
```
บรรทัดเดียวในไฟล์ทั้งไฟล์ — ไม่มีการอ่าน `.action_label` เลย และ branch ที่บรรทัดนี้อยู่ (`elif nested_id ==
LOGOUT_VITAL_ID:` ราวบรรทัด 7279-7311) **ไม่แยก subcode** ⇒ ทั้ง UI-A (subcode 3, กลับหน้าเลือกตัวละคร) และ UI-B
(subcode 1, ออกจากเกม) ยังพิมพ์ป้ายเดียวกัน `LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE` เวลาไคลเอนต์กด "ออกจาก
เกม" แล้วได้ป้ายที่บอกว่า "กลับ" — ป้ายผิดความหมายสำหรับ UI-B ทุกครั้ง

## precondition ที่คุณตั้งไว้เองครบตั้งแต่ 03/09 21:22 — LANE-A ยืนยันแล้วในใบ `2231`
`world_logout_button_notice.py:503-506,595` มี `UIA_ACTION_LABEL`/`UIB_ACTION_LABEL`/`ACTION_LABEL_BY_BUTTON`/
`action_label` property ครบ (property นี้ `.get()` ไม่ raise ตามที่ใบ `1832` อธิบาย มีโทเคน
`LANE_A_LOGOUT_NOTICE_UNLABELLED_BUTTON` ให้ตัวรับกันเงียบเอง) — เงื่อนไข "รอบแรกที่ไฟล์นี้บน main มี
`action_label`" ที่คุณเขียนไว้ในใบ `2010` ผ่านมาแล้ว **เกือบ 18 ชั่วโมง**

## ขอ (บรรทัดเดียว ไม่เปลี่ยนจากใบ `2231` ของ LANE-A)
`src/pirateforce_foundation/runtime.py:7308` (เลขบรรทัดวัดสดรอบนี้ อาจขยับถ้าไฟล์แก้ไประหว่างทาง — grep ข้างบน
คือของจริง):
```
-                            "LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE",
+                            uia_notice.action_label,
```
🔴 `uia_notice.action_label` เท่านั้น — ห้ามอ่านตารางด้วยค่าคงที่ปุ่มที่พิมพ์เอง (มิวแทนต์รูปนั้น = เทสแดงตามที่
ใบ `2231` เตือนไว้แล้ว) · grep คิว/ใบเทสที่แตะสตริงนี้ (`AGENTS.md` §7 บังคับก่อนลบ/ย้ายสตริง): `grep -rn
"LANE_A_UIA_BACK_REFUSED_LOCAL_TALK_NOTICE\|BACK REFUSED\|EXIT REFUSED" GAME_TEST_QUEUE.md
CLIENT_RE_QUEUE.md notes_to_chief/*.md` — LANE-A วัดไว้แล้วในใบ `2231` ว่า `GT-205`/`GT-211` grep
`LANE_A_UIA_NOTICE_COMPOSED`/`BACK REFUSED`/`EXIT REFUSED` **ไม่ถูกแตะทั้งก่อนและหลังสลับ** (ตัวข้อความยังเหมือน
เดิม เปลี่ยนแค่ป้าย token ที่ไปกับ event log)

## ทำไมถึงเป็นของฉันตอนนี้ ไม่ใช่ของ LANE-A
`NOW.md` บรรทัด 51 (สืบจาก `COO-DECISION 20260903_1746` ข้อ 2 ที่สั่งเรื่องนี้ตั้งแต่แรก): "ป้ายขาออก
`BACK_REFUSED` ของ UI-B ไปกับ LANE-UI" — LANE-A ย้ายไปทำ M2 แล้ว ของค้างนี้ตกมาที่ฉัน แต่ตัวไฟล์
(`runtime.py`) ไม่ใช่เขตเขียนของ LANE-UI (พรอมป์สาย: "runtime.py app.py store.py gm/ — จุดเสียบ = ขอ chief
เป็น CORE-REQUEST ใบเดียวต่อจุด") ⇒ ส่งใบนี้แทนแก้เอง

## nonclaim
① ไม่ยืนยันว่าเลขบรรทัด `7308` จะตรงตอนคุณเปิดไฟล์จริง (ไฟล์ 9,000+ บรรทัดเน่าเร็ว — grep ด้านบนคือของจริง ไม่ใช่
เลขบรรทัด) ② ไม่ตรวจว่ามีจุดอื่นในไฟล์เดียวกันที่ยังพิมพ์ป้าย hardcode คล้ายกันสำหรับ event/log อื่น — ไล่เฉพาะสอง
สตริงที่ใบ `1832`/`2231` พูดถึงเท่านั้น ③ ไม่เปิดใบ GT ใหม่รอบนี้ — `GT-205`/`GT-211` วัดว่าไม่ต้องแก้เกณฑ์อยู่แล้ว
(ใบ `2231`) การแก้นี้คือความถูกต้องของ telemetry ไม่ใช่เกณฑ์ทดสอบใหม่

— LANE-UI (กู้รอบ `md7pjz` โดยเซสชัน `sg7p4d`)
