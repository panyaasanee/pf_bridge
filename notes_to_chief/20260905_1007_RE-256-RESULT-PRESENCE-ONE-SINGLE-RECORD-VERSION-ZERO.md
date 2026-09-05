[ถึง: LANE-A | cc: chief, COO | จาก: RE runner local | 2026-09-05T10:07+07:00]

# RE-256 RESULT — DONE/PASS · outer presence = 1, zero-or-one record, vital_version = 0

- ใบ: `RE-256 ADDSURVEYDATA-OUTER-PRESENCE-BYTE-VALUE-001 [OPEN] [STATIC-ON-BRIDGE]`
- START: `2026-09-05T09:58:43.669+07:00`
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB หรือ source/queue/external/gamedata/git
- verdict: เมื่อ `NavigationEx_AddSurveyDataVtial+0x14` ชี้ record อยู่ outer byte คือ tagged byte **`0B 01`**. มันเป็น boolean presence จาก `pointer != NULL` ไม่ใช่จำนวน record. คลาสนี้ถือ pointer เดียว จึงอ่านได้ **0 หรือ 1 record ต่อ vital**. `vital_version` ของคลาสนี้คือ **0 แบบ exact equality**.

## Input pins

- ticket block RE-256 (หัวใบถึง separator, 3,881 chars): SHA-256 `5f96d5854f1b32d48d7b351adb74b54ea41512b574764a7939ece1ea9bbdddcd`
- `GameClient.local.bin` 14,759,424 B: SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `external/PF_SERIALIZER_FIELDS.tsv`: SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- queue ณ START: SHA-256 `34937adf8a1c0187a60c88a6c211464d3415f807a1add3836a02a753fb226cb0`
- ใบต้นทาง LANE-A `20260905_0430...`: SHA-256 `250b334716a9f83cc08de2f3f432d0b3bea6df6a2826a92042756ed929535a62`
- ผลเดิม RE-086: SHA-256 `ddf6d8385d10df41bc9d28514125dfa5a99ea76710b56fddefa5c3322f0737f9`
- ผลเดิม RE-227: SHA-256 `dcdaa4e5261286d6a1128b9dfd93cc7145dc1ba609c05b7496c2f87ffbdfc80d`

## ช่องค้นบังคับ

- **ค้น `pf_bridge/external/` แล้ว:** recursive text search ครอบ inventory 2,683 files / 930,201,065 B; inventory fingerprint `d8d8daf84316d099126f01b33c5fd0489ea9f3609823af5722bbab4e95542f69`; คำค้น `AddSurveyData|NavigationEx|00733570|00733614|0072EC50|0072E590|0xC4AF` ใน `*.tsv/*.md/*.txt/*.json/*.csv`. พบ `PF_PROTOCOL_REGISTRY.tsv:465` ผูกชื่อคลาสกับ vtable `0x00F46F50` และ codec `0x00733570`; พบ `PF_SERIALIZER_FIELDS.tsv:6377-6388` ตรงกับสแปน/คำอ้างเดิม แต่ artifact เดิมยังไม่ให้ค่า presence หรือแยก logical order ของสอง branch. ไม่พบ crosswalk อื่นที่ตอบค่า byte นี้แทนการอ่าน image.
- **ค้น `gamedata/` แล้ว:** recursive text searchด้วยชุดคำเดียวกัน ครอบ inventory 1,109 files / 15,319,585 B; fingerprint `af1fdeb059fa1b23e9f99a1d3095e06c6c512d655ddbd2ef9ed51be3ead6a554`; **0 hit**. ขอบเขตผลลบนี้คือชื่อคลาส/VA/msg-id ในไฟล์ข้อความทั้ง tree; gamedata ไม่มี native-code crosswalk สำหรับ outer serializer นี้.

## Job 1 — ค่า presence byte

Outer codec `[0x00733570,0x00733614)` / file offset `0x00332970` / 164 B / SHA-256 `f8c751001819813123fa70eb2fee9ccf5d866418703dce39185dcf7b56af178c`:

1. W branch ที่ `0x00733586` ทำ `cmp dword ptr [esi+0x14],0`.
2. `0x0073358E setne al` แปลงผลเป็น boolean 0/1.
3. `0x00733593 mov byte ptr [esp+0x20],al` วางค่าลง buffer ที่ส่งให้ tagged-byte writer `0x0089A600` ที่ `0x00733597` (`tag=0x0B`, length=1).
4. เมื่อ pointer มี record ค่าเขียนจึงเป็น **1**; เมื่อ NULL เป็น **0**. ไม่มี arithmetic/count load จาก collection ใด.

คำตอบข้อ 1: **หนึ่ง record = `0B 01`; ไม่มี record = `0B 00`. ค่าเป็น pointer-presence boolean ไม่ใช่ record count.**

## Job 2 — ลำดับ W/R

ตารางเดิมเรียงไซต์ตาม file offset จึงทำให้ R ดูเหมือน call มาก่อนไบต์ แต่ image แสดงว่าเป็น **ฟังก์ชันเดียวสอง branch** แยกด้วย direction flag `BL`:

- W: write presence ที่ `0x00733597` แล้ว ถ้าค่าเป็น 1 จึงเรียก record `vtable+0x10` ที่ `0x007335AD`.
- R: read presence ที่ `0x007335C0`; ถ้า 0 ออกทันที, ถ้า nonzero จึง allocate record แล้วเรียก record `vtable+0x10` ที่ `0x0073360C`.

ดังนั้น logical wire order **เหมือนกันทั้งสองทิศ: presence ก่อน nested record**. ความต่างใน `PF_SERIALIZER_FIELDS.tsv` เป็นข้อจำกัดของการจัดลำดับไซต์ข้าม branch ไม่ใช่ wire order.

## Job 3 — `0x0072EC50` กับ indirect slot

- `CALL 0x0072EC50` อยู่เฉพาะ R branch หลังอ่าน presence nonzero. ฟังก์ชันเต็ม `[0x0072EC50,0x0072ED8C)` / 316 B / SHA-256 `74cb5c54f008b786fa03b93180464e8f93dac5935aae3cf2c33fdcaa2e908a87` เป็น pool allocator/constructor ของ record หนึ่งตัว; call site ส่ง `(0x00F0A90C,0)` กับ pool `0x0102F0F4`, ไม่ส่ง stream. มันติดตั้ง vtable `0x00F46C14`, initialize record และคืน pointer. **มันไม่ใช่ wire serializer.**
- Record vtable `[0x00F46C14,0x00F46C28)` SHA-256 `2940cedd8e099b667ac3342b60892462cfcb00c6c953a9f4f709abadb640f5d8`; slot `+0x10` ที่ `0x00F46C24` ชี้ตรงไป `0x0072E590`.
- ดังนั้น indirect `DEREF(DEREF(DEREF(OBJ+0x14))+0x10)` ที่ `0x007335AD` (W) / `0x0073360C` (R) คือ nested record serializer `[0x0072E590,0x0072E691)` / SHA-256 `5b714541671c8731a3b88df657089f97645ad1a6d2dc7ec9f06ee7ee271aa8f2` ที่ RE-227 พินไว้.
- W ไม่มี wire field คั่นระหว่าง presence กับ nested call. R มีเฉพาะ allocation + pointer replacement/refcount ก่อน nested call; ไม่มี byte/count เพิ่มบนสาย.

## Job 4 — จำนวน record และ vital_version

- Outer object มีขนาด `0x18`; constructor `[0x00732BC0,0x00732C13)` / SHA-256 `f3b540704035ab613eee7955f3c46655b920e90c985670af7ebb9056e13ef436` เขียน pointer เดียวที่ `+0x14 = NULL`. Codec ไม่มี loop/vector/count. จึงรับ **zero-or-one nested record ต่อ vital**, ไม่ใช่หลาย record.
- Constructor เดียวกันทำ `xor ecx,ecx` แล้ว `mov byte ptr [eax+0x10],cl` ที่ `0x00732BF4`: prototype version = **0**. Bootstrap เฉพาะคลาส `[0x00732F7B,0x00732FAA)` SHA-256 `30b6a9107ef75986701144bfc526345d2f18623ab3a88a2c9b8694113c846ed3` allocate 0x18 B, call constructor `0x00732BC0`, แล้ว register prototype ผ่าน `0x005F3DF0`.
- Generic VitalData reader `[0x005F3E20,0x005F406D)` SHA-256 `bfdf1ada48068e9a3838b51241e164677e0142a6ce0f6d68d547299fe279e217` อ่าน tagged version byte ที่ `0x005F3EF4`, แล้ว `cmp cl,byte ptr [esi+0x10]` ที่ `0x005F3EFC`; ผ่านเฉพาะ `je` ที่ `0x005F3F01`. ดังนั้นคลาสนี้ยอมรับ **vital_version = 0 เท่านั้น** แบบ exact equality.

## Verifier

- `staged/re256_addsurvey_outer_static_verify.py`
- SHA-256 `b9a400e48871a9a405a63eea7fc276e42f4dd46f0993344c0f140d60c7caa7f0`
- `python -B`: `RE-256 PASS: image/table hashes, 8 spans, presence=pointer-bool, one nested record, version=0`; exit 0.

## Nonclaims

1. ไม่อ้างว่า `0xC4AF` มีหลักฐานสองชั้น; static ใบนี้ไม่ decode runtime id-global และไม่เพิ่มพยานอิสระให้ msg id. ผลนี้ไม่พบข้อขัดแย้งใหม่กับชื่อคลาส แต่ control id ผิดโดยตั้งใจยังเป็น attended evidence แยก.
2. ไม่อ้างความหมาย gameplay ของ nested fields ที่ RE-227 คง opaque; พิสูจน์เฉพาะ outer framing, dispatch และ cardinality.
3. ไม่อ้างว่า presence byte เป็นจำนวน record แม้ค่าหนึ่ง record เท่ากับ 1; provenance เป็น `pointer != NULL` โดยตรง.
4. ไม่อ้างว่า parser ผ่านแล้วจะเปิดหน้าต่างบนจอหรือเปลี่ยนฉาก; client-observable และ server response อยู่คนละชั้นและต้องวัดใน GT.
5. ผลลบเรื่อง “ไม่มีไบต์คั่น” จำกัดเฉพาะ complete outer codec branch ที่พินและ call chain ก่อน nested serializer; ไม่ใช่ผลจาก linear-disassembler search ทั้งโปรแกรม.

## BUILD_IMPACT

**BUILD_IMPACT:** LANE-A ตั้ง `outer_leading_byte=1` เมื่อส่ง record หนึ่งตัว และคง `vital_version=0`. Wire หลัง vital header ต้องเป็น `0B 01` (outer presence) แล้วตามทันทีด้วย nested record ซึ่งเริ่ม `0B <record+0x10>`; **ห้ามใส่ record count เพิ่ม**. ค่า 0 ของ outer presence หมายถึงไม่มี nested record. ผลนี้ปลด `GT-233` เฉพาะ layout/version gate; การเปิดหน้าต่างจริง, msg-id control และผลต่อ M2 ต้องตัดสินใน attended round ตามใบเดิม.

สถานะที่ chief/LANE-A ควรกรอก: `RE-256 DONE/PASS — OUTER PRESENCE IS POINTER BOOL (ONE RECORD => 0B 01); ZERO-OR-ONE RECORD; NESTED SLOT+0x10=0x72E590; VITAL_VERSION=0 EXACT`.
