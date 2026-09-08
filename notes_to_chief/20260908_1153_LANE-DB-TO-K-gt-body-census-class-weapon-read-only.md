ADDRESSEE: LANE-K
cc: COO · chief (LANE-E) · ka1-A
FROM: LANE-DB รอบ `21lxm6` · 2026-09-08T11:53+07:00
ประเภท: เนื้อใบ attended (gt-body) — สั่งโดย COO `20260908_0542` หัวข้อ 4

# เนื้อใบ: census `characters.class_id` + แถวอาวุธ — **อ่านอย่างเดียว ไม่เขียนอะไรเลย**

## ทำไมต้องขึ้นรถบัส
PANYA ติ๊กข้อ 4 (`20260908_0025`) ว่า migration แก้อาวุธของตัวละครเก่าต้องรัน **ใต้ `LOCK_GAME`
พร้อม backup** · ก่อนจะมีใครรัน migration นั้นได้ ต้องรู้ก่อนว่า **มีกี่แถวจะถูกแตะ** — และ
canonical DB อยู่บนเครื่องเจ้าของเท่านั้น โคลนคลาวด์ไม่เคยมีสำเนา ⇒ ตัวเลขนี้วัดจากคลาวด์ไม่ได้
ใบนี้ **ไม่ใช่** ใบรัน migration · ใบนี้คือใบ "นับ" ที่เปิดฐานด้วย `mode=ro` ผ่าน file: URI
⇒ โพรเซสเขียนไม่ได้แม้จะสั่งให้เขียน (มีเทสพิสูจน์ว่า `DELETE` โยน `OperationalError`)

## ATTENDED:
1. บูตด้วยทรี `origin/main` ปัจจุบัน ไม่ต้องเปิดเกม ไม่ต้องล็อกอิน ไม่ต้องถือ `LOCK_GAME` (อ่านอย่างเดียว)
2. รันคำสั่งเดียว: `python -m pirateforce_foundation.persistence_class_weapon <path ของ state.sqlite3 จริง>` (ตั้ง `PYTHONPATH=src`)
3. ดูอะไร: บรรทัด `CLASS_WEAPON_CENSUS_CLASS ...` หนึ่งบรรทัดต่อคลาส + `CLASS_WEAPON_CENSUS_SUMMARY ...` บรรทัดสุดท้าย
4. ผ่าน = มีบรรทัด SUMMARY และ `writes_performed=0 read_only=YES` · **ไม่ผ่าน** = โพรเซสตาย หรือ `sha256` ของไฟล์ `.sqlite3` ก่อน/หลังไม่ตรง
5. ส่งกลับ: ก๊อปทุกบรรทัดที่ขึ้นต้น `CLASS_WEAPON_CENSUS` + `sha256` ก่อน/หลัง มาที่ `notes_to_chief/` จ่าหน้า `ADDRESSEE: LANE-DB`

HEADLESS_PROOF: `CLASS_WEAPON_CENSUS_SUMMARY classes=5 characters=6 rows_to_change=3 writes_performed=0 read_only=YES` — วัด 2026-09-08T11:4x+07 บนกิ่ง `claude/festive-tesla-21lxm6` (ตัดจาก `origin/main` `a92086c` วันนี้) ด้วยฐานชั่วคราวที่สร้างตัวละคร 6 ตัวผ่าน `FoundationSession.create` จริง แล้วขยับ `class_id` 6 ตัว/เปลี่ยน template อาวุธ 1 ตัว/ลบแถวอาวุธ 1 ตัว · ตัวเลขขยับตามแถวจริง (`rows_to_change=3` ไม่ใช่ศูนย์ที่พิมพ์ไว้ในสตริง — เทส `test_the_numbers_move_with_the_rows` เป็นตัวจับ) · โค้ดอยู่ใน PR ของรอบนี้ ยังไม่ขึ้น main ⇒ 🔴 **K อย่าเพิ่งจัดคิวจนกว่า PR จะขึ้น main แล้ว ka1-A รันโทเคนเดิมซ้ำได้ตรง** (กฎ `0159`)

บรรทัดต่อคลาสที่วัดได้ในรอบนี้ (จากฐานชั่วคราว ไม่ใช่ฐานเจ้าของ):
```
CLASS_WEAPON_CENSUS_CLASS class_id=1  name=Gladiator   characters=2 weapon_ok=2 weapon_wrong=0 weapon_missing=0
CLASS_WEAPON_CENSUS_CLASS class_id=2  name=Paladin     characters=1 weapon_ok=0 weapon_wrong=1 weapon_missing=0
CLASS_WEAPON_CENSUS_CLASS class_id=4  name=Sniper      characters=1 weapon_ok=0 weapon_wrong=1 weapon_missing=0
CLASS_WEAPON_CENSUS_CLASS class_id=16 name=Necromancer characters=1 weapon_ok=0 weapon_wrong=1 weapon_missing=0
CLASS_WEAPON_CENSUS_CLASS class_id=32 name=Sorcerer    characters=1 weapon_ok=0 weapon_wrong=0 weapon_missing=1
```

## สิ่งที่ใบนี้ไม่ได้อ้าง
- **ไม่ client-observable** ไม่มีจอ ไม่มีเฟรม ไม่มีใครเห็นอะไรบนหน้าจอจากใบนี้ — เป็นใบวัดขนาดงาน
- ไม่ได้อ้างว่ารู้จำนวนตัวละครจริงในฐานเจ้าของ · นั่นคือสิ่งที่ใบนี้ไปถาม
- ไม่แตะ canonical DB · ไม่ขอ `LOCK_GAME` · ไม่ขอ backup (ไม่มีอะไรให้ย้อน)
- คลาสที่ตารางอาวุธไม่รู้จักถูก **นับ** เป็น `weapon_missing` + `name=UNKNOWN` ไม่ทำให้โพรเซสตาย (เทสจับไว้)
