[ถึง: LANE-B | ADDRESSEE: LANE-B | cc: COO | จาก: chief รอบ `f7zt8z` (R295) · 2026-09-01T23:23+07:00]
[ตอบใบ: `notes_to_chief/CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md`]

# CHIEF-TO-LANE-B — มอบสองข้อจาก CODEX_URGENT P05 ให้สาย B ทำ (bounded, มี regression)

ใบ P05 ของ Codex (read-only, ยืนยัน self-contradiction จริงในโค้ดปัจจุบัน ไม่ใช่แค่ทฤษฎีต้นฉบับ)
รายงานสามข้อ ตัดสินตามที่ Codex เสนอ:

## มอบให้สาย B ทำรอบหน้า (bounded, มี regression ตามที่ Codex ระบุ)

1. **ศพเก่าถูก re-arm ทุกครั้งที่มีศพใหม่** — `runtime.py:4743-4760` compose ทั้ง register ด้วย
   timer เดียว (`20.0` แล้ว `0.0`) แทนที่จะเป็น per-identity/per-record ทำ timer เป็น per-identity:
   `>0` เฉพาะ identity ที่เพิ่งตาย ศพเดิมคง `<=0` เพิ่ม regression อย่างน้อย: A ตาย → B ตาย → census
   ของ A ต้องไม่กลับเป็น positive timer อีก
2. **Drop ข้ามฉากได้จาก ledger เดียวกัน** — `DropLedger` (`mob_loot.py:1362-1393`) ไม่มี scene term,
   scene sync ไม่ reset/reconcile loot (`runtime.py:4111-4191`), ทุก kill ส่ง live ledger ทั้งก้อน
   (`runtime.py:4912-4925`, `mob_drop_presence.py:342-443`) ผูก ownership กับ scene/generation หรือ
   reconcile ตอน scene transition ก่อน publish เพิ่ม regression: scene A มี drop → เปลี่ยน B → kill
   B → publication ของ B ต้องไม่มี key/position จาก A

**ทำไมสาย B**: ทั้งสองจุดอยู่ในโมดูล mob-combat/loot ที่สาย B เป็นเจ้าของอยู่แล้ว (BUILD-004/5/6)
ตามกฎ v6.4 ข้อ "ถ้ายังไม่รู้ว่าใครควรทำ ให้เลือกสายแล้วเขียนชื่อลงในใบ" — ไม่เขียน "X หรือ Y"

**ทำไม chief ไม่ทำเอง รอบนี้**: `runtime.py`/`mob_death.py`/`mob_loot.py`/`mob_scene_recompose.py`/
`mob_drop_presence.py` แตะข้ามหลายไฟล์ + ต้อง regression ใหม่ที่ต้องเข้าใจ mob-death state machine
ลึก ให้เจ้าของโมดูลทำเองใต้ pf-adversary review ตรงตามหลักการ "เหมือนจริงใช้จริง ทำครั้งเดียวจบ" —
รอบนี้ chief ใช้งบไปกับ CORE-REQUEST 2007/1838 (UI-B logout + RE-157 job2) แล้ว

## ไม่มอบตอนนี้ (ตามที่ Codex เองเตือน)

3. **Pickup/removal ยังไม่ต่อเข้าระบบจริง** — original policy ยัง OPEN ตาม Codex เอง ห้ามแก้ด้วย
   resend หรือ guessed count-zero clear แยกเป็นเรื่องของตัวเองต่างหาก ไม่รวมกับสองข้อบน

## ทำไมแจ้ง COO ด้วย (cc)

ข้อ 2 (drop ข้ามฉาก) เกี่ยวข้องตรงกับ **P-1 "ของดรอปต้องค้างอยู่บนพื้น"** ใน `NOW.md` — chief แก้
`NOW.md` เองไม่ได้ (ผู้เขียนคือ Panya/COO เท่านั้น) เสนอให้ COO พิจารณาว่าจะขยับสถานะ P-1 หรือรอผลจาก
สาย B ก่อน

-- chief
