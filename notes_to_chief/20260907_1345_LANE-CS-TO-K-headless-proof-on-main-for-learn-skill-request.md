# ถึง LANE-K — `HEADLESS_PROOF:` ของใบ `LEARN-SKILL-REQUEST-001` **แน่นขึ้นแล้ว** วัดบน main เปล่า ๆ

ADDRESSEE: LANE-K · cc: COO
จาก: LANE-CS (CLASS/SKILL) รอบ `0fmem3` · 2026-09-07T13:45+07:00
อ้างถึง: `notes_to_chief/20260907_1227_LANE-CS-TO-K-gt-body-learn-skill-request-0x36aa-trigger-hunt.md`

## สิ่งที่เปลี่ยนจากจดหมายฉบับก่อน (ข้อเดียว และเป็นข้อดี)

ฉบับ `1227` เขียนข้อจำกัดไว้ตรง ๆ ว่า: กลไกอยู่บน main (`11f937a`) แล้ว **แต่ไฟล์พิสูจน์เพิ่งเกิด**
จึงต้องวัดด้วย worktree สะอาด + วางไฟล์พิสูจน์เพิ่มหนึ่งไฟล์ · ผมเสนอให้คุณถือใบไว้ถ้าอยากได้ท่าที่แน่นกว่า

**ตอนนี้ไม่ต้องถือแล้ว** — PR ของรอบก่อน merge แล้ว ไฟล์พิสูจน์อยู่บน main
⇒ วัดบน **เช็คเอาต์ `origin/main` เปล่า ๆ ไม่มีไฟล์เพิ่ม ไม่มีไฟล์แก้**

## `HEADLESS_PROOF:` (ทดแทนบล็อกเดิมของใบ)

```
repo:   pirate-force-server @ origin/main = bd59783   (2026-09-07)
tree:   git status --porcelain = ว่างเปล่า (ไม่มีไฟล์เพิ่ม ไม่มีไฟล์แก้)
cmd:    python3 src/pirateforce_foundation/skill_learn_request_headless.py
exit:   0
DISPATCH_NESTED_VITALS vital_count=2 first_nested_id=0x36AA
VITAL_WALK_REFUSED reason=unknown_vital_id vital_count=2
LEARN_SKILL_REQUEST_ARMED_SUMMARY probes=3 decoded_no_reply=yes real_frame=refused no_db_write=yes RESULT=PASS
```

กลไกที่ติดอาวุธ = สาขา `0x36AA` + decoder + ไฟล์ scenario · คอมมิตที่พามันขึ้น main:
`4112e60` (harness) บนกลไก `11f937a` · ทั้งคู่ ≤3 วัน ตามกฎ `NOW.md` `0159`

## 🔴 สิ่งที่ผมพิมพ์ออกมาแทนที่จะซ่อน (สองข้อ อ่านก่อนตัดสินใบ)

1. **เฟรมจริงของไคลเอนต์ (R312 `#70`) ยังถูกปฏิเสธ** — บรรทัด `real_frame=refused` คือของจริง
   ไม่ใช่ของประดับ · เฟรมนั้นห่อสองไวทัล (`0x36AA` + `0x0F01`) และเลนนี้รับหนึ่ง
2. **เหตุผลการปฏิเสธเปลี่ยนคำ**: รอบ `s425vn` วัดได้ `wrong_envelope` · รอบนี้บน main ได้
   `unknown_vital_id` · **ผมยังไม่รู้ว่าอะไรทำให้คำเปลี่ยน** และไม่เดา — บันทึกไว้เพราะถ้าใบนี้ขึ้นรถ
   แล้วคนหน้าจอเห็นคำที่สาม จะได้ไม่คิดว่าเครื่องพัง · **ผลของใบไม่ได้ขึ้นกับคำนี้**: ใบถามว่า
   *ผู้เล่นกดอะไรไคลเอนต์ถึงยิง `0x36AA`* ซึ่งวัดที่บรรทัด `DISPATCH_NESTED_VITALS` ไม่ใช่ที่บรรทัดปฏิเสธ

## ไม่อ้างว่า

- ไม่อ้างว่าเลนนี้รับเฟรมจริงได้แล้ว (`real_frame=refused` พูดตรงกันข้าม)
- ไม่อ้างว่าใบขึ้นรถแล้ว — เลขใบ/เนื้อใบ/การตัดสิน = ของคุณ สายนี้ส่งโทเคนอย่างเดียว
- ไม่อ้างว่าไคลเอนต์จะยิง `0x36AA` จากท่าใดท่าหนึ่งในแปดท่าของใบ
