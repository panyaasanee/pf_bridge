# [CONSUMED โดย chief รอบ 100 — 2026-08-20 10:1x]

ฉบับเต็ม: `notes_to_chief\consumed\20260820_0945_PANYA-RULE-never-drop-untested-queue.md` (ไม่ได้ลบ)

**บริโภคไปทำอะไร:** บันทึกกฎแม่บ้านถาวรลง CHIEF_CONTINUATION.md (บล็อกรอบ 100):
ห้ามย้าย/ลบรายการ GAME_TEST_QUEUE ที่ยังเป็น PENDING/READY/BLOCKED/RUNNING ไม่ว่าค้างนานแค่ไหน ·
archive ได้เฉพาะ PASS/FAIL/DONE/supersede-โดยชื่อชัดเจน · เพดาน ~60KB ไม่ใช่เหตุผลย้ายคิวที่ยังไม่เทส
→ ถ้าเกินให้ปล่อยเกินแล้วรายงานว่าเกินเพราะรายการไหน · คิวยาว → จัดกลุ่ม/ทำสารบัญ ไม่ใช่เอาออก
chief รอบ 99 เข้าใจถูกอยู่แล้ว กฎนี้แค่ทำให้เป็นลายลักษณ์สำหรับ chief รอบถัดไปที่เริ่มจากศูนย์ ·
ผู้เทสแก้ต้นฉบับ agent_kit\chief_task_prompt.md แล้ว แต่ sync เข้า scheduled task ฝั่ง local ไม่ได้
→ Panya ต้องอัปเดต prompt ของ task บนเครื่องเองถ้าอยากให้มีผลข้ามรอบ · nonclaim: chief รอบ 100
ไม่เคยย้าย PENDING ออก ไม่มีอะไรต้องย้ายกลับ
