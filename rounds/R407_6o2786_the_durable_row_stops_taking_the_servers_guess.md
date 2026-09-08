# R407 (`6o2786`) — แถวถาวรเลิกรับ "ความเชื่อของเซิร์ฟเวอร์" มาปนกับพิกัดของผู้เล่น

รอบ: `6o2786` · LANE-E (chief) · 2026-09-08T21:22 -> 22:2x +07:00
claim PR: `pf_bridge#1960` · PR เซิร์ฟเวอร์: **`pirate-force-server#1183` เปิดแล้ว เป็น draft รอ gate**
🔴 draft ตามข้อยกเว้นใน COMMON (PR ที่แตะเส้นล็อกอิน/แถวที่ตัวละครโผล่) + `ADVERSARY_PENDING` — ห้ามอ่านว่า landed
takeover: ไม่มี · ไม่มี `[LANE-E]` claim เปิดค้างตอน list

## รอบนี้ขยับ NOW/M ข้อไหน
บรรทัด chief ใน NOW: **"`1808` ข้อ 1+2 แซงทุกอย่าง = บล็อกประตู M (`1943`)"** — จ่ายครบทั้งสองข้อในรอบนี้
ประตู M ทาง (ก) ค้างเพราะ `#1160` ของ LANE-A ปลด draft ไม่ได้ ซึ่ง COO ระบุว่าเหตุอยู่ที่ D1/D3 ใน `runtime.py` = เขตผม
รอบนี้ปิดต้นทางของแถวสองเจ้าของ + วางเทสของ writer ตัวจริง ⇒ ส่งลูกกลับให้ LANE-A แล้ว

## ทำอะไร (หนึ่งเรื่อง หนึ่ง PR)
`runtime.py` เส้นทาง `TargetPosVital` เลิกเรียก `foundation.checkpoint(candidate)` แบบไร้เงื่อนไข
เปลี่ยนเป็น `_checkpoint_unless_the_label_is_a_guess(candidate)`:
- ป้ายฉากไม่ใช่การเดา ⇒ เขียนถาวรเหมือนเดิมทุกประการ
- ป้ายเป็นการเดา **และ** `warp_scene_persist.login_would_accept(scene)` = False ⇒ **ไม่เขียนแถวถาวร**
  แต่ยัง `checkpoint` ด้วย `durable=False` ⇒ SELECT ตรวจสิทธิ์ lease ยังรัน · คอลัมน์ไม่ถูกแตะ ·
  แถวหน่วยความจำยังขยับ · พิมพ์ stderr `DURABLE_ROW_WITHHELD_UNCONFIRMED_SCENE <scene>`
- `session.checkpoint` / `lifecycle.checkpoint` รับ `durable=` เป็น keyword-only · lifecycle ใช้
  `allowed = durable and is_position_persist_allowed(...)` ⇒ ผู้เรียก **ลบการเขียนได้อย่างเดียว เพิ่มไม่ได้**

🔴 **สิ่งที่วัดแล้วและเปลี่ยนดีไซน์กลางรอบ**: ร่างแรกยับยั้งบน `scene_label_is_server_guess` เพียงอย่างเดียว
ชุดเต็มแดง 6 ใบ และทั้ง 6 ใบถูก ไม่ใช่เทสผิด:
- `gm/warp_send_watch._restore_selected_scene` คืนป้ายฉากต้นทางหลัง rollback **แต่ไม่มีใครล้างธง**
  ⇒ วาปที่เฟรมไม่เคยออก จะทำให้เซสชันนั้น **เลิกเก็บตำแหน่งตลอดชีวิต**
- `PANYA 1218` ข้อ 2 ต้องการตรงกันข้ามสำหรับ M2: เดินทาง + หนึ่งก้าว ต้องได้แถวที่พากลับ **ทะเล** ไม่ใช่ Port Royal
⇒ รั้วจริงคือ **"แถวที่ทำให้ล็อกอินไม่ได้"** ไม่ใช่ "ป้ายที่ยังไม่ยืนยัน" · ใช้รั้วเดิมของโปรเจกต์
(`login_would_accept` ตัวเดียวกับที่ R401 ใช้กับการ relabel) มาคุมการ **เขียน** ⇒ ทั้งสองจะไม่มีวันเถียงกัน
วัดวันนี้: ล็อกอินปฏิเสธ 17/126/304/305/343/345 · รับ 1/2/14/278/997 · และ **305 คือฉากที่ LANE-A วัดดีเฟกต์**

## ชุดเต็มจับของจริงหนึ่งข้อ (บันทึกไว้เพราะมันคือคุณค่าของเกต ไม่ใช่ค่าใช้จ่าย)
รันชุดเต็มรอบสอง แดง 1 ใบ: `test_multiplayer_readiness_audit` interlock **X06** — "ทุก checkpoint call ใน
`runtime.py` ต้องอยู่ที่ try-depth 0" · ร่างของผมห่อการเรียกแบบไม่ถาวรไว้ใน `try/except TypeError`
(รองรับ session double ที่ไม่มีคีย์เวิร์ด) ⇒ ผิดข้อนี้เต็ม ๆ เพราะ listener ของ v141 ไม่มี `except`
ครอบ `state.dispatch` แปลว่า checkpoint ที่ raise ถูกกลืนได้ = lease ถูกขโมยโดยไม่มีใครได้ยิน
แก้ด้วยการ **อ่าน signature** แทนการดัก TypeError โดยผูกชื่อโลคัลไว้ก่อน `try`
(ตัวตรวจจับข้อความ `self.foundation.checkpoint` ทุกที่ แยกการอ่าน signature กับการเรียกที่ถูกห่อไม่ออก
— ตัวตรวจที่แยกไม่ออกควรเชื่อฟัง ไม่ใช่เถียง) · re-pin `checkpoint_calls_at_try_depth_zero` 5 -> 6
พร้อมเหตุผลในรูปแบบบ้านของรายงานเอง

## หลักฐาน
- **wire/DB**: `tests/test_durable_row_two_owners.py` (ใหม่ 10 เคส) ยิงเฟรม `TargetPosVital` จริงผ่าน
  `dispatch()` แล้วอ่านแถวกลับจาก SQLite — **ไม่มีที่ไหนในไฟล์ประกอบ `Position` เองป้อน `lifecycle.checkpoint`**
  (นี่คือ `1808` ข้อ 2 คำต่อคำ) · **มิวแทนต์ 13 ตัว ตาย 13**
  สามตัวที่รอดในรอบแรกแล้วถูกฆ่าเพิ่ม: session double ที่ไม่มีคีย์เวิร์ด · `except TypeError` ที่ถูกขยายเป็น
  `except Exception` (จะกลืน stolen lease) · รั้วที่ fail-open เมื่ออ่าน registry ไม่ได้
- **client-observable**: **ไม่มีในรอบนี้** (G5 — ห้ามเอาชั้น wire มาอ้างแทน) · ออกเป็นใบ attended ให้ LANE-K
  ตั้งเลข: `notes_to_chief/20260908_2144_FROM_CHIEF-TO-K-gt-body-warp-the-client-never-follows.md`
  สถานะที่ขอ = **HELD-ON-BUILD** เพราะกลไกยังไม่อยู่บน main ⇒ `HEADLESS_PROOF:` วัดบน main ไม่ได้วันนี้
  เขียนตรง ๆ ว่า PENDING-MERGE พร้อม `git grep` สองบรรทัดให้คนที่สามปลด HELD เอง
- ledger: `verify_hypothesis_ledger.py` PASS (50) · `verify_functional_coverage.py` รันแล้ว · `pf_gate_preflight.py` PASS

## nonclaims
1. ประตูนี้ทำให้ **แถวผิดเกิดยากขึ้น** มัน **ไม่ได้ลบแถวผิดที่มีอยู่แล้ว** — คำถามปิดท้ายของ adversary ฝั่ง LANE-A
   ("อะไรเขียนทับแถวที่ผิด") ยังเปิดอยู่และเป็นของ COO
2. **ยังไม่ปิด (พูดตรง ๆ)**: วาปไปฉากที่ **ล็อกอินรับ** (278 คือตัวอย่างจริง `sent_before=NO`,
   `return_ticket=REQUIRED`) ที่ไคลเอนต์ไม่ตามไป **ยังเขียนแถวนั้นด้วยพิกัดต้นทาง** ⇒ ล็อกอินได้ เดินกลับบ้านไม่ได้
   มีเทสตรึงพฤติกรรมปัจจุบันไว้ (`test_the_gate_is_the_brick_not_the_guess`) เพื่อให้วันที่ปิดมีบรรทัดเดียวบอกว่าเปลี่ยนอะไร
3. **เส้นทาง logout ยังไม่ถูกแตะ**: `lifecycle.exit` (`lifecycle.py:422`) ยังเขียนแถวตอนปิดเซสชัน
   `/warp 305` แล้ว logout ทันทีโดยไม่เดิน ยังผ่านทางนั้นได้ — งานแรกของรอบหน้า
4. D9 ของ LANE-A (คอมเมนต์ `runtime.py` ~7160 ว่าฉาก 17 pin ปิด): **วัดบน origin/main แล้วยังจริง**
   (17 persist=False · registry `n_id:17` login/persist = False ทั้งคู่) จึง **ไม่ลบคอมเมนต์**
   แต่ตรึงข้ออ้างด้วยเทส ⇒ วันที่ LANE-A พลิก 17 เทสแดงทันที · แจ้งกลับเป็นจดหมายแล้ว

## QUEUE_TRIAGE:
- เพิ่มใบใหม่: ส่งเนื้อใบ attended ให้ LANE-K ตั้งเลข (HELD-ON-BUILD) — เจ้าของใบ/ผู้บริโภคผล = chief
- `GT-313` ตรวจแล้ว **ไม่กระทบ**: ใบนั้นเดินทาง login-scene override (`config/gm_login_scene.json` single-use)
  ซึ่งไปสาขา `login_scene_override_visit` ที่ยับยั้งแถวถาวรอยู่แล้ว — ประตูใหม่แตะเฉพาะสาขา `elif` เท่านั้น
- ไม่ถอน ไม่ย้าย ไม่ปิดใบใดในรอบนี้
- 🔴 **ตัวเลขที่ COO/K ควรเห็น**: `GAME_TEST_QUEUE.md` วันนี้ **970,446 ไบต์** เทียบเพดาน 300 KB ใน CHIEF §11
  (preflight ผ่านเพราะมันตรวจ *การโต* บนกิ่ง ไม่ใช่ขนาดสัมบูรณ์) — งาน archive ของ LANE-K ไม่ใช่ของผม แต่บันทึกไว้ให้เห็น

## READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ:
ไม่มีใบใหม่ที่พร้อมขึ้นรถบัสจากรอบนี้ (ใบของรอบนี้เป็น HELD-ON-BUILD จนกว่า PR จะลง main)

## รอบหน้าทำอะไร (เรียงแล้ว)
1. **เส้นทาง logout** — `lifecycle.exit` / `session.close(position)` ยังเขียนแถวจากป้ายที่ยังไม่ยืนยัน (nonclaim 3)
2. **D7 ของใบ `1808`** — `runtime.py` `10615/10694` กันเฉพาะเมื่อ `login_scene_override is not None`
   (COO `1943` บอกว่าเข้าคิวปกติ ไม่ใช่รอบนั้น)
3. ผล `pf-adversary` ของรอบนี้ ถ้าคืนหลังปลดล็อก = งานแรกของรอบถัดไปตาม COMMON
4. `0206` + ริด `CHIEF_CONTINUATION.md` §0 → `1553` → `GM-058` ตามบรรทัด chief ใน NOW

ADVERSARY_PENDING pirate-force-server (กิ่ง `claude/great-franklin-6o2786`) — สั่งต้นรอบ 21:45 ยังไม่คืนตอนปลดล็อก
🔴 **ห้ามอ่านไฟล์รอบนี้ว่า "ผ่าน adversary"** — ยังไม่มีผลคืน

SCOREBOARD: COMING | วาป GM ไปฉากที่ล็อกอินไม่รับ แล้วเดินหนึ่งก้าว เลิกเขียนแถวที่ตรึงตัวละครไว้ในฉากที่ไม่เคยไป ผู้เล่นล็อกอินกลับมาที่เดิมแทนที่จะเข้าเกมไม่ได้ | pirate-force-server PR ของรอบ 6o2786 (0f18272) + tests/test_durable_row_two_owners.py 10 เคส มิวแทนต์ 13/13
