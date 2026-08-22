ถึง: chief + Panya

# GT-001 recurring smoke — PASS บน latest main `cf81730`

เวลา: 2026-08-23 01:10–01:14 (+07:00) · ผู้เทส: Codex ATTENDED (LOCAL)

## คำตัดสินที่เสนอ

**[PASS]** full loop พื้นฐานบน main HEAD `cf817305327783c4187224c79df3150ced426ae3` (worktree clean): login → เลือก Pirate Force Local / Channel 1 → ยืนยัน PVP → เลือก Arena01 → เข้าแมพ → ออกด้วย X+ปุ่มยืนยัน → server Ctrl+C สะอาด

## Client-observable

- หน้าเลือกตัวละครแสดง Arena01 และ Port Royal ปกติ; ใช้ปุ่มกลางจากห้าปุ่มเข้าเกม
- เข้าแมพสำเร็จ: HP `100/100`, minimap, ชื่อ `Port Royal`, HUD X `-8553` Y `-2579`, และแชท `[system] : Pirate Force local server online` ครบในเฟรมเดียว
- ไม่กดเดิน; กด X มุมขวาบนครั้งเดียวแล้วเห็น dialog ออกจากเกม; กดปุ่มซ้ายยืนยัน หน้าต่างหายภายในไม่กี่วินาที
- ภาพ `pf_bridge\evidence_screens\GT001_map_smoke_20260823_0111.jpg`, 256,980 bytes, SHA256 `01926AC60B0C52C0F3290635ABE5BE1404BA1E839168B32C585421AEBB6A7A6F`

## Wire / DB

- jobs 1010 boot / 1011 teardown ผ่าน; backup ก่อบูต `pf_bridge\backup\pirateforce_before_gt001_20260823_011029.sqlite3` SHA256 `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7`
- selected sessions `7 → 8` (+1), blank-connection sessions `1 → 1`, max lease `8 → 9` (+1), open sessions หลังหยุด = 0
- position identity 1 ไม่เปลี่ยน: scene `1/0`, `(-8553.947265625,-2579.68896484375,186.0,4.53208589553833)`, `updated_at=2026-08-18T10:38:40.374998+00:00`
- backpack ไม่เปลี่ยน: `[(slot0,id1,2600001,q2),(slot1,id2,2400901,q1),(slot3,id4,2200002,q1)]`
- `PRAGMA integrity_check=ok`, FK rows=0; listener ready 2, stopped marker 1, traceback 0, stderr 0 bytes, listeners หลังจบ 0, GameClient 0, inbox ว่าง
- console SHA256 `1D521AD95ABFCE3CB862A348FD1E977FE362EE5ABF6B01E144503733B4AFA28D`; stderr empty SHA `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855`
- raw GAME `GameClient\capture_gt001_20260823_011029\capture_v141\GAME_20260823_011145_797800_64027.txt` SHA256 `F7F189EAE39E28CDA36CC6ADC583F74F1F7ABE2C136CBACFD0CCBF52ACB50DB7`
- `GAME_LIVE.txt` SHA256 `5DAC7FBA70C117C564332F1460D12ECAFC265D4C980E4A931FF04CB0B50DC7D1`

## Canonical SHA update

การเข้าเกมเพิ่ม session ตามที่ GT-001 คาดไว้ จึงทำให้ canonical DB SHA เปลี่ยนแบบคาดหมาย:

`6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7`
→ `23FD885AC4CBBFAC5E06C9B11506F6EA9F985DA82F4522383DFCC14A91C1816A`

`pf_bridge\CANON_SHA.txt` อัปเดตเป็นค่าใหม่แล้ว; backup ก่อเทสยังคงอยู่และ hash ตรงค่าเก่า

## Nonclaims

- smoke นี้ไม่พิสูจน์ inventory operation, combat, movement, chat input, delete หรือ logout button
- ไม่ใช้จำนวน session เปล่าเป็นตัวผ่าน; นับเฉพาะ `selected_character_id IS NOT NULL`
