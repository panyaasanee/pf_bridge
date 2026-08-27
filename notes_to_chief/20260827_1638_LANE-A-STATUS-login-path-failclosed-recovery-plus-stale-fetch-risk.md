[ถึง: chief cloud · COO · cc Panya, RE runner | จาก: สาย A (WORLD) | 2026-08-27T16:38+07:00]
[อ้างอิง: `20260827_1544_LANE-A-STATUS-scene17-provisional-spawn-decree-wired-*.md` (รอบ `0z3kjx` - PR ไม่ merge)]

# LANE-A STATUS - กู้คืน login-path fail-closed fix ของรอบ `0z3kjx` + แจ้งความเสี่ยง git fetch เก่าค้าง

## สรุปสั้น

รอบ `0z3kjx` (จดหมายอ้างอิงข้างบน) ทำงานจริงและมีค่า แต่ **PR ทั้งสองใบ (pirate-force-server #127, pf_bridge
#209) ปิดไปโดยไม่ merge** เกือบแน่นอนเพราะ session รอบนั้นเขียนโค้ดบน `main` ที่ `git fetch` คืน snapshot เก่ากว่า
จริง (บั๊กที่ orchestrator ยืนยันแล้วว่าเคยเก่าเกินหนึ่งวันเต็มในแซนด์บ็อกซ์นี้) ผู้ใช้กู้คืนฝั่ง `pf_bridge` (3
คอมมิตของรอบนั้น) ให้แล้วก่อนรอบนี้เริ่ม และตรวจแล้วว่างานส่วนใหญ่ (spawn/ground ของฉาก 17, M2-no-vehicle) ถูก
chief cloud รอบ `e0daaa` (R194, PR #124, อยู่บน main แล้ว) ทำซ้ำ/ดีกว่าไปแล้วอย่างอิสระ - **เหลือชิ้นเดียวที่ยังไม่
ถูกกู้คืน**: fail-closed fix ของ login path เอง (pf-adversary พบในรอบ `0z3kjx` เองเช่นกัน) รอบนี้เขียนใหม่ทั้งหมด
บนโค้ดปัจจุบัน (ไม่ apply patch เดิมตรงๆ เพราะกลไก `ground_bound_waiver` ที่ diff เดิมอิงอยู่ถูก R194 แทนที่ไปแล้ว)
รายละเอียดเต็มอยู่ใน `rounds/A_20260827_1638_login_path_failclosed_recovery.md`

## ความเสี่ยง operational ที่ควรรู้ (ไม่ใช่แค่รอบนี้)

`git fetch origin main` ในแซนด์บ็อกซ์นี้เคยคืน snapshot ของ `main` ที่เก่ากว่าจริง (เก่าเกินหนึ่งวันเต็มอย่างน้อย
หนึ่งครั้ง) ทั้งที่คำสั่งรายงานว่าสำเร็จ - แม้แต่ `pf_bridge` worktree ของรอบนี้เองก็เช็คเอาต์อยู่ที่ commit เก่า
กว่าจริงเกินหนึ่งวัน (`3733440`, ไม่มี 3 คอมมิตของรอบ `0z3kjx` ที่ควรมี) จนกว่าผู้ใช้จะแก้ให้ด้วย `git fetch` แบบ
ระบุ SHA ตรงๆ แทนการเชื่อ `origin main` เฉยๆ **รูปแบบ "PR สาย A merge ไม่ติด" ที่เห็นซ้ำอาจไม่ใช่ปัญหาคุณภาพงาน
แต่เป็นบั๊กเครื่องมือ git fetch เอง** - คุ้มค่าที่ chief/COO จะรู้ในวงกว้าง ไม่ใช่แค่รอบนี้รู้คนเดียว

## สิ่งที่พบจริงระหว่างต่อสาย (คุ้มค่าที่จะรู้)

`world_scene_entry.resolve_entry()` คือฟังก์ชันเดียวกันเป๊ะที่ `runtime.py:4715` เรียกตอน login จริงทุกวันนี้
**(ต่อสายแล้วจริง ไม่ใช่แผนอนาคต)** - module docstring เดิมของ `world_scene_entry.py` ยังเขียนว่า "NOTHING CALLS
IT YET" ซึ่งล้าสมัยไปแล้ว (ไม่ได้แก้เองรอบนี้ นอก scope) หลังฉาก 17 มี spawn จริงจาก R194 การ refuse ฟรีที่เคย
ป้องกันแถวตัวละคร persist ฉาก 17 ไว้ก็หายไปด้วย (ไม่มี `CHECK` constraint บน `scene_id` เลย -
`migrations/001_initial.sql:5`) - latent เท่านั้น (ยังไม่มีทางเขียน `scene_id=17` ลง DB จริงวันนี้) แต่เป็นการเอา
fail-safe ออกไปเงียบๆ

## ของที่แตะใน `pirate-force-server` (7 ไฟล์ ไม่แตะ `runtime.py`/`app.py`/`current/`)

| ไฟล์ | อะไร |
|---|---|
| `scenarios/world_scene_registry_001.json` | ฉาก 17 เพิ่ม `login_entry_allowed: false` + คำอธิบาย |
| `src/pirateforce_foundation/world_scene_travel.py` | เพิ่มฟิลด์ `login_entry_allowed` (schema+dataclass+loader) |
| `src/pirateforce_foundation/world_scene_entry.py` | เพิ่ม `via_login` param + `REFUSED_NOT_ALLOWED_AT_LOGIN` |
| `src/pirateforce_foundation/columbus_quest_dispatch.py` | ส่ง `via_login=False` explicit จากจุดเดียวที่ปลอดภัย |
| `tests/test_world_scene_entry.py` | +8 เทสใหม่ (`LoginEntryRestrictionTests`) + แก้ 2 เทสเดิม |
| `tests/test_world_scene_travel.py` | +3 เทสใหม่ |
| `tests/test_columbus_quest_dispatch.py` | +1 เทสใหม่ |

## ตัวเลขที่วัดได้

- เทสกลุ่มเป้าหมาย (6 ไฟล์): **246/246 ผ่าน, 102 subtests ผ่าน**
- เทสทั้งเรโป: **3305 เทสผ่าน, 198 skipped, 3573 subtests ผ่าน, 23 collection errors** (ทั้งหมดคือ
  `capstone`/`tools` module เดิมที่ขาดในแซนด์บ็อกซ์นี้ ไม่เกี่ยวกับไฟล์รอบนี้เลยสักไฟล์) - **0 FAIL จริง**
- เทสใหม่: **12 เทส**
- cp874-encodability: ทุกไฟล์ที่แตะใน `src/`/`tests/`/`scenarios/` ผ่านหมด

## pf-adversary self-review (ไม่มี agent ให้เรียกในสภาพแวดล้อมนี้ - ทำเองแบบ adversarial)

ตรวจ 3 ข้อบังคับตามที่ผู้ใช้สั่ง (default fail-closed / schema validate junk / ไม่มี `via_login` default ผิดที่
เปิดประตูเงียบ) ครบทั้งสามข้อ - รายละเอียดเต็มอยู่ในไฟล์รอบ หัวข้อ ⑦ **พบและแก้เอง 1 จุดจริง**: เทสเดิม 2 ตัวใน
`ProvisionalDecreeTests` ที่ทดสอบกลไก ground/decree relocation ของฉาก 17 พังหลังเพิ่ม gate ใหม่ (เพราะเรียก
`resolve_entry` แบบ login call shape) - แก้โดยเพิ่ม `via_login=False` ให้เทสทั้งสอง (คนละเรื่องกับ login gate)
รันซ้ำผ่านจริง

## ยังไม่ได้พิสูจน์ / รอมนุษย์

- ไม่มีอะไรเปลี่ยนบนจอเกม - นี่คือ fail-safe ชั้น foundation เท่านั้น
- ยังไม่มีใครพิสูจน์ว่า path นี้เคย exploit ได้จริง (latent เท่านั้น)

## BUILD-002 (ฉาก 278 เป็นเส้นทางออกเริ่มต้น)

ยืนยันซ้ำว่ายังบล็อกตาม `notes_to_chief/20260826_2147_COO-DECISION-BUILD-002-scene278-stays-blocked.md` -
ไม่ทำ ไม่เปิด ASK-COO ซ้ำตามที่จดหมายฉบับนั้นสั่งไว้

## mailbox

ตรวจจดหมายหลัง `2026-08-27 15:44` ทั้งหมด - พบ 3 ฉบับ cc สาย A จาก chief cloud (ความเสี่ยง M2 ที่พบระหว่างรอบ
`e0daaa`) ไม่มีข้อไหนสั่งงานสาย A โดยตรง ไม่มีจดหมายที่จ่าหน้าถึงสาย A ตรงๆ ที่ยังไม่ consume - ไม่เปิดงานปลอม

## CORE-REQUEST

none - `runtime.py:4715`'s call site เดิมได้พฤติกรรม fail-closed อัตโนมัติจาก default ของ `via_login=True`
โดยไม่ต้องแก้บรรทัดเดียว (grep ยืนยันมีแค่ 2 call site ของ `resolve_entry` ทั้งเรโป)

## เปิดใบให้สาย C

none

— สาย A · WORLD
