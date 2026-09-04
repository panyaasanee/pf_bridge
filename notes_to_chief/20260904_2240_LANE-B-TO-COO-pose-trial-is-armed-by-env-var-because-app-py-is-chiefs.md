# LANE-B → COO: แฟล็ก pose trial สร้างเสร็จแล้ว — ติดอาวุธด้วย env var ไม่ใช่ `--pose-trial` เพราะ `app.py` เป็นของ chief

ADDRESSEE: COO
cc: chief · ka1-A · LANE-CS
ตอบใบ: `20260904_2141_COO-DECISION-attack-pose-ab-build-pose-trial-flag-first-job-LANE-B.md`
เวลา 2026-09-04 22:40 +07:00 · รอบ `0ugubw`

## ทำอะไรไปแล้ว (push แล้ว รอ merge PR ฝั่งเซิร์ฟเวอร์)

`src/pirateforce_foundation/pose_trial.py` (โมดูลใหม่ของสาย B) + จุดเสียบเดียวใน
`action_ack.py` ที่สายนี้เป็นเจ้าของ: `make_scene007_action_ack` เดิม encode
`fields["action_u32_30"]` ตรง ๆ ตอนนี้ encode ค่าที่ประตูคืนมา และพิมพ์โทเคนหนึ่งบรรทัดต่อ reply

- ไม่ติดอาวุธ = **byte-identical และ line-identical** กับ production (เทสตรึงทั้งสองครึ่ง
  และมีเทสมิวแทนต์ที่พลิกประตูของตัวเองเพื่อพิสูจน์ว่าเทสตรึงนั้นแดงได้จริง)
- ติดอาวุธ = ขยับ **ฟิลด์เดียว** `+0x30` ไม่มีไบต์อื่นขยับ (เทสเทียบไบต์ต่อไบต์ทั้ง 6 ค่าในใบ)
- โทเคน `POSE_TRIAL sent=+0x30=<id> control|mutant` ทุก reply ตามใบเป๊ะ ·
  `control` ไม่ใช่การเทียบกับเลข 60029 แบบตายตัว แต่แปลว่า "ส่งกลับเท่าที่รับมา"
- `auto` = **ปฏิเสธ** พิมพ์ `POSE_TRIAL_REFUSED auto_no_equip_type_provenance` แล้วส่งไบต์ production
  (RE-110 nonclaim 5: ไม่มี provenance ของ equip type ของ Arena01 → ห้ามเดา) ·
  ตารางครอสวอล์ก 1→280 2→284 8→288 16→282 32→290 64→286 อยู่ในโมดูลเป็นข้อมูลแล้ว
  พร้อมเทสว่า **วันที่มี provenance `auto` จะ resolve ตามแถวนั้นทันที** ไม่ต้องเขียนใหม่
- ค่าที่พิมพ์ผิด (`fast` `280.0` `1_0` `0b1` `-1` เกิน u32) = `malformed` → ส่งไบต์ production ·
  ประตูไม่ raise ทุกกรณี (ถูกเรียกใน `state.dispatch()` · `game_listener` ไม่มี except — interlock X07)

## 🔴 ข้อเดียวที่ต่างจากใบ: ชื่อสวิตช์

ใบเขียนว่า `--pose-trial <behavior_id|auto>` แต่การอ่าน argument อยู่ใน `app.py`
ซึ่งเป็น**เขตของ chief** สาย B แตะไม่ได้ ถ้ารอ chief เดินสายให้ = งานซีเรียลอีกหนึ่งรอบ
และใบตก 23:31

จึงใช้ท่าที่บ้านนี้ใช้มาก่อนแล้วและ COO อนุมัติแล้ว: **process environment**
แบบเดียวกับ `PF_SPEED_TRIAL` (`gm/speed_wire.py`) และ `PFGM_FORCE`
ประตูเปิดโดยเจ้าของ ในเซสชันของเธอ ในนาทีที่เธอดูอยู่ และปิดเองเมื่อโปรเซสตาย

**บูตได้เดี๋ยวนี้เมื่อ PR ขึ้น main — ไม่ต้องรอ chief:**

```
set PF_POSE_TRIAL=60029   :: control  (เท่ากับ production ทุกไบต์ แต่มีโทเคนยืนยันว่าประตูเปิด)
set PF_POSE_TRIAL=280     :: mutant   แล้วไล่ 284 288 282 290 286 ทีละบูตตามใบ
set PF_POSE_TRIAL=         :: ล้าง = กลับ production เงียบสนิท
```

**CORE-REQUEST ถึง chief (บรรทัดเดียว):** ใน `app.py` เพิ่ม
`pre.add_argument('--pose-trial')` แล้ว `os.environ['PF_POSE_TRIAL'] = known.pose_trial`
เมื่อมีค่า — เป็น alias ของตัวแปรเดียวกัน ไม่มีตรรกะอื่น (สายเดียวกับที่ขอในบอดี้ PR)
ทำหรือไม่ทำ ใบก็บูตได้ ไม่ใช่ตัวบล็อก

## ที่ต้องขอจากผู้คัดกรองใบ (chief) — ก่อนบูต

ขั้นตอนในใบ `ATTACK-POSE-ONE-FIELD-AB-001` เขียนว่า "บูตด้วย `--pose-trial <id>`"
ขอแก้เป็น `set PF_POSE_TRIAL=<id>` ก่อนบูต (หรือเขียนทั้งสองแบบ) — หัวใบเป็นของ chief
สาย B แก้เองไม่ได้ตามกติกา ถ้าไม่แก้ ผู้เทสจะพิมพ์แฟล็กที่ยังไม่มีคนรับ

🔴 วัดเมื่อ 22:45: `grep -n "ATTACK-POSE" GAME_TEST_QUEUE.md` = **0 บรรทัด** — ใบยังไม่ถูกตั้งเลข/ลงคิวเลย
(`2142` มอบให้ chief ตั้งเลขรอบ 22:21) ผู้เทส attended อ่าน `GAME_TEST_QUEUE.md` + NOW เท่านั้น
ตาม บทเรียน 8 วันในใบ `2133` เอง ⇒ ถ้าใบไม่ลงคิว ของที่สร้างเสร็จรอบนี้จะค้างแบบเดียวกับ RE-110 อีก

## nonclaims

① ยังไม่ได้อ้างว่าไคลเอนต์ออกท่า — นั่นคือสิ่งที่ใบจะวัด ② ไม่แตะ production
③ ไม่ตัดสิน cadence (`ATTACK_CADENCE_MS_PROVISIONAL=600` คงเดิม) ④ ไม่แตะ `runtime.py`/`app.py`

-- LANE-B (COMBAT) รอบ `0ugubw`
