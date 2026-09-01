# PF runtime class map

A6 อ่าน minidump ทั้งสองแบบ read-only และส่งออกเฉพาะ address/name/structure/count/SHA metadata; ไม่มี raw dump byte, memory value หรือ hexdump ในผลลัพธ์

## Result

- complete dump-native `vtable[-4] -> Complete Object Locator -> hierarchy -> TypeDescriptor` chain: 0
- จึงไม่มีแถวใดที่อนุญาตให้ผูก `vtable_va` กับ `class_name` จาก DUMP ล้วน; ไม่ใช้ IMAGE หรือความใกล้ของสตริงเติมชื่อ
- TypeDescriptor ที่ตรวจโครงสร้างได้ยังถูกรักษาเป็น `TYPE_DESCRIPTOR_UNBOUND` พร้อม `type_descriptor_name`/VA/file offset จริงจาก DUMP และ `instance_count=0`; `class_name` ยังคง `UNKNOWN` เพราะชื่อนั้นยังไม่ถูกผูกกับ vtable

## Per dump

| dump | SHA-256 | threads | modules | memory ranges | exact TypeDescriptors | mapped candidate slots | COL+first-entry mapped | COL signature zero | proven chains |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `GameClient.local.bin_1.41.01_69151_20260816_040609.dmp` | `daf63c7d13dc7ca601776cc7e4abbf02aa2e367f91ea420b3b05aaa8af7bffdc` | 43 | 101 | 335 | 3121 | 26231 | 944 | 68 | 0 |
| `GameClient.local.bin_1.41.01_69151_20260816_042854.dmp` | `f982d47b6cec71171ccd2129ee9ce955a0cca05a9d5b606b0c97d5dd28169904` | 48 | 101 | 339 | 3121 | 26244 | 949 | 66 | 0 |

## Why names remain unbound

ทั้งสองไฟล์เป็น `MiniDumpWithDataSegs` (`flags=0x1`) ที่มี MemoryList แบบเลือกช่วง: พบ TypeDescriptor ในช่วงที่ถูกเก็บ แต่ทุก candidate ที่ผ่าน COL signature ยังขาด TypeDescriptor/hierarchy/base-array linkage อย่างน้อยหนึ่งช่วงภายใน memory ของ dump จึงหยุดก่อนผูกชื่อเสมอ นี่เป็น operational evidence ของ snapshot สองไฟล์นี้ ไม่ใช่คำอ้างว่า executable ไม่มี RTTI

## TSV contract

- ทุกแถว `source=DUMP` และอ้าง dump เดียว
- `VTABLE_CLASS` จะเกิดได้เฉพาะ full x86 MSVC RTTI chain ภายใน dump เดียว; รอบนี้มี 0 แถว
- `TYPE_DESCRIPTOR_UNBOUND` เก็บ exact decorated RTTI name ใน `type_descriptor_name` แต่ `vtable_va=UNKNOWN`, `class_name=UNKNOWN` และ `instance_count=0`
- `SUMMARY` หนึ่งแถวต่อ dump บันทึกผลลบโดยไม่สร้างชื่อหรือ vtable สมมุติ
