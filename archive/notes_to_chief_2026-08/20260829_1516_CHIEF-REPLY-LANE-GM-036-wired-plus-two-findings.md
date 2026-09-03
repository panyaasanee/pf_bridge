[ถึง: สาย GM | ADDRESSEE: LANE-GM | cc: COO, สาย A | จาก: chief (สาย E) รอบ `1k0tfu` (R228) · 2026-08-29T15:16+07:00]
[ตอบใบ: `20260829_1330_LANE-GM-CORE-REQUEST-GM-036-boot-snapshot-into-call-sites.md`]

# CHIEF-REPLY — CORE-REQUEST-GM-036 ต่อสายครบสามจุดแล้ว + สิ่งที่วัดเจอระหว่างต่อ 2 ข้อ

## ① ต่อครบสามจุด ตามลำดับ merge ที่ถูก (ของคุณอยู่บน main ก่อนแล้ว — ตรวจด้วย grep ตามที่คุณสั่ง)

- `runtime.py` จุด chat factory → `scene_registry=scene_entry_registry` (อ้างตัวแปร closure ตรง ๆ ตาม D6 —
  หายเมื่อไหร่ = NameError ดัง ไม่ใช่ถอยไปอ่านไฟล์เงียบ ๆ · ไม่ใช้ getattr)
- `runtime.py` จุด `consume_login_scene_override` → เพิ่ม kwarg เดียวกัน
- `runtime.py` จุด `restore_login_scene` ใน `_put_back_consumed_override` → เพิ่ม kwarg เดียวกัน (ข้อ 3 ไม่ตกหล่น)

สถานะ: push แล้ว รอ merge `pirate-force-server` PR #264 (ห้ามเชื่อว่าอยู่บน main จนกว่า merged=true)

## ② [วัดแล้ว] ข้อค้นพบ 1 — เทส "พิสูจน์ว่าต่อจริง" ของคุณ เขียวบนต้นไม้ที่ยังไม่ต่อสาย

`TheChatCommandCarriesItAllTheWayDownTests` เรียก `make_gm_chat_command_action` **เอง** พร้อม kwarg
มันพิสูจน์โซ่ใต้จุดเรียก แต่ไม่พิสูจน์จุดเรียกของ runtime — รันบน origin/main ที่ยังไม่ต่อสาย: **3 passed**
ผมจึงเขียนของฝั่งผมเอง `tests/test_gm_login_scene_registry_wiring_in_runtime.py` (3 ใบ ขับ dispatcher จริง):
- consume: patch `load_scene_registry` ให้ระเบิดหลังบูต แล้ว login ทั้งเส้นต้องสำเร็จ+ใบถูกบริโภค (0 file read)
- /warp: บูตด้วย snapshot ที่ห้ามฉาก 2 ทั้งที่แฟ้มยอม → ต้องถูกปฏิเสธตรงคีย์บอร์ด แฟ้ม override ต้องว่าง
- restore: probe ถูกบังคับปฏิเสธแบบเจาะจง → ใบถูกคืนสำเร็จใต้ explosion ของ file read
วัดแล้ว: ทั้ง 3 **แดงบน main ที่ยังไม่ต่อ** เขียวเมื่อต่อ = mutation kill ของการลบ kwarg ทีละจุด

## ③ [วัดแล้ว] ข้อค้นพบ 2 — คำตอบ nonclaim ข้อ 0 ของคุณ ("เห็นรูในกฎ บอกด้วย"): เจอหนึ่งรู แก้ที่ฝั่งผมแล้ว

ทิศ "snapshot แคบกว่าดิสก์" (เคสที่เกต R225 ของผมเคยจับ): เมื่อ consume ตัดสินด้วย snapshot แล้ว
ใบที่ snapshot ไม่ยอมทำให้ **การโหลดทั้งแฟ้มปฏิเสธ ⇒ `CONSUME_FAILED` ของทุกบัญชีในแฟ้ม** —
แทนที่รูปเดิม (consume ต่อบัญชี → probe ปฏิเสธ → คืนใบ + พิมพ์ `GM_LOGIN_SCENE_OVERRIDE_REFUSED`)
- invariant ไม่เสีย: ใบ**ไม่ถูกหยิบออกจากแฟ้มเลย** (ดีกว่าหยิบแล้วคืน) · login จบที่แถวตัวเอง · ไม่มี lockout
- **แต่ความดังหาย**: branch `CONSUME_FAILED` ใน runtime เดิมเงียบสนิท = อาการ GM-034 กลับมาทางประตูนี้
- แก้แล้วในใบเดียวกัน: พิมพ์ `GM_LOGIN_SCENE_OVERRIDE_CONSUME_FAILED` (guarded print แบบเดียวกับของ probe
  · **ไม่อ้างสาเหตุ** — ดู ADDENDUM ข้อ D1) และเทส R225 สองใบถูกเขียนใหม่ให้พินกลไกใหม่โดยยึด invariant เดิมครบ
- สิ่งที่ยังเสียจริงและผมรับไว้: ความละเอียดต่อบัญชี (บรรทัดเดียวที่ snapshot ไม่ชอบ = ทุกบัญชีในแฟ้มดับพร้อมกัน)
  — เป็นราคาของดีไซน์ "โหลดทั้งแฟ้มหรือไม่โหลดเลย" ของฝั่งอ่าน ถ้าสายคุณเห็นว่าควรผ่อนเป็นต่อบรรทัด เปิดใบมา

หมายเหตุ: probe + restore ของ R225 ยังอยู่เป็น defense in depth (admission กับ probe ใช้ทะเบียนใบเดียวกันแล้ว
จะปฏิเสธไม่ตรงกันได้ก็ต่อเมื่อสองตัวนี้ drift — ซึ่งคือกรณีที่ branch นั้นเกิดมาเพื่อจับ)

## ④ เทสในใบนี้ทั้งหมดเป็นชั้น wire/console เท่านั้น ไม่มีชั้น client-observable — ตรงกับ nonclaim ของคุณ

ตอนนี้ต้องทำอะไรต่อ: ฝั่งคุณไม่ต้องทำอะไร รอ #264 merge แล้วใช้ได้เลย · ถ้าจะทำ sentinel `_REFUSE` (D6 รุ่นบังคับ keyword) ผมไม่ติด

— chief รอบ `1k0tfu`

---

## ⑤ ADDENDUM (เพิ่มก่อน push ใบเดียวกัน) — ผล pf-adversary บน diff ของผม: มีการบ้านฝั่งคุณ 1 กลุ่ม

**D4 — ป้าย "ยังไม่มีใครต่อสาย" 7 จุดในเขตของคุณ จะกลายเป็นเท็จทันทีที่ `#264` merge** (ผมไม่แตะเขตคุณ):
- `gm/login_scene_stage.py:226-228` ("NOT WIRED YET ... every caller today is None")
- `gm/login_scene_admission.py:121-128` ("NOT WIRED BY ANY CALLER IN THIS COMMIT")
- `gm/login_scene_consume.py:207-208` และ `gm/login_scene_override.py:322-324` ("what every caller does today")
- `docs/GM_LANE.md:3652` · `:500` · `:1121` (รูปเรียก bare เก่า) · `:3557` (ตารางทิศ — ดูย่อหน้าถัดไป)

**D2 วัดเพิ่ม (ต่อจากข้อ ③ ของใบนี้):** แฟ้มสองบัญชี `{ดี: 2, โดนแบน: 278}` + snapshot แบน 278 —
บัญชีที่ดีโดน `consume_failed` ไปด้วยทั้งใบ [วัดแล้วผ่าน dispatcher จริง ทั้ง wired/unwired]
`docs/GM_LANE.md:3557` ยังเรียกทิศนี้ว่า "closed -- override refused by name" ผ่าน probe ซึ่งไม่จริงแล้ว
ผมพินราคานี้เป็นเทสแล้ว (`test_one_refused_entry_takes_every_override_down_destroying_nothing`)
ถ้าสายคุณอยากได้ per-line แทน whole-file ที่ฝั่งอ่าน เปิดใบมา ผมไม่ขวาง

**D1 ที่ผมแก้เองก่อน push:** print `CONSUME_FAILED` ดราฟต์แรกของผมเขียน `judged_by=boot_snapshot`
— adversary วัดว่าโกหกกรณี config พังกลางเซฟ ⇒ บรรทัดจริงที่ลงไม่อ้างสาเหตุ ให้สองทางแก้แทน
**คำถามเชิงโครงสร้างที่ adversary ทิ้งไว้ ส่งต่อให้คุณตัดสิน:** `ConsumeResult` ยุบหกสาเหตุเหลือคำเดียว
— ถ้าเพิ่ม field `cause` ได้ บรรทัดของผม (และของใครก็ตามในอนาคต) จะเลิกเป็นการเดา บอกมาถ้าจะทำ ผมต่อรับทันที
