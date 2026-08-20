# ARCHIVE — GAME_TEST_QUEUE: GT-011 (ย้ายออกเมื่อรอบ 81, 2026-08-19)

> ย้ายมาจาก `pf_bridge\GAME_TEST_QUEUE.md` · **ไม่มีอะไรถูกลบ**
> GT-011 ปิดแล้วในทางโครงสร้าง: UI-REFRESH-001 (รอบ 80) พิสูจน์ว่าเกณฑ์เดิมของมัน
> ผ่านไม่ได้โดยโครงสร้าง (ไม่มี erase-by-key path ในไบนารี) · ผู้สืบทอดคือ **GT-018**

---

## GT-011 HYP-PF-015 v2 delete ack: client รับ ack แบบมี trailing mask แล้วลบตัวละคร/ช่องว่างจริงไหม  [🟡 PARTIAL PASS — รอบใหญ่ #3 17:0x]

> 🔴🔴 **[รอบ 80 — UI-REFRESH-001 ตอบว่าทำไม list ไม่รีเฟรช · อย่าลองรูปแบบ ack ใหม่อีก]**
> รายงาน: `reports/PF_UI_REFRESH001_CHARACTER_SELECT_STATE_MACHINE_STATIC_20260819.md` (verifier 292 guards exit 0)
> - **list ตัวละครมี buffer เดียว** = collection ที่ `+0x180` ของ singleton `[0x1081A90]` · สแกน `.text` ทั้งหมดเจอ 32 จุดที่ประกอบ `+0x180` พินครบ
> - **mutator มีแค่ 4 ตัว:** fill `0x5DDD00` (caller เดียวทั้งไบนารี = `0x5EFCAC` ใน apply ของ **SelectActorVital 0x36EF**) · append-one `0x5DDE10` (caller เดียว = `0x5EFD76` ใน CreateActorVital 0x36CF) · clear `0x5DDF00`/`0x5DE540`
> - 🔴 **ไม่มี erase-by-key path อยู่ในไบนารีเลย** ⇒ **ack ของคำสั่งลบ ไม่ว่าจะแต่งรูปแบบไหน เอาตัวละครออกจาก list ไม่ได้ตลอดกาล** — GT-011 step 4 จึงเป็นเกณฑ์ที่ผ่านไม่ได้โดยโครงสร้าง ไม่ใช่เพราะเราแต่ง frame ผิด
> - handler จริงของ ack: `0x5EFDC0` (vtable `0xF301A0` slot +0x1C) → `cStateCreateActor::OnDeleteResult 0x4BAEB0` · ต้องมีหน้าต่าง `Login_CharSelect_Panel_Operations` · field `+0x14 ∈ {3,4}` → เขียน countdown `record+0xF4` · **ค่าอื่นทุกค่า รวม `1` ที่เราส่ง = repaint เฉย ๆ** จาก collection เดิม
> - negative ตรวจครบช่วง `[0x4BAEB0, 0x4BB618)`: ไม่เรียก list mutator ตัวใดเลย · ไม่เรียก `CState::RequestNext 0x4C7320` · ไม่แตะ page variable `0x107A2C0`
> - ⇒ **เส้นทางเดียวที่ rebuild list ได้ = `SelectActorVital 0x36EF`** (reset `0x406C30`→`0x5DDF00` · refill `0x5DDD00` · สร้าง `cStateCreateActor` ใหม่ + RequestNext ที่ `0x5EFD1E`) → นี่คือเนื้อของ **DELETE-REFRESH-001** ที่ chief จะ implement (ดู GT-018)
> - อาการ "ปุ่มอื่นไม่ตอบสนอง": หน้าจอขับด้วย page variable `0x107A2C0` (per-frame `0x4C3C40` · jump table 15 ช่อง `0x4C3E30` · input gate `0x4BEEA9` ต้อง `== 0`) · animation ก่อนลบตั้ง `0x0B` ที่ `0x4BAE91` แล้ว OnDeleteResult **ไม่เคยเขียนคืน** — **กลไกพิสูจน์แล้ว แต่ค่า live ตอน GT-011 ยังเป็น ③เดา**
> - 🟢 **ผลต่อคิว:** GT-011 **ปิดในรูปแบบเดิม** (เกณฑ์ client-observable ผ่านไม่ได้โดยโครงสร้าง) → งานย้ายไป **GT-018**


> 🟡 **RESULT รอบใหญ่ #3 (17:0x, HEAD `f286945`, jobs 101/102) — PARTIAL PASS · ผลเต็ม: `pf_bridge\notes_to_chief\consumed\20260818_1745_biground3-results.md`**
> - ✅ **root cause fix ทำงานจริง:** ไม่มี GSCN error dialog อีกแล้ว (GT-010 เคยเด้ง `ErrorData=28317` ทุกครั้ง) → shape v2 แก้ที่ชั้น parse ได้
> - ✅ wire/DB: frame **79B ตรงสเปกเป๊ะ** (77B+2 trailing mask) · marker `HYP_PF_015_..._SOFT_DELETE_COMMITTED` · สำเนา DB `characters(1,'Arena01',selector=0,deleted_at=...)` = soft delete commit สำเร็จ · canonical ไม่ถูกแตะ
> - ❌ **client ไม่รีเฟรช list** — Arena01 ยังอยู่ nameboard ยังโชว์ ไม่มีช่องว่าง → ไม่ได้ทำ step 5
> - ❌ หลังยืนยัน ปุ่มอื่นบนหน้า char select ไม่ตอบสนอง (เข้ากับสมมติฐาน "socket ปิดหลัง ack" แต่ **ยังไม่วัด ยังไม่ยืนยัน**)
> - ⇒ **state divergence ยังอยู่** (server ลบแล้ว / client ไม่รู้) · lead ของผู้เทส (ไม่ใช่ข้อสรุป): client อาจรอ **list-refresh response** ไม่ใช่แค่ ack ของคำสั่งลบ
> - 🔎 **อาการร่วมกับ GT-013** ดูบล็อก HYP ใหม่ท้ายไฟล์

- objective: (claim เดียว — ชั้น client-observable เท่านั้น) ทำ GT-010 ซ้ำที่ HEAD ที่มี
  DELETE-SOFT-002 (v2 ack = echo เดิม + trailing derived-class mask `0B 00` ผ่าน
  make_runtime_vitals — แก้จาก root cause ของ ErrorData=28317 ที่ GT-010 เจอ):
  **หลังยืนยันลบ (dialog ใช่/ไม่ → password pad) ตัวละครหายจาก list โดยไม่มี error dialog
  ไหม? แล้วสร้างใหม่ลงช่องเดิมได้ไหม?** · ชั้น wire/DB พิสูจน์แล้ว headless
  (`reports/PF_DELETE_SOFT003_RUNTIMERES_TAIL_FIX_HEADLESS_20260818.md`) —
  **อย่าเทสซ้ำชั้น wire อย่านับเป็นเกณฑ์**
- db: สำเนา canonical สด (101 copy + เช็ค sha กับค่าใน LOCK ก่อนรัน — ณ ตอน stage =
  `B5557E9F..C9ED`) · canonical ต้องไม่ขยับ
- server args: (101 จัดให้ครบ) `--delete-actor-hypothesis-scenario
  scenarios\delete_actor_hypothesis_soft_delete.json` (console ต้องเขียน mode
  `delete-actor-hypothesis`)
- ⚠️ mutually exclusive: logout ack ไม่ทำงานรอบนี้ → ออกเกมด้วย **End task เท่านั้น**
- ⚠️ ลบที่หน้า char select ก่อนเข้าแมพ — ไม่ต้องเข้า world
- steps:
  1. ย้ายหน้าต่างเกมฝั่งซ้าย**ก่อนเริ่ม** → run staged `done\101_gt011_boot.ps1`
  2. login → หน้า char select (ตัวละครเดิม 1 ตัว) — **หยุด ไม่กด Start**
  3. ปุ่มลบ = **ปุ่มแรกซ้ายสุด** (ยืนยันจาก GT-010 — PLAYBOOK แก้แล้ว) → dialog ใช่/ไม่ →
     ยืนยัน → password pad คีย์บอร์ดสุ่ม → พิมพ์ `test` ด้วยคีย์บอร์ดจริง → ยืนยัน
  4. สังเกต ~10 วิ: **ไม่มี error dialog + ตัวละครหายจาก list / ช่องว่าง?** — บันทึกละเอียด
     ทุกจังหวะ UI (ภาพหน้าจอถ้าทำได้) · ถ้า error dialog โผล่อีก: จดข้อความเป๊ะ ๆ
     (โดยเฉพาะเลข ErrorData ใหม่ — ตัวเลขนี้คือข้อมูลออกแบบ) + เก็บ capture ครบ = รางวัลรอง
  5. ถ้า list ว่าง: กด**สร้างตัวละครใหม่** (ปุ่มที่ 2) ลงช่องเดิม ตั้งชื่อใดก็ได้ →
     สังเกตว่าสร้างผ่าน + โผล่ใน list ไหม (reuse ชั้น UI ครั้งแรกของโปรเจกต์)
  6. ออกด้วย **End task** → run staged `done\102_gt011_teardown.ps1`
- pass criteria (แยกชั้น):
  - **client-observable (เทสนี้):** ไม่มี GSCN error dialog + ตัวละครหายจาก list หลังยืนยัน +
    (ถ้าทำ step 5) สร้างใหม่ลงช่องเดิมสำเร็จและโผล่ใน list
  - **wire-DB (ยืนยันซ้ำเฉย ๆ ผ่าน 102):** marker `HYP_PF_015_DELETE_ACTOR_..._COMMITTED`
    ใน GAME_LIVE (ack live ตอนนี้ = **79B** ไม่ใช่ 77B — +2 จาก trailing mask) ·
    DB copy: แถวเดิม deleted_at ไม่ null · แถวใหม่ (ถ้าสร้าง) selector/identity เดิม ·
    canonical sha ไม่เปลี่ยน
- nonclaims: ไม่ claim ความหมาย op2/wstring token/28317-เลขใหม่ใด ๆ · ไม่ claim ว่า server เดิม
  ตอบแบบนี้ (ไม่มี golden) · ไม่ claim restore/undelete · ไม่ claim password pad ถูกตรวจฝั่งไหน ·
  ผล FAIL อีกครั้ง = falsify candidate 1 → chief เดินต่อ candidate 2 (LoginProtocol envelope —
  ดู `reports/PF_DELETE_SOFT002_NATURAL_0x36DB_DECODE_20260818.md` §d)
- result: (ผู้เทสกรอก)

> 👁️ **observation แถมรอบใหญ่ (จาก TELEPORT_AUDIT001 รอบ 45 — ไม่เพิ่ม step ใด แค่จดตอน teardown):**
> 1. ถ้ารอบไหนมี MARKER transport (เช่น full-loop GT-001): หลังจบ ให้ grep GAME_LIVE.txt หา
>    `TeleportVital` — คาดว่ามี**บรรทัดเดียว** (echo ตอน entry) ถ้าเจอบรรทัดที่สอง = ข้อมูลใหม่
>    (client echo หลัง transport กลางเซสชัน) จดไฟล์+บรรทัดลง result
> 2. ถ้าเห็น UI ของขวัญ/gift ค้างหรือ popup แปลก: จดไว้ — client ส่ง AskForSystemGiftVital
>    `0x8B93` ทุกเซสชันแล้วได้แค่ generic ack (อ้างอิง reports/PF_TELEPORT_AUDIT001_..._20260818.md)

---

> 📦 **[ย้ายไป archive 2026-08-17 23:1x (chief รอบ 44)]** GT-007 HYP-PF-012 clean logout [FAIL — processed `b03d207` · follow-up = GT-008 ด้านบน] → `pf_bridge/archive/GAME_TEST_QUEUE_ARCHIVE_20260817.md`

> 📦 **[ย้ายไป archive รอบ 78]** GT-012 CHAT-ECHO-002 speaker-wstring — **✅ PASS ทุกเกณฑ์ (รอบใหญ่ #3)**: เรนเดอร์ `[ทั่วไป] Arena01: PFCHATPROBE1` · ไม่ one-shot · SHORT เงียบ fail-closed → `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260818_R78_BIGROUND3.md`

> 📦 **[ย้ายไป archive รอบ 78]** GT-013 HYP-PF-016 worldinfo-first — **❌ FAIL (รอบใหญ่ #3)**: wire ถูกครบ (283B→46B) แต่ client ไม่ transition ทั้ง 03 และ 01 (01 confounded) ⇒ **shape ที่ 3 ถูก falsify · ครบสามแล้ว** · อาการร่วมกับ GT-011 ดูโน้ตหัวไฟล์ข้อ 3 → `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260818_R78_BIGROUND3.md`

> 📦 **[ย้ายไป archive รอบ 78]** GT-014 MOVE-AUTHORITY-001 observation — **🟢 เก็บครบ (รอบใหญ่ #3)**: ชนกำแพงหยุด ไม่ snap-back · `MovementAttr` server→client = 0 · `TeleportVital` 1 บรรทัด ⇒ ตอกย้ำ client-authoritative → `pf_bridge\archive\GAME_TEST_QUEUE_ARCHIVE_20260818_R78_BIGROUND3.md`

