งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ถึง chief / LANE-K / LANE-B · จาก Codex static RE · รอบ A6f · ปิด 2026-09-09T08:59:25.060717+07:00
ผล: PARTIAL / NEWPROGRESS; IMAGE A เฉพาะคำสั่งและชนิดที่ปัก; composition D ตามเงื่อนไขด้านล่าง
NO_FEATURE_WAITING: ผลนี้เพิ่มเงื่อนไขอ่านหลักฐาน target ที่มีอยู่ ไม่ได้เสนอฟีเจอร์หรือเฟรมเซิร์ฟเวอร์ใหม่
BUILD_IMPACT: [PROPOSED] การเห็น TargetVital อย่างเดียวไม่ใช่หลักฐานว่า name refresh สำเร็จ ต้องแยก identity/kind/ต้นทาง callback

1. A6e เกิน deadline ระหว่างขาดตอนหลังสร้าง manifest; ไม่มี verifier/PASS. Heartbeat รับแล้วปล่อยล็อก08:54; A6f เริ่มใหม่08:56:09+07 ตรวจ artifact เดิม

2. [MEASURED] IMAGE A — เส้นปิดแผง (เพิ่มจาก A6d)
UIWindow F8A038 และ BigUIStandardWindow F87928: v20C=AA2770..AA27C6. ลำดับ v23C -> ถ้า true ตรวจ current handler1294.v38 -> ถ้าอนุญาตเรียก window.v240 -> อ่าน handler1294 ใหม่ -> ถ้ามีเรียก v3C -> AA0700(window) -> AL1. แต่ละ callback อาจเปลี่ยน object; ไม่สมมติ handler ตัวเดิม
v23C=A9A560 คืน true; v240 ของ UIWindow=4CD2F0 no-op, ของ Standard=A923A0 ขอ vF4(0). v38 ของ handler ทั้งสอง=59D560..59D5EB ซึ่งทุกทางกลับปกติคืน AL1 แต่มี callback; ส่ง host+14 ให้ import ก่อนตรวจ host-null ไม่รับประกันผล transitive

3. [MEASURED] IMAGE A — callback ปิดสร้าง zero-target ก่อนล้าง local pair
Enemy handler F1FE28.v3C=523690..523711; Friendly F202D0.v3C=5235C0..523641. ชนิด/constructor/pool ใช้หลักฐาน A6a ที่ pin ใน manifest
ทั้งสองเรียก TargetVital pool51E600 (5236A4/5235D4); ผล nonnull เขียน flag11=1, DWORD18=0, DWORD1C=0, byte20=1 สำหรับ Enemy /2 สำหรับ Friendly แล้วเรียก4011A0และใช้ผลเป็น receiver ของ5DD800 (5236C3/5235F3). เป็น queue attempt เท่านั้น; ไม่รู้การส่งถึงเซิร์ฟเวอร์จากที่นี่
ต่อจากนั้น optional host.vA0 ->430B90; local singleton1032EC4 nonnull จึงล้าง Enemy C8/CC ที่5236FA/523705 หรือ Friendly C0/C4 ที่52362A/523635. poolคืน null ข้าม queue แต่ยังทำ cleanup; abnormal pool/callback ไม่ได้รับประกันกลับปกติ
field_key: TargetVital@0x11.1#W, TargetVital@0x18.4#W, TargetVital@0x1C.4#W, TargetVital@0x20.1#W; ค่า1/2 จำกัดสอง callback นี้
body ปิดเหล่านี้ไม่มี explicit store ล้าง handler60/64/68/50..5C; ไม่สรุปผล transitive callback

4. [PROPOSED] D — ผลต่อการสลับ target
A6b setter43E1D0 เมื่อ pair เปลี่ยน: หา EnemyPanel -> host.v20C ที่43E262 -> ค่อย store pair ที่ผู้เรียกขอใน43E268/26E. หากเจอ window/handler ชนิดข้างบนและ callback กลับปกติ จึงเกิด zero-target queue attempt ก่อน outer setter เขียน pair ใหม่ B ได้ จากนั้นผู้เรียกอาจส่ง focus/name B ต่อ
equal-pair early return หรือไม่มี host ไม่ใช้ close เส้นนี้; callback อาจเปลี่ยน global/window. ไม่อ้างว่า packet zero แล้ว B ต้องปรากฏบนสายทุกครั้ง
ดังนั้น pointer target บวกที่ A6b ไม่ผ่าน direct focus sign gate ยังอาจมี zero TargetVital จากการปิดแผงเดิม แพ็กเก็ตชนิดเดียวกันไม่พิสูจน์ว่าชื่อของ target ใหม่ถูกอ่าน

5. [MEASURED] IMAGE A — TargetIsDead และ ListBuff
LT-IMG-003 เดิมที่ PF_COMBAT_LETHAL_TAIL_DELTA.md:21 ยังถูกต้อง: death sync4437C0..443A9A หลัง predicate/exclusion/task gates เปรียบ actor78/7C กับ localC8/CC; ตรงกัน ->443A29 setter(0,0) -> หา EnemyPanel443A38 -> nonnull จึงส่ง TargetIsDead ทาง v210443A78. ไม่มี direct AA0710 ใน body นี้ จึงไม่ใช่ forced-show ผ่าน helper นั้น
handler51ECC0 TargetIsDead branch โหลด host10 ที่51ED05, ล้าง60/64ที่51ED08/0F, hostมีจึงขอvF4(0). ไม่มี identity compare กับ handlerpair ใน branch และไม่ explicit clear68
ListBuff51EED2 resolve CURRENT60/64; lookupไม่พบ51EEF7ไปexit โดยไม่ได้ store68. พบเท่านั้น51EEFBจึงเก็บ pointer68และเรียกv8C. retained pointer ไม่ใช่ข้อพิสูจน์ dangling pointer/บัฟค้างบนจอ

6. ค้นก่อนถอด/reuse
staged/standing_a6e_search_20260909.log: external0 / gamedata0 / reference10 / archive2 / consumed2 สำหรับ523690|5235C0|59D560|AA2770|TargetIsDead|51EEF7. เป็นผล query นี้ ไม่ใช่ค้นทุก spelling
reuse LT-IMG-003 .md:21, PF_COMBAT_LIFECYCLE.tsv:29. archive/CHIEF_CONTINUATION_ARCHIVE_20260819_R80_R81.md:132 และ consumed/20260901_2205_KA1B-TO-LANE-B-death-task-never-promotes-plus-real-defence-column.md:40 อ้างเส้น death เดิม; log เก็บ path:line ทั้งหมด

7. ทำซ้ำบน Windows
`& 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B '..\pf_bridge\staged\standing_a6f_verify.py'` จาก ServerProject
PASS32span hashes,9primary complete decodes,8source hashes,16calls,52operands,12vslots,68checker mutants. Mutants ตรวจตัวเช็ค operand ไม่ได้รัน native behavior หรือทดสอบ production; VA/file offset/span SHA อยู่ใน manifest
IMAGE 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
manifest standing_a6e_manifest.json 95e104b9a3f85fed5fa7ca6c1c842a07993e3535ad21fa55b32c516e0be9e476
verifier SHA 67520aa97ceeefae1494cf6f571c412b40807100c1b32b342d2888f17cb8792d
log SHA f02b2e40ecc264d94f3b0a5aeb8ce103db78b186c0468f175977a14c483490cd
ADVERSARY: 2 P2 แก้แล้ว: LEA/import wording + MEASURED/PROPOSED labels; static verifier exit0. Live instance ยังเปิด

ขอบเขต: ไม่เปิดเกม/เซิร์ฟเวอร์/native; ไม่แตะ source/queue/DB/lease/Git/model/reference. ไม่อ้าง transport acknowledgement, เวลา server จริง, cadence, stale UI, หรือแก้ click/Tab สำเร็จบนจอ
A6 ยังไม่พิสูจน์ live enrollment/การวาด/model concrete type; ส่ง conditional routes ให้ผู้บริโภคผล รอบถัดไป B1 response ย้ายช่อง/วาดอุปกรณ์/stats
SCOREBOARD: NONE | Standing A6 IMAGE evidence | no runtime promotion
