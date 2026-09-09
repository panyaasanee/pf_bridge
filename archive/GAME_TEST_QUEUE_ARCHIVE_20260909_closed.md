# GAME_TEST_QUEUE archive — closed 2026-09-09 (moved by LANE-K round ajt28l)

## GT-186 UI-B-REAL-LOGOUT-BUTTON-001  [🟠 **RE-266 ANSWERED — BOUNDED-NEGATIVE / STATIC ANSWERED, ปิดใน `archive/CLIENT_RE_QUEUE_ARCHIVE_20260907_closed.md`** — พับโดย LANE-K รอบ `ci8200` 2026-09-08T17:xx+07:00 ตาม PANYA `1520` ข้อ 1 / `COO-DECISION 20260908_1642 gt186-label-flip-and-gt185-fact-correction` คำต่อคำจากบรรทัดสถานะของจดหมายผล `notes_to_chief/20260905_2242_RE-266-RESULT-NO-DIRECT-SELECT-UI-NO-GETWORLD-REPLY-FLAG.md`: "สถานะ: BOUNDED-NEGATIVE / STATIC ANSWERED (ไม่เขียน DONE เพราะไม่มี client-observable ตามเกณฑ์ใบ)" · ผลลบแบบมีขอบเขต: static ไม่พบเส้นทางในไคลเอนต์ที่ true branch ของ `0x709E` เรียกเปิด UI/หน้าเลือกตัวละครตรง ๆ (apply gate บังคับ `cStateCreateActor` อยู่แล้วก่อนเข้าทางนี้ -- ไม่ใช่เส้นที่ HOME ใช้) และ `GetWorldInfoVital 0x3D4B` R-side natural handler ไม่มี pending-reply/ack flag ใด ๆ · BUILD_IMPACT ของจดหมายผล: "ห้าม retry `0x709E` จาก HOME ด้วย payload tweak" · 🔴 **NEEDS-NEW-BODY: LANE-UI** — ผลลบนี้ปิดทางที่เนื้อใบเดิมวางแผนไว้ (retry `0x709E` หวังเปิด dialog ต่อจาก push) เป็นทางตันที่วัดแล้ว K ไม่เขียนเนื้อใบใหม่เอง (นอกเขต) ส่งจดหมายใบเดียวถึง LANE-UI ให้เขียนวัตถุประสงค์ใหม่ก่อนขึ้นคิวบูตอีกครั้ง · ป้าย `BLOCKED-ON-RE-266` เดิมถอดแล้ว (RE-266 มีผลแล้ว ไม่ได้ block รออีกต่อไป)] [🟠 ประวัติป้ายเดิมก่อนพับ (ไม่ลบ): ~~🔴 **BLOCKED-ON-RE-266 (historical label text, hyphens intentionally non-ASCII so this archived quote does not match a literal grep for the retired ASCII label -- see the live status above)** -- ป้ายเดิม `BLOCKED-ON-WIRING` เปลี่ยนโดย chief (LANE-E) รอบ `rz1fxh`/R358 ตาม `COO-DECISION 20260905_1352` ข้อ 4 และ `20260905_1845` ข้อ 4 (ถ้อยคำ = chief · LANE-UI เสนอมาใน `20260905_1405`) · **ตัวบล็อกไม่ใช่ "ยังไม่ได้ต่อสาย" อีกแล้ว มันถูกต่อและวัดแล้วว่าไม่พอ**: R311 + R319 NEGATIVE -- push `0x709E` ก่อน ACK ไม่พา client เปลี่ยนหน้า (R319 13:47 วัดสด ไบต์ออกจริง 2/2 หลัง `GetWorldInfoVital` แต่จอไม่เปลี่ยน ⇒ HYP-PF-040 FALSIFIED) · เกตของ `0x709E` เองปิดตอบแล้วโดย `RE-075` (state gate `cStateCreateActor` + field gate `vital+0x14==0x1E` · payload ศูนย์ล้วนของ R319 ตกเกตชั้น 2 แน่นอน และตกชั้น 1 อยู่ดีเพราะ client อยู่ HOME ไม่ใช่หน้าสร้างตัวละคร) · **ตัวบล็อกที่เหลือ = `RE-266`** (downstream ของเกตที่ผ่าน + `GetWorldInfoVital 0x3D4B` reply-wait) · 🔴 **ห้ามบูตซ้ำจนกว่า `RE-266` จะชี้ทางใหม่** (`1352` ข้อ 2) · ใบนี้ออกจากหมวด "รอเครื่องคุณ" แล้ว -- มันรอผล RE ไม่ได้รอผู้เทส · **PANYA-ORDER `20260905_1911` (COO `1948`): LANE-UI งานแรกคือ UI-B ล็อกเอาต์จริง headless เป็น PR เซิร์ฟเวอร์ ก่อนใบ RE ใหม่ทุกใบ** -- ใบนี้ไม่ใช่ข้ออ้างให้ไม่มี PR · ประวัติเดิมไม่ลบ ต่อท้ายทันที: รันแล้ว R311 (`notes_to_chief/20260904_1931_KA1A-R311-RESULTS-*`) = **NEGATIVE / hypothesis not exercised**: ปุ่ม "ออกจากเกม" ส่ง `GetWorldInfoVital 0x3D4B` เต็ม 268 B (เซิร์ฟไม่ตอบ) แล้ว `0x1B40` subcode 01 → `HYP_PF_013_LOGOUT_SUBCODE01_ACK_THEN_SERVER_SOCKET_CLOSE` 46 B แล้วปิด socket · จอไม่เปลี่ยน ไม่มีข้อความ 90 วิ (ภาพ `20260904_192633.png`) · `OBSERVER_CONFIRMED: 2026-09-04T19:26+07:00` · 🔴 **push `0x709E` ของ scenario `logout_hypothesis_dialog_open_push` ไม่เคยออกจากเซิร์ฟเวอร์** (ไม่มี `[G>]` เฟรมนั้นทั้งรอบ) ⇒ ยังตัดสิน HYP-PF-040 ไม่ได้ · ห้ามบูตซ้ำจนกว่า **LANE-UI** จะแก้ให้ push ออกจริง (รันใหม่ ~6 นาที) · ป้ายเขียนโดย chief (LANE-E) รอบ `t7bsfx`/R342 ตาม `COO-DECISION 20260904_1948` ข้อ 5~~] [ประวัติป้ายเดิม] [BLOCKED -- branch-6 (dialog-open unsolicited 0x709E push) module built round `bkgaq8`, `pirate-force-server` PR `#471`: src/pirateforce_foundation/logout_dialog_open_hypothesis.py, not wired into runtime.py yet. CORE-REQUEST open in this letter's own round file/letter for chief to wire; production_allowed stays False until wired + re-read by pf-adversary once more. Do not boot this ticket until wiring lands on main] [STALE as of round `tmizmk` 2026-09-01T15:58+07:00 -- wiring landed round `liq4ri` (PR #476); sixth allowlist profile landed round `tmizmk` (PR pending merge). Boot now with `--logout-hypothesis-scenario scenarios/logout_hypothesis_dialog_open_push.json`. `production_allowed` still False, unchanged -- stop_rule still requires an attended GT-184/GT-186 pass first. Ready for attended capture.] [MEASURED, round `2ahq88` 2026-09-01T16:35+07:00 -- "PR pending merge" above is stale: `pull_request_read get` confirms `pirate-force-server#484` merged=true (merged_at 2026-09-01T09:17:06Z) and `pf_bridge#724` merged=true (merged_at 2026-09-01T09:08:21Z). Sixth allowlist profile is on `main` now, not pending. No other change to this ticket's status -- still awaiting attended capture.] [🔴 **SUPERSEDED-BY: GT-308** — ถอนออกจากคิวรถบัส ตาม `COO-DECISION 20260908_1943_COO-DECISION-retire-gt186-and-hold-gt184-for-a-mechanism-LANE-K.md` ข้อ 1 คำต่อคำ (LANE-K รอบ `g3nkno` 2026-09-09T14:25+07:00) — เหตุ: `GT-308` ถามคำถามเดียวกัน (กดปุ่มออกจากเกมแล้วเกิดอะไร) บนกลไกที่มีจริงบน main พร้อม `HEADLESS_PROOF:` สด · กฎ `0159` "ผลใหม่ครอบ = ถอน" · 🔴 ไม่มี `tickets/GT-186.md` แยก (หัวใบยังอยู่ใต้เพดาน 8,192 B) — ป้ายนี้จึงวางไว้ที่หัวใบนี้เอง ไม่ใช่ไฟล์ `tickets/` ตามที่โทเคนตรวจของ COO สมมติไว้ · ยกให้ COO ยืนยันในไฟล์รอบ]

> Opened by chief this round, directly per Panya's order, same provenance as `GT-182`.
> Source: PANYA-ORDER `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` section 3 (UI-B: "a
> real logout button, distinct from the X close-window button, must work"). Build-owner
> lane: **LANE-A** per chief's broadcast letter this round.

- objective: single claim -- clicking the HOME-menu "ออกจากเกม" (exit/quit) control while
  in a live map ends the session cleanly and takes the client itself out of the game
  (screen changes away from the map and/or the client process exits on its own), as a
  genuine alternative to forcibly closing the window with the OS-level X button. `GT-033`
  already measured this exact button (subcode 01 of `LogoutVital 0x1B40`) under variant A
  (ack + close-socket) and found the client's own process did NOT exit on its own within
  the observation window; variant B (adding `ReturnSelectServerVital` first) was
  deliberately NOT run against subcode 01. This entry is scoped to whatever NEW mechanism
  the implementing lane builds, not a repeat of variant A.
- background (read before running):
  - `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` GT-033 RESULT block, subcode-01
    column specifically: variant A measured, process did not exit on its own; variant B
    subcode 01 explicitly NOT measured -- if the implementing lane's fix is close to
    variant B in shape, running that untested cell for the first time here would itself be
    new information, not a repeat.
  - Distinguish this from `GT-184`/`GT-185`: those are about the "back to character
    select" -> "back into game" round trip. This entry is about actually LEAVING/ending
    the client session as a deliberate, clean alternative to the destructive X-kill.
- db: fresh copy of `state\pirateforce.sqlite3` (never canonical) -- record filename +
  sha256 before/after; verify canonical file's sha256 unchanged.
- server args: standard boot, `-SecondPasswordMode bypass`. Requires whatever new
  response/sequence the implementing lane builds for the exit path; if the fix is shared
  code with `GT-184`'s fix, say so explicitly in this entry's result and cross-reference,
  but still test this button and this subcode separately.
- steps:
  1. Boot per standard playbook; confirm server up first; confirm fresh server (not reused
     after a killed client).
  2. Log in normally. Right-click-drag camera only for a clean baseline view. Screenshot
     BASELINE, full resolution, record every name label's colour (one per line, "none" if
     empty).
  3. Open the HOME menu, click "ออกจากเกม" (exit/quit -- record the exact label text
     seen). Note the wall-clock time.
  4. Watch continuously for at least 90 seconds. Screenshot at +5s, +30s, +60s, +90s,
     labelled STEP-A through STEP-D. Record at each: is the client window still open, is
     it still showing the map, has any dialog/disconnect-notice appeared, and (if the
     window is still open and showing name labels) every name label's colour.
  5. If the client process exits on its own at any point, record the exact wall-clock time
     it happened relative to the click in step 3.
  6. If the client is still sitting on the same map screen after 90 seconds with no change
     of any kind, this is the negative result this entry is built to catch.
- pass criteria (two layers, kept separate):
    wire/DB: server console/capture log shows the `LogoutVital 0x1B40` subcode-01 request
      arriving AND `sessions.closed_at` being written server-side AND whatever new
      response frame(s) the implementing lane sends, logged with a distinct, greppable
      token.
    client-observable: does the human watching the screen see the client actually leave
      the map -- either the process exits on its own, or the screen changes to something
      that clearly indicates a completed logout -- within the 90-second window, without
      the tester needing to close the window with X.
- nonclaims:
  1. Does not test the "back to character select" button or `LogoutVital` subcode 03 --
     that is `GT-184`, a separate claim, even if it turns out to share implementation code.
  2. Does not test what a killed/X-closed client looks like server-side.
  3. Does not claim any existing teardown-template age limit changes because of this
     entry's result either way.
  4. Does not attribute a negative result to any specific untested branch from `GT-033`'s
     six-branches list without first checking whether the implementing lane's fix actually
     touches that branch.
- RECHECK: `cd pirate-force-server && git log --all --oneline -i --grep="UI-B" --grep="logout" --grep="GT-186" | head -5`
  (empty output = still BLOCKED-ON-WIRING).
- links: `notes_to_chief/20260901_0215_PANYA-ORDER-*.md` (section 3, UI-B) --
  `archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` (GT-033 full result, subcode-01
  column) -- `GT-184` (sibling UI ticket, different subcode) -- `PROCESS_GATES.md` rule #18.
- numbering: see `GT-182`'s numbering note. This entry is `186`.
- result: (tester/build lane fills in: PASS/FAIL/BLOCKED, evidence, timestamp,
  OBSERVER_CONFIRMED line per G-OBS once client-observable evidence exists)

