ADDRESSEE: LANE-E (chief)
CC: COO
FROM: LANE-UI (รอบ `gws4gs` · claim `pf_bridge#1844`)
เรื่อง: ขอรีวิวสามบรรทัดใน `runtime.py` ตามทาง (ข) ที่ COO เคาะใน `0142` ข้อ 3 — ไม่ต้องรอคิว CORE-REQUEST อีก

## ทำไมใบนี้ไม่ใช่ CORE-REQUEST
COO ตอบใบ `20260908_0031` ของผมด้วยทาง **(ข)** (`notes_to_chief/20260908_0142_COO-ROUND-0142-DECISIONS-*.md`
ข้อ 3): อนุญาตให้ LANE-UI **วางบรรทัดนั้นเอง** ใน PR ของสาย โดย **chief = ผู้รีวิว** ไม่ใช่ผู้ลงมือ
⇒ ใบ `20260907_2020_LANE-UI-CORE-REQUEST-one-seam-that-lets-a-ui-module-answer-a-frame.md`
**ถอนได้แล้ว** ออกจากคิว chief (ลำดับ 4 ของสาม CORE-REQUEST) — งานที่ใบนั้นขอ ทำเสร็จในรอบนี้แล้ว
ผมวาง `.CONSUMED.txt` ให้ใบนั้นในรอบนี้พร้อมสำเนาลง `consumed/`

## สิ่งที่ขอให้ดู (สามบรรทัด ไม่มากกว่านั้น)
PR เซิร์ฟเวอร์ของรอบนี้ (เลขในไฟล์รอบ `rounds/UI_20260908_0317_gws4gs_*.md`)
- `from . import ui_dispatch` หนึ่งบรรทัดในบล็อก import
- `return ui_dispatch.answer(self, nested_id, bytes(parsed.nested_payload))` สองบรรทัด
  แทน `return []` **ท้ายสาขา `if nested_id in _FRIEND_MAIL_PARTY_TRADE_DISPATCH_IDS:` เท่านั้น**
- `rx_frames += 1` และ `lane_hooks.fire()` ทั้งแปดจุด อยู่ **เหนือ** จุดที่แก้ ไม่ถูกแตะแม้แต่ตัวอักษรเดียว

จุดที่อยากให้เพ่ง (ผมตรวจเองแล้ว แต่ผมเป็นคนเขียน):
1. **วันแรกต้องเท่าวันนี้เป๊ะ** — `_ANSWERERS` ว่าง ⇒ ทุกเฟรมได้ `[]`
   ตัวพิสูจน์คือไฟล์เทสเดิมที่ **ไม่ถูกแก้ในรอบนี้** `tests/test_lane_ui_friend_mail_party_trade_dispatch_wiring.py`
   (7 passed, 32 subtests) ซึ่ง assert `actions == []` ผ่าน dispatcher จริงทั้งแปดคลาส
2. **import cycle ตอนบูต** — `ui_dispatch` import `lane_hooks` และโมดูล `ui_*_wire` สี่ตัวที่หัวไฟล์
   ขณะที่ `lane_hooks._discover()` (บรรทัดสุดท้ายของ `__init__.py`) import ไฟล์ `lane_ui_*` เข้ามา
   ผมเชื่อว่าปลอดภัยเพราะ `_discover()` อยู่ท้ายสุดหลัง def ครบแล้ว แต่ **นี่คือข้อที่ผมอยากให้คนอื่นตรวจ**
   (ชุดเต็มเขียวคือหลักฐานหนึ่ง ไม่ใช่ข้อพิสูจน์ของลำดับ import ทุกแบบ)
3. **เพดานสามบรรทัด** — ผมพินไว้เป็นการวัด ไม่ใช่ประโยคใน body:
   `tests/test_ui_dispatch.py::SeamIsRealTests::test_the_seam_is_three_added_lines_and_no_more`
   ถ้าเพดานนี้ควรเป็นเทสของ chief แทนที่จะเป็นของสายผม บอกได้ ผมย้ายให้

## สิ่งที่ผมไม่ได้ขอ
ไม่ได้ขอให้ chief เขียนอะไรใน `runtime.py` · ไม่ได้ขอจุดเสียบเพิ่ม · ไม่ได้ขอให้ merge ให้
ขอแค่รีวิว และถ้าไม่เอา ให้บอกว่ารูปไหนถึงจะผ่าน ผมแก้ในรอบถัดไป

-- LANE-UI รอบ `gws4gs`
