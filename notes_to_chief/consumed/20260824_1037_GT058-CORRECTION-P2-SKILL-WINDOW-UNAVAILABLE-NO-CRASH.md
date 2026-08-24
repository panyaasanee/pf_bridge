ถึง chief — ผลแก้ไข GT-058 หลัง Panya ทักว่ารอบก่อนยังไม่ได้เปิดหน้าต่างสกิล (K)

# GT-058 correction — P2 bounded negative; skill window unavailable before/after sweep; NO-CRASH

- เวลา: 2026-08-24T10:11:07+07:00 ถึง 2026-08-24T10:33:46+07:00
- รอบนี้แทนที่ **เฉพาะข้อสรุป client-observable ที่เกี่ยวกับหน้าต่างสกิล** ในจดหมาย `20260824_0953_GT058-RESULT-NO-UI-CHANGE-NO-CRASH.md`; ห้ามใช้จดหมายเดิมอ้างว่าได้เฝ้าหน้าต่างสกิล
- คำตอบต่อข้อทักของ Panya: รอบเดิมมี gap จริงเพราะไม่ได้เปิด K แต่เมื่อแก้รอบนี้แล้วพบว่า **ไม่ใช่เพียงลืมเปิด** — ไอคอนมี tooltip `สกิล (K)` แต่ทั้ง hotkey K และคลิกไอคอนโดยตรงไม่เปิดหน้าต่าง ทั้งก่อนยิงและหลัง sweep
- verdict: **P2 bounded negative + NO-CRASH** — `0x673C` เดี่ยว ๆ ทั้งห้าเฟรมไม่ทำให้เกิด UI/chat/system-message ที่มองเห็น และไม่ทำให้หน้าต่างสกิลเปิดขึ้น; แต่ **NO-RESULT ต่อการเปรียบเทียบ content ภายใน skill window** เพราะ baseline เปิดหน้าต่างนั้นไม่ได้

## Environment / green boot

- resolver receipt: `pf_bridge/outbox/1082_gt058_resolver.txt`
- `origin/main=94f0ce33194aabdfa9d39e78a085d4b86babd294`
- `BOOT_COMMIT=fa1e804a336323c2273dd3c3716db5204495f0d7`
- green tree = main tree = `4412cfd645e7de601dee7c4e190244394e222a81`
- guards ครบ: verdict success + sha exact; flag present; scenario present; `COUNT3_TRAIL1` present; `9691bcc` เป็น ancestor
- boot stamp `20260824_101412`; trigger ที่อ่านจาก source/predicate และใช้จริง `PFCHATPROBE1` (printable ASCII 12 ตัว)
- scenario manifest: `pf_bridge/boot_trees/gt058_1083_20260824_101412/scenarios/learn_skill_result_hypothesis_learn_sweep.json`

## Corrected client-observable procedure

1. เข้า Port Royal เห็น HP 100/100, minimap, map name และ `[ระบบ] : Pirate Force local server online`.
2. คลิกโลกเพื่อคืน focus แล้วลอง `K`/`k`; หน้าต่างสกิลไม่เปิด.
3. ไล่ไอคอนจน tooltip ระบุชัดว่า `สกิล (K)` แล้วคลิกไอคอนนั้นโดยตรงหลายครั้ง; หน้าต่างสกิลไม่เปิด. หน้าต่างอื่นที่เปิดจากการไล่ไอคอนถูกปิดก่อนยิง.
4. คลิกช่องแชต, พิมพ์ `PFCHATPROBE1`, เห็นครบ 12 ตัวใน S0 แล้วกด Enter **ครั้งเดียว**. ช่อง input เคลียร์ทันที.
5. เฝ้าวิดีโอต่อเนื่องและเก็บ S1..S5 หลังเฟรมแต่ละสเต็ป.
6. หลัง sweep ลอง K และคลิกไอคอน `สกิล (K)` อีกครั้ง; ยังไม่เปิด. ภาพ `...SKILL_BUTTON_TOOLTIP_NO_WINDOW_936p000s.jpg` แสดง tooltip ชัดและไม่มี skill window.
7. client ยังมีชีวิต/วาด idle animation/รับ click focus และเปิด exit-confirm dialog ได้. ลอง Q/E แล้วแต่ไม่เห็น camera rotation ที่แยกจาก idle ได้ชัด จึงไม่ใช้ Q/E เป็นหลักฐานเกินจริง; NO-CRASH อิง process/window ที่ยังอยู่และ interaction/exit dialog ที่ตอบสนอง.

### Per-step observable result

| Step | Frame | สิ่งที่เห็น |
|---|---|---|
| S0 | baseline ก่อน Enter | trigger อยู่ใน chat input; ไม่มี skill window |
| S1 | COUNT0_TRAIL0 | input เคลียร์; ไม่มี skill window/list, แชตหรือข้อความระบบใหม่, HUD/map ไม่เปลี่ยน |
| S2 | COUNT1_TRAIL0 | เหมือน S1; ไม่เห็นผลใหม่ |
| S3 | COUNT1_TRAIL1 | เหมือน S1; ไม่เห็นผลใหม่ |
| S4 | COUNT3_TRAIL0 | เหมือน S1; ไม่เห็นผลใหม่ |
| S5 | COUNT3_TRAIL1 | เหมือน S1; ไม่เห็นผลใหม่ |

การขยับท่า idle เล็กน้อยระหว่างภาพไม่ถูกนับเป็นผลของเฟรม เพราะไม่มีหลักฐานผูก causal กับสเต็ปใด.

## Wire evidence — ครบห้าเฟรม เรียงถูก อย่างละหนึ่งครั้ง

- trigger ถูกจับใน `GAME_EVENTS_LIVE.txt` เวลา `2026-08-24T10:27:37.605+07:00` เป็น frame 416, `UNKNOWN_0xAC52`, payload เป็น UTF-16LE `PFCHATPROBE1`.
- raw GAME log บรรทัด 4716, 4725, 4737, 4748, 4763 มี `SENT HYP_PF_033_LEARN_SKILL_RESULT_*` ตามลำดับด้านล่างอย่างละ 1 ครั้ง และ hexdump เต็มอยู่ต่อเนื่องในไฟล์เดิม.

| ลำดับ | label | bytes | manifest frame sha256 |
|---:|---|---:|---|
| 1 | `COUNT0_TRAIL0` | 37 | `B92F0DBE0DD2B6FB01DBFB5419C2BCCB97A9401116BFDB28AE6B926362268F14` |
| 2 | `COUNT1_TRAIL0` | 50 | `0A6A7D93EB7CECF09BD657252AE10FEBB83271AA853208B85D9BC734916F7A7A` |
| 3 | `COUNT1_TRAIL1` | 50 | `1A213A98F458DE2A12BF664533C0D918AAB7B890EDA7C096D6DF150FC9DF3D77` |
| 4 | `COUNT3_TRAIL0` | 77 | `0EE12033D6A917B75B578AD2E4BF1935D597FB5D8CE5D47224EC63BB81CE718A` |
| 5 | `COUNT3_TRAIL1` | 77 | `C445872E4EA632567B85D06001CE951532F42B0FA058DAC9DA40CF5E60612D87` |

โครงทุกเฟรมตรงพิน: msg tag `0x673C`, `count u16` tag `0x12`, record `(u32 0x14 / u16 0x12 / u32 0x14)`, trailing `u8` tag `0x0B`.

## DB / teardown

- canonical ก่อน/หลัง: `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21` ตรง `CANON_SHA.txt` — ไม่เปลี่ยน
- backup/run-copy ก่อน: `670CE5349A4A694B2C85D27EFE69C83D8CA1FE4DBCD8BD1CE0EEC343681FEC21`
- run-copy หลัง: `27EB4C35548699503521A76F06057C43D1AD38638545A506893A881D49D749F7`
- `PRAGMA integrity_check=ok`, FK rows 0; selected sessions 10 -> 11, max lease 11 -> 12, open sessions 0.
- diff เชิงตารางแบบ read-only พบเปลี่ยน **เฉพาะ `sessions`**: เพิ่ม row `(b4fc140930cc44b085bd0821fca76953, account=1, selected_character=1, lease=12, opened=03:18:14.571157Z, closed=03:32:24.900785Z)`; ตารางอื่น row digest ตรงกัน.
- ดังนั้น strict criterion ที่ว่า run-copy ต้อง byte-identical ก่อน/หลัง **ไม่ผ่านตามตัวอักษร** เพราะ session bookkeeping แม้ scenario เองไม่เขียน gameplay state. ใบเดียวกันกำหนด `sessions +1` ไว้ด้วย; chief ควรตัดสินว่าจะยกเว้น `sessions` หรือแก้ criterion ในใบถัดไป.
- teardown: GameClient 0 process, ports 10188/10189 = 0, server/console stopped, traceback markers 0, canonical guard OK.

## Evidence + sha256

- full video: `pf_bridge/evidence_video/1083_gt058_FULLROUND_20260824_101414.mkv`
  - duration `1165.666s`; sha256 `75C81CFFAD714F1602B71F03CD27A9A561907B7F2DF0810A0B95C86E7B1C62A2`
- S0: `pf_bridge/evidence_screens/GT058_20260824_101412_S0_baseline_800p000s.jpg`
  - `5C7F86889114DB6685AA4C56A872279DF5443CCDE93A44C950A93F69C7442660`
- S1: `.../GT058_20260824_101412_S1_COUNT0_TRAIL0_804p000s.jpg`
  - `3AA20BF7BC43E4E1DB26CA20588E98CFDED3C60C955D6BD874BFD6E5B87F263B`
- S2: `.../GT058_20260824_101412_S2_COUNT1_TRAIL0_807p000s.jpg`
  - `D80225FC9531BC63A3996B2AD0231716A3DEC60BC44D29B4D7766F82588DAB05`
- S3: `.../GT058_20260824_101412_S3_COUNT1_TRAIL1_810p000s.jpg`
  - `B8F41AC860F33F0C5B0F08C08CFFCF0708E58E23BDABB377A185266EB8D080F4`
- S4: `.../GT058_20260824_101412_S4_COUNT3_TRAIL0_813p000s.jpg`
  - `D7B3CC1ADD26CE0DAB2CB4AF5EBC64F218473514CBD552F301CDEB88BDE9FEDA`
- S5: `.../GT058_20260824_101412_S5_COUNT3_TRAIL1_816p000s.jpg`
  - `808CCE4FD32A6DEC53CC13C369B0FB7A7F77DD7FF9B7381897AA19993F79A189`
- skill-button proof: `pf_bridge/evidence_screens/GT058_20260824_101412_SKILL_BUTTON_TOOLTIP_NO_WINDOW_936p000s.jpg`
  - `AE1F30E37118C03BEA92149FD86C53B086C69D80112E93E70970A4EBC1AD8224`
- raw GAME: `GameClient/capture_gt058_20260824_101412/capture_v141/GAME_20260824_101814_611858_53760.txt`
  - `78E7537BE609C2FE7F8EA1AD08654ADCA2A7CD4AA374495C02379AB6AEFDAB05`
- GAME events: `.../GAME_EVENTS_LIVE.txt`
  - `C0352D7097B83DC367B757754277A58E62D5BE101F5399FCD030F7DBF05FDA57`
- server console: `GameClient/capture_gt058_20260824_101412/server_console_live.out.txt`
  - `593A579435A765716F07D0091E3AF7042423437B1FD3EEB3B474B8615BCF4DA0`
- scenario manifest sha256: `BF0C111584B1F5922C38DBF1782D535D26279B7718D82127B9C2E39C93365EE4`

## Interpretation / redirect

- ข้อเท็จจริง: skill button มีอยู่, tooltip ระบุ K, แต่หน้าต่างไม่เปิดทั้งก่อน/หลังเฟรม; sweep ไม่ทำให้ UI/chat/HUD ที่มองเห็นเปลี่ยนและ client ไม่ crash.
- inference (ไม่ใช่สิ่งที่ใบนี้พิสูจน์): baseline local อาจขาด prerequisite/population/state ที่ทำให้ skill window เปิด. ถ้าต้องการตอบว่า record เปลี่ยนรายการภายในหน้าต่างหรือไม่ ควรเปิดใบ follow-up บน baseline ที่ยืนยันก่อนยิงว่า K เปิด skill window ได้ หรือเติม prerequisite packet/state แบบมีพินก่อน; ผู้เทสไม่เปิดใบเอง.

## Nonclaims

- ไม่ตีความความหมายของสมาชิก record `(u32/u16/u32)`; semantics ยัง opaque.
- ไม่ claim ว่า original server เคยใช้เฟรม/version นี้; การประกอบและ version byte 0 เป็นดีไซน์ของเรา.
- ไม่ claim ว่า count/trailing map กับความหมายเชิงเกม; sweep นี้วัด tolerance/observable behavior เท่านั้น.
- ไม่พิสูจน์ทิศทาง client ส่งกลับ; ใบนี้ inbound-only observe.
- ไม่ claim ว่า skill list ภายในไม่เปลี่ยน เพราะหน้าต่างนั้นเปิดไม่ได้; claim เฉพาะว่าไม่มีผลที่มองเห็นและเฟรมไม่ทำให้หน้าต่างเปิด.
