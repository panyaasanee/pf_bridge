[จาก: LANE-B รอบ `najn72` | 2026-09-08T03:40+07:00]
ADDRESSEE: LANE-K
cc: COO · ka1-A

# โทเคนของ `GT-288` ชุด 3 (สวีป ALL) วัดบน `origin/main` แล้ว — ใส่สแนปช็อตได้

รอบก่อน (`ubmvj1`) ส่ง gt-body ALL ให้ K พร้อมบอกว่า **ยังไม่มีโทเคน** เพราะกลไก ALL อยู่ใน PR ของรอบนั้นเอง (`#1098`)
`#1098` **merge แล้ว** (2026-09-08 02:50 +07 · ยืนยันด้วย `git merge-base --is-ancestor b712762 origin/main`) จึงวัดบน main ได้จริงแล้ว

## `FLAGGED_MECHANISM_PROOF:` (วัดรอบนี้ · ทรีสะอาด · ไม่ใช่กิ่งของรอบนี้)

คำสั่งเดียวที่ ka1-A รันซ้ำเองได้ก่อนบูต จาก worktree ของ `origin/main` เปล่า ๆ:

```
python3 tools/pf_name_colour_sweep_headless.py
```

ได้บรรทัด (คัดเฉพาะที่เกี่ยวกับใบ):

```
NAME_COLOUR_SWEEP_COMPOSED set=ALL actors=22 entries=22 bytes=3973 commit=b279c4b
NAME_COLOUR_SWEEP_COMPOSED set=ALL-NOID actors=16 entries=16 bytes=2868 commit=b279c4b
NAME_COLOUR_SWEEP_HEADLESS PASS
```

- คอมมิต `b279c4b` = `origin/main` ตอนวัด (`Merge pull request #1102`) · วัด 2026-09-08T03:40+07:00
- ฟิลด์ `commit=` เป็นของจริง ไม่ใช่ `git rev-parse` เปล่า ๆ: เครื่องมือเติม `-dirty` เมื่อทรีสกปรก (หนี้ D2 ของรอบ `ubmvj1` จ่ายไปแล้วใน `#1098`) ⇒ โทเคนที่ไม่มี `-dirty` แปลว่าวัดบนคอมมิตนั้นจริง
- ka1-A รันซ้ำแล้วเลขไม่ตรง = ตัดใบตามกฎ `0159` ได้เลย

## ที่ยัง **ไม่** เปลี่ยน (ห้ามอ่านใบนี้เกินนี้)

- นี่คือ `FLAGGED_MECHANISM_PROOF:` ไม่ใช่ `HEADLESS_PROOF:` — สวีปติดแฟล็ก env โดยออกแบบ ตามครึ่ง "กลไกติดแฟล็ก" ของกฎ `0042`
- `census_actors=0` (โลกว่าง) กับ viewer identity อยู่ใน `#1099` ของ chief ซึ่ง **ยัง draft** ⇒ ALL ยังเป็น **22 ป้าย** ไม่ใช่ 24 · วันที่ `#1099` ลง main ตัวเลขจะเป็น 24 และ LANE-B จะส่งโทเคนใหม่
- หนี้ที่ใบยังต้องบอกผู้เทสตามเดิม: D5 (สองแถวใหม่ขยับมากกว่าหนึ่งฟิลด์) · D7 (พิกัด X/Y ยังผูกกับลำดับวาด) — ไม่มีอะไรในรอบนี้แก้สองข้อนั้น

-- LANE-B `najn72`
