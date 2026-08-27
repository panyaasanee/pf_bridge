# GT-084-R2 RESULT 2026-08-27 16:20 +07:00 — ประตูข้อแรกผ่าน (นกเป็นศัตรูจริง) + ผลต่อของ GT-084: ตี 5 ครั้ง ตายบนสายครบ DYING/DEAD/LOOT — แต่บนจอ "ศพแข็งลอยค้าง ไม่ล้ม" และ single-click ไม่มีแผงเป้าด้านบน

ถึง: สาย B (เจ้าของใบ GT-084/GT-084-R2 · ADDRESSEE: LANE-B) · chief · RE runner · cc COO, สาย A
จาก: attended session "กะ1" (Panya ขับ UI เองทั้งรอบ ตามกติกาใหม่ "อธิบายก่อน → ทราบ → บูต") · OBSERVER_CONFIRMED: 2026-08-27T15:52-15:55+07:00 (เจ้าของเห็นเอง + ภาพในเกม 4 ใบ + วิดีโอเต็มรอบ)

## สถานะที่ควรเป็น
- **GT-084-R2 = PASS (claim เดียวของใบ: client ปฏิบัติกับ Tornado Eagle เป็นศัตรูตั้งแต่ก่อนโจมตี)** — แต่ผ่านด้วยหลักฐาน "พฤติกรรม" ไม่ใช่ "สีตามใบ": ป้ายชื่อเป็น**สีชมพู/magenta** (ไม่ใช่แดง) · single-click ได้**ขอบแดงรอบตัว + ลูกศรแดงคู่ล็อกที่ชื่อ** · **ไม่มีแผง UI ข้อมูลเป้าหมายด้านบนจอ** (ใบเขียนเกณฑ์ "แผงเป้าแดง" — แผงไม่ขึ้นเลย) · ดับเบิลคลิกแล้วตัวละครวิ่งเข้าตีได้จริง มีเลขดาเมจ นกกระตุกทุกครั้ง ⇒ hostile จริงทั้งชั้น wire และชั้น client แต่**เกณฑ์สี/แผงของใบต้องแก้ตามที่เห็นจริง** (เจ้าของมีข้อมูลเทียบเซิร์ฟเวอร์เดิมเรื่องการตีมอน จะเล่าเพิ่ม — รอใบต่อ)
- **ผลต่อของ GT-084 (ขั้นโจมตี-ตาย) = PASS ชั้น wire ครบ / FAIL ชั้นจอ 2 จุด**: (1) ศพไม่ล้ม — ค้างท่าลอย "แข็ง" ไม่ขยับ ไม่กระพือปีก จน logout, cursor ไม่รับรู้ว่ามี actor ตรงนั้นอีก (2) ไม่เห็น loot บนพื้นทั้งที่เซิร์ฟเวอร์ส่ง MOB_LOOT_DROP 2 ใบ (ผู้เทสยังไม่ได้ถามเจ้าของตรง ๆ ว่ามองหาแล้วหรือยัง — ถือเป็น "ไม่ได้รายงานว่าเห็น" ไม่ใช่ "ยืนยันว่าไม่มี")
- **GT-104 (widen death scope) ยังไม่ได้แตะ** — เป้าหมายรอบนี้คือ 0x201F เท่านั้น

## บูต (jobs 1296 hold+resolve · 1294 boot_video · 1295 teardown_video วางโดยเจ้าของผ่าน STOP_ROUND_AND_VIDEO.bat · release 1297)
- BOOT_COMMIT **0cbab133** = main HEAD (merge #126) มีคำตัดสินเขียวของตัวเอง (workflow_dispatch run 33054759907 08:46Z) · code delta vs main 0 · ไร้แฟล็ก (SERVER_CMDLINE: `-m pirateforce_foundation.app --db ...run_gt084r2_20260827_154848.sqlite3 --capture-root ...` ไม่มี `--*-scenario`)
- ด่าน 1: `E38E575_ANCESTOR_OK` · ด่าน 2 (อ่านโค้ดจริง): print อยู่ที่ runtime.py:4881-4885 ใน `_dispatch_with_lanes` กิ่ง `elif not active_lanes:` (บรรทัด 4806) — **นอก** `_npc_hostile_start_game_response` (3031) และนอก `if npc_hostile_hypothesis_scenario is not None:` (4802) ⇒ ผ่าน · หมายเหตุให้คนเขียนใบ: grep ตามใบ (`"PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game"` ทั้งสตริง) ได้ 0 เพราะซอร์สต่อสตริงจาก f-string 3 ท่อน — ต้อง grep `sent_on_flagless_start_game` (job 1293 รอบแรกตกด่านด้วยเหตุนี้ แก้เป็น 1296)
- DB สำเนา run_gt084r2_20260827_154848 · canonical 4FF37060… ไม่เปลี่ยน (ก่อน/หลัง) · teardown สะอาด listeners 0 clients 0 ffmpeg 0 · integrity ok
- วิดีโอเต็มรอบ: evidence_video\1294_gt084r2_FULLROUND_20260827_154851.mkv (469 s, 151 MB) · ภาพในเกมของเจ้าของ: evidence_screens\GT084R2_ingame_20260827_155206/155231/155310/155341.png · stills จากวิดีโอ: GT084R2_video_stills_*.png

## ชั้น wire/DB (GameClient\capture_gt084r2_20260827_154848\server_console_live.out.txt — เลขบรรทัดของไฟล์นั้น)
- L165 `PLAYER_FACTION basic_faction=1 sent_on_flagless_start_game` — พิมพ์ตอน StartGame ของเซสชันนี้จริง (ระหว่าง WORLD_SCENE L163 กับ FOUNDATION_SELECTED_START_GAME) ⇒ เกณฑ์ wire ข้อหลักของใบผ่าน
- L255 `MOB_DEATH_ROSTER_OVERRIDE_COVERAGE matched=13/13` · L256 `WORLD_CENSUS assembled=115/115` · L258 `[G>] WORLD_CENSUS_INITIAL_115` (HB#16 ≈ +3 s หลัง login) · L1573 REAPPLY (HB#17) — **หลังจากนั้นไม่มีเฟรมสำมะโนอีกจน hit แรก** (ไม่มี spawn เพิ่มเติม ไม่มี refresh ระยะใกล้)
- โจมตี: client ส่ง ActionVital 5 ใบ (L3167 113B, ที่เหลือ 84B) → `MOB-COMBAT-001 hit: performer 0x10010001 -> target 0x201F` 5 ครั้ง (L3176/4545/5878/7211/8556) แต่ละครั้ง `MOB_COMBAT_BAR_CENSUS_RECOMPOSE actor_count=115` + `[G>] MOB_COMBAT_ANNOUNCE 95B` + `[G>] MOB_COMBAT_BAR 21021B` (4 ครั้งแรก) — world-wipe fix ของสาย B ทำงานจริงบน client (เจ้าของไม่รายงานว่า NPC อื่นหายระหว่างตี)
- ตาย: L8556 hit ที่ 5 `hp 1 -> 0 of 3857 overkill by 963` → L8562 `MOB-DEATH-001 kill … (ceiling 3857)` · dying frame 164B timer 20.0 · dead frame 164B timer 0.0 · hold 700 ms · `MOB_DEATH_FRAMES_CENSUS_RECOMPOSE actor_count=115` · L8568 `MOB_LOOT_DROPS_CENSUS mob='Tornado Eagle' template=31 drops=2 items=2400046:x1@0x100000,2400047:x1@0x100001` · L8576 `[G>] MOB_DEATH_DYING 20968B` · L9887 `[G>] MOB_DEATH_DEAD 20968B` · L11198/11202 `[G>] MOB_LOOT_DROP 54B ×2` (ทั้งหมดใน HB#95 เดียวกัน)
- ไม่มี traceback · ไม่มี socket reset (client ปิดเองตอน logout ปกติ) · G< รวม: TargetPosVital 54, COnLandVital 17, ActionVital 5, TeleportVital 1

## ชั้น client-observable (คำเจ้าของ คำต่อคำโดยสรุป + วิดีโอยืนยัน)
1. **นกเกิดช้ากว่า NPC อื่นมาก**: NPC ทุกตัวโผล่ตอนเริ่มกดเดิน แต่นกยังไม่มีตอนเดินมาถึง (ภาพ 155206 ที่ผนังมี "Local people" แต่ไม่มีนก) — โผล่หลังถ่ายภาพแรกเสร็จ · วิดีโอ: นกอยู่แล้วที่ 15:52:28 (offset 216 s) ⇒ โผล่ระหว่าง 15:52:06-15:52:28 · **ฝั่งสาย: นกอยู่ในเฟรมสำมะโนเดียวกับ NPC ทุกตัวตั้งแต่ L258 และไม่มีเฟรมเพิ่มหลังจากนั้น** ⇒ ความช้าเป็นเรื่องฝั่ง client (โหลดโมเดล/สตรีมตามระยะ?) ไม่ใช่เซิร์ฟเวอร์ส่งช้า — [ไม่อ้าง] สาเหตุ
2. **single-click**: ขอบแดงรอบตัว + ลูกศรแดงคู่ล็อกที่ชื่อ (ชื่อสีชมพู) · **ไม่มีแผง UI ข้อมูลเป้าหมายด้านบนจอ** (ต่างจาก GT-045 v3 ที่ single-click เปิดแผงเป้าได้)
3. **ดับเบิลคลิก** = วิ่งเข้าไปตี 1 ครั้ง/ดับเบิลคลิก มีเลขดาเมจ นกกระตุกทุกครั้ง (ตรง ActionVital 5 ใบ = hit 5 ครั้ง)
4. **เลือดหมด**: ข้อความ "Tornado Eagle บาดเจ็บหนักและล้มลง!" ขึ้น (ทั้งลอยที่ตัวและในแชต) แล้วนก**แข็งค้างท่าลอย** ไม่ล้ม ไม่มีอนิเมชัน cursor ไม่จับ actor นั้นอีก ค้างจน logout (วิดีโอ 15:53:02-15:54:17 ท่าเดียวกันทุกเฟรม เจ้าของหมุนกล้องรอบตัวแล้ว)

## nonclaims
- [ไม่อ้าง] ว่าสีชมพูของชื่อ = "hostile" ในความหมายของ client เดิม — เจ้าของจะเทียบกับเซิร์ฟเวอร์เดิมให้ (ใบต่อ)
- [ไม่อ้าง] สาเหตุที่ศพแข็ง — ข้อสังเกตเชิงลำดับ: dying frame ประกาศ timer 20.0 แต่ DEAD ตามมาใน 700 ms (ค่า "provisional, unmeasured" ตามคอนโซล) · client แสดงข้อความตายได้ (รับ DYING) แต่ไม่เล่นอนิเมชันล้ม และหลัง DEAD actor หายจาก picking แต่ mesh ค้าง ⇒ สมมติฐานที่ต้องวัด: (ก) DEAD มาเร็วเกินตัด dying animation (ข) เฟรม dying ขาดฟิลด์ที่สั่ง animation (ค) เฟรม DEAD ลบ actor จาก logic แต่ไม่ลบ render — ทั้งสามต้องให้ RE/สาย B ตอบ ห้ามเดา
- [ไม่อ้าง] ว่า loot ไม่ปรากฏ — เจ้าของไม่ได้รายงานว่าเห็น/ไม่เห็น ผู้ช่วยจะถาม
- [ไม่อ้าง] ว่าไม่มีแผงเป้า = ฝั่งเซิร์ฟเวอร์ผิด — อาจต้องมี vital ตอบ select-target ที่เรายังไม่ส่ง (RE)

## ต่อไป (เสนอ)
1. สาย B: อัปเดตหัวใบ GT-084/GT-084-R2 ตามผลนี้ (สิทธิ์แก้หัวใบของตัวเองตามใบสั่ง 1405) · เปิดใบ RE 2 ใบ: "client ทำอะไรกับ dying/dead frame ของ 0x201F — animation ใช้ฟิลด์ไหน / ทำไม mesh ค้าง" และ "select-target UI panel ต้องการเฟรมอะไรจากเซิร์ฟเวอร์" · ทบทวน hold 700 ms vs timer 20.0 (วัดจริงก่อนเปลี่ยน)
2. สาย A/B: ทำไมนกโผล่ช้ากว่า NPC ทั้งที่อยู่เฟรมเดียวกัน — เทียบ entry ของ 0x201F กับ NPC ใน WORLD_CENSUS (ฟิลด์ต่าง?) และลองรอบ 2 ว่าเร็วขึ้นไหมเมื่อโมเดล cache แล้ว
3. GT-104 เปิดได้แล้ว (ตายบนสายทำงานกับ 0x201F) แต่ควรรอแก้ "ศพแข็ง" ก่อนเรียกเจ้าของ ไม่งั้นเห็นอาการเดิมซ้ำ
4. ใบเทสถัดไปที่เรียกเจ้าของได้: ยังไม่มี — จนกว่าจะมี fix ให้ดู

## หลักฐาน
คอนโซล L163-165, 255-258, 3167-3188, 8556-8580, 9887, 11198-11205 · outbox\1296_gt084r2_hold_and_resolve.utf8.txt (ด่าน + บริบทโค้ด ctx 4870-4887) · outbox\1294_gt084r2_boot_video.utf8.txt · outbox\1295_gt084r2_teardown_video.out.txt (`GT084_TEARDOWN_VIDEO=PASS`, exit 0, 15:56:48) · LOCK_GAME release 1297
