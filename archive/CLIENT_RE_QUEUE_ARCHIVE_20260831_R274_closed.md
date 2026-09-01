# CLIENT RE QUEUE -- ARCHIVE 20260831 R274 (closed ticket moved verbatim from `CLIENT_RE_QUEUE.md`; one-line stub left in place; nothing here is deleted)

## RE-132 GM-GLOBAL-MESSAGE-VITAL-VERSION-001: ไบต์ `vital_version` ของ `Channel_GMGlobalMessageVital` (`0x9F2C`) ที่ client ยอมรับคือค่าอะไร -- ctor ของ vital นี้เขียนอะไรลง `+0x10`  [**CLOSED / ตอบครบ** -- ผล: `notes_to_chief/20260829_0010_RE-132-RESULT-VERSION-ZERO-RENDER-PATH.md` (DONE/PASS static, verifier 61/61) · บริโภคและปิดโดย LANE-GM (ผู้เปิดใบ) รอบ `z6gu2n` 2026-08-29T00:25+07:00]

> **คำตอบ:** ข้อ 1 `0x9F2C` → `vital_version = 0` (เขียนที่ `0x00657CC9` ผ่าน ctor ที่ prototype เรียกที่ `0x0065BCD0`)
> · ข้อ 2 ตัวคุม `0xAC52` → `0` ด้วยวิธีเดียวกัน ⇒ วิธีถูก · ข้อ 3 handler `0x0065C850` **ไม่ใช่ no-op**
> (router `0x00659870` → อ่าน body ที่ `+0x18` → display sink `0x005CBAF0`) = static render-path positive
> **ที่ใช้ต่อแล้วในรอบ `z6gu2n`:** `gm/say_wire.py` พินคำตอบเป็น `GM_GLOBAL_MESSAGE_VITAL_VERSION_RE132_STATIC = 0`
> พร้อม VA/sha และเทสสองข้อใน `tests/test_gm_say_action.py`
> 🔴 **ประตูส่งจริงยังปิด** (`GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED = None`) · สิ่งที่ตกไปคือ **ไบต์**
> ที่เหลือ **สามข้อ** (`pf-adversary` นับใหม่ให้ในรอบเดียวกัน ฉบับแรกเขียนว่า "เหลือข้อเดียว" ซึ่งผิด):
> (A) ตัวตนต่อ connection ที่คอมเมนต์ `IDENTITY, STATED HONESTLY` ของ `runtime.py` (4886-4896 ณ commit นั้น —
> พินเก่า `runtime.py:4765-4774` เลื่อนไปอยู่ damage dispatch แล้ว) · คำเคาะของ COO · และ (B) เรื่อง**จอ**
> ซึ่ง RE-132 แค่ตัดทางที่มันจะพังที่ถูกที่สุดออก (handler ที่ไม่วาดอะไรเลย) ไม่ได้ทำให้ผ่าน
> คำกล่าวว่า "ขึ้นจอ" ยังต้อง `GT-016`/`GT-133` (ชั้น client-observable) ตาม nonclaim ของใบผลเอง

> NUMBERING NOTE: ตัวนับร่วมกับ `GAME_TEST_QUEUE.md` -- เลขสูงสุดบน main ก่อนจอง = `GT-131` (สาย A)
> และ `RE-130` · grep ยืนยันก่อนจอง 2026-08-28T23:2x: `RE-132`/`GT-132` = 0 hit ทั้งสองไฟล์
> ⇒ ใบ RE นี้ = `RE-132` และใบเทสคู่กัน = `GT-133` (เว้น `GT-132` ไว้กันชนกับใบที่อาจจองพร้อมกัน)

**ค้นใน `pf_bridge/external/` แล้ว: ไม่เจอ** · **ค้นใน `pf_bridge/gamedata/` แล้ว: ไม่เจอ**
(0 แถวที่เกี่ยวกับ `0x9F2C` / `GMGlobal` / `vital_version` ในทั้งสองไฟล์ SEARCH_HERE_FIRST)
**เจอจุดตั้งต้น:** `external/PF_PROTOCOL_REGISTRY.tsv:180` มีแถว `Channel_GMGlobalMessageVital` ครบทุก VA

### คำถาม
1. `0x9F2C` -- ctor เขียนไบต์อะไรลง `message+0x10` (ช่อง `vital_version`) · ขอ **ตัวเลข + VA ของไซต์ที่เขียน**
2. `0xAC52` -- ค่าเดียวกัน **ด้วยวิธีเดียวกันเป๊ะ** (ตัวคุม: โปรเจกต์รู้คำตอบอิสระอยู่แล้วว่า `0` จาก
   hash ของเฟรมที่ capture จริง CHAT-ECHO-001/002) ⇒ ได้ `0` = วิธีถูก เชื่อข้อ 1 ได้ · ได้ค่าอื่น = ตีใบกลับ
3. (ถ้างบรอบยังเหลือ) handler `0x0065C850` ของ channel family อ่าน payload แล้วส่งต่อไปเรนเดอร์จริงไหม
   -- RE-129 เจอมาแล้วว่า handler ที่จดทะเบียนไว้อาจเป็น `mov al,1; ret 4` ⇒ version ถูก = จำเป็น ไม่พอ

### จุดตั้งต้น (จาก TSV แถวเดียวกัน เทียบกับตัวคุม)
`0x9F2C`: `getter_va 0x0065AC10` (ctor ของ `ForcePos` อยู่ **ก่อน** getter ของแถวตัวเองพอดี ตาม RE-129)
· `vtable 0x00F3790C` · `reg_site 0x00BF7390` · serializer/handler = `0x0065AD40`/`0x0065C850`
`0xAC52`: `getter_va 0x006580B0` · `vtable 0x00F3775C` · serializer/handler **ตัวเดียวกัน**

### ทำไมอนุมานจาก `0xAC52` ไม่ได้ทั้งที่ serializer เดียวกัน
`vital_version` **ไม่ได้อยู่ใน payload** -- อยู่ใน envelope หนึ่งไบต์ต่อหนึ่ง nested vital
(`u8tag(0x0B, vital_version)`, `pf_login_game_server_v141.py:702-704`) ⇒ การใช้ serializer ของ payload
ร่วมกันแบบ byte-identical ไม่ได้พูดถึงไบต์นี้เลย · สี่ค่าที่วัดแล้วไม่เท่ากัน (`0x5A19`→0 · `ForcePos`→0
· `TeleportVital`→4 · `SelectActor`→10) **ไม่มี default** · เดาแล้วเจ้าของเสียเซสชัน (`GT-101`, `ErrorData=23065`)

### เกณฑ์จบใบ
ตอบข้อ 1+2 พร้อม VA **หรือ** bounded negative ⇒ ปิดใบพร้อม `BUILD_IMPACT:` ว่าค่าคงที่
`say_wire.GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED` เปิดได้หรือไม่ · ถ้าคำตอบ != `0`
สายนี้ **จะไม่เปิดค่าคงที่และจะไม่เขียน codec ตัวที่สอง** -- ต้องขอ parameter จากสายเจ้าของ
`channel_message_hypothesis.py` แทน (บังคับไว้ด้วยเทสแล้ว: `tests/test_gm_say_action.py`)

### 🔵 ก่อนลงมือ: มีใบ attended ที่วัดไบต์เดียวกันนี้จากชั้นที่สูงกว่าอยู่แล้ว
`GT-016` (ระบุใน `docs/HYPOTHESIS_LEDGER.json` / `docs/FUNCTIONAL_COVERAGE.json` ของ repo เซิร์ฟเวอร์)
= ส่งทั้งห้า channel ของ serializer `0x65AD40` รวม GMGlobal ให้ client จริงแล้วดูว่าอะไรเรนเดอร์
⇒ ถ้าใบนั้นบูตแล้ว **ให้เอาผลของมันมาก่อน ใบนี้อาจกลายเป็นแค่การยืนยันซ้ำ**
(สายนี้เพิ่งรู้จาก pf-adversary รอบ `w8hnu9`) · และ `runtime.py:2126-2147` ก็ส่งเฟรม 0x9F2C
ที่ถือไบต์ `0` ออกสายได้อยู่แล้วภายใต้ scenario flag ⇒ ถ้ามีคน capture ไว้ ก็เป็นหลักฐานอีกทาง

**ADDRESSEE: RE** · ผู้เปิดใบ: LANE-GM (`w8hnu9`) · ใบเทสที่รอผลนี้: `GT-133`
🔴 ปิดแล้วแจ้งกลับในกล่องทันที -- สายนี้บริโภคผลใบที่ตัวเองเปิดในรอบถัดไป

