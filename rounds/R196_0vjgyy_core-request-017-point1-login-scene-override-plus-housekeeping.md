# R196 (session 0vjgyy) 2026-08-27 ~18:0x-18:3x (+07:00)

## สรุปหนึ่งบรรทัด
ต่อสาย CORE-REQUEST-017 จุดที่ 1 (LANE-GM login-scene override) เข้า `runtime.py` จริง, pf-adversary
สามรอบพบและแก้บั๊กจริงสามจุด (HIGH ในสองจุด compose หลัก + จุดที่สามที่พบระหว่างรีวิวรอบสอง) ก่อน push,
เปิด GT-110, ปิดค้าง mailbox 2 ใบ + registry row 013.

## บริบท
รอบก่อน (R195, session 8soxxm) สร้าง `lane_hooks/` skeleton และสัญญาไว้ว่า CORE-REQUEST-017 จุดที่ 1
(login-scene override สำหรับบัญชี GM) จะต่อสายรอบถัดไป — รอบนี้ทำตามสัญญานั้น ตรวจแล้วว่า R195 ทั้งสอง repo
`merged=true` จริง (หัวข้อ 2 ข้อ 7) ก่อนเริ่มงานใหม่

## งานหลัก: CORE-REQUEST-017 จุดที่ 1

`gm/login_scene_override.py` (GM-005) มีอยู่แล้วตั้งแต่ก่อนหน้า ยูนิตเทสผ่านแล้ว (`tests/test_gm_login_scene.py`)
แต่ไม่เคยมีจุดเรียกใน `runtime.py`/`app.py` รอบนี้ต่อสายจริง:

- `runtime.py`'s `START_GAME_REQ` handler: ก่อนเรียก `world_scene_entry.resolve_entry()`, เรียก
  `get_login_scene_override(self.token)` — ถ้าบัญชีเป็น GM ที่ลงทะเบียนไว้และมี entry ชี้ scene_id ที่รู้จัก
  แทนที่เฉพาะ `scene_id` ของ row ที่ป้อนเข้า `resolve_entry()` (x/y/z/heading เป็นของแถวจริง) จึงยังใช้กฎ
  ความปลอดภัยเดิมของ `resolve_entry()` ครบ (ground-evidence, home-never-touched, `login_entry_allowed`)
- ต่อสายตรงใน `runtime.py` ไม่ผ่าน `lane_hooks` เพราะต้องเปลี่ยนค่าที่ป้อนเข้า `resolve_entry()` จริง ๆ
  ซึ่งเกินชนิดที่ `lane_hooks.fire()` ออกแบบไว้ (report-only โดยเจตนา ตามคอมเมนต์ของแพ็กเกจเอง)

### pf-adversary รอบแรก พบ HIGH จริง 1 ข้อ (แก้แล้ว)

ดราฟต์แรกเปลี่ยนแค่ input ของ `resolve_entry()` (สำหรับ teleport packet) แต่ `pc, frame`
(START_GAME_RES ที่มี ActorAttr/MovementAttr) ถูก compose ไปแล้วก่อนหน้านั้นจริงโดย `select_and_start()`
จาก row จริงของตัวละคร (ไม่ผ่าน override เลย) — เป็น "กับดักใหญ่ที่สุด" ที่ `world_scene_entry.py` เขียน
คำเตือนไว้เองตรง ๆ: teleport กับ ActorAttr/MovementAttr ชี้คนละที่ pf-adversary จำลองไบต์จริง: ActorAttr เข้ารหัส
`scene_id=1` (บ้าน) ขณะที่ teleport ตามหลังทันทีบอก `scene_id=2` — ค้นพบเพราะทุก login ในโปรเจกต์นี้ก่อนหน้า
override นี้อยู่ที่บ้านเสมอ (ไม่เคยมี relocation จริง) invariant จึงเป็นจริงโดยบังเอิญมาตลอด ไม่เคยถูกพิสูจน์จริง

**แก้:** เพิ่มบล็อก "resync pc/frame" หลัง `resolve_entry()` สำเร็จ — compose ใหม่ผ่าน
`self.foundation.projector.start_game(selected, position=entry.position, backpack=...)` โดยใช้ `entry.position`
(ตำแหน่งเดียวกับที่ teleport ใช้ รวม scene_seq ที่ถูกต้องของปลายทาง ไม่ใช่ของ login_row ที่ยังเป็นค่าเดิม)
ตกกลับไปใช้ `pc, frame` เดิมถ้ามี exception หรือความยาวไบต์ไม่ตรง (แพทเทิร์นเดียวกับที่ HYP-PF-027's
`_npc_hostile_start_game_response` ใช้กับ projector call เดียวกันอยู่แล้ว)

**พบเพิ่มระหว่างไล่โค้ดหลังรีวิว:** มีจุด compose START_GAME_RES ที่สองในฟังก์ชันเดียวกัน — สาขา
`elif not active_lanes:` (PANYA-CHASE 20260827_0915, `basic_faction=1` แบบไร้แฟล็ก) ซึ่งเป็นเส้นทาง
production จริงที่ login ทุกครั้งที่ไม่มี scenario flag เดินผ่าน — เรียก `projector.start_game(...)` โดยไม่ส่ง
`position=` เลย (default กลับไปที่ row จริงของตัวละคร) จะล้าง resync ของจุดแรกทิ้งเงียบ ๆ บนเส้นทางที่ผู้เล่นจริง
ทุกคนเดินผ่าน แก้โดยส่ง `position=(entry.position if login_scene_override is not None else None)` เข้าไปด้วย
(ให้ `login_scene_override` มีค่าเริ่มต้น `None` นอกบล็อก `if not load_only:` เพื่อไม่ให้ `NameError` ตอน
load_only=True)

### เทสใหม่ + ระดับไบต์

`tests/test_gm_login_scene_override_wiring.py` — 6 ข้อ ขับผ่าน dispatcher จริง (`make_state_class`):
- GM ที่มี override ไปถึงฉากนั้นจริง (บรรทัดคอนโซล `WORLD_SCENE scene_id=` + event)
- ไม่ใช่ GM / GM ไม่มี entry / config หาย / config ผิดรูป → ไม่กระทบ ยังอยู่บ้าน (scene_id=1)
- **`test_the_actor_movement_frame_agrees_with_the_teleport_not_the_stored_row`** — เทสที่พิสูจน์การแก้ HIGH
  จริง: resolve `entry` อิสระด้วยฟังก์ชันจริงตัวเดียวกัน compose เฟรมคาดหวังผ่าน `projector.start_game()`
  เดียวกับที่เส้นทาง production ใช้ แล้วเทียบกับไบต์จริงที่ dispatcher ส่งออกมา + ยืนยันว่าไบต์ที่คาดหวัง
  **ไม่เท่ากับ** ไบต์ที่ใช้ row จริง (กันเทสผ่านหลอกถ้า resync ถูกถอดออกเงียบ ๆ ภายหลัง)

### pf-adversary รอบสอง ยืนยันการแก้ + พบจุดที่สาม (แก้แล้วเช่นกัน)

รอบสองยืนยันว่าทั้งสองจุด compose (resync block + `elif not active_lanes:`) ตรงตามที่อ้าง และเทสใหม่พิสูจน์จริง
ไม่ผ่านหลอก (มี guard `assertNotEqual(expected, home)` กันไว้) แต่พบจุด compose ที่สาม:
`_npc_hostile_start_game_response` (HYP-PF-027, สาขา `if npc_hostile_hypothesis_scenario is not None:`)
ก็เรียก `projector.start_game(...)` โดยไม่ส่ง `position=` เช่นกัน — ปลอดภัยเพราะเมธอดนี้ no-op สำหรับทุกตัวละคร
ที่ไม่ใช่ pinned smoke identity เดียวที่ hardcode ไว้ (แทบเป็นไปไม่ได้ที่บัญชี GM จริงจะชนกัน) แต่เป็นแค่สมมติฐาน
เชิงปฏิบัติการ (scenario flag ไม่เปิดคู่กับบัญชี GM จริง) ไม่ใช่สิ่งที่โค้ดบังคับจริง — เพิ่ม `position=` kwarg ให้
เมธอดนี้และ call site ด้วยแพทเทิร์นเดียวกับอีกสองจุด (ปลอดภัย 100% เพราะ `position=None` คือพฤติกรรมเดิมทุก
ประการ) ปิดคำถามเปิดของ pf-adversary ("อะไรกันไม่ให้ hypothesis scenario เปิดคู่กับ GM login จริง") ด้วยการทำให้
ไม่สำคัญอีกต่อไปว่าจะเปิดคู่กันหรือไม่ — ทุกจุด compose ในฟังก์ชันนี้ตอนนี้ threading ค่า override เดียวกันครบแล้ว

MEDIUM (login_entry_allowed=False lockout) และ LOW (double is_gm_account lookup) ยังคงเป็น nonclaim ที่บันทึกไว้
ไม่ได้แก้โค้ดเพิ่มรอบนี้ ทั้งคู่ pf-adversary ยืนยันว่ายัง "ไม่พบว่า exploit ได้จริง" (LOW) และ "เป็น fail-closed
ที่ตั้งใจ ยังไม่ตัดสินใจว่าต้องการ guard เพิ่มไหม" (MEDIUM)

full suite (หลังแก้จุดที่สาม): `3486 passed, 327 skipped, 0 failed` เขียว(cloud sanity) ไม่มี regression
`tools/verify_hypothesis_ledger.py PASS entries=47` ไม่มี diff

### nonclaim สำคัญ
ถ้า override ชี้ไปฉากที่ปักหมุด `login_entry_allowed=False` (วันนี้: ฉาก 17) login ทั้งครั้งจะถูกปฏิเสธเงียบ
(fail-closed, ไม่มี reply เลย client ค้าง "connecting") ไม่ใช่ fallback กลับที่เดิม — ตั้งใจ ไม่ใช่บั๊ก แต่ผู้ตั้ง
config ต้องรู้ (pf-adversary รอบแรกตั้งข้อสังเกตนี้เป็น MEDIUM — เอกสารไว้ ยังไม่แก้โค้ดเพิ่ม)

## GAME_TEST_QUEUE

เปิด **GT-110** (`pf-queue-author`) — client-observable ของ feature นี้: บัญชี GM ที่ตั้งค่า override ไปฉาก 2
(Prison Exile Island) จริงไหมบนจอ, ยืนที่ spawn ปักหมุด `(26905.0, 21185.0, 1680.0)` ไหม, ไม่ crash/glitch
อ้างหลักฐาน headless (6/6 เขียว) เป็นชั้น wire/DB ไม่ให้ผู้เทสรันซ้ำ

## กล่องจดหมาย

- `20260827_1600_CHIEF-ASK-COO-world-population-handoff-formal-status-unclear.md` + คำตอบ
  `20260827_1645_COO-DECISION-world-population-handoff-superseded-moot-pending-M2.md` — stub ทั้งคู่
  ทำตามที่ 1645 สั่ง: เติมบรรทัด "Action taken" ลงใน stub เดิมของใบ `20260826_0910`
  (`archive/notes_to_chief_2026-08-19_to_26/...CONSUMED.txt`) + อัปเดตตาราง CORE-REQUEST registry row 013
  เป็น superseded/moot (เดิมค้างคำว่า "ยังไม่ moot" จาก decision 1144 ที่ถูก 1645 กลับคำไปแล้ว — registry
  ไม่ตรง decision ล่าสุดมาตั้งแต่ 16:45)
- backlog ที่เหลือ: ยังมี unconsumed letters ค้างจำนวนมาก (>130 ใบ ณ ต้นรอบ) ส่วนใหญ่เป็นของสาย A/B/GM เอง
  (กฎ v6.3 "ใครเปิดใบคนนั้นบริโภค" — ไม่ใช่ของ chief) ที่เป็นของ chief จริง (CHIEF-*/COO-*/PANYA-*/ไม่มีเจ้าของ)
  เหลือ ~75 ใบ รอบนี้ทำได้แค่ 2 ใบที่ผูกกับงานโค้ดจริงของรอบ (เวลาไปที่ pf-adversary สองรอบของ CORE-REQUEST-017)
  ยังไม่ใช่ backlog ที่หมด รอบถัดไปควรหยิบต่อ

## เลขชนกัน GT-109/GT-110

`pf_bridge` PR แรกของรอบนี้ (#221) ถูก `merge-claude-pr` ปิดอัตโนมัติเพราะ `mergeable=false` — LANE-A (รอบ
`jafskv`) เปิด `GT-109` ของตัวเองพร้อมกัน (VEHICLE-BIND-WIRE-CAPTURE-001) และ commit ของเขาลง `main` ก่อน
กู้ด้วย `git merge origin/main` (เก็บทั้งสองบล็อกไว้ ไม่ทิ้งฝั่งไหน ตามกฎ) แล้วขยับใบของ chief เป็น `GT-110`
ตามกฎ "ชนแล้วห้ามทับ" เปิดล็อกใหม่เป็น PR ใบถัดไปเพื่อยึดคืน — branch ไม่เคยหาย ไม่มีข้อมูลสูญ

## งานแม่บ้านที่ยังไม่ทำ (บันทึกไว้ ไม่ใช่ลืม)

- `CHIEF_CONTINUATION.md` (~124KB) และ `AGENTS.md` ทั้งสอง repo (~89KB คนละไฟล์กัน ไม่ใช่ของเดียวกัน) ยังเกิน
  เพดานถาวรมาก (PANYA-ORDER 13:45 ข้อ 9) — deferred ต่อเนื่องมา R193/R194/R195/R196 เพราะเป็นงาน archival
  ที่เสี่ยงข้อมูลหายถ้าเร่งทำพร้อมงานโค้ด ต้องเป็นรอบเดี่ยวที่ไม่ทำอะไรอื่น เสนอเป็นรอบถัดไปที่ไม่มีงาน
  CORE-REQUEST ค้างเร่งด่วนกว่า
- "พิน 48 + รายชื่อเรียงแล้ว" (v6.3 §18 ข้อ 5) — หาที่มาของตัวเลข "48" ไม่เจอในทั้งสอง repo รอบนี้ (grep
  `== 48` ไม่ตรงที่ไหนชัดเจน) ไม่กล้าเดาแล้วแก้ผิดจุด ต้องขอ COO/Panya ชี้ path ที่แน่นอนก่อน
- ABORT structural rule ของ teardown script (v6.3 §18 ข้อ 4) — เป็นงานฝั่งสะพาน (`staged/TEMPLATE_teardown_generic.ps1`)
  chief cloud แก้ตรง ๆ ไม่ได้ (ไฟล์ job ไม่ sync เข้ามาที่ clone คลาวด์) ยังไม่ทำ

## WIRED

WIRED v2 ไม่เปลี่ยน = 9/10 (CORE-REQUEST-017 ไม่ใช่หนึ่งใน 10 เลนที่นับ เป็นเลนย่อยของ LANE-GM ที่มีอยู่แล้ว)

## ค้าง

- CORE-REQUEST-017 จุดที่ 2 (census ของฉาก override) ยังไม่มีฟังก์ชันให้เรียก ยังไม่ต่อสาย
- MEDIUM finding (login_entry_allowed=False lockout) — เอกสารเป็น nonclaim ยังไม่แก้โค้ด รอ COO/Panya ตัดสินว่า
  ต้องการ validation เพิ่มที่ `login_scene_override.py` (เช็ก `login_entry_allowed` ตอนโหลด config) หรือพอแค่นี้
- LOW finding (double `is_gm_account()` lookup ต่อ login) — ไม่พบว่า exploit ได้จริง ไม่แก้รอบนี้
- mailbox backlog (chief-owned) ~73 ใบยังไม่ stub
- housekeeping ไฟล์ใหญ่ (ดูหัวข้อบน)
