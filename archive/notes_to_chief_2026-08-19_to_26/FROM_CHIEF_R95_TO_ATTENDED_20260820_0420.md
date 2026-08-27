# จาก chief รอบ 95 → เซสชันหลัก ATTENDED (2026-08-20 04:2x)

**HEAD ตอนนี้ = `72d6129`** (สอง commit คืนนี้: `dbcbf8f` = IMG-QUERY-001 runner ของรอบ 94 ที่ตายเงียบ · `72d6129` = DAMAGE-NPC-TARGET-001)
canonical DB ไม่ถูกแตะ (sha `6BFCEDD5..8FC7` ตรวจก่อน-หลังทุกจ็อบ) · ธงทั้งสองใบ RELEASED · inbox ว่าง · เลขจ็อบผู้เทส = **933** ต่อไป

## คิวรอบใหญ่ #9 — เรียงตามผลตอบแทน/ความเสี่ยง

1. **GT-001 smoke ที่ `72d6129`** (re-arm เพราะ commit แตะ src/ — ทุกจุดอยู่หลังธง opt-in ที่ boot ปกติไม่ใช้ · full suite 1530 passed แล้ว) — รันก่อนเพื่อยืนยันแท่นก่อนทดลองใหม่
2. **GT-027 DAMAGE-ON-NPC-001** ⭐ ของใหม่คืนนี้ — boot ท่า GT-024 เดิมเป๊ะ เปลี่ยนแค่ไฟล์:
   `--damage-model-hypothesis-scenario scenarios\damage_model_hypothesis_npc_sweep.json`
   - ทริกเกอร์แชต ascii 12 ตัวเดิม → 4 เฟรม **ห่างกัน 15 วิ** (ถ่ายทันทุกเฟรม)
   - console ต้องเห็น label `HYP_PF_024_DAMAGE_NPC_*` + event `damage_model_hypothesis_npc_sweep_sent` — ถ้าเห็นชื่อเดิมของ GT-024 แปลว่าบูตผิดไฟล์
   - คาด (ถ้า map มี `0x2001`): 63 → 379 → MISS → 63+reaction **บนหัว NPC ตัวแรก Port Royal** · ยืนให้เห็นทั้งผู้เล่นและ NPC ในเฟรมเดียวก่อนยิง
   - 🔴 **ไม่มีเลขเลย = ผลลบที่มีค่า** (0x2001 ไม่อยู่ใน map ตอนรัน) — ถ่ายหลักฐาน "ไม่มีอะไรเกิด" ด้วย · เลขขึ้นบน**ผู้เล่น**แทน = หักล้าง static รอบ 93 จดละเอียด
3. **GT-028** — รันคู่กับ GT-027 ในบูตเดียว (จังหวะ 15 วิพอถ่าย 63/MISS/เทียบ reaction) · ถ้า GT-027 ลบ รายการนี้กลับ BLOCKED อัตโนมัติ
4. **GT-029 วงนับถอยหลัง** — ใช้ท่า GT-025 (`dying_latch_only`) ที่มีอยู่แล้ว latch ค้างถาวร · ถ่ายวงทีละ ~1 วิ ≥10 วิ · เลขลด=client นับเอง (รื้อเลน) · เลขค้าง=ยืนยันข้อสรุปเดิม — มีความหมายทั้งสองทาง
5. **GT-026 EXIT-PATHS-001** — ยัง PENDING เหมือนเดิม ไม่ต้องรอ commit ใด

## ของที่ควรรู้

- **`image_queries\` ใช้งานได้จริงแล้ว** — ฝั่ง local รัน `py -3 tools\pf_image_query_runner.py --image <GameClient.local.bin> --pending pf_bridge\image_queries\pending --answered pf_bridge\image_queries\answered` (kinds: bytes/hash/search · sha-pin · เพดาน 4KB/64KB · refusal มีชื่อ) — ถ้า chief ฝั่งไหนหย่อนคำถามไว้ รันทีเดียวตอบหมด
- **งบ version ของ HYP-PF-024 เต็มแล้ว (3/3)** — ใครอยากได้ profile damage เพิ่ม ต้องให้ chief เปิด entry ใหม่/ขอ approval อย่าแก้ของเดิม
- รายละเอียดเต็มทุกรายการอยู่ใน `GAME_TEST_QUEUE.md` (อัปเดตคืนนี้แล้ว) · บล็อกรอบ 95 ใน `CHIEF_CONTINUATION.md`
