# [CONSUMED โดย chief รอบ 104 — 2026-08-20 14:2x]

ฉบับเต็ม: `notes_to_chief\consumed\20260820_1410_ORDER-fix-actions-selfcheck-exitcode.md` (ไม่ได้ลบ · sha ตรงกันยืนยันแล้ว)

**บริโภคไปทำอะไร (จบครบในรอบเดียว — commit `6bd1b95` job 166 allGreen):**
- แก้ `SELF-CHECK` step ใน `.github/workflows/gate-windows.yml` — ปิดท้ายด้วย `exit 0` + คอมเมนต์เล่าเหตุ (ตรงตามที่สั่งทุกบรรทัด)
- **audit ทั้งไฟล์ตามคำสั่ง "อย่าแก้จุดเดียว":** ไม่มี step อื่นเป็นบั๊กเดียวกัน — `cp874 static tripwire` จบด้วย throw-guard ที่ success path ทิ้ง `$LASTEXITCODE=0` · `THE GATE` จบด้วย `exit 0/1` ชัดเจนอยู่แล้ว (runbook ก็จดกฎนี้ไว้เองแต่ step SELF-CHECK ไม่ได้ทำตาม) · step ที่เหลือจบด้วย cmdlet ไม่ใช่ native
- `README_GATE_CI.md`: เพิ่ม postmortem run #1 + ติดป้าย RESOLVED บน blocker `.gitignore` (ปิดโดยรอบ 103) + หมายเหตุ supersede ใต้ "NOT proven" (setup steps วัดบน runner จริงแล้ว · steps หลัง SELF-CHECK ยังไม่เคยรัน)
- จดตามคำสั่ง: **run #1 ไม่นับเป็นข้อ 5 ของเช็คลิสต์** — deliberate red ยังค้าง ลำดับ เขียวก่อน → แดงจงใจ → เขียวกลับ
- **ไม่ push** — Panya push เอง · จบรอบทันทีตามคำสั่ง 12:30 ไม่หยิบงานอื่น
