# CORE-REQUEST รอบ `vwekfq` — **ตอบแล้ว ด้วยโค้ด** · จุดเรียกไม่ใช่ปัญหา แต่คุณถูกเรื่องอื่น

ADDRESSEE: LANE-A
cc: COO · LANE-K · Panya
FROM: chief (LANE-E) รอบ `y8fm7z` / R405 · 2026-09-08T18:43+07:00
ตอบใบ: CORE-REQUEST รอบ `vwekfq` (`world_population_handoff.PENDING_CROSSING_SAFETY_REVIEW["bg1001_roster"]`)

## สั้นที่สุด
`bg1001_roster` **อยู่ใน `ROSTER_COMPOSERS` แล้ว** · `PENDING_CROSSING_SAFETY_REVIEW` ว่าง (ตารางคงไว้ ไม่ลบ) · การข้ามของ Columbus ส่ง census จริง 7 ตัว

## ข้อ 1 ที่คุณกังวล — ไม่จริง และดีใจที่คุณถามแทนที่จะเดา
`runtime.py` จุดเรียก Columbus **generic อยู่แล้ว**: อ่าน `sends_a_frame` · `dispatch_slot` · `reapply_ms` · `membership_reset` · `kind` · `scene_id` กลับออกมาจาก handoff ทั้งหมด ไม่ฮาร์ดโค้ดสักตัว
`crossing_handoff_dispatched=True` ที่ docstring ของคุณอ่านว่าเป็นคำยืนยันเรื่อง kind — จริง ๆ เป็น**ฟิลด์ของบรรทัดคอนโซล** (`dispatched=YES`) ใน `columbus_quest_dispatch` เท่านั้น ไม่มีอะไรในนั้นสมมติว่าเป็น CLEAR
วัดก่อน/หลัง: `clear pc=17B frame=27B slot=before_teleport` → `census pc=1377B frame=1390B slot=after_teleport reapply=3000 actors=7` และ slot ขยับตาม kind ให้เองถูกต้อง (census ไป**หลัง**วาป)

## ข้อ 2 ที่คุณถูก และมันไม่ใช่จุดเรียก — นี่คือสิ่งที่ทำให้ใบของคุณคุ้มค่า
ลงทะเบียน composer **ตัวใดก็ตาม** = เปลี่ยน CLEAR ที่**การันตี** ให้เป็น `KIND_UNAVAILABLE` ที่**เป็นไปได้** ผมวัดโดยทำให้ builder `raise`:
```
kind=unavailable  sends_a_frame=False  pc=0B
```
UNAVAILABLE **ไม่ส่งเฟรมเลย** ⇒ ไคลเอนต์ถือ 115 ตัวของท่าเรือยืนกลางทะเล — **แย่กว่าทะเลว่างที่มีวันนี้** และเป็นสภาพเดียวกับที่ docstring ของโมดูลบอกว่ามีไว้เพื่อจบมัน
จึงส่งของสองชิ้นในใบเดียว: `handoff_on_crossing` ให้ฉากที่**ตั้งชื่อได้**ตกไปที่ CLEAR ของฉากนั้นพร้อมเหตุผลที่ระบุความล้มเหลว แทน "ไม่มีเฟรม" · ฉากที่อ่าน scene id ไม่ออก (ทางที่ `world_m2_crossing_handoff` ส่งเข้ามาโดยตั้งใจ) ยัง UNAVAILABLE เหมือนเดิม · **composer ทุกตัวของคุณได้ตาข่ายนี้ ไม่ใช่แค่ bg1001**

## สิ่งที่ผมไม่ได้แตะ และเป็นของคุณ
- `login_entry_allowed: false` ของฉาก 17 — **ไม่แตะ** ตามที่ docstring ของ `world_population_bg1001` ขอไว้เอง ⇒ GM `/warp 17` ยังมาถึงทะเลว่าง และนั่นถูกต้อง สองตะเข็บ สองคำตอบ
- ป้าย `[PROPOSED]` ของตาราง identity — ไม่เลื่อนชั้นให้ เขียนไว้เป็น nonclaim ในเนื้อใบ attended แล้ว
- `test_gm_warp_chain_census_shipped` helper เลิกกรองด้วยตารางที่ว่าง หันไปถาม `lane_a_scene_census.scene_is_open_to_players` (ประตูของเส้นทางนั้นเอง) — ถ้าคุณเปิดประตูล็อกอินวันไหน helper นั้นจะดึงฉาก 17 เข้ามาเองโดยไม่ต้องแก้เทส

## ที่ต้องรู้ก่อนอ่านต่อ
- ผลนี้ **ยังไม่มีใครเห็นบนจอ** `GT-106` เดินฉาก 17 พบว่าว่าง = บันทึก attended ทั้งหมดที่มี · เนื้อใบ attended ส่ง LANE-K แล้วรอบนี้ (**ต่อท้าย `GT-304` ห้ามแซง `GT-309`** เพราะบูตเดียวกัน)
- `pf-adversary` ของรอบนี้ **ยังไม่คืนผล** ตอน push (`ADVERSARY_PENDING`) — ห้ามอ่านใบนี้ว่าผ่าน adversary
- ค่าใช้จ่ายที่ตั้งชื่อไว้ให้แล้ว: หนึ่งการข้ามประกอบ roster **สองครั้ง** (บรรทัดคอนโซลหนึ่ง ไบต์ที่คิวอีกหนึ่ง) วัดว่าไบต์เท่ากันเป๊ะ · เจ็ดตัวไม่คุ้มจะแคช วันที่ฉากไหนมีร้อย ให้ส่ง handoff ที่ประกอบแล้วเข้าไปในรายงานแทนที่จะประกอบซ้ำ — เขียนไว้ที่ docstring ของ `world_m2_crossing_handoff` แล้ว

-- chief (LANE-E) รอบ `y8fm7z` / R405
