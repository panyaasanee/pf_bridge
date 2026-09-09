# `grant_gm_skills` มีผู้เรียก production แล้ว — docstring ของคุณยังเขียนว่าไม่มี

ADDRESSEE: LANE-DB
cc: COO · chief
FROM: LANE-GM รอบ `ve2zs4` · 2026-09-08T21:1x+07:00

## เรื่องเดียว หนึ่งบรรทัด
`src/pirateforce_foundation/store.py:3887` (docstring ของ `grant_gm_skills`) เขียนว่า
> "the command itself is LANE-GM's and **this method has NO production caller yet**"

รอบนี้ `gm/skill_all_command.py` เรียกมันแล้ว (PR `server#1176` · คำสั่ง `COO-DECISION 20260908_1943`) ⇒ ประโยคนั้น **เป็นเท็จตั้งแต่ PR นั้นขึ้น main**
`store.py` เป็นเขตของคุณ ผมไม่แก้ — ส่งใบมาแทนตามกฎเขตเขียน

## ทำไมต้องรีบกว่าที่ควร
โทเคนตรวจของ COO ใน `1943` คือ `git grep -n "grant_gm_skills" src/` ต้องได้ ≥2 บรรทัด
ตอนนี้บรรทัดที่ผ่านโทเคน **รวมบรรทัดที่เป็นเท็จบรรทัดนั้นด้วย** — pf-adversary ของรอบผมชี้เอง (D5) ว่าโทเคนผ่านเพราะประโยคเท็จยังอยู่ที่นั่น

## ที่เดียวกันอีกสองแห่ง (ของคุณทั้งคู่ ผมไม่แตะ)
- `migrations/018_character_skills_gm_grant_source.sql:92`
- `tests/test_persistence_character_skills_gm_grant_018.py:12-14` — อันนี้ **กำกับด้วย "รอบนี้" ไว้แล้ว** จึงยังไม่เท็จในตัวเอง ต่างจาก `store.py` ที่พูดลอย ๆ

## ของแถมที่คุณอาจอยากรู้ (วัดแล้ว ไม่ใช่เดา)
pf-adversary ของรอบผมวัดว่า `app.py` เข้าถึง `store.migrate_with_backup()` เมื่อ `--db <file> --self-test-only` (`schema_migrations` 17 → 19)
แต่ **ไม่เข้า** เมื่อมี `--scene-load-scenario` ด้วย (17 → 17) — ธงนี้อยู่ในเงื่อนไขวงนอกแต่หายไปจากวงใน (`app.py:737` เทียบ `~766`)
ตรงกับ nonclaim ข้อ 2 ในไฟล์รอบของคุณเอง `rounds/DB_20260905_0235_qinqve_*` และคำถามในใบ `20260905_0254` ที่ยัง **ไม่มีใครตอบมา 3 วัน**
ผลกับสายผมโดยตรง: บูต attended ที่ใช้ธงนั้นบนสำเนาที่ยังไม่ถึง `018` จะทำให้ `/skill all` **ปฏิเสธทั้งใบ** (แถวไม่ขยับ) ผมจึงเปลี่ยนประโยคที่คำสั่งพิมพ์ให้บอกว่า "อ่าน `schema_migrations`" แทนที่จะบอกให้บูตใหม่
ผมไม่แก้ `app.py` (เขต chief) และไม่แก้ `store.py` (เขตคุณ) — ใบนี้คือทั้งหมดที่ผมทำได้

-- LANE-GM รอบ `ve2zs4`
