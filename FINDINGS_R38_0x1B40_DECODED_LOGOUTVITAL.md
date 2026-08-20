# FINDINGS R38 — `UNKNOWN_0x1B40` = **`LogoutVital`** (decode สำเร็จ, headless, อ่านอย่างเดียว)

รอบ 38 (scheduled, 2026-08-17 17:55–18:1x) · งานตาม next ของ LOCK รอบก่อน + ข้อ 27.5(ก)
ไม่แตะ src · ไม่เปิดเกม · ไม่ request_access · หลักฐานทั้งหมด read-only

## Claim เดียวของ finding นี้ (เกรด B)

**เฟรม `0x1B40` ที่ client ส่งตอนกดปุ่มใน dialog ออกจากเกม (GT-002, 16:44–16:52) คือ
vital ชื่อ `LogoutVital` ของโปรโตคอลฝั่ง client** — server (Foundation) ยังไม่มี handler
จึงไม่ตอบ → ปุ่มออกทุกปุ่มใน dialog นั้นใช้ไม่ได้ (ตรงกับที่ผู้เทสเห็น client2 ค้าง)

## วิธี decode (ทำซ้ำได้ทุกขั้น)

1. registry hash ของเกม (กู้ไว้แล้วใน `current/pf_login_game_server_v141.py` บรรทัด 5150):
   `protocol_name_id(name) = sum((i+1)*ord(c) for i,c in enumerate(name)) & 0xFFFF`
2. ดึง identifier strings ทั้งหมดจาก `GameClient/GameClient.local.bin` (สำเนาใน /tmp,
   ไฟล์ต้นฉบับไม่ถูกแตะ): regex `[A-Za-z_][A-Za-z0-9_]{3,60}` → **15,954 strings**
3. หา string ที่ hash = 0x1B40 → **เจอตัวเดียวทั้ง binary: `LogoutVital`**
4. validation ของวิธีการ (ไม่ใช่การเดา):
   - `0x3D4B` → candidate เดียว = `GetWorldInfoVital` (ตรงกับ NAMES เดิม) ✓
   - NAMES ทั้งตารางของ v141 (47 ชื่อ): **46/47 hash ตรง id + string อยู่ใน binary จริง**
     (ยกเว้น `ItemOperateVital` 0x36FE ซึ่ง hash ตรงแต่ string ไม่อยู่ใน binary — ชื่อ
     ฝั่ง server-registry เดิม ไม่กระทบวิธีการ)
   - namespace ชื่อ vital ที่ไม่ใช่ AV* มี **327 ชื่อ, hash ไม่ชนกันเลย (0 collisions)**
     → การจับคู่ id→ชื่อภายใน namespace นี้ unambiguous
5. หลักฐานประกอบใน binary: มี `AVLogoutVital` (twin แบบเดียวกับ AV* ของทุก vital ที่รู้จัก)
   และ `AVSystemSettingLogoutConfirmEventHandler` / `AVSysetmSettingLogoutEventHandler`
   (typo ของเดิมในเกม) = handler ของ dialog ยืนยัน logout — ตรงพฤติกรรมที่จับได้เป๊ะ
   (เปิด dialog → ยิง `GetWorldInfoVital` → กดยืนยัน → ยิง `LogoutVital`)

## โครง payload 14B (parse ตาม tag ที่ v141 ใช้อยู่: 0x08=u8, 0x14=u32)

`08 <subcode> 08 00 14 00000000 14 00000000`
- subcode `01` = ปุ่ม "ออกจากเกม" (จับได้ 3 ครั้ง: seq 3/5/7)
- subcode `03` = ปุ่ม "กลับหน้าเลือกตัวละคร" (seq 9)
- ที่เหลือ (u8=0, u32=0 สองตัว) — ความหมาย field ยังไม่พิสูจน์ (nonclaim)

## ของแถม (เกรด C — candidate แข็งแรง ยังไม่ถึง claim)

**`0xAC52` ของ GT-006 (แชท) น่าจะ = `Channel_LocalTalkMessageVital`** — ใน namespace
vital ไม่มีตัวชน (มี collision เดียวคือ `AVCreateActorPickEventHandler` ซึ่งเป็น
handler ฝั่ง client ไม่ใช่ wire name) + semantic ตรง payload ที่จับได้
("PFCHATPROBE1/2" UTF-16LE = ข้อความแชท local ที่ผู้เทสพิมพ์) → ยกระดับเป็น claim ได้
เมื่อเขียน handler/response แล้วพิสูจน์ runtime — แถว matrix `chat/client_chat_input`
มีชื่อ protocol ให้อ้างแล้ว

**Asset ใหม่:** `pf_bridge\VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — ตาราง
id→ชื่อ ครบ **327 wire vitals** จาก client binary (collision-free) = unknown id
ตัวถัดไปทุกตัว decode ได้ทันทีด้วย lookup เดียว ไม่ต้องทำงานนี้ซ้ำ

## Nonclaims

1. ไม่ claim ว่ารู้ semantic ครบของ payload (รู้แค่ subcode 01/03 จาก correlation ปุ่ม)
2. ไม่ claim ว่ามี subcode 02 หรือค่าอื่น (ไม่เคยจับได้ — `ReturnSelectServerVital`
   0x709E เป็น vital แยกต่างหาก อย่าเหมารวม)
3. ไม่ claim ว่า server "ควร" ตอบอะไร — คำตอบที่ถูกของ original server ไม่มีใน corpus
   (ต้องเป็น hypothesis ใหม่ถ้าจะ implement)
4. ไม่ claim เหตุที่ client1 ปิดผ่าน X ได้แต่ client2 ไม่ได้ — dialog ปิดเกมของ client1
   เป็น client-local ยังไม่เห็นเส้นทางที่ต่างกันจากข้อมูลชุดนี้
5. การมีชื่อใน binary ≠ server ต้องรองรับทุกตัว — 327 ชื่อคือ namespace ของ client
   ไม่ใช่ backlog งาน

## ข้อเสนอต่อ Panya (ตัดสินใจใหญ่ — เขียนค้างไว้ ไม่ทำเอง)

เปิด **HYP-PF-012 "LogoutVital acknowledged logout"**: Foundation ตอบ `LogoutVital`
subcode 01/03 แล้วปิด session สะอาด (`closed_at` เขียน, client ได้ออกจริง) —
ปลดสถานะ "client ค้างต้อง End task" + เพิ่มแถว matrix `session_lifecycle/clean_logout`
· ต้องออกแบบ response shape เอง (ไม่มี golden ใน corpus → production_allowed=false,
opt-in scenario, fail closed) · เทสยืนยันชั้น client-observable ต้องเข้าคิวรอบใหญ่
