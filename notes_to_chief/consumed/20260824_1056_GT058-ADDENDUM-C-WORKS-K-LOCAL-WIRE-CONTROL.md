ถึง chief — addendum ตามคำถาม Panya: เมนูอื่นเปิดได้หรือไม่ และตอนกด K มีแพ็กเกจอะไรวิ่งบนสาย

# GT-058 UI/wire control — C, Quest, Reward เปิดได้; K/Skill ไม่เปิดและไม่ปล่อย application request

- เวลา control: 2026-08-24T10:41:33+07:00 ถึง 2026-08-24T10:50:54+07:00
- ข้อสรุป client-observable: hotkey `C` เปิดหน้าต่าง `CHARACTER` ได้ทันที; คลิกไอคอน `Quest (J)` และ `Reward` ที่เมนูล่างซ้ายก็เปิดหน้าต่างของตนได้ตามปกติ. แต่ hotkey `K` และการคลิกไอคอนที่ tooltip ระบุ `สกิล (K)` โดยตรงยังไม่เปิดหน้าต่างใด.
- ข้อสรุป wire: ในช่วงครอบคลุมการกด K และคลิก Skill โดยตรง ไม่มี client->server application request เพิ่มขึ้น. มีเฉพาะ Runtime heartbeat ตามรอบและ server heartbeat/keepalive พื้นหลัง.
- ดังนั้นอาการไม่ใช่ keyboard injection, focus หรือระบบเมนูล่างซ้ายเสียทั้งชุด; failure ถูกจำกัดอยู่ที่เส้นทางเปิด Skill window ใน local baseline นี้. สาเหตุภายในยังไม่พิสูจน์.

## Procedure / visual control

1. เข้า Port Royal บน green boot เดิม เห็น HP 100/100, minimap, map name และข้อความ local server online.
2. คลิกโลกเพื่อ focus แล้วกด `C`: หน้าต่าง `CHARACTER` เปิดสำเร็จ.
3. ปิด Character, คลิกโลกเพื่อ focus แล้วกด `K`: ไม่มีหน้าต่างเปิด.
4. คลิกไอคอน Skill โดยตรง: tooltip `สกิล (K)` แสดง แต่ไม่มีหน้าต่าง Skill.
5. คลิกไอคอน Quest: หน้าต่าง `QUEST` เปิดสำเร็จ; ปิดด้วย X.
6. คลิกไอคอน Reward: หน้าต่าง `REWARD` เปิดสำเร็จ; ปิดด้วย X.
7. ปิด client ผ่าน X + ปุ่มยืนยัน แล้วทำ guarded teardown.

## Wire control — สิ่งที่วิ่งตอน K

แหล่งหลักคือ `server_console_live.out.txt`, raw GAME log และ `GAME_EVENTS_LIVE.txt` ของรอบนี้. วิดีโอเริ่ม `2026-08-24T10:41:33.087+07:00`; Character ปิดก่อน K ประมาณ offset 390s, direct Skill click เห็น tooltip ตั้งแต่ประมาณ offset 423s และ Quest เปิดประมาณ offset 434s. ดังนั้น K/Skill action ทั้งชุดอยู่ก่อน Reward click แน่นอน.

- C2S frame `#21` ถึง `#178` รวม 158 เฟรม: **ทุกเฟรมยาว 12 bytes และเป็นเพียง `GSCN_RunTimeProtocolReq` id 28271 (`0x6E6F`) แบบไม่มี nested vital**; `NON12=0`.
- ใน interval เดียวกัน S2C มี exact-empty `RuntimeRes v4` 98 ครั้ง (PC 14 bytes) และ `HYP_PF_009_SECOND_PASSWORD_OK_KEEPALIVE` 60 ครั้ง (44 bytes). ทั้งสองชนิดเป็น traffic พื้นหลังที่วิ่งต่อเนื่องอยู่แล้ว ไม่ใช่ผลตอบ K.
- `GAME_EVENTS_LIVE.txt` ไม่มี event ระหว่าง TeleportVital frame `#18` เวลา `10:45:43.405+07:00` กับ frame `#179` เวลา `10:49:04.720+07:00`.
- non-heartbeat C2S ตัวแรกหลัง K/Skill controls คือ frame `#179`: outer `GSCN_RunTimeProtocolReq`, nested unknown id `0x4BF1`, 24-byte PC, nested payload `0B060B00`. เวลา `10:49:04.720` ลบ video start ได้ offset `451.633s` ซึ่งตรงกับช่วงคลิก Reward/หน้าต่าง Reward เปิดในวิดีโอ; จึงแยกออกจาก K control. ไม่ตีความ semantics ของ `0x4BF1` เกิน correlation นี้.
- control ถัดไปที่ไม่ใช่ heartbeat คือ frame `#202`, `UserSetting_UpdateServerSettingVital`, เกิดในช่วงออกจากเกม ไม่เกี่ยวกับ K.

ข้อจำกัด: raw GAME log ไม่ timestamp heartbeat ทุกเฟรม จึงไม่อ้างว่า heartbeat หมายเลขใดตรงกับ keydown แบบ sub-second. หลักฐานเป็น interval ครอบที่กว้างกว่า action จริง; แต่เพราะทุก C2S frame ทั้ง interval `#21..#178` เป็น empty heartbeat จึงตัด distinct K/Skill application request ออกจาก capture รอบนี้ได้.

## Evidence + sha256

- full video `pf_bridge/evidence_video/1085_gt058_FULLROUND_20260824_104132.mkv`
  - duration `556.133s`, sha256 `F51B93BB1B2E059AADBDA4F7E46280ECB316932B028B89884A8CBCC18870C6A1`
- C/Character open `pf_bridge/evidence_screens/GT058_UICTRL_C_CHARACTER_OPEN_330s.jpg`
  - `A3FEC7D810B5248E50F2532F9B6AA88BD5AA2692218CF6C628F25A54C2CD4A43`
- K/Skill direct-click, tooltip present but no window `pf_bridge/evidence_screens/GT058_UICTRL_K_SKILL_ICON_NO_WINDOW_425s.jpg`
  - `1729CA86CE1D09790E885C05EFCE9D32BFE11527A9E8D0B344903D35E9BFB28B`
- Quest icon open `pf_bridge/evidence_screens/GT058_UICTRL_QUEST_ICON_OPEN_435s.jpg`
  - `ED5991F5BACBD4C3C427BA55A002064F4CC3145359D47581E1AA939A98513A9E`
- Reward icon open `pf_bridge/evidence_screens/GT058_UICTRL_REWARD_ICON_OPEN_455s.jpg`
  - `6167AB97C5C5CD3010FABC848AE6A644C7FAC7238784307EB9D1443669B3F2F2`
- raw GAME `GameClient/capture_gt058_20260824_104128/capture_v141/GAME_20260824_104416_015691_61300.txt`
  - `5F454166CF05FAAEF1579A0AEFF7EEAA9DE10AF96313833BF19368FF01D4EB16`
- GAME events `GameClient/capture_gt058_20260824_104128/capture_v141/GAME_EVENTS_LIVE.txt`
  - `08750BD77E74E4E011130A0474EBB39A4F27C3AED57AFBF2E819E2F64CD9886F`
- server console `GameClient/capture_gt058_20260824_104128/server_console_live.out.txt`
  - `B5E8FCFE56F4352008C2E8CB91E16E4133ED59F2ECD10B726AD2A62A196590FB`

## DB / teardown

- canonical ก่อน/หลังตรง `CANON_SHA.txt`: `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21`; ไม่เปลี่ยน.
- run-copy หลัง `6A4F3B15082A285BD875C6ED15A11D2D634D57174B24695B13D6060FA9D9FE97`; เปลี่ยนเฉพาะตาราง `sessions` โดยเพิ่มหนึ่ง closed session, selected sessions 10 -> 11, max lease 11 -> 12, open sessions 0.
- `PRAGMA integrity_check=ok`, foreign-key rows 0; ตารางอื่นมี row digest ตรง backup.
- final topology: listeners 10188/10189 = 0, GameClient = 0, server/console = 0, ffmpeg = 0, traceback markers = 0.

## Interpretation / nonclaims

- สิ่งที่พิสูจน์: UI framework และ keyboard input ใช้งานได้; K/Skill path ไม่เปิดหน้าต่าง และไม่ปล่อย distinct application request ใน capture นี้.
- inference เท่านั้น: Skill window น่าจะเป็น client-local path ที่ถูก baseline state/prerequisite ปฏิเสธก่อนถึง network. รอบนี้ไม่ได้พิสูจน์ prerequisite หรือ root cause.
- ไม่ claim ว่า client ไม่มี traffic เลย: มี Runtime heartbeat และ keepalive พื้นหลังชัดเจน.
- ไม่ claim semantics ของ `0x4BF1`; ระบุเพียง timing correlation กับ Reward control.
- addendum นี้เสริม `20260824_1037_GT058-CORRECTION-P2-SKILL-WINDOW-UNAVAILABLE-NO-CRASH.md`; ไม่เปลี่ยน wire verdict ของ five-frame GT-058 sweep.
