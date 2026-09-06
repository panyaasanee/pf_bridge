# LANE-A round q02brx (2026-09-06T14:52+07:00) — basic_faction on every login scene

## รอบนี้ขยับ NOW/M ข้อไหน
NOW.md "LANE-A งานแรกรอบถัดไป" (`1347` P-2 ชั้นแรก): ส่ง `basic_faction` ของผู้เล่นทุก login scene (ทะเล 126 ด้วย) — บล็อก GT-220/223/242 และเป็นชั้นที่สองของ "มอนเขียวตีไม่ได้" ที่ ka1-A ระบุใน `KA1A-R321-RESULTS §1`. ไม่ขยับ M2/M3 โดยตรง (M3 = P-2 สีมอน ยังเป็นชั้นสองของ B) แต่ปลดบล็อก GT-220/223/242 เมื่อขึ้น main.

## ที่ทำ
`pirate-force-server` (`src/pirateforce_foundation/world_faction_admission.py`): `admits(scene_id)` เดิมส่ง faction เฉพาะฉากที่ registry บอก `login_entry_allowed=True AND n_SAVE==1` (บวกพื้น `(1,2)` ที่ GT-032 พิสูจน์). สาเหตุจริงที่ ka1-A วัด: login ผ่านตั๋ว relog GM `/warp 126` (ทดสอบ M2 arrival ที่ยังไม่ใช่ทางเดินเรือจริง) ตกทั้งสองเงื่อนไข (126: `login_entry_allowed=false`, `n_SAVE=0`) → เฟรม `FOUNDATION_SELECTED_START_GAME` ไม่มี `basic_faction` → client ไม่อ่านฟิลด์นี้ซ้ำอีกเลยทั้งเซสชัน → มอนเขียวทุกฉากจนกว่าจะ login ใหม่บนบก

แก้: `admits()` ไม่อ่าน registry อีกต่อไป — รับทุก scene_id ที่เป็น `int` จริง (ไม่ใช่ `bool`) ปฏิเสธเฉพาะที่ไม่ใช่ int เลย ไม่มีเลขฉากฝังโค้ด ไม่เช็คเลเวล ตามคำสั่ง COO ตรงตัว

**ทำไมไม่เปิดประตูฉากไหนเพิ่ม:** `world_faction_admission` ถูกเรียกที่เดียวคือตัวประกอบเฟรม (`player_wire.make_actor_attr_with_name_class_and_faction`) เพื่อตัดสินว่าจะเสียบฟิลด์ 5 ไบต์เพิ่มลงเฟรมที่ประกอบเสร็จแล้วหรือไม่ — คนละเรื่องกับ "ฉากนี้ล็อกอินเข้าได้ไหม" ซึ่งเป็นของ `world_scene_entry.resolve_entry`'s `login_entry_allowed` (คนละโมดูล ไม่แตะ) grep ผู้เรียก `admits`/`admitted_scene_ids` ทั้งต้นไม้แล้ว ไม่มีที่ไหนใช้ตัดสินการเข้าฉากจริง

แก้ตามเทสที่พังจากการเปลี่ยนนี้ (registry-gated negative controls กลายเป็นไม่จริง): `tests/test_world_faction_admission.py` (เขียนใหม่เกือบทั้งไฟล์ — พิสูจน์ "ทุกฉาก" แทน "ฉากที่ registry อนุญาต"), `tests/test_world_scene_marker.py` (1 assertion), `tests/test_player_hostile_pairing.py` (1 เทสพลิกจากคาดปฏิเสธเป็นคาดยอมรับ), `tests/test_player_wire_probe_base1.py` (1 sub-case เปลี่ยนจาก int เป็น non-int เพราะ int ไม่ถูกปฏิเสธอีกแล้ว) + docstring 7 ไฟล์ (`world_population_bg1001/3001/3007/3008.py`, `world_bg3001/3007/3008_identity.py`) ที่เคยเขียนว่า "ฉากนี้ไม่มี faction frame เพราะ world_faction_admission ปฏิเสธ" — ตอนนี้เท็จ

ชุดเทสเต็ม: `python3 -m pytest tests/ -q` → 12343 passed, 365 skipped, 0 failed
`tools_bridge/pf_gate_preflight.py --repo <server>`: PASS

**TWO_SESSIONS_SAME_SCENE:** ไม่แตะ — รอบนี้จำกัดอยู่ที่ฟิลด์ faction บนเฟรม login ครั้งเดียวตอน StartGame ไม่มีการอ่าน/เขียน world registry ที่แชร์ข้าม session

## จดหมาย
- บริโภค `notes_to_chief/20260906_1347_COO-DECISION-ka1a1255-...LANE-A.md` (stub + copy ไป `consumed/` แล้ว)
- ส่งเนื้อใบ GT ให้ LANE-K ตั้งเลข: `notes_to_chief/20260906_1515_LANE-A-TO-K-gt-body-basic-faction-every-login-scene.md`

## adversary
`ADVERSARY_PENDING pirate-force-server#927` — สั่ง pf-adversary ต้นรอบ (agent id ab334c7a81dc9b32d) พร้อม diff เต็ม ยังไม่คืนผลตอน push · PR #927 เปิดเป็น **draft ไม่มี marker** ตามกฎ (แตะเฟรมล็อกอิน/ตัวตน actor) จนกว่าผลจะคืนและแก้ครบ

## รอบหน้าทำอะไร
1. ถ้า agent ab334c7a81dc9b32d คืนผลระหว่างเซสชันนี้ยังไม่จบ: อ่านผล แก้ตามที่พบ (ถ้ามี) แล้ว undraft PR #927 + เติม `PF-AUTOMERGE: v4` ปลดล็อก claim PR `[LANE-A] round q02brx: claim` (pf_bridge#1501) เอง — ไม่ต้องรอรอบใหม่
2. ถ้าเซสชันจบก่อนผลคืน: รอบถัดไปของ LANE-A สั่ง pf-adversary บนกิ่ง `claude/magical-goldberg-q02brx` เป็นงานแรก (เหมือนกรณี PENDING) แล้ว undraft + ปลดล็อกตามข้อ 1
3. หลังขึ้น main: ตาม NOW.md ต่อคิว M2 (`GT-233` บนเครื่อง Panya) และ remote-player/choose-npc งานที่ #1476 ส่งต่อ

## ติดอะไร / ใครปลด
ไม่มีจุดติดที่ต้องรอ COO — รอแค่ pf-adversary คืนผลเพื่อปลดล็อกรอบนี้เอง

SCOREBOARD: COMING | มอนเขียวตีไม่ได้หลัง login ฉากทะเล/ฉากไม่ปกติจะหาย (ผู้เล่นได้ basic_faction ทุก login ไม่ใช่แค่ฉากที่ registry อนุญาต) | pirate-force-server#927 (draft, ADVERSARY_PENDING) · pf_bridge round q02brx
