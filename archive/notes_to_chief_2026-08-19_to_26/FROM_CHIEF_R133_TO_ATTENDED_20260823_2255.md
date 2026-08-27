# จดหมายจาก chief — R133 · 2026-08-23 22:55 (+07:00)

ถึงคนหน้าเครื่องสะพาน (และ Panya),

## ข่าวเดียวของรอบ: GT-054 พร้อมรันแล้ว

PR #12 ฝั่งโค้ด (reader ชุดส่งมอบ RE — `tools/pf_external_registry.py`) **merge เข้า `main` แล้ว**
(merge commit `1e0b20b` · gate เขียว(Actions run 32645331917 · subset) · ฝั่ง cloud ยืนยันซ้ำ: เทส external 16/16 เขียว(cloud sanity))

⇒ ใบ **GT-054 SPAN-VERIFY-EXTERNAL-REGISTRY** ใน `CLIENT_RE_QUEUE.md` ปลดจาก "รอ merge" เป็น **runnable**
เป็นใบเดียวในคิวที่จบด้วยคำสั่งเดียว:

```
cd <pirate-force-server clone>
git pull
py -3 tools\pf_external_registry.py --verify-spans ..\GameClient\GameClient.local.bin --json
```

**แนะนำรันใบนี้ก่อนหรือขนานใบอื่น** — ผลของมันตัดสินว่า GT-050/052/053 พึ่งตารางส่งมอบได้แค่ไหน
(ก่อนรันยืนยันว่า `git pull` ถึง `1e0b20b` และไฟล์ `tools\pf_external_registry.py` มีจริง)

⚠️ สองข้อที่จะเจอ `REFUSED exit 3` โดยยังไม่ได้รันจริง (อ่านข้อความ REFUSED ก่อนแก้):
- tool บังคับว่า clone `pf_bridge` ต้องเป็น**โฟลเดอร์พี่น้องชื่อ `pf_bridge` เป๊ะ**ข้างโฟลเดอร์ clone เซิร์ฟเวอร์ (เช็คนี้ยิงก่อนเช็คอิมเมจ)
- path อิมเมจต้องชี้ `GameClient.local.bin` ตัวจริง (sha เดียวกับที่ GT-050 พิน)

## ของที่ยังค้างรอฝั่งนั้น (ไม่เปลี่ยนจากรอบก่อน)
1. `git add` 3 ตาราง external ที่เหลือ: `PF_PROTOCOL_PRIORITY.tsv` · `PF_DATA_EVIDENCE.tsv` · `PF_TAG_CENSUS.tsv` (จดหมาย R131)
2. Panya เคาะ whitelist `gamedata/` 188 ตาราง (จดหมาย R132)
3. คิว static: GT-053 -> GT-052 -> GT-050 (+ GT-054 แทรกได้ทุกเมื่อ)

## คำถามค้าง (ไม่บล็อกงาน — ตอบเมื่อสะดวก)
- **สองไฟล์คิวขัดกันใครชนะ:** รอบนี้ adversary จับได้ว่าสารบัญใน `GAME_TEST_QUEUE.md` ยังพูดว่า GT-054 "รอ merge"
  ทั้งที่ `CLIENT_RE_QUEUE.md` ปลดแล้ว — chief แก้บรรทัดสถานะให้ตรงแล้ว (ไม่ใช่ใบใหม่ · precedent R125)
  แต่ขอ Panya เคาะกติกา: เมื่อสองไฟล์ขัดกัน ไฟล์ไหนเป็น authority และการแก้บรรทัดตัวเชื่อมระหว่างพัก attended ทำได้เสมอใช่ไหม
- milestone สำรอง not_started เหลือ 5 แถว แต่ทุกแถวเป็นสถาปัตยกรรมใหญ่/persistence ตารางใหม่
  (mob AI · PvP · chat table · multi-account auth · loot ที่ R118 ปิดไปแล้วบน cloud)
  ⇒ ถ้าอยากให้ cloud เดินแถวไหนระหว่างรอเลนสกิล ขอ Panya ชี้หนึ่งแถว + กรอบที่ยอมให้ตัดสินใจเอง
  ระหว่างนี้ chief จะไม่เปิดเองเพราะเสี่ยงรื้อและโควตาเหลือครึ่งสัปดาห์

## สถานะรอบ
- เลน attended พักตามคำสั่ง 16:56 — ไม่มีใบใหม่ลง `GAME_TEST_QUEUE.md`
- กล่องจดหมายเคลียร์ · ล็อก draft-PR ไม่หลุด · ไม่แตะ repo โค้ด

**ตอนนี้ต้องทำอะไรต่อ (ขั้นเดียว):** เปิดเครื่องสะพานเมื่อไหร่ รัน GT-054 ตามคำสั่งข้างบนแล้ว paste ผลลงจดหมาย

— chief (R133 · wgd504)
