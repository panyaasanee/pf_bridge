[ถึง: chief cloud (cc) และ Panya · จาก: ผู้เทส Codex LOCAL]

# GT-034 HOSTILE-NATIVE-001 — เสนอ NO-RESULT / รอ Panya

เวลาโดยรวม: 2026-08-24 02:10:47–02:28:23 (+07:00)

## สถานะที่เสนอ

**คง GT-034 เป็น PENDING / NO-RESULT และรอ Panya ทดสอบด้วยตาวันที่ 2026-08-26**

รอบนี้หยุดก่อน input แรกในเกม เพราะ Windows Computer Use คืน error ดิบ `computer-use request timed out: list_apps` สามครั้งติดกัน: ครั้งแรก, retry หลังรอ 2 วินาที, และครั้งสุดท้ายหลัง reset JavaScript session ตาม recovery ของสกิล จึงยังไม่ได้เข้าแมพและยังไม่ได้วัดคำถามหลักของใบ

- ห้าม redirect Door A
- GT-035 / GT-036 คง BLOCKED; ผู้เทสไม่ได้ปลดเอง
- พิกัดตัวละคร: **ยังไม่ได้วัด** (client ค้างที่หน้าเลือกเซิร์ฟเวอร์ก่อน teardown)
- ทิศกล้องที่กวาด: **0 ทิศ / 0 รอบ — ยังไม่ได้วัด**
- S0 / S1 / S2 / S3: **ยังไม่ได้ผลิต** เพราะยังไม่ถึงหน้าแมพ
- input: click 0 ครั้ง, key 0 ครั้ง, chat 0 ครั้ง, movement 0 ครั้ง, attack 0 ครั้ง

## Gate และสิ่งที่บูตจริง

- `pf_resolve_green_boot.py --fetch` exit 0: `BOOT_COMMIT 7b2e1e50d2794491265bc9b9c02a0ec0e7945422`
- decision file: `sha` ตรงและ `conclusion=success`
- `git grep` พบ `scene-load-scenario` ใน `src/pirateforce_foundation/app.py`
- `git cat-file` พบ `scenarios/port_royal_tornado_eagle_p30_load_only.json` (`SCENARIO_PRESENT`)
- boot tree `2313bd867d64974e64955f84411effcdfc452440` ตรง tree ของ `main` HEAD `1408e22e23507a6237af5def0151c477afa52d0f`; worktree สะอาด
- main attempt: jobs `1066` boot + continuous video, `1067` guarded teardown; `1068` release lock
- preflight `1060` PASS; `1061` lock wrapper หยุดอย่างปลอดภัยก่อนเขียนธงจาก empty-string binding; `1062` ถือธงสำเร็จ; `1063` resolve ผ่าน
- tooling attempt แรก `1064` ถูก teardown ครบด้วย `1065` ก่อน retry เพราะ stdout/stderr redirection ทำให้ bridge รอ child process
- เลขจ็อบผู้เทสตัวถัดไป: `1069`

## หลักฐานชั้น client-observable

วิดีโอหลักอัดด้วย FFmpeg 9.0 `gdigrab`, H.264, 1920x1080, **30 fps** ตั้งแต่ก่อน server/client ขึ้นจน generic teardown ตรวจ DB/canonical เสร็จ:

- path: `C:\Users\Panya\Desktop\Pirate Force\pf_bridge\evidence_screens\GT034_FULLROUND_1066_20260824_022354.mkv`
- SHA256: `91793B36E2517B9BE5D8C4DB165EFDC5F9E087DC2C193D0764A5F6A057F2CB26`
- ระยะ: `165.366` วินาที · bytes `58,771,334`
- เวลาเริ่ม: `2026-08-24 02:23:56.439 (+07:00)`
- ช่วงควรดู:
  - `00:00–00:06` — video เริ่มก่อน server และ GameClient
  - `00:20` — GameClient window ขึ้น แต่ยังเป็นเฟรมขาว; ffmpeg console ทับกลางจอ
  - `02:15` — หน้าเลือกเซิร์ฟเวอร์อ่านออก; ffmpeg console ยังทับกลางจอ; ยังไม่เคยรับ input
  - `02:22–02:45` — teardown ปิด client, ส่ง Ctrl+C ให้ server, ตรวจ DB/canonical แล้วหยุด video

เฟรมที่สกัดจากวิดีโอหลัก:

- `pf_bridge\evidence_screens\GT034_BLOCKED_server_select_t+20s.png` — SHA256 `F12149ADDB7EE9C3005823622A9A2658FAE7A70D6440029A6A9E720A34AC8421`
- `pf_bridge\evidence_screens\GT034_BLOCKED_pre_teardown_t+135s.png` — SHA256 `71BCD57A5EB7EB1CD7EA517DE3D8E16613A6681EDF2DEE25C9D187A9EC28E2A3`
- `pf_bridge\evidence_screens\GT034_BLOCKED_teardown_t+160s.png` — SHA256 `2D18D7CCCDD15FB2563B226A07FBB876C538E76CEEA41BCC6429016FD47FC31C`

ข้อเท็จจริงจากวิดีโอ: client ไปถึงหน้าเลือกเซิร์ฟเวอร์ แต่ controller enumerate หน้าต่างไม่สำเร็จ จึงหยุดโดยไม่เดาพิกัดคลิก นอกจากนี้ boot `1066` มี error ดิบแบบ non-terminating:

`Exception setting "ShowWindow": "The property 'ShowWindow' cannot be found on this object."`

ผลคือ ffmpeg console เปิดแบบมองเห็นและทับกลางหน้าต่างเกมตามเฟรมข้างต้น จดเป็น tooling blocker เพิ่ม ไม่ใช้เป็นคำตอบเรื่องตัวนก

artifact จาก tooling attempt แรก (ไม่ใช่วิดีโอหลัก): `pf_bridge\evidence_screens\GT034_FULLROUND_1064_20260824_021828.mkv` · SHA256 `9CB9545444C9AFD4B27DED2C931BF289352202DA5CB9C12A7D69FC1DDE4DD125` · 116.733 วินาที; attempt นี้ teardown แล้วก่อน retry

## หลักฐานชั้น wire / DB

main attempt capture root:

`C:\Users\Panya\Desktop\Pirate Force\GameClient\capture_gt034_20260824_022354`

- server console: `server_console_live.out.txt` 12,271 bytes; `server_console_live.err.txt` 0 bytes
- LOGIN capture: `capture_v141\LOGIN_20260824_022430_106482_54979.txt` 1,334 bytes; login request/response ถูกบันทึก
- runtime counts: `StartGameReq=0`, `StartGameRes=0`, `SCENE2_LOAD_ONLY_SELECTED_START_GAME=0`, `SCENE2_LOAD_ONLY_TELEPORT_MARKER2_ONCE=0`
- จึงยังไม่ได้ยิง scene-load scenario และชั้น wire ยังไม่ได้วัดตำแหน่ง/heading/teleport ของ GT-034 รอบนี้
- `Traceback=0`, `ErrorData 28317=0`, `[FOUNDATION] stopped=1`

DB main attempt:

- canonical ก่อน: `EE785A79EAC3FDC962AF66E13C2F5943DACF733F0B8D85EAFB658F889A79C17C`
- canonical หลัง: `EE785A79EAC3FDC962AF66E13C2F5943DACF733F0B8D85EAFB658F889A79C17C`
- run-copy ก่อน: `EE785A79EAC3FDC962AF66E13C2F5943DACF733F0B8D85EAFB658F889A79C17C`
- run-copy หลัง: `EE785A79EAC3FDC962AF66E13C2F5943DACF733F0B8D85EAFB658F889A79C17C`
- backup: `pf_bridge\backup\pirateforce_before_GT-034_20260824_022354.sqlite3` SHA256 เดียวกัน
- run DB: `Pirate Force ServerProject\state\run_gt034_20260824_022354.sqlite3`
- ก่อน/หลัง: sessions with selected character `9 -> 9`; max lease `10 -> 10`; open sessions `0`; integrity `ok`; FK rows `0`

## Teardown

- tooling attempt แรก teardown `1065` ผ่าน
- main attempt teardown `1067` ผ่าน
- GameClient `0` process
- listeners 10188/10189 `0`
- ffmpeg `0` process หลังวิดีโอถูก finalize และ `ffprobe` ผ่าน
- server stopped marker `1`; traceback `0`; stderr `0B`
- canonical SHA ตรง `CANON_SHA.txt` ก่อนและหลัง
- run-copy SHA ตรงก่อนและหลัง
- inbox ว่าง
- `LOCK_GAME.txt` ปล่อยเป็น RELEASED เวลา `2026-08-24 02:28:23 (+07:00)`

## Nonclaims

- รอบนี้ยังไม่ได้วัด `native_render`, สีชื่อ/กรอบของ Tornado Eagle, `heading_mapping`, `camera_orientation`, `client_standing_position`, `scene_id_numeric_provenance` หรือ `scene_seq_provenance`
- วิดีโอแก้จุดบอดเหตุการณ์เสี้ยววินาทีได้เฉพาะเมื่อเหตุการณ์อยู่ในภาพ; รอบนี้ยังไม่ถึงหน้าแมพ
- ชั้น wire/DB ตอบแทนชั้น client-observable ไม่ได้ และชั้น client-observable ตอบแทน wire/DB ไม่ได้
- faction / AI / drops เป็นข้อมูลที่ ship มากับ client ไม่ใช่พฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ
- การย้ายจุดวางตัวละครเป็นดีไซน์ GEO-PF-006 ของเรา; รอบนี้ scenario ยังไม่ถูกยิง
- ใบนี้ไม่ตอบการตี (GT-035) หรือการฆ่า (GT-036)
