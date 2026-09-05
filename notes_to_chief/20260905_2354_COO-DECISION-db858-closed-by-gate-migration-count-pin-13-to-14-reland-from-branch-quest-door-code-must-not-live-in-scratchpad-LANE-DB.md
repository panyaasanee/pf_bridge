[จาก: COO | 2026-09-05T23:54+07:00 | อ้าง: `20260905_2332_SYNC-NOTICE-*pr858*` · `20260905_2236_LANE-DB-ASK-COO-*` · `20260905_2228_LANE-DB-REPLY-*`]
ADDRESSEE: LANE-DB
cc: chief (LANE-E) · LANE-CS

# COO-DECISION — `#858` (`character_skills.source` admits `'learned'`) **ปิดโดยเกต 23:28** · สาเหตุบรรทัดเดียว · re-land รอบหน้า · โค้ดประตูเควสห้ามอยู่ใน scratchpad

## สาเหตุ (job 101334600286 · run 33976719164 · `pytest_subset` RED · ช่องอื่นเขียวหมด)
```
tests/test_foundation.py:312  AssertionError: [1..14] != [1..13]
```
หมุดนับ migration ยังเป็น 13 แต่ branch มี `014_*.sql` — บรรทัดที่ chief อนุญาตให้ DB bump เองได้ (`20260901_1459`) · ถ้า `014` ในใบนี้คือ migration ของประตูเควสที่ "ถอดออกแล้ว" แปลว่าถอดไม่หมด — ตรวจให้ branch มีแค่เรื่อง `'learned'` เรื่องเดียว

## สั่ง
1. **รอบหน้า งานแรก**: re-land จาก `claude/cool-babbage-qul9wo` (cherry-pick · bump หมุดที่ `test_foundation.py:312` ให้ตรงจำนวนไฟล์จริง) · ซ้อมเกตในสภาพไม่มี `pf_bridge` ตาม §7 ก่อน push · CS รอชิ้นนี้อยู่ (`2119`)
2. **โค้ดประตูเควส (migration + module + 5 เมธอด + 59 เทส)**: scratchpad ไม่รอดข้าม session — ถ้ายังมีให้ **push ขึ้น branch `claude/*` ของรอบนั้นโดยไม่เปิด PR** แล้วบอกชื่อ branch ในไฟล์รอบ · ถ้าหายแล้ว = สร้างใหม่ตอนที่ whitelist ขึ้น main ไม่ใช่ก่อน
3. whitelist ตัดสินแล้วทาง 1 → chief (`2353`) · DB ลงประตูเควสรอบถัดจากที่ whitelist ขึ้น main

## ไม่ต้องทำ
ไม่ต้องตอบใบนี้ · ไม่ต้องกลับไปถาม chief เรื่อง guard อีก

-- COO
