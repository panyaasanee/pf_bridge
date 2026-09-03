[ถึง: chief cloud · LANE-B · COO · cc Panya | จาก: RE runner LOCAL | 2026-08-28T20:18+07:00]

# RE-130 RESULT — DONE/PASS · ป้ายชื่อมี owner ต่อ element · one-entry generation แทนของเก่าด้วย omission

- ใบ: `RE-130 GROUND-ITEM-LABEL-LIFETIME-VS-LIST-MEMBERSHIP-001 [STATIC-ON-BRIDGE]`
- ticket START: `2026-08-28T20:10:29+07:00`; round START `2026-08-28T20:01:46.472+07:00`
- วิธี: static/read-only เท่านั้น · ไม่เปิดเกม · image base `0x00400000`
- verdict หลัก: runtime object ของแต่ละ list element ถือ `NameBoard_ITEM` ไว้ที่ `runtime+0x80`; CREATE เติม `s_NAME` และ text property ลง object เดียวกัน. full-list clear เรียกเส้นทาง disable/hide ต่อ runtime ทุกตัว และ destructor ปล่อย reference ที่ `+0x80`. ป้ายจึง **มี ownership ผูกกับ element/runtime membership** ไม่ใช่หลักฐานของ detached one-shot เพียงอย่างเดียว.
- verdict emission shape: list codec รับ `count > 1`; ทุก nonempty generation reconcile keyed tree แล้วลบ key เก่าที่ไม่อยู่ใน generation ใหม่. ดังนั้นการส่ง N เฟรมแบบ `count=1` ด้วยคนละ key ทำให้เฟรมหลังแทนเฟรมก่อนด้วย omission. `count=0` เป็น no-op ใน consumer นี้.

## ช่องค้นบังคับ

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** RuntimeRes/derived-list codec, create/update, item-label property path และ prior registry/serializer rowsที่ช่วย crosswalk identity; tree 30 ไฟล์ / 29,900,221 bytes / manifest fingerprint `3b742370873829347ec7827e610c96e8091b0400fde70ceae9965c6f3664e811`. **ไม่เจอ** artifact ที่ตอบ lifetime/expiry หรือ semantic ของ field `NameBoard+0x24 = 0xC8` โดยตรง จึงเดิน native ownership/teardown ต่อ.
- **ค้น gamedata แล้ว: ไม่เจอ** `NameBoard_ITEM`, `LABEL_ITEM_NAME`, RuntimeRes list membership, one-shot expiry หรือ crosswalk ของ `0xC8` ใน tree 1,109 ไฟล์ / 15,319,585 bytes / manifest fingerprint `e8e44669b2e7b7b06a8722be9c622ee988ab5c169a4b170ad8956751d9428e5b`. การพบเลข 200 กระจัดกระจายในตารางอื่นไม่ใช่ crosswalk และไม่ได้ใช้เป็นหลักฐาน timer.

## T0 — input/SHA gate และของเดิมที่ reuse

- image `GameClient.local.bin` `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- queue `ce1a8cc8737c431e141a59d398db7669b5491b2a71eb07d95e9856afdfd01ffc`; AGENTS `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`; orders `0e107cd392358cb78767b4562b958f4a59c5ae67bda2e1fe0e69c25ae829c315`
- RE-082 verifier `re082_static_verify.py` `b72e39aa29906f23bcd33a02298ef0e9a67730a4a33a3c27399b3756ca6d70ab`; rerun PASS/exit 0 ก่อน reuse keyed-list answer
- RE-111 result `f0ea844e798f4e9d8b56aabe2ffb3839261b85d871a3ecbff857185268e5e235` (SHA verified; ใช้เพียง layout/context ที่ปิดแล้ว)
- current lane source `ground_loot_nameprop_hypothesis.py` `8e07e133eb3d122d702afc66b1f5ebfee8388260b885a1c5886704a17b736c70`; `mob_loot.py` `52bd656fcd3c631ee4166be5e0ae42cd1194668a77417b9e1f606b3098940a7b`
- ไม่ใช้ item id `28317` หรือ `115` และไม่ยืม semantic จาก id `97`; static proof นี้เดินจาก object/key ownership เท่านั้น.

## T1 — crosswalk จาก element ไปป้ายชื่อ

1. Runtime constructor `[0x005F49C0,0x005F4AEA)` SHA `f4dd4e94aa07f0a1307c1ae992d3811167d2ceb3460a8f69e2da7be42eb14cf9` allocate 0x34 bytes, เรียก `0x005BBC40`, เก็บ ref ที่ `runtime+0x80`, แล้วเรียก virtual `+0x14` ด้วย string `board01`.
2. NameBoard constructor `[0x005BBC40,0x005BBC79)` SHA `53d2e14b79e7160e1a1360fdf3a5a8f9d6739db0a3bb773e78ee2cd95c783a50` ลง vtable `0x00F2CDC0`.
3. setup `[0x005BE2F0,0x005BE37C)` SHA `f3f8edaa82025f191856ed914cc9a60dd23a9dda2098619b4af4de48d0e5927f` resolve UTF-16 `NameBoard_ITEM` @ `0x00F2CFF8` และ child `LABEL_ITEM_NAME` @ `0x00F1C7F4`.
4. CREATE `[0x005F41E0,0x005F4897)` SHA `d8011e41a99fef62e6c311e804b715b20f3187dc57128276e35b947a7510f105` query `s_NAME` @ `0x005F4722`, เรียก setter `0x005BACA0` บน `runtime+0x80` @ `0x005F476C`, และ apply property ผ่าน `0x005BACF0` @ `0x005F4822`.

นี่เป็น crosswalk field/object จริง: decoded element → keyed runtime → owned `runtime+0x80` → `NameBoard_ITEM/LABEL_ITEM_NAME`; ไม่ใช่จับคู่เพราะ id หรือชื่อคล้ายกัน.

## T2 — membership/teardown

- clear iterator `[0x006AF840,0x006AF8B4)` SHA `f965e9a7ede7294704726bf501ac3ada37787d0cc77aae9f5ffb440f7f406566` เดิน keyed runtime objects และเรียก `0x005F48A0` @ `0x006AF890` ทุกตัว.
- label-disable `[0x005F48A0,0x005F48DF)` SHA `ef2920f53ff2027342043aeaa9ea05b0668c0b9f4c9c3fd368e06533618c5ed7` อ่าน `runtime+0x80`, ทำ deactivate ที่ backing UI object, เรียก virtual `+0x18`, แล้ว virtual `+0x20(0)` เพื่อปิด/ซ่อน.
- runtime destructor `[0x005F5060,0x005F5164)` SHA `17b1a602e280f3c0de6f2288ff5cd683b1cd47eb05c2db0aea109c4454ab024b` teardown `runtime+0x80` ผ่าน `0x005F4FC0` และ release ref ผ่าน `0x0088D060` @ `0x005F512C`.

ผล: membership/owner มีเส้นทางที่กระทบ label โดยตรง. อย่างไรก็ตาม omission path มี world/map teardown เพิ่มอีกชั้น และ static นี้ไม่แปลงมันเป็นเวลาบนจอรายเฟรม.

## T3 — count, replace-vs-merge, key และ clear timing

- complete consumer `[0x006AF970,0x006B03E3)` SHA `e5eb9e1fdae15544773c7e94fa6ff6aaa6990650cbb05f20e39a009941575663` ยืนยันคำตอบเดิม RE-082: `count` อ่านจาก list object `+0x2C`; codec loop รองรับมากกว่า 1.
- element key: wire `u32 tag 0x14` → element `+0x10` → keyed runtime tree โดยไม่มี transform.
- generation ใหม่ที่ **nonempty** update/create key ปัจจุบัน แล้ว erase key เก่าที่ omitted (`0x005E0D40` @ `0x006AFF84`/`0x006B0368`). นี่คือ replacement-by-omission ไม่ใช่ merge สะสม.
- `count=0` branch ไป epilogue โดยตรง; จึงไม่ใช่ clear command ใน consumer นี้. full clear เป็น lifecycle path แยกที่ `0x006AF840`.

## T4 — verifier

- `pf_bridge\staged\re130_ground_label_membership_static.py`
- SHA `5d656e5544b95f05dfe82802b5fc3f8a964f981292555945dd47d1d6fd6818c4`
- `py -3 -B`: PASS/exit 0; pin 10 code spans, 4 UTF-16 crosswalk strings และ image SHA; ไม่มี `.pyc`.

## Nonclaims / evidence separation

- `NameBoard+0x24` ถูกตั้งเป็น `0xC8` ใน constructor จริง แต่ใบนี้ **ไม่พบ semantic consumer/crosswalk** ที่บอกว่าเป็น milliseconds หรือ lifetime. ห้ามเรียกว่า timer 200 ms.
- client-observable เดิมที่เห็น label ประมาณ 0.2–0.4 s เป็นหลักฐานอีกชั้น; ไม่ใช้พิสูจน์ static ownership และ static ownership ก็ไม่ใช่การพิสูจน์ visible duration.
- ไม่เคลมว่า coalescing แล้วป้ายจะค้างนานขึ้น เพราะยังมี UI visibility/timing, viewport, rendering และ item validity เป็น confound.
- ไม่เคลมว่า omission เรียก `0x005F48A0` แบบ direct ที่ callsite เดียวกัน; ที่ปิดคือ omission เอา keyed runtime/world entry ออก, full clear เรียก disable direct, และ destructor ปล่อย owned NameBoard ref.
- ไม่มีการแก้ client/server/external/gamedata/queue และไม่มีการเปิดเกม.

## BUILD_IMPACT

- **ให้ LANE-B coalesce ของที่ต้องอยู่พร้อมกันเป็น RuntimeRes collection เดียวที่มีหลาย element/key**; codec รองรับ `count > 1`.
- **อย่าส่ง N nonempty single-element collections ต่อกัน** หากตั้งใจให้ N drops อยู่พร้อมกัน: เฟรมหลังลบ key ก่อนหน้าด้วย omission และตัด owner path ของ `NameBoard_ITEM` ตัวก่อน.
- key ต้อง unique/stable ต่อ drop ใน generation นั้น; การส่ง `count=0` ไม่ได้ clear tree นี้.
- การเปลี่ยน emission shape นี้แก้ confound ด้าน membership/owner เท่านั้น ไม่รับประกัน visible label lifetime; หากต้องตอบเวลาบนจอ ยังต้องใช้ attended client-observable แยกชั้น.

**FINAL:** `DONE/PASS` — objective #1 ปิดเชิง ownership/membership; #2/#3 ปิดจาก codec/consumer พร้อม site และ key. ไม่มี method-ceiling checkpoint ค้างในใบนี้.
