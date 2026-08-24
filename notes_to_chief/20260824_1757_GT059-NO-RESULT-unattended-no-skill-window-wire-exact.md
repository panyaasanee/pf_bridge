ถึง: chief + Panya

# GT-059 — NO-RESULT (unattended): wire byte-exact; รอบนี้ไม่พบ Skill window ทั้งก่อน/หลัง sweep และหลัง relog

- เวลา: `2026-08-24T17:31:28+07:00` ถึง `2026-08-24T17:55:08+07:00`
- ผู้เทส: OpenAI Codex LOCAL — **UNATTENDED ตามคำสั่ง Panya**
- ขอบเขต: GT-059 ใบเดียว; static preflight + เกมจริงสอง session ตามใบ; ไม่แตะ GT อื่น
- สถานะที่เสนอ: **NO-RESULT / รอ Panya** — ชั้น wire/DB ครบแบบ byte-exact แต่ผล client-observable เป็นการเห็นจากวิดีโอ/ภาพในรอบ unattended และ S1 ระหว่างสองเฟรมเก็บไม่ทัน จึง **ห้ามปิดเป็น P2/falsify จากจดหมายนี้เพียงฉบับเดียว**

## คำตอบสั้น

1. **รอบนี้ไม่พบหน้าต่าง `Skill_Main2`** จากทั้ง hotkey `K` และปุ่มที่ tooltip ยืนยันว่า `สกิล (K)` ที่ S0, S2, S3, S4, S5 และ S6.
2. relog variant ไม่เปลี่ยนภาพที่สังเกตได้: session 2 ไม่กด K ก่อน trigger, รับ sweep จบแล้วจึงกด K ครั้งแรก แต่ยังไม่พบหน้าต่างที่ S5; คลิกปุ่มโดยตรงที่ S6 ก็ยังไม่พบ.
3. client ไม่ค้าง: `C` เปิดหน้าต่าง `CHARACTER` ได้ชัดเจนในทั้งสอง session และออกด้วย X + ปุ่มซ้ายได้สะอาด = **NO-CRASH positive control**. มี Q tap ใน session 1 แต่ภาพไม่ต่างพอ จึงไม่ใช้ Q เป็นหลักฐาน.
4. raw wire มี sweep ครบ 3 triggers รวม 6 เฟรม: ทุก trigger เป็น 57 → 68 bytes ห่าง 3.000–3.001 s และ SHA256 ตรง pin ทั้งคู่ทุกครั้ง.
5. เนื่องจากเป็น unattended ผลด้านจอให้เขียนว่า **“ไม่พบในรอบนี้ · ยังไม่ได้วัดผลลบโดย Panya”** ไม่ใช่ “ไม่มี/ไม่เกิด”.

## ก่อนบูต / guards

- main HEAD ตอนจับ lock: `543382c463cc1f614d62fc2d33edbeaf297377fa`, clean.
- resolver เลือก green boot `01b8b9ea0b3d6055d4a6706767853ebe3e49434e`; boot tree `3acc336cb76f0adfef536d599aea521fb8f4433f` ตรง main tree byte-for-byte.
- ci verdict `success`; flag `--skill-attr-hypothesis-scenario`, scenario `skill_attr_hypothesis_attr_sweep`, mode `skill-attr-hypothesis`, label `COUNT1_KEY1`, frame sizes และ pins ผ่าน guard ทั้งหมด.
- trigger ใช้ `skillattr001` printable ASCII 12 ตัวเป๊ะ; เลือกตัวละครช่องแรกตาม identity guard.
- canonical ก่อนบูตทั้งสอง session ตรง `CANON_SHA.txt`: `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21`.

## ชั้น client-observable — provisional เท่านั้นเพราะ unattended

### Session 1 — baseline + สอง sweeps

เข้า Port Royal แล้วเห็น HP `100/100`, minimap, ชื่อ `Port Royal`, พิกัดประมาณ `X:-8,653 Y:-2,579` และแชต local server online.

| จุด | action / เวลาเทียบวิดีโอ | สิ่งที่เห็นในรอบนี้ | สถานะหลักฐาน |
|---|---|---|---|
| S0-K | K ก่อนยิงเฟรม, ~238 s | ไม่พบ Skill window | เก็บภาพแล้ว; unattended negative ยังไม่ปิดใบ |
| S0-button | คลิกปุ่ม Skill โดยตรง, ~259 s | ไม่พบ Skill window | เก็บภาพแล้ว |
| S1 | K ระหว่างเฟรม 3 s | **ไม่ได้เก็บ** — action จาก computer-use ลงหลัง `COUNT1_KEY1` แล้ว | A/B UNRESOLVED; ห้ามแต่งผล |
| S2 | K หลัง sweep แรก, ~311 s | ไม่พบ Skill window | เก็บภาพแล้ว |
| S3 | ปุ่ม Skill หลัง sweepแรก, ~322 s | tooltip `สกิล (K)` ชัด แต่ไม่พบ window | เก็บภาพแล้ว |
| S4 | K หลัง sweep ที่สอง, ~384 s | ไม่พบ Skill window | เก็บภาพแล้ว |
| control | C, ~408 s | หน้าต่าง `CHARACTER` เปิดชัด | positive NO-CRASH |

จังหวะ S1: trigger แรกออก `COUNT0` `17:38:58.802`, `COUNT1` `17:39:01.803`; K ที่ตั้งใจเก็บ S1 ลงหลังจากนั้นมาก จึงจัดเป็น S2 เท่านั้น. สาเหตุคือ round-trip ของ computer-use/action-refresh ยาวเกินหน้าต่าง 3 s ไม่ใช่ product result.

### Session 2 — trigger ก่อน K ครั้งแรก

- restart server และใช้ run-copy ใหม่ตามใบ; ก่อน trigger **ไม่กด K เลย**.
- Enter trigger เวลาใกล้ `17:48:23.238`; raw ส่ง `COUNT0` `17:48:23.798` และ `COUNT1` `17:48:26.799`.
- S5: K ครั้งแรกของ session ลงหลัง sweep จบเกิน 5 s (~232 s ของวิดีโอ); รอบนี้ไม่พบ Skill window.
- S6: คลิกไอคอนตรง ๆ (~246 s); tooltip `สกิล (K)` ชัด แต่รอบนี้ไม่พบ Skill window.
- control C (~256 s) เปิด `CHARACTER` ชัด; X + ยืนยันซ้ายปิด client สะอาด.
- คำตอบ provisional เรื่อง relog: **ภาพที่สังเกตในรอบนี้ไม่ต่างจาก session 1**; ยังไม่ใช่คำตัดสินผลลบ attended.

## ชั้น wire — แยกจากภาพเด็ดขาด

### timeline

| session / trigger | COUNT0_EMPTY (57 B) | COUNT1_KEY1 (68 B) | delta |
|---|---|---|---:|
| S1 / trigger 1 | `17:38:58.802` | `17:39:01.803` | 3.001 s |
| S1 / trigger 2 | `17:40:11.509` | `17:40:14.509` | 3.000 s |
| S2 / trigger 1 | `17:48:23.798` | `17:48:26.799` | 3.001 s |

ทุก occurrence มี frame bytes ตรงกันและตรง scenario pin:

| label | bytes | actual SHA256 | pin verdict |
|---|---:|---|---|
| `HYP_PF_035_SKILL_ATTR_COUNT0_EMPTY` | 57 | `62BDFD389A618E12E784A58C8E8D1411BA86E0536D136EE6EE63DEB22173718F` | PASS ×3 |
| `HYP_PF_035_SKILL_ATTR_COUNT1_KEY1` | 68 | `489331F80430F700638BA660B1D1292CCBC9BB7AB62160FD7A6E8D4AE0B1722E` | PASS ×3 |

โครงสายที่เห็นใน hexdump: carrier `0x309A`; attr block class id `0x1661`; body เริ่ม `0B 01`, identity qword `0x10010001`, COUNT0 เป็น `12 00 00`; COUNT1 เป็น `12 01 00` แล้ว record 11 bytes `12 01 00 / 12 00 00 / 14 00 00 00 00`.

**event retention caveat:** source branch ที่ dispatch sweep append `skill_attr_hypothesis_attr_sweep_sent` หนึ่งครั้งก่อนคืน actions แต่ server console build รอบนี้ **ไม่ได้ serialize ชื่อ event ภายในนี้ออกไฟล์**. ดังนั้นจดหมายไม่อ้างว่าเห็น literal event string; หลักฐาน actual ที่เก็บได้คือ `[G>]` action labels + raw `SENT`/FRAME hexdump อย่างละ 2/2 และ 1/1 triggers. Chief ควรถือเป็นช่องว่างด้าน event-text retention แม้ byte dispatch จะครบ.

### raw artifacts

| artifact | bytes | SHA256 |
|---|---:|---|
| `GameClient\capture_gt059_s1_20260824_173407\capture_v141\GAME_20260824_173623_524172_60173.txt` | 450,982 | `8B280F29C3E3F3ABAB5BC34E7DAC0CA83363296A86A1EFA09F804300E37919B3` |
| `...s1...\GAME_LIVE.txt` | 67,274 | `BE0BFF0FCAA83D53BC254B4BBF78FCED66F7D839C21339AFF0849543D4593AA3` |
| `...s1...\server_console_live.out.txt` | 93,864 | `93A6252E187EB1B7F53F64714884DCB6AC6F703935A85398B728F51EE81B3168` |
| `GameClient\capture_gt059_s2_20260824_174445\capture_v141\GAME_20260824_174650_851475_57773.txt` | 173,536 | `C6492237201603A96B2453AEE7A6290098E9556214E22A42A3E1478E81258075` |
| `...s2...\GAME_LIVE.txt` | 25,958 | `899D9740C8ABB5BA50978F8F8B03C5E221685327C904626FD218A0C77AEA4BF1` |
| `...s2...\server_console_live.out.txt` | 45,195 | `4B79112409D322DE74AFC4E49F1735E6AC7BC20492EEB02B259F8A3DA063D6D0` |

console err ทั้งสอง session = 0 B; stopped marker 1, ready marker 2, traceback 0 ต่อ session.

## DB / canonical / teardown

row-diff read-only ทุกตารางเทียบ backup สดก่อนบูต:

- Session 1: schema เท่ากัน; changed table count = 1; `sessions` 11 → 12, added 1, removed 0; session ใหม่ selected character `1`, lease `12`, ปิดแล้ว. run SHA `670CE534...FEC21` → `39CB69A522094688250E28D8E34DD9BBB644198A32FD0D29EB3552B8F89785D9`.
- Session 2: schema เท่ากัน; changed table count = 1; `sessions` 11 → 12, added 1, removed 0; session ใหม่ selected character `1`, lease `12`, ปิดแล้ว. run SHA `670CE534...FEC21` → `151A982F8792F6915D8D0249003691B0DEE5B87530C8F2D5F7020EE31FF05168`.
- ทั้งสี่ DB view: integrity `ok`, FK rows `0`; analyzer อ่านแบบ `mode=ro&immutable=1` และ SHA ก่อน/หลังการอ่านคงเดิม.
- canonical หลัง session 1, หลัง session 2 และ final ยังตรงเดิม: `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21`.
- final topology หลังแต่ละ teardown: listeners 10188/10189 = 0, GameClient = 0, ffmpeg = 0; server ปิดสะอาด.

backup/run-copy:

- `pf_bridge\backup\pirateforce_before_GT-059_20260824_173407.sqlite3`
- `Pirate Force ServerProject\state\run_gt059_s1_20260824_173407.sqlite3`
- `pf_bridge\backup\pirateforce_before_GT-059_20260824_174445.sqlite3`
- `Pirate Force ServerProject\state\run_gt059_s2_20260824_174445.sqlite3`

## ภาพ / วิดีโอและ SHA256

- `pf_bridge\evidence_video\1091_gt059_s1_FULLROUND_20260824_173410.mkv` — 497.900 s, 51,633,077 B, `CCEF4B5AD03E162E4E8CC26D792D32C47E92C6512BC92123184A32E441D8BE54`
- `pf_bridge\evidence_video\1093_gt059_s2_FULLROUND_20260824_174452.mkv` — 306.466 s, 24,957,564 B, `8865728C6D23F109DE6BA842FC9B7C82E2C36B5F635F2974279283D27AC234C8`

| mapping | evidence_screens file | SHA256 |
|---|---|---|
| S0-K | `FRAME_GT059_S1_POINTS_238s_20260824_175457.jpg` | `EA8D15D81848B647B0DE5F9B9D26F22221A8800038633B6FEE653FC7F3274EC1` |
| S0-button | `FRAME_GT059_S1_POINTS_259s_20260824_175457.jpg` | `386D4119F0EDA626C37FD915806C9306CF5D30244CBDF0C9EA69E3F4C77ECC21` |
| S2 | `FRAME_GT059_S1_POINTS_311s_20260824_175457.jpg` | `88501F7DC212C5605DF2FEF3EC1BE36B87FC01A1806D107A47A74C341AA5D42A` |
| S3 | `FRAME_GT059_S1_POINTS_322s_20260824_175457.jpg` | `4520C52BDCB59B603F701A88751030F3D68AB3356EF682826FA6C148896E8846` |
| S4 | `FRAME_GT059_S1_POINTS_384s_20260824_175457.jpg` | `8B950C5DA34C2306A4623E92BC13285358D468F23117B04C644C757BAC92F1A2` |
| S1 control C | `FRAME_GT059_S1_POINTS_408s_20260824_175457.jpg` | `5A98D3AAFEA088BC89346CE19E953BA01888CA3051462EEF76AAB9476F6CFC55` |
| S5 | `FRAME_GT059_S2_POINTS_232s_20260824_175503.jpg` | `E0809A61C8B7B212B429F55895944DCB605F38628A42F4EFAC5D0F3D494C3DAF` |
| S6 | `FRAME_GT059_S2_POINTS_246s_20260824_175503.jpg` | `30F5B2D8903CCB8F5327E51C525E9A1499F983AB50E7839C7673256844D12882` |
| S2 control C | `FRAME_GT059_S2_POINTS_256s_20260824_175503.jpg` | `F03A92E263585A8BFE8C75D47316DBD3B542708B7316BEAEBE90F76785126639` |

S1 ไม่มีไฟล์เพราะไม่ทันหน้าต่าง; **ห้ามนำ S2 มาตั้งชื่อเป็น S1**. วิดีโอเต็มทั้งสอง session เก็บช่วงดังกล่าวต่อเนื่องและ frame proof รวม 9/9 ผ่าน.

## อ่านคู่ RE-062

ผล static RE-062 บอกว่า inbound สามารถ decode/insert `CSkillAttr` ใน generic attribute map แต่ไม่ repair dedicated slot `[actor+0x3E8]` หาก slot เป็น null; ในทางกลับกัน normal `CMyActor` constructor ปกติสร้าง slot นี้ไว้ก่อน. ดังนั้นภาพ “ไม่พบ window” ในรอบนี้ **แยกไม่ได้** ระหว่าง (ก) runtime slot null แล้ว sender repair ไม่ได้ กับ (ข) slot non-null แต่มี base/UI gate อื่น. ไม่มี runtime crosswalk สำหรับตัดสินสองกรณีนี้ และ unattended round นี้ไม่เพิ่ม claim ดังกล่าว.

## Jobs / tooling notes

- tester jobs: `1087` preflight PASS; `1088` lock; `1089` resolver attempt ปฏิเสธอย่างปลอดภัยเพราะ local extra ancestor guard เข้มเกิน; `1090` resolver retry PASS; `1091/1092` session 1 boot/teardown PASS; `1093/1094` session 2 boot/teardown PASS; `1096` keyframe extraction PASS.
- `1095` keyframe extraction attempt แรก fail อย่างปลอดภัยก่อนเขียนภาพ เพราะ bridge process ไม่มี FFmpeg ใน PATH; retry `1096` ใส่ path ที่ได้จาก boot info แล้วผ่าน 9/9. ไม่ใช่ product failure.
- `1097` release attempt แรก fail อย่างปลอดภัยเพราะ `Write-Flag` ไม่รับ empty string จากบรรทัดว่างใน history; lock ยัง HELD ไม่เสียข้อมูล. retry `1098` normalize บรรทัดว่างเป็น space ก่อนเขียน.
- computer-use `list_apps` timeout หนึ่งครั้งตอนเริ่ม session 1 แล้ว retry สำเร็จ; ไม่มี input ซ้ำจาก timeout.
- server console เคย overlay หน้า character select ชั่วครู่ แต่ action ถัดไป target GameClient ทำให้เกมกลับ foreground; จุดวัดในแมพทั้งหมดไม่มี overlay.

## Nonclaims

- ไม่ตีความความหมายของ `opaque_u16`, `opaque_u32` หรือ `key=1`; ทั้งหมดเป็น probe ตามใจเรา.
- ไม่ claim ว่า original server เคยส่ง `CSkillAttr` รูปนี้, version นี้, record นี้, spacing นี้ หรือจังหวะนี้; ทั้งหมดเป็นดีไซน์ server เรา.
- ไม่พิสูจน์ว่าสกิลใช้งานได้; วัดเฉพาะ window gate.
- ไม่ใช้ wire ว่าพิสูจน์หน้าต่างเปิด/ไม่เปิด และไม่ใช้ภาพว่าพิสูจน์เฟรม dispatch.
- ไม่ claim ว่า `[actor+0x3E8]` เป็น null หรือ non-null ใน runtime รอบนี้.
- ไม่ claim ว่า `CSkillAttr` เป็นเงื่อนไขเดียว แม้ภายหลังจะได้ผลบวก.
- ไม่ claim ผลลบ P2 จากรอบ unattended; ข้อความที่อนุญาตคือ **ไม่พบในรอบนี้ · ยังไม่ได้วัดผลลบโดย Panya**.

## สิ่งที่ขอให้ chief ทำ

1. รับข้อมูล wire/DB + artifacts เข้าคิวได้ แต่คง GT-059 เป็น `PENDING/NO-RESULT` จน Panya ยืนยันภาพ negative หรือรัน attended.
2. อย่าใช้ S2 แทน S1; A/B COUNT0-vs-COUNT1 ยัง unresolved.
3. ตัดสินว่าจะรับ raw `[G>]` labels เป็นหลักฐานแทน literal internal event หรือเปิดงานให้ exporter พิมพ์ `skill_attr_hypothesis_attr_sweep_sent` ในรอบหน้า; ผู้เทสไม่เปิดใบเอง.
