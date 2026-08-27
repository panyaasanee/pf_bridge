[ถึง: **COO (รอบคลาวด์)** · **chief / สาย E** · สาย A · สาย B · Panya | จาก: **มือเขียนแทน Panya (เซสชัน attended [กะ1])** · 2026-08-26T15:00+07:00 · คำสั่งเจ้าของ: *"ดูให้หน่อยตอนนี้องค์กรเรามีปัญหาตรงไหนไหม งานคอขวดตรงไหน … ฉันไม่ต้องการปัญหาเงียบมาประทุ"*]

# ORG-AUDIT 15:00 — **เลน production 10 ใบ · ต่อสายเข้ารันไทม์ 0 ใบ** · คอขวดคือ "chief เป็นจุดต่อสายเดียวและได้รอบละครั้งต่อชั่วโมง" · บวก flow defect 2 ข้อที่วัดได้

## ① ตัวเลขที่วัดจาก `main` (`40969a65` · 14:5x)
| วัด | ค่า |
|---|---|
| `scenarios/*.json` ที่ `production_allowed=true` | **10 / 54** (combat_aggro · combat_death · combat_first_hit · combat_loot · combat_pickup · field_mobs_hostile · world_population_full · world_scene_density · world_scene_registry · world_travel_gates) |
| โมดูลของสาย A/B ที่ถูก **import หรือเรียก** จาก `runtime.py`/`app.py` | **0** — `field_mobs` `mob_aggro` `mob_combat` `mob_death` `mob_loot` `mob_pickup` `mob_ai_control` `field_mob_ai_tables` `world_travel_gate` `world_scene_entry` `world_scene_liveness` `world_density` `world_population_handoff` = grep 0 hit ทุกตัว |
| สิ่งเดียวที่ต่อสายแล้ว | สำมะโน `world_population` (R173 → `#56` 12:28) |
| สาย A รอบล่าสุด | **3 รอบติด (12:50 · 13:52 · 14:29) "ยังบล็อกที่ CORE-REQUEST-003/004"** = รอ chief ต่อสายประตูออกเมือง |
| กำหนด M2 | **23:59 คืนนี้** — ถ้า chief ไม่ต่อสาย 003/004 ในรอบ 14:51 หรือ 15:51 M2 เลยแน่ |

🔴 **นี่คือปัญหาเงียบที่เจ้าของกลัว:** ตัวชี้วัดรอบผู้บริหารของ COO นับ `production_allowed` (10) ซึ่งขึ้นทุกชั่วโมง แต่ผู้เล่นเข้าเกมแล้ว **เห็นของใหม่ 0 อย่าง** (ยกเว้นเมือง 115 ที่เจ้าของปฏิเสธไปแล้ว) · สาย B ผลิตโมดูลไปแล้ว 7 ใบที่ไม่มีใครเรียก

**ขอ COO:** เพิ่มตัวชี้วัด **`WIRED = จำนวนโมดูลเลน production ที่ `runtime.py`/`app.py` import`** ข้าง `production_allowed` ทุกรอบผู้บริหาร · `WIRED` ไม่ขยับ 2 รอบ chief ติดกัน = escalation สาย E อัตโนมัติ

## ② flow defect A — **chief ติดล็อกตัวเอง 6 ชม. ทุกครั้งที่เอา draft ออกหลัง push สุดท้าย (รีโปเซิร์ฟเวอร์)**
วัดจาก `#57` R175: push สุดท้าย 13:24 → gate จบ 13:25 → `decide` เห็น PR ยังเป็น draft ⇒ ข้าม → chief เอา draft ออก + แก้หัวข้อ 13:51 → **ไม่มีอะไรปลุกอีก** เพราะ `merge-claude-pr` ฝั่งเซิร์ฟเวอร์ตื่นด้วย `workflow_run` เท่านั้น (`edited` ไม่ปลุก — ต่างจาก `pf_bridge`) ⇒ ค้างจน reaper 6 ชม. · มือเขียนแทน re-run gate 14:45 → merge 14:49 · **ถ้าไม่มีใครปลุก รอบ 14:51 ของ chief จะจบทันทีเพราะ "ติด `#57`"**
ลำดับ "push → เอา draft ออก → แก้หัวข้อ" ใน prompt §3 **ถูกสำหรับ pf_bridge แต่ผิดสำหรับรีโปเซิร์ฟเวอร์**
**ทางแก้ 2 ชั้น:** (ก) prompt chief §3: หลังเอา draft ออก+แก้หัวข้อ **push commit เปล่าหนึ่งใบ** (`wake gate`) ให้ gate รันตอน PR พร้อม merge — ราคา gate 1 รอบ (~5 นาที) แลกกับไม่ค้าง 6 ชม. · (ข) chief แก้ `.github/workflows/merge-claude-pr.yml` ฝั่งเซิร์ฟเวอร์ให้ `decide` ตื่นเพิ่มจาก `pull_request_target: [ready_for_review, edited]` แล้วอ่านคำตัดสินจาก `ci-status` ของ head sha (ยังคงความปลอดภัยแบบเดียวกับ pf_bridge) — (ก) ใช้ได้ทันที (ข) ถาวร

## ③ flow defect B — **โหมดเล่นของเจ้าของได้เมือง 3 ตัว**
`PLAY_PIRATE_FORCE.bat` → `staged\9001_play_boot.ps1` ใส่ `--second-password-mode bypass` · `runtime.py:771` (R173) ปิดสำมะโนเมื่อ bypass ⇒ เจ้าของกดเล่นเองไม่มีวันเห็นของที่ M1 ทำ · ทางแก้: เอา bypass ออกจาก 9001 (รหัสผ่านขั้นสองจะโผล่เฉพาะตอนลบตัวละคร/เปิดกระเป๋า พิมพ์อะไรก็ผ่าน — เจ้าของยืนยันเอง) หรือ chief เปลี่ยนกฎกักกัน — **รอเจ้าของเลือก**

## ④ ของที่ดีแล้ว (ไม่ต้องแตะ)
COO ตอบภายในรอบทุกใบ (12:46/12:47/12:48/14:42) · `_BRIDGE_HEARTBEAT.txt` มีแล้ว (14:42 OK) · sync/watchdog เขียว · Actions กลับมาหลัง public · สาย B เดินต่อเนื่อง (#53 #55 #58 #59) · reaper ปิด `#54` ที่ซ้ำกับ `#56` ถูกต้อง

## ⑤ ยังค้าง (ไม่เร่ง แต่ห้ามลืม)
reap ไม่ปิด PR ไม่มีมาร์กเกอร์ (immortal lock) · กฎ ⑤-1 ลง AGENTS.md · band fix 0x2073→0x2095 · gate รันซ้ำ 2 ครั้งต่อ push (event `push` + `pull_request`) — ฟรีแล้วตอน public แต่ช้า 2 เท่า chief พิจารณาตัด `push` สำหรับกิ่ง `claude/*`

nonclaims: "0 wired" วัดด้วย grep ชื่อโมดูลใน runtime.py/app.py เท่านั้น — ถ้ามีการ import ทางอ้อม (เช่นผ่าน world_population) จะนับพลาด แต่ 13 ชื่อ 0 hit ทั้งหมดไม่น่าใช่ความบังเอิญ · ไม่ได้ตรวจว่าโมดูลของสาย B ทำงานถูกหรือไม่ แค่ว่าไม่มีใครเรียก
