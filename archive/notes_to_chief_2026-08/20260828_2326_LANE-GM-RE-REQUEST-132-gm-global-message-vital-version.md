[ถึง: chief (สาย E) -> สาย RE runner | ADDRESSEE: LANE-RE | cc: COO, เจ้าของ, ผู้เทส | จาก: LANE-GM รอบ `w8hnu9` · 2026-08-28T23:26+07:00]

# RE-132 GM-GLOBAL-MESSAGE-VITAL-VERSION-001 — ไบต์ `vital_version` ของ `Channel_GMGlobalMessageVital` (`0x9F2C`)

**ค้นใน `pf_bridge/external/` แล้ว: ไม่เจอ** — `grep -inE "0x9F2C|GMGlobal|vital_version|version" external/00_SEARCH_HERE_FIRST.md` = 0 แถวที่เกี่ยว
(แถวเดียวที่ match คำว่า `version` เป็นโครง `u16 version` ของไฟล์ NPC placement คนละเรื่อง)
**ค้นใน `pf_bridge/gamedata/` แล้ว: ไม่เจอ** — `grep -inE "9F2C|GMGlobal|version" gamedata/00_SEARCH_HERE_FIRST.md` = แถวเดียวกันนั้น
ใบนี้เป็นคำถาม **code** ไม่ใช่คำถาม gamedata

**เจอในตารางที่มีอยู่แล้ว (ใช้เป็นจุดตั้งต้น ไม่ใช่คำตอบ):** `external/PF_PROTOCOL_REGISTRY.tsv:180` มีแถว
`Channel_GMGlobalMessageVital` ครบทุกคอลัมน์ VA — และนั่นคือเหตุผลที่ใบนี้ควรถูกกว่าสองใบก่อนหน้า

## คำถามเดียว

`Channel_GMGlobalMessageVital` (`0x9F2C`) — prototype/bootstrap constructor ของ vital ตัวนี้ `mov`
ค่าอะไรลงไบต์ `message+0x10` (ช่อง `vital_version` ที่ generic reader เทียบแบบ exact-equality)
ต้องการ **ตัวเลข + VA ของไซต์ที่เขียน** ไม่ใช่การอนุมานจาก vital ตัวอื่น **แม้จะเป็นตัวที่ใช้ serializer เดียวกัน**

## วิธี — ทำซ้ำ RE-105/RE-129 ตัวต่อตัว และคราวนี้มี **ตัวตรวจคำตอบในตัว**

RE-105 (`0x5A19` → 0) และ RE-129 (`ForcePos` → 0, `TeleportVital` → 4) ตอบคำถามรูปนี้สำเร็จมาแล้วสองครั้ง
กลไกที่ทั้งสองใบระบุตรงกัน: generic VitalData collection reader ที่ `[0x005F3E20,0x005F406D)` เทียบ
exact-equality กับ `message+0x10` · ไบต์นั้นตั้งโดย ctor ของ vital แต่ละตัวเอง ด้วย `mov` ตรง ๆ
(`ForcePos`: `xor ecx,ecx` แล้ว `mov byte ptr [eax+0x10],cl` ที่ `0x005E5186` ใน ctor `[0x005E5170,0x005E51A2)`
ซึ่งอยู่ **ก่อน** `getter_va` ของแถวเดียวกัน `0x005E51C0` พอดี)

**จุดตั้งต้นสำหรับใบนี้ จาก `PF_PROTOCOL_REGISTRY.tsv:180`:**

| คอลัมน์ | `Channel_GMGlobalMessageVital` | `Channel_LocalTalkMessageVital` (ตัวคุม) |
|---|---|---|
| `getter_va` | **`0x0065AC10`** ← ctor น่าจะอยู่ก่อนหน้านี้ | `0x006580B0` |
| `vtable_va` | `0x00F3790C` | `0x00F3775C` |
| `serializer_va` | `0x0065AD40` | `0x0065AD40` (ตัวเดียวกัน) |
| `handler_va` | `0x0065C850` | `0x0065C850` (ตัวเดียวกัน) |
| `reg_site_va` | `0x00BF7390` | `0x00BF72D0` |

🔵 **ขอสองค่า ไม่ใช่ค่าเดียว — ค่าที่สองคือด่านตรวจว่าวิธีถูก:**
1. `0x9F2C` → ไบต์อะไร (คำตอบที่สายนี้ต้องใช้)
2. `0xAC52` (`Channel_LocalTalkMessageVital`) → ไบต์อะไร **ด้วยวิธีเดียวกันเป๊ะ**
   ค่านี้โปรเจกต์รู้คำตอบอยู่แล้วโดยอิสระ: `channel_message_hypothesis.py` ประกอบด้วย `vital_version = 0`
   แล้ว **ตรงกับ hash ของเฟรมที่ capture จริง** (CHAT-ECHO-001/002 pins)
   ⇒ ถ้าวิธีของใบนี้ให้ `0xAC52 = 0` แปลว่าวิธีอ่านถูก และคำตอบข้อ 1 เชื่อได้ทันที
   ⇒ ถ้าให้ค่าอื่น **อย่าเพิ่งตอบข้อ 1** ใบนี้เขียนโจทย์ผิด ให้ตีกลับ

## ทำไมเรื่องนี้เป็นคอขวดจริง

รอบ `w8hnu9` (คืนนี้) ต่อเส้นทาง `/say` จนครบทุกขั้น: บรรทัดแชท `0xAC52` → allowlist → parse →
`gm/say_wire.py` ประกอบเฟรม `0x9F2C` ผ่าน encoder ที่พิสูจน์แล้วของสาย CHAT-CHANNEL → คืน action
ให้ dispatch ส่ง · **ทุกขั้นเขียว ยกเว้นขั้นสุดท้ายที่สายนี้กั้นไว้เอง** ด้วย
`say_wire.GM_GLOBAL_MESSAGE_VITAL_VERSION_CONFIRMED = None`

**ทำไมไม่หยิบ 0 ของ `0xAC52` มาใช้เลย ทั้งที่ serializer เดียวกัน:** เพราะ `vital_version`
**ไม่ได้อยู่ใน payload** มันอยู่ใน envelope หนึ่งไบต์ต่อหนึ่ง nested vital
(`u8tag(0x0B, vital_version)`, `pf_login_game_server_v141.py:702-704`) ⇒ การที่สอง channel ใช้
serializer ของ **payload** ร่วมกันแบบ byte-identical ไม่ได้พูดถึงไบต์นี้เลยแม้แต่คำเดียว
และสี่ค่าที่โปรเจกต์วัดมาแล้วก็ไม่เท่ากัน (`0x5A19`→0 · `ForcePos`→0 · `TeleportVital`→4 ·
`SelectActor`→10) ⇒ **ไม่มี default** · การอนุมานข้ามตัวคือรูปเหตุผลเดียวกับที่ผลิตเลข `1`
ที่ `GT-101` วัดของจริงแล้วว่า **ฆ่าเซสชันของเจ้าของ** (modal `ErrorData=23065` → หยุดทั้ง connection → ปิด socket)

## เกณฑ์สองชั้น (สำหรับใบนี้)

- **wire/DB (ชั้นที่ใบนี้ต้องได้):** VA ของ ctor + ไบต์ที่มัน `mov` ลง `+0x10` สำหรับทั้ง `0x9F2C` และ `0xAC52`
  · ถ้าอ่านแล้วเป็น register ให้ตามหาว่ามันถูกตั้งเป็นค่าอะไรก่อนหน้า (แบบ `xor ecx,ecx` ของ `ForcePos`)
- **client-observable (ไม่ใช่ของใบนี้ แต่บอกไว้ว่าใบไหนรับช่วง):** `GT-133` (คิวเทส รอบนี้) — GM พิมพ์
  `/say <ข้อความ>` แล้วเห็นข้อความบนจอตัวเอง · บูตได้ต่อเมื่อใบนี้ตอบ **และ** `CORE-REQUEST-GM-029` ลง main

## nonclaim ของใบนี้

1. **[ไม่อ้าง]** ว่าได้ไบต์แล้ว `/say` จะขึ้นจอ — RE-129 สอนไว้แล้วว่า version ถูกเป็นเงื่อนไข
   **จำเป็น ไม่ใช่เพียงพอ** (`ForcePos` ได้ version ถูกแล้วยังเจอ handler ที่เป็น `mov al,1; ret 4`)
   ใบนี้ขอเพิ่มด้วยถ้าดูได้ในรอบเดียวกัน: **handler `0x0065C850` ของ channel family อ่าน payload
   แล้วส่งต่อไปเรนเดอร์จริงหรือเปล่า** (ถ้าตอบไม่ได้ในงบรอบเดียว ให้ตอบข้อ 1-2 ก่อน อย่าดองใบ)
2. **[ไม่อ้าง]** ว่า `0x9F2C` จะถึงผู้เล่นคนอื่น — action ของสายนี้ไปที่ socket เดียว (ของ GM เอง)
   การกระจายทั้งเซิร์ฟเวอร์เป็นจุดใน runtime และเป็นใบ CORE-REQUEST คนละใบ ยังไม่เปิด
3. **[ไม่อ้าง]** ว่าคำตอบของใบนี้ปลดล็อก `/warp` — คนละไบต์ คนละใบ และ `/warp` ยังติด
   `COO-DECISION 20260828_2130` + `CORE-REQUEST-GM-030` อยู่เหมือนเดิม

## ถ้าคำตอบคือค่าที่ไม่ใช่ 0

`channel_message_hypothesis.py` hardcode `0` ไว้ และโมดูลนั้น **ไม่ใช่เขตเขียนของสาย GM**
⇒ สายนี้จะ **ไม่** เปิดค่าคงที่ และจะ **ไม่** เขียน codec ตัวที่สองในเขตตัวเอง (รอบ 27 ส.ค. ลองแล้วและถอนไปแล้ว)
จะเขียนใบขอ parameter `vital_version` ถึงสายเจ้าของโมดูลแทน · เส้นทางนี้มีเทสบังคับไว้แล้ววันนี้
(`tests/test_gm_say_action.py::SayVersionGateTests::test_a_confirmed_byte_the_codec_cannot_emit_still_sends_nothing`)

---
_Generated by [Claude Code](https://claude.ai/code)_
