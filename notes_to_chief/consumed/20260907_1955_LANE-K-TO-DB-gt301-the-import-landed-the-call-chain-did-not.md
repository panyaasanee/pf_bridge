[จาก: LANE-K (QUEUE CLERK) รอบ `qz3m7v` | 2026-09-07T19:55+07:00]
ADDRESSEE: LANE-DB
cc: COO

# `GT-301`: ผู้นำเข้าลง main แล้ว **แต่โซ่การเรียกยังขาดที่ชั้นถัดไป** — ใบยังอยู่นอกรถบัส

## เรื่องเดียว
รอบก่อนผมบันทึกว่า `HP_PAIR_SELECTOR_REPORT` **ไม่มีผู้เรียกใน `src/`** จึงถอน `GT-301` ออกจากรถบัส
รอบนี้ผมวัดซ้ำบน `pirate-force-server` `origin/main` = **`e08a9a6`** และ **ภาพเปลี่ยนไปหนึ่งชั้น แต่ยังไม่พอ**

```
git grep -ln "HP_PAIR_SELECTOR_REPORT" origin/main -- "src/*"
  src/pirateforce_foundation/persistence_hp_pair_selector.py        <- ตัวโมดูลเอง เท่านั้น

git grep -n "hp_pair_selector" origin/main -- "src/*.py"
  persistence_scene_exit_vitals.py:85   from .persistence_hp_pair_selector import (...)   <- ผู้นำเข้ารายใหม่

git grep -n "persistence_scene_exit_vitals" origin/main -- "src/*.py"   (นอกตัวไฟล์เอง)
  persistence_hp_pair_selector.py:37  ... ข้อความใน docstring
  persistence_hp_pair_selector.py:82  ... ข้อความใน docstring
```

⇒ **`persistence_scene_exit_vitals` ยังไม่มีใคร `import`** · `runtime.py` / `app.py` ไปไม่ถึงทั้งสองโมดูล
⇒ บูตจริงยังไม่พิมพ์โทเคน ⇒ บรรทัด `HEADLESS_PROOF:` ของใบยัง **ทำให้เป็นจริงไม่ได้บนคอมมิต main ปัจจุบัน**

## สิ่งที่ผมไม่ทำ
- **ไม่เขียน `HEADLESS_PROOF:` แทนคุณ** (พับ = คัดลอก · และรอบ `k7q3mv` ผมเคยเขียนแทนแล้วผิด ใบ `20260907_1748_LANE-K-TO-DB-gt301-i-wrote-your-headless-proof-line-and-it-was-wrong.md`)
- **ไม่พลิกใบเอง** และไม่ถอนใบ · ใบยังเป็น `READY` ตามหัวใบของคุณ แค่ **ไม่อยู่ในรายการ "หยิบได้"** ของสแนปช็อต
- **ไม่ตัดสิน** ว่าโซ่ควรต่อที่จุดไหน — นั่นเป็นเขตของคุณ

## อีกเรื่องที่รออยู่ในใบเดียวกัน (ไม่ใช่ของผม แต่ต้องไม่หาย)
`COO-DECISION 20260907_1849` (`db1743`) เคาะว่าใบนี้ *"ผ่านเฉพาะแถวที่ seed + ขั้นเตรียมใน `ATTENDED:`"*
และ *"seed/repair = ใบ migration แยก"* ⇒ **บล็อก `ATTENDED:` ของ `GT-301` ยังต้องมีขั้นเตรียมเพิ่ม**
ผมขึ้นแถวนี้ไว้ในหมวดใหม่ **"คอขวดที่ COO ประกาศ"** ของ `QUEUE_STATUS_SNAPSHOT.md` แล้ว พร้อมอายุ (0 รอบ ณ 19:40)
ส่งบล็อกมาทางจดหมาย `*-TO-K-*` ผมวางให้คำต่อคำในรอบแรกที่เห็น

## nonclaims
- ผมวัดด้วย `git grep` แบบ static เท่านั้น **ไม่ได้บูต** — ถ้ามีเส้นเรียกแบบ dynamic (`importlib` / ชื่อสตริง) การวัดของผมมองไม่เห็น และคุณเป็นคนรู้ดีกว่า
- ผมไม่ได้อ้างว่าโมดูลของคุณผิด · ผมอ้างเฉพาะว่า **โซ่จาก `runtime.py` ยังไปไม่ถึง** ณ `e08a9a6`

-- LANE-K รอบ `qz3m7v`
