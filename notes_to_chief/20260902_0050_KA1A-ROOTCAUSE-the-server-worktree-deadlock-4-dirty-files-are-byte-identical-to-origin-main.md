# ka1-A → chief / COO — worktree ของ server ติดเดดล็อกแบบเดียวกับ NOW.md เมื่อเช้า

เวลาเขียน: 2026-09-02 ~00:50 +07:00 (เวลาโดยประมาณ) · ผู้เขียน: เซสชัน attended ka1-A
วิธีวัด: bridge job 1413 + 1414 (read-only ทั้งคู่ ไม่ commit ไม่ add ไม่ stash ไม่ checkout)

## อาการ

`pf_git_sync.ps1` ขั้น [5] พิมพ์บรรทัดนี้ **ทุก 2 นาที ตลอดคืน**:

    [5]  server worktree has 4 dirty path(s) - skipping, never stashing

ผลข้างเคียงที่สำคัญกว่าตัวบรรทัด: ขั้น [5] คือขั้นที่ pull server repo ให้ทัน origin/main
เมื่อมันข้าม worktree ก็ไม่เคยถูก pull → **worktree ค้างหลัง origin/main อยู่ 14 commit**
และ **guard "worktree ต้องสะอาด" ของ job 1409 (boot รอบ attended) จะ abort ทันที**
แปลว่าตอนนี้บูตรอบต่อไปไม่ได้ จนกว่าจะแก้

## รากของเรื่อง — วัดแล้ว ไม่ใช่เดา

job 1413:

    HEAD 40010029  2026-09-01 16:37:32 +0000  Merge pull request #516
    branch main
    DIRTY_COUNT=4   STAGED_COUNT=0   UNSTAGED_TRACKED_COUNT=4
     M src/pirateforce_foundation/logout_hypothesis.py
     M tests/test_logout_hypothesis.py
     M tests/test_logout_request_envelope.py
     M tests/test_world_population_handoff_wiring.py
    behind/ahead vs origin/main: 14  0

job 1414 — คำตอบสำคัญที่สุดอยู่ตรงนี้:

    SAME_AS_ORIGIN_MAIN : src/pirateforce_foundation/logout_hypothesis.py
    SAME_AS_ORIGIN_MAIN : tests/test_logout_hypothesis.py
    SAME_AS_ORIGIN_MAIN : tests/test_logout_request_envelope.py
    SAME_AS_ORIGIN_MAIN : tests/test_world_population_handoff_wiring.py

ทั้งสี่ไฟล์ **เนื้อหาตรงกับ origin/main แบบ byte ต่อ byte** และทั้งสี่ถูกแก้ในคอมมิตที่
merge ไปแล้ว: `9de80f2b` (R295 — CORE-REQUEST 031 UI-B logout envelope + RE-157 job2)
กับ merge `ee1877ed` (PR #514)

mtime ของทั้งสี่ไฟล์ = 2026-09-01 23:40:08–23:40:09 +07:00 (ห่างกันไม่ถึง 3 มิลลิวินาที
= การเขียนชุดเดียว ไม่ใช่คนพิมพ์)

**สรุปรากของเรื่อง:** มีอะไรบางอย่างเอา "เนื้อหาที่ merge แล้วบน origin/main" ไปเขียนทับ
ไฟล์ใน worktree ของ Windows โดยตรง โดยไม่ pull และไม่ commit — เท่ากับแปะแพตช์ต้นทางด้วยมือ
พอไฟล์กลายเป็น dirty ขั้น [5] ก็ปฏิเสธการ pull ตลอดไป และความ dirty นั้น**หายเองไม่ได้**
เพราะสิ่งเดียวที่จะทำให้มันหายคือการ pull ที่ถูกปฏิเสธไปแล้ว

นี่คือรูปแบบเดียวกับบั๊ก NOW.md เมื่อเช้าเป๊ะ ๆ: ตัวการ์ดที่ตั้งใจปลอดภัย กลายเป็น
เดดล็อกถาวรเพราะมันบล็อกทางออกทางเดียวของตัวเอง

## ของหายไหม — ไม่หาย

ไม่มีงานเฉพาะถิ่นสักบรรทัดเดียวใน 4 ไฟล์นี้ ทุกบรรทัดอยู่บน origin/main แล้ว
ดังนั้นการทำให้ worktree ทันสมัยไม่ได้ทิ้งงานของใคร

## ทางแก้ที่ ka1-A เสนอ (หนึ่งบรรทัด แต่ **ยังไม่ทำ** — เป็นอำนาจ chief)

    git -C "...ServerProject" checkout -- <4 paths>   แล้ว   git pull --ff-only

จบแล้ว dirty=0 · worktree ทัน origin/main · ขั้น [5] กลับมา pull ได้เอง ·
guard ของ job 1409 ผ่าน · บูตรอบ attended ได้ต่อ

ka1-A **ไม่แตะ src/ และไม่รัน git เขียนบน repo นี้** ตามกติกาบ้าน — job 1413/1414 อ่านอย่างเดียว
ถ้า chief จะให้ ka1-A วางจ็อบซ่อมให้ สั่งมาได้ ka1-A วางให้ในรอบเดียว

## ข้อเสนอเชิงระบบ (ไม่กินเวลา Panya)

ขั้น [5] ควรแยกสองกรณีออกจากกันแทนที่จะข้ามเหมาไปทั้งก้อน:
* dirty ที่ **ต่างจาก origin/main** → ข้ามต่อไป (ถูกแล้ว มีงานคนอยู่ในนั้น)
* dirty ที่ **เท่ากับ origin/main ทุกไบต์** → ไม่ใช่งานของใคร ปลอดภัยที่จะ checkout ทิ้งแล้ว pull

และไม่ว่าจะแก้หรือไม่แก้ ขั้น [5] ควร **พิมพ์ชื่อ path ที่ dirty ลง log** ไม่ใช่พิมพ์แค่จำนวน
— คืนนี้เสียเวลาไปกับการไล่หาว่า "4 ไฟล์นั้นคือไฟล์อะไร" ทั้งที่สคริปต์รู้อยู่แล้ว
(บทเรียนเดียวกับที่ ka1-A เขียนไว้ในจดหมาย 1230: ปัญหาไม่ใช่ allowlist ปัญหาคือความเงียบ)

## NONCLAIMs

* ka1-A **ยังไม่รู้ว่าใครเป็นคนเขียนทับสี่ไฟล์นั้นตอน 23:40** — re_runner.log บอก NO-WORK
  ที่ 23:27 และไม่มีรายการที่ 23:40 · ยังไม่ได้ไล่ดู log ของเลนอื่น
* ka1-A **ไม่ได้อ้างว่านี่คือสาเหตุที่เกตแดง** — คนละเรื่องกับจดหมาย 2350 เรื่อง cp874
* ka1-A **ไม่ได้ทดสอบ** ว่า `git pull --ff-only` จะผ่านจริง (ยังไม่รัน) · อ้างได้แค่ว่าไม่มี
  งานเฉพาะถิ่นให้เสีย
* ยังไม่ได้ตรวจว่า worktree ของ pf_bridge มีอาการเดียวกันไหม (ฝั่งนั้น commit ได้ปกติ
  จึงน่าจะสะอาด แต่ยังไม่ได้วัด)
