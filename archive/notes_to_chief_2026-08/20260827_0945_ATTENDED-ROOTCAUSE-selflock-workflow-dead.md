# ATTENDED-ROOTCAUSE 2026-08-27 09:45 +07:00 — self-lock ซ้ำ ๆ ของทุกสาย: ต้นตอ 5 ข้อ แก้แล้ว 5 ข้อ

ถึง chief (สาย E) และ COO — จาก attended session ตามคำสั่งเจ้าของ 09:0x "หาสาเหตุที่ติด self-lock ซ้ำ ๆ ของสาย A และแก้ไขมัน แก้ปัญหา chief ด้วย และหาสาเหตุของปัญหาโดยรวมอื่น ๆ แล้วแก้โดยคิดว่าจะเกิดแบบนั้นอีก"

## ผลก่อน (สถานะ 09:38)
- pirate-force-server main = b9273b55 (#101 GM, #102 A, #103 B ถูก merge ครบใน 09:35-09:37 โดย job `finish` ตัวใหม่)
- open PR เหลือเฉพาะ #104 / pf_bridge #179 = draft ของรอบ chief 3t3klq ที่กำลังทำอยู่ ถูกต้อง
- gate บน main ถูก dispatch ให้ทุก merge commit (0b30b24a, 463ad967, 41e6b3e8, b9273b55) กำลังรัน
- workflow ทั้งสอง repo มีชีวิตแล้ว วัดจาก run 33033763252 (workflow_dispatch: finish success, reap success) และ pf_bridge run 33033641037

## ต้นตอที่วัดแล้ว
1. **workflow ฝั่งเซิร์ฟเวอร์ตายทั้งใบ 08:11–09:35** — R189 (a811d99) เพิ่ม `actions: write` ใต้ `actions: read` ที่ยังอยู่ ใน permissions ของ decide และ reap = mapping key ซ้ำ `yaml.safe_load` รับ (ตัวหลังทับ) แต่ GitHub ปฏิเสธไฟล์ทั้งใบ หลักฐาน: ตั้งแต่ #100 merge (01:11Z) push ทุกครั้งทุก branch ได้ run ชื่อ path `.github/workflows/merge-claude-pr.yml` event=push failure 0 job (8 ใบติด 01:18Z–02:26Z) และไม่มี run event workflow_run/schedule เลยหลัง 01:11Z → decide/reap ไม่วิ่ง → #101 #102 #103 ค้างพร้อมกัน นี่คือเมล "แดงอีกแล้ว" ที่เจ้าของเห็น
   - แก้: PR #105 commit 019d169b ลบ key ซ้ำ (`actions: write` รวม read อยู่แล้ว เขียนครั้งเดียว) + คอมเมนต์เล่าเหตุการณ์ในไฟล์
   - เพราะ workflow บน main ตาย จึงไม่มีอะไร merge #105 ได้เอง attended รอ gate เขียวทั้ง 2 run (push+pull_request, job gate=success) แล้ว merge ผ่าน API จากเครื่องเจ้าของ 09:35:45 (merge commit 0b30b24a, sha-pinned) แล้ว dispatch gate-windows + merge-claude-pr บน main
2. **PR ที่เอา draft ออกหลัง gate จบ ไม่มีอะไรปลุก decide** (#57 #61 #86 #91 เมื่อวาน) — decide ฟังแค่ workflow_run
   - แก้ (ใน #105 เดียวกัน): job `finish` วิ่ง schedule ทุก 10 นาที + workflow_dispatch: merge PR ที่ ไม่ใช่ draft + 6 เกตเดิม + มี marker + gate job success บน head ปัจจุบัน + ไม่มี gate run ค้าง + mergeable=true ไม่ปิดอะไรเลย ไม่แตะ draft reaper 6 ชม. คงเดิม concurrency group เดียวกันสำหรับ scheduled
3. **pf_bridge: ready_for_review ไม่อยู่ใน types ของ pull_request_target** — ต้นตอ self-lock สาย A #144 (และทุกสายที่เปิด draft แล้วเอา draft ออกโดยไม่แก้หัวข้อ) reaper เดิมรอ 6 ชม. แล้ว "ปิดทิ้ง" = งานหาย
   - แก้: pf_bridge PR #180 (merge แล้ว 09:33 โดย workflow เดิมเอง) types += ready_for_review; schedule */10; reap: PR พร้อม+marker+mergeable → merge ทันที / mergeable=false → ปิดทันที (conflict ไม่หายเอง รอมีแต่ล็อก) / draft เกิน PF_STALE_HOURS=2 → ปิด (รอบตาย) branch เก็บทุกกรณี
4. **marker หายตอนเขียน body รอบจริง** (#86) — PATCH body = เขียนทับทั้งก้อน
   - แก้: กฎใน prompt v6.2 §3 ข้อ 3 (GET กลับมายืนยัน marker หลัง PATCH) + addendum ข้อ B ให้ทุกสาย
5. **"push แล้ว" ถูกจดเป็น "เสร็จ"** (R186 #84 ปิดแดง แต่ CHIEF_CONTINUATION บอกว่า landed 9 ชม.) และ **tool GitHub ตายกลางรอบแล้วรอบจบเงียบ** (สาย GM #72/#131 ค้าง draft 8 รอบ)
   - แก้: v6.2 §2 ข้อ 7 ตรวจชะตา PR รอบก่อนของตัวเองทันทีหลังถือล็อก (closed+unmerged = กู้จาก branch ก่อน) + §3 บันทึกท้ายรอบต้องเขียน "push แล้ว รอ merge" + §3 กฎ tool ตาย (push ก่อน ลอง curl บอกในจดหมาย) + addendum A/C/D ให้ทุกสาย

## กฎใหม่ที่ chief ต้องถือ (อยู่ใน PROMPT_PF_Chief_v6.2.txt ที่ staged/ เจ้าของจะวางให้)
- §7 แตะ .github/workflows/*.yml ต้องผ่านตัวตรวจ key ซ้ำ (สคริปต์อยู่ใน prompt) + bash -n ทุกก้อน run: + หลัง push ดู runs?head_sha ว่าไม่มี run ชื่อ path 0 job + รอบถัดไปหลัง merge ต้องเห็น run จริงของ workflow นั้น
- §8 ข้อ 5 merge commit บน main ต้องมี ci/<sha>.json โผล่ภายในรอบถัดไป (post-merge dispatch ทำงานแล้ว) ไม่โผล่ = รายงาน
- §17 ข้อ 3 นับ CORE-REQUEST-GM-* ด้วย และ WIRED ตามนิยาม v2 ของ COO
- §18 ข้อ 0 รอบแรกที่อ่าน v6.2 ต้องยืนยันว่า workflow ทั้งสอง repo มีชีวิต (เกณฑ์เขียนไว้แล้ว)
- §18 ข้อ 6 ถอนคำอ้าง "GT-001 ปลด HOLD ได้แล้ว รันผ่านจริงแล้ว" ของ v6/v6.1 — ไม่มีหลักฐาน ต้องมี OBSERVER_CONFIRMED ก่อน

## ขอ COO
- เคาะ PF_STALE_HOURS=2 สำหรับ draft ฝั่ง pf_bridge (รอบ chief/lane ยาวเกิน 2 ชม. = ถือว่าตาย) ถ้าไม่เห็นด้วยให้บอกเลขที่ต้องการ attended จะแก้ให้
- ส่ง addendum (staged/ADDENDUM_LANES_v6.2_20260827.txt) ให้สาย A B GM ผ่านช่องทางที่ COO ใช้อยู่ หรือให้ chief แนบใน CORE-REQUEST รอบถัดไป (v6.2 §18 ข้อ 5)

## สิ่งที่ยังไม่ได้พิสูจน์
- job `finish` บน schedule จริง (ไม่ใช่ dispatch) ยังไม่มีตัวอย่าง รอ tick ถัดไป (ทุก 10 นาที) attended จะตรวจ
- curl+git credential fill บน Routine ยังไม่ได้วัด (ติดป้าย [เสนอ] ในทั้งสองไฟล์)
- ci/<merge-sha>.json ของ 4 merge commit เช้านี้ ยังรันอยู่ตอนเขียน

ตอนนี้ต้องทำอะไรต่อ: chief รอบถัดไป (:51) อ่าน v6.2 §18 ข้อ 0 แล้วยืนยันว่า workflow มีชีวิต และตรวจว่า #104/#179 ของรอบ 3t3klq จบตามลำดับ §3 (marker อยู่ใน body ใหม่)
