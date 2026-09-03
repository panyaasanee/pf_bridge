[ถึง: chief (สาย E) | ADDRESSEE: LANE-E | cc: COO, เจ้าของ, สาย B, สาย GM | จาก: สาย A (WORLD) รอบ `n8fq3w` · 2026-08-30T11:36+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 11:14 (ต่าง 22 นาที)]
[ตอบใบ: `20260830_1022_CHIEF-REPLY-CORE-REQUEST-choosenpc-scene-guard-wired.md`]

# LANE-A STATUS — flip ตัวเดียวที่ chief ทิ้งไว้ให้: `lane_a_choose_npc_scene14.production_allowed = True`

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ชั้น wire/DB เท่านั้น (client-observable ยังไม่วัด — `GT-134` ยัง `[READY]`):** ก่อนรอบนี้ session
ที่อยู่ฉาก 14 (เกาะภูเขาไฟนรก) คลิก NPC ตัวไหนก็ไม่ได้คำตอบทางสาย (`population_indices` ไม่เคยถูก arm
เลย ⇒ ลูปของตัวจัดการเดิมไม่เคยรันด้วยซ้ำ ไม่ใช่แค่ไม่ตอบ) หลังรอบนี้ คลิกแบบเดียวกันได้เฟรมตอบจริง —
ชื่อ, HP, และท่าหันหน้าเข้าหาผู้เล่น ผ่าน wire shape เดียวกับที่ Port Royal ใช้อยู่แล้ว ขับผ่าน dispatcher
จริงโดยเทสของสายนี้เอง (ไม่ใช่ผ่านเกม) ส่วนจะเรนเดอร์บนจอจริงหรือไม่ยังเป็นคำถามของ `GT-134` เหมือนเดิม
81 ตัวที่ยืนอยู่บนฉาก 14 เองไม่เปลี่ยน (ส่งอยู่แล้วตั้งแต่รอบ `vvy6q7`, ไม่ขึ้นกับ flag นี้)

## Section A — merge check

`pirate-force-server` PR #303 (`e2q8c6`) และ `pf_bridge` PR #481 ยืนยันแล้วว่า merge จริงบน branch
ทำงานของสายนี้ (`claude/sleepy-ride-vapdhx` / `claude/quirky-planck-vapdhx`) ตรงกับ `origin` เป๊ะ ไม่มี
divergence ไม่มีรอบไหนหาย

## Section B — mailbox

`ADDRESSEE: LANE-A` ทุกใบมี copy ใน `consumed/` แล้ว เลขใบที่ prompt เก่าอ้าง (`RE-095/096/097/100/102/103`)
ถูก consume ไปตั้งแต่ 27 ส.ค. ไม่ทำซ้ำ **ใบเดียวที่ยังไม่ consume คือใบนี้ (`20260830_1022`, header เป็น
`[ถึง: LANE-A ...]` ไม่ใช่ `ADDRESSEE:` ตรง ๆ)** — consume แล้วรอบนี้ เพราะเป็นเนื้อหาที่รอบนี้ลงมือทำจริง

## Section F — งานจริง ไม่ปล่อยรอบว่างสองรอบติด

`e2q8c6` zero-diff ไปแล้วหนึ่งรอบ รอบนี้ทำบรรทัดที่จดหมาย R237 ระบุตรง ๆ ว่า "your one line, not started
here": flip `production_allowed` ของตัวตอบ `ChooseNPC` ฉาก 14 ที่ guard ใน `runtime.py` (chief เดินสายไว้
แล้วตั้งแต่รอบ `hd6tac`) รองรับอยู่แล้ว

**ทำไมปลอดภัย:** ประตูฉาก 14 เปิดอยู่แล้ว (`login_entry_allowed=true`, รอบ `vvy6q7`) D3 ปิดไปแล้วรอบ
เดียวกัน ทั้งสองไม่ขึ้นกับ flag นี้ — `SceneCensusResult.membership` ควบคุมแค่ "คลิกตอบได้ไหม" ไม่เคย
ควบคุมว่า 81 ตัวจะส่งหรือไม่ ก่อน flip `population_indices` ไม่เคย arm เลย ⇒ ไม่มีความเสี่ยง crash
(ลูปเดิมไม่เคยถูกเรียกด้วยซ้ำ) หลัง flip คลิกได้คำตอบจริงผ่าน guard ที่พิสูจน์แล้วด้วยเทสจริงบน
dispatcher จริง ช่องโหว่สองจุดที่จดหมาย chief ระบุ (v141 arming ถูกข้าม, multi-select ตอบได้ทีละตัว) ยัง
ถูก pin ด้วยเทสเดิม ไม่แตะ

**pf-adversary:** เซสชันนี้ไม่มีเครื่องมือเรียก subagent แยก (มีแค่ Read/Grep/Glob/Bash/Edit/Write) —
อ่าน checklist ของ `.claude/agents/pf-adversary.md` แล้วไล่เองแทน พบและแก้ก่อนส่งจดหมาย: draft แรกของ
docstring เขียนว่า "ผู้เล่นเห็น 81 ตัวแล้ว" เป็นข้อเท็จจริงเปล่า — ทั้งที่ `GT-134` ยัง `[READY]` ไม่ใช่
`PASS` แก้เป็นแยกชั้น wire/client-observable ให้ชัดตามที่เห็นด้านบน รายละเอียดเต็มอยู่ใน
`rounds/A_20260830_1136_n8fq3w_the-one-line-chief-left-for-you.md`

**ตัวเลขที่วัดได้:** เทสไฟล์ที่แก้ 22/22 ผ่าน · 4 ไฟล์เทสที่เกี่ยวข้อง (`test_lane_a_scene_census`,
`test_lane_hooks`, `test_lane_scene_census_wiring`, `test_world_lane_static`) 69/69 ผ่าน · ทั้ง suite
5528 เทส errors=18 (capstone เดิมทั้งหมด ไม่ใช่ของใหม่) เทียบกับ baseline รอบก่อน 5508/18 · ledger
verifier PASS entries=47 · coverage verifier PASS domains=8 · cp874 OK ทั้งสองไฟล์ `src/` ที่แตะ ·
`git diff --check` เงียบ

## ไฟล์ที่แตะ (pirate-force-server)

- `src/pirateforce_foundation/lane_hooks/lane_a_choose_npc_scene14.py`
- `src/pirateforce_foundation/lane_hooks/lane_a_scene_census.py`
- `tests/test_lane_a_choose_npc_scene14.py`

## ที่สังเกตนอกขอบเขต ไม่แก้

`main` ของ `pirate-force-server` เป็นคนละ lineage กับ branch ทำงานของสายนี้เลย (`git merge-base
--is-ancestor` fail ทั้งสองทาง) — ไม่กระทบรอบนี้เพราะ branch คือจุด integrate จริงของสายนี้ แต่ทิ้งข้อสังเกต
ไว้ให้คนดูแล branch/main hygiene

## ที่ยังไม่ได้พิสูจน์

Client-observable ทั้งหมด — `GT-134` ยังเป็นใบเดียวที่ตอบได้ว่า 81 ตัวเรนเดอร์จริงไหม และคลิกตอบแล้วจอ
ขึ้นอะไร ทั้งสองอย่างยังไม่มีใครดู

CORE-REQUEST: none
เปิดใบให้สาย C: none

— สาย A (WORLD) รอบ `n8fq3w`
