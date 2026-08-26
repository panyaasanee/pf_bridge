[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-082 RESULT — PASS/DONE · `object_ref` คือ wire element key โดยตรง

- เวลา: `2026-08-26T10:17:41+07:00`
- ใบ: `RE-082 PICKUP-OBJECT-REF-SOURCE-001`
- หมวด: `STATIC-ON-BRIDGE` ล้วน · ไม่เปิดเกม/เซิร์ฟเวอร์ · ไม่จับ `LOCK_GAME` · ไม่แตะ canonical DB
- image: `GameClient\GameClient.local.bin`, ImageBase `0x00400000`, size `14,759,424`, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- verifier: `pf_bridge\staged\re082_static_verify.py`, sha256 `b72e39aa29906f23bcd33a02298ef0e9a67730a4a33a3c27399b3756ca6d70ab` · final exit 0 สองรอบ · 10 recursive-CFG spans, gap 0 / decode errors 0 ทุก span

## คำตอบ objective ประโยคเดียว

**YES — dword ที่คลิกซ้ายก๊อปจาก `[drop-runtime+0x7C]->element+0x10` ลง `PickupTerrainThing+0x14` คือคีย์ u32 ของ collection element ที่ list codec อ่านจาก wire tag `0x14` แล้วเขียน `element+0x10` โดยตรง ไม่มี transform/handle/index/hash คั่นกลาง; สมมติฐานของ `MOB-PICKUP-001` ถูกต้องสำหรับ client image นี้.**

## ช่องค้นบังคับก่อนถอด

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `PickupTerrainThing` ใน `PF_PROTOCOL_REGISTRY.tsv` (`serializer 0x005E5E30`, handler `0x005EF640`, vtable `0x00F3005C`) และ field rows ใน `PF_SERIALIZER_FIELDS.tsv`: dword ที่ `+0x14` ใช้ tag `0x14`, byte ที่ `+0x18` ใช้ tag `0x08`; `PF_FIELD_VALIDATION.tsv` ระบุทั้งคู่ `NOT_OBSERVED`. ชุดส่งมอบให้ pin จุดเริ่ม/โคเดค แต่ไม่ตอบ provenance ของ runtime `+0x10` จึง verify SHA แล้ว re-derive จาก image.
- **ค้น gamedata แล้ว: เจอ** ตารางกลุ่ม `DROPS_*`/item และคอลัมน์ `n_ID_MODEL`, `n_DROPMODEL_TYPE` ใน `PF_GAMEDATA_INDEX.tsv`/`PF_GAMEDATA_COLUMNS.tsv`; **ไม่เจอ** field/crosswalk ที่ผูก wire element key หรือ runtime pointer กับแถว gamedata. ไม่ใช้ชื่อ/เลขแถวที่ id เท่ากันมา join และไม่ใช้ gamedata พิสูจน์ control flow.

## T0 — control gate PASS

list codec สร้าง element vtable `0x00F313C4` (`0x005F8311`) แล้ว consumer สร้าง outer runtime object คนละชนิด vtable `0x00F30FAC` (`0x005F49F3`). จุดชี้ขาดคือ create path รับ pointer-to-element จาก incoming tree (`0x006B019A..0x006B01A0`), โหลด exact pointer ที่ `0x005F4222`, retain refcount แล้วเขียน pointer เดิมลง outer `+0x7C` ที่ `0x005F424D`.

ดังนั้น object ที่ click path อ่านจาก `[esi+0x7C]` **คือ exact element ชนิดเดียวกับที่ list `0x005F85B0` สร้าง** แม้ `esi` เองเป็น wrapper/runtime object คนละ vtable. ด่านคุมผ่านโดยไม่อาศัยชื่อชนิดหรือเลข offset ตรงกันเฉย ๆ.

## T1 — `+0x10` คือ wire element key

สายข้อมูลแบบ instruction-exact:

1. list codec อ่าน u32 ผ่าน stream read ที่ `0x005F8766`; ค่าอยู่ stack `+0x44` (`0x005F876B`).
2. เขียนค่าเดิมลง `element+0x10` ที่ `0x005F8779`.
3. เขียนค่าเดิมเป็น key ของ pair ที่ `0x005F8801`, เขียน element pointer เป็น value ที่ `0x005F8805`, insert tree ที่ `0x005F881F`.
4. click producer type-gate candidate (`0x006B0453 -> 0x005F4B90`, `0x006B0459 -> 0x0088F2B0`), ยืนยัน left click `WM_LBUTTONDOWN=0x201` ที่ `0x006B0570`, สร้าง request ที่ `0x006B0639`.
5. `0x006B0642 mov edx,[esi+0x7C]` -> `0x006B0645 mov ecx,[edx+0x10]` -> `0x006B0649 mov [eax+0x14],ecx` -> enqueue `0x006B0653`.

ไม่มี arithmetic, table lookup, counter, hash หรือ index ระหว่าง `element+0x10` กับ request `+0x14`.

## T2 — N/A

ไม่ใช่ handle ที่ไคลเอนต์ตั้งเอง จึงไม่มีฟังก์ชัน map-back เพิ่มเติม. ฝั่งเซิร์ฟเวอร์ต้อง resolve ค่าเป็น **element key ที่ยัง live อยู่ใน ledger/container ของเลน** ตามการ์ดที่สาย B วางไว้; static นี้ไม่รับรองความ live หรือ authorization ของค่า.

## T3 — byte `+0x18` ที่ left click ส่ง = `0`

factory ทั้งสอง allocation paths กำหนด dword `+0x14=0` และ byte `+0x18=0` (`0x005E8FE0/0x005E8FE3`, `0x005E9061/0x005E9064`). Click path overwrite เฉพาะ `+0x14`; serializer ส่ง `+0x14` แล้ว `+0x18` ที่ `0x005E5E49..0x005E5E58`. ดังนั้นค่า opaque-u8/subcode ของ left-click path ที่พิสูจน์นี้คือ **0**.

## T4 — container/removal

- incoming decoded elements อยู่ tree ที่ argument `+0x10`; count เป็น u16 ที่ incoming `+0x2C`.
- live runtime wrappers อยู่ keyed tree ของ receiver `this+0x18` (`0x006AFA15..0x006AFA23`).
- สำหรับ generation ที่ **nonempty** consumer หา key เดิมใน incoming ผ่าน `0x005F8400` (`0x006AFA6E`), update key ที่ match ผ่าน `0x006AFDE9 -> 0x005F4C00`, erase key ที่ถูก omit ผ่าน `0x006AFF84 -> 0x005E0D40`, และ create/insert key ใหม่ที่ `0x006B014F..0x006B0211`.
- สำหรับ list ที่ `count=0`, `0x006AF9B4/0x006AF9BF` branch ตรง epilogue `0x006B03BC`: **ไม่ล้าง live tree**.
- สำหรับ incoming pointer เป็น null มีเส้น clear/erase current tree (`0x006B024F` ถึง erase `0x006B0368 -> 0x005E0D40`).

คำตอบที่วัดได้คือ object ถูกลบเมื่อ reconciliation รอบถัดไปแบบ nonempty omit key นั้น (หรือ null-input clear path); **ยังผูกไม่ได้ว่าป้ายอายุ 0.2–0.4 วินาทีเป็นตัวสั่ง erase**. จึงห้ามสรุปว่าหน้าต่างคลิกจริงเท่ากับอายุป้ายจาก static ชุดนี้.

### ผลข้ามใบ RE-077 ที่ chief ควร amend

ใน consumer เดียวกัน **nonempty one-entry collection มี replacement-by-omission**: entry เก่าที่ไม่อยู่ใน generation ใหม่ถูก erase. แต่ **zero-entry collection เป็น no-op** ไม่ clear. นี่ตอบ rider T5 ของ `RE-077` เชิง static โดยตรง; ขอ chief amend ใบเดิม ไม่ต้องเปิดใบใหม่.

## Correction ต่อ pin เดิมของ GT-046

span factory ที่จดหมาย GT-046 พิน `[0x005E8F90,0x005E907E)` len 238 จบหลัง byte แรกของ instruction สุดท้าย `ret 8`; ขอบเขต instruction-complete ที่ verifier รอบนี้ใช้คือ:

`[0x005E8F90,0x005E9080)` · file off `0x001E8390` · len 240 · sha256 `26e181b37c5abf990b6728c3e041c25cb0382f447ddc6f46e91d30f9a7507674` · 83 instructions · gap 0 / errors 0.

เป็น correction ของ span boundary เท่านั้น; factory field initialization และข้อสรุป GT-046 ไม่เปลี่ยน.

## Span manifest

```text
ELEMENT_ALLOC    [0x005F82C0,0x005F83F9) off 0x001F76C0 len  313 sha d13db4d5abbccf0879a600b6d76de19a15b7958610f4f28c2c53ae5fcda26ae6 insns 103
ELEMENT_KEY_FIND [0x005F8400,0x005F848B) off 0x001F7800 len  139 sha 3718926d3800e7feaee4ea88a7d1f5161d575ebcad92d2ec4d75a93147ca7b48 insns  54
LIST_CODEC       [0x005F85B0,0x005F8869) off 0x001F79B0 len  697 sha ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b insns 236
MODULE_FACTORY   [0x006AF720,0x006AF834) off 0x002AEB20 len  276 sha c3d4d79f9978832998b0fa5edcf033e9278df611505e287015aba0412b27535d insns  87
CONSUMER         [0x006AF970,0x006B03E3) off 0x002AED70 len 2675 sha e5eb9e1fdae15544773c7e94fa6ff6aaa6990650cbb05f20e39a009941575663 insns 742
CREATE           [0x005F41E0,0x005F4897) off 0x001F35E0 len 1719 sha d8011e41a99fef62e6c311e804b715b20f3187dc57128276e35b947a7510f105 insns 416
MODULE_CTOR      [0x005F49C0,0x005F4AEA) off 0x001F3DC0 len  298 sha f4dd4e94aa07f0a1307c1ae992d3811167d2ceb3460a8f69e2da7be42eb14cf9 insns  88
PICKUP_FACTORY   [0x005E8F90,0x005E9080) off 0x001E8390 len  240 sha 26e181b37c5abf990b6728c3e041c25cb0382f447ddc6f46e91d30f9a7507674 insns  83
PICKUP_SERIALIZE [0x005E5E30,0x005E5E83) off 0x001E5230 len   83 sha 8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066 insns  35
PICKUP_PRODUCER  [0x006B03F0,0x006B069B) off 0x002AF7F0 len  683 sha a393f3d41b7f389fac31bc82a7cf4e78367d0413a5427d5dfe91d762b9685827 insns 188
```

ทุก span ใช้ ImageBase `0x00400000`; recursive CFG coverage เต็ม span, gap 0 / decode errors 0. Producer มี tail jump ที่รู้แล้ว `0x006B0628 -> 0x005CBC00` นอก span; ไม่ใช้เส้นนอก span นั้นพิสูจน์ผลลบ.

## SHA ก่อน = หลัง / reproducibility

- image `96272114...b623`; AGENTS `5ff41a9d...8519`; queue snapshot ที่เลือกใบ `b57fd56b...0002c`
- external index `6f6c092c...a459`; registry `27daac0c...cfb4d`; serializer fields `99282bdf...c123`; field validation `080a5f32...41c3`
- gamedata index `a9ab5efd...0b5bc`; gamedata columns `6f1a00dc...94d89`
- GT-046 letter `f8221b8d...6247`; RE-066 letter `f12dbce2...ee4fb`; RE-066 verifier `676c5837...1308`

image/external/gamedata/จดหมายอ้างอิงทั้งหมดที่พึ่งตรงก่อน–หลัง. ระหว่างเริ่มรอบ sync เพิ่ม RE-082 ทำให้ snapshot queue แรกถูกทิ้ง แล้วอ่าน queue ใหม่ทั้งไฟล์ก่อนเลือกใบ. หลังเขียนผลมี sync อิสระอีกครั้งเวลา `10:18`: queue `b57fd56b...0002c -> a8a44640...35be`, `NEW_ORDERS d216cfbb...39f7 -> d311e10f...73c3`; อ่าน queue/RE-082 ใหม่แล้ว objective/จ็อบ/nonclaims ของใบไม่เปลี่ยน และ NEW_ORDERS ระบุว่าไม่มีจดหมายใหม่. การเปลี่ยนนี้ไม่ใช่ของ runner; verifier อ่าน image อย่างเดียว.

## Nonclaims บังคับ

1. ไม่ตอบ opcode จริง; `0x4543` ยัง DERIVED/NOT_OBSERVED และอาจมีเส้น `FightingDrop*` อื่น.
2. ไม่พิสูจน์ว่ามีของ/โมเดลให้คลิก; ถ้าไม่มี runtime object ก็ไม่มี pointer ให้ click path อ่าน.
3. ไม่ยกเพดานหลักฐานของ `MOB-PICKUP-001`: ยังไม่มี runtime transaction และไม่มี DB row ถูกเขียน.
4. ไม่แตะกำแพง allowlist ของกระเป๋า/relog ใน `inventory.require_known_backpack`.
5. ไม่พิสูจน์ client-observable click window, label lifetime, หรือความสัมพันธ์เชิงเวลาระหว่าง label expiry กับ object erase.
6. ผลลบจำกัดที่ 10 concrete CFG spans/การอ้าง direct ที่พิน; ไม่ใช้ linear disassembler อ้างว่าไม่มี indirect/UI owner ทั่วทั้ง image.

`BUILD_IMPACT: MOB-PICKUP-001 สมมติฐานถูกยืนยัน — resolve_claim ใช้ element key จาก request ได้โดยตรงและคงการ์ด live-ledger/ownership เดิม; left-click opaque_u8=0; nonempty generation แทนที่โดย omission แต่ zero-entry generation เป็น no-op. ไม่ต้องย้อนธุรกรรม นอกจาก chief ควร amend RE-077 T5 และแก้ GT-046 factory span pin เป็นขอบเขต instruction-complete.`

## สรุปส่ง chief

`RE-082 PASS/DONE — OBJECT-REF-IS-ELEMENT-KEY · T0/T1/T3/T4 ปิด · T2 N/A · integrity identical except documented concurrent queue sync · static-only.`
