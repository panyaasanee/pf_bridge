# LANE-GM STATUS -- ปิดของค้างจากรอบ 50x5xt: rate limit + collision-loop bound

ถึง: chief, COO, Panya
จาก: LANE-GM (session kzwdle)
เวลา: 2026-08-27T18:43+07:00

## สรุปหนึ่งบรรทัด

ปิดสองข้อที่ `docs/GM_LANE.md` ("What is intentionally NOT built yet") ระบุไว้ชัดว่าเป็น
"รอบถัดไป" ตั้งแต่รอบ `50x5xt`: per-account rate limit บน `0x51E9` capture writes และขอบเขต
ของ filename-collision retry loop -- แล้ว `pf-adversary` (verify pass ก่อนออกจาก draft) เจอ
บั๊กจริงในดราฟต์แรกของ rate limiter เอง (timestamp ordering race) ซึ่งแก้ไปในรอบเดียวกันแล้ว

## รายละเอียด

- `gm/dispatch.py`: sliding-window rate limit ต่อบัญชี (20 ครั้ง / 5 วินาที ค่าเริ่มต้น,
  คำนวณจากจังหวะจริงของใบเทส GT-103) refusal ใหม่ `REFUSAL_RATE_LIMITED` รูปแบบเดียวกับ
  refusal เดิมที่มีอยู่แล้ว (authorized=True เพราะเป็น GM จริง, captured_path=None)
- `gm/command_capture.py`: bound การ retry ชื่อไฟล์ชนกันที่ 1000 ครั้ง เกินแล้ว raise OSError
  (ของเดิมใน dispatch.py จับให้เป็น refusal อยู่แล้ว ไม่ต้องแก้จุดนั้นเพิ่ม)
- `pf-adversary` (รอบนี้เอง, verify pass): พบว่าดราฟต์แรกอ่านนาฬิกาก่อนถือ lock -- สองเธรด
  ของบัญชีเดียวกันแข่ง lock แล้วบันทึกเวลาไม่เรียงลำดับได้ (reproduce จริงด้วยเธรดจริง)
  self-healing เสมอ ไม่ใช่ช่องโหว่ (กัก account ไว้นานกว่าที่ตั้งไว้ ไม่เคยปล่อยเร็วกว่า) แต่เป็น
  บั๊กจริง แก้โดยอ่านนาฬิกาในล็อกเดียวกัน + ใช้ `bisect.insort` แทน `append` -- แก้โดยโครงสร้าง
  ไม่ใช่วินัยผู้เรียก
- `pf-adversary` เดียวกันเจอว่า `docs/GM_LANE.md` ยังเขียนของสองข้อบนเป็น present-tense ว่า
  ยังไม่ปิด ทั้งที่ commit เดียวกันปิดไปแล้ว -- แก้เอกสารในรอบเดียวกัน

## เทส

`tests/test_gm_*.py` 225/225 (จาก 215) · repo-wide `unittest discover` 3620 เทส, error 18
ใบเดิม (capstone import, baseline เดิม) ไม่มี failure ใหม่

## PR

- `pirate-force-server`#138 (commits `5494ffd`, `d59ffd2` บน `claude/upbeat-knuth-kzwdle`)
- `pf_bridge`#223 (round file + ใบนี้ บน `claude/magical-cannon-kzwdle`)

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: ไม่มี -- robustness/correctness ล้วนในเขตเขียนของสายนี้
รายละเอียดเต็มใน `rounds/GM_20260827_1843_rate-limit-plus-collision-bound-plus-adversary-timestamp-race-fix.md`

nonclaim: tooling/robustness ภายในเขตเขียนของสาย GM เท่านั้น ไม่มี wire fact ใหม่ ไม่มีการแก้
`runtime.py` ไม่มีการทดสอบผ่านเกมจริง
