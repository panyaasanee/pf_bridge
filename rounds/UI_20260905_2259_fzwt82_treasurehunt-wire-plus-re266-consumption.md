# LANE-UI round fzwt82 -- 2026-09-05T22:49+07:00 start

## ล็อกรอบ
- list เปิด `[LANE-UI]` ทั้งสองรีโป: พบ `pf_bridge#1370` (round `wzdzf7`, created_at 13:06Z, อายุ
  2h41m) ค้าง — กิ่งมีไฟล์รอบจริงแทน `_claim.md` แล้ว
  (`rounds/UI_20260905_2005_wzdzf7_ui-b-real-exit-game-logout-headless.md`) และ server PR
  `pirate-force-server#846` ของรอบนั้น merge แล้ว (`merged_at 2026-09-05T14:37:08Z`, ยืนยันด้วย
  `pull_request_read get`) แต่ marker ไม่เคยถูกเติม ⇒ **เข้าเงื่อนไข "เสร็จแล้วแต่ไม่ได้ปลด"**
  เติม `PF-AUTOMERGE: v4` ให้ `#1370` แทนเขา (ตรวจด้วย `pf_gate_preflight.py --pr-body ... --pr-stage
  final` = PASS ก่อนเปิด แล้ว GET body กลับมายืนยัน marker อยู่จริง) **released #1370 on behalf**
- เปิด claim ของตัวเอง `pf_bridge#1388` (`[LANE-UI] round fzwt82: claim`, ไม่ draft, body ตรวจด้วย
  `--pr-stage claim` = PASS ไม่มี marker) จากกิ่ง `claude/peaceful-pascal-fzwt82` (pf_bridge) และ
  `claude/inspiring-feynman-fzwt82` (pirate-force-server) — ทั้งสองกิ่งเป็นกิ่งที่ระบบมอบให้เซสชันนี้
  ตั้งแต่ต้น (`claude/*`) ไม่ได้ตั้งชื่อเอง
- list ซ้ำทันทีหลังเปิด: ไม่มีใบ `[LANE-UI]` อื่นเก่ากว่าและยังมีชีวิตแข่งอยู่ ⇒ ชนะ ทำงานต่อ

## กล่องจดหมาย (ADDRESSEE: LANE-UI / UI, ยังไม่ consumed ก่อนรอบนี้)
- `20260905_2242_RE-266-RESULT-*` (ใบของตัวเอง, ticket `1405`) — บริโภคแล้ว: เขียนจดหมายเสนอ
  chief แก้หัวใบ `GT-184`/`GT-186` + บล็อก `ATTENDED:` (ดูจดหมาย `20260905_2259_LANE-UI-TO-CHIEF-*`)
  และอัปเดต `docs/UI_LANE.md`'s UI-A row ในรอบเดียวกัน — ไม่แก้ `GAME_TEST_QUEUE.md` เอง (ไฟล์ของ
  chief) · stub วางแล้ว
- `20260905_2054_COO-DECISION-*adversary-unavailable*` — ตรวจแล้วว่าถูกทำไปก่อนรอบนี้ (`#846`
  undraft+merge จริง `merged_at 14:37:08Z`) ไม่มีอะไรต้องทำเพิ่ม · stub วางแล้ว
- `FROM_CHIEF_R358_TO_ALL_20260905_2011.md` ข้อ 1 (LANE-UI) — ข้อมูลถูกแทนที่แล้วโดย RE-266 result
  ที่มาทีหลัง และเขตเขียนที่มันอ้าง (`pf_bridge/docs/UI_LANE.md`) ถูกแก้เป็น `pirate-force-server`
  repo โดยรอบก่อนหน้าตาม NOW `2149` — ไม่มีอะไรต้องทำเพิ่ม · stub วางแล้ว (เฉพาะข้อ 1)

## AGENTS.md section 7 — อ่านครบรอบนี้
ไม่มีกฎใหม่ที่กระทบงานของรอบนี้โดยตรง นอกจากที่ใช้ไปแล้ว: PR body marker ต้อง derive จาก
`.github/workflows/merge-claude-pr.yml`'s `PF_MARKER` ไม่ใช่ copy จากจดหมาย (ตรวจแล้ว = ตรงกับ
`PF-AUTOMERGE: v4` ที่ใช้อยู่แล้ว) และต้องรัน `pf_gate_preflight.py --pr-body` ก่อนเปิด/แก้ body ทุกใบ
(ทำแล้วทั้งสองใบ ผล PASS ทั้งคู่ — เอาต์พุตแนบในจดหมาย/คอมมิตนี้)

## งานหลัก (คิว LANE-UI) — สถานะ
1. UI-B ล็อกเอาต์จริง headless: **ปิดแล้วก่อนรอบนี้** (`#846` merged, `merged_at` ยืนยันด้วยกราฟ
   git ไม่ใช่ field `merged`) — ยังไม่ wired เข้า `runtime.py` dispatch จริง (grep ยืนยัน: ไม่มี
   `dispatch_real_exit_game_logout`/`ui_logout_exit_game` ใน `runtime.py` ณ `main` `322f7da`)
   CORE-REQUEST ค้างรอ chief ต่อ ไม่มีอะไรให้ LANE-UI ทำเพิ่มในเขตเขียนของตัวเองตอนนี้
2. UI-A กลับหน้าเลือกตัวละคร: **BLOCKED-ON-RE-266 → ตอบแล้วแบบ negative** ต้อง attended capture
   ต่อ (ดูจดหมายเสนอ chief ข้างบน) — ไม่มีโค้ดให้เขียนจนกว่าจะมีผล attended
3. tracepath auto-walk: BLOCKED-ON-LANE-A accessor (ไม่เปลี่ยนตั้งแต่ chief `1407`)
4. NPC shop: BLOCKED-ON-LANE-DB interface (ไม่เปลี่ยน)

⇒ **งานหลักทั้งสี่ข้อติดหมด** (2 ข้อรอเครื่อง Panya/chief, 2 ข้อรอสายอื่น) — หยิบงานสำรองข้อ 1
ทันทีในรอบเดียวกันตามกฎ (ไม่จบรอบเปล่า)

## งานสำรอง (ทำเมื่องานหลักติด) — 3 ข้อ
1. **[ทำแล้วรอบนี้]** ฟังก์ชันที่ layout รู้แล้วจาก `external/PF_SERIALIZER_FIELDS.tsv` (ไม่ต้องรอ
   RE): `TreasureHunt_StartExcavatingVital` (`0xE40B`) + `TreasureHunt_ExcavatingResultVital`
   (`0xF33F`) — ไฟล์: `pirate-force-server/src/pirateforce_foundation/ui_treasurehunt_wire.py`
   (ใหม่) + `tests/test_ui_treasurehunt_wire.py` (ใหม่, 9 เทส) — หลักฐานผ่าน: `pytest
   tests/test_ui_treasurehunt_wire.py tests/test_ui_trade_wire.py tests/test_ui_party_wire.py
   tests/test_ui_friend_wire.py tests/test_ui_mail_wire.py tests/test_ui_social_wire.py -q` =
   69 passed, 20 subtests passed; `tests/test_npc_interaction_wire.py` (guard-word/exemption
   census) = 31 passed, 33 subtests passed. TreasureHunt กลุ่มนี้ grep แล้วไม่เจอใบ RE/GT เดิม
   หรือโมดูลเดิม (`notes_to_chief/`, `CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`, `archive/`,
   `src/`, `tests/` — ผลลบเต็มอยู่ในโมดูล docstring)
2. ฟังก์ชันถัดไปที่ layout รู้แล้ว (backlog: `TreasureHunt_UpdateSceneTreasurePointVital` ต้องการ
   static RE ก่อนเพราะมี `CALL_UNCLASSIFIED` ปน, หรือกลุ่มถัดไปใน `Pets_`/`Channel_`/`Express_`/
   `BuildingCrystal_`/`Activity_`/`CollectionObj_`/`Winemaking_`/`KnowledgeGuru_`/`Gathering_`
   ที่ยังไม่ itemize) — ไฟล์: `ui_*.py` ใหม่ตามกลุ่มที่เลือก + `tests/test_ui_*.py` — หลักฐานผ่าน:
   pytest ไฟล์เทสใหม่ + sibling wire tests เขียว
3. เทส/technical debt ในโมดูล `ui_*` ที่ adversary เคยชี้ — รอบนี้ยังไม่มีผล adversary รอบใหม่คืน
   (ดู `ADVERSARY_PENDING` ข้างล่าง) รอบหน้าของ LANE-UI อ่านผลเป็นงานแรกก่อน claim ใหม่

## ADVERSARY_PENDING pirate-force-server (branch claude/inspiring-feynman-fzwt82, commit c1d11b92)
สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงานจริง (ครั้งที่ 1/2) ตรวจ diff `ui_treasurehunt_wire.py` +
`tests/test_ui_treasurehunt_wire.py` + `docs/UI_LANE.md` — ผลยังไม่คืนตอน push รอบนี้ · push ตามเดิม
ไม่ถือล็อกรอ · **รอบถัดไปของ LANE-UI อ่านผลเป็นงานแรกก่อน claim งานใหม่**

## เกต
`python3 tools_bridge/pf_gate_preflight.py --repo ../pirate-force-server` บนกิ่ง
`claude/inspiring-feynman-fzwt82`: `[cp874]` PASS · `[skips]` PASS (ไม่มี skip ใหม่) · `[mainmerge]`
PASS (`origin/main` `322f7da` อยู่ใน HEAD แล้ว) · `[census]` PASS · `[bridgesize]` PASS (ไม่มีไฟล์
กลางที่กิ่งนี้ทำให้โตกว่า `origin/main` ขณะเกินเพดาน) · `[branch]` แสดง RED ตอนรันจากเครื่องมือ
ท้องถิ่นเพราะโคลนของเครื่องมือ preflight เองอยู่บน `main` ไม่ใช่กิ่ง push จริง (การรัน push จริงผ่าน
GitHub API ไปที่ `claude/inspiring-feynman-fzwt82`/`claude/peaceful-pascal-fzwt82` ตรงตามกฎ)

## รอบหน้าทำอะไร
1. อ่านผล `pf-adversary` ของ commit `c1d11b92` ก่อนอื่น (ADVERSARY_PENDING ข้างบน) แก้ถ้ามีจริง
2. เช็คว่าจดหมาย `20260905_2259_LANE-UI-TO-CHIEF-*` ถูก chief รับ (หัวใบ `GT-184`/`GT-186` ขยับ
   หรือยัง) — ถ้าขยับแล้วและ Panya บูต attended แล้ว ให้ปิดวงจร; ถ้ายัง ให้ตรวจว่า chief ตอบอะไรมา
3. ถ้างานหลักยังติดหมด หยิบงานสำรองข้อ 2 ต่อ (กลุ่มถัดไปที่ layout รู้แล้ว)

## QUEUE_TRIAGE
ไม่ใช่หน้าที่ของ LANE-UI (เป็นของ chief ตาม `AGENTS.md` section 7) — ไม่เขียนบรรทัดนี้

SCOREBOARD: COMING | เขียนโมดูลถอดรหัสเฟรม TreasureHunt ขุดสมบัติ (เริ่ม/ผลขุด) ฝั่งเซิร์ฟเวอร์เสร็จ
พร้อมเทส 9 ตัวผ่านหมด แต่ยังไม่ต่อสายเข้าเกมจริง (ผู้เล่นยังกดอะไรไม่ได้จากงานนี้วันนี้); ปุ่ม
กลับหน้าเลือกตัวละครขยับจาก "รอผล RE" เป็น "รอเครื่อง Panya วัดจริง" | PR
`pirate-force-server` (กิ่ง `claude/inspiring-feynman-fzwt82`, commit `c1d11b92`), จดหมาย
`20260905_2259_LANE-UI-TO-CHIEF-re266-consumed-propose-gt184-186-attended-block.md`
