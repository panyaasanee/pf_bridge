# PANYA-DECISION → COO · ให้ LANE-Q ทำ "แผนที่ host API → ระบบ → มี/ยังไม่มี" (เคาะ 2026-09-06 ~17:00)

ADDRESSEE: COO (ยกลง NOW → Q รอบถัดไป) · CC: chief, LANE-Q
FROM: ka1-A (มือเขียนแทน Panya) · ช่องทาง: บุรุษไปรษณีย์ (เครื่อง Panya ปิด · ส่งทันทีตามกฎ owner-order)
เวลาเคาะ: 2026-09-06 ~17:00 +07 (โดยประมาณ) · คำ Panya ในแชท: "เคาะเลย" ต่อข้อเสนอด้านล่าง

## สิ่งที่ Panya เคาะ
ให้ LANE-Q ผลิตแผนที่ 1 ชุด: **ทุกฟังก์ชัน host API ที่สคริปต์ gamedata/lua (616 ไฟล์) เรียก → ระบบ server ที่ต้องมีอยู่หลังฟังก์ชันนั้น → ตอนนี้มี/ยังไม่มี** เพื่อให้ COO ใช้จัดลำดับว่าสร้างระบบไหนก่อนจึงปลดล็อกเควสได้มากที่สุด

## เหตุผลของ Panya (จากบทสนทนา ใช้ตีความงาน)
- เธอถาม "ถ้าเครื่องยนต์จากสคริปต์เสร็จหมด เกมจะเกือบสมบูรณ์ไหม" — คำตอบที่เธอรับ: ไม่ · 160 ฟังก์ชันเป็น "ประตู" เข้าหาระบบ หลังประตูต้องมีระบบจริง (CastSkillAt = ระบบต่อสู้ทั้งระบบ ไม่ใช่ฟังก์ชันเดียว) และของใหญ่ (สูตรต่อสู้ · AI มอน · ดรอป · เรือ/กะลาสี · สัตว์เลี้ยง · ตีบวก · กิลด์ · เมล · แผงลอย) ไม่ผ่านสคริปต์เลย
- เธอต้องการเห็นว่าสคริปต์ที่ได้มา "ช่วยให้งานเขียน server พัฒนาตรงไหน" — คำตอบ: มันคือรายการระบบของ server เดิมพร้อมสัญญาการเรียก (ชื่อ/อาร์กิวเมนต์/ค่าคืน) · แผนที่นี้ทำให้รายการนั้นจับต้องได้และวัดได้

## สเปกส่งมอบ (Q ทำในรอบเดียว · อ่าน src/ ได้ ไม่ต้องแก้โค้ดใด ๆ)
ไฟล์ 2 ไฟล์ใน pf_bridge (หรือที่ COO กำหนด ถ้าเขตเขียนของ Q ไม่ครอบ): `LUA_HOST_API_MAP.tsv` (เครื่องอ่าน ≤64 KB) + `LUA_HOST_API_MAP.md` (คนอ่าน ≤12 KB)

คอลัมน์ TSV 1 แถวต่อฟังก์ชัน:
1. `fn` (เช่น Player.AddItem) · 2. `namespace` · 3. `call_count` (นับจาก 616 ไฟล์) · 4. `files` (จำนวนไฟล์ที่เรียก)
5. `hook_side` = UI (พบเฉพาะใน OpenAcceptUI_Run/OpenReportUI_Run) / AUTH (Accept_*/Report_*/Delete_Run/Trigger*/Instance*/ScriptStart) / BOTH
6. `args_returns` (จาก gamedata/PF_LUA_API_SPEC.md + src/…/lua_api/api_spec.tsv)
7. `system` = ระบบ server ที่ต้องมี: inventory · exp-level · cash · buff · spawn · combat-skill · instance · teleport-warp · store · storage · party · guild · ship · flag-quest-state · timer · movie-ui (client-only) · อื่น ๆ ระบุชื่อ
8. `status` = REAL / STUB / MISSING — วัดจาก script_host.py + lua_api/* จริง อ้าง ไฟล์:บรรทัด ห้ามเดา
9. `system_exists` = YES (อ้างโมดูล server) / PARTIAL / NO
10. `blocker` สั้น ๆ: "ต้อง RE เฟรม X" / "ต้องระบบ Y ก่อน" / "client-only ทำ no-op+log" / ว่าง
11. `milestone` ที่ระบบนั้นสังกัดใน NOW (ถ้ามี)

กติกา:
- ตัวเลขทางการ = census ของ Q เอง (`gamedata/pf_lua_api_census.py`) · ka1-A นับด้วย regex 6 namespace ได้ 152 ชื่อ (Player 73 · Quest 34 · Trigger 18 · Mob 10 · Instance 9 · Scene 8) ส่วนทีมเคยพูด 160 — ให้ Q อธิบายส่วนต่างในบรรทัดเดียว
- ฟังก์ชันที่ `hook_side`=UI ล้วน (วัดแล้ว: Mob.ShowAnimation 499 · Quest.PlayNPCMovie 100 · Quest.PlayNPCVoice 4 พบเฉพาะใน OpenAcceptUI/OpenReportUI) = client วาดเอง ฝั่ง server ทำเป็น no-op ที่ log ได้ — ให้ระบุชัดใน status/blocker ไม่นับเป็นงานค้าง
- `.md` เรียงตาม system แล้วภายใน system เรียง call_count มาก→น้อย · ท้าย `.md` ใส่ตาราง 1 ใบ: system → จำนวน fn → รวม call_count → system_exists → ขนาดงาน S/M/L (1 บรรทัดเหตุผล) — บรรทัดนี้คือสิ่งที่ COO ใช้จัดลำดับ
- ไม่สร้าง/แก้ฟังก์ชันใดในรอบนี้ · ไม่แตะ NOW.md (COO ยกเอง) · จบรอบด้วย SCOREBOARD: NONE | … ตามปกติ

## สิ่งที่ COO ต้องทำ
1. ใส่ NOW ให้ Q รอบถัดไป = LUA_HOST_API_MAP (แทนงานอื่นของ Q 1 รอบ)
2. เมื่อได้ไฟล์: ใช้ตารางท้าย `.md` จัดลำดับระบบใน milestone แล้วสรุปให้ Panya ≤10 บรรทัดใน notes_to_chief (ka1-A จะเล่าต่อในแชท)

## สิ่งที่ Panya ไม่ได้เคาะ (อย่าขยาย)
- ไม่ได้สั่งเริ่มสร้างระบบใดเพิ่ม · ไม่เปลี่ยน milestone · งานเครื่องเธอยังเลื่อนตามจดหมาย 1645 (ไม่มีหน้าต่างก่อน 22:00)
