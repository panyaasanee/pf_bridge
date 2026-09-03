จาก: กะ3-A (attended · Panya ขับ UI เอง) · ถึง: chief (cc COO · สาย A · สาย B)
วันที่: 2026-08-30T00:30+07:00 (TZ=Asia/Bangkok date)
เรื่อง: ผลรอบรวม GT-131 (PASS เจ้าของยืนยัน) + GT-151 (PARTIAL) + 4 ช่องโหว่งานขัด + คำถามเจ้าของเรื่อง mob/npc สลับที่

## ข้อมูลรอบ
attended · Panya ขับเอง · jobs 1351-1354 · 00:00-00:27 (+07:00) ใต้เพดาน
BOOT_COMMIT `cf1f63f6f16a70c1d3b17210e91338b7b73528fd` = main HEAD (code-delta 0 · verdict success) · **บูตไร้แฟล็กจริง** (guard ตรวจ cmdline)
canonical `4FF37060…8454` เท่าเดิมก่อน-หลัง · teardown 1353 PASS (listeners/clients/ffmpeg 0 · integrity ok · FK 0)
วิดีโอ `1352_b131151_FULLROUND_20260830_000047.mkv` + FRAME proof 3 · ภาพเจ้าของ 4 ใบ `GameClient\Data\ScreenShot\20260830_00{0311,0741,1047,1423}.png` · 🔴 ห้ามลบ

## ① GT-131 — ✅ **PASS** (`OBSERVER_CONFIRMED: 2026-08-30T00:2x+07:00` โดย Panya คำต่อคำ: "ตำแหน่ง npc ถูก ตัวถูกต้อง ฉันให้เทสนี้ผ่าน")
ชั้น client-observable (ตาเจ้าของ · ภาพนิ่ง full-res):
- ท่าเรือ: **"Marine Transport Station / Columbus"** และ **"Royal Navy / Loie"** ขึ้นตรงตำแหน่ง ⇒ P1/P2 สมอของเจ้าของ **ยืนยันครบทั้งสอง** (จุดที่เคยเป็น Sebastian คือ Columbus แล้วจริง)
- ลานดอกไม้/ปืนใหญ่: **"Guild Administrator / Hields"** + **"Guild Assistant / Sase"** + **"Skill Trainer / Nayar"** + Training Iron Man
- ย่านร้าน: **"Illustrations Appraisers / Chalais"** + **"World Artist / Da Vinci"** + **"Herdsman / Aisha"**
- ท่าเรือฝั่งเรือเหลือง: **"Onboard Engineer / Saben"** + **"Sworn / Juliet"** · target panel เปิดได้ (Deserter Navy / Mackie HP 100)
⇒ ไม่พบชื่อเก่านอกกลุ่ม 13 placement ที่ใบระบุว่าเป็นของถูก
ชั้น wire (บูตเดียวกัน): `WORLD_CENSUS_INITIAL_108` + `WORLD_CENSUS_REAPPLY_108` · `undressable=7` · `ceiling=108/115` ตรงคำทำนายใบ · เฟรม `V98_NPC_FACE_PLAYER_POSITION_HEADING_*` และ `V98_NPC_CONVERSATION_DEFAULT_*` ออกจริงที่ P8/P50/P35/P109

## ② GT-151 — 🟡 **PARTIAL** (ไม่ปิดใบ)
- จุด **P0 (Navy Transfer เดิม, ห่างจุดเกิด ~100)**: ภาพจุดเกิดแสดงบริเวณนั้น**ไม่มีใครยืน** และมีตัวคุมชัด (Columbus/Loie ยืนใกล้ในเฟรมเดียวกัน) ⇒ สอดคล้องคำทำนาย "ว่าง"
- อีก 6 จุดไม่ได้เดินไปตรวจ ⇒ เขียนว่า **ไม่ได้ตรวจ** ตามกติกาใบ ห้ามเดา
- ชั้น wire ของใบครบแล้ว (`undressable=7 … ceiling=108/115`) — ที่ขาดคือชั้นจอ 6 จุด ยกไปรอบถัดไป

## ③ ช่องโหว่งานขัด 4 ข้อ ที่เจ้าของสั่งให้ "โน้ตไว้ แก้ค่อยเป็นค่อยไประหว่างสำรวจแมพต่อ ๆ ไป" (ไม่ใช่ใบด่วน)
1. **ชื่อ NPC เป็นสีเขียวทุกตัว** — สีเขียวสื่อว่าเป็นผู้เล่นอื่น · NPC ควรเป็น**สีเหลือง**
2. **หุ่นซ้อม Training Iron Man ยังไม่ใช่ mob ชื่อแดง** ทั้งที่ควรเป็น
3. **NPC ทุกตัวยืนหันหน้าไม่ถูกทิศ** (แม้เฟรม FACE_PLAYER_POSITION_HEADING จะออกจริงในบูตนี้ — ช่องว่างอยู่ระหว่างเฟรมที่ส่งกับท่าที่ client วาด)
4. รวม ๆ = **attr ยังไม่สมบูรณ์** ตามหลักการ `PANYA-DECISION 20260828_0125` (actor ทุกชนิดต้องส่ง attr ครบที่สุดเท่าที่รู้)
🔴 ทั้งสี่ข้อ **ไม่กระทบผล PASS ของ GT-131** — เป็นงานเก็บรายละเอียดที่เจ้าของอนุญาตให้ทยอยแก้

## ④ คำถามเจ้าของ (ขอสาย A/สาย B ตอบด้วยหลักฐาน ไม่ใช่ความเห็น)
**จุดเดียวกัน (ท่าเรือฝั่งเรือเหลือง) รอบก่อนเป็น mob `Jungle Tiger` วันนี้เป็น NPC `Sworn / Juliet` — อะไรทำให้ต่างกัน?**
[สมมติฐาน กะ3-A — ยังไม่พิสูจน์] รอบก่อนเป็นบูตที่ยังส่ง identity แบบเก่า (เลข Mob-Set ของไฟล์ฉากลงช่อง MOBS n_ID) ⇒ placement ได้ identity จากบล็อก 36-66 = roster Spice Paradise ซึ่ง `Jungle Tiger` อยู่ในบล็อกนั้นพอดี (ดู `PANYA-EVIDENCE 20260827_1020` §②) · รอบนี้บูตหลัง CLINE resolve ⇒ ได้แถว MOBS ที่ resolve จริง = NPC ของ Port Royal
⇒ ขอสาย A ยืนยัน/หักล้างจากโค้ดและตาราง (ถ้าจริง นี่คือหลักฐานตรงว่า CLINE เปลี่ยนตัวตนของ placement ทั้งชุด ไม่ใช่แค่ชื่อ) · 🔴 เรื่อง mob→npc นี้อาจอธิบายอาการ MOBS-ANSWER-AS-NPC ที่ค้างอยู่ด้วย

## ⑤ บันทึกความตั้งใจของเจ้าของสำหรับรอบหน้า
เจ้าของลืมเก็บผลหน้าต่างแผนที่ (`M`) รอบนี้ — **จะเก็บแถมในบูตใบถัดไป** พร้อมข้อสังเกตของเจ้าของว่า "ผลใน M ไม่น่าเกี่ยวกับว่าเซิร์ฟเวอร์สร้าง NPC หรือไม่ เพราะมันติดมากับ client ทุกรอบอยู่แล้ว" — บันทึกเป็นข้อสังเกต ยังไม่ใช่ข้อสรุป

ลงชื่อ: กะ3-A
