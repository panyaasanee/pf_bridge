# R228 (session `1k0tfu`) — CORE-REQUEST-GM-036 ต่อสาย + pf-adversary ได้ worktree ของตัวเอง

เวลา: 2026-08-29T15:16+07:00 (ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 14:42 ต่างไม่เกิน 60 นาที)

## งานหลัก 1 — CORE-REQUEST-GM-036 (หัวข้อ 17 ข้อ 3: CORE-REQUEST ก่อนงานอื่น)

ต่อ `scene_registry=scene_entry_registry` สามจุดใน `runtime.py` (เขต chief):
consume ตอน login · chat factory (`make_gm_chat_command_action`) · restore ใน `_put_back_consumed_override`
อ้าง closure local ตรง ๆ ตามข้อ D6 ของใบ (ไม่ใช้ getattr — สายหลุดต้องดัง ไม่ใช่ถอยไปอ่านไฟล์เงียบ ๆ)

สิ่งที่วัดเจอระหว่างต่อ (รายละเอียด + คำตอบ nonclaim ข้อ 0 ของสาย GM →
`notes_to_chief/20260829_1516_CHIEF-REPLY-LANE-GM-036-wired-plus-two-findings.md`):

1. เทสพิสูจน์ wiring ของสาย GM เขียวบนต้นไม้ที่ยังไม่ต่อสาย (มันเรียก factory เองพร้อม kwarg)
   ⇒ เขียนเทสฝั่ง chief ใหม่ `tests/test_gm_login_scene_registry_wiring_in_runtime.py` 3 ใบ ขับ dispatcher จริง
   [วัดแล้ว] แดง 3/3 บน origin/main ที่ยังไม่ต่อ · เขียว 3/3 เมื่อต่อ = mutation kill รายจุดเรียก
2. ทิศ "snapshot แคบกว่าดิสก์": consume ตัดสินด้วย snapshot ⇒ ใบที่ snapshot ไม่ยอมทำให้ทั้งแฟ้ม
   `CONSUME_FAILED` และ branch นั้นใน runtime **เงียบ** = อาการ GM-034 กลับมาทางประตูใหม่
   ⇒ เพิ่ม guarded print `GM_LOGIN_SCENE_OVERRIDE_CONSUME_FAILED judged_by=boot_snapshot ...`
   และเขียนเทส R225 สองใบใหม่ให้พินกลไกใหม่ (ใบไม่ถูกหยิบออกจากแฟ้มเลย · login จบที่แถวตัวเอง
   · ไม่มี lockout · คอนโซลบอกชื่อ) — invariant เดิมครบ กลไกเปลี่ยนตามดีไซน์ของ GM-036 เอง
3. พินรูปเรียกใน `test_gm_standalone_map_is_not_chat_writable.py` อัปเดตตามรูปเรียกใหม่
   (ยังพินว่า "ไม่ส่ง config path" — เจตนาเดิมของด่านไม่เปลี่ยน)

ไฟล์ที่แตะ (pirate-force-server, 4 ไฟล์): `src/pirateforce_foundation/runtime.py` ·
`tests/test_gm_login_scene_registry_wiring_in_runtime.py` (ใหม่) ·
`tests/test_gm_login_scene_override_registry_authority.py` · `tests/test_gm_standalone_map_is_not_chat_writable.py`

หลักฐาน: สวีตเต็ม 4,713 passed 0 failed เขียว(cloud sanity) · `HYPOTHESIS_LEDGER` PASS 47 ·
ไฟล์ที่แตะ ASCII สะอาดทั้งหมด (ด่าน encode ไม่ใช่รันแล้วดู) · pf-adversary รีวิวก่อน un-draft

## งานหลัก 2 — COO-DECISION 1444 ข้อ 2 (กำหนด ~16:51 วันนี้ — เสร็จในรอบ)

- `.claude/agents/pf-adversary.md` ทั้งสอง repo: เพิ่มหมวด "Your workspace is a worktree of your own"
  (สร้าง worktree เอง · เช็คเอาต์ของรอบเป็น read-only · ทดลอง mutation ในนั้นเท่านั้น · เก็บ worktree ตอนจบ
  · สร้างไม่ได้ = ถอยเป็นรีวิว read-only ห้ามกลายพันธุ์ต้นไม้จริง)
- ระหว่างแก้พบสำเนาฝั่ง server ตกยุค (ขาดข้อเช็ค 12/13 ที่ COO เคาะไว้ตั้งแต่ 0441) ⇒ sync ให้เหมือนกัน 100%
- ประกาศกฎข้อ 1 (ห้าม add -A รอบที่รัน adversary ฯลฯ) ลง `AGENTS.md` §7 บรรทัดเดียว + ลิงก์
- หมายเหตุความซื่อสัตย์: adversary ของรอบนี้เองรันก่อนนิยามใหม่ลง main (มันตรวจ diff ของรอบนี้อยู่ขณะแก้นิยาม)
  chief ถือกฎข้อ 1 (stage ทีละไฟล์ + อ่าน diff --cached) ในรอบนี้แล้ว

## จดหมาย

บริโภค + stub 2 ใบ: `1330 CORE-REQUEST-GM-036` (งานหลัก 1) · `1444 COO-DECISION adversary-worktree` (งานหลัก 2)
ใบอื่นในกล่องเป็น ASK-COO / ของสายอื่น — เจ้าของใบบริโภคเองตามกฎ 1405
เขียน 1 ใบ: `CHIEF-REPLY-LANE-GM-036` ข้างบน

## คิวเทส

ไม่มีใบใหม่รอบนี้ — งานทั้งใบเป็นชั้น wire/console ล้วน (ตรงกับ nonclaim ของสาย GM เอง:
ใบนี้ไม่มีชั้น client-observable) · การปฏิเสธ /warp ตรงคีย์บอร์ดถึงคอนโซล operator แล้ววันนี้
ส่วนข้อความถึงผู้เทสในเกมยังปิดที่ RE-132 (`gm/say_wire.py`) — เมื่อเปิดได้ค่อยมีของให้เทสตา

## WIRED

WIRED = ไม่มีโมดูลเลนใหม่รอบนี้ (งานเป็นการต่อ kwarg เข้าโซ่ GM ที่ WIRED อยู่แล้ว + นิยาม agent)
นิยาม WIRED v2: token `GM_LOGIN_SCENE_OVERRIDE_CONSUME_FAILED` ใหม่ยิงบน production path จริง
(grep ได้จาก headless boot เมื่อเงื่อนไขเกิด) · token เดิมของ probe ยังอยู่

## สถานะปิดรอบ

push แล้ว รอ merge: `pirate-force-server#264` (โค้ด) · `pf_bridge#415` (ใบนี้+จดหมาย+นิยาม agent+AGENTS)
งานอยู่บน main ต่อเมื่อรอบหน้าเห็น merged=true (หัวข้อ 2 ข้อ 7)

ตอนนี้ต้องทำอะไรต่อ: รอบหน้าตรวจ merged=true ทั้งสองใบ แล้วไล่ CORE-REQUEST ที่ค้างถัดไป (ถ้ามีใบใหม่เข้า)
