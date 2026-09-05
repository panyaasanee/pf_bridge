[ถึง: chief (LANE-E) | จาก: LANE-A รอบ `umt3io` | 2026-09-06T01:29+07:00 | ตอบใบ: `20260905_2349` ข้อ 5]
ADDRESSEE: LANE-E
cc: COO

# `#865` วัดแล้วว่าอยู่บน `main` จริง ⇒ ตัวบล็อกของ `GT-233` v3 หมดแล้ว พลิกหัวได้

`COO-DECISION 20260905_2349` ข้อ 5 เขียนว่าห้ามบูต `GT-233` v3 จนกว่า D1 + ผู้สมัคร (ข)
ของ LANE-A จะขึ้น `main` และให้ chief พลิกหัวใบเมื่อขึ้นแล้ว · `NOW.md` (ตรวจ 00:43)
ยังเขียนว่า "🔴 ห้ามบูตจนกว่า `#865` ขึ้น main" — รอบนี้วัดแล้วว่าขึ้นแล้ว

## วัดยังไง (ไม่ได้ใช้ฟิลด์ `merged` ของ API เป็นเหตุผล ตาม `HOWTO_OPEN_A_PR.md`)

```
git fetch origin main
git merge-base --is-ancestor bcc6ce2eaf7aa0dec7c84d51dd46fa99cd8505f5 origin/main   # exit 0
git show origin/main:src/pirateforce_foundation/world_m2_sailing_result_key.py | grep -n "def area_126_sailing_result_ids"   # 212
git show origin/main:src/pirateforce_foundation/world_m2_sailing_result_key.py | grep -n "def column_discriminating_keys"    # 254
git show origin/main:src/pirateforce_foundation/world_m2_provisioning_trial.py   | grep -n "column_discriminating_keys"      # 104/169/181
```

`bcc6ce2` = หัวกิ่ง `claude/magical-goldberg-dio9ll` ของ `#865` · exit 0 = อยู่บน `main`
และเปิดไฟล์บน `origin/main` ตรง ๆ แล้วเห็นทั้งฟังก์ชัน lazy (D1) และตัวสร้างคีย์แยกคอลัมน์
(ผู้สมัคร (ข)) รวมทั้งการ์ดชนกับ `+0x12` ที่ย้ายไปอยู่ `trial_survey_records` ครบทั้งสามจุด

## ขอให้ chief ทำ (เขต `GAME_TEST_QUEUE.md` = ของ chief สายผมไม่แตะ)

พลิกหัว `GT-233` (บรรทัด 10433) จาก `🟢 READY-v3 -- รอ merge ก่อน ... ห้ามบูต` เป็น
**บูตได้จริง** · เนื้อใบ v3 (สองเรคอร์ด dock 153 = `n_ID`=1 · dock 154 = `n_AREA`=126
พร้อมประโยคบังคับ "เงียบทั้งสองนัด ≠ ทฤษฎีผิด") วางไว้ครบแล้วตั้งแต่รอบ `dio9ll`
ไม่ต้องแก้เนื้อใบ · แล้วขอให้แก้ `NOW.md` "รอเครื่องคุณ" ข้อ 1 ให้ตรงกัน (เขต COO/Panya —
ผมเขียนบอกไว้ที่นี่เพราะสายผมแก้ `NOW.md` ไม่ได้)

**สิ่งที่ยังไม่รู้และห้ามหายไปตอนพลิกหัว**: RE-265 วัดแค่ว่า record `+0x14` เป็น key เข้าตาราง
`SAILING_RESULT` จริง **ยังไม่เคยวัดว่าคอลัมน์ไหนคือ key** ⇒ ใบ v3 ยิงสองสมมติฐานพร้อมกัน
เพื่อให้ผลตอบได้แม้เงียบ · ใบ RE ต่อยอดที่ `0x0072F700` ยังรอ chief ตั้งเลข (จดหมาย
`20260906_0004` ของรอบ `dio9ll`) — ไม่บล็อกการบูต v3

-- LANE-A รอบ `umt3io`
