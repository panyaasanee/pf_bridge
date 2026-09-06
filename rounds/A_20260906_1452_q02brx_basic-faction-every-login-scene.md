# LANE-A round q02brx (2026-09-06T14:52+07:00) — basic_faction on every login scene

## รอบนี้ขยับ NOW/M ข้อไหน
NOW.md "LANE-A งานแรกรอบถัดไป" (`1347` P-2 ชั้นแรก): ส่ง `basic_faction` ของผู้เล่นทุก login scene (ทะเล 126 ด้วย) — บล็อก GT-220/223/242 และเป็นชั้นที่สองของ "มอนเขียวตีไม่ได้" ที่ ka1-A ระบุใน `KA1A-R321-RESULTS §1`. ไม่ขยับ M2/M3 โดยตรง (M3 = P-2 สีมอน ยังเป็นชั้นสองของ B) แต่ปลดบล็อก GT-220/223/242 เมื่อขึ้น main.

## ที่ทำ
`pirate-force-server` (`src/pirateforce_foundation/world_faction_admission.py`): `admits(scene_id)` เดิมส่ง faction เฉพาะฉากที่ registry บอก `login_entry_allowed=True AND n_SAVE==1` (บวกพื้น `(1,2)` ที่ GT-032 พิสูจน์). สาเหตุจริงที่ ka1-A วัด: login ผ่านตั๋ว relog GM `/warp 126` (ทดสอบ M2 arrival ที่ยังไม่ใช่ทางเดินเรือจริง) ตกทั้งสองเงื่อนไข (126: `login_entry_allowed=false`, `n_SAVE=0`) → เฟรม `FOUNDATION_SELECTED_START_GAME` ไม่มี `basic_faction` → client ไม่อ่านฟิลด์นี้ซ้ำอีกเลยทั้งเซสชัน → มอนเขียวทุกฉากจนกว่าจะ login ใหม่บนบก

แก้: `admits()` ไม่อ่าน registry อีกต่อไป — รับทุก scene_id ที่เป็น `int` จริง (ไม่ใช่ `bool`) ปฏิเสธเฉพาะที่ไม่ใช่ int เลย ไม่มีเลขฉากฝังโค้ด ไม่เช็คเลเวล ตามคำสั่ง COO ตรงตัว

**ทำไมไม่เปิดประตูฉากไหนเพิ่ม:** `world_faction_admission` ถูกเรียกที่เดียวคือตัวประกอบเฟรม (`player_wire.make_actor_attr_with_name_class_and_faction`) เพื่อตัดสินว่าจะเสียบฟิลด์ 5 ไบต์เพิ่มลงเฟรมที่ประกอบเสร็จแล้วหรือไม่ — คนละเรื่องกับ "ฉากนี้ล็อกอินเข้าได้ไหม" ซึ่งเป็นของ `world_scene_entry.resolve_entry`'s `login_entry_allowed` (คนละโมดูล ไม่แตะ) grep ผู้เรียก `admits`/`admitted_scene_ids` ทั้งต้นไม้แล้ว ไม่มีที่ไหนใช้ตัดสินการเข้าฉากจริง

แก้ตามเทสที่พังจากการเปลี่ยนนี้ (registry-gated negative controls กลายเป็นไม่จริง): `tests/test_world_faction_admission.py` (เขียนใหม่เกือบทั้งไฟล์ — พิสูจน์ "ทุกฉาก" แทน "ฉากที่ registry อนุญาต"), `tests/test_world_scene_marker.py` (1 assertion), `tests/test_player_hostile_pairing.py` (1 เทสพลิกจากคาดปฏิเสธเป็นคาดยอมรับ), `tests/test_player_wire_probe_base1.py` (1 sub-case เปลี่ยนจาก int เป็น non-int เพราะ int ไม่ถูกปฏิเสธอีกแล้ว) + docstring 7 ไฟล์ (`world_population_bg1001/3001/3007/3008.py`, `world_bg3001/3007/3008_identity.py`) ที่เคยเขียนว่า "ฉากนี้ไม่มี faction frame เพราะ world_faction_admission ปฏิเสธ" — ตอนนี้เท็จ

ชุดเทสเต็ม: `python3 -m pytest tests/ -q` → 12357 passed, 365 skipped, 0 failed (หลังแก้ตาม adversary)
`tools_bridge/pf_gate_preflight.py --repo <server>`: PASS (ตรวจซ้ำหลัง merge origin/main รอบสุดท้าย)

**TWO_SESSIONS_SAME_SCENE:** ไม่แตะ — รอบนี้จำกัดอยู่ที่ฟิลด์ faction บนเฟรม login ครั้งเดียวตอน StartGame ไม่มีการอ่าน/เขียน world registry ที่แชร์ข้าม session

## จดหมาย
- บริโภค `notes_to_chief/20260906_1347_COO-DECISION-ka1a1255-...LANE-A.md` (stub + copy ไป `consumed/` แล้ว)
- ส่งเนื้อใบ GT ให้ LANE-K ตั้งเลข: `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md`
- ส่งจุดคอมเมนต์ค้างนอกเขตให้ chief/LANE-GM: `notes_to_chief/20260906_1546_LANE-A-TO-CHIEF-stale-comments-outside-my-zone-after-world-faction-admission-widening.md`

## adversary
pf-adversary คืนผลแล้ว (agent id ab334c7a81dc9b32d, รันในเวิร์กทรีแยก) — สรุป:
- ยืนยันด้วย mutation testing สดว่าเทสจับ regression จริง (ไม่ใช่ผ่านลอย): `admits()` ที่ปล่อย `bool` ผ่าน / `admits()` ที่คืน `True` เสมอไม่มี fail-closed → ทั้งสองแบบถูกจับ (แบบหลังทำให้ `u16tag` ของ V141 ตัวจริง crash เป็น `TypeError`)
- ยืนยัน `world_scene_entry.resolve_entry` (ประตูเข้าฉากจริง) ไม่ถูกแตะเลย (diff ว่าง) และไม่มีผู้เรียก `admits`/`admitted_scene_ids` ที่เอาไปตัดสินการเข้าฉาก
- เทสที่เขียนใหม่ไม่ใช่ tautology — ลองสองรอยแตก (bool ผ่าน, ไม่มี fail-closed เลย) แล้วเทสจับได้ทั้งคู่
- **พบ:** docstring ค้างใน `player_wire.py` (`make_actor_attr_with_name_class_and_faction`) อ้างกฎ registry เดิม — **แก้แล้ว** (commit `50b30cf0`) เทสรันซ้ำผ่านหมด (12357 passed)
- **พบเพิ่ม นอกเขตเขียนของผม** (ไม่แก้เอง ส่งต่อ): `runtime.py` (chief) 1 จุด · `gm/attr_wire.py` + `gm/login_mask.py` + `tests/test_gm_attr_wire.py` (LANE-GM) 3 จุด · `live_named_attr_values.py` (เจ้าของไม่ชัด) 1 จุด — ทั้งหมดเป็นคอมเมนต์ค้าง ไม่กระทบพฤติกรรมจริง (โค้ดที่เรียกจริงดึงค่าไดนามิก ไม่ hardcode) — รายละเอียดในจดหมายข้างบน
- **ข้อสังเกตไม่ใช่ข้อบกพร่องของรอบนี้:** client "ไม่อ่าน faction ซ้ำหลัง login" อาจกระทบเฟรมอื่นที่ย้ายฉากกลางเซสชัน (teleport, M2 sailing ในอนาคต) — ยังไม่มีใครวัด ฝากไว้เป็นคำถามเปิด ไม่ใช่บั๊กที่วัดแล้วของรอบนี้

**ปลดล็อกแล้ว:** PR `pirate-force-server#927` undraft + เติม `PF-AUTOMERGE: v4` (ยืนยันด้วย GET: `draft:false`, marker อยู่จริง) → claim PR `[LANE-A] round q02brx: claim` (pf_bridge#1501) เติม marker ปลดล็อกด้วย (ดูขั้นตอนถัดไป)

## รอบหน้าทำอะไร
ตาม NOW.md ต่อคิว M2 (`GT-233` บนเครื่อง Panya) และ remote-player/choose-npc งานที่ #1476 ส่งต่อ

## ติดอะไร / ใครปลด
ไม่มี — รอบนี้ปลดล็อกเองแล้ว

SCOREBOARD: COMING | มอนเขียวตีไม่ได้หลัง login ฉากทะเล/ฉากไม่ปกติจะหาย (ผู้เล่นได้ basic_faction ทุก login ไม่ใช่แค่ฉากที่ registry อนุญาต) — รอ merge เข้า main + ใบ GT attended ยืนยันบนจอ | pirate-force-server#927 (open, marker + adversary ผ่าน, รอ gate) · pf_bridge round q02brx
