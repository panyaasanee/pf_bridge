[ถึง: chief cloud (cc) และ Panya · จาก: Codex LOCAL]

# ผลต่อ recorder: ซ่อนคอนโซล + frame proof

เวลา: 2026-08-24 07:50:10 ถึง 07:57:41 +07:00

## 1) isolated test: PASS หลังแก้ defect ที่วัดเจอ

- รอบแรก 07:50:10-07:50:27: ffmpeg gdigrab 1920x1080 30 fps อัดครบ 15.000 วินาที และ `FRAME_PROOF=OK` แต่ตัวซ่อนยังไม่ผ่าน จึงไม่นับเป็น PASS
- error ดิบรอบแรก: `Cannot overwrite variable Pid because it is read-only or constant.` สาเหตุคือ parameter `$Pid` ใน `Get-VisibleWindowsForPid` ชน automatic variable `$PID` ของ PowerShell ซึ่งไม่แยกตัวพิมพ์เล็ก/ใหญ่
- แก้เป็น `$TargetProcessId` แล้วรันใหม่ 07:50:54-07:51:12 ด้วย `Win32_Process.Create` + `Win32_ProcessStartup.ShowWindow=0` แบบเดียวกับจ็อบ 1066
- ผลรอบใหม่: `HIDE_WINDOW pid=23340 seen=0 hidden=0 still_visible=0`, `HIDE_WINDOW=OK`, exit 0
- วิดีโอรอบใหม่: 15.000 วินาที, 1,038,499 bytes, `FRAME_PROOF=OK`, 3/3 เฟรม
- เปิด PNG ดูจริงครบทั้งสามเฟรมที่ 5.0s / 7.5s / 12.0s: เป็นเดสก์ท็อปเต็มภาพ ไม่มีคอนโซล ffmpeg หรือ PowerShell ทับกลางภาพ
- path ตอนเปิดดู: `evidence_screens\FRAME_TEST_5s_20260824_075110.png`, `evidence_screens\FRAME_TEST_7p5s_20260824_075110.png`, `evidence_screens\FRAME_TEST_12s_20260824_075110.png`
- ตามคำสั่ง ห้ามลบ: ย้ายวิดีโอและ PNG ของทั้งรอบแรก/รอบ retry ไปแล้วที่ `_to_delete\` ปัจจุบัน proof ที่เปิดดูอยู่ที่ `_to_delete\FRAME_TEST_5s_20260824_075110.png`, `_to_delete\FRAME_TEST_7p5s_20260824_075110.png`, `_to_delete\FRAME_TEST_12s_20260824_075110.png`

## 2) การต่อเทมเพลต

- ใน tree ไม่มี video-recorder template เดิม มีเพียง `done\1066_gt034_boot_video_retry.ps1` ที่ถูก ignore และ `staged\1067_gt034_teardown_video_retry.ps1` ซึ่งผูกกับ GT-034 โดยเฉพาะ จึงสร้าง reusable template ตัวเดียวที่ `staged\TEMPLATE_video_recorder.ps1` โดยยกท่าที่พิสูจน์แล้วจาก 1066/1067
- boot function ตรวจ ffmpeg process + output file ว่ายังมีชีวิตก่อน แล้วเรียก `agent_kit\pf_recorder_hide_window.ps1` ด้วย PID
- exit code 2 จาก hide helper เป็น `VIDEO_WARN` เท่านั้น รอบเดินต่อ; error อื่นก็เป็น warning ถ้า ffmpeg ยังมีชีวิต แต่ถ้า ffmpeg ตายจึงหยุด boot
- teardown function หยุด ffmpeg ด้วย PID/name/start-time guard ก่อน แล้วเรียก `pf_recorder_frame_proof.ps1 -JobTag <รอบ>` เสมอ และคืน `ResultCode`/path เฟรมให้ teardown job รวมผลเอง
- template ผ่าน parse gate, ASCII gate (non-ASCII bytes 0) และ integration test จริง: `HIDE_WINDOW=OK`, `FRAME_PROOF=OK`; เปิด `_to_delete\FRAME_TEMPLATE_TEST_4s_20260824_075538.png` ดูจริงแล้วไม่มีคอนโซล
- test artifacts ของ integration test ถูกย้ายไป `_to_delete\` เช่นกัน ไม่มีการลบ

## 3) commit

- จับ `LOCK_GIT` เวลา 07:57:23 +07:00; stage ด้วย path ระบุชื่อ 3 ไฟล์เท่านั้น; ตรวจ `git status --short` และ cached names ตรง 3/3
- commit: `234c51f289d26c0c30ebec98ac861f633907735f` (`add hidden recorder and frame-proof template`)
- committed paths: `agent_kit\pf_recorder_hide_window.ps1`, `agent_kit\pf_recorder_frame_proof.ps1`, `staged\TEMPLATE_video_recorder.ps1`
- exact post-status ของสาม path ว่าง; ปล่อย `LOCK_GIT` เป็น `RELEASED` เวลา 07:57:23 +07:00
- ไม่ได้ push

## 4) .gitignore

- PASS: สองไฟล์ `agent_kit\*.ps1` ไม่ถูก ignore
- `git check-ignore -q` คืน rc=1 ทั้งสองไฟล์; verbose match ก่อนหน้าแสดงกฎเปิด `!/agent_kit/**` ที่ `.gitignore:43`
- ไม่ได้แก้ `.gitignore`

## ขอบเขต/สภาพจบ

- ไม่เคยจับ `LOCK_GAME`; หัวธงยังเป็น `RELEASED: 2026-08-24T02:28:23+07:00`
- ไม่เปิดเกม ไม่เปิด server ไม่แตะ canonical DB และไม่อ่าน/แก้ไฟล์คิวทั้งสาม
- ffmpeg process ตอนจบ = 0
- ไม่ลบหรือเปลี่ยนชื่อไฟล์เดิมใน `notes_to_chief\`
