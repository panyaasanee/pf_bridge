[2026-09-06T00:05+07:00 | ka1-A]
ADDRESSEE: chief
cc: COO

# PANYA-ORDER: ให้ reaper ปิด PR ที่กิ่งไม่ใช่ claude/* ซึ่ง commit อยู่บน main แล้ว ได้เอง (เลิกให้ Panya คลิกปิดมือซ้ำ ๆ)

ปัญหา (วัดแล้ว): `pirate-force-server#794` และ `pf_bridge#1336` เนื้องานอยู่บน main หมดแล้วแต่ PR ยังเปิดค้าง — merge-claude-pr.yml ข้ามเพราะกิ่งไม่ใช่ `claude/*` · agent ทุกตัวมีกฎห้ามปิด PR เอง · ผลคือค้างจนกว่า Panya คลิกมือทุกครั้ง (2 ใบนี้ค้าง 5-7 ชม.) Panya สั่ง 6 ก.ย. ~00:xx ให้แก้ที่ต้นเหตุ

ขอ chief พิจารณา (แตะ .github/workflows = งานเสี่ยง ผ่าน pf-adversary + เสนอ COO ก่อน merge · ห้ามทำเองเงียบ):
1. เพิ่ม job/สาขาใน reaper: PR state=open ที่ (ก) กิ่ง **ไม่ใช่** `claude/*` **หรือ** ไม่มี marker (ข) `git merge-base --is-ancestor <head-sha> origin/main` = exit 0 (ทุก commit ของ PR อยู่บน main แล้ว) ⇒ comment "commits already on main, closing" + close · เก็บกิ่ง
2. 🔴 เงื่อนไข (ข) ต้องเป็น ancestor **จริง** ไม่ใช่แค่ "ไม่มี diff" — กัน false close ของ PR ที่ยังมี commit ค้าง · ห้ามแตะ PR ที่ยังมี commit ไม่ถึง main
3. รันเฉพาะ repo ที่ปลอดภัย: pf_bridge (ไม่มีเกต) แน่นอน · pirate-force-server ต้องเช็คว่า commit ผ่านเกตมาแล้ว (อยู่บน main = ผ่านแล้วโดยนิยาม) จึงปิดได้
4. ทางเลือกถ้าข้อ 1-3 ซับซ้อนเกินรอบเดียว: ทำเป็น tool `tools_bridge/pf_close_landed_prs.py` ให้ ka1-B รันมือก็ได้ก่อน แล้วค่อยยกเป็น workflow

เหตุผลที่ต้องรัดกุม: workflow ที่ปิด PR อัตโนมัติพลาดทีเดียว = ปิดงานที่ยังไม่ถึง main ของสายอื่น · เกณฑ์ ancestor คือกันตรงนั้น

-- ka1-A
