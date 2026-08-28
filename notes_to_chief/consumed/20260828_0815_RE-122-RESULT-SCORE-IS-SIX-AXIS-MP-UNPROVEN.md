[ถึง: chief cloud · LANE-A/LANE-B · COO | จาก: RE runner local · 2026-08-28T08:15:10.718+07:00]

# RE-122 RESULT — `s_SCORE` มีจริงแต่เป็น six-axis char-create score; MP และ authentic five-stat baseline ยังไม่พิสูจน์

## สถานะ

**DONE / BOUNDED-NEGATIVE (static-only)** — ปิด T0–T4 ตามเกณฑ์ทางเลือกของใบ `PLAYER-STANDARD-STATUS-AND-CHARCREATE-SCORE-VALUES-001`; current corpus ไม่ให้ provenance ที่พอสำหรับเติม MP/STR/CON/DEX/INT/PER constants และห้ามนำค่า probe/buff/UI score ไป production

- ticket START: `2026-08-28T08:03:53.4098965+07:00`
- client SHA-256: `GameClient.local.bin = 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- raw client table SHA-256: `GameClient/Data/B_CONSTDATA_TH.pc_ = 496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8`
- verifier: `staged/verify_re122.py` SHA-256 `d16a4024c104367db9ac70de1b0271c85d22058f271883c2d02d2df8ddbb329d`
- verifier result: `PASS 44/44`
- existing pinned wire suite: `tests/test_stats_progression_static.py` SHA-256 `0f6667105264c1ae3c56e44b5cf164c86534532ff85b7d0a83f3640e78c73d8c`; `25 passed in 1.67s`

## T0 — input/control และ mandatory searches

ค้น `pf_bridge/external/` ทั้งชุดแล้ว: 30 files, 29,900,221 bytes, deterministic manifest SHA-256 `180424fe457e680e47b38b5b8e9a8094d2dc33c0c9c1f904b9f5a9a040dd11c5`

- exact/name search ครอบคลุม `STANDARD_STATUS`, `POTENTIAL`, `STANDARD_BUFF`, `CHARCREATE_CLASS`, `s_SCORE`, `n_HPMAX`, `n_STAMINAMAX`, และชื่อ primary stats
- ไม่พบ table row, formula หรือ crosswalk ที่ให้ค่า player level 1 class 1; external มีเพียงรายงาน/index เดิมและ wire-contract material ที่ไม่บอก authentic values

ค้น `pf_bridge/gamedata/` ทั้งชุดแล้ว: 1,109 files, 15,319,585 bytes, deterministic manifest SHA-256 `6c7d05ca272d2fbb53098861606478af2c6ad41bdb637378c4554526357aee59`

- พบ `CHARCREATE_CLASS`, `POTENTIAL`, `STANDARD_STATUS`, `STANDARD_BUFF` ใน extracted tables และตรึง SHA แยกรายไฟล์ด้านล่าง
- ไม่พบตาราง/formula อื่นที่มี crosswalk จาก class 1 + level 1 ไป MP current/max หรือห้า ActorAttr wire fields

SHA control เพิ่มเติม:

- `CLIENT_RE_QUEUE.md = f8052303f07f51d644e6dda61b361aeb72a8bddb15fef5b393d8dc7598a2696e`
- `AGENTS.md = 8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`
- `NEW_ORDERS.txt = a19efcb410a23614d8af4106f7d712bb314a5edbbf1b3df793227c3bf811fc5c`
- `PF_JOB001_CHARCREATE_CLASS_STATIC_BOUNDARY_20260816.md = b1375a66686f7b31d91b85ea9b2926d3cc7cee57639a5d14eee4d0de9a34c670`
- `PF_STATS_PROG001_CHARACTER_STATS_AND_PROGRESSION_STATIC_20260818.md = cc8b701cb988b74ee1a95ffd40d33d22b220f2d81ec72538fef0bdcb16abf05e`

`NEW_ORDERS.txt` mtime ขยับระหว่างรอบเป็น `08:04:07+07`; อ่านใหม่แล้วพบเพียง `FROM_CHIEF_R209_TO_ATTENDED_20260828_0759.md` ซึ่งเป็น attended lane นอกขอบเขต RE จึงไม่หยิบมาทำ

## T1 — `CHARCREATE_CLASS.s_SCORE` มีจริง แต่ไม่ใช่ five-stat wire crosswalk

`CONSTDATA_TH__CHARCREATE_CLASS.tsv` SHA-256 `2a2668ab38d7a4501cfec8fada9d140f80527b8a4f0f85bfb1c4269e39b7f4c7` มี 5 rows x 38 columns และมี field ชื่อ `s_SCORE` จริง; class 1 row เป็น:

`n_ID=1`, `s_ICON=Icon_Class_Gladiator`, `s_SCORE=4;3;4;1;1;2`

จุดนี้แก้ premise เก่าจาก `PF_JOB001` ที่รายงาน 37 columns/ไม่มี `s_SCORE`: report นั้น stale เมื่อเทียบกับ extracted table ปัจจุบันและ raw-table SHA ข้างต้น

แต่ `GameClient/Data/GUI/Model/Login_CharCreate_Main.model` SHA-256 `eef1eb1a45929d6770e1fe4e7dfad31208a3de99cde768a6103b35c6e206066c` ระบุกราฟสร้างตัวละครหกแกนชัดเจน: `STATUS_STR`, `STATUS_AGI`, `STATUS_CON`, `STATUS_INT`, `STATUS_PER`, `STATUS_CHA` ค่า `s_SCORE` ก็มีหก component ขณะที่ ActorAttr target มีเพียง STR/CON/DEX/INT/PER ห้าช่อง และไม่มี field ที่ทำ crosswalk component-to-wire

ดังนั้นมีหลักฐานว่า `s_SCORE` เป็น six-axis character-create display score แต่ยังไม่มีหลักฐานว่าค่าใดเป็น authentic base stat ที่ต้องส่งใน ActorAttr; ห้ามทิ้ง CHA แล้วจับห้าค่าที่เหลือตามลำดับเอง

## T2 — `POTENTIAL` ว่าง; `STANDARD_STATUS` ไม่มี HP/MP/stat columns; ค่าใน `STANDARD_BUFF` คนละ domain

- `CONSTDATA_TH__POTENTIAL.tsv` SHA-256 `d798d5acefc620980e25746fafaebfada2b0dd55ca3481183ea15af99f93c614`: schema 11 columns แต่ **0 data rows** จึงไม่มี level-1 formula/base point ให้คำนวณ
- `CONSTDATA_TH__STANDARD_STATUS.tsv` SHA-256 `d7794acfe3261a16c52a1b8235ad685a2a40d2ddfaaa226a44f2e74b009f94c4`: 255 data rows แต่มีเพียง EXP/ability/deadloss/PVP/defence columns; ไม่มี `n_HPMAX`, `n_STAMINAMAX` หรือ primary-stat columns
- `CONSTDATA_TH__STANDARD_BUFF.tsv` SHA-256 `a2906ebf78918f90b925c65624931c2d9692012a9ed4e22846e9add3521bc784`: row 1 มี `n_HPMAX=337`, `n_STAMINAMAX=100` และห้า stat columns = 5 จริง แต่ชื่อตารางและ binary consumer จัดมันอยู่ใน buff domain ไม่ใช่ player baseline

binary anchors ที่ verifier ปักหมุด:

- loader region `0x004A2C00..0x004A4500` อ้าง `STANDARD_STATUS` และ `POTENTIAL` แยกกัน; span SHA-256 `e567f27c21dca2ae4d0b773561b04461fb564cbc6226b8f3961928cce096460c`
- buff loader region `0x00655A40..0x00656600` อ้าง `STANDARD_BUFF`, `n_HPMAX`, `n_STAMINAMAX` และชื่อ primary stats ทั้งห้า (รวม typo จริง `n_CONSITUTION`); span SHA-256 `fc51cc6e49e7562ae2ec35719a45d90a50290ea48b6ce0bd0ff11929f5e415d3`

จึงห้ามนำ `100` หรือห้าเลข `5` จาก `STANDARD_BUFF` มาอธิบายเป็น MP/stat เริ่มต้นของผู้เล่น

## T3 — wire positions ยังผ่าน static suite แต่ไม่มีแหล่งที่สองอิสระสำหรับ authentic values

ชุดทดสอบ static ที่ปัก `ActorAttr +0x82/+0x84/+0x86/+0x88/+0x8A`, masks `0x20/0x40/0x80/0x100/0x200`, tag `0x12` ผ่าน 25/25; รอบนี้ไม่ทำตำแหน่ง wire ซ้ำและไม่พบแหล่ง static อิสระใหม่ที่เปลี่ยนข้อสรุปเดิม

ตรวจ owner probe เพิ่ม:

- `adhoc_attr_probe.py` SHA-256 `f1a439855c0a8996592850d4626bab03fa7b036450717c6b95e6675ddeb9c430`
- source ระบุเองว่า mapping ห้าค่าแรกจาก `s_SCORE` ไป STR/CON/DEX/INT/PER คือ `-- [เดา]`
- source ระบุ `MP_PLACEHOLDER = 50  # probe value, no table source`

ดังนั้น client-observable เดิมที่ UI แสดงค่าตาม probe พิสูจน์เพียงว่า client รับ/แสดงตัวเลขที่เราส่งเข้า wire slots ได้ ไม่ได้เปลี่ยนเลข 50 หรือ mapping ที่เดาให้เป็น authentic original-server values และไม่นำหลักฐาน client-observable มาใช้พิสูจน์ wire/DB layer

## T4 — result และ static ceiling

ไม่พบค่าที่มี provenance พอเติม constants:

- MP current/max level 1 class 1: **UNPROVEN**
- STR/CON/DEX/INT/PER base values level 1 class 1: **UNPROVEN**
- level/class formula: **NOT FOUND** ในขอบเขต external + gamedata + pinned client loader regions ข้างต้น

นี่เป็น method ceiling ของ corpus/static objective ปัจจุบัน ไม่ใช่ time checkpoint: ห้ามรันใบเดิมซ้ำจน chief เปิดใหม่พร้อม artifact/objective ที่เปลี่ยนอย่างมีสาระ เช่น known-good original-server ActorAttr/BasicAttr capture, authoritative server table/formula หรือ recovered crosswalk ที่ผูก six-axis UI score เข้ากับห้า wire fields ได้โดยตรง

## Nonclaims

- ไม่กล่าวว่า `s_SCORE=4;3;4;1;1;2` ไม่มีความหมาย; กล่าวเพียงว่าไม่มี crosswalk พอใช้เป็นห้า authentic wire values
- ไม่กล่าวว่า `STANDARD_BUFF` row 1 ไม่เคยมีผลต่อผู้เล่น; กล่าวเพียงว่า static evidence นี้จัดมันเป็น buff template และไม่พิสูจน์ว่าเป็น login baseline
- ไม่กล่าวว่า wire positions ผิด; positions ยังผ่าน pinned static suite แต่ไม่ตอบคำถามตัวเลขของใบนี้
- ไม่ใช้ linear disassembly เป็นหลักฐานผลลบ; negative จำกัดตาม exact tables/manifests, named-field searches และ pinned loader spans ที่ระบุ
- ไม่มีเกม/server boot, ไม่มี capture ใหม่, ไม่มี client-observable evidence ใหม่ และไม่แตะ canonical DB

## BUILD_IMPACT

`BUILD_IMPACT: hard guard / no value patch` — LANE-A/LANE-B ต้องไม่เติม `MP=50/50`, `MP=100/100`, flat stats `5/5/5/5/5` หรือ map `s_SCORE` ห้าค่าแรกเข้า STR/CON/DEX/INT/PER ใน production; ให้คง MP/stat bits absent ตาม safe policy ปัจจุบันจนมี authoritative value source/crosswalk ข้างต้น แล้วจึงเปิด RE ใหม่อย่างชัดเจน

ไม่มีการแก้ `GameClient/`, server, `external/`, `gamedata/`, queue หรือไฟล์ source ใด ๆ
