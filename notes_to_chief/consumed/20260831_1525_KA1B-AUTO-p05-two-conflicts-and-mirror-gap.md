[ถึง: chief เพื่อ dispatch | จาก: กะ1-B (อัตโนมัติ) · 2026-08-31 15:25]

# ใบตีความ generation `105cc7692579f079` (P0-5)

Codex ส่ง checkpoint ของตัวเองไว้แล้วที่ `20260831_2202_CODEX-CHECKPOINT-P05-COMBAT-LIFECYCLE.md` และใบอัตโนมัติของ digest อยู่ที่ `20260831_1520_CODEX-NEWGEN-105cc769-*` — ใบนี้ไม่เล่าซ้ำ เอาเฉพาะสิ่งที่**ตรวจกับโค้ดที่รันจริงแล้ว**และสิ่งที่ chief ต้องตัดสินใจ

## 1) เลน B (combat) — `ActionVital+0x30` เติมช่องที่ทีมบันทึกว่า "unproven" ด้วย predicate ที่แน่นอน

ทีมบันทึกเองใน `mob_combat.py` (MOB_COMBAT_NONCLAIMS บรรทัด 336-338) ว่า "the inbound half is unproven" และผมตรวจแล้วว่า `attack_from_observed_action` (mob_combat.py:1633-1680) อ่านแค่ `field_qword_20` เป็น target — **ไม่มีการเช็ค `+0x30` เลย** ตรงตามที่ Codex ชี้ (conflict `4d48dc31…`)

ของใหม่ที่ Codex ปิดได้ (ชั้น IMAGE ทั้งหมด):
- inbound `ActionVital+0x30` เป็น **behavior selector**
- ค่า valid ต้องผ่าน lookup `0x00702A10` ก่อน client สร้าง `CActorTask_UseBehavior` ที่ `0x0047AB30`

nonclaim ของแถวนี้: จำกัดเฉพาะ cited path — ไม่ใช่คำตัดสินว่า parser ทั้งระบบผิด และ**ไม่พิสูจน์**ว่า original server เคย validate แบบเดียวกัน; exact equipment-dependent choice ยังเปิด

ข้อเสนอ: ตามรายงาน §A แถว 3 — เมื่อได้สิทธิ์แก้ server ค่อยทำ fail-closed validation หรือ shadow log ที่ผูก `+0x30` กับ equipped state; ระหว่างนี้แค่บันทึกว่า nonclaim "inbound half is unproven" ของทีม**ยังจริงครึ่งเดียว** — รูปร่างฝั่ง client รู้แล้ว ที่ยังไม่รู้คือ input จริงจะยิง shape นี้ไหม

## 2) เลน B — CHitResult flags: โค้ดที่รันวันนี้ส่งค่าที่เข้า reaction lane ของ client ไม่ได้

ตรวจแล้ว: `mob_combat.py:323-324` allowlist มีแค่ `0x0000`/`0x0001` และจุด emit (เช่น :1004) ส่ง `FLAGS_HIT=0x0001` จริง. Codex (conflict `bb8832a5…`, evidence `5787cd57…`) ปิด reaction branch ฝั่ง client ที่ต้องการ `(flags&0x0001)!=0 && (flags&0x0008)!=0 && (flags&0x0010)==0` — ค่า `0x0001` เดี่ยว ๆ เข้า branch นี้ไม่ได้แน่นอน

nonclaim สำคัญ (ห้ามข้าม): **ไม่พิสูจน์**ว่า `0x0009` คือ original policy และ**ไม่พิสูจน์**ว่า branch นี้ควรเกิดทุก hit. [สมมติฐาน] GT084-R2 เคยเห็น target flinch ทั้งที่ส่ง `0x0001` — ถ้าจริงทั้งคู่ แปลว่า reaction lane ที่ Codex ปิดเป็นคนละ lane กับ flinch ที่เคยเห็น; อย่าเพิ่งแก้ค่าคงที่ ให้คง conflict เปิดตามที่รายงานแนะนำ

## 3) การถอนใน §0 — กระทบเราน้อย แต่ต้องรับทราบ

Codex ถอนการอ่าน flat pose ว่าเป็น `_F_DIE_000` และถอน "ศพแข็ง/ท่าตายช้า" จากการเป็นหลักฐานลำดับ original (GT-025: `DYING_LATCH` เดี่ยว ๆ ก็ให้ flat pose ได้). ตรวจแล้วโค้ดทีมไม่เคย claim เรื่องนี้ — `mob_death.py:108,905` เขียนไว้เองว่า `_F_DIE_000` "has never been observed" — จึง**ไม่มีโค้ดหรือคำตัดสินที่ต้องแก้** แค่ห้ามใครหยิบท่าศพไปอ้าง ordering ในอนาคต

## 4) ต้อง chief ตัดสิน — ตาราง P0-5 ตกหล่นจากท่อส่ง GitHub

`PF_COMBAT_LIFECYCLE.tsv` (41,063 bytes) และ `.md` (2,423 bytes) อยู่ใน manifest และผ่าน sha256 แล้ว แต่**ไม่ถูกมิเรอร์**เข้า `notes_to_chief/reference_codex_attr/` เพราะ `tools_bridge/pf_attr_conflict_digest.py` บรรทัด 61 กรองด้วย prefix (`PF_ATTR_`, `PF_A2_`, `PF_A3_`, `PF_A6_`, `PF_ERRATUM_`) — ชื่อ `PF_COMBAT_*` ไม่เข้าเงื่อนไขสักตัว ทีมฝั่ง GitHub จึงยังไม่เห็นตาราง 34 แถวของ P0-5 เลย

แก้ได้บรรทัดเดียว (เพิ่ม `"PF_COMBAT_"` เข้า MIRROR_PREFIXES) แต่เป็น tooling ของท่อส่ง ผมไม่แก้เองโดยไม่มีคำสั่ง และไม่ copy มือเข้า mirror เพราะ C-09 ของ Codex ระบุว่า packaging ต้อง owner-approved. หมายเหตุ: C-09 ที่บอกว่า mirror ค้าง generation เก่าและขาด selector TSVs นั้น**ล้าสมัยบางส่วนแล้ว** — `PF_ATTR_NAME_COLOR_SELECTOR/QUEST_MARK_SELECTOR/ROLE_DISCRIMINATOR.tsv` มิเรอร์แล้วรอบนี้เพราะขึ้นต้นด้วย `PF_ATTR_`; เหลือค้างจริงคือคู่ `PF_COMBAT_*` กับสามไฟล์เกิน 2 MB เดิม

## ไม่ส่ง probe request รอบนี้ (จงใจ)

lifecycle blockers 8 แถวต้องการ original S2C timing/producer proof ซึ่ง headless `probe x y` ให้ไม่ได้ และ `C-07` (`FightAttr +0x54` concrete owner) Codex ระบุเองว่าต้องการ typed owner/RTTI ไม่ใช่ attended probe — จึงไม่มีรายการใดผ่าน intake gate ทั้ง 4 ข้อ; คิว probe อยู่ที่ 0 ตามเดิมโดยถูกต้อง ไม่ใช่ตกหล่น

-- กะ1-B (อัตโนมัติ)
