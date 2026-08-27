ถึง: chief + Panya

# GT-042 DROPTHING-REDERIVE-001 — PASS หลัง adversarial re-derive พร้อม erratum ขอบเขต handler หนึ่งจุด

เวลา: 2026-08-23 01:54–02:03 +07:00  
ชั้นหลักฐาน: STATIC/wire เท่านั้น; ไม่มี GameClient, server, DB, `LOCK_GAME` หรือภาพหน้าจอ  
อิมเมจ: `GameClient/GameClient.local.bin` size `14759424`, PE32, ImageBase `0x00400000`

## ผลชี้ขาด

- แถว semantic หลักของ GT-040 A/B/C **รอดทั้งหมด**: ตารางฟิลด์สอง sub-serializer, generation-stamp reconcile, gate bit `0x02`, removal call, vtable/serializer และ handler สองทางตรงกับไบต์ที่ re-derive ใหม่
- พบแถว metadata ที่ **ตายหนึ่งจุด**: span `[0x005EF640,0x005EF908)` len 712 มี SHA ตรงตามใบเดิม แต่ **ไม่ใช่ handler หนึ่งฟังก์ชัน**. Handler ที่ vtable ชี้จบที่ `[0x005EF640,0x005EF66F)` len 47; `0x005EF66F=CC` และ `0x005EF670` เริ่ม prologue ฟังก์ชันถัดไป. ความหมาย “อ่าน `+0x18`, แยก FC/FD/FE, คืน true” ยังรอด
- `0x402A20` ปิดชิ้นที่ขาดได้: มัน **ไม่ใช้ argument ที่ caller push มา**; one-time init แล้วคืน global singleton `0x0102C6C0`. `[mgr+0x24]` เป็น head/sentinel ของ ordered map ที่ `mgr+0x0C` ใน singleton นี้. เส้นทาง insert ที่พิสูจน์ได้มาจาก `0x446990` สำหรับ actor_type 2..6 ผ่าน `0x446090` (ผู้เรียกจุดเดียว). ดังนั้นลิสต์ที่ reconcile กวาดคือ **network-actor registry subset ที่ manager นี้สร้าง/ลงทะเบียน ไม่ใช่ actor-entry collection ของเฟรมล่าสุด และไม่ใช่ scene-load population ทั้งหมด**
- ข้อสันนิษฐานแฝงว่า `[esi+0x1C]+0x10` เป็นตัวเลือก manager **ตาย**: pointer นั้นถูก push ค้างไว้และสุดท้ายถูก `ret 4` ของ `0x446F30` เก็บ stack; `0x402A20` ไม่อ่าน stack argument เลย
- หลังแก้ erratum ขอบเขต handler แล้ว GT-040 ผ่าน adversarial audit; เสนอให้ chief ปลดข้อห้าม “ห้ามเขียน module/encoder” เฉพาะบนแถวที่รอด/ขอบเขตที่แก้แล้ว (ยังไม่ใช่คำสั่งให้เขียน)

## Job 1 — field tables A

### `0x005E2960` / derived bit `0x04` / object `+0x24`

span `[0x005E2960,0x005E2AF6)`, offset `[0x1E1D60,0x1E1EF6)`, len 406, SHA256 `259e551604b81fece3659d38f74be5f5a9148cbf44c9cc7d74c2301c995d8acc` — guard ผ่านก่อน decode

แถวที่รอดทีละแถว:

- head `tag 0x14 -> +0x10 / len4`: `5E2978 lea [esi+10]`, `5E297C push 14`, `5E296C push 4`
- head `tag 0x0B -> +0x14 / len1`: `5E2985 mov cl,[esi+14]`, `5E2993 push 0B`, `5E2988 push 1`
- head `tag 0x0B -> +0x18 / len1`: `5E299C mov al,[esi+18]`, `5E29A6 push 0B`, `5E299F push 1`
- member count `tag 0x12 / len2`: `([+2C]-[+28])>>2`, `movzx eax,dx`, `push 12`, `push 2` ที่ `5E29B3..5E29CE`
- member `tag 0x0B -> elem+0x10 / len1`: `5E29FC..5E2A09`
- member `tag 0x2A -> elem+0x14 / len4`: `5E2A0E..5E2A18`
- read path ที่ `5E2A33..5E2AEE` สะท้อน tag/offset/len เดียวกัน
- allocator `0x5E2630` มี `push 0x18` ที่ `5E265B`; exact span SHA `45f18808c0263ed6f9a9172a119549247ebc242ebe62d441bb537d5a1dd967b9`

### `0x005F85B0` / derived bit `0x08` / object `+0x20`

span `[0x005F85B0,0x005F8869)`, offset `[0x1F79B0,0x1F7C69)`, len 697, SHA256 `ce0a58f72c5798f1d5263ebdb5ee449659ed04e2974f63f77657ea968a4f1b5b` — guard ผ่านก่อน decode

แถวที่รอดทีละแถว:

- count `tag 0x12 <- [obj+0x2C] / len2`: `5F85EE..5F85FF`
- always `tag 0x14 -> payload+0x10 / len4`: `5F864D..5F8662`
- always `tag 0x0B -> payload+0x28 mask / len1`: `5F8678..5F8685`
- mask `0x02`: `tag 0x14 -> +0x14 / len4` ที่ `5F8690..5F869E`
- mask `0x04`: `tag 0x0F -> +0x18 / len2` ที่ `5F86A3..5F86B2`
- mask `0x08`: `tag 0x05 -> +0x1B / len1` ที่ `5F86B7..5F86C6`
- mask `0x10`: helper `0x5F3490` จาก `+0x1C` ส่ง `tag 0x2A / len4` สามครั้ง; exact span `[0x005F3490,0x005F34C7)` SHA `b5f5a2063ff9fc8f22830e3238a8b30387d781505ace23d889c3a1500ea47454`
- mask `0x20`: `tag 0x08 -> +0x1A / len1` ที่ `5F86DD..5F86EC`
- read path `5F8719..5F884D` สะท้อนตารางเดียวกัน
- allocator `0x5F82C0` มี `push 0x2C` ที่ `5F82EF`; exact span SHA `d13db4d5abbccf0879a600b6d76de19a15b7958610f4f28c2c53ae5fcda26ae6`

parent-link census ทั้ง `.text`+`.code` พบผู้เรียกแต่ละ sub-serializer 2 จุด (write/read) เท่านั้น. Write path ที่ `5E3F40` test bit `0x04`, โหลด `[esi+0x24]`, call `0x5E2960`; ต่อด้วย `5E3F52` test bit `0x08`, โหลด `[esi+0x20]`, call `0x5F85B0`. Raw E8/E9 census ภายในสองฟังก์ชันไม่ไป `0x4469BD`; dword `0x00F3093C`/`0x00F0BAD0` ในสอง span = 0/0. ข้ออ้าง “bit 0x08 มี record สาม float ที่ไม่ผ่าน actor type 2..6” รอดในชั้น static; **ยังไม่ใช่หลักฐานว่ามันเป็น loot หรือ render ได้**

## Job 2 — generation-stamp reconcile B

guards:

- `0x446F30` len430 SHA `9c1157d3109c27c41783d6eed630a6eb46511ef6789a4e121306944ec1271d7d`
- `0x441C40` len81 SHA `f7b9b6afd070ed2a9082675109224ee20a830595eefa54899614562927061861`
- `0x5E4060` len365 SHA `85ff71ffceff5345f94facc9b7fa1c39c8efd2e429248d112cdba578d3df944e`
- `0x88F2B0` len33 SHA `00076eb0d61b7763ba58709f657437f455e6c6a2e3da83b3005bef0b847a61e9`

แถวที่รอด:

- `446F37 inc [mgr+4]`
- loop1 lookup/create/update และ `446FBE..446FC1 mov [obj+D0],[mgr+4]`
- loop2 เดิน `[mgr+24]`; `44702F..447038` เก็บ generation ปัจจุบัน; `44703E..44705D` เก็บตัวที่ `IsKindOf(0x102CB04)` ผ่าน
- ที่เหลือเข้าคิวแล้ว `4470B2 call 0x441C40`; ต่อด้วย `4470B7 or [obj+70],0x100000`
- `0x441C40` ถอดจาก registry `[0x01093198]+0x180` และล้าง intrusive list ก่อน return
- inbound gate รอด: `5E4073 mov eax,[esi+1C]`; `test`; `5E4078 je 5E408A`; มีค่าแล้ว `add eax,10`, `call 402A20`, `call 446F30`
- dword sweep เฉพาะ reconcile: `0x01081A90=0`, `0x01093198=0` — generation stamp ไม่ diff สำเนาเฟรมก่อน
- full exec census: caller `0x446F30` = 1 (`0x5E4085`); caller `0x441C40` = 1 (`0x4470B2`)

## Job 3 — ขอบเขต `[mgr+0x24]`

exact spans ที่เพิ่มจากการ re-derive:

- accessor `[0x00402A20,0x00402A87)` offset `[0x1E20,0x1E87)` len103 SHA `5823a612986173266ba33447188d218b81c3267341ad708020bba0873fc07022`
- singleton ctor `[0x004473F0,0x00447485)` offset `[0x467F0,0x46885)` len149 SHA `a365bae067db087d8a8e2e6a159fe377256b2073bc92bc455d5422bb82f2df2c`
- insert wrapper `[0x00446090,0x00446170)` offset `[0x45490,0x45570)` len224 SHA `d6e35ba65fb47a37a6ea096123e647e50c4848ce6443d07045c1afeeaa03ca0b`
- lookup `[0x00446170,0x004461E6)` offset `[0x45570,0x455E6)` len118 SHA `9aca8f9a7b933faf54502943e8474362617f3c703cb82750990ba7a9488960e7`

หลักฐานขอบเขต:

- `402A20` ใช้ guard `0x102C730`, construct `this=0x102C6C0` ด้วย `0x4473F0`, แล้วคืน `eax=0x102C6C0`; ไม่อ่าน argument
- ctor สร้าง ordered container ที่ `mgr+0x0C`; iterator/head ที่ reconcile อ่านคือ `mgr+0x24` (offset `+0x18` ภายใน container เดียวกัน); vector removals อยู่ `mgr+0x2C`
- lookup `0x446170` ใช้ map `mgr+0x0C` และ key สอง dword
- actor creator `0x446990` dispatch เฉพาะ actor_type 2..6 ที่ jump table `0x4469BD`; เมื่อ create สำเร็จและ flag เปิด เรียก `0x446090`
- `0x446090` insert object เข้า map `mgr+0x0C`; full exec census พบ caller จุดเดียว `0x446AA8`

คำตอบประโยคเดียวตามใบสั่ง: **`[mgr+0x24]` ครอบคลุม ordered registry ของ network actor objects (actor_type 2..6) ที่ singleton `0x0102C6C0` สร้าง/ลงทะเบียน — เป็น subset ของ runtime actors ไม่ใช่ collection ของเฟรมล่าสุด และไม่ครอบคลุม scene-load NPC/world population ทั้งหมด.**

## Job 4 — Part C

guards และ chain รอด:

- serializer `[0x005E5E30,0x005E5E83)` len83 SHA `8e439d4f3ff1479e723b220d8dd78a262b41df3b74839da9d4cb728f69773066`
- old broad handler span `[0x005EF640,0x005EF908)` len712 SHA `22da3ff4c2bcf8f7a006fab20d48f6ed5102617954cad3c68305c82480726c83` (hash ตรง แต่ boundary label ผิด)
- GetId `[0x005E46A0,0x005E46A7)` SHA `d3fc621e95d5e98c081cab3e22ab7d424901e8fb0cb3d7d2be5f90d9fe6919b1`
- registration `[0x00BEE5E0,0x00BEE5F8)` SHA `8fa9ec1ebc0b36405b847ff82adcfdbf31bb82ace52ea8efcf70bdeb1926dc81`
- vtable `0x00F3005C`: slots `+00 5E4690, +04 5E7D80, +08 401B20, +0C 716010, +10 5E46A0, +14 5EB0D0, +18 5E5E30, +1C 5EF640`
- serializer write/read ทั้งคู่มี `tag 0x14 -> +0x14 / len4`, แล้ว `tag 0x08 -> +0x18 / len1`; ไม่มีฟิลด์ที่สาม
- handler exact `[0x005EF640,0x005EF66F)` offset `[0x1EEA40,0x1EEA6F)` len47 SHA `5d17fc4fdeeafde0a4a34e900e76d0336e404f8d2f058ba085044ae8d88d602e`; อ่าน `+0x18`, แยก FC/FD/FE ไป message 1F/03/22 แล้วคืน true
- census dword: `PickupTerrainThing 0xF3093C` 1 จุด; `0x108202C` 2 จุด (GetId read + registration write); getter VA พบ 1 จุดใน vtable; vtable literal พบ constructor 3 จุด

## บัญชีรอด / ตาย

| รอด | ตาย / ต้องแก้ |
|---|---|
| A: field rows ทั้งหมด, bit0x08 record สาม float, non-actor path | ไม่มี semantic field row ตาย |
| B: generation stamp, no prior-frame globals 0/0, bit0x02 gate, one-call removal | สมมติฐานว่า argument ของ `0x402A20` เลือก manager — ตาย; accessor ignore argument |
| C: vtable, serializer 2 fields, handler FC/FD/FE two-way | “handler ทั้งฟังก์ชัน len712” — ตาย; แก้เป็น exact len47 SHA ข้างบน |
| Job3: scope ปิดเป็น network-actor registry subset | คำเดิม “scope unknown” ปิดแล้ว |

optional mask bits `0x01/0x40/0x80` นอก `0x5F85B0` ไม่ได้เดิน data-flow census รอบนี้ตามสิทธิ์ข้ามของใบสั่ง; ไม่กระทบการปิดแกน jobs 1–3

## Artifacts

ผลดิบอยู่ใน `pf_bridge/outbox/`:

- `1017_gt042_job1_field_tables_retry.out.txt` SHA `9D8B9FC9B35B2DF2D9C1F4F5F91B1EE6A8034025291D85FE78C41BC1E33C4A47`
- `1018_gt042_job2_reconcile.out.txt` SHA `8DA49D33AA3FCF2188FB2E430C9FADEEBEFE99277C1BC3100B8E063A9BE726FA`
- `1019_gt042_job3_402a20_probe.out.txt` SHA `B2111878629D73CFB9B6E79479A98DDC9AEB7A2F26CC34C09D7FBD270E6A239A`
- `1020_gt042_job3_402a20_trace.out.txt` SHA `5969273507F6908F5D395B1D2E7B4CFBFEA37CA2D2CB79F88A371CC9B7B722FD`
- `1021_gt042_job3_scope_proof.out.txt` SHA `30A248DD93FB689528C6376C7A7D527C256D53FAF0E0B53EC796609D1EB1DA16`
- `1022_gt042_job4_partc.out.txt` SHA `A41AC86ADF56246EF6C613777300D6B9A5D587ACCC1332268DC737E4CE503565`
- `1023_gt042_partc_handler_boundary.out.txt` SHA `1A93BB43C04FAD12CDCE684B2728F1B95B191DDD48D62EABB7C3A201841E606C`
- `1024_gt042_job1_support_spans.out.txt` SHA `882040C568E8721AF8F0945D26527B86A876C3EBF4CD33EB19B999A90F2FB929`
- `1025_gt042_job1_parent_links.out.txt` SHA `8AD9BA078EA2F0D759B576DF183FFDFC8B109B3936AA6F4C9CAC867AD4B85F68`

จ็อบ `1016` fail ก่อนอ่านอิมเมจเพราะ Windows native argument quoting; retry `1017` เปลี่ยนเป็น stdin และผ่าน. ไม่มีผลวิเคราะห์จาก `1016`.

## Guards / nonclaims

- SHA256 อิมเมจก่อนและหลัง **ทุกจ็อบ** = `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`; ไม่มีการเขียนอิมเมจ
- ไม่แตะ repo source/tools/tests, DB, server, client หรือ `LOCK_GAME`; final listeners 0, GameClient 0, inbox 0, worktree clean
- ไม่ claim ว่าเซิร์ฟเวอร์ต้นฉบับเคยส่งฟอร์แมตนี้, ไม่ claim render/client-observable, ไม่ตั้งชื่อคลาส record bit0x08 หรือ exempt class, ไม่ยืนยัน derived id `0x4543`, และไม่ตีความ tag เกิน len ที่ไบต์พิสูจน์
- คำว่า network-actor registry subset เป็นข้อสรุปจาก singleton/map/create/insert chain ในอิมเมจ ไม่ใช่ข้อพิสูจน์ว่ามี actor ใดปรากฏบนจอ; GT-043 เป็นคนละชั้นหลักฐาน
