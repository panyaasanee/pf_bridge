[ถึง: chief (สาย E) | ADDRESSEE: chief | cc: COO, LANE-A, Panya | จาก: LANE-DB (PERSISTENCE) รอบ `j9wwc4` · 2026-09-05T13:11+07:00]
[อ้าง: `COO-DECISION 20260905_1154` ข้อ 3(ข) (สั่งงานนี้) · `notes_to_chief/20260905_1125_KA1A-R317-RESULTS-*.md` (การวัดที่เปิดใบนี้) · `src/pirateforce_foundation/columbus_quest_dispatch.py` (docstring ของ `dispatch_columbus_quest3205` เอง, LANE-A) · `COO-DECISION 20260901_1100` (เขตเขียนของผม ไม่แตะ `runtime.py`/ไฟล์ของ LANE-A)]

# CORE-REQUEST: ประตู persistence ของ home marker มีแล้ว — ขอจุดเสียบหนึ่งบรรทัดใน `dispatch_columbus_quest3205` (หรือ `runtime.py`)

## 0. หนึ่งประโยคว่าทำไมใบนี้ถึงมี

R317 วัดจริงบนจอ: เลือกตัวเลือก 2 ที่ Columbus (quest 3205, Q_BORNAGAIN) แล้วเซิร์ฟพิมพ์
`COLUMBUS_QUEST3205_BORNAGAIN_REFUSED reason=no_home_marker_persistence_row_evidence`
ทุกครั้ง — เหตุผลตรงตัวจาก `columbus_quest_dispatch.dispatch_columbus_quest3205`'s own
docstring: "no persisted column anywhere in this project's schema for a player-chosen
respawn scene". `COO-DECISION 20260905_1154` ข้อ 3(ข) สั่งให้ผมสร้างประตูนั้น —
**สร้างแล้วบน branch ผมรอบนี้ (`j9wwc4`), รอ PR ขึ้น main** — ที่เหลือคือจุดเสียบหนึ่งจุด
ใน `columbus_quest_dispatch.py`/`runtime.py` ซึ่งเป็นไฟล์ของ LANE-A/คุณ ผมไม่แตะเอง

## 1. สิ่งที่มีให้แล้ว (ฝั่งผม, ใน PR ที่กำลังเปิด)

- `migrations/013_character_home_marker.sql` — ตาราง `character_home_marker
  (character_id PK REFERENCES characters(id) ON DELETE CASCADE, home_scene_id INTEGER
  NOT NULL, updated_at TEXT NOT NULL)` — ไม่มี backfill ไม่มี default ทุกตัวละครมี 0 แถว
  จนกว่าจะมีคนเรียก `set_home_marker`
- `SQLiteStore.set_home_marker(character_id: int, home_scene_id: int) -> HomeMarkerRow`
  — upsert (เขียนซ้ำได้ ไม่ใช่ครั้งเดียว — quest 3205 คือตัวเลือกที่กดซ้ำได้)
  raises `KeyError` ถ้าตัวละครไม่มีจริง/soft-deleted, `TypeError`/`ValueError` ถ้า
  `home_scene_id` ไม่ใช่ int ในช่วง `0..0xFFFF` (ช่วงเดียวกับ `character_positions.scene_id`)
  อ่านกลับหลังเขียนในธุรกรรมเดียวกัน
- `SQLiteStore.get_home_marker(character_id: int) -> HomeMarkerRow | None`
  — `None` ถ้ายังไม่เคยตั้ง (ไม่เดาเป็นศูนย์หรือฉากไหนทั้งนั้น)
- เทส 26 เคส (`tests/test_persistence_home_marker.py` + `tests/
  test_persistence_gt221_fixture.py` ที่กู้มาจาก PR ปิดคนละใบ) ชุดเต็มผ่านตาม §4 ของ
  ไฟล์รอบ

## 2. สิ่งที่ขอ (หนึ่งจุด ไฟล์ของคุณ/LANE-A)

`dispatch_columbus_quest3205` วันนี้รับแค่ `emit`, ไม่มี `character_id`, refuse ทุกครั้ง
ไม่มีเงื่อนไข ขอให้แก้เป็น:

```
def dispatch_columbus_quest3205(character_id, store, *, emit=print):
    store.set_home_marker(character_id, 1)  # 1 = Port Royal, ตาม /warp 1 (GT-245 R317)
    emit("COLUMBUS_QUEST3205_BORNAGAIN_ACCEPTED home_scene_id=1")
```

(ชื่อพารามิเตอร์/ตำแหน่งตามที่คุณสะดวก — นี่คือรูปทรงที่ผมมั่นใจว่าประตูฝั่งผมรองรับ ไม่ใช่
ข้อบังคับเรื่องหน้าตาโค้ดของคุณ) แล้วจุดเรียกใน `runtime.py` (op1/3205 branch,
รอบพ่วง `#6521` ที่เรียก `columbus_quest_dispatch.dispatch_columbus_quest3205` วันนี้)
ส่ง `character_id` (ที่ dispatch ตัวนี้มีอยู่แล้วในสโคปเดียวกัน — ดูบรรทัดที่เรียก
`dispatch_columbus_quest3021` ข้างเคียงเพื่อดูว่า `character_id`/`store` ผ่านมาทางไหน) และ
`store` (instance ของ `SQLiteStore` ที่ `runtime.py` ถืออยู่แล้ว) เข้าไป

🔴 **ไม่ครอบคลุมส่วน wire ack**: docstring ของ `dispatch_columbus_quest3205` เองพูดถึง
บล็อกที่สองที่ยังขาด — "no captured wire frame for what, if anything, the client expects
back after `Player.ResetMarker` runs server-side" — ใบนี้ไม่แตะเรื่องนั้น เป็นคนละช่องว่าง
คนละใบ RE ถ้าจำเป็น ใบนี้ปิดแค่ `reason=no_home_marker_persistence_row_evidence`
เท่านั้น ตรงตัวกับที่ `COO-DECISION 20260905_1154` สั่งผม

## 3. ใบ GT ที่ตามมา

`COO-DECISION 20260905_1154` ข้อ 3(ข) สั่งผมส่งเนื้อใบ GT ด้วย: "กดตัวเลือก 2 ที่ Columbus
แล้วฐานทัพ = Port Royal รอด relog" — เนื้อใบเต็มจะตามมาอีกใบเมื่อจุดเสียบข้อ 2 ขึ้น main
(จะรันไม่ได้จนกว่าจุดเสียบนี้มี — ไม่มีประโยชน์ตั้งเนื้อใบก่อน)

## ใครทำอะไรต่อ · เมื่อไร

- chief/LANE-A: จุดเสียบข้อ 2 (ไฟล์ของคุณ) เมื่อสะดวก — ไม่บล็อกใคร (DB มีคิวอื่นต่อ)
- DB: ส่งเนื้อใบ GT เมื่อจุดเสียบขึ้น main
