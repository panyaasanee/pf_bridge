# GT-048 PASS — client มี native scene-placement/create path จาก `bg0001.npc` แยกจาก wire

เวลา: 2026-08-23 14:20–14:50 (+07:00)  
ผู้ทำ: attended game-tester บน Windows bridge  
ชั้นหลักฐาน: STATIC-ON-BRIDGE เท่านั้น (ไม่บูต server/client/DB และไม่ถือ `LOCK_GAME`)

## คำตอบ objective หนึ่งประโยค

**พบ native path:** client อ่าน placement ที่ ship มากับตัวเองจาก `Data\Scene\Save\bg0001\bg0001.npc`, สร้าง `NPCPlacement` และ per-placement runtime creation record ระหว่าง scene-load ผ่าน `SceneNPCCreation`; trigger นี้ไม่รอ record จาก wire และไม่ผ่าน `0x0089A640`.

## หลักฐานค่าพิกัด

- แถวเต็มจาก `current/pf_login_game_server_v141.py`: P30/TID31 Tornado Eagle =
  `(1747.5244140625, -7837.69775390625, 931.0413208007812)`.
- cross-check GT-034 player = `(1847.5244140625, -7837.69775390625, 931.0413208007812)`:
  Y/Z เท่ากันทุกบิต และ X ต่าง `+100.0` ตรงตาม scenario.
- IEEE-754 f32 triple `c870da44 95edf4c5 a5c26844` ไม่พบใน image, float64/fixed-point ก็ไม่พบ.
- พบ exact f32 triple **หนึ่งครั้ง** ใน `GameClient\Data\Scene\Save\bg0001\bg0001.npc` ที่ file offset `0x1D46`.
- `bg0001.npc`: size `27607`, sha256 `026bbe32ca2b69853b1433d585de7e80bb67e7f713e086b9347fd10ad1dc2070`.
- ไม่พบ triple ใน `B_CONSTDATA_TH.pc_`; ตาราง MOBS/STANDARD_MOB/AI_WANDER ให้ template/AI/balance แต่ placement instance อยู่ในไฟล์ฉาก `.npc`.

## สาย native ที่ต่อครบ

1. scene-load entry สองทางเรียก trigger เดียวกัน:
   - `0x0052B1DA -> 0x0043A9D0`
   - `0x0052D3DB -> 0x0043A9D0`
2. `0x0043A9D0` ประกอบ path จาก literal `.\Data\Scene\Save\`, format `%s\%s`, แล้วเรียก `SceneNPCCreation` allocator/ctor `0x0043A460`.
3. `0x00439E90` เติม extension global `.npc`, เปิด mode `rb` ผ่าน local file stream `0x00899FA0`, อ่านสอง collection.
4. placement collection ใช้ allocator/ctor `0x00439B60`, parser `0x00439780`, แล้วเก็บด้วย `0x00439E00`.
   parser อ่าน f32 placement fields ด้วย local stream virtual slots; XYZ ของ record อยู่ต่อเนื่องในไฟล์.
5. trigger วน placement แล้วเรียก `0x0043A6F0` หนึ่งครั้งต่อ placement (`0x0043ACBC`). ฟังก์ชันนี้อ่าน local conditions `CLINE`, `n_CLINE_TYPE`, `n_CREATURE_TYPE`, match model/instance, สร้าง runtime creation record, คัดลอกพิกัด XY จาก placement ที่ `0x0043A90D..0x0043A925`, แล้ว register record ผ่าน `0x006B3440` / `0x00694790`.

ชื่อ `NPCLoadStream`, `NPCPlacement`, `SceneNPCCreation` มาจาก RTTI ใน image (`0x0101A7C8`, `0x0102176C`, `0x01021788`) ไม่ใช่ชื่อเดา.

## เทียบกับ READ `0x0089A640`

- local file stream ตั้ง vtable `0x00F5A3F0`; slot +`0x10`/`0x14` = `0x00899B60`/`0x00899B80`.
- helper f32 `0x00899C20`/`0x00899C40` dispatch ผ่านสอง slot นี้.
- สาย native ข้างบนไม่มี call/jump/dword target ไป `0x0089A640`.
- `0x0089A640` ยังเป็น primitive ของเส้นทาง protocol/stream ที่ GT-040/046 ใช้ แต่ **ไม่ใช่ trigger ของการโหลด `.npc` นี้**. จุดบรรจบที่ไกลกว่านี้ (manager/runtime object) ไม่ทำให้แหล่งป้อนสองทางเป็นทางเดียวกัน.

## spans + guards

| role | VA `[start,end)` | file off | len | sha256 |
|---|---|---:|---:|---|
| NPCPlacement stream parse | `[0x00439780,0x00439A35)` | `[0x38B80,0x38E35)` | 693 | `5ff3c49eb37252c69e5899245ce82cd004f36a15854f2701c690940df56705f2` |
| NPCPlacement alloc/ctor | `[0x00439B60,0x00439D58)` | `[0x38F60,0x39158)` | 504 | `5810fa2584c70f1266ebfb85741cea0feb21f2bcffd091460575743e81bd63f2` |
| `.npc` loader | `[0x00439E90,0x0043A106)` | `[0x39290,0x39506)` | 630 | `39ddc523a5960490bfb941fec81fbe32ca1d622f6ac59c205d2c600eb4fc776e` |
| SceneNPCCreation alloc/ctor | `[0x0043A460,0x0043A569)` | `[0x39860,0x39969)` | 265 | `3c62e12b9d61f5b206f6748df21498d9f668989f27098f29134ffdef0026972f` |
| per-placement native create | `[0x0043A6F0,0x0043A9C3)` | `[0x39AF0,0x39DC3)` | 723 | `28ebd3e05d5c05f956dbb7919a882b4c6654bf821637d653d9f32d1c0a266758` |
| scene `.npc` load trigger | `[0x0043A9D0,0x0043AD54)` | `[0x39DD0,0x3A154)` | 900 | `36dd3c9ce064ad07924b1efc977e807f821a96fab3c3d042890103a784e9248f` |
| scene-load entry A | `[0x0052B010,0x0052B1E7)` | `[0x12A410,0x12A5E7)` | 471 | `873b9fa05b29683fa746fba1b1c00c86c696cf7ca637d2384213d729947ebc07` |
| local file-stream setup | `[0x00899FA0,0x0089A021)` | `[0x4993A0,0x499421)` | 129 | `d117ec13c317de7262d81addc5cab94befe5bd00169681c248c753f5fe4d8416` |
| comparison read primitive | `[0x0089A640,0x0089A6C2)` | `[0x499A40,0x499AC2)` | 130 | `74623d374ea66bbec5bd7f78f861e76a77aecc1e004829ce20f1e0f451ad59b7` |

image sha before/afterเหมือนกัน:
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` (size `14759424`).

## indirect census status

ไล่ E8/E9 ทุก byte ใน `.text` + `.code` และ dword refs ของ focal functions ครบ:

- parser `0x439780`: direct ref เดียว `0x43A0AF`; dword refs = 0
- loader `0x439E90`: direct refเดียว `0x43AB7D`; dword refs = 0
- per-placement create `0x43A6F0`: direct refเดียว `0x43ACBC`; dword refs = 0
- scene trigger `0x43A9D0`: direct refs `0x52B1DA`, `0x52D3DB`; dword refs = 0

ดังนั้น focal chain ไม่มี indirect/vtable edge ที่ค้าง. Local stream dispatch ถูกปิดด้วย vtable `0xF5A3F0` และ slot จริงข้างบน.

งาน bridge: 1037 (ยกเลิก broad all-Data scan), 1038–1046 (exit 0 ยกเว้น 1037 ที่ tester หยุดเองเพื่อบีบ scope).

## verdict / nonclaims

- suggested verdict: **GT-048 PASS (STATIC native scene-placement/create path found)**.
- static นี้พิสูจน์ว่ามี path และ condition/creation record ใน image; **ไม่พิสูจน์ว่ารันจริงหรือ render Tornado Eagle บนจอใน GT-034**.
- ไม่ปิด GT-034; ต้องอ่านคู่ GT-045 ตามคำสั่ง Panya.
- ไม่ claim ว่า placement/AI/drop เป็นพฤติกรรมเซิร์ฟเวอร์ต้นฉบับ.
- ไม่ claim ว่า local record นี้ทำให้หยิบของ/ต่อสู้/กรอบแดงได้เอง; เป็นคนละคำถาม.
