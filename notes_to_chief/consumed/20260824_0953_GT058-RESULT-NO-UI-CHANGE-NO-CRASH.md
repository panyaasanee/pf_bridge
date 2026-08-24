ถึง: chief + Panya

# GT-058 RESULT — 5-frame sweep accepted; NO-CRASH / NO-OBSERVABLE-UI-CHANGE

เวลา: 2026-08-24 09:43–09:52 (+07:00) · ผู้เทส: Codex UNATTENDED (LOCAL)

## คำตัดสินที่เสนอ

**[DONE — WIRE PASS / CLIENT BOUNDED NEGATIVE / NO-CRASH]** client รับ sweep `CLearnSkillResultVital (0x673C)` ครบ 5 เฟรมโดยไม่หลุดหรือค้าง แต่ไม่เห็นอะไรบนจอเปลี่ยนทั้ง 5 สเต็ป: ไม่มี skill window/list เปลี่ยน, ไม่มีแถวแชต/ข้อความระบบใหม่ และ HP/HUD/แมพยังคงเดิม

ขอบเขตที่พิสูจน์ได้: `0x673C` เดี่ยวๆ ในรูปที่เลนนี้ประกอบ ไม่พอขยับ UI ที่สังเกตได้; version byte `0` ไม่ทำให้ client reject/crash ใน sweep นี้

## ก่อนบูต

- resolver คืน `fa1e804a336323c2273dd3c3716db5204495f0d7`; tree ตรง main HEAD `94f0ce33194aabdfa9d39e78a085d4b86babd294`
- `9691bcc` เป็น ancestor; verdict `success` SHA ตรง; flag/scenario/`COUNT3_TRAIL1` guard ครบ 4 ข้อ
- trigger อ่านจาก source fixture: `PFCHATPROBE1` = printable ASCII 12 ตัวพอดี; พิมพ์ในช่องแชตที่ focus แล้วกด Enter ครั้งเดียว

## ชั้น wire

raw: `GameClient\capture_gt058_20260824_094625\capture_v141\GAME_20260824_094807_404629_62314.txt`, SHA256 `99417C686A5EC3CD148BEBB9931BF3271CF7778CF49E21F718CBDF1AF7387592`

| step | bytes | frame SHA256 | pin |
|---|---:|---|---|
| `COUNT0_TRAIL0` | 37 | `B92F0DBE0DD2B6FB01DBFB5419C2BCCB97A9401116BFDB28AE6B926362268F14` | PASS |
| `COUNT1_TRAIL0` | 50 | `0A6A7D93EB7CECF09BD657252AE10FEBB83271AA853208B85D9BC734916F7A7A` | PASS |
| `COUNT1_TRAIL1` | 50 | `1A213A98F458DE2A12BF664533C0D918AAB7B890EDA7C096D6DF150FC9DF3D77` | PASS |
| `COUNT3_TRAIL0` | 77 | `0EE12033D6A917B75B578AD2E4BF1935D597FB5D8CE5D47224EC63BB81CE718A` | PASS |
| `COUNT3_TRAIL1` | 77 | `C445872E4EA632567B85D06001CE951532F42B0FA058DAC9DA40CF5E60612D87` | PASS |

action labels อย่างละ 1 ครั้ง เรียงตาม manifest, ระยะ 3 s; `GAME_LIVE.txt` SHA256 `A2B246AB3816497A91A17F14956F26E7679B4BD934FE1FDF61AC1D30F57C30A2`

## ชั้น client-observable

- S0 ก่อยิง: Port Royal, HP 100/100, แชท online ปกติ
- S1 `COUNT0_TRAIL0`: ไม่เปลี่ยน
- S2 `COUNT1_TRAIL0`: ไม่เปลี่ยน
- S3 `COUNT1_TRAIL1`: ไม่เปลี่ยน
- S4 `COUNT3_TRAIL0`: ไม่เปลี่ยน
- S5 `COUNT3_TRAIL1`: ไม่เปลี่ยน
- หลัง sweep ทั้งห้า client ยังรับ input `Q`, เปิด exit dialog ด้วย X และปิดด้วยปุ่มซ้ายได้ = **NO-CRASH / responsive**

ภาพ `pf_bridge\evidence_screens\GT058_20260824_0951_S0.png` … `S5.png` SHA256 ตามลำดับ:

`FEB7A44CD9F374D9CF2F2CA0CB0E884262C7A05E81856A73D67451FD7358F5B3`
`F15D2E8A25A35218B4AD9C598269D3D5602598A334AF54F8C6207901B5CE8E11`
`24F430B4D65FBF69206CBF5E2599B7F1B43B547653BA69D2C327B97EFA099F77`
`89BE008B87107690896EAA81ABF7422177696617C2808605484135B518A326D5`
`9EE27598D90B8F311BF36D584F305F95F58E320A4993A3F11FB272F769D20A0C`
`F10BBE349A9584DC534133B4F6F5CBE38BF26EB5E468945EDBBB860ED4E89CE7`

วิดีโอเต็มรอบ `1075_gt058_FULLROUND_20260824_094627.mkv`, SHA256 `EE4444E0CE9A5472CAC94211452739A0771DC1305CF968F66A161C002B5AB7B7`; frame proof 3/3 OK

## DB / teardown

- run-copy selected sessions `10 → 11`, max lease `11 → 12`, open 0, integrity `ok`, FK rows 0
- canonical SHA คงเดิม `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21`
- run-copy SHA `670CE5... → E78363807235381A51AB7B58FF56E0D4F5C60B7E615BEB58514603A931E6C3D7`; row-by-row diff ทุก table เจอต่างเฉพาะ `sessions` เพิ่ม 1 แถว (selected character 1, lease 12) — ไม่มี scenario/gameplay table อื่นเปลี่ยน
- stopped marker 1, ready 2, traceback 0, stderr 0 B, listeners/client/ffmpeg หลังจบ = 0

### ข้อขัดกันใน pass criteria

ใบสั่งกำหนดทั้ง `sessions selected +1` และ `run_gt058.sqlite3 ไบต์ตรงก่อน-หลัง`; สองข้อนี้เกิดพร้อมกันไม่ได้เมื่อ session ถูก persist ลง run-copy. ผลวัดที่ใช้ได้คือ **scenario ไม่เขียนอะไรนอกจาก session lifecycle ที่ใบเองก็คาดให้ +1**; เสนอ chief แก้ byte-identical เป็น row-diff-except-one-expected-session

## Nonclaims

- ไม่ตีความ field `(u32/u16/u32)` หรือ trailing byte
- ไม่ claim ว่า original server เคยใช้เฟรม/version แบบนี้
- ไม่ map count/trailing กับความหมายเชิงเกม
- ไม่พิสูจน์ทิศทาง client ส่งกลับ; รอบนี้ inbound-only observe
