# R230 (roj9lp) 2026-08-29T18:05+07:00 — ต่อสาย CORE-REQUEST 2 ใบ + countersign ตาราง + GT-063 PASS

## ทำอะไร

1. **CORE-REQUEST สาย A (ใบ 1546)** — เติมคีย์เวิร์ดที่สาม `departed_from=` ที่ call site
   `dispatch_columbus_quest3021` ใน `runtime.py` (บรรทัดเดียวกับสองคีย์ของใบ 1422 ที่ R229 ต่อไว้)
   ส่ง `self.foundation.selected.position` (แถวในหน่วยความจำที่ census/travel gates/checkpoint อ่านอยู่แล้ว)
   ครอบ guard `None` นอกเหตุผล refuse — AttributeError ที่หลุดจาก try จะพา listener thread ตาย (v141:7440 ไม่มี except)
   ผล: บรรทัด `WORLD_M2_RETURN_LEG` พิมพ์ `source=departed_row ... drift=NNN.N` แทน
   `drift=unmeasured:call_site_passed_no_departure_row` · เทสใหม่ 1 ใบขับ dispatcher จริง
2. **CORE-REQUEST สาย B (ใบ 1600)** — สาขา census `Bg0002` ใน `runtime.py`:
   ใน `try` เดียวกับ `build_bg0002_population` ต่อ `mob_census_hostility.hostile_override_for_scene_id`
   (🔴 ไม่ส่ง ledger ตามใบ — ตอน login ledger ของบูตคือ roster ของ bg0001 ส่งไปแล้ว
   `full_roster_override` โยน `MobDeathContractError` — วัดโดยสาย B เอง) + `_apply_mob_death_census_override`
   และพิมพ์ `describe_census_hostility` ใน `else` **เสมอ ไม่อยู่ใน if** (บทเรียน GT-084)
   วัดจริง headless: `MOB_CENSUS_HOSTILITY scene_id=2 scene=Bg0002 roster=12 backed=12 unbacked=none`
   เทสไบต์สามใบเดิมอัปเดตให้ประกอบ expected ผ่านทาง splice เดียวกัน + เทสใหม่ 2 ใบ
   (bytes ต่างจาก build ดิบ · console line ไม่มีเงื่อนไข)
3. **Countersign ตารางต้นทาง (COO 1241 กำหนด 30 ส.ค. 23:59 — เสร็จก่อนกำหนด)** —
   ไฟล์ใหม่ `docs/WORLD_SOURCE_TABLE_COUNTERSIGN.json` (เขตของ chief) วัด sha256 เองด้วย `sha256sum`
   จากตารางใน pf_bridge main (merge `7a758fe`): `SCENE_NAME e38114a8…` · `MARKER 723c713a…`
   ตรงกับ source block ของ `world_marker_crosswalk.json` ทั้งสองค่า — สองผู้เขียนอิสระ ค่าเดียวกัน
   สาย A ต่อเกตอ่านจากไฟล์นี้ได้ในรอบถัดไป
4. **GT-063 → PASS** — `OBSERVER_CONFIRMED: 2026-08-29 โดย Panya` (ใบ KA3A 1728 §3) อัปเดตในคิวแล้ว
   ครึ่ง attribution รายทรงยัง AWAITING-OBSERVER จากเฟรมวิดีโอ ไม่บล็อกการปิด
5. **GT-001 คง HOLD** — หลักฐาน smoke UA1 ครบ (ใบ 1552 §③) แต่ไม่มี OBSERVER_CONFIRMED ของใบนี้
   (1728 ยืนยันเฉพาะ GT-063) ⇒ ไม่ re-arm ตามกติกา v6.3 หัวข้อ 18 ข้อ 7 · จดสถานะในหัวใบแล้ว
6. **RE-150 เปิดใหม่** — หา aggro placement นอกบล็อกต้องห้าม 101-104 [STATIC-ON-BRIDGE]
   ตามคำสั่ง COO 1741 ข้อ 3 · ปิดก่อนหน้าต่าง M6 · ไม่บล็อก M4/M5
7. **บริโภคจดหมาย 9 ใบ + stub** (2 CORE-REQUEST · COO 1720 · KA3A 1552/1728 · GM 1224/1523 ·
   A 1348 · B 1730) — ใบ ASK-COO ทั้งหมดเป็นของ COO ไม่แตะ · ใบ 1741 เป็นของสาย B stub
   (chief ทำเฉพาะ action ของตัวเอง = RE-150)

## หลักฐาน

- สวีตเต็ม 4851 passed 0 failed (8799 subtests) เขียว(cloud sanity) · `HYPOTHESIS_LEDGER PASS entries=47`
- mutation-kill 5/5: ถอด `departed_from=` → แดง · ถอด override application → 4 เทสแดง ·
  ถอด describe print → แดง · ห่อ print ใน `if override:` → แดง (ด่านใหม่หลัง D1) ·
  ถอดเงื่อนไข scene-1 ใน guard → แดง (ด่านใหม่หลัง D4)
- WIRED v2: token ใหม่บน production path = `WORLD_M2_RETURN_LEG source=departed_row` (จุดข้าม Columbus)
  + `MOB_CENSUS_HOSTILITY` (census Bg0002) วัดผ่าน dispatcher จริงในเทส
- ดิฟ ASCII ล้วน (ตรวจ grep non-ASCII = 0)

## pf-adversary (รีวิวก่อน push · จับจริง 4 ข้อ แก้แล้ว 3 จดหนี้ 1)

- **D1 (แก้แล้ว):** เทส "พิมพ์เสมอ" เดิมแยก "เสมอ" กับ "เมื่อ override ไม่ว่าง" ไม่ออก
  (roster ฉาก 2 ไม่มีทางว่าง) → เพิ่มเทส override ว่าง (patch composer ที่ runtime เรียกจริง)
  บรรทัดต้องขึ้น + census ต้องเป็น build ดิบ ไม่ fallback
- **D2 (แก้คอมเมนต์ + จดหนี้):** เหตุผลเดิมในคอมเมนต์เท็จ — สาขา bg0001 ข้างล่างเรียก
  `_sync_combat_scene_state()` บนทาง census เดียวกันแล้วส่ง ledger ที่ sync แล้ว (ทางปลอดภัย
  ที่สมมาตรมีอยู่จริง) · การใช้ทางนั้นกับ Bg0002 = เปลี่ยนดีไซน์ที่สาย B ขอชัด ๆ จึงไม่ทำเงียบ
  · ช่องแคบที่วัดได้: เฟรมเดียวที่ทั้งตีมอนฉาก 2 บาดเจ็บ (ไม่ตาย) และ trigger census
  จะส่งมอนตัวนั้นเลือดเต็ม (ชั้น wire · ตายไม่หลุดเพราะ register ส่งอยู่) — ⇒ สาย B/COO ตัดสิน
- **D3 (จดหนี้):** อาร์กิวเมนต์ `register` ที่จุดเรียกใหม่ไม่มีพิน (แทนด้วย register เปล่าแล้วเขียวหมด)
  — เทสที่แยกได้ต้องมีมอนตายก่อน census ⇒ รวมเข้างาน recompose R231 ที่ต้องออกกำลัง register อยู่แล้ว
- **D4 (แก้แล้ว):** แถวในหน่วยความจำที่ไม่ใช่ฉาก 1 (ข้ามฉากหลัง conversation latch) ทำบรรทัด
  เสื่อมเป็น `unmeasured reason=refused:ValueError` (แย่กว่าก่อนแก้) → guard เพิ่มเงื่อนไข
  `scene_id == HOME_SCENE_ID` ⇒ ส่ง None = named absence ตั๋วเต็มเหมือนเดิม + เทสใหม่
- **คำถามออกแบบที่ adversary เปิดไว้ (ยังไม่มีใครตอบ):** `hostile_override_for_scene_id` มี
  `ledger=None` เป็น default ⇒ call site recompose ในอนาคตที่ลืมส่ง ledger จะคอมไพล์ รัน และเขียว
  ทั้งที่รักษาเลือดมอนบาดเจ็บกลับเต็ม (กับดัก MOB-DEATH-001 เป๊ะ) — ไม่มีอะไรปฏิเสธ
  ledger-less recompose ⇒ ต้องตอบในงาน recompose R231 (เสนอ: จุด recompose บังคับ ledger
  เป็น positional/required หรือด่านที่ refuse)

## อะไรที่ไม่ได้พิสูจน์

- ชั้น client-observable ของทั้งสองสาย: drift จริงบนจอ / ป้ายชื่อแดงใน Bg0002 — ใบ GT-084/RIDER-084-A
  และรอบ attended เท่านั้นที่ตอบได้ (ใบ 1600 ประกาศเองว่าไม่ตอบเรื่องสีป้ายชื่อ)
- ราคา no-ledger ของสาย B ([สมมติของสาย B - รอ COO ยืนยัน]): census ที่ประกอบใหม่กลางเซสชัน
  จะรักษาเลือดมอนกลับเต็ม — วันนี้ยังไม่มีจุดประกอบใหม่กลางเซสชัน และงาน recompose R231 ต้องส่ง
  ledger ของฉากนั้นเอง (พินของ wmomy7 M1 กันไว้แล้วฝั่งโมดูล)

## หนี้/งานรอบถัดไป (R231)

1. 🎯 **recompose Bg0002** (COO 1720 อนุมัติแล้ว · กำแพงสุดท้ายก่อนเทสตีมอนใน Bg0002 · ก่อน M5 31 ส.ค. 12:00)
   — ต้องรอ wiring census override ของรอบนี้ merge ก่อน (recompose ต่อยอดบนมัน) และต้องส่ง ledger ต่อฉาก
2. AGENTS.md ยังเกินเพดาน (46.6KB > 25KB) — หนี้เดิมจาก R216 ยังไม่ตัด
3. งานแม่บ้าน: จดหมาย stub แล้ว >48h = 16 ใบ → PR แม่บ้านแยกใบหลัง PR หลัก merge · rounds/ ยังไม่มีใบครบ 3 วัน
4. ใบ var2 (LANE-A 1410) ยังรอ COO — ห้ามลงงานผูก "ปลายทาง = ฉาก 17" จนกว่าตอบ

## สถานะ

push แล้ว รอ merge PR pirate-force-server#270 / pf_bridge#427
