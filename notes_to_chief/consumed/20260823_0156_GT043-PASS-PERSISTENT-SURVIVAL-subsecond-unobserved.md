ถึง: chief + Panya

# GT-043 POP-SURVIVAL-001 — PASS สำหรับการอยู่รอดแบบไม่หายค้าง; ช่วง 0–3.524 วินาทีหลังยิงยังไม่ถูกสังเกต

เวลา attended: 2026-08-23 01:33–01:50 +07:00  
ผู้เทส: Codex ATTENDED (tester LOCAL)  
host lane: GT-032-family / HYP-PF-027 NPC-hostile faction-pairing  
HEAD: `cf817305327783c4187224c79df3150ced426ae3` (clean; ผู้เทสไม่แตะ git)

## คำตอบภาษาคน

หลังส่งเฟรม count-1 bit `0x02` หนึ่งเฟรม **ไม่พบ Navy Transfer หรือวัตถุฉากที่ติดตามหายแบบค้าง**: ในภาพมุมเดิมที่จับได้จริงตั้งแต่ `+3.524s` ถึง `+9.978s` ยังเห็น NPC ตัวเดิม พร้อมตัวเรือ/โคม/หัวน็อตเรือ/เสาผูกเรือ/โซ่/ช่องประตูในตำแหน่งเดิม และภาพ P2 หลังแพนกล้องยังพบ NPC เป้าหมายกับวัตถุฉากเหล่านี้อยู่

🔴 **ขอบเขตสำคัญ:** เครื่องมือจับภาพรอบนี้ให้ภาพแรกหลัง trigger ช้าถึง `+3.524s` แม้ร้องขอที่ 0/80/160/300/600/1000 ms และไม่มีวิดีโอต่อเนื่องที่ใช้ได้ ดังนั้น **ไม่ claim ว่าไม่มีการหาย/ดาเมจ/ข้อความหรือเอฟเฟกต์ชั่วคราวในช่วง 0–3.524s แล้วกลับมา**. ผลนี้ปิดได้เฉพาะ “ไม่มีการกวาดประชากรแบบหายค้างที่ยังเห็นหลัง +3.524s” ไม่ใช่ “ไม่มี transient ต่ำกว่า 1 วินาที”.

## Wire/DB — เฟรมออกจริง

- ผู้เทสเปิดแชตด้วย `Return`, ตรวจข้อความที่เห็นเป็น `PFCHATPROBE1` (ASCII 12 ตัวเป๊ะ), แล้วกด `Return` ส่งหนึ่งครั้ง
- raw GAME: `2026-08-23T01:46:09.596 SENT label=HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN frame_bytes=190 delay=0.00 late_ms=0.4`
- console พบ label `HYP_PF_027_NPC_HOSTILE_HOSTILE_SPAWN` **1 ครั้ง**, ขนาด **190 bytes**
- `compose_refused=0`, `already_sent=0`, `refusal=0`, `ErrorData=28317=0`, `Traceback=0`
- scenario: `Pirate Force ServerProject/scenarios/npc_hostile_hypothesis_faction_pairing.json` SHA256 `EADFE03C89423CBBB9907768CBDFFABDCD994C6B5617EAEE7422E410D5C6C1E6`
- run DB: `Pirate Force ServerProject/state/pirateforce_gt043_20260823_013319.sqlite3`
- canonical ก่อน/หลังตรง `CANON_SHA.txt`: `23FD885AC4CBBFAC5E06C9B11506F6EA9F985DA82F4522383DFCC14A91C1816A`
- teardown job `1015`: exit 0; stopped marker 1; stderr 0 B; open sessions 0; integrity `ok`; FK rows 0; listeners 0; GameClient 0; inbox 0

raw files:

- `GameClient/capture_gt043_20260823_013319/capture_v141/GAME_LIVE.txt` SHA256 `7E7C6476CCE76E976BF29B3C287E69DFD91D88814665D437778D4F1905CDFE2B`
- `GameClient/capture_gt043_20260823_013319/capture_v141/GAME_EVENTS_LIVE.txt` SHA256 `A148634A760EFA9C096EEEE7149073A9A5CED80B246C23F9673970F1689A4766`
- `GameClient/capture_gt043_20260823_013319/capture_v141/GAME_20260823_013426_226720_49673.txt` SHA256 `5D82832AA691961C5BA354811F02F30D8ACACDB4C246BEFF8CAF3E34AA0A790F`
- `GameClient/capture_gt043_20260823_013319/server_console_live.out.txt` SHA256 `BED31B8BC4A9AFBC902DB94A9784590200D4D7C48174A2B42B523B2E35F69B85`

## Client-observable

### ก่อนยิง

- `GT043_R2_P0_preselect_20260823_0139.png` — ภาพรวมผู้เล่น + Navy Transfer +วัตถุฉากหลายชิ้น; SHA256 `2A1A9BFCB114194770114E4DE701CE8C6A671E5F12540734DBCDF288A760E715`
- `GT043_R2_P0a_NavyTransfer_before_20260823_0140.png` — แผงเควสต์อ่านชื่อ Navy Transfer ได้และมีเส้นเลือกสีเหลือง; SHA256 `6FF39FDC589555E694852A9618AD8F7336FDC0ABA590F5AC2C22E610DED79749`
- `GT043_R2_P0_overview_same_angle_20260823_0141.png` / `GT043_R2_P0r_minimap_20260823_0141.png` — มุม baseline เดียวกันพร้อม minimap; SHA256 ทั้งคู่ `DDF333C16BE2D8E4B21C43A8F2BD8C8F389502E7C9252C14E658C1E514FB2160`

### หลังยิง — มุมเดิม

เฟรมที่ร้องขอเร็วถูกจับจริงช้ากว่าเป้าหมาย แต่ทั้งหกภาพยังเห็น NPC และ landmark ที่ติดตาม:

- requested 0 ms → actual `+3524ms`, SHA256 `3BC38111666DDA74DD7CFC94444D0B575FC7DE5D4A2EA746DB9743913ECEA104`
- requested 80 ms → actual `+7318ms`, SHA256 `060CB133590F16348F6565275B221728314BE64185BC8822A49B5389F82BFC72`
- requested 160 ms → actual `+8630ms`, SHA256 `611566C63FDC12A26A94EB533296C8C5E3916A6B0BFABF21D59E32D73582A4CB`
- requested 300 ms → actual `+9006ms`, SHA256 `2A2F8BC3FF12F437145C010112F3B969DD483A19D5CD26B403F05945B8D5F89C`
- requested 600 ms → actual `+9335ms`, SHA256 `8D50315BC1320740ABDAF3F9C0AF0D7229178535351E84F61BF73819FD1500E0`
- requested 1000 ms → actual `+9978ms`, SHA256 `D4E03CE86A91C6D8C746E547B9A1161A7A172B1B90A31F5939948AAA626A8DD1`

ไฟล์อยู่ใต้ `pf_bridge/evidence_screens/GT043_R2_P1_rapid_*.png`; ทุกภาพรวม minimap จึงใช้เทียบ P1/P1r กับ P0/P0r ได้ในเฟรมเดียวกัน

### P-tab และ P2

- `GT043_R2_Ptab_before_20260823_0148.png`: หลังยิง ก่อน Tab — Navy Transfer ยังอยู่ แต่ไม่มีเส้นแดง/แผง target; SHA256 `F213B2A5C152389CE1B7538B055CCCDB9EEF7E4597D4F5A128C689D5653ACE0B`
- กด `Tab` หนึ่งครั้ง
- `GT043_R2_Ptab_after_20260823_0149.png`: NPC ตัวเดิมมีเส้นแดง/ลูกศรแดงและแผง target HP `100/100`, Lv.1; SHA256 `DF0EF4261A59D8C6C3B0D60F938854FB9F059261E6133BF8FEF7F6CF3D39ABCA`
- ข้อนี้ตอบโน้ต GT-032 ได้ในรอบนี้: **hostility frame อย่างเดียวไม่ทำให้เส้นแดงขึ้น; เส้นแดงปรากฏหลัง Tab-select** (ภาพก่อน/หลัง Tab แยกกัน)
- `E` แบบกดสั้นหนึ่งครั้งไม่ให้การเปลี่ยนมุมที่วัดได้จากภาพนิ่ง จึงไม่ claim ว่า E ไม่ทำงาน
- `GT043_R2_P2_rightclick_pan_20260823_0151.png`: แพนกล้องสำเร็จไปยังมุมกว้าง; NPC เป้าหมาย/แถบ HP และวัตถุฉากยังอยู่; SHA256 `1A4E923F1795D5CAC5CD1E239D2CED470E44AADB15287ED11DC0C5A3E90EE56D`

หลักฐานเสริมตามคำบอกของ Panya เรื่องล้อเมาส์: `GT043_aux_mousewheel_up_20260823_0152.png` แสดงมุมซูมกว้างขึ้นหลัง wheel-up (SHA256 `B84B76785ED115A121980F9DC0CD577C33429ECCC5AA1745A8D426D6A00B9465`); ภาพหลัง wheel-down ถูกเก็บที่ `GT043_aux_mousewheel_down_20260823_0153.png` (SHA256 `376D100DBE3DF53144B4127CA3F64E930781576AF48FA33F33A6B39C776BA7BE`) แต่ความต่างจากเฟรมก่อนหน้าไม่ชัดพอให้ตัดสินทิศทาง/ระยะในใบนี้ — ให้ GT-038 เป็นใบตัดสิน control โดยตรง

## เหตุการณ์รอบแรกที่ยกเลิก

boot `1012` ถูกยกเลิกก่อนส่ง trigger เพราะเครื่องมือจับภาพทำให้หน้าต่างเกมเลื่อน; ไม่มี host label ออก. teardown `1013` exit 0, listener/GameClient 0 และ canonical ไม่เปลี่ยน. ผลข้างต้นมาจาก fresh rerun `1014` เท่านั้น

## Nonclaims

- ไม่ claim ว่าไม่มี transient/ตัวเลขดาเมจ/เอฟเฟกต์ต่ำกว่า 3.524 วินาที; ภาพนิ่งที่พลาดช่วงนั้นพิสูจน์การไม่เกิดไม่ได้
- ไม่ claim ว่าทำไมประชากรไม่หายแบบค้าง และไม่เชื่อมภาพจอกับ `[mgr+0x24]`/`0x441C40`; งานนั้นเป็น GT-042
- ไม่ claim combat, aggro, persistence, HP write หรือของลูทบนพื้น
- เฟรม/faction ของ host lane เป็นดีไซน์การทดสอบ ไม่ใช่การกู้ดีไซน์เซิร์ฟเวอร์ต้นฉบับ

## ข้อเสนอให้ chief ลง ledger

`GT-043 = PASS-PERSISTENT-SURVIVAL / subsecond-unobserved`: count-1 bit-0x02 frame ออกจริง 1×190 B; ไม่พบ NPC/วัตถุฉากที่ติดตามหายแบบค้างในช่วงที่จับได้ +3.524..+9.978s และหลังแพน; ช่วง 0..3.524s ห้ามสรุป. GT-032 side-note: เส้นแดงเกิดหลัง Tab-select ไม่ใช่จาก hostility frame เพียงอย่างเดียว.
