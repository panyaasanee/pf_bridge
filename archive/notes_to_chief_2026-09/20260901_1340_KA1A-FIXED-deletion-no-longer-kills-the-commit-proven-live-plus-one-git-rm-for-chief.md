# แก้แล้วและพิสูจน์บนของจริง: การลบหนึ่งไฟล์ไม่ฆ่าทั้ง commit อีกต่อไป · เหลือ `git rm --cached` หนึ่งคำสั่งให้ chief

ADDRESSEE: chief
FROM: ka1-A (เซสชัน attended)
WHEN: 2026-09-01 ~13:40 +07:00 (โดยประมาณ)
สั่งโดย: Panya โดยตรงในแชท ~13:0x — *"แก้ให้การลบหนึ่งไฟล์ไม่ฆ่าทั้ง commit"*
และ *"บอกวิธีแก้ ขั้นที่ 2 จะพังซ้ำ"*

## หลักฐานว่ามันพังซ้ำจริง ภายในชั่วโมงเดียว

ka1-A คืนไฟล์มาร์กเกอร์ตอน ~12:1x และบอกเจ้าของว่ามันจะเกิดซ้ำ **13:36 มันเกิดซ้ำจริง**
routine Codex rename มาร์กเกอร์ตัวเดิมอีกรอบ แล้ว `sync.log` ก็ขึ้น
`refusing the whole commit` เหมือนเดิม นี่ไม่ใช่ความเสี่ยงเชิงทฤษฎีอีกต่อไป

## สิ่งที่แก้ — `pf_git_sync.ps1` บล็อก `[4]`

`Finish 5 'REFUSED_DELETION'` (บายทั้งรอบ) → **ข้ามเฉพาะ path ที่ถูกลบ แล้ว commit ที่เหลือ**

**ทำไมถึงปลอดภัย — invariant "การลบไม่เคยถูก commit" ไม่ได้อยู่ที่บล็อกนี้ และไม่เคยอยู่:**
- path ที่ถูกลบเข้า `$deletions` ไม่เคยเข้า `$candidates`
- index ถูกสร้างใหม่ด้วย `read-tree HEAD` แล้ว `git add` ทีละ path **ตามชื่อ** ไม่มี `add -A`
- หลัง add ยังมีด่าน `git diff --cached --name-status` หา `^D` แล้ว
  `Finish 5 'REFUSED_STAGED_DELETION'` + รีเซ็ต index ถ้าเจอ — **ด่านนั้นไม่ถูกแตะเลย**

บล็อกนี้ตัดสินแค่ว่า "path ที่ถูกข้ามหนึ่งอัน มีสิทธิ์ยกเลิกของสะอาดที่ยืนอยู่ข้าง ๆ ด้วยไหม"
คำตอบเป็นอันเดียวกับที่ **โปรเจกต์นี้เคยตัดสินไปแล้วเมื่อ 2026-08-24** สำหรับด่าน size/proprietary
ที่อยู่ถัดลงไปสิบบรรทัด และคอมเมนต์ของมันเขียนไว้เองว่า:

> *"Skipping ONLY the offending paths is strictly safer - the bad file still never
> reaches the remote and everything clean keeps moving. The guard is per-file, so
> per-file is honest."*

ka1-A ไม่ได้คิดนโยบายใหม่ แค่เอากฎที่ตัดสินไปแล้วมาใช้กับกิ่งสุดท้ายที่ตกหล่น

## พิสูจน์บนของจริง ไม่ใช่คำอ้าง

จ็อบ `1408` (อ่านอย่างเดียว): `PARSE_OK tokens=5479` · `NONASCII=0` ·
`-SelfCheck` รันผ่าน `candidates=35 deletions=1 refusals=25`

แล้วรอบสด 13:38 ของ scheduled task เอง:

    [4]  candidates after the guard: 10
    [4]  committed 10 path(s)
    [4]  pushed 1 commit(s)
    [7]  heartbeat  OK  committed=10 newletters=0 deletions_skipped=1

**มีการลบอยู่ (`deletions_skipped=1`) และ commit ผ่าน** — คือพฤติกรรมที่สั่งเป๊ะ

## สิ่งที่ยอมรับและบันทึกไว้ตรง ๆ

- **rename จะทำให้ main มีสองชื่อชั่วคราว** (ชื่อใหม่ commit ขึ้นไป ชื่อเก่ายังอยู่)
  = ของซ้ำที่มองเห็นได้ ไม่ใช่ข้อมูลหาย และหายเองเมื่อมีคน commit การลบอย่างตั้งใจ
- **ตกค้างโดยตั้งใจ**: verdict ของ `-SelfCheck` (บรรทัด ~503) ยังขึ้น
  `SELFCHECK_WOULD_REFUSE` เมื่อมีแค่การลบ ตอนนี้มันแค่ **มองโลกในแง่ร้ายเกินจริง** ไม่ใช่ผิด
  ka1-A ไม่แก้ในเอดิตเดียวกันเพราะมันมีผู้บริโภคที่ยังไม่ได้ตรวจ (เช่น `1178_verify_watchdog_sync_check`)
  **chief ตัดสินแยกเอง**
- `verdict` ยังเป็น `OK` เมื่อ commit สำเร็จ **โดยตั้งใจ** — การลบกลายเป็นเหตุการณ์ปกติที่เกิดทุกครั้ง
  ที่เจ้าของเทสเกม ถ้าให้มันเปลี่ยน verdict ตัวเฝ้าระวังจะเด้งเข้ามือถือเธอทุกครั้ง = เสียงรบกวน
  จำนวนอยู่ในโน้ต `deletions_skipped=N` และใน `sync.log` ครบ

## เหลือให้ chief ทำ: หนึ่งคำสั่ง แล้วมาร์กเกอร์จะหายไปเลย

    git rm --cached notes_to_chief/reference_codex_attr/.skipped_for_game_lock
    git rm --cached "notes_to_chief/reference_codex_attr/.skipped_for_game_lock.done.*"

🔴 **ห้ามทำโดยไม่มี pattern ใน `.gitignore`** — ka1-A ใส่ pattern ไปแล้ว (พร้อมคอมเมนต์ว่ามันเฉื่อย
จนกว่าจะมีคนสั่ง `git rm --cached`) เหตุผลคือกับดักตรงนี้: `notes_to_chief` อยู่ใน **ALLOWLIST**
ซึ่ง**พาไฟล์ untracked ไปด้วย** ⇒ untrack เฉย ๆ โดยไม่ ignore = sync จะ add มันกลับเข้าไปใหม่
ในรอบถัดไป วนไม่จบ ต้องทำสองอย่างคู่กันเสมอ

หลังจากนั้น `deletions_skipped` จะกลับเป็น 0 และจะไม่มีไฟล์ `.done.<stamp>` งอกบน main
เพิ่มขึ้นเรื่อย ๆ ทุกครั้งที่เจ้าของเทสเกมอีก

## NONCLAIM

- ไม่ได้รัน `pf_git_sync_selftest.ps1` ตัวเต็ม (39 KB ยังไม่ได้ตรวจว่ามันแตะ fixture อะไรบ้าง)
  พิสูจน์ด้วย parse + `-SelfCheck` + รอบสดจริงหนึ่งรอบเท่านั้น
- ไม่ได้ทดสอบเคส "ลบไฟล์ที่ควรลบจริง ๆ" ว่าตอนนี้มันจะค้างเป็น skipped ตลอดไปหรือไม่
  — ตามโค้ดคือใช่ และนั่นคือเจตนา แต่ไม่มีใครวัด
- ka1-A ไม่ได้ commit อะไรเอง ตามกฎบ้าน ทุกอย่างข้างบนไหลขึ้น main ผ่าน pf_git_sync เอง
  เพราะ `pf_git_sync.ps1` และ `.gitignore` อยู่ใน `SHARED_TRACKED` อยู่แล้ว
