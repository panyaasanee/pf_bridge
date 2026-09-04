# KA1A-R314-RESULTS — GT-247 = NOT-EXERCISED (เซิร์ฟไม่เคยตอบ ActionVital: เกต TargetVital ต้อง vital_count==1 แต่ client ส่งพ่วง TargetPos) + 🔴 หัว main บูต scene-load scenario ไม่ได้ตั้งแต่ 17:51Z (class_id backfill ก่อน migrate)
ADDRESSEE: chief
cc: LANE-B (เจ้าของใบ) · LANE-DB · COO · ka1-B (ระบบ: ข้อ 3)
ผู้เขียน: ka1-A (ผู้เทส attended · Panya ขับ UI เอง) · เวลา 2026-09-05 02:33 +07:00 (ประมาณ)

## 0. ทำไมไม่บูตตามใบ (ถอดหัวใบก่อนเรียก Panya — Panya เคาะทางเบี่ยงเอง 02:2x)
ใบ GT-247 สั่ง "บูตไร้ธง + `set PF_POSE_TRIAL=<id>` แล้วคลิกตีมอน" — แต่ในโค้ด `pose_trial.selector_for_reply` ถูกอ่านที่เดียวคือ `action_ack.make_scene007_action_ack` ซึ่งเรียกจาก `runtime.py` เฉพาะใต้ `--scene-load-scenario` ที่มี `action_ack` และ**ยิงครั้งเดียวต่อ process** (latch `scene_action_ack_sent`) · ทางตีมอน production (`_dispatch_mob_combat`) **ไม่ส่ง ActionVital ตอบเลย** (ส่งแต่ `MOB_COMBAT_BAR`) ⇒ บูตตามใบ 7 รอบ = ไม่มีอะไรเปลี่ยนแน่นอน (docstring `pose_trial.boot_banner` ของ LANE-B เขียนเตือนไว้เอง: "An operator who arms the variable and boots without the scenario … sees a console byte-identical to an unarmed boot") — ใบไม่ได้บอก = กับดักแบบ GT-184/186 ครั้งที่ 3
Panya เลือก: ลอง 1 บูตด้วย `--scene-load-scenario scenarios\port_royal_fighting_fish_soldier_hp3857_player_faction1_ea7d_ack.json` + `PF_POSE_TRIAL=280` (ค่าเดียว)

## 1. รอบ R314 (02:22-02:31)
- 1514 บูตหัว main (`c8280a63`, เขียว) → **เซิร์ฟตายตอนเปิด** `sqlite3.OperationalError: no such column: class_id` ที่ `app.py:802 persistence_class_id_backfill.backfill_missing_class_ids` (ดู §3) → abort สะอาด
- 1514c บูต **`f2a62bf0`** (เขียว · บิลด์เดียวกับ R312 · มี pose_trial · ก่อน backfill) + scenario + env=280 → ขึ้น · `POSE_TRIAL_BOOT` banner ไม่ปรากฏใน `server_console_live.out.txt` เพราะพิมพ์ตอน import ก่อน tee (ไม่ใช่หลักฐานว่าไม่ armed — R313 พิสูจน์แล้วว่า env ตกทอดถึงลูก) · run DB `run_gt247_20260905_022735` · canonical ไม่เปลี่ยน
- Panya: เข้าเกม → เดิน → มอน Fighting Fish soldier โผล่ (`[G>] SCENE2_P60_MOBS34_HP3857_INITIAL` 229 B) → เดินไปชิด → คลิกเลือก → คลิกตี หลายครั้ง → **"ไม่มีใครออกท่าใด ๆ ทั้งนั้น"** (OBSERVER_CONFIRMED 2026-09-05T02:31+07:00)

## 2. wire — ทำไมเซิร์ฟไม่ตอบ (วัดแล้ว ไม่ใช่เดา)
- client ส่ง #28 **TargetVital 60 B = 2 vital ในเฟรมเดียว** `[TargetVital kind 1 target 0x203D] + [TargetPos]`:
  `12 6F 6E 14 00 00 00 00 08 00 0B 02 12 02 00 12 DD 1A 0B 00 32 3D 20 00 00 00 00 00 00 08 01 12 90 2A 0B 00 2A F2 4A BB 44 2A CB F1 8F C4 2A 00 80 68 44 2A 0E 83 2E 3F 0B 01 0B 00`
- เกต `scene_object.is_scene_remote_hostile_target` ต้อง **`parsed.vital_count==1`** (TargetVital เดี่ยว) → ไม่ผ่าน → `scene_hostile_target_captured` ไม่เคยเป็นจริง → `make_scene007_action_ack` ไม่ถูกเรียก → **ไม่มี `POSE_TRIAL sent=` / `SCENE007_EA7D_ACTION_ACK_ONCE` เลย** (EVID = 0 ทั้งคู่)
- ส่วน ActionVital ของ client มาถูกทรงทุกอย่าง: #28 113 B = `[ActionVital, TargetPos]` (= SCENE-006 shape เป๊ะ) target `0x203D` action `+0x30 = 7D EA 00 00` (60029) — คือถ้าเกต TargetVital ผ่าน ตัวตอบจะทำงาน · เฟรมถัดมา #29-#35 = ActionVital ซ้ำ 2-7 ตัวในเฟรมเดียว (คลิกรัว) 153/182/498/291 B
- hex เต็มทุกเฟรม: `GameClient\capture_r314_20260905_022735\capture_v141\GT247_hex_windows.txt`
- ⇒ ผล GT-247 = **NOT-EXERCISED** (ไม่ใช่ NEGATIVE: ไม่มี reply ให้ client ตัดสิน) · client วันนี้พ่วง TargetPos กับ TargetVital/ActionVital เกือบทุกเฟรม (เห็นแบบเดียวกันใน R312 CLearnSkill+UserSetting และ R313 chat+UserSetting) — parser ยุคสิงหาที่ยึด "vital เดี่ยว" ใช้กับ client ตอนนี้ไม่ได้

### เสนอ LANE-B (ทางที่ Panya จะได้ผลในบูตเดียว)
ก. ย้ายตัวสลับไปตอบใน **ทาง production** `_dispatch_mob_combat`: เมื่อ armed ให้ echo ActionVital กลับ 1 เฟรมต่อ 1 hit (performer/target/+0x30=ค่าที่ arm) — ทดสอบได้กับมอนจริงทุกฉาก คลิกกี่ครั้งก็ได้ (ตอบคำถาม auto-repeat ด้วย) · ไม่ armed = byte-identical เหมือนเดิม
ข. ถ้าจะคง scene-load: แก้ `is_scene_remote_hostile_target` ให้รับเฟรมหลาย vital (หา TargetVital ในทุก nested) และปลด latch ครั้งเดียว
ค. ระหว่างรอ: หัวใบ GT-247 → **BLOCKED-ON-WIRING** พร้อมเหตุผลข้างบน (ห้ามเรียก Panya จนกว่า ก หรือ ข ขึ้น main)
ง. ทางเลือกลดจำนวนบูต: ให้ค่า arm เปลี่ยนได้ผ่านคำสั่ง GM (`/posetrial <id>`) จะเหลือ 1 บูต 7 คลิก แทน 7 บูต

## 3. 🔴 ระบบ (ka1-B/chief/LANE-DB): หัว main บูต scenario แบบอ่านอย่างเดียวไม่ได้ ตั้งแต่ `7717c747` 17:51Z
- `app.py:802` เรียก `persistence_class_id_backfill.backfill_missing_class_ids(store)` **นอก** กิ่ง `migrate_with_backup()` → scenario ตระกูล scene-load/read-only (ไม่ migrate) ชน `no such column: class_id` บน canonical schema → เซิร์ฟ exit ก่อนฟัง port · บูตไร้ธง/scenario ที่ migrate ไม่โดน (R313 c055dbc6 ผ่าน)
- แก้: ย้าย backfill เข้าไปหลัง `migrate_with_backup()` ทั้งสองกิ่ง หรือ guard ด้วย "มีคอลัมน์ class_id ไหม" · เพิ่มเทส "บูต scene-load scenario บน DB schema เก่า"
- ผลกระทบตอนนี้: ทุกใบ attended ที่ใช้ `--scene-load-scenario` (ตระกูล GT-104/GT-122 เก่า และรอบนี้) บูตหัว main ไม่ได้ · ใบ flagless ไม่กระทบ
- traceback เต็ม: `GameClient\capture_r314_20260905_022237\server_console_live.err.txt`

## nonclaims
- ไม่ตัดสินว่า 280 ออกท่าหรือไม่ (reply ไม่เคยออก) · ไม่ตัดสิน cadence · ไม่แตะ production
- `POSE_TRIAL_BOOT` banner ที่ไม่เห็น = ข้อจำกัดการเก็บ stdout ก่อน tee ไม่ใช่หลักฐาน unarmed (nonclaim ทั้งสองทาง)
- teardown 1515: DB query `hp_current` ล้มเพราะ run DB ใต้ scenario read-only ไม่ถูก migrate (คอลัมน์ยังไม่มี) → exit 36 แม้ตัว teardown จริงผ่าน (listeners 0 · canonical ไม่เปลี่ยน · integrity ok) — template ต้องไม่ assume schema หลัง migrate

## บทเรียนเครื่องมือ
- ก่อนเรียก Panya กับใบที่มี "สวิตช์ทดลอง": ไล่ว่าสวิตช์ถูกอ่านที่ call site ไหน และ call site นั้นเดินได้ในบูตแบบไหน (บทเรียนซ้ำ GT-184/186 → GT-247)
- parser ที่ยึด `vital_count==1` ทุกตัวในโค้ด (grep `vital_count==1` / `vital_count == 1`) ควรถูกทบทวน — client ตอนนี้พ่วง vital บ่อย

-- ka1-A
