ถึง: chief (cloud)

# GT-045 v2 — WIRE EXACT / CLIENT NO-RESULT (viewpoints not reached)

เวลา: 2026-08-24 09:54–10:06 +07:00  
ผู้รัน: OpenAI Codex LOCAL, unattended ตามคำสั่ง Panya รอบนี้

## คำตัดสิน

- ชั้น wire/DB: **PASS ตรง v2**
- ชั้น client-observable: **NO-RESULT — ห้ามปิดเป็นผลลบ**
- ในมุมกล้องที่บันทึกต่อเนื่อง ไม่เห็นป้ายชื่อหรือโมเดลใหม่ แต่ตัวละครค้างอยู่หน้าแผงถัง/ชั้นไม้ที่จุดเกิด และการกดสั้นผ่าน computer control ไม่พาไป G1b/G2 หรือกวาด 360 องศาได้ จึงยังแยก “ไม่วาด” ออกจาก “วาดนอกมุม/ถูก geometry บัง” ไม่ได้

## Wire v2

- exact green boot: `fa1e804a336323c2273dd3c3716db5204495f0d7`; tree ตรง main HEAD `94f0ce33194aabdfa9d39e78a085d4b86babd294`
- trigger TargetPos แรกหลัง runtime ack: `(-8553.947265625, -2579.68896484375, 186.0)` heading `4.532132625579834`
- `GROUND_LOOT_BIT08_RENDER_NEAR_ONCE` แล้ว `...FAR_ONCE` อย่างละ 1 ครั้ง เรียงถูกต้อง
- near PC 44 bytes; decoded `(-8523.947265625, -2579.68896484375, 186.0)` = trigger `+30X`; masked SHA256 `915331D5103215675E246B0011B054C9D4F7D2C4D48C8E2B010A45C3D0F5FC33` PASS
- far PC 44 bytes; decoded `(-7753.947265625, -2579.68896484375, 186.0)` = trigger `+800X`; masked SHA256 `DC6A8FE62BC2C89B92AFA8060D2CEC5DCCDF23D81A242F95AA354C5BD48F8A14` PASS
- raw GAME: `GameClient\capture_gt045_20260824_095602\capture_v141\GAME_20260824_095733_476507_64798.txt`; SHA256 `59A3AE899EC048C7FFAE46C4B674EC8CBB6252F72F99BC482A19B21FD2BF5763`

## Client-observable

- G0/HUD: Port Royal, HP 100/100, `X -8,553 / Y -2,579`, local-server-online; กล้องถูกชั้นไม้และถังบังพื้นที่ข้างหน้า
- near/far ออกประมาณ `09:59:03.447–09:59:03.466 +07`; วิดีโอเริ่ม `09:56:04.820`, ดังนั้นช่วงยิงอยู่ที่ประมาณ `t=178.627s`
- contact sheet 10 fps ช่วง `t=177.5–181.5s` และภาพเดี่ยว `t=170, 179.1, 184, 420s` ไม่เห็นป้ายชื่อ/โมเดลใหม่ใน **มุมที่เห็นอยู่**; ไม่ใช้สิ่งนี้สรุปว่าไม่มี render ที่พิกัด
- Q/Q/D และชุด W/S แบบกดสั้นไม่ทำให้ HUD/ภาพหรือ TargetPos เปลี่ยนจากค่า trigger; computer-control สูญเสียการ enumerate หน้าต่างช่วงท้าย ทั้งที่ process ยังอยู่ จึงปิดด้วย guarded teardown (CloseMainWindow 15s แล้ว force เฉพาะ PID ที่ identity/time-window ผ่าน)
- วิดีโอ: `pf_bridge\evidence_screens\1079_gt045_FULLROUND_20260824_095604.mkv`; 603.300s; SHA256 `3F6A4DDB98A7B66F9D6128162FC4A17173260B5791A603CDFA22B7FCC9016838`
- contact: `GT045_20260824_G1_177p5-181p5_10fps-contact.png`; SHA256 `42368C9D9EF94521AF5CE1A9E8737AFF95CBCA909ECC5C0AD16BF8E48378C471`

## DB / teardown

- run copy selected sessions `10 -> 11`; max lease `11 -> 12`; open sessions `0`; `integrity_check=ok`; FK rows `0`
- canonical SHA ก่อน/หลังตรง `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21`
- stopped marker `1`; ready markers `2`; traceback `0`; stderr `0B`; final listeners `0`; GameClient `0`; ffmpeg `0`

## Nonclaims

- ไม่ claim ว่า original server เคยใช้ช่องนี้; element เป็นดีไซน์ของเรา
- ไม่ claim ว่า render = หยิบได้; render/pickup เป็นคนละเรื่อง
- วิดีโอเป็น client-observable ไม่ใช่หลักฐาน transport
- ไม่แปลงหน่วยพิกัดโลกเป็นหน่วยจริง
- สำคัญที่สุด: **ไม่ claim ว่าบิต `0x08` ไม่วาด** เพราะ G1b/G2 ไม่ถึงและมุมปัจจุบันถูก geometry บัง

