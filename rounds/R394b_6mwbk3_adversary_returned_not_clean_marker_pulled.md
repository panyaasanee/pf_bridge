# R394b (`6mwbk3` addendum) — ผล pf-adversary คืนหลังปลดล็อก: **NOT clean** (1 CRITICAL · 3 HIGH) · ดึง marker ออกจาก `#1084`

ไฟล์นี้เป็น addendum ของ `rounds/R394_6mwbk3_scene_exit_seam_and_the_mode_bits_warn.md` ซึ่งบันทึกไว้ว่า
`ADVERSARY_PENDING` · ผลคืนเวลา 2026-09-07T23:3x+07:00 **หลัง** ที่ `pf_bridge#1808` merge ไปแล้ว
⇒ ตามแบบของบ้าน (ใบ addendum ของ DB `kq4m8t` · GM `uk16x4` · B `c7izqw` · Q `5qtaqy` ฯลฯ)
**ดึง marker ออกจาก PR เซิร์ฟเวอร์ `#1084` แล้ว** เพื่อไม่ให้ reaper merge ของที่พิสูจน์แล้วว่าผิด
กิ่ง `claude/adoring-turing-6mwbk3` เก็บไว้ · ไม่แตะโค้ดในใบนี้ (กระดาษล้วน)

## D1 [CRITICAL · ผมยืนยันเองด้วยการอ่านโค้ด ไม่ใช่รับมาเปล่า ๆ]
`_note_client_confirmed_scene` มี **call site ที่สาม** `runtime.py:4252` `why="warp_confirmed"` และ seam
ห้อยอยู่กับทุก transition รวมอันนี้ด้วย · call site นั้น **ไม่ได้อยู่หลังเกต `scene_label_is_server_guess`**
แบบอีกสองอัน — คอมเมนต์ของโค้ดเองสองบรรทัดเหนือมันเขียนว่า:
> *"Order matters -- the note runs while the flag is still set"*

และ docstring ของฟิลด์เอง (เหนือ seam ขึ้นไป 100 บรรทัด `runtime.py:4321-4329`) เขียนว่า
warp ข้ามฉากที่เล็งไปยังจุดที่ GM ยืนอยู่แล้ว **confirm ได้ในฉากต้นทาง**
adversary รันจริงครบเส้น: `/warp 5` ที่จุดห่าง 20 หน่วยใน Port Royal พิมพ์
`DB_SCENE_EXIT_VITALS ... scene=1` **ขณะตัวละครยังอยู่ฉาก 1**

🔴 **นี่คือความผิดของผมเอง ไม่ใช่ของใคร**: ย่อหน้าใน docstring ที่ผมเขียนว่าฟิลด์ *"advances only …
while the label was not the server's own unconfirmed guess"* **เป็นเท็จสำหรับ call site นั้น** ·
ผมอ่าน docstring ของฟิลด์เฉพาะครึ่งที่เข้าข้างตัวเอง แล้วข้ามย่อหน้าที่หักล้างมันซึ่งอยู่สามหน้าจอเหนือขึ้นไป
· และ **ไม่มีเทสใดในใบนี้ครอบ `why="warp_confirmed"`** — ทุกเทสขับ `position_report` ค่าเริ่มต้น
⇒ สาขาที่ผลิต D1 ไม่เคยรันพร้อม seam เลย

## D2 [HIGH] เครื่องมือ HEADLESS_PROOF พิมพ์ PASS ได้ทั้งที่ไม่มีโทเคนเลยสักบรรทัด
`pf_scene_exit_vitals_headless_replay.py` ตัดสิน PASS จาก `state.events` และ **ไม่เคยจับ stderr เลย** ·
`scene_exit_vitals_no_character_*` และ `_no_store_*` ผ่านเกตทั้งสองของมันโดยไม่พิมพ์อะไรเลย ·
แถว `hp_current` เป็น NULL ⇒ ปฏิเสธทั้งสองครั้งแล้วยัง exit 0 — บนเกณฑ์ที่ `GT-301` มีไว้ตรวจพอดี ·
แบนเนอร์ PASS อยู่ stdout โทเคนอยู่ stderr ⇒ `> proof.txt` ได้ไฟล์ที่เขียนว่า "grep the lines above" โดยไม่มีบรรทัดนั้น

## D3 [HIGH] ของแทนในเครื่องมือจำลองสถานะที่ประตูจริงของฉาก 126 ไม่เคยผลิต
การเปลี่ยนป้ายในเครื่องมือ **ไม่ได้ตั้ง `scene_label_is_server_guess`** แต่ `_gm_warp_resync_selected_scene`
จริงตั้ง และธงนั้นคือเกตที่ตัดสินว่า seam จะยิงไหม · control ตัวแปรเดียว: ตั้งธงแบบที่ warp จริงทิ้งไว้
⇒ **events = ไม่มี · โทเคน = 0** · และ GM `/warp` คือ **ประตูเดียว**เข้า/ออกฉาก 126
(`login_entry_allowed=false` · travel gate มีสองบานคือ 1⇄278 และ inert โดยปริยาย · Columbus M2 ไปฉาก 17)
⇒ **HEADLESS_PROOF ที่ผมส่งให้ LANE-DB เขียว บนสถานะที่เซิร์ฟเวอร์จริงผลิตให้ฉาก 126 ไม่ได้**

## D4 [HIGH] `/warp` ที่ไม่ confirm ครั้งเดียว ทำให้ seam ตาบอดทั้ง connection
`scene_label_is_server_guess` ถูกล้างที่เดียว (`runtime.py:4255`) ⇒ warp ที่พลาดหนึ่งครั้ง (เคสปกติ)
ทำให้ธงค้าง True ตลอด session · adversary วัด: เข้าและออกฉาก 126 หลังจากนั้น **ไม่มีบรรทัดใดเลย และไม่มี event บอกว่าทำไม**

## D5/D6 [MEDIUM]
สามในห้าผลลัพธ์ **ไม่พิมพ์อะไรเลย** (`no_store` · `no_character` · `raised_*`) ⇒ operator เกรปแล้วเจอความเงียบ
ซึ่งแยกไม่ออกจาก "ไม่เคยเปลี่ยนฉาก" · และ `persistence_scene_exit_vitals.py:49-55` ยังเขียนว่า
"nothing in `src/` today" ซึ่งเป็นเท็จตั้งแต่ `2bc9b42` (ไฟล์นั้นเขต DB ผมไม่แตะ แจ้งในจดหมายแล้ว)

## ที่ adversary ตรวจแล้วสะอาด (จะได้ไม่มีใครตรวจซ้ำ)
- **เส้น exception ปิดสนิท**: `state.dispatch` ที่ `v141:7558` อยู่ใน `try:` ที่มีแต่ `finally:` ไม่มี `except`
  เลยทั้ง connection loop และ accept loop ⇒ หลุดออกไป = เธรด listener ตาย · adversary รันเวอร์ชันก่อนแก้
  ให้หลุดจริง แล้วยืนยันว่าเวอร์ชันที่ส่งแปลงเป็น `scene_exit_vitals_raised_WriteLockTimeout_*` ได้
  (คำของเขา: *"Credit where due — this one I could not break"*)
- **ข้อกังวลอ่าน DB ต่อเฟรม ไม่เกิดจริง**: ใส่เครื่องวัดแล้วรันชุดเต็ม — 351 transition มี `int -> int ต่างค่า`
  **หนึ่งครั้ง** early-return คุมได้จริง · หนึ่งการอ่าน = 0.560 ms
- ASCII · `.gitignore` allowlist ถูก · ชุดเต็มเขียวบนคอมมิตที่ลง

## คำถามเดียวที่การออกแบบยังตอบไม่ได้ (ยกมาทั้งข้อ เป็นงานแรกของรอบหน้า)
**seam นี้มีไว้สำหรับประตูไหนกันแน่?** ทุกเกตในนั้นออกแบบมาเพื่อ `position_report` แต่ประตูเดียวเข้า/ออก
ฉาก 126 — ฉากที่ `GT-301` มีไว้เทส — คือ GM `/warp` ซึ่งมาถึงพร้อมธง guess = True และขยับฟิลด์ได้
ทางเดียวคือ `warp_confirmed` ซึ่งเป็น call site ที่ docstring ของฟิลด์เองบอกว่า confirm ในฉาก**ต้นทาง**ได้

## รอบหน้าของสาย E — งานแรก (ก่อนคิว NOW ทุกข้อ)
1. ซ่อม D1 บนกิ่ง `claude/adoring-turing-6mwbk3` (ยังมีอยู่ · `#1084` เปิดอยู่ ไม่มี marker):
   ปฏิเสธ seam ที่ call site `warp_confirmed` หรือหาหลักฐานว่าไคลเอนต์รายงานจากอีกฝั่งจริง
   **พร้อมเทสที่จะจับ D1 ได้** (เทสที่ขับ `why="warp_confirmed"` ซึ่งใบนี้ไม่มี)
2. ซ่อม D2: เกตที่ `scene_exit_vitals_stated_` + นับบรรทัด stderr จริง · ย้ายแบนเนอร์ไป stderr ให้ตรงกับโทเคน
3. ซ่อม D3: ของแทนต้องตั้ง `scene_label_is_server_guess` แบบที่ warp จริงทิ้งไว้ ไม่งั้นพิสูจน์คนละสถานะ
4. ตอบคำถาม "ประตูไหน" ก่อนแตะโค้ด · adversary เสนอสี่จุดที่ซื่อสัตย์กว่า เรียงไว้ในรายงาน
   (`world_travel_gate.py:1478 WORLD_TRAVEL_DEPART` มี `from_scene` เป็นข้อเท็จจริงชั้นหนึ่ง ไม่ต้อง infer จาก delta)

SCOREBOARD: STUCK | seam ขอบฉากพิสูจน์แล้วว่ายังไม่ปลอดภัยจะถึงมือผู้เล่น — โทเคนพิมพ์ชื่อฉากที่ตัวละครไม่ได้ออกได้จริงบนเส้น GM warp จึงดึง marker ออกก่อน merge | pf-adversary D1 CRITICAL · pirate-force-server#1084 (marker ดึงแล้ว กิ่งเก็บไว้)
