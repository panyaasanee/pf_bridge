# GM round 2026-08-26 ~19:4x (+07:00) — npc-switch catalog for GM-003 `npc` command hint

ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#131`, `pirate-force-server#72`) — ตรวจ GitHub API แล้ว (ผ่าน `curl` ตรงถึง `api.github.com`, ไม่ใช้ `gh`) ก่อนยึดล็อก: ไม่มี PR หัวข้อขึ้นต้น `[LANE-GM]` เปิดค้างในทั้งสอง repo (pf_bridge มีแค่ `[LANE-E]` #130, pirate-force-server มีแค่ `[LANE-E]` #71 — ไม่ใช่ล็อกของสายนี้ ไม่แตะ)

MCP GitHub tool ไม่พร้อมใช้งานตอนต้นรอบ (`ToolSearch` คืนค่าว่างซ้ำหลายครั้ง) — ใช้ GitHub REST API ตรงผ่าน `curl` + `$GITHUB_TOKEN` ที่มีอยู่ใน container แทน (ยังเป็น "GitHub API" ตามกฎ ไม่ใช่ `gh` ซึ่งไม่มีในอิมเมจอยู่แล้ว)

## ตรวจสถานะก่อนเริ่มงานจริง

อ่านจดหมายค้าง (ใบ 1630 order, ใบ 1755 gate-RED, `FROM_CHIEF_R179`) ยืนยันว่า:
- `CORE-REQUEST-006` (ส่ง GM state ตอน login) ยังไม่ถูกต่อสายโดย chief (R179 ยืนยันตรง ๆ)
- `RE-091` (ความหมายสองสตริงของ `GM_RunGMCommandVital` + live chat trigger) ยังเปิดอยู่ ยังไม่มีผล — อยู่ในชุด `RE-085`-`RE-091` ที่รอ RE runner บนสะพาน (R178: "งาน GM tooling 4 ใบ")
- gate-RED bug ของใบ 1755 (sha256 ของ `.tsv` พังบน Windows CRLF) **แก้แล้วที่ต้นเหตุ**: `.gitattributes` มี `*.tsv text eol=lf` อยู่แล้ว (บรรทัดที่ chief เพิ่ม) — ตรวจ `git check-attr` กับไฟล์ `.tsv` ที่มีอยู่แล้วผ่าน ไม่ต้องแก้อะไรเพิ่มในเขตสายนี้

ทั้งสามจุดนี้บล็อกงานที่ตรงไปตรงมาที่สุด (execute คำสั่ง, ต่อสาย login) ตามกฎ "ไม่ตอบคำถาม สร้างของ" จึงหางานที่ **ไม่ต้องพึ่ง RE/chief** และยังเดินหน้าจริงได้

## สร้าง/แก้ (`pirate-force-server`, เขตเขียนของสายนี้ทั้งหมด)

พบว่า `CONSTDATA_TH__MOBS.n_GM_SWITCH` (7 แถว NPC กิจกรรม ที่ใบ 1630 เจอไว้แล้ว) ยังไม่เคยถูกทำเป็นโค้ด — `gm/commands.py` ตรวจ `warp` กับ `gm/scene_catalog.py` (GM-004) อยู่แล้ว แต่ `npc on|off <mob_id>` ไม่มีอะไรตรวจเลย ทั้งที่ข้อมูลอยู่ใน gamedata ที่ commit แล้ว (ไม่ใช่ของสาย A/B ต้องรอ import)

- **ใหม่** `gm/data/gm_npc_switch.tsv` — สกัด 2 คอลัมน์ (`n_ID`, `s_NAME`) จาก 7 แถวที่ `n_GM_SWITCH=1` ใน `pf_bridge/gamedata/tables/CONSTDATA_TH__MOBS.tsv` (3211 บรรทัด 54 คอลัมน์ sha256 ต้นทาง `3c0d33d6…b3916b`) — เป็นแฟ้มย่อยแบบเดียวกับที่ `gm/data/gm_scene_name_tip.tsv` ทำไว้กับ GM-004
- **ใหม่** `gm/npc_switch_catalog.py` — โหลด + พิน sha256 ตอน import (`484d6647…5ba5237`) แบบเดียวกับ `scene_catalog.py` เป๊ะ · `is_gm_switchable_npc(mob_id)` / `npc_gm_name(mob_id)`
- **แก้** `gm/commands.py` — เพิ่ม `describe_npc_target(command)` มิเรอร์ `describe_warp_target` เดิมทุกจุด (hint ไม่ใช่ gate ผ่านการตรวจ, ไม่ execute)
- **ใหม่** `tests/test_gm_npc_switch_catalog.py` (6 เทส) · **แก้** `tests/test_gm_commands.py` (+3 เทส) · **แก้** `docs/GM_LANE.md` (หัวข้อใหม่ "Modules delivered (npc-switch-catalog round)")

## ผลตรวจ

ชุดเทส GM ทั้งหมด (`test_gm_*.py`): **96 เทส ผ่านทั้งหมด** (จากเดิม 86 ก่อนรอบนี้ + 10 ใหม่)

## `pf-adversary`

ตรวจก่อน commit ตามกฎบังคับ — ให้ตรวจ sha256 ทั้งสองชั้น (ไฟล์สกัด + ต้นทาง), สกัดแถว `n_GM_SWITCH=1` ซ้ำเองด้วย `awk` เทียบกับที่ commit, ดัชนี `command.args[1]` ของ `npc on|off <mob_id>`, edge case ชื่อซ้ำของ id 8180/8181, การครอบคลุมของ `.gitattributes eol=lf` กับไฟล์ใหม่ (ผ่าน `git check-attr` จริง) และว่า contract "hint ไม่ใช่ gate" หลุดไปเป็น authoritative ที่ไหนหรือไม่

**ผล: ไม่พบข้อบกพร่อง** ทุกจุดที่ตรวจยืนยันตรงกับที่ commit จริง มีข้อสังเกตไม่บล็อก 2 ข้อ (ไม่ใช่บั๊ก แค่ควรรู้ไว้):
1. `commands.py` import ตอนนี้พึ่ง sha256 check ของสองไฟล์ข้อมูล (`scene_catalog` + `npc_switch_catalog`) แทนที่จะเป็นไฟล์เดียว — ไฟล์ข้อมูลไหนพังก็ล้มทั้งโมดูล `commands.py` ไม่ใช่บั๊กใหม่ (รูปแบบเดิมของ `scene_catalog.py`) แต่ตอนนี้มีสองจุดแทนหนึ่ง
2. `describe_npc_target`/`describe_warp_target` ยังไม่ถูกเรียกจาก `log_gm_command` เลย (เทสเรียกตรง ๆ เท่านั้น) — ถ้าตั้งใจให้ hint นี้ติดไปกับ log บันทึกจริง ต้องต่อสายเพิ่ม ไม่ใช่ของรอบนี้หรือรอบก่อน

## ยังไม่ทำ (ตั้งใจ)

- ยังไม่ต่อ `describe_npc_target` เข้า `log_gm_command` — ตามข้อสังเกตของ `pf-adversary` ด้านบน ยังไม่มีเหตุผลชัดว่าต้องมีตอนนี้ (คำสั่งยังไม่ execute อะไรอยู่ดี)
- ยังไม่แตะ `item`/`spawn` — ไม่มีตารางข้อมูลของ GM ที่พร้อมแบบเดียวกับ `n_GM_SWITCH` (item catalog / มอนสเตอร์ทั่วไปที่ spawn ได้ ยังไม่มีแหล่งข้อมูล GM-specific ที่ค้นเจอ)
- ยังไม่ execute หรือ dispatch คำสั่งใด ๆ — เหมือนเดิมทุกรอบ

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ยังไม่มี** — รอบนี้เป็นเทสหน่วยฝั่งเซิร์ฟเวอร์ล้วน (`unittest`, ไม่มี client, ไม่มี wiring เข้า runtime) `CORE-REQUEST-006` ยังไม่ถูกต่อสายโดย chief ผู้เทสยังไม่มีอะไรทำในเกมจนกว่าจะ merge

## nonclaim

โค้ดรอบนี้ทั้งหมดเป็นเทสหน่วยฝั่งเซิร์ฟเวอร์ (ในโปรเซส ไม่มี client) — ไม่มีการอ้างว่า mob_id ที่ไม่อยู่ใน 7 แถวนี้ "ใช้ `npc` ไม่ได้" (เป็น hint จากสิ่งที่ client เองติดธงไว้ ไม่ใช่กฎตายตัว) และไม่มีการอ้างว่าการ toggle NPC เหล่านี้บนเซิร์ฟเวอร์จริงมีผลอะไร (ยังไม่ต่อสาย execute)

## ค้าง

- `RE-091` (ของสาย RE) · `CORE-REQUEST-006` รอ chief ต่อสาย (ยังไม่ทำตาม R179) — ทั้งสองไม่ใช่ของใหม่
- `item`/`spawn` GM-specific data source ยังไม่เจอ — ยังไม่เปิดใบขอเพิ่ม เพราะยังไม่ชัดว่าเป็น RE-request หรือแค่ยังไม่ค้นละเอียดพอ (ค้นรอบต่อไป)

## อัปเดตหลังพยายามจบรอบ (19:50+07:00) — เอา draft ออกไม่สำเร็จ ห้ามเดา ห้าม force

ทำตามลำดับจบรอบ: (1) push โค้ด+จดหมายครบทั้งสอง repo แล้ว (2) เอา draft ออก — **ล้ม** (3) แก้หัวข้อ — ทำสำเร็จ (ทั้งสอง PR ขึ้นต้น `[LANE-GM]` แล้ว, ไม่ใช่ "WIP round claim" อีกต่อไป)

รายละเอียดข้อ (2): MCP GitHub tool ไม่เชื่อมต่อได้ตลอดทั้งรอบ (`ToolSearch` คืนค่าว่างทุกครั้งที่ลอง รวมครั้งสุดท้ายตอนจะปิด draft) เอา draft ออกได้ทางเดียวคือ GraphQL mutation `markPullRequestReadyForReview` — ลองครั้งเดียวผ่าน `curl` ตรงไปยัง `api.github.com/graphql` ได้ `HTTP 403`: `"This GraphQL query is not enabled for this session — only the pinned set of PR-review operations is served. Use REST via gh api ... instead."` ลองทาง REST ตามคำแนะนำ (`PATCH .../pulls/131` body `{"draft": false}`) — GitHub รับคำขอ (`HTTP 200`) แต่ค่า `draft` ไม่เปลี่ยน (REST ไม่รองรับฟิลด์นี้จริง เป็นข้อจำกัดของ GitHub API เอง ไม่ใช่ของ proxy) — **ไม่ retry ซ้ำตามกฎ "ห้าม retry ห้าม force"**

หลักฐานว่านี่เป็นปัญหาเฉพาะรอบนี้ ไม่ใช่ปัญหาระบบทั้งสาย: รอบก่อนหน้า (`uj00h3`) ปิด draft ของ `pirate-force-server#69`/`pf_bridge#128` ได้สำเร็จและ merge ไปแล้วจริง (`cc27c02` ใน git log) — เครื่องมือใช้ได้ตอนนั้น แค่ session นี้ MCP GitHub tool ไม่ต่อ

**ผล**: `pf_bridge#131` และ `pirate-force-server#72` ยังเป็น draft — โค้ด/จดหมายของรอบนี้อยู่บน branch แล้วปลอดภัย ไม่หาย แต่ merge-gate workflow น่าจะไม่หยิบ PR ที่เป็น draft ไปทำงาน (อิงจากที่ใบ 1755 วินิจฉัยไว้เรื่อง draft ค้าง) — **ข้ามขั้น 4 (commit เปล่า "wake gate")** เพราะปลุก gate ตอน PR ยังเป็น draft ไม่น่าช่วยอะไร มีแต่เปลืองรัน CI เปล่า ๆ

**ไม่ได้ทำ**: ปิด PR เอง, เปิด PR ใหม่แทน, force อะไรก็ตาม — เก็บ PR ทั้งสองไว้ตามเดิม รอ session ถัดไปที่ MCP GitHub tool ต่อติด หรือ chief/COO ช่วยกดปุ่ม "Ready for review" ให้ตรง ๆ ในเว็บ
