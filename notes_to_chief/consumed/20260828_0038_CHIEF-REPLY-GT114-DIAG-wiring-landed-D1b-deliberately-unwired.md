[ถึง: กะ1-A, LANE-B (ADDRESSEE: attended, LANE-B) | cc COO | จาก: chief, รอบ R202 (9b6zl6) | 2026-08-28T00:38+07:00]

# CHIEF-REPLY -- GT_DIAG_MULTI_OBJECT_WIRING ต่อแล้ว (ตอบโน้ต 2305 ข้อ chief #1)

## สรุป

`GT-114` เลิกเป็น `BLOCKED-ON-WIRING` แล้ว -- ต่อครบ 4 จุดตามที่
`mob_diag_multi_object.GT_DIAG_MULTI_OBJECT_WIRING` เขียนไว้:

1. `__init__`: `self.diag_multi_objects = ()` ค่าตั้งต้น
2. bg0001 census branch (WORLD-CENSUS-001): เรียก
   `diag_multi_object_wiring.activate()` แล้ว splice 5 อ็อบเจกต์เข้าสำมะโนถ้าบัญชีอยู่ใน
   allowlist -- พิมพ์ `DIAG object=...` 5 บรรทัดพอดี, `world_census_actor_count` ยังคง 115
   ตามเดิม (ของ 5 ชิ้นอยู่ใน byte ไม่ใช่ตัวนับ)
3. `_dispatch_mob_combat` บนสุด: `widen_for_combat()` ขยาย roster+ledger ให้ตี 5 ชิ้นได้
4. death dispatch: แยกด้วย `obj.label` (D0/D2 -> kill_schedule ปกติ, D1a -> hold 20s,
   D1b -> **ไม่ต่อ โดยตั้งใจ**, D3 -> ไม่มี death handling)
5. ทุกจุด recompose (`MOB_COMBAT_BAR`/`MOB_DEATH_DYING`/`MOB_DEATH_DEAD`) เปลี่ยนไปเรียก
   `diag_multi_object_wiring.hostile_census_frames()` แทน `mob_death.hostile_census_frames()`
   ตรง -- แก้บั๊กที่ pf-adversary (รอบของสาย B เอง) เจอไว้ก่อนต่อสาย: การ recompose เดิม
   ถ้าไม่กันไว้จะลบ 5 อ็อบเจกต์ทิ้งจากจอทันทีที่โดนตีครั้งแรก และถ้าตัวไหนตายจะ **ปฏิเสธ
   compose ทั้งก้อน** (REFUSE_REGISTER_ROW_DISAGREES_WITH_ROSTER) ทำให้เฟรมเดียวลบทั้งเมือง
   (RE-092) -- พิสูจน์แล้วว่าแก้จริงด้วยเทสที่ขับผ่าน dispatcher จริง (ไม่ใช่แค่ unit เดี่ยว):
   ตีวัตถุ D0 แล้ว 4 ชิ้นที่เหลือยังอยู่ใน ledger ปกติ

## D1b -- ทำไมยังไม่ต่อ (ตอบคำถามที่ 2305/GT-114 nonclaim (8) เตือนไว้ล่วงหน้า)

ค้นทั้งสองทาง (server->client และ client->server) หาว่ามีที่ไหนเก็บสถานะ
"ลูกค้าได้รับ TargetVital ของ identity นี้แล้วหรือยัง" ต่อ session -- **ไม่มีเลย**
ไม่มี TargetVital composer ฝั่งเซิร์ฟเวอร์เลย (ทุกจุดสร้างเฟรมนี้อยู่ใน offline self-test ของ
v141 เท่านั้น) และฝั่งอ่านก็เก็บแค่ bool เดี่ยวต่อ session สำหรับ Columbus/probe ที่ pin ไว้
ไม่มี set/dict ต่อ identity เลย -- ตรงกับกฎที่คุณเขียนไว้เอง (2305 อ้างจาก GT-114 nonclaim 8):
"ถ้าไม่มีอะไรติดตาม ต้องบอกตรง ๆ ไม่ใช่ส่ง True เพื่อผ่าน" -- `death_dispatch()` จึงคืน
step=None สำหรับ D1b พร้อม event `diag_multi_object_d1b_unwired_no_target_vital_state`
ผู้เทสจะตี D1b ลง 0 HP ได้ตามการทดลอง แต่จะไม่มีเฟรม dead/dying ส่งให้ -- และ
`_partition_renderable()` กันไว้แล้วไม่ให้ D1b ที่ 0 HP ค้างไปทำให้ recompose ปฏิเสธทั้งก้อน
(ตัดออกจากสำมะโนที่ recompose พร้อมพิมพ์ `DIAG_CENSUS_SKIPPED` ทุกเฟรม)

ถ้าจะต่อจริง ต้องมี CORE-REQUEST ใหม่เพิ่ม per-session set ของ identity ที่เคยส่ง
TargetVital ให้ -- ยังไม่ทำรอบนี้ เพราะเป็น session-state เปลี่ยนใหม่ ไม่ใช่แค่ประกอบ census

## เทส

`tests/test_diag_multi_object_config.py`, `tests/test_diag_multi_object_wiring.py`
(unit, ของสาย B) + `tests/test_diag_multi_object_runtime_wiring.py` (ใหม่รอบนี้, ขับผ่าน
`make_state_class` จริง ไม่ใช่ synthetic function call เดี่ยว): บัญชีไม่อยู่ allowlist =
login เหมือนเดิมทุกไบต์ (ไม่มี `DIAG object=` เลย แม้แต่บรรทัดเดียว), บัญชีอยู่ใน allowlist =
5 บรรทัด `DIAG object=` พอดี + ตี D0 แล้ว 4 ชิ้นที่เหลือไม่หาย -- full suite 3806 ผ่าน (18
error เดิมจาก capstone/pefile ไม่ติดตั้งใน sandbox นี้ ไม่ใช่ของใหม่)
pf-adversary รีวิวรอบนี้ก่อน commit ตามกฎ (ผลแยกจดหมายถ้าเจออะไรต้องแก้)

## config

`config/diag_multi_object.json` -- repo นี้ไม่ ship ไฟล์นี้ (นั่นคือสวิตช์ปิด) env var
`PF_DIAG_MULTI_OBJECT_CONFIG` override path ได้ รูปแบบเดียวกับ `PF_GM_ACCOUNTS_CONFIG`
ผู้เทสต้องสร้างไฟล์เองบนเครื่องที่รันเทส attended พร้อม key `diag_multi_object_accounts`
เป็น list ชื่อบัญชี

## เรื่อง LANE-B 2344 (build004 reverify)

โน้ต 2344 บอกว่างานยังไม่ commit/push เพราะกฎรอบขัดกับ hard-limit ของเลน -- ตรวจแล้ว
โค้ดจริง (`field_mobs.py` duplicate spawn-position guard) ขึ้นเป็น
`pirate-force-server#156` [LANE-B] ready-for-review อยู่แล้วในตอนที่รอบนี้เริ่ม (สาย B
เปิด PR เองสำเร็จ ไม่ต้องให้ chief commit ซ้ำ) และ pf_bridge ฝั่ง round file/status letter
ก็ merge ไปแล้วใน pf_bridge#248 -- ไม่มีอะไรให้ chief ทำเพิ่มสำหรับใบนี้ ถือว่า
self-resolved ก่อนรอบนี้เริ่ม

-- chief
