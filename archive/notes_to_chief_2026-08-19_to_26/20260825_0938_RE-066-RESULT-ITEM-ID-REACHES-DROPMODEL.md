[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-066 RESULT — PASS/DONE · `+0x14` ถูกใช้เป็น full item ID และถึง item-row decoder

- เวลา: `2026-08-25T09:38:47+07:00`
- ใบ: `RE-066 GROUNDLOOT-DWORD-IS-IT-READ-001`
- หมวด: `STATIC-ON-BRIDGE` ล้วน · ไม่เปิดเกม/เซิร์ฟเวอร์ · ไม่จับ `LOCK_GAME` · ไม่แตะ DB ใด
- ตัวตรวจ: `pf_bridge\staged\re066_static_verify.py` · final exit 0 สองรอบ · ASCII output · recursive CFG 17 span, gap 0 / errors 0 ทุก span

## คำตอบ objective ประโยคเดียว

**YES / T2 FALSIFIED — dword ที่ list codec `0x005F85B0` อ่านลง element offset `+0x14` ถูก consumer ขาเข้าอ่านกลับเป็น full item ID จริง: create path เดินถึง decoder ทางเลือกที่ RE-060 พิน `0x00892580 -> 0x00890FC0 -> 0x00890EF0 -> 0x00890E70` และ query `s_NAME`; อีก create path เดิน `0x00892DD0 -> 0x00892610 -> 0x00890FC0 -> 0x00890E70` แล้ว query `n_DROPMODEL_TYPE`; update path ใช้ decoder หลังเช่นกันและ query `s_TAG_EXTRA`/`n_QUALITY` — ดังนั้น T2 ที่ว่า handler ไม่แตะ dword ถูกหักล้างเชิงโครงสร้างสำหรับ client image ที่ ship มา ส่วนการวาดโมเดลจริงยังเป็นคำถาม runtime ของ GT-045.**

## ช่องค้นบังคับก่อนถอด

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** `GSCN_RunTimeProtocolRes` ใน `PF_PROTOCOL_REGISTRY.tsv` (`serializer 0x005E3EE0`, handler `0x005E4060`), `DropThingModule_Client`, และ metadata ของ list/read primitive ใน `PF_SERIALIZER_FIELDS.tsv`; ชุด external ยืนยันจุดเริ่มแต่ **ไม่เจอคำตอบ downstream ว่า `+0x14` ไป field ใด** จึง verify SHA แล้วเดิน image ต่อ.
- **ค้น gamedata แล้ว: เจอ** `CONSTDATA_TH__EQUIPMENT_BASE.tsv` และ `CONSTDATA_TH__ITEM_MISC.tsv` ซึ่งมีคอลัมน์ `n_ID_MODEL`, `n_DROPMODEL_TYPE`, `s_NAME`, `n_QUALITY`, `s_TAG_EXTRA`; ตัวอย่าง `ITEM_MISC n_ID=1` มี `n_ID_MODEL=0/n_DROPMODEL_TYPE=0`, `EQUIPMENT_BASE n_ID=3` มี `2/1`, และ `n_ID=423` มี `0/1`. ใช้เพียงตรวจว่าชื่อ field มีอยู่จริง — **ไม่ใช้เลข/แถว gamedata join เพื่อพิสูจน์ control flow**.

ค้นก่อนถอดตามกฎแล้วพบเพียง pins/registry ไม่พบคำตอบ objective สำเร็จรูป จึง re-derive จาก image โดยอาศัย pins ของ GT-042 และ RE-060.

## จ็อบ 0 — control gate PASS

- image `GameClient\GameClient.local.bin`, size 14,759,424, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- list codec `[0x005F85B0,0x005F8869)`, file off `0x001F79B0`, len 697, sha256 `ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b` ตรง GT-042
- stream READ `[0x0089A640,0x0089A6C6)`, file off `0x00499A40`, len 134, sha256 `4b58ff55a1e7fdd1640f7be47db6a44a41d1e83093bd8dd271c5c0d1dab3ca51`
- exact store: `0x005F878D lea eax,[esi+0x14]` แล้ว `0x005F8795 call 0x0089A640`; element ctor กำหนด `[esi+0x14]=0` ที่ `0x005F8329`; element vtable `0x00F313C4`
- ทั้ง image, pinned span และ read primitive ตรงก่อนเดินต่อ; recursive CFG ของทั้งสอง span gap 0 / errors 0

## จ็อบ 1 — inbound chain และผู้อ่าน `+0x14`

parent `GSCN_RunTimeProtocolRes` อ่าน list ที่ `[esi+0x20]` ผ่าน call site `0x005E4042 -> 0x005F85B0`; handler ส่ง list ต่อ `0x005E40D5 -> 0x005F53A0`, แล้ว handoff call site `0x005F5428 -> 0x006AF970`.

ใน concrete inbound consumer graph พบผู้อ่านสามกลุ่ม:

1. **compare/update decision** ใน `0x006AF970`: `0x006AFCF8 mov esi,[eax+0x14]`, เทียบอีก element ที่ `0x006AFD0D cmp esi,[edx+0x14]`, mismatch ไป update branch.
2. **create** `0x005F41E0` (call site `0x006B01A0`): อ่านที่ `0x005F426D` และ `0x005F46FA`.
3. **update** `0x005F4C00` (call site `0x006AFDE9`): อ่านที่ `0x005F4CAC`.

bounded call/ref census ทั้ง image:

- `0x005F41E0`: rel32 caller มี `0x006B01A0` จุดเดียว; raw dword refs 0
- `0x005F4C00`: rel32 callerมี `0x006AFDE9` จุดเดียว; raw dword refs 0
- `0x005F85B0`: rel32 callers `0x005E3F63, 0x005E4042`; raw dword refs 0
- element vtable `0x00F313C4` มี refs `0x005F8265, 0x005F8313, 0x005F83AB` เท่านั้น ซึ่งอยู่ใน dtor/allocator

ขอบเขตของคำว่า “ครบ” คือ concrete graph ที่ parent/handler ข้างต้นส่งเข้า consumer + whole-image exact rel32/dword/vtable census; ไม่ได้อ้างว่าตัด indirect alias ที่ไม่มี literal/rel32 ได้ทั่วทั้งโปรแกรมด้วยชื่อชนิดเพียงอย่างเดียว.

## จ็อบ 2–4 — decoder chains และ field ที่อ่าน

### create path A — full code/table/row + `s_NAME`

`0x005F46FA mov eax,[eax+0x14]` -> call site `0x005F4703 -> 0x00892580` -> call sites `0x008925A6 -> 0x00890FC0`, `0x008925BB -> 0x00890EF0`, `0x008925E8 -> 0x00890E70` -> push literal `s_NAME` (`0x00F0C294`) ที่ `0x005F4722` -> `0x005F4731 -> 0x00892050`.

นี่คือ alternative decoder `0x00892580` ที่ RE-060 พินไว้ และถึง code-tree, table object และ row lookup ครบ จึงตอบ objective ว่า **ถึง item-table decoder จริง** แม้ call แรกไม่ใช่ entry `0x00892530`.

### create path B — row + `n_DROPMODEL_TYPE`

`0x005F426D mov eax,[eax+0x14]` -> `0x005F4276 -> 0x00892DD0` -> `0x00892DEA -> 0x00892610` -> `0x00892653 -> 0x00890FC0` -> `0x00892682 -> 0x00890E70` -> push literal `n_DROPMODEL_TYPE` (`0x00F30F88`) ที่ `0x005F4285` -> `0x005F4291 -> 0x00891EE0`.

### update path — `s_TAG_EXTRA` และ `n_QUALITY`

`0x005F4CAC mov eax,[eax+0x14]` -> `0x005F4CB5 -> 0x00892DD0`; row ที่ได้ query `s_TAG_EXTRA` (`0x00F0C27C`) ที่ `0x005F4CC9` ผ่าน `0x005F4CD0 -> 0x00892050` และ query `n_QUALITY` (`0x00F0C190`) ที่ `0x005F4D21` ผ่าน `0x005F4D2D -> 0x00891EE0`.

literal `n_ID_MODEL` มีหนึ่ง UTF-16 occurrence ที่ `0x00F1D3C8` และ raw dword refs ทั่ว image 21 จุด แต่ refs ในสาม concrete spans `CREATE`/`UPDATE`/`CONSUMER` = 0. จึงรายงานได้เพียงว่า graph นี้มี named lookup `n_DROPMODEL_TYPE` และไม่มี named lookup `n_ID_MODEL`; **ไม่อ้างว่า client ทั้งโปรแกรมไม่เคยอ่าน `n_ID_MODEL` หรือว่าไม่มี alias อื่น**.

## Span manifest — ทุกฟังก์ชันที่พึ่ง

ทุกแถว recursive CFG gap 0 / decode errors 0:

```text
PARENT_CODEC  [0x005E3EE0,0x005E404E) off 0x001E32E0 len  366 sha ea5a21f39f095780b3f83fec2d465f3fe435f6b0ffc04a1e67107ffad489ea60
INBOUND       [0x005E4060,0x005E41CD) off 0x001E3460 len  365 sha 85ff71ffceff5345f94facc9b7fa1c39c8efd2e429248d112cdba578d3df944e
HANDOFF       [0x005F53A0,0x005F5456) off 0x001F47A0 len  182 sha 77136c150b0e557ad4facea096191de0fb9f23e9c30ee5c550c8fa6594b33894
ELEMENT_ALLOC [0x005F82C0,0x005F83F9) off 0x001F76C0 len  313 sha d13db4d5abbccf0879a600b6d76de19a15b7958610f4f28c2c53ae5fcda26ae6
LIST_CODEC    [0x005F85B0,0x005F8869) off 0x001F79B0 len  697 sha ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b
CONSUMER      [0x006AF970,0x006B03E3) off 0x002AED70 len 2675 sha e5eb9e1fdae15544773c7e94fa6ff6aaa6990650cbb05f20e39a009941575663
CREATE        [0x005F41E0,0x005F4897) off 0x001F35E0 len 1719 sha d8011e41a99fef62e6c311e804b715b20f3187dc57128276e35b947a7510f105
UPDATE        [0x005F4C00,0x005F4DEE) off 0x001F4000 len  494 sha 7b14d16ca60fc6917328cc9a59f8c8f7ab6e13052eac3764c69dae45d41c06c2
STREAM_READ   [0x0089A640,0x0089A6C6) off 0x00499A40 len  134 sha 4b58ff55a1e7fdd1640f7be47db6a44a41d1e83093bd8dd271c5c0d1dab3ca51
FULL_ID_ROW   [0x00892580,0x00892606) off 0x00491980 len  134 sha 1ce8aa30afadc034fcfabadcf2ab67c6bf828fad0e30bf48af68283901c368e7
COMPACT_ROW   [0x00892DD0,0x00892DFF) off 0x004921D0 len   47 sha 86207aa54679d54db4eda09a55b86574c774519627d35a15a5825093e75cab7b
COMPACT_DEC   [0x00892610,0x008926A9) off 0x00491A10 len  153 sha 8712036d008b51d1806958c1dafea404935be0b13ca867bcbb0ff22007bf2f7c
CODE_LOOKUP   [0x00890FC0,0x00891026) off 0x004903C0 len  102 sha 9b11d687e5d0ed8030f58e3f9678f9bf82da49fad374f93af6b6a052fe3bbaa3
TABLE_LOOKUP  [0x00890EF0,0x00890FB2) off 0x004902F0 len  194 sha c1c8e488dd696234840e151b293aee0a6ab20495cc7b6f1fa3abfcb66bba8503
ROW_LOOKUP    [0x00890E70,0x00890EE5) off 0x00490270 len  117 sha cb6809072db9b73a7ac43226b54cb413409d67e8ad35079e476073a672548f78
NUMERIC_FIELD [0x00891EE0,0x00891F25) off 0x004912E0 len   69 sha 20f58d14ac4d6c1a5c3113b0c5e5e4af501660a01d7a953db890f45f60829271
STRING_FIELD  [0x00892050,0x0089207F) off 0x00491450 len   47 sha 550c11788729c0b64e8f27501fc7b31a831d5124abd66f70f2d56eacaac3be69
```

## Reproducibility และ SHA ก่อน = หลัง

- verifier `pf_bridge\staged\re066_static_verify.py` final sha256 `676c58370a640f85c254b40c50d3fc3a0d036be2259cfb27f1e285cdaf511308`; วัดก่อน/หลัง final rerun ตรงกัน; exit 0 และ `RE066_VERDICT=PASS`
- image ก่อน = หลัง = `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `external/00_SEARCH_HERE_FIRST.md` `6f6c092c...edb1a459`; registry `27daac0c...716cfb4d`; serializer fields `99282bdf...67b5c123`; runtime classmap `c53a6eaf...c3484985` — ก่อน/หลังตรงกัน
- `gamedata/00_SEARCH_HERE_FIRST.md` `f19db140...10ea2153`; index `a9ab5efd...2110b5bc`; columns `6f1a00dc...1294d89`; EQUIPMENT_BASE `dc39d8b3...b6924c97`; ITEM_MISC `8cd1774d...02d5292` — ก่อน/หลังตรงกัน
- GT-042 pin letter `74eede40...3de4df2`; RE-060 letter `cddb7e79...a5c0f91e`; GT-045 result `af937456...ef47173e`; `AGENTS.md` `25082302...7b0ffca6`; queue `14d55455...5192f411` — ก่อน/หลังตรงกัน
- ไม่แก้ `CLIENT_RE_QUEUE.md`, `GAME_TEST_QUEUE.md`, `CHIEF_CONTINUATION.md` หรือ source ใด

## ชั้นหลักฐานและผลต่อ GT-045

- **static/wire structural:** PASS — byte-exact image + recursive CFG + exact call/ref census
- **client-observable/runtime:** ว่างโดยเจตนา — รอบนี้ไม่เปิดเกม ไม่มีภาพ/วิดีโอ และไม่มี runtime claim
- สำหรับรอบ attended ถัดไป การเปลี่ยนจาก `2600001` ไปแถวที่ `n_DROPMODEL_TYPE` ต่างกัน **เป็นการทดสอบตัวแปรที่ client อ่านจริง**; ผล static นี้ไม่ได้รับประกันว่าจะเห็นโมเดล เพราะ runtime อาจไม่เดิน path/lookup อาจ null/เงื่อนไข render อื่นอาจตก

## Nonclaims

- ผล static ไม่บอกว่า runtime จะเดินเส้นนี้จริง; SCENE-013 null prior ยังเป็นความเสี่ยงแยก
- ผลนี้ไม่แทนที่รอบ attended GT-045 — เพียงหักล้าง T2 และทำให้ตีความการเปลี่ยน item ID ได้ถูก
- ไม่ใช้ gamedata join เพื่อพิสูจน์ control flow และไม่สรุปจาก ID เท่ากันเฉย ๆ
- ไม่อ้างว่า `n_ID_MODEL` ไม่ถูกอ่านที่อื่น; รายงานเฉพาะ named lookups ใน concrete inbound graph นี้
- ไม่พิสูจน์ว่า original server เคยส่งค่าหรือเส้นทางแบบใด; server ต้นฉบับปิดและกู้ไม่ได้ ผลนี้พูดถึง shipped client เท่านั้น

## สภาพจบรอบ

- เกม/เซิร์ฟเวอร์ไม่ถูกเปิด · `LOCK_GAME` ไม่ถูกจับ · canonical DB ไม่ถูกอ่านหรือแตะ
- เพิ่มเฉพาะ verifier ใน `pf_bridge\staged\` และจดหมายฉบับนี้; ไม่ลบ/เปลี่ยนชื่อไฟล์เดิม
- ขอ chief ปิด `RE-066` เป็น **PASS/DONE (YES · T2 FALSIFIED · T1 TESTABLE)** และปรับคำอ่าน GT-045 ว่า item number เป็น input ที่ client consume จริง
