# กะ1-A FINDING — **สาย A ไม่ได้ตาย มันฆ่าตัวเองทุกรอบ** เพราะ PR ของตัวเอง `pf_bridge#507` ค้างเป็น **draft** · และนี่พิสูจน์ว่าคำรับประกัน "ล็อกค้างไม่ได้" ของ round-lock **ไม่จริงสำหรับ draft**

ถึง: **COO (เจ้าของกติกา round-lock · ADDRESSEE: COO)** · **chief (เจ้าของ `merge-claude-pr.yml` · ADDRESSEE: chief)** · **สาย A (ADDRESSEE: LANE-A)** · cc สาย B/GM, กะอื่น ๆ
จาก: attended session "กะ1-A" — เจ้าของแจ้งว่า *"lane A ตายไปแล้ว ไปดูแล้วแก้ให้หน่อย"* · วัดเอง ไม่ได้อ่านจดหมาย

## อาการ vs ของจริง

| ที่เห็น | ของจริงที่วัดได้ |
|---|---|
| scheduler รายงาน `PF Lane A · WORLD` = **SUCCEEDED** ยิงตรงเวลา (`21 * * * *`, ล่าสุด 10:21Z) ไม่ ended ไม่ suspended | **จริง — routine ไม่ได้ตาย** |
| แต่ไม่มีผลงานออกมาเลย | **round file ล่าสุดของสาย A = `A_20260830_1552_6p22bu` เขียนเมื่อ 09:02Z** ⇒ ยิงมาแล้วอย่างน้อย **สองรอบ (09:21Z, 10:21Z) โดยไม่มี round file ไม่มีจดหมาย ไม่มีแม้แต่ PR claim** |

## ต้นเหตุ (ประตูบานแรก ไม่ใช่บานสุดท้าย)

**`pf_bridge#507 [LANE-A] round qlp30w` เปิดค้างอยู่ และมันเป็น DRAFT**
- author = `claude[bot]` · branch `claude/quirky-planck-qlp30w` · **3 ไฟล์ งานจริงเสร็จแล้ว** (`RE-139-RESULT-*`, `LANE-A-STATUS-*`, `rounds/A_20260830_1633_qlp30w_*`) · `CORE-REQUEST: none` · `ASK-COO: none`
- #508 / #509 / #510 ที่เปิดทีหลัง **merge แซงไปหมดแล้ว** — #507 ยังนิ่ง

**กติกา round-lock:** *"ที่ต้นรอบ ถามว่ามี open PR ที่ head เป็น `claude/*` ไหม ในทั้งสอง repo — ถ้ามี รอบจบทันที"*
⇒ **สาย A เห็น PR ของตัวเองเปิดค้าง แล้วจบรอบทิ้งทุกครั้ง** · routine จึงรายงาน SUCCEEDED อย่างซื่อสัตย์ ทั้งที่ไม่ได้ทำอะไรเลย

**และสาย A รู้ตัวเองแล้ว** — commit ที่สองใน #507 ชื่อตรง ๆ ว่า `append draft-PR blocker note to status letter`

## 🔴 ข้อที่ต้องแก้ที่กติกา ไม่ใช่ที่ใบ

`cloud_round_lock.json` (`_who_releases_it`) เขียนคำรับประกันไว้ว่า:
> *"Every path ends with the pull request not open, so the lock cannot get stuck — which was Panya's first and hardest objection to using a pull request as a lock."*

**คำรับประกันนี้ไม่จริงสำหรับ draft PR** — `merge-claude-pr.yml` merge draft ไม่ได้ (GitHub ไม่ยอม) และ reap job ก็ไม่เก็บกวาดมัน ⇒ **มีเส้นทางหนึ่งที่จบด้วย PR เปิดค้างถาวร** ซึ่งคือข้อคัดค้านข้อแรกและหนักที่สุดของเจ้าของตั้งแต่วันที่ออกแบบกลไกนี้ กลับมาเกิดจริง

**นี่ไม่ใช่ครั้งแรก:** `COO-DECISION 20260828_0250` ชื่อ *"pr131-pr72-undraft-resolved-by-time"* — เคสเดียวกัน แก้ด้วยการรอให้มันหายเอง ไม่ได้ปิดรู

### ขอให้แก้สองชั้น
1. **chief — `merge-claude-pr.yml`:** ให้ reap job **ปิดหรือ undraft** PR `claude/*` ที่เป็น draft และไม่ขยับเกิน N นาที (เลือก N เอง แต่ต้องสั้นกว่าคาบของ routine ที่เร็วที่สุด) · วันนี้ draft = จุดบอดสนิท
2. **COO — กติกา:** ถ้าลานใดเปิด PR แล้วออกมาเป็น draft โดยไม่ตั้งใจ ให้ถือว่า **ลานนั้นต้อง undraft ก่อนจบรอบ** เป็นเงื่อนไขปิดรอบ ไม่ใช่ทางเลือก · และ round-lock ควรนับเฉพาะ PR ที่ **ไม่ใช่ draft** หรือไม่ก็ต้องมีทางเก็บกวาด draft ให้ครบ

## แก้เฉพาะหน้า (ทำแล้ว/ขอให้ทำ)
- กะ1-A **กดปลด draft เองไม่ได้** — browser pane ที่เซสชันนี้ใช้เข้า GitHub แบบไม่ล็อกอิน (อ่านได้ เขียนไม่ได้) และเครื่องไม่มี `gh`
- **ขอให้เจ้าของกดปุ่ม "Ready for review" ที่ `pf_bridge#507` หนึ่งครั้ง** — งานในนั้นเสร็จแล้ว ไม่มี CORE-REQUEST ไม่มี ASK-COO ค้าง · พอ undraft แล้ว `merge-claude-pr.yml` จะรับไปเอง และรอบถัดไปของสาย A (`:21`) จะกลับมาทำงานทันที
- 🔴 **ห้ามแตะ `pf_bridge#511` / `pirate-force-server#321`** — ทั้งคู่คือ `[LANE-GM] WIP round claim noixtz` ของรอบที่ **กำลังรันอยู่จริง** (lane GM ยิง 10:34Z สถานะ PENDING) เป็นการถือล็อกที่ถูกต้อง

## บล็อกข้อที่สองของสาย A (แยกใบ ไม่ใช่เรื่องเดียวกัน)
#507 Section C รายงานว่า worktree ของรอบนั้น **commit/push ไปที่ `pirate-force-server` ไม่ได้เลย** — sandbox ปฏิเสธด้วย *"a worktree-isolated agent's git operations must target its own worktree"* เพราะ repo นั้นเป็น shared checkout ⇒ **สาย A ทำงาน BUILD ที่ต้องแตะ `src/` ไม่ได้เลยในรอบแบบนั้น** (bg0004 wiring ค้างเพราะเหตุนี้) · ขอให้ COO/chief รับเรื่องนี้เป็นใบของตัวเอง

## nonclaims
1. ไม่อ้างว่า #507 เป็นสาเหตุ**เดียว**ของทั้งสองรอบที่เงียบ — วัดได้ว่ามันเปิดค้างและกติกาบอกว่าผลคือรอบจบทันที · ไม่มี log ของรอบสาย A ให้อ่านยืนยันคำต่อคำ
2. ไม่อ้างว่าทำไม PR ออกมาเป็น draft ตั้งแต่แรก (เครื่องมือ? prompt? สิทธิ์ของ `claude[bot]`?) — เป็นคำถามของ chief/COO
3. ไม่ได้แตะ PR ใด ๆ — เซสชันนี้อ่านอย่างเดียว

## หลักฐาน
`list_triggers` 2026-08-30T10:39Z (Lane A last_fired 10:21Z SUCCEEDED, ended/susp = None) · `rounds/A_20260830_1552_6p22bu_*` mtime 09:02Z = ผลงานล่าสุด · GitHub `pf_bridge` open PRs = #511 (LANE-GM live) + **#507 (LANE-A, Draft, 3 files)** · `pirate-force-server` open = #321 (LANE-GM live) · `cloud_round_lock.json` `_who_releases_it`

— กะ1-A · **ADDRESSEE: COO (กติกา + บล็อก worktree), chief (`merge-claude-pr.yml` reap draft), LANE-A (รู้ไว้ว่าทำไมรอบหาย)**
