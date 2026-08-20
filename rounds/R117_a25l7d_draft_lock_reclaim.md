# R117 (a25l7d) — ล็อกรอบถูก merge ทิ้งอีกครั้งตามที่ v5 สั่ง แล้วยึดคืนด้วย draft PR

- **เวลา:** เริ่ม 2026-08-21 06:00 (+07:00) = 2026-08-20 23:00 UTC
- **รันบน:** Claude Code Routine (cloud) · Linux 6.18 x86_64
- **branch รอบนี้:** `pf_bridge` -> `claude/zealous-turing-a25l7d` · `pirate-force-server` -> `claude/quirky-ride-a25l7d`
- **ฐานต้นรอบ:** bridge `dc79c82` (= main หลัง R116 merge)

---

## 1. การ์ดกันรอบซ้อน — ทำตาม v5 เป๊ะ แล้วเสียล็อกอีกรอบ (รอบที่สามของบั๊กเดิม)

ลำดับที่ทำ: `git fetch --all` -> ถาม API -> **PR เปิดค้าง 0 ใบทั้งสอง repo** -> claim commit `97068ee`
"round claim: a25l7d" -> push -> เปิด PR #13 **แบบไม่ใช่ draft ตามตัวอักษรของ v5 ข้อ ①**

**ผล:** PR #13 เปิด 23:00:45Z -> ถูก merge เข้า `main` เป็น `db91887` และ **ปิดภายในไม่ถึงหนึ่งนาที**
⇒ ล็อกหลุดตั้งแต่ยังไม่เริ่มงาน — อาการเดียวกับที่ R115 ขุดเจอและบันทึกไว้แล้ว
(`rounds/R115_pb54cq_draft_lock_fix_and_mailbox_stubs.md` หัวข้อ 1)

**ทำไมแก้ทีหลังไม่ได้:** ลอง `update_pull_request(draft=true)` แล้ว GitHub ปฏิเสธ —
*"panyaasanee does not have permission to convert the pull request to draft"*
⇒ **draft ต้องเป็น draft ตั้งแต่ตอนเปิด** แปลง PR ที่เปิดไปแล้วไม่ได้

**สิ่งที่รอบนี้ทำแทน:** commit งานจริงหนึ่งใบ -> push -> เปิด PR ใบใหม่ **เป็น draft ตั้งแต่แรก** พร้อม marker
`PF-AUTOMERGE: v4` ⇒ ถือล็อกได้ตลอดรอบ (กลไกพิสูจน์แล้วโดย R115: `merge-claude-pr.yml:140` ข้าม draft)

🔴 **ของที่ต้องให้คุณแก้เอง (chief แก้ไม่ได้):** ข้อความ routine prompt ยังเป็น **v5** ซึ่งข้อ ① สั่งให้เปิด PR
แบบธรรมดา ⇒ **ทุกรอบที่รันด้วย v5 จะเสียล็อกช่วงต้นรอบเหมือนกันหมด** จนกว่าจะแก้เป็น v6

---

## 2. ผล PROBE ของรอบนี้

(เติมท้ายรอบ)

## 3. งานของรอบ

(เติมท้ายรอบ)
