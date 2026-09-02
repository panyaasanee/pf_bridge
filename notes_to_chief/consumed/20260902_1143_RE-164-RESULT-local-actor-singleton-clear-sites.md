[ถึง: chief cloud (cc), LANE-GM และ Panya · จาก: RE runner LOCAL]

# RE-164 RESULT — ข้อ 1 ปิด static: `CMyActor` singleton มี clear-site สองทาง

- เวลา: `2026-09-02T11:43:33.637+07:00`
- สถานะ: **DONE สำหรับงาน static ที่เหลือในข้อ 1**; ข้อ 2/3/4 ปิดมาก่อนแล้ว
- เหตุที่หยิบรอบนี้: เจ้าของสั่งตรงให้ทำและตรวจใบที่พลาดข้าม; ตัวกรองเดิมเห็นคำว่า `CLOSED` ของงานย่อยในหัวใบแล้วตัดทั้งใบ ทั้งที่หัวเดียวกันเขียน `PARTIAL` และข้อ 1 ยัง `STATIC-PARTIAL`
- ขอผู้บริโภค LANE-GM/chief ปิดหัว `RE-164` หลังบริโภคผลนี้

## Input pins

- queue section `RE-164`: 31,427 UTF-8 bytes, SHA-256 `af68e60b6ecbc9b5cb92b72b92341a6899417f32461893f6fdfd8856024dfcf1`
- `GameClient.local.bin`: 14,759,424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- ผลเดิม `20260901_2132_RE-164-RESULT-item3-closed-item1-writesite-found-plus-gamemasterdll-flag.md`: SHA-256 `ec6a5cb99569a95b65227d73223c02d9837ac13dd18bc981fc9004c9a0eb2f42`

## คำตอบข้อ 1

`[0x01032EC4]` เป็น process-global pointer หนึ่งช่องของ local `CMyActor`; มันไม่ใช่ตัวระบุ server connection/session และ lifecycle ปกติมีการล้างก่อนเปลี่ยน actor จึงไม่รองรับสมมติฐานว่า click handler อ่าน context ของคนละ connection เพราะ login เร็ว ๆ กัน

พบ direct write ของ absolute slot นี้สามแห่ง:

1. `0x0044CB7D`: `89 35 C4 2E 03 01` — `mov [0x01032EC4], esi` ภายใน constructor `0x0044C990`; `ESI=ECX` ตั้งแต่ `0x0044C9B5` และ vtable `0x00F0D7A8` ถูกใส่ที่ `0x0044C9C5` จึงเป็นจุด publish ตัว `CMyActor`
2. `0x0044C4E2..0x0044C4EF` ภายใน destructor `0x0044C3B0`:
   - `39 35 C4 2E 03 01` — `cmp [0x01032EC4], esi`
   - `75 06` — ข้ามถ้า slot ไม่ใช่ object นี้
   - `89 1D C4 2E 03 01` — `mov [0x01032EC4], ebx`; `EBX=0` จาก `xor ebx,ebx` ที่ `0x0044C430`
   deleting-destructor ที่ vtable slot `0x00F0D7AC` (`0x0044C7B0`) เรียกฟังก์ชันนี้ที่ `0x0044C7B3` ดังนั้น object เก่าล้าง slot เฉพาะเมื่อยังเป็นเจ้าของ ไม่ล้างทับ object ใหม่
3. `0x004B4B33`: `89 2D C4 2E 03 01` — `mov [0x01032EC4], ebp`; `EBP=0` จาก `xor ebp,ebp` ที่ `0x004B4B12` เป็น unconditional clear ก่อน call path ที่สร้าง/ผูก actor ใหม่ในฟังก์ชัน `0x004B4AD0`

direct-reference census ของ DWORD `0x01032EC4` ใน `.text` พบ 2,016 จุดและ relocation target ตรงครบ 2,016 จุด; ถอดตามขอบเขตคำสั่งแล้วเป็น read/test 2,013 จุดและ direct write 3 จุดข้างบน ไม่มี literal occurrence นอก `.text` จุดที่ linear pass เคยเหลือหนึ่งจุดตรวจซ้ำจาก function boundary `0x004328B0` แล้วเป็น read-only `cmp dword ptr [0x01032EC4],0` ที่ `0x004328B3`

Evidence spans:

- destructor/conditional clear `[0x0044C400,0x0044C530)`: SHA-256 `e37c6f4296a8b1a1217d133fa844f7501f65ec69e179fd2602f0895c49298bdb`
- constructor/publish `[0x0044C940,0x0044CBD0)`: SHA-256 `d0a15f9d0ca922ce3e11867d2babd3692403b3113810a427d3c960720aa2be5b`
- actor-transition clear `[0x004B4A60,0x004B4C00)`: SHA-256 `3db76aa1e2a438ebec21aa38dc003367080be3804384a3444ca7443e505e174a`

## ค้นก่อนถอด

- `pf_bridge/external/`: ตรวจ inventory ร่วม 2,683 ไฟล์ / 930,201,065 bytes, manifest fingerprint `89390abfef41fa1fb4618edbb07dd8dccf4c187568fbcdc99a01f08b1c4d891f`; พบ `0x0044CB7D`/`CMyActor` ในตาราง semantics เดิม ซึ่งยืนยัน publish-site แต่ไม่มี clear-site/destructor span จึงต้องอ่าน image ต่อ
- `GameClient/gamedata/`: ตรวจ inventory ร่วม 1,109 ไฟล์ / 15,319,585 bytes, manifest fingerprint `741a31ba08d930aa498b5cef8443b2f9ec506988c4b1489bb633cb50b3c28eb7`; ไม่พบ `01032EC4`, `0044CB7D`, `CMyActor`, `GameMaster.dll` หรือ `GMUI_BASIC` ในขอบเขตนี้

## BUILD_IMPACT

- ไม่มีการแก้ build/source/data
- ถอนผู้ต้องสงสัย “connection context คนละ session” และ “singleton ค้างข้าม lifecycle ปกติ” ออกจากข้อ 1 ได้; gate นี้วัดว่ามี local actor ที่ publish อยู่
- ถ้า `BT_GM` ยังเงียบ ให้เดินต่อที่ plugin/fallback/empty-key chain จากข้อ 3 หรือ abnormal lifecycle ที่มีหลักฐานใหม่ ไม่ควรแก้ server session state เพื่อไล่ slot นี้

## Nonclaims

1. นี่เป็น static IMAGE evidence ไม่ใช่ client-observable และไม่ได้เปิดเกม/เซิร์ฟเวอร์
2. ไม่อ้างว่า destructor/transition path ถูกเรียกครบใน crash, forced termination หรือ corruption ทุกแบบ; สรุป stale ถูกปิดเฉพาะ lifecycle ปกติที่ผ่านทางเหล่านี้
3. direct-reference census ไม่พิสูจน์ว่าไม่มี indirect alias, self-modifying code หรือ bulk overwrite ที่ไม่ฝัง absolute address; ข้อสรุปอาศัย clear-site เชิงบวก ไม่ใช่ผลลบจาก linear disassembler
4. ไม่อ้างว่า `GameMaster.dll` มีหรือหายจาก install ปัจจุบัน และไม่ใช้เรื่องนั้นปิดข้อ 1
5. ไม่เชื่อม object กับ connection จากเลข/ตำแหน่งเท่ากัน; crosswalk มาจาก constructor + vtable + destructor เดียวกัน

