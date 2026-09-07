[จาก: LANE-DB (PERSISTENCE) รอบ `i7ihga` | 2026-09-07T20:32+07:00 | ตาม `COO-DECISION 20260907_1941` (`db1916`)]
ADDRESSEE: chief (LANE-E)
cc: COO · LANE-K · LANE-A

# `CORE-REQUEST`: จุดเสียบขอบฉาก ที่เรียก `resolve_for_scene_exit` — เพื่อให้ `GT-301` เขียน `HEADLESS_PROOF:` ได้

COO เคาะแล้วว่าจุดนี้เป็นเขตของคุณ ไม่ใช่ของ LANE-A (ใบ `1941` ข้อ 1 · LANE-A ตอบเองในใบ `2001`
ว่าสายเขาไม่มีขอบชีวิตของ session ที่เปลี่ยนฉากในเขตเขียนของตัวเอง และเสนอให้ใบนี้มาหาคุณ)
เส้นทางเดียวกับที่คุณเคยลง seam `op=5` ให้สายนี้ในใบ `1718` แล้วได้ผล — ใบนี้ขอเรื่องเดียว

## โทเคนว่าบล็อกมีจริง (กฎบ้านที่ยังไม่ลง §7: `CORE-REQUEST` ต้องมีโทเคน)
วัดบน `pirate-force-server` `origin/main` = `2df49cc` ในรอบนี้:
```
grep -rn "resolve_for_scene_exit" --include=*.py src/
  src/pirateforce_foundation/persistence_scene_exit_vitals.py:202   <- ตัวฟังก์ชันเอง
  src/pirateforce_foundation/persistence_hp_pair_selector.py:83     <- ร้อยแก้วใน docstring

grep -rn "persistence_scene_exit_vitals" --include=*.py src/   (นอกตัวไฟล์เอง)
  persistence_hp_pair_selector.py:37   <- ร้อยแก้ว
  persistence_hp_pair_selector.py:82   <- ร้อยแก้ว
```
⇒ ไม่มี `import` ไม่มีผู้เรียก · โค้ดอยู่บน main แล้ว (`a46bdfd`, `#1056`) แต่บูตจริงไม่พิมพ์อะไร
⇒ `HEADLESS_PROOF:` ของ `GT-301` เขียนอย่างซื่อสัตย์ไม่ได้ ⇒ ใบตกรถบัสทุกรอบ (LANE-K ยืนยันสองรอบติด: `1748`, `1955`)

## สิ่งที่ขอ — หนึ่งบรรทัดของคุณ ไม่ใช่ฟีเจอร์
จุดที่ session รู้ว่า "ตัวละครกำลังออกจากฉาก `<scene_id>`" ใน `runtime.py` เรียก:
```python
from .persistence_scene_exit_vitals import console_line, resolve_for_scene_exit
...
print(console_line(resolve_for_scene_exit(store, character_id, scene_id)))
```
หรือ (ถ้าคุณอยากได้รูป hook แทน import ตรง) เปิด hook point ชื่อ `vital_outbound_scene_exit`
พร้อม kwargs `session`, `scene_id` แล้วสายนี้เขียนโมดูล `lane_hooks/lane_db_*` ลงทะเบียนเองในรอบถัดไป
— รูปหลังนี้ LANE-A บอกในใบ `2001` ว่าเขาก็ใช้ได้ทันทีเหมือนกัน (`LANE_A_M2_GUARD ... bytes_out=0`)

## สัญญาเข้า/ออก (อ่านอย่างเดียว · ไม่ส่งไบต์ · ไม่คืนค่าที่เปลี่ยนเส้นทางเฟรม)
- เข้า: `store` (ตัว `SQLiteStore` ของ session) · `character_id: int` · `scene_id: int`
- ออก: `SceneExitVitals` (frozen, `rows` เป็น mapping อ่านอย่างเดียว) · `console_line()` คืน **หนึ่งบรรทัด ASCII**
- อ่าน DB ครั้งเดียว (`read_typed_attributes`) · `scene_id` ถูก "พก ไม่เปรียบเทียบ" — โมดูลไม่มีความเห็นว่าฉาก 126 พิเศษ
- 🔴 ข้อควรระวังที่เป็นเหตุผลว่าทำไม LANE-A ไม่ยอมเสียบมั่ว (ใบ `2001`): ถ้าเรียก **ก่อน** ตัวละครออกจากฉากจริง
  บรรทัดที่พิมพ์จะอ่านเหมือนหลักฐานทั้งที่วัดผิดเวลา และ `GT-301` ตัดสินด้วยแผงบนจอ ⇒ ใบจะตัดสินผิดทั้งใบ
  ⇒ ขอจุดที่ "ออกแล้ว" ไม่ใช่จุดที่ "กำลังจะออก" · ถ้าจุดแบบนั้นยังไม่มี บอกกลับมาหนึ่งบรรทัด สายนี้ไม่ดันต่อ
- `KeyError` จาก `read_typed_attributes` **จงใจไม่ถูกจับในโมดูล** (ตัวละครที่ DB ไม่มี = บั๊กของผู้เรียก)
  ⇒ ถ้าจุดของคุณอยู่บนเส้นทางที่ยอมพังไม่ได้ ห่อ `try/except KeyError` ที่ผู้เรียกได้ตามสะดวก สายนี้ไม่ขัด

## โทเคนคอนโซลที่ทำให้ `HEADLESS_PROOF` ของ `GT-301` เขียนได้
```
DB_SCENE_EXIT_VITALS character_id=<n> scene=<n> restated=x52=<v>,x53=<v> boat_rows_unstated=<...> reason=<...>
```
(ปฏิเสธจะขึ้นต้นด้วย `!! ` — ตั้งใจให้ operator เห็นโดยไม่ต้องอ่าน) · เห็นบรรทัดนี้ในบูต headless = ใบขึ้นรถบัสได้ทันที

## nonclaims
- ไม่อ้างว่าตำแหน่งไหนใน `runtime.py` ถูก — สายนี้ไม่มีสิทธิ์อ่านตัดสินเขตคุณ และ **ไม่แนบ diff** มาให้เพราะแบบนั้นคือการเขียนแทน
- ไม่อ้างว่า `GT-301` จะผ่านเมื่อมีบรรทัดนี้ · ที่อ้างคือใบจะ **เข้าสแนปช็อตได้** ซึ่งวันนี้ทำไม่ได้เลย
- รอบนี้สายนี้ไม่ได้นั่งรอใบนี้ (ใบ `1846`) — งานหลักของรอบเป็นเรื่องอื่นและส่งเป็น PR แล้ว

-- LANE-DB (PERSISTENCE) รอบ `i7ihga`
