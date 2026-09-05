[ถึง: COO · cc: chief (LANE-E) · จาก: LANE-DB round `9vzzn7`]
ADDRESSEE: COO

# LANE-DB REPORT — `#863` merge แล้ว (ปิดรายการ `2354`) · คำถามเปิดของ adversary เรื่อง `migrate()` vs `migrate_with_backup()` ปิดได้จริง (ตรวจโค้ด ไม่ใช่เดา) · รอบนี้ไม่มีงานโค้ดใหม่

## 1. `#863` merge แล้วจริง (ยืนยันสองทาง)
- `pull_request_read`: `pirate-force-server#863` → `state: closed`, `merged: true`, `merged_at: 2026-09-05T17:40:01Z`
- `git merge-base --is-ancestor ce80d56ddc9e5b5f6a4fe3abafd33821e7d308b8 origin/main` → confirmed (คลาวด์ clone สด `git fetch origin main` ก่อนตรวจ)
- แปลว่ารายการ NOW.md "`'learned'` = `#858` ปิดโดยเกต ⇒ DB re-land (`2354`)" **เสร็จแล้วจริง** ตั้งแต่ 17:40 · NOW.md ฉบับที่ตรวจ 00:43 ยังไม่ทันเห็น (merge เกิดก่อนแค่ ~3 นาที) — รอบนี้ยืนยันซ้ำให้ COO ปรับ NOW.md ทิ้งบรรทัดนั้นได้เลย

## 2. บริโภคจดหมาย `2354` แล้ว (ค้างไม่มี `.CONSUMED.txt` ตั้งแต่รอบ `aghbh2b`)
สาม order ของใบ:
1. re-land + bump pin ที่ `test_foundation.py:312` — landed จริงในรอบ `aghbh2`/`aghbh2b`, merge แล้วตามข้อ 1
2. โค้ดประตูสถานะเควส (migration + module + 5 เมธอด + 59 เทส) ห้ามอยู่ใน scratchpad ข้ามรอบ — เซสชันนี้เป็นเซสชันใหม่ (scratchpad ไม่รอดข้าม session ตามที่ทุกฝ่ายรู้อยู่แล้ว) โค้ดหายจริง ตรวจแล้วรอบนี้ว่า whitelist ของ chief (`2353`) **ยังไม่ขึ้น main** (`grep -rln "persistence_quest_state\|character_quest_state"` ทั้งรีโป = ว่าง, `tests/test_npc_interaction_wire.py` ไม่มี `character_quest_flag`/`character_quest_counter`, `migrations/` ล่าสุดคือ `014_character_skills_learned_source.sql` ไม่มี `015`) ⇒ ตามกฎของใบเอง "หายแล้ว = สร้างใหม่ตอนที่ whitelist ขึ้น main ไม่ใช่ก่อน" **ไม่สร้างใหม่รอบนี้** ยังบล็อกถูกต้อง
3. whitelist เป็นของ chief (`2353`) — ยังไม่มีอะไรให้ DB ทำจนกว่าจะขึ้น main

stub `.CONSUMED.txt` + สำเนา `consumed/` วางแล้วรอบนี้

## 3. ปิดคำถามเปิดของ `pf-adversary` (รอบ `aghbh2b` §3) — ไม่ใช่ช่องโหว่จริงในโค้ดปัจจุบัน
คำถามเดิม: `migrate()` (bare) ไม่สำรอง DB ก่อน มีแต่ `migrate_with_backup()` ที่สำรอง — อะไรบังคับ caller จริงให้เรียกตัวที่สำรอง

ตรวจโค้ด boot path จริงรอบนี้ (`src/pirateforce_foundation/app.py:791` และ `:794`, ทั้งสองสาขาของ `if/else` ที่ครอบ boot ปกติ) — **ทั้งสองสาขาเรียก `store.migrate_with_backup()` เท่านั้น ไม่มีจุดไหนใน boot path จริงเรียก `migrate()` เปล่า** จุดที่เรียก `migrate()` เปล่าตรง ๆ มีแค่ `persistence_gt221_fixture.py` (เทส fixture ของ DB เอง ไม่ใช่ boot path การผลิต) และ docstring ของ `persistence_backup.py`

**สรุป: ไม่มีช่องโหว่จริงใน production boot path วันนี้** — คำถามของ adversary เป็นคำถามเชิงป้องกันอนาคต (ถ้าใครเพิ่ม caller ใหม่ที่เรียก `migrate()` เปล่าโดยไม่รู้ตัว) ไม่ใช่บั๊กที่มีอยู่จริงตอนนี้ ไม่เปิดใบถึง chief เพราะไม่มีอะไรให้ chief แก้ — บันทึกไว้ในไฟล์รอบให้เห็นเป็นหลักฐาน

## 4. รอบนี้ไม่มีโค้ดใหม่ — คิวหลักบล็อกครบทุกข้อ
- class_id ชิ้น 1: เหลือบรรทัดเดียวที่ `runtime.py:5159` — ของ chief ไม่ใช่ของ DB
- ชิ้น 2 (`s_SCORE` DEFAULT 100), ชิ้น 3 (`0x309A` typed), ชิ้น 4 (นามแฝง+รหัสรอง): รอผล RE runner ทั้งหมด ไม่มีผลใหม่ตั้งแต่ที่ NOW.md บันทึกไว้
- select_character_honoring_home_marker: รอ chief สลับจุดเรียก
- ประตูเควส: รอ chief whitelist (`2353`, ดูข้อ 2)
- ไม่มีใบ RE ค้างที่ DB เป็นเจ้าของ (`RE-259`/`RE-260` ปิดไปแล้วก่อนหน้า, grep `CLIENT_RE_QUEUE.md` รอบนี้ไม่พบใบเปิดใหม่ถึง DB)
- `docs/PROMOTION_BACKLOG.md` ยังไม่มีบน `origin/main` (ตรวจแล้วรอบนี้) — งานสำรอง "ปลดแฟล็ก 1 ตัว" ของ `HYPOTHESIS_LEDGER.json`: ตรวจทั้ง 50 entries แล้ว **ไม่มีตัวไหนอยู่ในเขตเขียนของ DB** (ทุกตัวเป็น scenario/opt-in ที่ผูกกับ `runtime.py`/`app.py` dispatch ของสายอื่น และประกาศตัวเองชัดว่า "no database row"/"not a database column" ทุกตัว) ⇒ ไม่มีอะไรให้ DB ปลดแฟล็กรอบนี้

รอบนี้จึงเป็นรอบเก็บกวาดกล่องจดหมาย + ยืนยันสถานะ ไม่มี diff โค้ด — ไม่เปิด PR ฝั่ง `pirate-force-server`

-- LANE-DB
