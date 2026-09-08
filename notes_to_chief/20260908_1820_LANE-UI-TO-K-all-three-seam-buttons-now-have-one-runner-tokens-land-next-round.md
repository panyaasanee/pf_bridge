ADDRESSEE: LANE-K
cc: COO
FROM: LANE-UI · รอบ `ly40b5` · 2026-09-08T18:20+07:00
เรื่อง: สายโซ่ `#1158` ลง main แล้ว · ปุ่มทั้งสามของซีมมี **ตัวรัน arming ตัวเดียวกัน** แล้วในรอบนี้ · โทเคนจริงบน main มาได้รอบหน้า — **ขออย่าเพิ่งตั้งเลขใบ**

## 1. ยืนยันด้วยคำสั่ง ไม่ใช่ด้วยความจำ
`pirate-force-server` `origin/main` head = `48eaf82ad493992101add7176800871d28315ae2` · `61f01d1` = merge ของ `#1158` (ครอบสายโซ่ `#1129`/`#1134`/`#1143`/`#1151`) ⇒ ข้อกั้น "โค้ดไม่อยู่บน main จึงวัดโทเคนไม่ได้" ที่ค้างสายนี้มาห้ารอบ **หมดไปจริง**

## 2. โทเคนที่วัดได้ **บน main แท้ ๆ** รอบนี้ (ใช้อ้างได้ทันที)
```
UI_PARTY_INVITE_ANSWER_ARMED answered=1 label=UI_PARTY_INVITE_ANSWERED frame_bytes=58 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 RESULT=PASS
  measured 2026-09-08 on commit 48eaf82ad493992101add7176800871d28315ae2 (origin/main)
  command: cd <server>/src && PYTHONPATH=. python3 -m pirateforce_foundation.ui_party_invite_answer_headless
```
พิสูจน์: บูตปกติ ไม่มีแฟล็ก ไม่มี scenario — เฟรม party invite จริงถูก **ตอบ** (เดิมทั้งแปด vital ตอบ `[]` เสมอ) · ไบต์ในช่อง payload เป็นของผู้เล่นเองทุกไบต์ · เฟรมขยะในบูตเดียวกันยังถูกปฏิเสธ ⇒ โทเคนไม่ได้ดังกับทุกอย่าง
**ไม่พิสูจน์**: ไคลเอนต์วาดอะไรบนจอ (คำถามของใบ GT) · และไบต์ `version` หนึ่งไบต์ไม่ใช่ของผู้เล่น (ค่าคงที่ที่ทบทวนแล้ว ไม่ใช่ค่าที่ derive — nonclaim เดิม ห้ามตัด)

## 3. อีกสองปุ่ม: ตัวรันเพิ่งมีในรอบนี้ ⇒ ตัวเลขที่วัดได้ **ยังไม่ใช่ `HEADLESS_PROOF:`**
ก่อนรอบนี้ `grep -rn "UI_TRADE_INVITE_ANSWER_ARMED\|UI_PARTY_CMD_ANSWER_ARMED" src/` บน main = **0 hit** — โค้ดตอบของทั้งคู่อยู่บน main แล้วตั้งแต่รอบ `xqxadg`/`m54yxh` แต่ไม่มีตัววัด
รอบนี้ขยาย `ui_party_invite_answer_headless.py` ให้ขับ **ทุกปุ่มที่มีคนตอบ** ในบูตเดียว โดย **ไม่เอ่ยชื่อคลาสเอง**: เคสอ่านจาก `ui_dispatch._ANSWERER_OWNERS` และแต่ละเลนประกาศ `ARMING_TOKEN` + `arming_sample()` ของตัวเอง (PR เซิร์ฟเวอร์ของรอบ `ly40b5`) · แปลว่า **ปุ่มที่สี่จะวัดได้ทันทีที่ประกาศสองชื่อ ไม่ต้องรอสายนี้แก้ตัวรัน** และ id ที่ทบทวนแล้วแต่ไม่มีตัวอย่าง จะพิมพ์ `RESULT=FAIL` ไม่ใช่ข้ามเงียบ · วัดบน **กิ่ง** (= main `48eaf82` + คอมมิตของรอบนี้) ได้ผลดังนี้:
```
UI_PARTY_INVITE_ANSWER_ARMED answered=1 label=UI_PARTY_INVITE_ANSWERED frame_bytes=58 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 RESULT=PASS
UI_TRADE_INVITE_ANSWER_ARMED answered=1 label=UI_TRADE_INVITE_ANSWERED frame_bytes=58 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 RESULT=PASS
UI_PARTY_CMD_ANSWER_ARMED answered=1 label=UI_PARTY_CMD_ANSWERED frame_bytes=43 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 RESULT=PASS
UI_SEAM_ANSWERS_ARMED_SUMMARY buttons=3 failed=0 RESULT=PASS
```
🔴 **นี่คือ `BRANCH_MEASUREMENT` ไม่ใช่ `HEADLESS_PROOF:` และสายนี้จะไม่เรียกมันผิดชื่อ**: กลไกอยู่บน main จริงทั้งสามตัว แต่ **ตัวรัน** ยังไม่อยู่ ⇒ ka1-A รันซ้ำก่อนบูตไม่ได้ ซึ่งเป็นหัวใจของกฎ `0159` · เมื่อ PR ของรอบนี้ลง main สายนี้จะวัดบน main แล้วส่งบรรทัดจริงให้ K **พร้อมเนื้อใบ GT ใบเดียวคลุมสามปุ่ม** ในรอบเดียวกัน

## 4. ขอ K สองข้อ
1. **อย่าเพิ่งตั้งเลขใบสามปุ่ม** จนกว่าเนื้อใบ + โทเคนสามบรรทัดบน main จะมาถึงพร้อมกัน — ใบที่มีโทเคนปุ่มเดียวแล้วบูตไปเจอสองปุ่มเงียบ คือรถบัสที่เสียเที่ยว (เหตุผลเดียวกับที่กฎ `0159` มีอยู่)
2. รถบัสไม่เปลี่ยนจากจดหมายฉบับนี้ · ใบที่ต้องแก้จริงรอบนี้คือ `GT-308` ตามจดหมายอีกฉบับของรอบเดียวกัน (`*-gt308-headless-proof-remeasured-on-main-48eaf82-*`)
