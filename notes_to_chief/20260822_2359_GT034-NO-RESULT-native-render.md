ถึง: chief + Panya

# GT-034 HOSTILE-NATIVE-001 — NO-RESULT ของคำถามหลัก (กรณี 3)

เวลา: 2026-08-22 23:47–23:56 (+07:00) · ผู้เทส: Codex ATTENDED (LOCAL)

## คำตัดสินที่เสนอ

**คง GT-034 เป็น PENDING / NO-RESULT ตามตารางกรณี 3**: เข้า Port Royal ที่พิกัดตามคำทำนายและหมุนกล้องอย่างเดียวครบ 360° แล้ว แต่ไม่เห็นมอนสเตอร์รูปนกหรือป้ายชื่อ `Tornado Eagle` เลย จึงตอบไม่ได้ว่า hostile ตัวจริงขึ้นแดงเองตอน scene-load หรือไม่

- ห้ามอ่านเป็น “เห็นนกแต่ไม่แดง” และห้าม redirect Door A
- **GT-035/GT-036 ยัง BLOCKED**; ผู้เทสไม่ได้ปลดเอง
- ไม่มีการเดิน ไม่มีการโจมตี ไม่มี chat trigger และไม่มีการเลือกเป้า

## Gate และสิ่งที่บูตจริง

- `pf_resolve_green_boot.py --fetch` exit 0: `BOOT_COMMIT b665d9276bcd05ac256132372310fb64d26b163f`
- `origin/ci-status:ci/b665d9276bcd05ac256132372310fb64d26b163f.json`: `sha` ตรงและ `conclusion=success`
- `git grep` พบ `scene-load-scenario` ใน `src/pirateforce_foundation/app.py`
- `git cat-file` พบ `scenarios/port_royal_tornado_eagle_p30_load_only.json`
- `HEAD cf81730` กับ boot commit มี tree เดียวกัน: `39edf49dd73a5307343eec1dc251f8a7067c21e1`
- บูตจาก exact green tree ที่ materialize ด้วย `git archive` ณ `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\boot_trees\gt034_20260822_234733`; main worktree/HEAD ไม่ถูก checkout หรือแก้
- boot stamp `20260822_234733`; job 983 boot, job 984 teardown, job 985 helper เปลี่ยนชื่อหน้าต่าง console เพื่อให้ input bridge แยกหน้าต่างเกมได้

## ชั้น client-observable

- S0 ทันทีหลังเข้าแมพ ก่อน input: HUD `HP 100/100`, `Port Royal`, `X 1,847 / Y -7,837`; ภาพตรงหน้าเป็นกำแพง/อาคาร ไม่เห็นนก
- S1 หลังยืนนิ่งประมาณ 30 วินาที: พิกัดและภาพรวมเดิม ไม่เห็นนก
- หมุนด้วย Q อย่างเดียวเป็นช่วง 300+500+800+700+700+700+300 ms รวมประมาณ 4.0 วินาที พร้อมตรวจภาพทุกช่วง; มุมมองกวาดผ่านกำแพง ลานเปิด/ปราสาท บันได และตลาด ก่อนกลับมาใกล้มุมเริ่มต้น = ครบ 360° โดยตำแหน่ง HUD ไม่ขยับ ไม่เห็นสิ่งมีชีวิต/ป้ายชื่อเป้าหมาย
- **ไม่มี S2 โดยเจตนา**: step 8 กำหนด S2 เมื่อเห็นเป้าและเลือกหนึ่งคลิก แต่รอบนี้ไม่เห็นเป้า จึงไม่มี target panel ให้ถ่าย; การสร้าง S2 ปลอมจะขัดโปรโตคอล
- S3 หลัง sweep หลัก: ไม่เห็นนก; ภาพเป็นมุมกดลงจากผลข้างเคียงของการทดลอง right-drag หลัง sweep หลัก (ดูข้อสังเกตเครื่องมือด้านล่าง)
- ไม่เห็นนกเข้าโจมตีเอง และผู้เล่นไม่ถูกโจมตี

คำตอบสี่ข้อ:

1. (ก) ไม่เห็นมอนสเตอร์รูปนกในทุกทิศหลัง sweep 360°; จึงระบุทิศ/ระยะไม่ได้
2. (ข) ไม่มีป้ายลอยหรือ target panel จึงระบุชื่อหรือสีแดง/neutral ไม่ได้
3. (ค) HUD จริง `X 1,847 / Y -7,837` ตรงค่าคาดเมื่อปัดเศษ (`1847.5244, -7837.6978`); HUD รุ่นนี้ไม่แสดง Z แต่ wire ส่ง `931.0413208007812`
4. (ง) กล้องแรกเข้าเห็นกำแพง/อาคาร ไม่เห็นเป้า; จึงไม่ยืนยัน mapping ของ heading π กับทิศกล้อง

ภาพถาวร:

- `pf_bridge\test_evidence\GT034_S0_first_frame_20260822_2348.png` — SHA256 `2F2F58412139514C23D2E07AC18BA733D64158C9FCFFF34A46CDF4445B3EB3D2`
- `pf_bridge\test_evidence\GT034_S1_stationary_30s_20260822_2349.png` — SHA256 `6952CA5C5446B8896932F1F9C867C552D1D8D5E6F31F648E7CD61B41939ADD7F`
- `pf_bridge\test_evidence\GT034_S3_final_after_360_20260822_2356.png` — SHA256 `AB9FF09A43CC610DF7CA458C1CE7AE8CD37C910231916972ECDE166C6E66D199`

## ชั้น wire / DB

- StartGameRes label `SCENE2_LOAD_ONLY_SELECTED_START_GAME` พา f32:
  `x=1847.5244140625`, `y=-7837.69775390625`, `z=931.0413208007812`, `heading=3.1415927410125732`
- server→client label `SCENE2_LOAD_ONLY_TELEPORT_MARKER2_ONCE` พา XYZ exact ชุดเดียวกัน; client→server `TeleportVital` รายงานกลับ `1847.5244140625, -7837.69775390625, 931.0, 3.1415927410125732` (Z ที่ client รายงานกลับปัดเป็น 931.0)
- runtime outbound labels ไม่มีชื่อที่มี `SPLICE|POPULATION|FACTION|NPC|MONSTER|BIRD|ACTOR`; ไม่มี population หรือ remote_actor lane
- `ErrorData=28317` = 0
- raw GAME: `C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt034_20260822_234733\capture_v141\GAME_20260822_234851_609592_59146.txt` (565,171 bytes)
- console: `C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt034_20260822_234733\server_console_live.out.txt` (110,270 bytes); stderr 0 bytes
- canonical / run copy / backup = 86,016 bytes และ SHA256 เท่ากันทั้งหมดก่อน-หลัง:
  `6BFCEDD5593D316A27A6C300206A9A3BEEC5E65631835308E02289B5FE498FC7`
- run DB `integrity_check=ok`, FK=0, sessions with character=7, open=0, max lease=8

## Teardown และข้อสังเกตเครื่องมือ

- client ออกผ่าน X + ปุ่มยืนยันซ้าย; GameClient=0, listeners=0, server/console stopped, stopped marker=1, traceback=0, stderr=0B, inbox ว่าง
- job 979 และ 981 abort ก่อน server เริ่ม เพราะ quoting ของ Windows PowerShell 5; แก้เป็นส่ง Python script ทาง stdin แล้ว job 983 ผ่าน
- wrapper `984_gt034_teardown.ps1` ส่ง `-JobTag 984_gt034_teardown` แต่ template ภายในประกาศ `$jobTag=''` ซึ่งชนแบบ case-insensitive กับ parameter `$JobTag`; receipt จึงถูกตั้งชื่อ `TEMPLATE_teardown_generic.*` แทน `984_*` แม้ teardown สำเร็จครบ ขอ chief/เจ้าของ tooling แก้ชื่อ local variable
- หลัง sweep Q หลัก ทดลอง right-drag 4 ครั้ง: tool ตอบ success แต่กล้องกลายเป็น top-down และ drag กลับไม่คืนมุมเดิม; ไม่ใช้ช่วงนี้เป็นหลักฐานว่าหมุนเพิ่มหรือเป็นผลของเกม
- mouse wheel ขึ้น/ลง 2 ครั้งไม่เห็นความเปลี่ยน zoom ชัดเจนในภาพรอบนี้ จึงไม่ claim ว่าซูมทำงาน/ไม่ทำงาน
- keyboard injection ของ Sky หลายครั้งไม่หมุน; custom input bridge `hold_game_key(Q)` 7/7 ครั้งหมุนได้ตามระยะกด คาดว่าเสียเวลาประมาณ 4 นาทีในการแยกปัญหา input
- คลิก UI 7 จุด (server, channel, enter, PVP-left, Arena01, character-enter, X/confirm นับเป็นลำดับออก) สำเร็จโดยไม่เกิดการลบตัวละครหรือกดผิด action

## Nonclaims บังคับ

- faction / AI / drops เป็นข้อมูลที่ ship มากับ client ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ ซึ่งกู้ไม่ได้ตลอดกาล
- การย้ายจุดวางตัวละครเป็นดีไซน์ GEO-PF-006 ของเรา; ไม่ claim ว่าผู้เล่นจริงเคยเกิดตรงนี้
- ใบนี้ไม่ตอบว่าตีนกได้ไหมหรือฆ่าได้ไหม และไม่ได้พิสูจน์ native-red เพราะไม่เห็นตัว
- `heading_mapping`, `camera_orientation`, `native_render`, `client_standing_position`, `scene_id_numeric_provenance`, `scene_seq_provenance` ยังเป็น nonclaims
- “แมพเดียวกัน” ยังพิสูจน์ที่ระดับ placement/file-membership + HUD `Port Royal`; เลข scene id เชิงตัวเลขยังต้อง GT-044

