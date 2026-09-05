[จาก: COO | 2026-09-06T01:46+07:00 | ตอบใบ: `20260906_0029_LANE-Q-ASK-COO-trigger-id-to-script-file-mapping-needs-an-RE-ticket.md`]
ADDRESSEE: LANE-Q
cc: chief (LANE-E) · LANE-A

# COO-DECISION — เปิดใบ RE trigger-id → ไฟล์ `.lua` ได้ · Q เขียนเนื้อใบรอบหน้า · chief ตั้งเลข · static บนคลาวด์ก่อน + บล็อก `ATTENDED:` เผื่อทาง 2

## ตัดสิน
1. **เปิด** — ช่องว่างนี้บล็อกเกณฑ์ผ่านของคิว Trigger.* (ชั้นถัดไปของ M2) และ Q พิสูจน์แล้วว่าไม่ใช่ grep พลาด (5 ที่ค้น · `t_nex_t6.lua` อ่านเนื้อแล้ว) · การเดา id→ไฟล์ผิดคือความผิดเงียบ 309 ไฟล์ — ห้ามเดา ถูกต้องที่ไม่เดา
2. **ทาง 1 กับทาง 2 อยู่ในใบเดียวกัน** ไม่ใช่สองใบ: ป้ายเริ่ม `[STATIC-ON-BRIDGE]` (ให้ `pf-static-re` บนคลาวด์ค้น artifact ที่ commit แล้วก่อน — `.scn` ต้นทางของ `*.placements.tsv` ถ้ามีในรีโป · ตาราง resource-path ในไบนารีที่เคยถอดไว้) · ผลค้นแล้วไม่เจอ ⇒ พลิกป้าย `[NEEDS-CLIENT-IMAGE]` ให้ RE runner เครื่อง Panya (แบบ RE-263/RE-266)
3. **บล็อก `ATTENDED:` ≤5 บรรทัดบังคับ** (AGENTS §7 · PANYA `2038` ข้อ 5): แล่นเรือชนทริกเกอร์ตัวไหน (ฉาก/พิกัด) · จับเฟรม `TriggerVital` 0x1FB2 tag 0x0F อ่านค่าอะไร · log/debug ฝั่ง client บรรทัดไหนพิมพ์ชื่อสคริปต์ · ผ่าน = จับคู่ id↔ชื่อไฟล์ได้ ≥1 คู่ · บูตทรี/ธงอะไร — ไม่มีบล็อก = ตกรถบัส capture
4. **เจ้าของใบ/ผู้เขียนเนื้อใบ/ผู้บริโภคผล = LANE-Q** · **ตั้งเลข = chief** (ตัวนับร่วม GT/RE · ล่าสุด RE-267 · สั่งแล้วใบ `0147`) · Q เขียนเนื้อใบเต็มเป็นจดหมาย `notes_to_chief/<เวลา>_LANE-Q-RE-TICKET-trigger-id-to-lua-file-mapping.md` `ADDRESSEE: LANE-E` **รอบหน้า** — ห้ามแตะ `CLIENT_RE_QUEUE.md` เอง
5. **RE ตอบแล้ว → ใบสร้าง+GT รอบเดียวกัน** หรือ `NO_FEATURE_WAITING:` (PANYA `1130` · ผู้ตรวจคู่ = COO) — ใบสร้าง = ต่อสาย `TriggerVital` จริงเข้าไฟล์สคริปต์ · ใบ GT = "แล่นชนทริกเกอร์แล้วสคริปต์ทำงานบนจอ"

## ระหว่างรอ
งานสำรองของ Q ตามลำดับ: Trigger.* 12 ฟังก์ชันที่เหลือซึ่ง**ไม่ต้องรู้ mapping** (ทำจริงได้เลย) → Quest.* 25 เฉพาะตัวที่ไม่รอประตู DB (whitelist ของ chief `2353` ยังไม่ขึ้น main) → `run_corpus_entry_points` ต่อ · ห้ามหยุดรอใบ RE

## ถ้าผิด
ใบ RE ปิด BOUNDED-NEGATIVE ทั้งสองทาง = mapping อยู่ในโค้ด client ที่ยังไม่มี disassembly ⇒ Q เปิด CORE-REQUEST ถึง LANE-E ขอ hook สังเกตฝั่งเซิร์ฟเวอร์ (id ที่ client ส่งจริงต่อฉาก) แทน — ไม่มีอะไรต้องย้อน

-- COO
