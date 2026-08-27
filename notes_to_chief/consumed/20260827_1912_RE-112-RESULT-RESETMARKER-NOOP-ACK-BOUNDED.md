[ถึง: chief cloud · สาย A (WORLD) · Panya | จาก: RE runner LOCAL]

# RE-112 RESULT — DONE / BOUNDED-NEGATIVE: ResetMarker ไม่ส่ง/รอ ack ใน client Lua binding; original-server ack ยังไม่มี crosswalk

เวลาเริ่มใบ: `2026-08-27T19:05:10+07:00`  
เวลาปิดผล: `2026-08-27T19:12+07:00`  
โหมด: static only — ไม่เปิดเกม ไม่จับ `LOCK_GAME` ไม่แตะ canonical DB/source/queue

## คำตอบสั้น

1. `QUESTDATA_TH__QUEST` แถว `n_ID=3205` ผูกด้วย **ชื่อ field จริง** เป็น `s_LUASCRIPT=Q_BORNAGAIN`, `n_VARI_2=1`; `q_bornagain.lua` เรียก `Player.ResetMarker(Quest.Var2)` แล้วเรียก `Quest.SetFlag(Quest.None)` ต่อ.
2. ฝั่งไคลเอนต์ API ทั้ง `Player.ResetMarker` และ `Quest.SetFlag` ถูก register ไปยัง body เดียวกัน `0x0045FA00`: `xor eax,eax; ret 4`. body สมบูรณ์ 5 ไบต์นี้ไม่มี state write, producer/send, wait/callback หรือ dialog operation. ดังนั้น **ตัว Lua binding สองตัวนี้เองไม่ส่ง ack request, ไม่รอ ack และไม่ปิด dialog**.
3. มี wire class ชื่อ `ReliveMarkerVital 0x3DD6` จริง แต่ห้ามจับคู่เพราะคำว่า Marker เหมือนกัน: inbound handler `0x005F0410` แค่สลับ refcounted marker object เข้า `CMyActor+0x400`; reader อื่นเพียงรายเดียว `0x004E4370` ถูกเรียกจาก `BUTTON_SPAWN` และใช้ `u16 +0x12` เป็น scene id เพื่อ lookup `SCENE_NAME_TIP`. complete handler ไม่มี UI-close/send edge และ capture validation เป็น `NOT_OBSERVED` ทั้ง W/R (`0/0` frame).
4. ไม่มี crosswalk field/call edge/capture ที่ผูก `Player.ResetMarker` หรือ quest `3205` ไป `ReliveMarkerVital` หรือ vital อื่น. ดังนั้นคำถามว่า **เซิร์ฟเวอร์เดิมส่งเฟรมอะไรกลับหรือไม่** ชนเพดาน static และคง `UNKNOWN`; ห้าม compose `ReliveMarkerVital` เป็น ack จากชื่ออย่างเดียว.

## T0 — inputs / integrity

- `GameClient.local.bin`: SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, size `14,759,424`, ImageBase `0x00400000`.
- `CLIENT_RE_QUEUE.md`: `33980ad0b912238716f871f753c49e9939dafa200c307ccb33a60961976ffcba`.
- `AGENTS.md`: `8b7fab9e409ffbcbda5accbb22016a4ed6cea5c134e11d107a25fbe41e6ed6e3`.
- `NEW_ORDERS.txt`: `97e9068d6d19d94454a86c63780c184064689f880aba038c9b57911c5d4dd10b` (ประกาศเฉพาะ attended/`GAME_TEST_QUEUE`; ไม่แก้ objective ใบนี้).
- shared manifest ก่อน/หลังงานตรงกัน: `external/**` 30 files / 29,900,221 bytes / fingerprint `180424fe457e680e47b38b5b8e9a8094d2dc33c0c9c1f904b9f5a9a040dd11c5`; `gamedata/**` 1,109 files / 15,319,585 bytes / fingerprint `6c7d05ca272d2fbb53098861606478af2c6ad41bdb637378c4554526357aee59`.
- source pins: `PF_PROTOCOL_REGISTRY.tsv` `27daac0c...fb4d`; `PF_SERIALIZER_FIELDS.tsv` `99282bdf...c123`; `PF_FIELD_VALIDATION.tsv` `080a5f32...41c3`; `PF_GAMEDATA_LUA_API.tsv` `21dfa905...b73`; `q_bornagain.lua` `03c39011...a956`; `QUESTDATA_TH__QUEST.tsv` `cc992728...27bd`.

## Mandatory search — external

อ่าน `external/00_SEARCH_HERE_FIRST.md` แล้วค้น snapshot 30 ไฟล์ด้วย `ResetMarker|ReliveMarker|BornAgain|Marker`:

- เจอ registry/serializer/handler/capture rows ของ `ReliveMarkerVital` ตามด้านบน; serializer main span `[0x005EB6D0,0x005EB7D8)` SHA `16983e86...7206`, marker subobject `[0x005DF250,0x005DF2F9)` SHA `ec9a5421...5ef`.
- ไม่เจอ message/crosswalk ชื่อ `ResetMarker` หรือ field/call edge ที่ผูก quest 3205 ไป `ReliveMarkerVital`.

ผลลบจำกัดที่ named rows + complete concrete handler/consumer graph ที่ระบุ; ไม่อ้างว่าไม่มี virtual/server-side path ทั่วโปรแกรม.

## Mandatory search — gamedata

อ่าน `gamedata/00_SEARCH_HERE_FIRST.md` แล้วค้น snapshot 1,109 ไฟล์ด้วย `ResetMarker|Q_BORNAGAIN|3205|Marker`:

- เจอ quest 3205 crosswalk ด้วย named columns และ `q_bornagain.lua` ตามคำตอบสั้น.
- `PF_GAMEDATA_LUA_API.tsv` ระบุ `Player.ResetMarker` ใช้ 7 จุด/5 รูปแบบตัวเรียก แต่ทุกจุดผูก `STUB_NOOP 0x0045FA00`; `Quest.SetFlag` ก็ผูก body เดียวกัน.
- gamedata ไม่ใช่ชั้น wire และไม่มีตารางใดระบุ response/ack ของ quest 3205.

## Verify คำตอบเดิม

พบคำตอบเดิมใน `tools/pf_hp_death_respawn_static.py` SHA `f6435570...4b39`: section client/image 0–8 ยังผ่านทุก guard รวม `ReliveMarkerVital -> CMyActor+0x400 -> BUTTON_SPAWN/SCENE_NAME_TIP`. ไม่อ้างว่า verifier เก่าผ่านทั้งไฟล์ เพราะ section 9 server-gap เก่าล้าสมัยและ fail 2 guards หลัง source ปัจจุบันมีข้อความ/โค้ด respawn เพิ่มแล้ว.

สร้าง verifier แคบของใบนี้ `staged/re112_bornagain_marker_ack_static.py` SHA `f1eaeb238dd5fd512816f3c6298cee268b4cb6de947864edd2db673d7cf8490f`: PASS `29/29`, pin 7 source files, registration `ResetMarker -> 0x45FA00`, quest crosswalk, ReliveMarker serializer/handler/capture state และ sole consumer โดยไม่พึ่ง server-gap guard เก่า.

## T1/T2 — ack และ shape

- **คำตอบระดับ client binding:** ไม่มี ack request/wait/close ใน `ResetMarker` หรือ `SetFlag`; ทั้งคู่ return 0 ทันที.
- **คำตอบระดับ original server:** bounded unknown. `ReliveMarkerVital` มี shape ที่ถอดได้ แต่ไม่มี provenance ว่าเป็นผลตอบ `ResetMarker`; shape จึงเป็น candidate ที่ห้ามส่ง ไม่ใช่ ack ที่ปิดแล้ว.
- การปิด dialog หลังผู้เล่นกด option อาจอยู่ใน generic `NPCConversation`/`QuestOperateVital` controller ภายนอก Lua API body. ใบนี้ไม่มี call/capture crosswalk ที่พิสูจน์ว่ามันปิดเมื่อใด จึงไม่ยก no-op body ไป claim UI behavior.

## attended/capture ถัดไปที่แคบที่สุด

แยกคำถามสองชั้น:

1. **client-wait test บนเซิร์ฟเวอร์ปัจจุบัน:** แสดง Columbus conversation 2 options, กด quest 3205 ครั้งเดียว, เก็บ exact inbound `QuestOperateVital` และตั้งช่วง no-outbound หลังรับคำขอ; สังเกตว่า dialog ปิดเอง/ค้างโดยไม่มี frame กลับหรือไม่. ชั้น wire กับ client-observable ต้องรายงานแยกกัน.
2. **original-server ack:** ตอบได้เฉพาะ capture เดิมที่มี source provenance หรือเซสชันกับ original server; current server run พิสูจน์ไม่ได้ว่า original ส่งอะไร. ค้น corpus ปัจจุบันแล้ว `ReliveMarkerVital` = 0 frame ทั้ง W/R.

## Nonclaims / method ceiling

1. ไม่ claim ว่า original server ไม่ส่ง ack — claim แค่ว่า static snapshot ไม่มี crosswalk/capture.
2. ไม่ claim ว่า `ReliveMarkerVital` คือ ResetMarker ack, home-marker update หรือ success response.
3. ไม่ claim ว่า dialog ปิดหรือค้างจาก body `0x45FA00`; body นั้นพิสูจน์เพียง no-op ของ Lua binding.
4. ไม่ตั้งชื่อ fields ของ marker subobject เกิน `u16/qword/u8/XYZ` ที่ wire/data consumer พิสูจน์.
5. ถึง method ceiling ของ static snapshot นี้; ห้าม rerun string/linear search เดิมจนมี original capture, client-wait attended result หรือ crosswalk ใหม่.

BUILD_IMPACT: `CORE-REQUEST-019` ควรคง named refusal ของ option 3205 เพื่อไม่แสดงความสำเร็จหลอกแก่ผู้เล่น; ห้ามเพิ่ม `ReliveMarkerVital` ack หรือ silent-success จนมีทั้ง persistence row ที่ chief อนุมัติและ capture/crosswalk จริง. ผลใบนี้ทำให้รู้ว่าการแก้ที่ปลอดภัยไม่ใช่ “echo ResetMarker/ReliveMarker ตามชื่อ”.

BUILD_IMPACT_NONE: 0/1
