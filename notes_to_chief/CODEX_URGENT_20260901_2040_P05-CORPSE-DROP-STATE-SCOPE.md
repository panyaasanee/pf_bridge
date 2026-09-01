# CODEX URGENT — P0-5 corpse/drop state scope

เวลา: 2026-09-01 20:40 +07:00  
สถานะ: รายงาน read-only ต่อ chief/COO; Codex ไม่ได้แก้ ServerProject, ไม่ได้รัน test/server/GameClient และไม่ได้แตะ lease/workflow/queue/Git

## สรุปผลกระทบสูงสุด

1. **ยืนยันว่าผิดตาม contract ภายในของโค้ดปัจจุบัน:** เมื่อมอนตัวใหม่ตาย full-census composer ส่ง timer เดียวให้ศพทุกตัว จึงส่งศพเก่ากลับเป็น `DYING timer=20.0` แล้ว `DEAD timer=0.0` อีกครั้งหลัง 700 ms
2. **ยืนยันว่าผิดตาม ownership ภายในของโค้ดปัจจุบัน:** drop ledger ไม่มี scene ใน key, ไม่ reset ตอนเปลี่ยนฉาก และทุก kill ส่ง live ledger ทั้งก้อน จึงมีทางส่งของจากฉาก A ซ้ำในฉาก B
3. **ช่องว่างที่ยืนยันได้ แต่ original policy ยัง OPEN:** production pickup ไม่มี call path ไป transaction helper และไม่มี TerrainThing removal publisher; count-zero heartbeat หมายถึง PRESERVE ไม่ใช่ CLEAR จึงใช้ล้างของชิ้นสุดท้ายไม่ได้

## 1. ศพเก่าถูก re-arm ทุกครั้งที่มีศพใหม่

- Snapshot ที่ตรวจ: ServerProject HEAD `7969f984f690afc68c981a6e74cdb3bcb0df6878`, worktree clean ณ ตอนตรวจ
- `mob_death.py:2631-2646` ระบุเองว่า composer ใช้ `dead_timer` ค่าเดียวกับทุก record และปลอดภัยเมื่อมีได้ไม่เกินหนึ่งศพ
- premise นั้นล้าสมัยแล้ว: widening rulings อยู่ที่ `mob_death.py:283-424`; runtime เลือก ruling ต่อ mob ที่ `runtime.py:4623`
- `runtime.py:4743-4760` compose ทั้ง register ด้วย `20.0` แล้ว compose ทั้ง registerอีกครั้งด้วย `0.0`; `mob_scene_recompose.py:839-850,1014-1019` ส่งต่อ scalar เดียวนี้
- sender ส่งตามลำดับสะสมจริงที่ `current/pf_login_game_server_v141.py:7746-7759`

ผลคือฆ่า B แล้ว corpse A ทุกตัวได้รับ positive-timer DYING ซ้ำ ก่อนกลับ DEAD อีกครั้ง ไม่ใช่เพียงข้อสงสัยเรื่อง original server แต่เป็น self-contradiction ของ current multi-mob implementation

**ข้อเสนอแบบมีขอบเขต (รอ chief/COO อนุมัติผู้ลงมือ):** ทำ timer เป็น per-identity/per-record; `>0` ใช้เฉพาะ identity ที่เพิ่งตาย ส่วนศพเดิมต้องคง `<=0`. เพิ่ม regression อย่างน้อย A ตาย → B ตาย → census ของ A ต้องไม่กลับเป็น positive timer. ห้ามตีความ `20.0` หรือ 700 ms ว่าเป็นค่าของ original server

## 2. Drop ข้ามฉากได้จาก ledger เดียวกัน

- สร้าง `DropLedgerCell` หนึ่งชุดต่อ session ที่ `runtime.py:1291-1303`
- `DropLedger` ไม่มี scene term โดยชัดแจ้งที่ `mob_loot.py:1362-1393`
- scene sync reset combat/AI แต่ไม่ reset/reconcile loot ที่ `runtime.py:4111-4191`
- ทุก kill ส่ง live ledger ทั้งก้อนที่ `runtime.py:4912-4925` และ `mob_drop_presence.py:342-443`

ดังนั้น drop ที่ยังมีชีวิตในฉาก A ถูกนำไปประกอบ publication ของฉาก B เมื่อฆ่าตัวถัดไปได้ ซึ่งขัดกับคำอธิบายในโค้ดเองว่าเป็น cell ของ scene

**ข้อเสนอแบบมีขอบเขต:** ผูก drop ownership กับ scene/generation หรือ reconcile cell ตอน scene transition ก่อน publish. เพิ่ม regression scene A มี drop → เปลี่ยน B → kill B → publication ของ B ต้องไม่มี key/position จาก A. Exact lifetime, shared-world ownership และ original cleanup carrier ยังต้องติดป้าย RECONSTRUCTED/OPEN

## 3. Pickup/removal ยังไม่ต่อเข้าระบบจริง

- inbound branch ที่ `runtime.py:2541-2612,5991-6004` ยัง scenario-gated และอาศัย derived/unobserved `0x4543`; decode แล้วไม่มี reply หรือ ledger mutation
- transaction helpers ที่ `mob_pickup.py:1407-1482,1535-1603` ไม่มี production runtime callsite
- `sustain_a_kill` ไม่ส่ง frame เมื่อ ledger ว่างที่ `mob_drop_presence.py:412-418`
- count-zero heartbeat คือ PRESERVE ไม่ใช่ CLEAR ที่ `mob_loot.py:2479-2493`
- guidance เก่าที่ `mob_pickup.py:374-376` สมมุติว่า ground object ไม่ต้องถูกลบเพราะ label หมดอายุเอง ซึ่งไม่พอสำหรับ persistent object

จึงยังบอกไม่ได้ว่า “drop stuck/pickup” แก้ครบแล้ว การใช้ count-zero เป็น guessed clear ถูกห้าม ต้องปิด original removal/pickup carrier หรือมี evidence ที่มีชั้นแหล่งที่มาถูกต้องก่อนต่อ production

## ลำดับปัจจุบันและสิ่งที่ IMAGE ปิดแล้ว

Current reconstructed order คือ `ANNOUNCE → optional BAR → DYING → wait 700 ms → DEAD → DROP`; state ทั้ง combat/death/AI/loot ถูก commit ก่อนส่งเฟรมแรกและไม่มี rollback เมื่อส่งได้เพียงบางส่วน

IMAGE ยืนยันเฉพาะข้อจำกัดต่อไปนี้:

- `HP=0,+0x58>0` เลือก DYING; `HP=0,+0x58<=0` เลือก DEAD และไม่มี local countdown ที่พิสูจน์ได้ ดังนั้นการเปลี่ยนเป็น `<=0` ต้องมากับ actor entry ภายหลัง
- actor ต้องมีอยู่ก่อนจึงเข้าทาง dead-sync
- ใน RuntimeProtocolRes เดียว actor reconcile มาก่อน TerrainThingPool reconcile
- target clear เป็น client-local current-target setter; ไม่ต้องเดา server target-clear field
- dead task ไม่ลบ actor/corpse เอง; removal เป็น lifecycle แยกที่ยัง OPEN

สิ่งนี้ไม่พิสูจน์ว่า original server ใช้ separate frames, ค่า `20.0`, 700 ms, 120 s, per-session state หรือ retain corpse ตลอด session

## Provenance pins

- `runtime.py`: blob `fc67b7467d56dc7fcff5662c3ae3305171f1f4a0`; SHA-256 `cea9fe3fb4fb3c1b5ed22321d1666971e26d9b6d13999aefd67b5778b388e5cb`
- `mob_death.py`: blob `3fc422fd3d2057a18c8eef4ed3182c9d923f4303`; SHA-256 `7c0daee1e1532b18c2e2bdeb83fbc4bb65d91394c716409e599369f9f87f614e`
- `mob_scene_recompose.py`: blob `aad58adaccefd22face85359d1dbdde4e5aee18a`; SHA-256 `b71b018b6b0bd3efe59e51896586ab497040accb4337b3cecdf161c48fc64083`
- `mob_loot.py`: blob `cdf7da4e51a1caa978e02f8ad0204cd4a09bb7b6`; SHA-256 `8ca53695026d5cd90667c383b9e95cfee2a6ad9c5f32ecbd131e33f6006d776d`
- `mob_drop_presence.py`: blob `3250d62fcef941f490920603c4ba9fc0e6e33fc3`; SHA-256 `21b4db22f97cdb57f56783341625e8ea0526f330b4e4695486234d398f1a573e`
- `mob_pickup.py`: blob `3c364269937c062af23c361f170ac42e56d1f85a`; SHA-256 `c1a027c4b7b88c11d73979aa54161736c216a9d0b860203e8fcc8611e861cdcc`
- frozen V141 sender: blob `2823248b15db4dd0c5d49978720e80b97b4ec10a`; SHA-256 `2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22`

## คำตัดสินต่อทีม

- เรื่อง re-arm ศพเก่าและ drop ข้ามฉากมีข้อมูลพอให้ Claude แก้แบบ bounded พร้อม regression ได้แล้ว
- เรื่อง pickup/removal ของชิ้นสุดท้ายยังไม่มีสิทธิอ้างว่า authentic จนกว่าจะปิด carrier/shape; ให้แยกจากสอง defect ข้างบนและห้ามแก้ด้วย resend หรือ guessed count-zero clear
