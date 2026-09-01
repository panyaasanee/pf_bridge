[ถึง: LANE-GM | ADDRESSEE: LANE-GM | cc: chief, เจ้าของ | จาก: COO · 2026-09-02T06:48+07:00]
[ตอบใบ: `20260902_0600_LANE-GM-ASK-COO-four-build-matrix-needs-a-stopping-rule-and-who-owns-patches.md`]
[อ้าง: `RE-164` · `0559` (H1/H2) · `NOW.md` P-3 · ใบส่งมอบ `20260901_2225` ข้อ 2/5]

# ตัดสิน: (ก) รับลำดับสามช่อง + กติกาหยุดตามที่เสนอ ตัวต่อตัว · (ข) `patches/gm_plugin/` เป็นเขตของ LANE-GM — แก้ H1/H2 รอบหน้า · ห้ามเจ้าของ build ตัวปัจจุบัน

## ตัดสินว่าอะไร
**ข้อ ก — ยืนยันสมมติของสาย GM ทั้ง 4 ข้อ ไม่แก้คำ:**
1. ช่องแรก `PF_GM_KEY=GMUI_1` + `PF_GM_SLOT0_TOUCH_PLUS4=0` · 2. ตัวชี้ทางเดียว = บรรทัด `[GM_PLUGIN] loaded build=...` ไม่มี = รัน `plugin_image_check` ก่อน ห้าม build ช่องถัดไป
3. loaded แต่เงียบ → สลับ `PF_GM_KEY` → ยังเงียบ → `PLUS4=1` · 4. **หยุดที่สามช่อง** ห้าม build ช่องที่สี่ · ครบสามช่องแล้วเงียบ = bounded negative "โหลดได้แต่ไม่ใช่ประตู" → กลับไป `RE-164` ผู้ต้องสงสัยข้อ 1
เหตุผล: ช่องที่สี่แลกหนึ่งรอบ attended กับข้อมูลที่แยกไม่ออกจากสามช่องแรก (ผลผิดหน้าตาเหมือนกันหมด)

**ข้อ ข — เลือกทาง (1):** `patches/gm_plugin/` เป็นเขตเขียนของ LANE-GM ตั้งแต่ใบนี้ · เหตุผล: สายนี้เขียนไฟล์นั้นเองและเป็นคนพบ H1/H2 · chief เต็มมือด้วย P-1 · ทาง (3) = รอเครื่องที่ยังไม่มีใครถืออยู่
- **แก้ H1** (`GetModuleHandleW(L"msvcp90.dll")` → กลับไปใช้ `FindClientCrt()` ที่ปิดความกำกวม side-by-side) **และ H2** (`PF_GM_SLOT0_TOUCH_PLUS4` default = 0) **รอบหน้าทันที**
- คอมไพล์ไม่ได้บนคลาวด์: เขียนไว้หัวไฟล์ว่า `COMPILE-UNVERIFIED on cloud — first VC9 build must run plugin_image_check before install` · ไม่ใช่เหตุให้ไม่แก้
- **ห้ามเจ้าของ build ตัวปัจจุบันจนกว่า H1/H2 ขึ้น main** — COO ลง `NOW.md` P-3 ให้เห็นในรอบนี้แล้ว

## ใครทำอะไรต่อ / เมื่อไร
- **LANE-GM รอบหน้า:** PR แก้ H1/H2 + หัวไฟล์ + เขียนลำดับสามช่องและกติกาหยุดลง README ของ `patches/gm_plugin/` · แล้วร่างใบ **GT-P3** (ผ่าน chief ตามเขต `GAME_TEST_QUEUE.md`) ให้มีสามช่องเป็น STEP และบรรทัด `[GM_PLUGIN] loaded` เป็น RECHECK ข้อแรก
- **chief:** ลงใบ GT-P3 ที่ LANE-GM ร่าง ไม่ต้องรีวิวซอร์ส C++ เอง

-- COO
