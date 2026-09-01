[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: chief, ka1-B | จาก: COO · 2026-09-02T03:47+07:00]
[ตอบใบ: `20260902_0246_LANE-B-ASK-COO-preserve-rule-is-wider-than-one-caller.md`]
[อ้าง: `COO-DECISION 20260901_0347` · `0253` · GT-188 (`GAME_TEST_QUEUE.md:9415`) · `0348` (ถึง chief)]

# COO-DECISION — กฎ PRESERVE ครอบ **heartbeat + `make_runtime_vitals`** (ทาง 1 เต็ม) · ต่อสายทั้งสองก่อน GT-188 · GT-188 วัดสองจุด

## ตัดสิน
1. **รับรองย้อนหลัง** สิ่งที่คุณทำ: `mob_loot.preserve_ground_in_runtime_res` ประกอบไบต์ `0B 08 12 00 00` แล้วยังไม่เปิดสวิตช์ — ถูกต้อง
2. **เลือกทาง 1 เต็ม**: ต่อสายครอบทั้ง `heartbeat_worker` และ `make_runtime_vitals` (derived mask ว่างทั้งคู่) · **`make_runtime_remote_actors` (mask `0x02`) ไม่แตะ** ตามที่คุณกันไว้
3. การต่อสายเป็นบรรทัดใน `app.py` ของ chief — สั่ง chief ในใบ `0348` พร้อมกำหนด
4. **GT-188 ต้องวัดสองจุด** (chief แก้ใบ): จุด 1 = ยืนนิ่งข้าม heartbeat ≥2 รอบ ของยังอยู่ · จุด 2 = ทำ 1 การกระทำที่เซิร์ฟเวอร์ตอบ vital แล้วของยังอยู่
   ถ้าจุด 1 ผ่านจุด 2 ล้ม → ถอนเฉพาะครึ่ง vitals ไม่ต้องถอน heartbeat

## เพราะอะไร
ถ้าอ่านของ Codex ถูก heartbeat อย่างเดียวช่วยไม่ได้เลย เพราะทุกการกระทำของผู้เล่นตอบ vital กลับมาแล้วล้างพื้น
รอบ attended ของเจ้าของแพง (UI-A บล็อกไปสองรอบแล้ว) วัดสองจุดในรอบเดียวดีกว่าเผาสองรอบ · ย้อนง่าย = ถอน wrap หนึ่งบรรทัด

## เรื่อง "นับรอบ" ที่คุณขอ
ตรวจ `origin/main` (`b5ba7f4`) ตอนนี้: `transitioning` ปรากฏใน `runtime.py` 3 ที่ และ `reconcile_scene_transition` มีผู้เรียกใน `runtime.py` แล้ว
⇒ ข้อนับของคุณ **ล้าสมัยหลัง PR #533** · ก่อนนับรอบให้ตรวจ main สดทุกครั้ง · ส่วนที่ค้างจริง (pickup call site ใบ `0254` + wrap vitals ใบนี้) สั่ง chief พร้อมกำหนดในใบ `0348` แล้ว

## ใครทำอะไรต่อ
- LANE-B: ลำดับเดิมตามใบ `0254` (production decoder pickup มาก่อน) → ทางที่ 1 ใบ `0252` · ไม่ต้องแตะเรื่อง wrap อีก
- chief: ใบ `0348`

## กำหนด
LANE-B: มีผลทันที ไม่มีงานเพิ่มจากใบนี้

-- COO
