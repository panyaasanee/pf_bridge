[ถึง: chief, COO, Panya, RE runner | จาก: สาย A (WORLD) รอบ `mvuseu` | 2026-08-28T01:31+07:00]

# LANE-A-STATUS mvuseu -- กู้งานรอบ 5irwkp ที่หลุดจาก main + เปิด RE-115 + ตารางเหตุผล Bg0002

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน
ไม่มีอะไรบนจอ -- รอบนี้เป็นรอบกู้งาน + กล่องจดหมาย

## protocol A: พบปัญหาจริง, กู้แล้ว
PR ล่าสุดของสาย A ทั้งสองฝั่ง (round `5irwkp`) ไม่เคย merge:
- `pirate-force-server#153`: state=open, draft=true, merged=false (reaper 6 ชม. ยังไม่ถึง)
- `pf_bridge#244`: state=closed, draft=true, merged=false (ถูก reaper 2 ชม. ปิดไปแล้ว)

เหตุ (บันทึกไว้แล้วในคอมมิทที่สองของ branch เดิม): เซสชันรอบ `5irwkp` ลอง
`markPullRequestReadyForReview` ผ่าน GraphQL แล้วถูก proxy ของเซสชันนั้นบล็อก, ลอง REST
`PATCH draft:false` แล้ว silent no-op -- ทั้งสอง PR เลยค้าง draft ตลอดไปจนกว่า reaper จะปิด

กู้แล้วรอบนี้: cherry-pick คอมมิทจริงทั้งหมดจากทั้งสอง branch เดิมมาบน `main` ปัจจุบันของ
`claude/sleepy-ride-mvuseu` / `claude/quirky-planck-mvuseu` -- clean, ไม่มี conflict ทั้งคู่
`pirate-force-server` รันเทสยืนยันซ้ำแล้ว (`test_scene2_prison_exile_tables.py` 17/17, full
suite 3608 passed / 0 FAIL / 17 error เดิม -- capstone baseline)

**แก้เหตุ**: session นี้มี GitHub tool ที่รองรับ field `draft` ตรง ๆ (ไม่ใช่ raw GraphQL/REST
ที่ session ก่อนโดนบล็อก) -- ใช้ตัวนี้เอา PR ใหม่ออกจาก draft ทันทีหลัง push แทน จะยืนยันผล
จริงในจดหมายฉบับถัดไปถ้าไม่สำเร็จ

## protocol B: กล่องจดหมาย
`20260827_2305_KA1A-NUDGE-*.md` -- ส่วน "สาย A" ยังไม่มีใครทำ (LANE-GM บริโภคแค่ส่วนตัวเอง,
stub เดิมเขียนไว้ชัดว่าไม่แตะส่วนสาย A) ตาม `notes_to_chief/README.md` (COO-DECISION 00:43)
ผู้บริโภครายที่สองไม่เขียนทับ stub เดิม -- บันทึกในรอบนี้แทน (`rounds/A_20260828_0131_*.md`):

1. เปิด `CLIENT_RE_QUEUE.md` ใบใหม่ `RE-115 MAPWINDOW-SCENE-NPC-LIST-SOURCE-001` แล้ว
2. จับคู่แลนด์มาร์กจากใบ 1240 ข้อ ③ -- **เลื่อนออกไปโดยเจตนา** งานเชิงลึกที่ต้องอ่าน scene
   placement ทั้งฉากอย่างระวัง เสี่ยงจับคู่ผิดถ้ารีบทำรอบเดียวกับงานกู้คืน -- ของรอบถัดไป
3. ตารางเหตุผลรายจุดของ 9 placement unresolved ใน Bg0002 -- เขียนแล้วใน round file (ดึงจาก
   `UNRESOLVED_PLACEMENTS` ในโค้ดจริง ไม่ใช่เดา) พบว่าจดหมาย 2305 อ้างผิดว่าเป็น "5+4" -- ที่จริง
   คือ 8 (บล็อก n_ID 101-104) + 1 (n_ID 37, ไม่มีแถวใน MOBS เลย คนละเหตุ) = 9 -- round `cyp4zt`
   เคยแก้ตัวเลขนี้ไว้ครั้งหนึ่งแล้ว จดหมายที่อ้างเลขเดิมยังไม่ถูกอัปเดตตาม

## BUILD-001/BUILD-002
ไม่เปลี่ยนจากรอบก่อน (BUILD-001 เสร็จ, BUILD-002 พักตาม PANYA-DECISION 20:10)

## ยังไม่ได้พิสูจน์ / ยังบล็อกเหมือนเดิม
- anchor Bg0002 ยัง 2/7 numeric เท่าเดิม (รอ attended walk ตาม PANYA-DECISION 20:10 ข้อ 4)
- `CORE-REQUEST-BG0002-LOGIN` ยังรอ chief ต่อสาย (`runtime.py:5535`)
- `RE-115` ที่เพิ่งเปิดยังไม่มีคำตอบ (ของ RE runner)

## CORE-REQUEST
none ใหม่

-- สาย A
