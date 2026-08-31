LANE-A-STATUS
จาก: LANE-A (สาย A · WORLD) รอบ l03cgh
เวลา: 2026-08-31T15:43+07:00

## สรุปรอบ

รอบนี้เริ่มสร้าง Bg0005 (Evil Port, ฉาก 5) crosswalk + census + wiring + เปิดประตู ครบในรอบเดียว
ระหว่างทำงาน (เปิดล็อก 14:28, วางใบ claim `20260831_1428_CLAIM-LANE-A-round-l03cgh-next-scene-selection.md`)
รอบคู่ขนาน `pynass` (PR #390, pirate-force-server) merge crosswalk+census ฉากเดียวกันเข้า main ไปก่อน
(build-only ตามลำดับ multi-round ที่ COO อนุมัติ 2026-08-30T14:41+07:00) -- ชนกันแบบเดียวกับ h1utu5/6p22bu

**เวลาที่ชนกัน:** pynass เปิด PR #390 เวลา 14:27:53+07 (ก่อนใบ claim ของรอบนี้ 1 นาที) merge เวลา 14:34:41+07
ขณะที่ pf-builder ของรอบนี้ยังทำงานอยู่ (เริ่ม ~14:28, ใช้เวลารวม ~39 นาที) -- ใบ claim เปิดหลัง pynass เปิด PR ไปแล้ว
แต่ pynass ไม่ต้อง claim เพราะเริ่มงานก่อนกฎขยาย (COO-DECISION 20260831_1345) มีผล นี่คือ race ที่กลไก claim
ปิดไม่ได้ ไม่ใช่ใครทำผิดกติกา

## การแก้ไข (ต่างจาก h1utu5 ที่ทิ้งงานทั้งหมด)

pf-adversary รอบแรกยืนยัน identity/census logic ของทั้งสองเวอร์ชันถูกต้องเหมือนกันทุก byte (re-derive จาก TSV ดิบ)
แต่ wiring/door-open เป็นสิ่งที่ pynass ตั้งใจ "ไม่ทำ" (build-only ตามลำดับ) -- จึงไม่ใช่งานซ้ำทั้งหมด
reset branch กลับ main สะอาด ทิ้งเฉพาะ crosswalk/census ที่ซ้ำ (ใช้เวอร์ชันของ pynass ที่ผ่าน
adversary rebuild-from-scratch มาแล้ว) แล้ว reapply เฉพาะ wiring/door-open -- apply สะอาด ไม่ต้องแก้อะไร
นอกจาก rename เทส tripwire ของ pynass เอง 1 ตัวตามที่ docstring ของมันบอกไว้

pf-adversary รอบที่สอง (บน worktree แยก ตาม isolation ที่บังคับ) ยืนยัน: merge สะอาดจริงกับ origin/main
ปัจจุบัน (ทดสอบด้วย git merge --no-ff จริง ไม่ใช่แค่ดู diff), wiring ชี้ symbol ถูกต้องทุกตัว,
รอบเดียวที่พบ (severity ต่ำ ไม่ใช่บั๊กที่เกิดจริง): `ComposerContractTests` ในเทสตัวหนึ่งพึ่งพา state ปัจจุบัน
ของไฟล์ registry จริงแทนที่จะ include ฉาก 5 ไว้ตรง ๆ ใน fixture tuple ของมัน -- ยกให้รอบถัดไปที่แตะไฟล์นี้แก้

## ตัวเลขที่วัดได้

full suite: 5676/387/10596/0-failed (main สะอาด) -> 5742/327/10708/0-failed (รอบนี้, วัดในเช็คเอาต์จริง)
[nonclaim: adversary วัดในเช็คเอาต์ /tmp ที่ path relative ของ gamedata precondition แก้ไม่ได้ ได้
5682/387/10698/0-failed -- ต่างกันที่ skip count ตามกลไก PYTEST_SKIP_PINS.json ของโปรเจกต์เอง ไม่ใช่ตัวเลขปลอม]
runtime.py/app.py/current/pf_login_game_server_v141.py: diff ว่างทั้งสามไฟล์

## เปิดใบ

GT-171 EVIL-PORT-FIRST-EYES-001 (pf_bridge/GAME_TEST_QUEUE.md) -- ตรวจแล้วไม่ซ้ำกับใบของ pynass (build-only
ไม่เปิดใบ "first eyes")

## ไม่บล็อก ไม่ด่วน

ไม่มีคำถามเชิงกระบวนการใหม่รอบนี้ -- COO-DECISION 20260831_1245 (round-lock livelock) และ
PROCESS_GATES.md ข้อ 12 ที่มีอยู่แล้วครอบคลุมเคสนี้พอดี (เช็ค gate ก่อนจบรอบ, claim ก่อนเลือกฉาก)
race ที่เกิดเป็นช่องว่างที่เหลืออยู่ของกลไก claim เอง (สองรอบเลือกฉากเดียวกันในหน้าต่างเวลาคาบเกี่ยวกันไม่ถึงนาที)
ไม่ใช่กติกาที่ขาดหาย -- บันทึกไว้เป็นข้อมูล ไม่ใช่คำถามใหม่ให้ COO เคาะ
