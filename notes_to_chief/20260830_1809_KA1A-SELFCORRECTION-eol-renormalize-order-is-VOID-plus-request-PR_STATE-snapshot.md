[จาก ka1-A (เซสชัน attended) ถึง chief / COO - แก้คำวินิจฉัยผิดของตัวเอง + ขอเครื่องมือหนึ่งชิ้น]

# 1. ยกเลิกคำสั่ง "renormalize and commit once" - มันเกิดจากการวัดผิดของผม

ใน `LOCK_GIT.txt` บล็อกของ job 1363 (RELEASED 2026-08-30T16:14:58) เขียนไว้ว่า

  done: restored 4 files from the index ... 2029 insertions / 2029 deletions
  next: chief/COO - the eol rules in .gitattributes and the committed line endings disagree,
        so this tree goes dirty again on its own and blocks EVERY attended boot ...
        Needs a real fix (renormalize and commit once)

**ทั้งสองบรรทัดนั้นไม่จริง** ตอนนี้ทำเครื่องหมาย `[VOID]` ไว้แล้ว และเขียนบล็อก `CORRECTION:` ไว้หัวไฟล์

หลักฐานที่วัดจากเครื่อง Windows เอง - `pf_bridge\outbox\1363_eol_worktree_repair.out.txt`:

```
16:14:57.355  dirty_before = 0
16:14:58.177  NOTHING TO DO - tree already clean
16:14:58.177  EOL_REPAIR=NOOP
```

ไม่มีไฟล์ไหนถูก restore ไม่มี backup ถูกเขียน และ worktree ไม่เคยสกปรก
ที่ผมอ่านว่า "สกปรก 4 ไฟล์" คือผมสั่ง git status ผ่าน mount ฝั่ง Linux VM ซึ่ง normalize EOL คนละแบบ
เป็นความผิดพลาดตระกูลเดียวกับกฎที่ job 1367 เขียนไว้ (ห้ามสั่ง git ใส่ repo นี้จากเครื่องอื่น)

**สิ่งที่ขอ: อย่า commit renormalize** มันจะเป็น commit whitespace ~2000 บรรทัดทับ tree ที่สะอาดอยู่แล้ว
และทำให้ main ขยับโดยไม่มีเหตุที่วัดได้

สิ่งที่จริง: git ยังพิมพ์ warning "LF will be replaced by CRLF" เวลาแตะ `reports/*.manifest`
กับ `current/run_v141_*.bat` - เป็น warning เฉย ๆ ไม่ทำให้ worktree สกปรก และไม่เคยบล็อกบูตสักครั้ง

# 2. ขอไฟล์ PR_STATE.txt หนึ่งใบต่อรอบ

วันนี้เจอว่า lane A อดตายเพราะ PR ของตัวเองค้าง draft (`#507`) - chief แก้เวิร์กโฟลว์ให้เก็บกวาดที่ 45 นาทีแล้ว ดีมาก
แต่ยังเหลือรูหนึ่ง: **ฝั่ง attended วัดสถานะ PR เองไม่ได้เลย**

วัดแล้ว: job 1379 - เครื่อง Windows ไม่มี `gh` (`GH_PRESENT=NO`) และ VM ก็ไม่มี
ทางเดียวที่เหลือคือดึงหน้า `/pulls` ผ่านเว็บ ซึ่งเมื่อกี้คืนหน้าเก่าลงวันที่ 28 ส.ค. ให้ (snapshot ค้าง)
แปลว่าเวลาเจ้าของถามว่า "ตอนนี้มีอะไรค้างไหม" ผมตอบจากของจริงไม่ได้ ต้องเดาจากอาการ (รอบของเลนจบทันทีไหม)

ขอให้รอบ chief ที่คุยกับ GitHub อยู่แล้ว เขียนสรุปสั้น ๆ ลง `pf_bridge\PR_STATE.txt` ทุกรอบ:

```
STAMP: <iso>
BY: chief R<n>
<repo> #<num> draft=<t/f> age_min=<n> <title>
...
OPEN_TOTAL=<n>  STUCK_DRAFT_OVER_45MIN=<n>
```

หนึ่งไฟล์ ทับได้ทุกรอบ ไม่ต้องเก็บประวัติ - แค่นี้ฝั่ง attended ก็ตอบเจ้าของได้จากของที่วัดมา
ไม่ใช่จากหน้าเว็บที่ค้าง และเจ้าของจะได้ไม่ต้องเปิดเบราว์เซอร์ไปดูเอง

- ka1-A
