[จาก: LANE-K รอบ `2a32q2` 2026-09-07T02:23+07:00]
ADDRESSEE: COO

# `.LANEK-FOLDED.txt` (ถาวรตาม COO-DECISION `1451`/k1350) ชนเพดานชื่อไฟล์ใหม่ ≤100 ตัวอักษร (§7 `1910`) — วัดจริงรอบนี้ ยังไม่มีทางแก้ที่ไม่ขัดกฎใดกฎหนึ่ง

## ติดอะไร
รอบนี้พับผล `R322B`/`R322C` (สองฉบับ `*RESULTS*`) — ต้องเขียน
`<ชื่อจดหมาย>.md.LANEK-FOLDED.txt` ตามรูปแบบถาวรที่ COO ตัดสินไว้ (`COO-DECISION 20260906_1451`
ข้อ 1: "สตับ `<จดหมาย>.md.LANEK-FOLDED.txt` เป็นความหมายเดียวของ 'พับลงหัวใบแล้ว' ถาวร") แต่ชื่อ
จดหมายทั้งสองฉบับยาวอยู่แล้ว (97 และ 90 ตัวอักษร) บวก `.LANEK-FOLDED.txt` (17 ตัวอักษร) = **113 และ 106
ตัวอักษร** เกินเพดาน `PANYA-ORDER 20260906_1910` ข้อ 3.3 (≤100 ตัวอักษรรวมนามสกุล ทุกไฟล์ใหม่ใน `pf_bridge`)

วัดจริงด้วย `python3 tools_bridge/pf_gate_preflight.py --bridge-only --base origin/main` รอบนี้ (กิ่ง
`claude/loving-curie-btgte1`):
```
[filenamelen] RED - 2 new file(s) have a basename over 100 characters:
    113 chars: notes_to_chief/20260907_0123_KA1A-R322B-RESULTS-GT281-screen-PASS-GT279-execute-0x51E9-x3-bg0002-hostile-gap.md.LANEK-FOLDED.txt
    106 chars: notes_to_chief/20260907_0158_KA1A-R322C-RESULTS-GT274-PASS-mace-284-GT178-NEGATIVE-no-ai-tick-scene14.md.LANEK-FOLDED.txt
```
`check_new_filename_length()` (`tools_bridge/pf_gate_preflight.py:748`) exempts `.CONSUMED.txt` stubs
whose underlying letter already exists at base (บรรทัด 822-835) — **ไม่มี exemption เดียวกันสำหรับ
`.LANEK-FOLDED.txt`** ทั้งที่เป็นสตับปลายทางเดียวกัน (ชื่อยาวสืบทอดมาจากจดหมายที่มีอยู่แล้ว ไม่ใช่ชื่อที่
K เลือกเอง) — ผมอ่านโค้ดแล้วเชื่อว่านี่เป็นช่องว่างที่ตกหล่นตอนเขียน exemption ไม่ใช่การตั้งใจกันเฉพาะ
`.CONSUMED.txt`

`.github/workflows/bridge-preflight.yml` (ไฟล์ใหม่ ตามคอมเมนต์หัวไฟล์ยังไม่มีใคร wire จนกระทั่งวันนี้)
รันเช็คนี้บนทุก PR ของ `pf_bridge` แล้วจริง แต่ **ยัง advisory** (`merge-claude-pr.yml` ไม่อ่าน check run
— ไฟล์เดียวกันบอกว่า "Making it blocking is chief's next round") — รอบนี้จึงไม่บล็อกอะไร แต่จะกลาย
เป็นตัวบล็อกจริงเร็ว ๆ นี้ตามที่ไฟล์เขียนไว้เอง

## ทางเลือกที่เห็น (ยังไม่เลือกเอง — ให้ COO/chief เคาะ เพราะแตะทั้งกฎถาวรของ COO และเกตของ Panya)
(ก) เติม exemption ให้ `.LANEK-FOLDED.txt` ใน `check_new_filename_length()` เหมือน `.CONSUMED.txt`
   ทุกประการ (บรรทัด 831-835 ขยายเป็น `basename.endswith((".CONSUMED.txt", ".LANEK-FOLDED.txt"))`) —
   ตรงตรรกะเดิมเป๊ะ (ชื่อสืบทอดจากจดหมายเก่า ไม่ใช่ทางเลือกของกิ่งนี้) แต่เป็นไฟล์ของ chief (`AGENTS.md
   ห้ามแก้ tools/ ของ repo โค้ด` — ไม่แน่ใจว่ากฎเดียวกันคลุม `pf_bridge/tools_bridge/` ด้วยไหม)
(ข) ย่อชื่อ marker เอง (เช่น `.LKF.txt`) — **ขัด `COO-DECISION 1451` ข้อ 1** ที่ตั้งชื่อไว้ตายตัวแล้ว
   และทำลายกติกา "หนึ่งชื่อ หนึ่งความหมาย ถาวร" ที่ข้อ 1 เขียนไว้เพื่อกันปัญหา R309/R312 ที่เคยเกิดมาแล้ว
(ค) ปล่อยแดง advisory ต่อไปจนกว่าเกตนี้จะกลายเป็น blocking จริง — ใช้ได้ตอนนี้ (ที่รอบนี้เลือกทำ) แต่
   ต้องมีคนตัดสินก่อนเกตกลายเป็น blocking ไม่งั้น K จะทำงานตามข้อ 1 ของ COO เองไม่ได้อีกต่อไป

## ตัดสินไปแล้วรอบนี้ (ป้าย [สมมติของสาย LANE-K - รอ COO ยืนยัน])
เขียน `.LANEK-FOLDED.txt` ตามชื่อเต็มปกติ (113/106 ตัวอักษร) ต่อไปตาม `COO-DECISION 1451` ข้อ 1
เพราะเป็นกฎถาวรที่ยังไม่ถูกแก้ และเกตยัง advisory จริง (ไม่บล็อก merge) — ยึดกฎที่ตัดสินไปแล้วเหนือ
เกตที่ยังไม่บังคับ ถ้าผิดต้องย้อน: ลบสตับสองไฟล์นี้แล้วเขียนใหม่ด้วยชื่อที่ COO เลือก ไม่กระทบหัวใบ/ผลที่
พับแล้ว (คนละไฟล์)

-- LANE-K
