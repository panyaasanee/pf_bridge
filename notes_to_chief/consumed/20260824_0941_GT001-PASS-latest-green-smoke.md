ถึง: chief + Panya

# GT-001 recurring smoke — PASS บน latest green `fa1e804`

เวลา: 2026-08-24 09:33–09:41 (+07:00) · ผู้เทส: Codex UNATTENDED (LOCAL)

## คำตัดสินที่เสนอ

**[PASS]** full loop พื้นฐานบน resolver-selected green commit `fa1e804a336323c2273dd3c3716db5204495f0d7` (tree ตรง main HEAD `94f0ce33194aabdfa9d39e78a085d4b86babd294`): login → Pirate Force Local / Channel 1 → ยืนยัน PVP → Arena01 → เข้า Port Royal → ออกด้วย X+ปุ่มซ้ายยืนยัน → server Ctrl+C สะอาด

## Client-observable

- เข้าแมพสำเร็จ; เห็น HP `100/100`, minimap, ชื่อ `Port Royal`, HUD X `-8553` Y `-2579` และแชท `[system] : Pirate Force local server online`
- ไม่กดเดิน ไม่สัมผัส inventory/combat; กด X มุมขวาบนครั้งเดียว เห็น dialog และกดปุ่มซ้ายยืนยัน; GameClient ปิดเอง
- ภาพ `pf_bridge\evidence_screens\GT001_20260824_0940_MAP-POSITIVE.png`, SHA256 `0976B3D64F1A382A070DB3B8005134EA0173C7DC432F6E6424E03F0BD2477C77`
- วิดีโอเต็มรอบ `pf_bridge\evidence_screens\1071_gt001_FULLROUND_20260824_093702.mkv`, 15,312,139 bytes, SHA256 `EFEDE73C45CE1E630AF0A39ACB27EF8E963EFCEBF32F8B093A10F95EDF21AA8D`; frame proof 3/3 OK

## Wire / DB / teardown

- selected sessions `9 → 10` (+1), blank sessions `1 → 1`, max lease `10 → 11` (+1), open sessions หลังหยุด = 0
- position identity 1 ไม่เปลี่ยน: scene `1/0`, `(-8553.947265625,-2579.68896484375,186.0,4.53208589553833)`
- backpack ไม่เปลี่ยน: `[slot0/id1/2600001/q2, slot1/id2/2400901/q1, slot3/id4/2200002/q1]`
- `PRAGMA integrity_check=ok`, FK rows=0; listener ready 2, stopped marker 1, traceback 0, stderr 0 bytes, listeners หลังจบ 0, GameClient 0, ffmpeg 0
- `GAME_LIVE.txt` SHA256 `32F6FC0107F9580461A086ABE9B174DEF639B555221CA69AA6C8C0CF53B2D60E`

## Canonical SHA update

การเข้าเกมเพิ่ม selected session/lease ตามที่ใบ GT-001 คาดไว้:

`EE785A79EAC3FDC962AF66E13C2F5943DACF733F0B8D85EAFB658F889A79C17C`
→ `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21`

`pf_bridge\CANON_SHA.txt` อัปเดตแล้ว; backup ก่อเทส `pf_bridge\backup\pirateforce_before_GT-001_20260824_093720.sqlite3` ยังอยู่และ SHA256 ตรงค่าเก่า

## Nonclaims

- smoke นี้ไม่พิสูจน์ inventory operation, combat, movement, chat input, delete หรือ logout button
- ไม่ใช้จำนวน session เปล่าเป็นตัวผ่าน; นับเฉพาะ `selected_character_id IS NOT NULL`
