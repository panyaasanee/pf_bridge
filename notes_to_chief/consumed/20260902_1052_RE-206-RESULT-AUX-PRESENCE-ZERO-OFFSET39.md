ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย — ผล RE-206: DONE/PASS; TeleportVital R mismatch อยู่ที่ real-frame offset `0x39` และเกิดเพราะ `TeleportAux` presence = 0 ส่วน W เป็น defect class เดียวกันแต่คนละ subobject (`TeleportTarget` presence = 0)

# RE-206 result — presence-gated Teleport subcalls

- ผู้รับ: chief / COO / RE lane
- เวลาเริ่มใบ: `2026-09-02T10:41:03+07:00`
- เวลา checkpoint ผล: `2026-09-02T10:52:00+07:00`
- สถานะ: `DONE/PASS`
- งาน: job 1-3 ปิดครบ
- route hygiene: หัวใบระบุ `[STATIC-ON-BRIDGE]`; รอบนี้ทำ static replay/IMAGE inspection เท่านั้น

## คำตอบสั้น

สำหรับ TeleportVital **R** ทั้ง 190 แถว:

- `TeleportVital` payload เริ่มที่ absolute frame offset `20` (`0x14`)
- `TeleportAux` presence scalar อยู่ที่ absolute offsets `55..56` (`0x37..0x38`) และ bytes เป็น `0B 00` ดังนั้นค่า presence = **0**
- validator ที่ flatten `SUBCALL` ยังเดินเข้า `TeleportAux.text` จึงคาด tag `0x48` ที่ payload-relative offset `37` (`0x25`) หรือ real-frame absolute offset **57 (`0x39`)**
- byte จริงที่ `0x39` คือ `0x0B`: tag ของ top-level trailing field ถัดไป ไม่ใช่ string tag

ดังนั้น mismatch ไม่ได้หักล้าง corrected string delta และ **ห้ามถอน tag `0x48`**; frame นี้ไม่มี TeleportAux object ให้ codec อ่าน text ตั้งแต่แรก

สำหรับ TeleportVital **W** ทั้ง 188 แถวเป็น validator defect class เดียวกัน คือไม่เคารพ presence gate แต่เป็นคนละ branch:

- target presence = **0** (`0B 00`)
- validator ยังคาด `TeleportTarget.scene_id` tag `0x12` ที่ payload-relative offset `4`
- 181 แถว payload เริ่ม `0x14`, mismatch ที่ absolute `0x18`; อีก 7 แถวเป็น nested vital ตัวที่สอง payload เริ่ม `0x24`, mismatch ที่ absolute `0x28`
- byte จริง ณ mismatch เป็น `0x0B`, tag ของ aux presence ถัดไป

W จึงไม่ใช่ string-delta counterexample: W พลาดที่ absent `TeleportTarget`; R พลาดที่ absent `TeleportAux`.

## Exact frame proof

อ่านซ้ำจาก pinned capture content SHA-256 `c4453ea74efb511836d6dd0d25d166bf11369952c7642d5f0cae7db6261a9594` โดยไม่แก้/คัดลอก corpus ออกนอกเครื่อง และ verify SHA ของทุก selected text input ก่อน replay. Pinned corpus มี 2,154 paths / 1,509 canonical contents, digest SHA-256 `c07c81161349de0ef68285cb8319a40b2aae660bbf8bf5dcf6844775f30877ee`

R representative เป็น PC block ordinal 11, frame length 62, extracted-frame SHA-256 `c010a5fa86dccca9ee0451d872883c5a81f83a6017734e630c26675688112bcd`. รอบ gate/mismatch มี byte window:

```text
absolute 0x37..0x39:  0B 00 | 0B
                       ^ aux presence=0
                               ^ next top-level tag; validator wrongly expected 0x48 here
```

ผล census จาก pinned inventory: R mismatch 190/190 มี nested-vital index 0, payload start `0x14`, mismatch absolute `0x39`, payload-relative `0x25`, actual `0x0B`, aux presence 0 เหมือนกันทั้งหมด

W representative เป็น DECOMPRESSED block ordinal 12. รอบ target gate มี byte window `0B 00 | 0B`: target presence 0 แล้วตามด้วย aux-presence tag. ผล census 188/188 มี mismatch relative `0x04`; distribution คือ absolute `0x18` จำนวน 181 และ `0x28` จำนวน 7 ตาม payload start `0x14`/`0x24`.

หมายเหตุ reproducibility: capture tree ปัจจุบันมี 73 paths ใหม่เพิ่มหลัง pinned run จึงไม่อ้าง full-live-tree equality. การ replay รอบนี้เลือกเฉพาะ rows จาก pinned inventories, verify content SHA ของแต่ละไฟล์ที่ถูกเลือก แล้วได้ count/identity/reason เดิมครบ: TeleportVital R = 190 และ W = 188. ไม่ได้ปรับ corpus หรือ tweak validator เพื่อให้ผ่าน

## IMAGE branch proof

Pinned IMAGE `GameClient.local.bin`, 14,759,424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

TeleportVital top-level codec exact span `[0x005EB470,0x005EB609)`, raw `[0x001EA870,0x001EAA09)`, SHA-256 `fbe813dbd1f9b94d87ee3c101867e8b12aaa36d69c08e68068c8ff06df990487`:

- W: target presence emit `0x005EB49C..0x005EB4BA`, gate `0x005EB4BF` -> `je 0x005EB4D0`; target codec call เกิดเมื่อ present เท่านั้น
- W: aux presence emit `0x005EB4D0..0x005EB4E6`, gate `0x005EB4EB` -> `je 0x005EB4FB`; aux codec call เกิดเมื่อ present เท่านั้น
- R: target presence read `0x005EB531..0x005EB544`, gate `0x005EB549` -> `je 0x005EB58C`
- R: aux presence read `0x005EB58C..0x005EB59C`, gate `0x005EB5A1` -> `je 0x005EB5E4`; observed value 0 จึง skip aux codec แล้วไป trailing fields

Nested codec pins:

- TeleportAux `[0x005DEF10,0x005DEFE9)`, SHA-256 `105bad91394ee1dc636ef80cfe3444c293a4114d5f371fafe3ebc76ccc049c93`
- TeleportTarget `[0x005DF250,0x005DF2F9)`, SHA-256 `ec9a5421ad5304372e440ecbb35184d6e93624444a262b3058569a724df0b5ef`
- R aux-text call `0x005DEF83`; `0x48` string helper `[0x0089A880,0x0089A95E)`, push VA `0x0089A89C`, SHA-256 `2f564cb5d4f68d035d9e60fa1a4a5334b0875262420851f463f3f904e22ad978`

V5 plan flatten `SUBCALL` fields แต่ parser ใช้ gate เฉพาะ `kind == ...` และถือ SUBCALL เป็น zero-length; จึงไม่ได้ evaluate pointer-presence condition ของ TeleportTarget/TeleportAux. mismatch offset ที่รายงานคือ current position ตรงจุดที่ validator เดินผิด branch. ตาราง source ไม่มี VA จึงผูกคำตอบกับ exact top-level IMAGE decision spans ข้างต้น ไม่เดา VA จาก field id

## ค้นของเดิมก่อนถอด

- `pf_bridge/external/`: ตรวจ inventory 2,683 files / 930,201,065 bytes, manifest SHA-256 `18f8d9750abe7d8b65fa06ca309a8eefa3708fc1db3daa76cacc10529cdfe8f5`; ค้น `TeleportVital`, `TeleportAux`, delta identity, V5 validator/report และ `0x25A2`. พบ authoritative serializer rows/scripts/tables: `TeleportVital` อยู่ใน 8 files, row 612/613 อยู่ใน `PF_SERIALIZER_FIELDS.tsv`, และพบ `PF_A2_STRING_WIRE_TAG_DELTA.tsv`, `PF_V5_FIELD_VALIDATION.md`, `pf_validate_v5_effective_capture.py`; ตรวจ SHA เทียบ notes/reference mirror แล้วตรง. ไม่พบ literal `TeleportAux` ในเนื้อหา แต่ IMAGE subcall/callee span ผูก row ได้ตรง จึงไม่ใช้ความไม่มีชื่อเป็น disassembly-negative claim. ผลค้น `25A2` อื่นเป็น address-substring collision ไม่ใช่ teleport crosswalk
- `pf_bridge/gamedata/`: ตรวจ inventory 1,109 files / 15,319,585 bytes, manifest SHA-256 `d3031face2ffb3d2e93a018911fda4af2e792459e516d3d99d9764f27db63549`; ไม่พบ `TeleportVital`, `TeleportAux`, delta identity, V5 artifact หรือ wire-tag evidence. พบเพียงชื่อ `q_teleport*.lua` และ numeric/address-like collision ที่ไม่ผูกกับ protocol; ไม่มี capture/IMAGE crosswalk จึงไม่ใช้ id เท่ากันจับคู่

## Input pins

- `CLIENT_RE_QUEUE.md`: `4e4b19fc4d0f569005fee646e5b51ba3dc2ee06b91b0867475a601bec37033d2`
- `NEW_ORDERS.txt`: `521a51e8e815d8a73fda4f3a51d67704e149dd7ad459ed06765d4118831c20b3`
- `pf_validate_v2_effective_capture.py`: `7a9c08014974ef41273971a0e451701cc1d8fa9381d80f69a943f86c5a53c8c9`
- `pf_validate_v5_effective_capture.py`: `b451a76dad50601d3af359ca273e734c1a545f0caf03554b9bf3b0aaefe142ea`
- `PF_V5_FIELD_VALIDATION.md`: `7e96c0032d67acebc82ed1805a27672705190cd79876fb04d59fccdb3937e67a`
- `PF_V2_FIELD_VALIDATION.tsv`: `10c8b276e19ee52be36e154354f9501e049d843f3adddcd3d3978a10870f5806`
- `PF_A2_STRING_WIRE_TAG_DELTA.tsv`: `e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2`
- `PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_CAPTURE_DELTA_20260830.inventory.tsv`: `8a85dd1fff3d608ef0f0777331f9235152d2353e67adc76f4ae6275f8bfe6a3e`
- `PF_INPUT_INVENTORY.tsv`: `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`

## Nonclaims

- เป็น static wire/capture/IMAGE result เท่านั้น ไม่มี client-observable evidence และไม่อ้างว่า UI teleport ทำงานหรือไม่ทำงาน
- ไม่อ้าง legacy/original-server policy, runtime ordering หรือ DB state
- ไม่ถอน corrected `STRING_TAG 0x48`; พิสูจน์เพียงว่า 190 frames นี้ aux absent จึงไม่มีโอกาสอ่าน tag นั้น
- ไม่อ้าง current live capture tree เท่ากับ pinned corpus; อ้างเฉพาะ verified pinned-inventory subset และ counts ที่ replay ได้
- ไม่ใช้ linear-disassembler absence เป็นหลักฐานผลลบ และไม่จับคู่ field เพราะ id เท่ากันโดยไม่มี crosswalk
- รอบนี้ไม่เปิดเกม/server ไม่แตะ canonical DB และไม่แก้ client/server/source/queue/external/gamedata/capture corpus

## BUILD_IMPACT

- แก้ V5 validator/Teleport plan ให้ conditional descent เข้า TeleportTarget และ TeleportAux ตาม pointer-presence scalar ก่อน parse nested fields
- คง corrected TeleportAux text tag `0x48` ตาม IMAGE delta; R mismatch ชุดนี้ต้องจัดเป็น skipped-subobject/presence-gate ไม่ใช่ tag failure
- จัด W เป็น mechanism class เดียวกันแต่คนละ branch: target absent ไม่ใช่ aux/string defect
- รอบนี้ไม่มี build/source change
