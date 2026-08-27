[จาก: chief cloud (cc) รอบ R131 · session exciting-goldberg-0dcmm7 · ถึง: ผู้ช่วย/คนหน้าสะพาน และ Panya]

# R131: โค้ดอ่านชุดส่งมอบ RE ตัวแรกเสร็จแล้ว (รอ gate) · ขอ `git add` 3 ตารางท้าย · ใบใหม่ GT-054

**เวลา:** 2026-08-23 ~21:3x (+07:00) · บันทึกรอบเต็ม: `rounds/R131_0dcmm7_external_re_reader_and_span_verify_ticket.md`

## ผลรอบนี้ (สั้น)

1. ✅ **จดหมาย 20:39 บริโภคแล้ว** — เห็นคำตัดสิน Panya (push ทั้งไฟล์ ไม่ mask + เส้นใหม่เรื่อง proprietary) ครบ
2. ✅ **สนองข้อ ⑤ ของทั้งสองใบ:** สร้าง `pirate-force-server/tools/pf_external_registry.py` = โค้ดตัวแรกที่อ่าน
   ตารางชุดส่งมอบใน `pf_bridge/external/` — pin sha256/rows/header ทั้ง 5 ตาราง · cross-check 6 invariant ที่วัดจริงก่อน pin ·
   โหมด `--verify-spans` เตรียมไว้ให้เครื่องสะพาน (cloud ไม่มีอิมเมจ — ปฏิเสธเปิดเผย exit 3 ไม่เนียนเขียว)
   + เทส 16 ใบ · precondition key ใหม่ (`external_re_tables` · เครื่อง gate ไม่มี repo พี่น้อง ⇒ skip แบบประกาศ+pin 12)
   · **เขียว(cloud sanity) 1917 passed / 324 skipped / 0 failed · census PASS** · ผ่าน pf-adversary ก่อน commit
   (พบ 6 defect แก้ครบ — ตัวร้ายสุดคือไฟล์เทสมีคำว่า `GameClient` แล้ว gate จะ `--ignore` ทั้งโมดูลเงียบ ๆ · รายละเอียดในบันทึกรอบ)
   · **PR ฝั่งโค้ดเปิดแล้ว รอ gate** — merge เมื่อเขียวโดย workflow ตามปกติ
3. 🆕 **ใบ GT-054 SPAN-VERIFY-EXTERNAL-REGISTRY** เข้า `CLIENT_RE_QUEUE.md` — รัน span verification กับอิมเมจบนสะพาน
   หนึ่งคำสั่ง (`py -3 tools\pf_external_registry.py --verify-spans ..\GameClient\GameClient.local.bin`)
   คาด `spans=392 verified=392 mismatched=0 unreadable=0` · 🔴 **รอ merge ฝั่งโค้ดก่อน** (เขียนกำกับในใบแล้ว)
4. ✅ `.gitignore` ของ `pf_bridge` whitelist 3 ตารางท้ายแล้ว (ชื่อตามที่จดหมาย 20:39 ยืนยัน) — ดูข้อขอด้านล่าง
5. สารบัญคิว + บล็อกสถานะใน `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md` อัปเดตตามจริงแล้ว (บรรทัด "ยังไม่มีโค้ดอ่าน" ปลดแล้ว)

## 📌 สิ่งที่ขอจากฝั่งสะพาน (ขั้นเดียว สั้น)

**`git add` รายไฟล์ 3 ตารางท้ายใน `pf_bridge\external\` แล้วปล่อยท่อ sync ตามปกติ:**
```
git add -- external/PF_PROTOCOL_PRIORITY.tsv
git add -- external/PF_DATA_EVIDENCE.tsv
git add -- external/PF_TAG_CENSUS.tsv
```
whitelist ใน `.gitignore` รอไว้แล้ว (merge รอบนี้) ⇒ สามคำสั่งนี้ไม่ควร error · หลังขึ้น `main` เลนชุดส่งมอบเปิดครบ 8/8
🔴 ตามคำเตือนของผู้ช่วยในจดหมาย 20:39: **อย่า add ไฟล์ `.py` ในโฟลเดอร์นั้น** จนกว่าจะตรวจแยกอีกรอบ

## 📌 ถึง Panya — ถ้อยคำกฎเหล็กใหม่ (ขอให้วางใน prompt ของ Routine เอง)

จดหมาย 20:39 ขอให้แก้กฎ "ห้ามอัปโหลด proprietary" ให้ตรงเส้นที่คุณเคาะ — **cc แก้ prompt เองไม่ได้**
(กติกา v4: คุณเป็นคนสร้าง/แก้ routine) ⇒ ถ้อยคำแทนที่ เตรียมพร้อมวาง:

> **ห้ามอัปโหลดเด็ดขาด:** `GameClient*.bin` ทั้งไฟล์ · capture corpus · `.dmp` · canonical DB
> **ขึ้น remote ได้:** metadata ที่ derive มา — VA · file offset · span · sha256 · ตารางฟิลด์ · ตัวนับ ·
> รวมถึงสตริงไบต์คำสั่งสั้น ๆ ที่ฝังในตารางวิเคราะห์ (Panya เคาะ 2026-08-23 20:39)
> **ห้ามใครขยายเส้นนี้เองอีก** — เพิ่มข้อจำกัดต้องให้ Panya เคาะก่อน พร้อมจดวันเวลา

## ทำไมรอบนี้ไม่มีใบเทสเกมใหม่ (กติกา v5 ⑤)

เลน attended พักทั้งหมดตามคำสั่งคุณ 16:56 และของที่รอบนี้ผลิตเป็นเครื่องมือฝั่ง cloud/สะพานล้วน —
ของที่ต้องใช้เครื่องคนไปลง `CLIENT_RE_QUEUE.md` เป็น **GT-054** แล้ว (คิว static ขนานกับคิวเกมได้ ไม่แย่งกัน)

## ตอนนี้ต้องทำอะไรต่อ (ขั้นเดียวต่อคน)

- **คนหน้าสะพาน:** `git add` สามไฟล์ข้างบน · แล้วเมื่อเห็น PR โค้ด R131 merge → หยิบ **GT-054** ได้เลย (คำสั่งเดียวจบ)
- **Panya:** วางถ้อยคำกฎเหล็กใหม่ลง prompt เมื่อสะดวก — ไม่มีอะไรบล็อกงานระหว่างรอ

## nonclaims

- ยังไม่ได้พิสูจน์ว่าตารางชุดส่งมอบตรงกับอิมเมจจริง — นั่นคือหน้าที่ GT-054 (cloud ตรวจได้แค่ internal consistency + sha ไฟล์)
- เขียว(cloud sanity) ≠ เขียว gate — PR ฝั่งโค้ดรอ Actions ตัดสิน · GT-054 ยังรันไม่ได้จนกว่า merge
