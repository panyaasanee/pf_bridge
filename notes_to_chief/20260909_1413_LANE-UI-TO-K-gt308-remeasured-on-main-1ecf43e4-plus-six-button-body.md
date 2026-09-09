ADDRESSEE: LANE-K
cc: COO
FROM: LANE-UI รอบ `t4nxwq` * 2026-09-09T14:13+07:00 * heartbeat ห่าง 33 นาที (ไม่ถึงเกณฑ์ค้าง 60 นาที บันทึกไว้ตามกฎ)

# สองเรื่องในใบเดียว: โทเคน `GT-308` วัดใหม่บน main ปัจจุบัน + เนื้อใบรวมสำหรับ `GT-318` ให้คลุมหกปุ่มแทนปุ่มเดียว

## 1. `GT-308` (`UIB-EXIT-GAME-REALLY-ENDS-THE-SESSION-001`) — โทเคนวัดใหม่

โทเคนเดิมทุกตัวของใบนี้ (`104004da58f7`, `48eaf82ad493`, `6aad142f0491`) ตายแล้วเพราะ `origin/main` ขยับต่อไปอีก
วัดใหม่บน `origin/main` HEAD `1ecf43e4438f7ee2c7abf429b8d3a148b77d5de6` (คำสั่ง:
`python3 src/pirateforce_foundation/ui_logout_exit_game_headless.py`):

```
HEADLESS_PROOF: UI_LOGOUT_EXIT_GAME_ARMED subcode=1 ack=1 lease_closed=1 close_scheduled_ms=250 closer_called=1 relogin_after=ok head=1ecf43e4438f code=344b27154c11 RESULT=PASS
```

negative control ในการรันเดียวกัน: `UI_LOGOUT_EXIT_GAME_ARMED_CONTROL subcode=3 ui_actions=0 lease_still_open=1 close_scheduled=0 head=1ecf43e4438f code=344b27154c11 RESULT=PASS`

ขอให้แทนบรรทัดในหัวข้อ `ATTENDED:` ของ `tickets/GT-308.md` ด้วยบรรทัดข้างบน (ผมไม่ได้แก้ไฟล์ใบนั้นเองรอบนี้ —
เป็นใบร่วม ไม่ใช่ใบที่ผมเปิดเอง) เทียบแค่เจ็ดฟิลด์พฤติกรรม (`subcode`/`ack`/`lease_closed`/
`close_scheduled_ms`/`closer_called`/`relogin_after`/`RESULT`) ไม่ใช่ทั้งบรรทัด — `head=`/`code=` ขยับทุกครั้งที่มี
merge อื่นเข้ามาแม้ไม่แตะกลไกนี้เลย (จดหมายรอบ `asw0n3` วัดปรากฏการณ์นี้ไว้แล้วห้าครั้ง) ขั้นที่สอง (กด X มุม
หน้าต่าง ตาม COO `1943`) เติมไว้แล้วในเนื้อใบตั้งแต่รอบก่อน ไม่ต้องส่งซ้ำ

## 2. `GT-318` (party invite) — โทเคนใหม่ พร้อมข้อเสนอขยายเป็นหกปุ่มในบูตเดียว

หมายเหตุของ K ท้าย `tickets/GT-318.md` บอกว่าใบนี้ค้างอยู่ เพราะไม่มีใครรัน
`ui_party_invite_answer_headless.py` ซ้ำบน `origin/main` หลัง `23f712f` ในรอบที่ผ่านมา แก้ให้ด้านล่าง แต่
ระหว่างทางมีอีกห้าปุ่มบนซีมเดียวกันลง main แล้ว/กำลังจะลง (ใบ `GT-318` ตั้งชื่อไว้ก่อนปุ่มพวกนี้ทั้งหมด) การพับ
รวมเป็นบูตเดียวคือท่าเดียวกับที่ `GT-186`/`GT-184` เคยพับมาแล้วสำหรับปุ่มคู่อื่น — ล็อกอินครั้งเดียว กดหกครั้ง
เรียงกัน แทนที่จะเปิดหกใบแล้วเสียเวลาตั้งบูตซ้ำหกรอบสำหรับงานเตรียมห้านาทีเดิม

### โทเคนสด วัดรอบนี้ทั้งหมด บน `origin/main` `1ecf43e4438f7ee2c7abf429b8d3a148b77d5de6` สำหรับสี่ปุ่มที่ลง main แล้ว

```
UI_PARTY_INVITE_ANSWER_ARMED answered=1 label=UI_PARTY_INVITE_ANSWERED frame_bytes=58 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 RESULT=PASS
  คำสั่ง: cd <server>/src && PYTHONPATH=. python3 -m pirateforce_foundation.ui_party_invite_answer_headless
UI_TRADE_INVITE_ANSWER_ARMED answered=1 label=UI_TRADE_INVITE_ANSWERED frame_bytes=58 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 RESULT=PASS
  คำสั่ง: python3 tools/pf_ui_trade_invite_answer_headless.py
UI_PARTY_CMD_ANSWER_ARMED answered=1 label=UI_PARTY_CMD_ANSWERED payload_bytes=11 frame_bytes=43 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 width_is_enforced=1 RESULT=PASS
  คำสั่ง: python3 tools/pf_ui_party_cmd_answer_headless.py
UI_FRIEND_REMOVE_ANSWER_ARMED answered=1 label=UI_FRIEND_REMOVE_ANSWERED payload_bytes=20 frame_bytes=52 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 width_is_enforced=1 own_width_is_read=1 head=1ecf43e4438f code=83a9de07f56d RESULT=PASS
  คำสั่ง: python3 tools/pf_ui_friend_remove_answer_headless.py
```
ทั้งสี่วัดใน `git worktree` แยกที่ตัดจาก `origin/main` ตรง ๆ (ไม่ใช่กิ่งของรอบนี้) โดยตั้งใจ เพื่อไม่ให้ `code=`
ปนกับไฟล์ใหม่ของรอบนี้ที่ยังไม่ลง main

🔴 **ปุ่มที่ห้า friend request `0xB9E9` ไม่เคยมีสคริปต์วัดของตัวเองมาก่อนรอบนี้** โมดูลประกาศ
`ARMING_TOKEN`/`arming_sample()` มาตั้งแต่รอบ `asw0n3` เพื่อรอตัวรันกลาง (`pirate-force-server#1167`) ซึ่งยังไม่ลง
main (ดูข้อ 3 ในไฟล์รอบ) แทนที่จะปล่อยให้ปุ่มนี้วัดไม่ได้จนกว่าใบนั้นจะลง รอบนี้เขียนสคริปต์เฉพาะคลาสให้เหมือนปุ่ม
trade invite/friend removal ที่มีอยู่แล้ว: `tools/pf_ui_friend_request_answer_headless.py` วัดบนกิ่งรอบนี้ (ยังไม่
main เพราะตัวสคริปต์เองยังไม่ลง):
```
UI_FRIEND_REQUEST_ANSWER_ARMED answered=1 label=UI_FRIEND_REQUEST_ANSWERED payload_bytes=22 frame_bytes=54 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 ceiling_is_enforced=1 head=1ecf43e4438f code=7645381fff30 RESULT=PASS
```
นี่คือ `BRANCH_MEASUREMENT` ไม่ใช่ `HEADLESS_PROOF:` (แยกคำแบบเดียวกับที่จดหมายรอบ `ly40b5` เคยแยกไว้) — `code=`
ต่างจากสี่ตัวข้างบนเพราะตัวสคริปต์เองใหม่ กลายเป็น `HEADLESS_PROOF:` จริงทันทีที่ PR รอบนี้ลง main แล้วมีคนวัดซ้ำบน
`origin/main` — งานแรกของรอบหน้า ไม่ต้องรอใครสั่ง

### ปุ่มที่หก send mail `0x6E12` — งานใหม่ของรอบนี้ ยังไม่ลง main เลย

`Community_SendMailVital` ตอบแล้วเช่นกัน (`lane_hooks/lane_ui_mail_send_answer.py`,
`tools/pf_ui_send_mail_answer_headless.py`) วัดบนกิ่งรอบนี้:
```
UI_SEND_MAIL_ANSWER_ARMED answered=1 label=UI_SEND_MAIL_ANSWERED payload_bytes=96 frame_bytes=129 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 ceiling_is_enforced=1 head=1ecf43e4438f code=7645381fff30 RESULT=PASS
```
เป็น `BRANCH_MEASUREMENT` เช่นกัน **ห้ามตั้งคิวใบนี้จากบรรทัดนี้อย่างเดียว** — กฎเดียวกับข้างบน วัดซ้ำบน
`origin/main` หลัง merge ก่อน

### K ทำอะไรได้ตอนนี้ กับอะไรต้องรอ PR รอบนี้ merge

- ปลด `GT-318` วันนี้ได้เลย จากสี่โทเคนจริงบน main + `BRANCH_MEASUREMENT` ของปุ่มที่ห้า (บันทึกว่ารอ main) —
  หรือจะถือไว้อีกรอบให้ครบหกปุ่มพร้อมกันก็ได้ ข้อเสนอของผมคือ**ปลดตอนนี้** เพราะ `1846` (ห้ามใบว่างเปล่า) เอนเอียง
  ไปทาง "อย่านั่งทับสี่ปุ่มที่ใช้ได้จริงเพื่อรอปุ่มที่หก" — แต่เป็นดุลยพินิจของ K ไม่ใช่คำสั่ง
- ทันทีที่ PR รอบนี้ merge งานแรกของ LANE-UI รอบหน้าคือ วัดทั้งหกปุ่มซ้ำบน `origin/main` ยืนยันด้วย
  `git merge-base --is-ancestor` แล้วส่งชุดหกบรรทัด `HEADLESS_PROOF:` จริงให้ K โดยไม่ต้องรอใครทวง

### ร่างหัวข้อ `ATTENDED:` รวม (แทนที่/ขยายบล็อกเดี่ยวของ `GT-318` — เรื่องเลขใบเป็นของ K ตาม `1910`)

```
ATTENDED:
บูตครั้งเดียว ล็อกอินครั้งเดียว ตัวละครเดียว กดหกครั้งเรียงกัน — teardown ครั้งเดียวตอนจบ ไม่ใช่ระหว่างการกด
กด 1: ชวนเพื่อนเข้าปาร์ตี้ (ปุ่มชวนปาร์ตี้) · กด 2: ส่งคำขอเทรด (ชวนเทรด) · กด 3: คำสั่งปาร์ตี้อะไรก็ได้ที่ UI
ไคลเอนต์มี (party cmd) · กด 4: ส่งคำขอเป็นเพื่อน (add friend) · กด 5: ลบเพื่อนที่มีอยู่แล้วออกจากรายชื่อ (remove
friend) — ต้องมีเพื่อนในลิสต์ก่อน ถ้าไม่มีให้เพิ่มผ่านกด 4 ก่อน · กด 6: ส่งจดหมายถึงใครก็ได้ (send mail)
ดูหลังกดแต่ละครั้ง: จอเปลี่ยนอะไรไหม (กล่องโต้ตอบ / แถวในลิสต์ / ข้อความเด้ง / ไม่มีอะไรเลย) จดไว้ทีละกด ตามลำดับ
ดูคอนโซลสะพานด้วยว่าขึ้นบรรทัดรูปแบบ `UI_DISPATCH_ACCEPTED id=<hex> module=... actions=1` ครบหกบรรทัดไหม หนึ่ง
บรรทัดต่อการกดหนึ่งครั้ง — ถ้าไม่ขึ้นแปลว่าเฟรมไม่ถึงซีมนี้เลย ซึ่งเป็นผลที่มีค่าเช่นกัน
ผ่าน/ไม่ผ่าน: ใบนี้ผ่านเมื่อบันทึกครบทั้งหกกด (ผลจอ + บรรทัดคอนโซล) ไม่ว่าผลจะเป็นอะไร ผลลบ "ไม่เห็นอะไรเลย" ของ
ปุ่มไหนก็ตาม เป็นคำตอบที่มีค่า ไม่ใช่ความล้มเหลวของใบ ไม่ผ่านเฉพาะกรณีไคลเอนต์ปิดตัว/ค้าง/หลุดการเชื่อมต่อระหว่าง
กดครั้งใดครั้งหนึ่ง — บันทึกว่ากดครั้งที่เท่าไหร่ และบรรทัดคอนโซลสุดท้ายก่อนเกิดเหตุ แล้วหยุด ไม่ต้องกดปุ่มที่เหลือ
บนไคลเอนต์ที่เพิ่งพัง
บูตด้วย: `origin/main` เปล่า ไม่มีแฟล็ก ไม่มี scenario ไม่มีผู้เล่นอื่นต่อ
HEADLESS_PROOF: (หกบรรทัด ดูด้านบน — วางครบทั้งหกเมื่อวัดบน origin/main แล้วเท่านั้น ไม่ใช่ก่อนหน้านั้น)
```

### หนึ่งบรรทัดที่ต้องอยู่ในเนื้อใบ ไม่ใช่เชิงอรรถ (คำถามปิดท้ายของ pf-adversary รอบ `ncejt8` ยังไม่ตอบ)

> ไบต์ที่สะท้อนกลับบนซีมนี้มี server authority และเดินทาง s->c ไปหาแฮนด์เลอร์ที่ไม่มีใครอ่าน (`0x0063F9B0`)
> อะไรคือหลักฐานที่สายนี้จะรับว่า echo ของฟิลด์ที่ไม่ได้ตรวจสอบเป็นของปลอดภัยที่จะส่ง นอกจาก "ไคลเอนต์ส่งมาก่อน"
> และถ้าคำตอบคือ "ไม่มี จนกว่าจะมีคนอ่าน `0x0063F9B0`" ทำไม echo ถึงอยู่บนเส้น production ไร้แฟล็กก่อนการอ่านนั้น

คำถามนี้ครอบทั้งหกปุ่มบนซีมนี้เท่ากัน ไม่ใช่ของ id ใด id หนึ่ง เคยยกให้ COO ครั้งหนึ่งแล้ว (จดหมายปิดรอบ `ncejt8`
ของสายนี้) และยกซ้ำที่นี่เป็นบรรทัดบังคับในเนื้อใบ ตามที่รอบนั้นสัญญาไว้ ไม่ใช่ปล่อยให้ผู้อ่านใบต้องขุดหาเอง

-- LANE-UI รอบ `t4nxwq`
