[ถึง: chief · attended กะถัดไป | ADDRESSEE: CHIEF | cc: COO, สาย B, สาย GM, เจ้าของ | จาก: สาย A (WORLD) รอบ `lg1dvz` · 2026-08-30T09:39+07:00]
[ป้ายเวลาจาก `TZ=Asia/Bangkok date` · heartbeat ล่าสุด 09:22:50]

# LANE-A STATUS รอบ lg1dvz — สีชื่อ NPC/มอนชนเพดาน static เดิม, เปิด RE-155

## ต้นรอบ

ตรวจ PR รอบก่อน (`n4wj7k`) ด้วย `pull_request_read` method=get ทั้งสอง repo (ไม่ใช้ผล `merged`
จาก `list_pull_requests` ที่รายงานผิดเป็น `false` — ตาม gotcha ที่ `pirate-force-server#297`
เพิ่งบันทึกไว้) → `merged: true` ทั้งคู่ ยืนยันงานอยู่บน main แล้ว ไม่ต้อง cherry-pick กู้คืน
กล่องจดหมาย: พบไฟล์เดียวที่ไม่มี `.CONSUMED.txt` — ใบที่สาย A เองเขียนไว้รอบก่อน
(`20260830_0830_LANE-A-RE-mob-npc-...`) 🔴 **แก้ไขระหว่างรอบ (pf-adversary จับได้ก่อน commit):**
ฉบับแรกของ stub ปิดใบนี้ว่า "แค่หัวจดหมาย ไม่มีคำสั่งค้าง" ทั้งที่ตัวใบมีข้อ 🔴 ยกงานไว้ให้รอบถัดไปจริง
(index `58` vs `60` สองตารางดูไม่ตรงกัน) — ตามรอยแล้วพบว่า**ไม่ใช่บั๊ก** สองตารางคนละแกน
(placement_index vs Mob-Set number) และตรงกันสมบูรณ์เมื่อแปลงแกนถูก รายละเอียดเต็มใน `.CONSUMED.txt`

## งานหลักรอบนี้

รับช่องโหว่งานขัด 4 ข้อจาก `FROM_CHIEF_R236_TO_ATTENDED_20260830_0855.md` ข้อ ② (เจ้าของสั่งไว้ตอน
GT-131 PASS ว่า "โน้ตไว้ ไม่ใช่ใบด่วน") — ลงมือข้อ 1-2 (สี NPC เขียว→เหลือง, Training Iron Man
ควรชื่อแดง) ก่อน เพราะไม่พึ่ง identity

ผลตรวจสอบ: ทั้งสองข้อชนเพดาน static evidence เดิมที่ปิดไปแล้วสามใบ (`RE-067`/`RE-068`/`RE-109`)
`RE-109` วาง `BUILD_IMPACT: NONE` ห้าม hard-code สีจนกว่าจะมี attended one-field crosswalk ไว้ตรงตัว
ตรวจซ้ำสองข้อเท็จจริงจากซอร์สเอง (ไม่ได้อ้างใบเก่าเฉย ๆ): `NPC_STYLE_ACTOR_TYPE=4` ถูกต้องตามที่
`RE-109` pin ไว้ (ไม่ใช่บั๊ก actor_type) · Training Iron Man ได้ hostile splice ทุกบูตอยู่แล้ว
(เหมือน `GT-032` ที่เคยพิสูจน์ว่าไม่ได้ชื่อแดงจากไบต์ชุดเดียวกัน) ⇒ **ไม่มี field ที่รู้ค่าแล้วเหลือให้ต่อสาย**

ตามกติกาข้อ 2 (ไม่หยุดรอ เปิดใบแล้วเดินต่อ): เปิด `RE-155`
(`ACTOR-NAME-COLOR-NPC-VS-HOSTILE-MOB-ONE-FIELD-CROSSWALK-001`, `CLIENT_RE_QUEUE.md`, +65 บรรทัด)
ขอ attended one-field A/B capture — ทางเดียวที่เหลือหลังสามใบ static ชนเพดาน

**ไม่แก้ src/ รอบนี้** เพราะการเขียนสีตอนนี้จะขัดกับ `BUILD_IMPACT: NONE` ของ `RE-109` เอง —
เลือกความถูกต้องของหลักฐานมากกว่าจำนวนไฟล์ที่แก้

## เทส

`pytest tests/test_field_mobs.py tests/test_mob_death.py tests/test_mob_death_wired_widening.py
tests/test_mob_census_hostility.py tests/test_population.py` — 184 passed, 1 skipped
(ยืนยันโมดูลที่อ่านไม่ถูกแก้และยังเขียว ไม่ใช่ผลจากพฤติกรรมใหม่)

## ถึงกะ attended ถัดไป

`RE-155` ต้องการช่วง capture สั้น ๆ: ยืนที่ placement เดิมของ `GT-131` (identity ยืนยันแล้ว)
ถ่ายภาพฐาน แล้วลองสลับทีละฟิลด์ (`CONSTDATA_TH__FACTION.tsv` แถวนอกช่วง 1-6 ก่อน ตามที่ `RE-109`
เสนอไว้) เทียบภาพ — ผลลบก็ปิดใบได้ (bounded-negative) ไม่ต้องได้ผลบวกเท่านั้นถึงจะปิด

## ยังไม่ได้ทำรอบนี้ (ไม่ใช่ติดเพดาน แค่หมดเวลา)

ข้อ 3 (ทิศทางหันหน้า NPC) จากใบเดียวกัน — chief เรียกว่าน่าสนใจที่สุด และดูเหมือนเป็นข้อมูลที่มีอยู่แล้ว
ในตาราง placement มากกว่าจะเป็นคำถามฝั่งไคลเอนต์ที่ตอบไม่ได้ ควรหยิบรอบหน้า

## CORE-REQUEST

ไม่มี

รายละเอียดเต็ม: `rounds/A_20260830_0939_lg1dvz_npc-mob-name-color-hits-re067-068-109-ceiling-re155-opened.md`
