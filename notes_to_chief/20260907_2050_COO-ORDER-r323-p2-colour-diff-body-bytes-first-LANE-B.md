[จาก: COO รอบ `2050` | 2026-09-07T20:50+07:00 | ที่มา: `20260907_2027_KA1A-R323-RESULTS-GT288-colour-not-actor-type-GT299-blocked-empty-skill-list.md` (OBSERVER_CONFIRMED Panya 19:46)]
ADDRESSEE: LANE-B
cc: LANE-K · ka1-A · chief (LANE-E) · Panya

# `GT-288` ชุด 2 วัดแล้ว: **สีชื่อไม่ขึ้นกับ actor_type/สกิน** — งานแรกรอบหน้า = diff body N-BASE vs M-BASE แล้วสวีปทีละฟิลด์ (P-2 = M3 มาก่อน M4)

## ผลที่เจ้าของเห็นเอง (ตาราง ka1-A)
หุ่น 6 ตัววาดครบ · N-* เขียวทั้ง 3 (รวม actor_type 5 + สกิน) · M-* ชมพูทั้ง 2 ที่มีป้าย · M-SKIN ไม่มีป้าย · `NAME_COLOUR_SWEEP_ARMED actors=6 census_actors=108 wire=114` ตรง `HEADLESS_PROOF` ของคุณทุกตัว
⇒ ตัวตัดสินสี = **ฟิลด์ body ที่ต่างกันระหว่างต้นแบบ NPC (n_ID 1) กับต้นแบบมอน (916)** · `actor_type 5` ตัดออก (และทำ NPC เปลือย/มอน T-pose ⇒ ไม่ใช่ทาง production)

## สั่ง (AUTO-DECIDED — เรียงคิวในสาย: M3 ก่อน M4)
1. **งานแรกรอบหน้า**: diff ไบต์ body ของ N-BASE กับ M-BASE ในเฟรม `WORLD_CENSUS_INITIAL_108_SWEEP_6` (21516 B · `capture_r323a_20260907_193650/` บนเครื่องสะพาน · ถ้าโคลนคลาวด์ไม่มี capture = สร้างเฟรมเดียวกันจาก headless บน main แล้ว diff) → รายการฟิลด์ที่ต่าง พร้อม offset ใน `NPCAttr` (`+0x98` = ผู้สมัครเดิม)
2. ออกแบบ **ชุด 3 ใหม่** = สวีป**ทีละฟิลด์** จากรายการนั้น · **ชุด 1 (faction 7/12/999) ก่อน** · ส่ง `*-TO-K-gt-body-*` + `HEADLESS_PROOF:` (บน main ปัจจุบัน ≤3 วัน + **precondition บนจอ**ตามกฎใหม่) รอบเดียวกัน · ชุด 3 เดิม**ยังห้ามบูต**จนใบใหม่แทน
3. หลังจากนั้นค่อย `name_tokens` → `GT-300` ตามลำดับเดิม · `bg0002` ยังห้ามพลิก

## โทเคนตรวจ
ไฟล์รอบ B มีบรรทัด `P2_BODY_DIFF: fields=<n> first=<ชื่อ/offset>` + จดหมาย `*LANE-B-TO-K-gt-body-*` ของชุด 3 ใหม่ ภายใน 1 รอบของ B

## ถ้าผิดย้อนอะไร
ลำดับคิวอย่างเดียว (เจ้าของสลับกลับได้บรรทัดเดียวใน NOW)

-- COO รอบ `2050`
