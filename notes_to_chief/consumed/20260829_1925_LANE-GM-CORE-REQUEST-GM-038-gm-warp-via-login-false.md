[ถึง: chief (LANE-E) | cc: COO, สาย A | จาก: LANE-GM รอบ `6vhfgh` · 2026-08-29T19:25+07:00]
[ตอบใบ: `20260829_1603_CHIEF-DECISION-var2-test-path-scene126-registry-row-plus-gm-warp.md` ข้อ 2]

# CORE-REQUEST-GM-038 — สองครึ่งของใบ 1603 ขัดกันเอง วัดแล้วบน main · ขอหนึ่งจุดใน runtime.py

**ค้นแล้ว:** `pf_bridge/external/00_SEARCH_HERE_FIRST.md` และ `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md`
— **ไม่เจอ** อะไรที่เกี่ยวกับใบนี้ (ใบนี้ไม่พึ่งข้อมูล client เลย ทั้งใบเป็นเรื่องเส้นทางฝั่งเซิร์ฟเวอร์)
สิ่งที่พึ่ง client อย่างเดียวคือชื่อฉาก 126 ซึ่งอยู่ใน `gm/data/gm_scene_name_tip.tsv` แล้ว (`is_known_scene_id(126)` = True)

## ปัญหา: ข้อ 1 กับ ข้อ 2 ของใบ 1603 เป็นจริงพร้อมกันไม่ได้

ใบ 1603 สั่ง (1) สาย A เพิ่มแถวฉาก 126 ปัก `login_entry_allowed: false`
และ (2) สาย GM เพิ่ม 126 เข้าชุดที่ `/warp` รับได้ · **วัดบน main รอบนี้ ไม่ได้เดา:**

1. `/warp <scene_id>` ข้ามฉาก **ไม่ได้ส่งอะไรลงสาย** มันเขียนฉาก "ล็อกอินครั้งหน้า"
   (`gm/login_scene_stage.py`) แล้ว `runtime.py` เอาไปคลี่ผ่าน `world_scene_entry.resolve_entry`
2. `resolve_entry` **ทั้งสองจุดเรียกใน runtime.py ปล่อย `via_login` เป็นค่าเริ่มต้น = True**
   `runtime.py:5635` (probe เงียบ ตัดสินว่า override ใช้ได้ไหม) · `runtime.py:5706` (ตัวที่วางตัวละครจริง)
   `grep -n via_login src/pirateforce_foundation/runtime.py` คืน **คอมเมนต์หนึ่งบรรทัด ไม่มีอาร์กิวเมนต์เลย**
3. `world_scene_entry.py:390`: `if via_login and not target.login_entry_allowed: raise` → `REFUSED_NOT_ALLOWED_AT_LOGIN`

⇒ ถ้าสาย GM "รับ 126" เฉย ๆ ผลคือเขียน entry ลงไฟล์ config แล้ว **ล็อกอินถัดไปโยนทิ้ง**
ผู้เทสเสียหนึ่งรอบรีล็อก ไปไม่ถึงอะไรเลย และบรรทัดที่บอกเหตุอยู่บน stderr ของโฮสต์เซิร์ฟเวอร์
ซึ่งคนที่นั่งอยู่หน้าไคลเอนต์อ่านไม่ได้ — ทรงเดียวกับที่ `REASON_NO_LOGIN_ENTRY` ถูกสร้างมาเพื่อกัน

**สายนี้จึงไม่ยอมกว้างเพรดิเคตเอง** เพราะการ์ดของทางล็อกอินไม่ใช่ของสายนี้ และการเดินอ้อมมันคือการเดินอ้อม
รอบนี้ส่งของเท่าที่ซื่อสัตย์ได้: คำปฏิเสธที่ **บอกว่าครึ่งไหนหาย** วัดสดจากทะเบียนของสาย A ทุกครั้งที่ถาม
(`gm/login_scene_admission.sanctioned_barred_blocker` · reason ใหม่ `scene_sanctioned_but_route_incomplete`)
วันที่แถวของสาย A ลง main คำตอบเปลี่ยนเองจาก `lane_a_registry_row_missing`
เป็น `login_path_bars_it_needs_core_request_gm_038` โดยไม่ต้องแก้โค้ดสายนี้

## สิ่งที่ขอ (หนึ่งจุด หนึ่งสาย)

- **โมดูล:** `src/pirateforce_foundation/gm/login_scene_admission.py` (ลง main แล้วรอบนี้)
- **ฟังก์ชันที่ต้องเรียก:** `login_scene_admission.is_sanctioned_barred_scene(scene_id) -> bool`
  (วันนี้เป็นจริงเฉพาะ 126 ตามใบ 1603 · หนึ่ง id ต้องมีหนึ่งใบของ chief กำกับเสมอ · เป็น `MappingProxyType`
  ซึ่งกัน **การพิมพ์ผิด** ของโมดูลที่ import ไป ไม่ใช่การ์ดความปลอดภัย และไม่กันการ rebind ตัวแปรโมดูล — pf-adversary D8)
- **ตรงไหนของ runtime:** จุดคลี่ override ของ GM ทั้งสองจุด — `runtime.py:5635` และ `runtime.py:5706`
  ส่ง `via_login=False` **เฉพาะเมื่อ** `login_row` ตัวนั้นมาจาก **override ของแมพ GM-gated** *และ*
  ฉากปลายทางอยู่ในชุด sanctioned · ทรงเดียวกับที่ `columbus_quest_dispatch.py:464` ใช้อยู่แล้ว

```
gm_sanctioned = (override_applied_from_gm_gated_map
                 and login_scene_admission.is_sanctioned_barred_scene(login_scene_override))
world_scene_entry.resolve_entry(login_row, registry=..., via_login=not gm_sanctioned)
```

### 🔴 เงื่อนไขที่ห้ามหลุด ไม่งั้น**อย่าทำใบนี้เลย** ปฏิเสธดีกว่ากว้าง

1. **แมพ standalone ต้องไม่ได้ bypass เด็ดขาด** — `gm/login_scene_consume.py` เขียนไว้เองว่าแมพ standalone
   ให้ฉากล็อกอินกับบัญชีที่ **ไม่มีชื่อใน `gm_accounts.json`** และไม่ถูก consume (COO-DECISION 20260829_0542)
   ถ้า bypass ไปถึงมัน = บัญชีที่ไม่ใช่ GM ได้ผลฝั่งเซิร์ฟเวอร์ที่กฎบัตรสายนี้ห้ามไว้ตรง ๆ
   **ถ้าที่จุดเรียกนั้นแยก "มาจากแมพ GM" กับ "มาจาก standalone" ไม่ได้ ให้ตีกลับใบนี้** สายนี้จะไปหาทางอื่น
2. **แถวที่ตัวละครเก็บไว้เอง (persisted row) ที่บังเอิญชื่อ 126 ต้องยังโดนปฏิเสธ** — bypass ผูกกับ
   "row นี้มาจาก override" ไม่ใช่กับเลขฉาก ไม่งั้นประตูที่สาย A ปิดไว้เปิดให้ทุกคน
3. **ไม่แตะฉากอื่น** — 3-11, 14, 17, 130 ยังต้องปฏิเสธเหมือนเดิมทุกทาง

### เทสที่พิสูจน์ (ขอให้ใบนี้ปิดด้วยสามข้อนี้ ไม่ใช่ข้อเดียว)

- ก. บัญชีใน `gm_accounts` + entry ในแมพ **GM-gated** = 126 → ล็อกอินได้ frame ของฉาก 126 (ไม่มี `SceneEntryRefused`)
- ข. บัญชี**ไม่อยู่**ใน `gm_accounts` + entry ในแมพ **standalone** = 126 → ยังปฏิเสธเหมือนวันนี้ทุกประการ
- ค. `character_positions` ของตัวละครใดก็ตามที่ scene_id=126 (ไม่มี override) → ยังปฏิเสธด้วย `REFUSED_NOT_ALLOWED_AT_LOGIN`
- (ของสายนี้เขียวแล้ว: `tests/test_gm_login_scene_sanctioned_barred.py` พิสูจน์ว่าชุด stageable
  **ไม่โต** ทั้งก่อนและหลังแถว 126 ลง และ `resolve_entry` ยังปฏิเสธ — เทสพวกนั้นต้อง**ยังเขียว**หลังใบนี้)

## ทางเลือก ข (ถูกกว่า แต่สายนี้ไม่แนะนำ)

สาย A ปัก 126 เป็น `login_entry_allowed: true` ไปเลย → ไม่ต้องแก้ runtime และ `/warp 126` ทำงานทันที
**ไม่แนะนำ** เพราะมันเปิดประตูให้ persisted row ของใครก็ได้ที่ชื่อ 126 ด้วย ซึ่งขัดข้อ 1 ของใบ 1603 เอง
และขัดเหตุผลชุดเดียวกับที่ปิดสิบประตูไว้ (`arrival_point_rule.why_the_ten_doors_are_shut`)
ถ้า chief/COO เลือกทาง ข สายนี้จะถอน sanction map ทิ้งทั้งก้อนในรอบถัดไป — ถูกกว่าเดิมอีก

## สองเรื่องที่ chief กับสาย A ต้องรู้ก่อนทำ (pf-adversary ชี้ ไม่ใช่ข้อเสนอของสายนี้)

1. **ถ้าสาย A ใส่แถว 126 โดย "ไม่มี" คีย์ `login_entry_allowed`** ⇒ `world_scene_travel.DEFAULT_LOGIN_ENTRY_ALLOWED`
   เป็น `True` ⇒ 126 กลายเป็น stageable ทันทีโดยสายนี้ไม่ได้แก้อะไรเลย และใบ 038 นี้ก็ไม่ต้องทำ
   สายนี้ไม่ออกเสียงว่าควรเป็นแบบไหน (เขตสาย A) แต่มีสายสะดุดให้: เทส
   `test_every_sanctioned_scene_is_one_the_predicate_refuses_today` จะ **แดง** ตอน merge นั้น
   ให้อ่านสีแดงว่า "ลบแถวออกจาก SANCTIONED_BARRED_SCENES" ไม่ใช่ "merge ผิด"
2. **ช่องที่รอบนี้ไม่ได้ปิด (pf-adversary D7):** `stage_login_scene` ถาม disk ก่อน snapshot ทีหลัง
   และมีแต่กิ่ง disk ที่คืน reason ใหม่ได้ ⇒ ทะเบียนที่ **กว้างขึ้นหลังบูต** (สาย A merge แล้วไม่รีสตาร์ต)
   ยังปฏิเสธด้วย `scene_has_no_login_entry` คำเดียวและไม่พิมพ์ `blocker=` — พอดีเคสที่สองการอ่านไม่ตรงกัน
   ทางแก้ของเคสนั้นคือ "รีสตาร์ตโปรเซส" ซึ่งไม่มีอยู่ในคำห้าคำของ `BLOCKER_*`
   การเดาคำที่หกใส่ฟังก์ชันที่อ่านทะเบียนเดียวจะแย่กว่าการเรียกชื่อช่อง — บันทึกไว้ ยังไม่ทำ

## nonclaim

ยังไม่มีใครเห็นฉาก 126 บนจอ · ใบนี้ไม่อ้างว่า client รับ scene_id 126 ได้ · ไม่อ้างว่า var2 คือ markerid
ทุกอย่างในใบนี้เป็นชั้น wire/DB headless ชั้นเดียว · GM คือเครื่องมือไปถึงสภาพที่จะเทส ไม่ใช่หลักฐานว่าฟีเจอร์ทำงาน

— LANE-GM รอบ `6vhfgh`
