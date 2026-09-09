งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
[ถึง: chief / LANE-K และสายอุปกรณ์ร่วม LANE-B · จาก: Codex RE runner]
เวลาเริ่ม 2026-09-09T09:38:37.353949+07:00 · B1d · ปิด 2026-09-09T09:52:51.588614+07:00
ผล PARTIAL / NEWPROGRESS: 26ช่อง Char_Info2 + typed inputs + ActorAttr stat gates; เฟรม equip→stat ยังไม่ปิด

[MEASURED][IMAGE A] เส้นทางของตัวละคร
- CNetActor ctor457340→443160: pool43F3D0→4679F0/vtableF0E8E0 ใส่ actor+24C ที่4433B1; pool43F2B0→64A160/vtableF36E80 ใส่ actor+248 ที่4433CF. Net ctorสร้าง ActorAttr ผ่าน456D20→464BE0/vtableF0E7A0 ใส่ actor+348 ที่4573CA
- Net.v2C=43B7F0; My.v2C=448E80→43B7F0. หลัง5FBA00 และเมื่อ actor+24C ไม่เป็นnull: push actor+248, เรียก actor.v74=44C630 ซึ่งคืน actor+348, แล้ว9F1990ใส่ FightAttr+14/+18 ตามลำดับ. inputอาจnull; ไม่พิสูจน์ callback/lifetimeจริง
- FightAttr.v34 และ v18=515EC0 มีเพียง ret8: ช่องนี้ไม่มี wire payload ของค่าพลัง. CBuffAttr.v34=64A430 เป็นคนละ codec และรับรายการ record; offset aggregate ที่สูตรอ่านไม่ใช่ช่อง wire ตรง ๆ

[MEASURED][IMAGE A + DATA] CharInfoEventHandler v2C=5839E0 เรียก57E1D0 เมื่อ localplayer1032EC4มีค่า; 57E1D0อ่าน player+24C และหยุดเมื่อ FightAttrเป็นnull. binder584150→AA1750 ผูกชื่อ control ผ่าน typecheckก่อนเก็บ pointer; จับคู่กับ GameClient/Data/GUI/Model/Char_Info2.model ได้ครบ26ชื่อแบบหนึ่งต่อหนึ่ง
ตารางตัวอย่าง (offsetของ handler / getter / ID):
84 / 467A60 / LABEL_STR; 88 / 467AF0 / LABEL_CON; 8C / 467B80 / LABEL_DEX
90 / 467CA0 / LABEL_INT; 94 / 467C10 / LABEL_PER; AC / 467E60 / LABEL_SPEED
B0 / 468340 / LABEL_MC; B4 / 468250 / LABEL_AC
B8 / 467F80 / LABEL_MATK; BC / 467E90 / LABEL_ATK
ครบ26ช่องและVAใน manifest.bindings
- ค่า integer ใน branchปกติส่งเข้า widget+220 และตั้ง byte+218=1; ชนิด DATA คือ BigUINumberLabel. ค่า floatอีกกลุ่มผ่าน894D20 ด้วย %.2f หรือ %.2f%s แล้วเรียก widget.v128; DATA เป็น UILabel. default DATA ไม่ใช่ค่าจริง
- ทุกจุดในตารางมี gate pointerของwidget. MC/AC/MATK/ATK และอีกบางช่องมี branchเมื่อ handler+1B9!=0 ที่บวกค่าของ handlerเองก่อนแปลงเป็นinteger. ค่า UI จึงไม่เท่ากับ getter ทุกสถานะ
- ใช้สูตร29ตัวเดิมจาก external/PF_ATTR_COMPUTED_SEMANTICS.tsv ตรวจhashซ้ำครบ. ตัวอย่าง STR ใช้ ActorAttr WORD82+WORD182+global103382C และ CBuff D4/158; ATK ใช้ผล STR ร่วม CBuff EC/16C และ branch NPC. ขอบเขตนี้พิสูจน์ client computation ไม่พิสูจน์ server damage authority

[MEASURED][IMAGE A] ฟิลด์ stat ที่ ActorAttr.v34=466230 อ่าน
หลัง BasicAttr codec4656F0: mask64 tag32/8 ลง1B4/1B8 แล้ว flag byte tag05/1 ลง1BC. ฟิลด์10ตัวข้างล่างอยู่หลัง branch4667E4..E7 ซึ่งข้ามทั้งกลุ่มไป466A61เมื่อ1BC=0; นอกจาก flag ต้องมี bit ของ maskต่ำ1B4ด้วย ทุกตัว tag12/2 และสูตรอ่าน unsigned WORD:
STR: +82 bit20 (call46684E), +182 bit40000 (4669C6)
CON: +84 bit40 (466869), +184 bit80000 (4669E4)
DEX: +86 bit80 (466884), +186 bit100000 (466A02)
INT: +88 bit100 (4668A2), +188 bit200000 (466A20)
PER: +8A bit200 (4668C0), +18A bit400000 (466A3E)
ตัวเลขทั้งหมด hex. นี่คือ read contract ของ child Attr ไม่ใช่เฟรมเต็ม; ยังไม่พิสูจน์วิธีรักษาฟิลด์ที่ไม่ได้ส่งตอน apply/copy

ค้นก่อนถอด: staged/standing_b1d_search.log ชุดแรก MD/PY matched lines external3/gamedata0/reference3/archive15/consumed1; ชุดเสริมค้น FightAttr|CBuffAttr|LABEL_ATK ใน TSV/MD/PY พบ25/0/23/11/9ไฟล์ตามลำดับ. พบสูตร/attachmentเดิมและ UI getter ของrefresh6CFC90; เพิ่มชื่อช่องของ57E1D0; ไม่ใช่global negative
แก้หน่วยในจดหมาย B1c 20260909_0938: 18/0/19/7/2 เป็นจำนวนบรรทัดตรงคำค้น ไม่ใช่จำนวนไฟล์; หลักฐาน Binary และผลอื่นคงเดิม 

BUILD_PROPOSED: ต่อผล GT-272 โดยจับค่าพลังก่อน/หลัง equip จากข้อมูลต้นทางที่มีหลักฐาน และตรวจช่อง Char_Info2 ตามcrosswalkนี้ พร้อมรักษาค่า/ตัวตนเดิม | สายอุปกรณ์ร่วม chief/LANE-B | token: FRAME_SHA+identity+ค่าต้นทาง+26ช่องที่เกี่ยวข้องก่อนหลัง+bag/appearanceคู่กัน; ยังไม่มี token และยังต้องปิด CBuff record→aggregate/apply กับ partial-preservationก่อนเลือกเฟรม
[PROPOSED D] งานต่อ B1e: ไล่ CBuff read/copy→aggregate และ ActorAttr apply เพื่อกำหนด candidateที่ไม่ล้างข้อมูลอื่น; หยุด trialเมื่อค่าที่ไม่เกี่ยวข้องเปลี่ยนหรือรูป/identityหลุด. ผู้บริโภคเปิดใบสร้าง+GT เมื่อcandidateพร้อม

หลักฐาน IMAGE 14,759,424ไบต์ SHAก่อน=หลัง
9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
VA/file-offset/ช่วง/hash และ7source hashes: staged/standing_b1d_manifest.json
004fff8645fee074b223126865218d52c04d013431583d0d46c6a9275529fc16
ช่วงครึ่งเปิดหลัก: 43B7F0..43B835, 57E1D0..57F42A, 584150..58573D, 466230..466C79
Re-run: Python314 -B staged/standing_b1d_verify.py → PASS70 spans/31 decoded ranges/83calls/95operands/10vslots/26bindings/10stat gates/29formula spans; ตรวจbyteไม่รันnative
ADVERSARY: /root/a6f_review ตรวจ frozenชุดนี้และ26lookup/typecheck/store ซ้ำ; verifier exit0 ไม่พบข้อผิดพลาดสาระสำคัญ. apply-preservation/rendering/equip→stat ยังไม่พิสูจน์
NONCLAIMS: ไม่มีภาพจริง/equipสำเร็จ/original reply policy/packetที่ผ่านเกม/damage authority/persistence. ไม่มี server/client invocation หรือแก้ DB/Git/ServerProject/queue/reference. Runtimeไม่ได้สำรวจใหม่
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
