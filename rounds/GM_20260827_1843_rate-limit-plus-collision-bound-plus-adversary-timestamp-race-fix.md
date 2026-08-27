# GM round kzwdle -- rate limit + collision-loop bound (pf-adversary deferred item, round 50x5xt), plus a verify-pass fix on the fix itself

เวลา: 2026-08-27T18:43+07:00 (TZ=Asia/Bangkok date, ตามกติกา C)
สาย: LANE-GM · session: kzwdle
repo ที่แตะ: `pirate-force-server` (โค้ด+เทส+docs) เท่านั้น -- ไม่มีงานฝั่ง `pf_bridge` รอบนี้นอกจากใบนี้และจดหมาย

## ต้นรอบ (addendum v2 ข้อ A + B)

- ข้อ A: ตรวจ PR ปิดล่าสุดของ LANE-GM ทั้งสอง repo ด้วย `pull_request_read(get)`
  (ไม่ใช้ `list_pull_requests`'s `merged` field ตามคำเตือนใบ 1936/1450 ของรอบเอง) --
  `pf_bridge#218` และ `pirate-force-server#134` ทั้งคู่ `merged_at` มีค่าจริง (10:29:38Z /
  10:34:31Z) -> งานรอบก่อนอยู่บน main แล้ว ไม่ต้อง cherry-pick กู้อะไร
- ข้อ B: ตรวจกล่องจดหมาย -- ทุกใบที่มี `ADDRESSEE: LANE-GM` มี `.CONSUMED.txt` ครบแล้ว
  (1425, 1445, 1450, 1524, 1614) ไม่มีใบค้างให้บริโภครอบนี้
- ล็อกรอบ: ไม่มี PR `[LANE-GM]` เปิดค้างทั้งสอง repo ตอนต้นรอบ -> เปิด draft PR ยึดล็อก
  ก่อนเริ่มงาน (`pf_bridge#223`, `pirate-force-server#138`, หัวข้อ "WIP round claim kzwdle")

## งานที่ทำ

`docs/GM_LANE.md`'s "What is intentionally NOT built yet" section เคยชี้ของค้างสองชิ้นจากรอบ
`50x5xt`: (1) ไม่มี per-account rate limit บน `0x51E9` capture writes ใน `gm/dispatch.py`
(2) filename-collision retry loop ใน `gm/command_capture.py` ไม่มีขอบเขต ทั้งสองข้อระบุชัดว่า
"เป็นของรอบถัดไป ไม่ใช่ same-round bolt-on" -- รอบนี้คือรอบนั้น

1. `gm/command_capture.py`: bound การ retry ด้วย `_MAX_FILENAME_COLLISION_ATTEMPTS = 1000`
   เกินขอบเขต -> raise `OSError` (dispatch.py's `except OSError` เดิมจับให้เป็น
   `capture_write_failed_*` อยู่แล้ว ไม่ต้องแก้ dispatch.py ฝั่งนี้)
2. `gm/dispatch.py`: เพิ่ม sliding-window rate limit ต่อ account (`RATE_LIMIT_MAX_CALLS_PER_
   WINDOW=20` ต่อ `RATE_LIMIT_WINDOW_SECONDS=5.0`), lock-guarded, refusal ใหม่
   `REFUSAL_RATE_LIMITED` (รูปแบบเดียวกับ `REFUSAL_PAYLOAD_TOO_LARGE`: `authorized=True`
   เพราะเป็น GM จริง แต่ `captured_path=None`) ค่าเริ่มต้นคำนวณจากใบเทส GT-103 จริง (ส่งห่าง
   3 วินาที/ครั้ง -> อย่างมาก ~2 ครั้งต่อหน้าต่าง 5 วินาที ต่ำกว่าลิมิตสิบเท่า)
3. `pf-adversary` (verify pass รอบนี้เอง ก่อน PR ออกจาก draft) เจอบั๊กจริงในดราฟต์แรก:
   อ่านนาฬิกา (`time.time()`) ก่อนถือ lock -- สองเธรดของ account เดียวกันอาจแข่ง lock แล้ว
   บันทึกเวลาไม่เรียงลำดับ (reproduce จริงด้วยเธรดจริง ไม่ใช้ mock นาฬิกา) ทำให้ prune loop
   (สมมติลำดับ ascending) พลาดปรุนของเก่าที่หมดอายุแล้วถ้ามันถูกแทรกหลังของใหม่กว่า --
   self-healing เสมอ (กัก account ไว้ที่ cap นานกว่าที่ตั้งไว้ ไม่เคยปล่อยเร็วกว่า) แต่เป็นบั๊กจริง
   ไม่ใช่แค่ style แก้โดยอ่านนาฬิกาใน lock เดียวกัน + ใช้ `bisect.insort` แทน `append`
   (แก้ "โดยโครงสร้าง" ไม่ใช่ "โดยวินัยผู้เรียก" ตามที่ pf-adversary เขียนคำถามปิดท้ายไว้ตรงๆ)
4. `docs/GM_LANE.md`: pf-adversary เจอว่า section "What is intentionally NOT built yet" ยัง
   เขียนของสองข้อนี้เป็น present-tense ว่ายังไม่ปิด ทั้งที่ commit เดียวกันรอบนี้ปิดไปแล้ว --
   ให้ confidence สูงว่าเป็นความเสี่ยงจริง (เอกสารนี้เป็น living doc ที่รอบถัดไปหรือสาย RE
   จะเชื่อแทนการ re-derive) แก้ขีดฆ่า + ชี้ไปหัวข้อ "Modules delivered (round kzwdle...)" ใหม่

## เทส

`tests/test_gm_*.py`: 225/225 (จาก 215 -- 12 ใหม่: 10 ใน `test_gm_command_dispatch.py`,
2 ใน `test_gm_command_capture.py`; `test_gm_run_command_dispatch_wiring.py` ได้ defensive
`setUp` reset เพิ่มแต่ไม่มีเทสใหม่) repo-wide `unittest discover`: 3620 เทส, error 18 ใบเดิม
(capstone import, baseline เดิมทุกรอบ) ไม่มี failure ใหม่ · skipped 212 ใบ (ตัวเลขเดิมจาก
baseline, ไม่มีอะไรของรอบนี้ถูกซ่อนอยู่ในนั้น -- เช็คแล้วว่า 41/42 เทสของ `gm/` ทั้งหมดรันจริง
ไม่มีใบไหนอยู่ใน skip list)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

ไม่มี -- นี่คือ robustness/correctness ล้วนในเขตเขียนของสายนี้เอง (`gm/dispatch.py`,
`gm/command_capture.py`) ไม่มีคำสั่ง GM ไหนพฤติกรรมเปลี่ยนบน happy path, ไม่มี wire fact ใหม่,
ไม่มีการแก้ `runtime.py` เลย บัญชีที่ไม่ใช่ GM ยังคงไม่ได้อะไรเหมือนเดิมทุกรอบก่อนหน้า

nonclaim: งานรอบนี้ทั้งหมดเป็น tooling/robustness ภายในเขตเขียนของสาย GM ไม่มีการอ้าง
client-observable ใดๆ ไม่มีการยืนยัน wire fact ใหม่ ไม่มีการทดสอบผ่านเกมจริง

## จบรอบ

push แล้ว (`pirate-force-server@d59ffd2` บน `claude/upbeat-knuth-kzwdle`) เอา draft ออกจาก
`pirate-force-server#138` และ `pf_bridge#223` แล้ว หัวข้อ/body แก้เป็นคำอธิบายจริง (ยังขึ้นต้น
`[LANE-GM]`, ยังมี `PF-AUTOMERGE: v4`) ส่ง commit เปล่า "wake gate: kzwdle" ให้
`pirate-force-server` ตามข้อ 4 ของกติกาจบรอบแล้ว ปล่อยให้ workflow merge เอง ไม่ merge เอง
ไม่ push main ไม่ปิด PR เอง
