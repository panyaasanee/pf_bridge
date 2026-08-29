[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-107 RESULT — DONE / DEATH-BRANCH-MODEL-GATE-BOUNDED

- เวลาเริ่มใบ/ปิดใบ: `2026-08-27T17:01:48+07:00` / `2026-08-27T17:11+07:00` (Gregorian, +07:00)
- หมวด: `STATIC-ON-BRIDGE` เท่านั้น — ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, ไม่แก้ source/queue
- อิมเมจ: `GameClient\GameClient.local.bin` · 14,759,424 B · SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- input หลัก: `CLIENT_RE_QUEUE.md` `0f04061378c69ab3ede55c9e3e9532c537dc88ba417d29594c849b9b8ef55a7c`; GT-084-R2 result `242247...341a`; Panya original-server reference `d3b79b...0b32`
- วิธี: PE section mapping + SHA-pinned spans + recursive CFG; ไม่ใช้ linear disassembly เป็นหลักฐานผลลบ

## ช่องบังคับก่อนถอด

- **ค้น `pf_bridge\external\` แล้ว:** manifest 30 files, fingerprint `42010a39b31acfb7b5770b899cee15f01e759eabf4cf13827373e28ce3e27ae1`. คำค้น `BasicAttr|NPCAttr|_F_DIE_000|death|dying` เจอ 4 ไฟล์ (`PF_FIELD_VALIDATION.tsv`, `PF_PROTOCOL_PRIORITY.tsv`, `PF_PROTOCOL_REGISTRY.tsv`, `PF_SERIALIZER_FIELDS.tsv`) — เจอ registry/field ของ `BasicAttr`/`NPCAttr` แต่ **ไม่พบ death animation, picking removal หรือ crosswalk ที่ผูก name/faction กับการเล่นคลิป** ภายใน corpus นี้.
- **ค้น `gamedata` แล้ว:** manifest 1,109 files, fingerprint `8a87a0ddc5f76f33145b3140fdfc58d0ee5a3178905595f02715eb87c26d68d0`. คำค้น `_F_DIE_000|s_ANIMATION|Tornado Eagle` เจอ 6 ไฟล์; `CONSTDATA_TH__BEHAVIOR.tsv`/`BUFF.tsv` มีคลิป `_F_DIE_000` หลายแถว และ MOBS id 31 คือ model class `M011`, preset `M011_000_000_SP3`, lv27. แต่ **ไม่มี crosswalk ว่า preset นี้รองรับ/ไม่รองรับ literal `_F_DIE_000` ที่ task ขอ**; แถว data จึงไม่ใช่ execution proof.

## T0 — ด่านคุม

image SHA/size ตรง pin. Verifier ใหม่ `staged/re107_mob_death_static.py` SHA-256 `2a4fb50a3691c43b562ec239c86e0754a6776345778ed0c45c1e262924731394` รันผ่านทั้งหมด (`RESULT=PASS failures=0`).

## T1 — predicate ไม่อ่าน name / mask / faction

recursive CFG ครบทั้งสองฟังก์ชัน:

- `0x43BD70..0x43BD9D` SHA `1df3c62b4bbe0aab1ebf1404320a7b2466ef20390db060e67ba183a1178127aa` — 45/45 B
- `0x43BDA0..0x43BDD2` SHA `04e08d24980faf23e0bcb7d9e6f1e69dfdba704abfedf6a8531ceeedbb5e8866` — 50/50 B

ทั้งคู่เรียก actor vt+`0x74` เอา resident BasicAttr, require `[attr+0x44] == 0` แล้วอ่าน `f32 [attr+0x58]`; ต่างกันเฉพาะ `<=0` (dead task) กับ `>0` (dying latch). **ไม่มี read ของ name, faction หรือ wire mask ใน CFG ใด**. ดังนั้น named+hostile body กับ unnamed/non-faction body ไม่แยกกันที่ predicate คู่นี้.

## T2 — จุดเลือกท่าตายและ gate จริง

- apply/death sync `0x4437C0..0x443A9A` SHA `85d294b84843e0bd46256e0257cf5d51be0415081739d82b0b4c254975ee9592`, recursive CFG 730/730 B, ถึง ctor `0x472810` ของ `CActorTask_Dead` เมื่อ HP=0 และ timer<=0.
- task update `0x472850..0x4728F3` SHA `e04385a8cd54b800add22c4c8c5cc751b4243e19d208d684acdb8af2b6350999`, CFG 163/163 B: ที่ `0x47289E` ทดสอบ `[actor+0x70] & 0x40`; เฉพาะเมื่อ set จึงส่ง literal `L"_F_DIE_000"` (`0xF0F060`) เข้า actor vt+`0x28`.
- รายงาน byte-exact เดิม `PF_HP_DEATH001...` (SHA `3df84dd1665168c306baf8f8223dcde176cb3d947e1037ea6c3dfdf6b5af0233`) census writer ของบิต `0x40` ได้เพียง `0x4448B4`/`0x4599B4` และระบุเป็น **model-loaded gate**. ชื่อ/faction ไม่ป้อน gate นี้.

คำตอบ static ที่ชี้ขาด: **server field ที่คุมสอง state มีแค่ HP/timer; การขอคลิปจริงมี gate เพิ่มเป็น client-local model-loaded bit.** `DEAD` มาเร็วหลัง `DYING` ไม่ได้สร้าง branch ที่ข้ามชื่อ/faction; แต่ static ไม่เห็นค่าบิตจริงของ actor `0x201F` ตอนเกิดเหตุ และ data corpus ไม่ยืนยันว่า preset M011 resolve `_F_DIE_000` สำเร็จ จึงไม่ claim ว่า gate นี้เป็นสาเหตุ runtime.

## T3/T4 — picking vs render และ bounded negative

ครบทั้ง `CActorTask_Dead` update CFG แล้วไม่พบ call ไป actor-map resolver `0x446170` หรือ inserter `0x446990`; task ยังเดิน model/render pointers ต่อ. จึง **ไม่พบ actor-map removal ใน task ที่เล่นท่าตาย**. แต่การที่ cursor ไม่จับอาจเกิดจาก pick filter ที่เห็น actor เป็น dead ซึ่งอยู่นอก CFG นี้; static ชุดนี้แยก “ถูกถอดจาก logic list” กับ “ยังอยู่แต่ pick filter ปฏิเสธ” ไม่ได้โดยไม่เดา.

attended capture ที่แคบที่สุดถ้าต้องแยก timing ออกจาก model/clip: ใช้ identity/preset/body เดิมของ `0x201F`, รอจนคลิก/ล็อกเป้าได้แล้ว ส่ง **DEAD actor-entry (HP=0,timer=0) เพียงเฟรมเดียวโดยไม่มี DYING positive-timer ก่อนหน้า** และเก็บ raw bytes + จอ. ถ้ายัง freeze ⇒ ตัด 700-ms DYING→DEAD cutover ออก เหลือ model-loaded/clip/pick path; ถ้าล้ม ⇒ sequencing เป็นตัวแปรจริง. ห้ามเปลี่ยน name/faction พร้อมกัน เพราะ static พิสูจน์แล้วว่าสอง field นี้ไม่ถูกอ่านใน death predicates/task gate.

## nonclaims

- ไม่ claim ว่า `DEATH_TASK_HOLD_MS=700` เป็นสาเหตุหรือไม่เป็นสาเหตุ; เพียงไม่พบ client branch ที่อ่านค่านั้น.
- ไม่ claim ว่า visual preset M011 ไม่มี `_F_DIE_000`; corpus ปัจจุบันไม่มี crosswalk นั้น.
- ไม่ claim ว่า actor ถูกลบจาก picking list; พิสูจน์ได้เพียงว่า complete dead-task update CFG ไม่เรียก actor-map resolver/inserter.
- ไม่เอา actor identity จากตำแหน่ง/ชื่อมาจับคู่แทน wire crosswalk และไม่อ้างกฎของ original server.

## BUILD_IMPACT

`BUILD_IMPACT: NONE` — งานนี้ static/read-only. ถ้าจะสร้าง diagnostic รุ่นถัดไป ให้แยกเป็น profile `DEAD-only after model-ready` ของ identity เดิม ห้ามแก้ 700 ms และห้ามเปลี่ยน name/faction พร้อมกัน.

## read-only integrity

- before: image/external/gamedata fingerprints ตามหัวจดหมาย
- after ณ เวลาปิดใบ: image SHA ยัง `962721...b623`; ตาราง MOBS/BEHAVIOR/BUFF SHA `3c0d33...916b` / `79ee11...bf4e` / `a84266...89eb7`; ไม่มี source input ถูกแก้
