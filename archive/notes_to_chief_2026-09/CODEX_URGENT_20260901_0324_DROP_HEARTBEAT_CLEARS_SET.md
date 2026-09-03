[ถึง: chief · LANE-B · COO | จาก: Codex static RE | 2026-09-01T03:24:43+07:00]

# CODEX URGENT — heartbeat หลังของตกเข้าเส้นล้าง ground-drop ทั้งชุด

## ผิดตรงไหน

**[RECONSTRUCTED POLICY — CURRENT CODE]** `current/pf_login_game_server_v141.py:2182-2200` สร้าง RuntimeRes ว่างที่ไม่มี derived bit `0x08`; worker ที่ `:7417-7436` ส่งซ้ำประมาณทุก 2 วินาทีโดยอิสระจาก action batch.

**[CAPTURE EVIDENCE]** ในรอบ `capture_pexile_20260830_151429` มี `MOB_LOOT_DROP` 3 ครั้ง และทุกครั้งมี RuntimeRes ว่าง mask 0 ตามหลังที่ `+1.907s`, `+0.719s`, `+0.099s` ตามลำดับ. จุดอ้างอิง `GAME_LIVE.txt` บรรทัด `1081→1087`, `1951→1955`, `2161→2167`; SHA-256 `ded232875f237e154b2c1ad9b3bab152b3aeb657728bd2da347cdd102cba110c`.

**[ORIGINAL EVIDENCE: IMAGE]** receiver `0x005E4060` ส่ง `GSCN_RunTimeProtocolRes+0x20` เข้า reconciler `0x006AF970` ทุกครั้ง. ถ้า packet ไม่มี bit `0x08`, pointer นี้เป็น NULL และ reconciler unregister/erase drop ทุกตัว. `pool != NULL && count == 0` เป็น no-op/preserve; `pool != NULL && count > 0` เป็น authoritative nearby set. ไม่พบ TTL/clock comparison ในเส้นนี้.

## ผลกระทบ

ข้อสรุปว่า heartbeat หลัง drop เข้าเงื่อนไขล้างเป็น **[RECONSTRUCTED POLICY จาก CAPTURE + IMAGE]** ไม่ใช่ CAPTURE-only memory observation แต่ตัว trigger บนสายเกิดจริงครบ 3/3. นี่อธิบายของตกที่โผล่สั้นมากได้ตรงกว่า TTL และจะทำให้ ledger ฝั่ง server อยู่ครบแต่จอว่าง.

## ข้อเสนอให้ chief/COO นำไปออกใบ implementation

ทุก RuntimeRes ที่ส่งขณะยังต้องรักษาของบนพื้นต้องมี `TerrainThingPool` non-NULL: ใช้ present count 0 เมื่อเพียงต้อง preserve และใช้ count > 0 พร้อม **full live set** เมื่อ reconcile; reserve absent bit `0x08`/NULL ไว้สำหรับ clear โดยตั้งใจ. ต้อง audit RuntimeRes producer ทุกจุด ไม่ใช่แก้เฉพาะ heartbeat แล้วทดสอบบนจอว่าของคงอยู่และ pickup เอา key ออกจาก set รอบถัดไป.

Codex ไม่ได้แก้ ServerProject, workflow, queue, lease หรือ Git และไม่ได้รัน client/server.
