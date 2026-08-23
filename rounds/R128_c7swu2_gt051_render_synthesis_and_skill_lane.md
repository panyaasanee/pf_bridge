# R128 (session c7swu2) — GT-051 RENDER-SYNTHESIS เสร็จ · เปิดเลนสกิล GT-050/GT-052 · ใบใหม่ GT-053 · พักเลน attended ตามคำสั่ง Panya

**เวลา:** 2026-08-23 ~17:4x–18:2x (+07:00) · chief cloud บน Routine
**ล็อกรอบ:** draft PR #29 (pf_bridge) เปิดก่อนทำงานตามลำดับ v5 — ล็อกไม่หลุด · ไม่มี PR ค้างตอนเริ่ม (เช็คทั้งสอง repo)
**probe:** GitHub API/tool อ่าน+เปิด PR ได้ ✅ · ทาง D `ci-status` มีชีวิต ✅ (`d_exit=0` · อ่านคำตัดสิน `4f31956` = `success` run 32631974238 sha ตรง)

## จดหมายที่บริโภครอบนี้ (copy + stub ตามกติกา R108)

1. `20260823_1605_...` — หลุมศพชื่อไฟล์ (ผู้ช่วยเขียนเวลาผิดแล้วเปลี่ยนชื่อ ทำท่อหยุด 17:12–17:2x · เนื้อจริงอยู่ฉบับ 1656)
   จดหมายสั่งเองว่า "ไม่ต้องบริโภค" ⇒ **ไม่ copy เข้า consumed/** · วางเฉพาะ stub แบบ tombstone-ack กันรอบหน้าอ่านซ้ำ
   (pf-adversary จับว่าร่างแรกบริโภคเต็มรูปแบบขัดคำสั่งในจดหมาย — แก้แล้ว)
2. `20260823_1656_PANYA-DIRECTION-pause-attended-open-class-skill-lane.md` — **คำสั่ง Panya**: พักใบ eye-dependent ทั้งหมด ·
   เปลี่ยนวิธีเก็บหลักฐานเป็นวิดีโอต่อเนื่อง (ของเพิ่ม) · เปิดเลนอาชีพ/สกิล · ร่างใบ 3 ใบ
3. `20260823_1718_GT050-SCOPE-CUT-...md` — ตัดขอบเขต GT-050 เป็น "ตรวจแล้วใช้" (Codex ถอดแถวสกิลไว้แล้วใน `external/*.tsv`) ·
   กติกาใหม่: ก่อนถอดใหม่ต้องเปิด `external/*.tsv` ก่อนเสมอ

## งานที่ทำ

### ① GT-051 RENDER-SYNTHESIS-001 — ทำเองบน cloud เสร็จในรอบ (ตามลำดับที่ Panya เสนอ ข้อ ⑤.1)
- ลูกมือ pf-static-re สองตัวขนานกัน: ฝั่ง render-FAIL (GT-030/034/045) และฝั่ง render-SUCCESS (GT-022/027-029/031/032/038/039/043/048 + SCENE-005/OBJECT-POP-002 ก่อนยุค GT)
- ผลเต็ม: **`FINDINGS_R128_GT051_RENDER_SYNTHESIS.md`** (ฉบับหลังแก้ตาม adversary) — คำตอบ = สมมติฐาน
  **RENDER-DISCRIMINATOR-H1 ฉบับ identity-band**: ไคลเอนต์วาด entity จาก wire actor_entry เมื่อ identity อยู่ใน band
  native ของฉากที่โหลด (`0x2000+1..0x2000+N`) หรือตัวผู้เล่นเอง — **wire override ตำแหน่ง/template ได้** ·
  identity นอก band ไม่วาด (หลักฐานแข็งใบเดียว GT-030 · ติด confound actor_type 2)
- 🔴 **รูปแรงของร่างแรก ("wire = อัปเดตของ native ในที่เดิมเท่านั้น") ถูก pf-adversary หักล้างสำเร็จ** ด้วยรายงาน
  ยุคก่อน GT ที่การกวาดรอบแรกไม่ครอบ: ARENA V1 (วาด `0x201F` ที่พิกัดที่ wire กำหนด) และ SCENE-007 (วาด `0x203D`
  template 34 ใน scene 1 ที่พิกัด P144 ทั้งที่ index 60 ของ bg0001 = template 62 คนละตัว) — แก้ทั้ง FINDINGS/stub/GT-053 แล้ว
- จุดตรวจถูกสุด = GT-053: **band membership ของ scene 2 (N ≥ 61 ไหม)** — ไม่ใช่ identity/template match (เกณฑ์ร่างแรกวัดผิดแกน)
- ผลกระทบ: เลนดาเมจไม่กระทบ (overlay แยกเชิงพฤติกรรม) · เลนลูท GT-045 v2 = ตัวทดสอบข้างเคียง (bit 0x08 คนละชนิดเรคคอร์ด) ·
  multiplayer: งาน static ถัดไปต้องเปิดคำถามคู่ (identity band vs actor_type 2 dispatch) — รอผล GT-053 ก่อน

### ② คิว — แบนเนอร์ R128 + ใบใหม่ 3 ใบ + stub 1 (ร่างโดย pf-queue-author · chief ตรวจวาง)
- แบนเนอร์: พักใบ attended (GT-045 rerun/030/034/035/036) ห้ามปิด unattended · ข้อเสนอวิดีโอ ffmpeg+gdigrab ·
  เปิดเลนสกิล · กติกา external/*.tsv · **GT-045 v2 merge แล้ว (PR #10 · เขียว(Actions run 32631974238) · merge `e51bdac`) แต่พักตามคำสั่ง**
- **GT-052 CLASS-SKILL-TABLE-001** [STATIC-ON-BRIDGE] — ขยับเลขจากร่าง GT-049 ในจดหมาย (GT-049 ถูกใช้แล้วโดย R127)
- **GT-050 SKILLCAST-WIRE-001** [STATIC-ON-BRIDGE] ฉบับ scope-cut สี่จ็อบ (verify sha → re-derive ปฏิปักษ์ → ปิด CLearnSkillResultVital → ทิศทาง+ตัวจุดชนวน)
- **GT-051 stub DONE** — กันเลขห้อยลอย ชี้ไป FINDINGS
- **GT-053 SCENE2-NATIVE-IDENTITY-CROSSCHECK-001** [STATIC-ON-BRIDGE] — decisive ทั้งสองทางต่อ H1 ·
  จุดสำคัญที่ pf-queue-author จับได้: พิกัดใน scenario เป็นค่าสังเคราะห์ (`synthetic_p60_minus100x_minus50y_samez`)
  ⇒ ห้ามใช้ผลเทียบพิกัดตัดสิน H1 — ตัวชี้ขาดคือ placement index 60 + identity/template

### ③ pf-adversary — ตรวจทั้งชุดก่อน commit · **จับ defect จริง 7 ข้อ แก้ครบก่อน commit**

## อุบัติเหตุระหว่างรอบ (บันทึกไว้ตรง ๆ)
- cwd ของ shell หลุดกลับ `/home/user` หลัง wakeup ระหว่างรอลูกมือ ⇒ heredoc ต่อท้าย GT-053 ไปสร้างไฟล์หลงทาง
  `/home/user/GAME_TEST_QUEUE.md` (นอก repo) · จับได้จาก `wc -l` ผิดปกติ (98 ≠ ~2470) · ย้ายเนื้อหาเข้าไฟล์จริงแล้วลบไฟล์หลง —
  **คิวจริงไม่เสียหาย ไม่มีการลบเนื้อหาเดิม** · บทเรียน: คำสั่งหลัง wakeup ให้ใช้ absolute path เสมอ

## ไฟล์ที่แตะรอบนี้ (pf_bridge เท่านั้น — ไม่แตะ repo โค้ด)
1. `GAME_TEST_QUEUE.md` (แก้ — แบนเนอร์ + 4 entry ท้ายไฟล์ · ไม่มีการลบรายการเดิม)
2. `FINDINGS_R128_GT051_RENDER_SYNTHESIS.md` (ใหม่)
3. `rounds/R128_c7swu2_gt051_render_synthesis_and_skill_lane.md` (ใหม่ — ไฟล์นี้)
4. `notes_to_chief/FROM_CHIEF_R128_TO_ATTENDED_20260823_1830.md` (ใหม่)
5. `CHIEF_CONTINUATION.md` (ต่อท้ายหนึ่งบรรทัด)
6. stub การบริโภค 3 ใบ + สำเนาใน `consumed/` 2 ใบ (`notes_to_chief/` — 1605 เป็น tombstone-ack stub อย่างเดียว ไม่มีสำเนา)

## สิ่งที่รอบนี้ **ไม่ได้** พิสูจน์
- H1 เป็นสมมติฐาน — ยืนบนผลลบแข็งใบเดียว (GT-030 · แคบ) + NO-RESULT สองใบ · ยังไม่พิสูจน์ว่าเพียงพอ (GT-034 ค้าน)
- ไม่มีหลักฐานใหม่จากรอบนี้เลย — เป็นการสังเคราะห์ล้วน · เอกสารต้นทางคือหลักฐานจริงเสมอ
- ไม่ได้แตะโค้ดเซิร์ฟเวอร์ ไม่ได้รันเทสใด — ไม่มี claim "เขียว" ใด ๆ ในรอบนี้

## adversary verdict — 7 defect · แก้ครบ

1. **(สูง) FINDINGS สำรวจไม่ครบ** — ARENA V1 / SCENE-007 / SCENE-002..006 เป็น counterexample ของรูปแรง H1 ⇒
   เพิ่มเข้าตาราง ① · แก้ H1 เป็นฉบับ identity-band · แก้เกณฑ์ GT-053 เหลือ band membership (N ≥ 61)
2. **(สูง) GT-053 อ่าน provenance พิกัดกลับด้าน** — `synthetic_*` เป็นของตำแหน่ง*ผู้เล่น* · พิกัด entity คือ authentic P60
   (ledger GEO-PF-002) ⇒ ยกการเทียบ f32 triple ขึ้นเป็นตัว verify หลักของใบ แทนที่จะสั่งทิ้ง
3. **(กลาง-สูง) confound identity-band vs actor_type** — GT-030 ต่างจาก success สองแกนพร้อมกัน ⇒ เขียนลง ② ตรง ๆ ·
   A/B อนาคตต้องตรึง actor_type 4 · เลน multiplayer เปิดคำถามคู่
4. **(กลาง) GT-053 หายจากลำดับที่ค้างในแบนเนอร์** ⇒ แทรกเป็นหน้าสุดของกลุ่ม static
5. **(กลาง) stub GT-051 แรงเกินหลักฐาน** ⇒ เขียนใหม่เป็นภาษาสมมติฐาน + ระบุ confound + ระบุว่าการกวาดยุคก่อน GT อาจไม่ครบ
6. **(ต่ำ) บริโภคหลุมศพ 1605 ขัดคำสั่งในจดหมาย** ⇒ ถอน consumed/ copy · stub เปลี่ยนเป็น tombstone-ack
7. **(ต่ำ) จุกจิก** — GT-050 CLASSMAP 6,244 → "6,244 data rows (6,245 รวม header)" · GT-045 หัวใบ flip เป็น
   PAUSED-รอ-Panya + merge แล้ว (ธรรมเนียม R127) · GT-053 การนับ index เขียนใหม่ "index 60 เมื่อนับตัวแรกเป็น index 0" ·
   FINDINGS GT-030 ระบุระยะครบสองจุด (~33 / ~52)

**คำถามเปิดที่ adversary ทิ้งไว้ (จดเข้า FINDINGS ④ ข้อ 4 แล้ว):** wire วาด in-band identity ที่ template/พิกัดไม่ตรง native —
client ย้าย/เปลี่ยนสกิน object เดิม หรือสร้าง object ที่สอง (native ตัวเดิมยังยืนอยู่ไหม)? — ใบ attended อนาคต (พักตามคำสั่ง)
