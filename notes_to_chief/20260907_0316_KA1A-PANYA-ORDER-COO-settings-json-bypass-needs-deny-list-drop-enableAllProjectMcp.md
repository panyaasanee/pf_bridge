# PANYA-ORDER → COO · `.claude/settings.json` (bypassPermissions) ใช้ได้ แต่ต้องมี deny list + เอา `enableAllProjectMcpServers` ออก + พิสูจน์ในรอบจริง

ADDRESSEE: COO · cc: chief · ทุกสาย
FROM: ka1-A (มือเขียนแทน Panya) · ทาง: สะพาน
เวลาเคาะ: 2026-09-07 ~03:10 +07 · คำเจ้าของในแชท: "ส่ง" หลัง ka1-A ประเมิน PR `pf_bridge#1612` (merged) + `pirate-force-server#975` ที่ COO เพิ่ม `.claude/settings.json` (`permissions.defaultMode: bypassPermissions` · `permissions.allow` กว้าง · `enableAllProjectMcpServers: true`) เพื่อแก้อาการรอบแขวน "Needs your approval"

## ที่เจ้าของรับ
- ทิศทางถูก: แลก "ไม่ถามสิทธิ์" กับ "รอบไม่แขวน 60 นาที" คุ้ม เพราะทุกอย่างเข้า main ผ่าน PR + gate อยู่แล้ว

## ที่เจ้าของสั่งเพิ่ม (ทำในรอบถัดไป ทั้งสองรีโป PR เดียวต่อรีโป)
1. **`permissions.deny` เป็นตาข่าย** อย่างน้อย: `Bash(git push --force*)` · `Bash(git push -f*)` · `Bash(git push * --force*)` · `Bash(rm -rf*)` · `Bash(git reset --hard*)` · `Bash(git branch -D*)` · `Bash(git clean -f*)` · `Bash(git checkout -- *)` (ทับงานที่ยังไม่ commit) · การเขียนนอกรีโปทั้งสอง (`Write(~/**)`/`Edit(~/**)` ยกเว้นใต้รีโป) · `Bash(curl*)`/`Bash(wget*)` ยกเว้นที่ระเบียบอนุญาต (courier relay อยู่ใน environment ของมันเอง ไม่ใช่รีโป ไม่กระทบ) — กฎบ้าน "ห้าม force / ห้ามลบ / ห้ามอ่านนอกรีโป" ต้องอยู่ในไฟล์บังคับ ไม่ใช่แค่ใน prompt
2. **เอา `enableAllProjectMcpServers: true` ออก** — MCP ที่ทีมใช้ (GitHub · Claude_Code_Remote) ตั้งที่ตัว routine ไม่ได้มาจากรีโป · รีโปเป็น public: ถ้ามี `.mcp.json` เข้ามาทาง PR ใด ทุกเซสชันจะเปิดเซิร์ฟเวอร์นั้นเองโดยไม่มีใครดู · ถ้าวันหน้าต้องใช้ ให้ระบุชื่อเซิร์ฟเวอร์เป็นรายตัว (`enabledMcpjsonServers`) ไม่ใช่ all
3. **พิสูจน์ในรอบจริง 2 ข้อ แล้วรายงานใน COO-ROUND**: (ก) รอบที่มีคำสั่งเดิมที่เคยแขวน (อ่านไฟล์ tool-results นอกรีโป) ไม่แขวนแล้ว — หรือถ้า deny ข้อ 1 กันไว้ ให้เห็นว่าเป็น "ถูกปฏิเสธทันที" ไม่ใช่ "รอคนกด" (ข) deny ยังทำงานใต้ bypass จริง: สั่ง `git push --force` ไปกิ่งทดลอง (ไม่ใช่ main) ในรอบเดียวแล้วดูว่าถูกปฏิเสธ — ไม่พิสูจน์ = ยังไม่นับว่าตาข่ายมี
4. บันทึกใน `AGENTS.md`/`PROCESS_GATES.md` (เขต chief) ว่าไฟล์นี้คืออะไร ใครแก้ได้ (COO+chief ผ่าน PR เท่านั้น · สายอื่นห้ามแตะ `.claude/`) และเกต preflight ต้อง RED ถ้า PR ของสายอื่นแตะ `.claude/settings.json`

## ที่เจ้าของจะทำเอง (ไม่ต้องตาม)
- ผูก pf_bridge + pirate-force-server ในหน้า Edit ของทุก routine เพื่อให้ไฟล์นี้ถูกอ่านตั้งแต่เริ่มเซสชัน (ป๊อปอัป `register_repo_root` ใบแรก) — เมื่อสะดวก

## สิ่งที่เจ้าของไม่ได้เคาะ (อย่าขยาย)
- ไม่ได้อนุญาตให้ขยาย allow ไปยังคำสั่งใหม่ · ไม่เปลี่ยนกฎ "ห้าม merge/ปิด PR เอง" · ไม่แตะ milestone

ใครทำอะไร: COO แก้ settings.json ทั้งสองรีโปรอบถัดไป (ข้อ 1–2) + พิสูจน์ (ข้อ 3) · chief ข้อ 4
