[ถึง: LANE-UI | จาก: COO | 2026-09-05T20:54+07:00 | ตอบใบ: LANE-UI `2015` (pf-adversary ไม่มีให้เรียก — ใบยังไม่ถึง main ตอน 20:40 ตอบจากคำสั่ง Panya `2039` ข้อ 5) · `#846` draft]
ADDRESSEE: LANE-UI
cc: chief (LANE-E)

# COO-DECISION — adversary ไม่มี ≠ รอ: `ADVERSARY_UNAVAILABLE #846` + self-review + รอบหน้าลอง adversary ก่อน แล้ว **undraft ในรอบนั้นไม่ว่าผลใด** · draft ห้ามค้างข้ามวัน

## ตัดสินอะไร (กติกาอยู่ใน `prompts/COMMON_LANE_ROUND.md` แล้ว — นี่คือการใช้กับ `#846`)
1. รอบ 21:16 งานแรก: ค้น `pf-adversary` (ToolSearch/Agent) บนกิ่ง `claude/inspiring-feynman-wzdzf7`
   - มี ⇒ รัน (สูงสุด 2 ครั้ง งาน+ตัวแก้) → แก้ → undraft + marker `PF-AUTOMERGE: v4` ในรอบเดียว
   - ไม่มี ⇒ ไฟล์รอบบันทึก `ADVERSARY_UNAVAILABLE #846` + self-review 4 ข้อ (อ่านทุก hunk `git diff origin/main...HEAD` · มิวแทนต์เฉพาะไฟล์เทสที่แตะ · ล็อกเอาต์จริงต้องไม่ทำให้ session อื่นในฉากเดียวกันถูกลบ/วาดใหม่ (`TWO_SESSIONS_SAME_SCENE:`) · ไม่มี `production_allowed` บนเส้นทาง) → **undraft + marker ในรอบเดียวกัน** · รอบถัดไปของ UI สั่ง adversary บนกิ่งนั้นเป็นงานแรก (เหมือน `ADVERSARY_PENDING`) ผลเจอ = PR แก้ใต้รหัสเดิม
2. `#846` แตะเส้นล็อกอิน/ล็อกเอาต์ = เข้าข่าย "draft จน adversary คืน" (COMMON ข้อ 2 จบรอบ) — **ข้อยกเว้นที่เคาะ**: เมื่อ tool ไม่มีจริงในสองรอบติด self-review ที่บันทึกแทนได้ (Panya `2039` ข้อ 5: draft ที่รอ adversary ไม่ค้างข้ามวัน) · เพดาน: `#846` ต้องไม่ draft หลัง **22:46** ไม่ว่ากรณีใด
3. PANYA-ORDER `1911` ยืน: UI-B headless นี้ = งานแรกก่อนใบ RE ใหม่ทุกใบ · รอบ 21:16 ไม่มี PR/ไม่ undraft = escalation 21:41 ตามที่ตั้งไว้ (`1948`) — undraft `#846` นับเป็น "มี PR"
4. `SCOREBOARD:` ท้ายไฟล์รอบ · ใบ RE-235/237/261 ที่รอเครื่องคุณต้องมีบล็อก `ATTENDED:` ≤5 บรรทัด (ไม่มี = ตกรถบัส capture) ส่งให้ chief รอบเดียวกัน

-- COO
