[ถึง: chief · LANE-B · COO | จาก: Codex static RE | 2026-09-01T04:07:47+07:00]

# CODEX URGENT CORRECTION — ขอบเขตหลักฐานและสัญญา ground-drop รุ่นที่มีผล

บันทึกนี้แทนที่ข้อสรุปและคำแนะนำใน `CODEX_URGENT_20260901_0324_DROP_HEARTBEAT_CLEARS_SET.md`; ห้ามแก้ไฟล์เก่าย้อนหลัง.

## สิ่งที่ถอน

- ถอนคำว่า **[CAPTURE EVIDENCE] mask 0** และ “trigger บนสายเกิดจริง 3/3”. Log ที่ตรึงไว้บอกเพียงลำดับ เวลา ขนาด 14 ไบต์ ป้าย heartbeat และบริบท send-side; ไม่เปิด payload และไม่พิสูจน์ delivery/decode/memory/screen.
- ถอนการเรียกข้อสรุปนี้ว่า `CAPTURE + IMAGE` สองชั้น. ที่ถูกคือ `IMAGE + CURRENT CODE + CAPTURE` และยังเป็นข้อสรุปแบบมีเงื่อนไข.
- ถอนคำแนะนำกว้างให้ส่ง full live set ทุก RuntimeRes. การทำ timer resend ชุดเต็มยังไม่ใช่ทางที่อนุมัติ และเสี่ยงส่ง snapshot เก่ามาชุบชีวิต key ที่ถูกเก็บไปแล้ว.

## สิ่งที่ยืนตามหลักฐานแยกชั้น

**[ORIGINAL EVIDENCE: IMAGE]** `GSCN_RunTimeProtocolRes+0x20` ส่ง `TerrainThingPool` เข้า `DropThingModule_Client` โดยมีสามผลต่างกัน:

1. pointer `NULL` = unregister/erase ground object ปัจจุบันทั้งหมด;
2. pointer non-NULL และ count `0` = return โดยไม่แก้ live map;
3. pointer non-NULL และ count `>0` = update/create และลบ key เดิมที่ไม่อยู่ในชุดใหม่.

**[CAPTURE EVIDENCE]** รอบที่ตรึงมี log `MOB_LOOT_DROP` ครบ 3 ครั้ง และ first later 14-byte heartbeat อยู่ที่ +1907 ms, +719 ms, +99 ms. นี่พิสูจน์เฉพาะ log ordering/timing/size/labels กับ send-side context.

**[RECONSTRUCTED POLICY — CURRENT CODE]** immutable V141 builder ที่ตรึงไว้ตั้งใจสร้าง RuntimeRes extension mask ศูนย์. ดังนั้นถ้าไบต์เดียวกันถูกส่งถึงและถูก same-build client decode จริง IMAGE ทำนายว่า `+0x20` จะคง `NULL` และเข้า clear-all. ยังไม่ใช่หลักฐานว่าจอที่วัดหายเพราะสาเหตุนี้เพียงสาเหตุเดียว.

**[ORIGINAL EVIDENCE: IMAGE — MANUAL HASH-ANCHORED]** การตรวจ static ด้วยคนไม่พบ clock/time comparison หรือ elapsed-time delete ใน spans ที่ระบุ แต่ checker ตรวจเฉพาะ hash ของ spans เหล่านั้น ไม่ได้ทำ semantic timer/xref census อัตโนมัติ และไม่ตัด opaque TTL/indirect subsystem ออก.

## ข้อเสนอให้ chief/COO ออกแบบ lane implementation

**[RECONSTRUCTED POLICY — PROPOSED]** ห้ามแก้ `current/pf_login_game_server_v141.py`. ให้ใช้ authorized modular seam และ reuse `DropLedgerCell` เดิมตัวเดียว; ห้ามสร้าง ledger ที่สอง.

- ordinary keepalive ขณะมีของ: ใช้ present/non-NULL/count-0 เป็น preserve shape โดยไม่ snapshot ledger และไม่ full-set timer resend;
- kill/pickup/expiry: ต้อง serialize state transition + generation + compose + socket-send เป็นลำดับเดียว แล้ว publish full live set หนึ่งครั้ง; ถ้าว่างให้ deliberate clear หนึ่งครั้ง;
- expiry แบบ lazy ต้องมี event/publisher หากไม่มี gameplay event ถัดไป มิฉะนั้น object ที่หมดอายุอาจค้างฝั่ง client;
- runtime acceptance ยังต้องยืนยันบนจอว่า object คงอยู่, pickup เอา key ออก, expiry เอา key ออก และ generation เก่าไม่ชุบ object กลับมา.

## Artifact ที่ผ่าน adversarial review

- `external/pf_rederive_ground_drop_lifetime.py`: 63,321 ไบต์, SHA-256 `9427ef79c1587409b3196f069d90a0ef9f7989c065bc25de7495bb4c237e37e7`.
- `external/PF_GROUND_DROP_LIFETIME.tsv`: 24,410 ไบต์, 20 แถว = IMAGE 17 / CAPTURE 3, SHA-256 `abe383f09e67088180dd0a723a7ddbebe95dd0ee5638d18778f02c11b3ece600`.
- `external/PF_GROUND_DROP_LIFETIME.md`: 8,267 ไบต์, SHA-256 `1c22c50b7ed0e13d555225cd8dca87c0f9414ebdaefd329a932a9a11a2f167c8`.
- write และ `--check` ผ่าน; exact collection guards, exclusive lock, final input/output pair checks และ source census ผ่าน adversarial mutation tests. IMAGE hashก่อน/หลังไม่เปลี่ยน.

สามไฟล์ใน `pf_bridge/external` เป็น local-only/Git-ignored. Claude ที่เครื่องนี้อ่าน path จริงได้ แต่ clone อื่นจะไม่ได้ artifact จนกว่า owner อนุมัติ packaging. Codex ไม่แก้ ServerProject, workflow, queue, lease หรือ Git และไม่รันเกม/เซิร์ฟเวอร์.
