[ถึง: chief / COO / สาย A · cc Panya | จาก: RE runner | 2026-08-27T01:56+07:00]

# RE-093 RESULT — PASS (bounded negative at T0): bg0001 has one 149-record placement block, not 113+36

## คำตอบสั้น

สมมติฐาน “มี placement block ที่สอง 36 records” ไม่จริงกับ raw นี้. เลข `113` คือ **definition count**, ส่วนเลข `149` คือ **placement count ของ block เดียว**. parser เดิน 149 variable-length records แล้วชน EOF พอดี จึงไม่มี byte เหลือสำหรับ block ที่สอง

## Layout ที่พิสูจน์จาก raw

| item | ค่า |
|---|---:|
| version | `2` |
| definition count | `113` |
| placement-count offset | `0x11C8` |
| placement count | `149` |
| first placement | `[0x11CA,0x122B)` |
| last placement | `[0x6B72,0x6BD7)` |
| raw length / parser end | `0x6BD7` / `0x6BD7` |

definition แรก/สุดท้ายคือ `Mob_Set_01` / `Mob_Set_113`; placement สุดท้ายอ้าง `Mob_Set_113` และ resolve template id `113`. Derived TSV มี 149 rows และ row สุดท้ายจบ `0x00006BD7` ตรงกัน

ดังนั้น T1–T3 ที่สั่งให้ decode “บล็อก 36 ตัว” เป็น **N/A เพราะบล็อกนั้นไม่มี** ไม่ใช่งานค้าง. ห้ามเอา `MOBS.n_ID=159` (Hields) หรือ `796` (Sase) มา join กับ definition/placement ordinal เพียงเพราะเป็นเลขเหมือน/ใกล้กัน; raw ไม่มี field crosswalk เช่นนั้น

## ค้นสองที่ (บังคับ)

- **ค้นใน `pf_bridge\external\` แล้ว:** ไม่เจอ schema/crosswalk สำหรับ “second placement block”, Hields หรือ Sase; เจอเพียง ancillary inventory/evidence ของ resource ใต้ `bg0001` ซึ่งไม่ใช่ decoder ของ `.npc`
- **ค้น `gamedata` แล้ว:** เจอ parser `pf_decode_lua_npc.py`, scene index และ `bg0001.placements.tsv` ที่แยก `definition_count=113` ออกจาก `placement_count=149` และบังคับ exact EOF; ทั้งสามแหล่งตรงกัน

## Verifier / integrity

- `pf_bridge\staged\re093_bg0001_no_second_block.py` SHA256 `8340b02f7e3c98e9d0e4606c8ff1893b664990e17aa4d27c40b792243f16fe43`
- รันสองรอบ: `SUMMARY guards=16 failed=0`, exit `0` ทั้งสองรอบ
- raw ก่อน/หลัง: length `27607`, SHA256 `026bbe32ca2b69853b1433d585de7e80bb67e7f713e086b9347fd10ad1dc2070`
- parser ก่อน/หลัง: `6ab38fd52079bf31fc0c355b49063043d55a2a14a60bb33d5fe3cacb2fcccf9e`
- derived TSV ก่อน/หลัง: `2e5b4115169160d609289d0e638e953d7da16a0000e267c12c118c7c1a4cfc5f`
- scene index ก่อน/หลัง: `c4016cf685671d4c7bbb1909bb300146afd802dd6b53f2d5e7b928249f26652d`

## BUILD_IMPACT

อย่าสร้าง “อีก 36 NPC” จาก `149-113`. ทั้ง 149 คือ placements ใน block เดียวที่ reuse 113 definitions ได้. ถ้าต้องการผูก Hields/Sase/Columbus กับ placement ใด ต้องเปิดใบจาก crosswalk field จริงหรือ client-observable evidence ไม่ใช่ ordinal arithmetic

## Nonclaims

- ไม่ได้บอกว่า Hields/Sase/Columbus มีหรือไม่มีในฉากจากชื่อ definition; พิสูจน์เฉพาะโครงสร้าง block
- ไม่ได้ระบุ HUD coordinate ของ Hields/Sase และไม่ได้ assign service role ให้ placement ใด
- ไม่ได้ใช้ผล “ไม่พบ second block” ขยายเป็น “ไม่มี NPC อีก 36 ตัวในเชิง gameplay” — มี placements 149 จริง แต่ไม่ใช่สองบล็อก
- ไม่ได้ใช้ linear disassembler

