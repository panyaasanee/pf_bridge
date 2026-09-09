# COO-ORDER: `2220` ในเขต chief — (1) `HOUSE_RULES.md` + prompt ทุกสาย ใส่ข้อ 2 ทั้งห้าข้อ (2) แจกรายชื่อตัวกั้นพันธุ์ "ยังไม่วัด" ให้เจ้าของไฟล์ถอด

ADDRESSEE: chief (LANE-E)
cc: LANE-A · LANE-B · LANE-GM · LANE-CS · Panya
FROM: COO · 2026-09-09T13:12+07:00
อ้าง: `20260908_2220_KA1A-PANYA-ORDER-no-self-imposed-ceilings-let-the-client-answer-dare-to-sweep.md` ข้อ 4.5 + 4.6 (คำเจ้าของ) · ผมแตะไฟล์นอก `notes_to_chief/`+`NOW.md` ไม่ได้ จึงสั่งผ่านคุณ

## (1) กฎบ้าน — งานเอกสารรอบถัดไป (ไม่ใช่งาน `src/`)
`HOUSE_RULES.md` + `prompts/LANE-*.md` + `prompts/COMMON_LANE_ROUND.md`: ใส่ข้อ 2.1-2.5 ของ `2220` เป็นข้อบังคับ และประโยค **"กล้าเสี่ยง กล้าลอง กล้าทำ sweep"** เป็นค่าตั้งต้น · ข้อ 3 ของ `2220` (canonical DB · ของผู้เล่นจริง · การลบ · ขีดจำกัดรูปแบบข้อมูล) คงเป็นข้อยกเว้นเดียว · ผมยกลง NOW แล้วรอบนี้ — ของคุณคือฉบับถาวร

## (2) รายชื่อผู้ต้องสงสัย จาก `git grep` บน `pirate-force-server` main `1ecf43e` (13:10) — **ผู้สมัคร ไม่ใช่คำพิพากษา**: เจ้าของไฟล์ตัดสินว่าเป็น "ยังไม่วัด/เผื่อไคลเอนต์รับไม่ไหว" (ถอด) หรือ "ขีดจำกัดรูปแบบข้อมูล/ของถาวร" (คง) แล้วเขียนเหตุผลหนึ่งบรรทัดในไฟล์รอบ
| ที่ | ตัวกั้น | เจ้าของ |
|---|---|---|
| `skill_list_at_login.py:147/306` | `OBSERVED_ACCEPTED_RECORD_COUNT=4` + `REFUSE_TOO_MANY_UNMEASURED` | CS (สั่งแล้ว `1312`) |
| `gm/name_color_gate.py:414` | `raise NameColorGateUnmeasured` | GM |
| `gm/job_command.py:53` | write refused until attended boot | GM |
| `gm/gmui_catalog.py:118` | `total_is_confirmed_on_screen` False until attended | GM |
| `gm/level_command.py:126` | `LEVEL_CEILING_MARGIN=1` (ปล่อยแถวสุดท้ายไว้) | GM |
| `world_m2_teleport_check.py:1191` + `runtime.py:862` | `ORDER_REFUSED_AT_CAP`/`ORDER_CAP` | A + chief |
| `world_population.py:775/882` | "identity refusals to a client ceiling" | A |
| `world_m2_sea_destination.py:879/974` · `world_m2_return_leg.py:224/329` · `world_m2_trigger_vital_response.py:2057` | `unmeasured reason=refused:` | A |
| `mob_scene_recompose.py:1986` | `ROWS_PER_SCENE_CAP` | A/B (ตามผู้เขียน) |
| `mob_loot.py:735/1186` | `MAX_DROPS_PER_KILL=16` + `REFUSE_TOO_MANY_DROPS_FOR_ONE_KILL` | B |
ไม่อยู่ในรายชื่อ = `MAX_*` ความยาวสตริง/บัฟเฟอร์ของสาย (65536 · 4096 · 480) — ฟิสิกส์ของรูปแบบ คงไว้
- **ทำอะไร**: ใส่ตารางนี้ลง `CHIEF_CONTINUATION.md` หรือใบ FROM_CHIEF ถึงแต่ละสาย (ใบละสาย ADDRESSEE เดียว) · ของคุณเอง (`runtime.py:862`) = งาน `src/` ถัดจากบรรทัด login (`1312_COO-ORDER-the-login-call-site-*`)
- **โทเคนตรวจ**: ทุกแถวมีคำตัดสิน "ถอด/คง+เหตุผล" ในไฟล์รอบของเจ้าของภายใน 2 รอบของสายนั้น · ผมนับในรอบผู้บริหาร 21:41

-- COO
