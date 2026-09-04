# LANE-GM round ydlvtt (2026-09-04T17:54+07:00)

## NOW: รอบนี้ขยับข้อไหน

**ไม่ขยับ CHARTER-02/บันไดไมล์สโตนโดยตรง** (M2 ยังคงเดิม รอ provisioning trial แล้ว attended)
รอบนี้ปิดข้อ 2 ของ `COO-DECISION 20260904_1646` (ตอบใบ `1620`/`1652` ของรอบ `q3cde9`
ที่ทำให้ `pirate-force-server#745` ขึ้น main ไปแล้วก่อนรอบนี้เริ่ม) — งานชิ้นแรกที่กติกา NOW
สั่งไว้: "ADVERSARY_PENDING #745 = งานชิ้นแรกของรอบ 17:41" ทำครบแล้ว (ดูหัวข้อ "ผล adversary #745"
ด้านล่าง) ไม่มีข้อไหนใน `## รอ Panya ติ๊ก` ที่รอบนี้แตะ

## ต้นรอบ: ตรวจล็อกและชะตา PR รอบก่อน (AGENTS.md §7 ข้อ 1 + Addendum A)

- list PR open ทั้งสองรีโปที่ขึ้นต้น `[LANE-GM]` ก่อนแตะโค้ด — **ไม่พบ** ใบไหนทั้งสองรีโป
  (ตรวจซ้ำอีกครั้งหลัง merge main ขยับ ก่อนเปิด claim — ยังไม่พบ) ⇒ ไม่มีล็อกให้ถอย ไม่มีใบผีให้ยึด
- PR ล่าสุดของสาย GM ที่ `state=closed`: `pirate-force-server#745` —
  **`merged=true`** (`merged_at` 2026-09-04T10:24:23Z = 17:24:23+07) ⇒ งานอยู่บน `main` แล้ว ไปต่อ
  (ไม่ต้อง cherry-pick อะไรกลับ)

## ผล adversary `#745` (งานชิ้นแรกตามกติกา NOW / `COO 1646` ข้อ 4)

`#745` merge ไปแล้วก่อนรอบนี้เริ่ม พร้อมตัวแก้ D1/D2/D5/D6/D7 ที่ pf-adversary ครั้งที่ 1/2
(รอบ `q3cde9`) จับได้และแก้ในรอบเดิม (ดูใบ `1652` และ `docs/GM_LANE.md` หัวข้อ "รอบ q3cde9")
สิ่งที่เหลือค้างจาก `1646` คือ **ข้อ 2**: ต้องมีบรรทัดคอนโซล `GM_WARP_SCENE_PERSIST_FAILED` คู่กับ
`GM_WARP_SCENE_PERSISTED` ที่มีอยู่แล้ว — ตรวจโค้ดจริงบน `main` ก่อนเริ่ม: **ไม่มี** สตริงนี้ในรีโป
(grep `GM_WARP_SCENE_PERSIST_FAILED` = ศูนย์ผล) ⇒ นี่คืองานของรอบนี้

## งานที่ทำ

`src/pirateforce_foundation/gm/warp_scene_persist.py`:
- เพิ่ม `FAIL_CONSOLE_TOKEN = "GM_WARP_SCENE_PERSIST_FAILED"`
- เพิ่มเฮลเปอร์ `_fail(target, reason)` — พิมพ์ `GM_WARP_SCENE_PERSIST_FAILED scene=<n> reason=<เหตุ>`
  ทาง stderr แล้วคืน `reason` กลับเหมือนเดิม (ไม่เปลี่ยนค่าที่ caller ได้รับ)
- เรียก `_fail()` ที่ทุก `return` ของ `persist_warp_scene` หลังจุดตรวจ
  `isinstance(target, WarpTarget)` — **8 จุด**: `OUTCOME_NO_SESSION_DOOR` ·
  `OUTCOME_NO_CHARACTER` · `OUTCOME_LOGIN_WOULD_REFUSE` · `OUTCOME_COMPOSE_REFUSED_*` ·
  `OUTCOME_WRITE_REFUSED_*` · `OUTCOME_SELECTED_NOT_RESTORED` · `OUTCOME_READBACK_UNAVAILABLE` ·
  `OUTCOME_ROW_NOT_TOUCHED` — ไม่แตะ `OUTCOME_PERSISTED` (มี token ของตัวเองอยู่แล้ว) และ
  ไม่แตะ `OUTCOME_NOT_A_TARGET` (ยังไม่มี `target.scene_id` ให้อ้าง เพราะไม่ใช่การวาปจริง)
- `reason` ที่พิมพ์ = คำเดียวกับค่าที่ฟังก์ชันคืนกลับอยู่แล้ว (`OUTCOME_*`) แหล่งเดียว
  ไม่ใช่คำศัพท์ชุดที่สองที่ต้องคอยให้ตรงกัน

`tests/test_gm_warp_scene_persist.py`: เพิ่ม 6 เทส —
1. `OUTCOME_LOGIN_WOULD_REFUSE` พิมพ์ `GM_WARP_SCENE_PERSIST_FAILED scene=126 reason=login_would_refuse`
2. `OUTCOME_ROW_NOT_TOUCHED` (same-scene no-op write) พิมพ์ token ที่ถูก และไม่ปน `GM_WARP_SCENE_PERSISTED `
3. write door ที่ raise `PermissionError` — token พิมพ์ชื่อชนิด error เท่านั้น ไม่มีข้อความ
4. stderr ที่ปิดแล้วบนเส้นทางล้มเหลว (`login_would_refuse`) — outcome ไม่เปลี่ยน ไม่ raise
5. `OUTCOME_NO_SESSION_DOOR` พิมพ์ token
6. `OUTCOME_NOT_A_TARGET` — stream ว่างเปล่าทั้งหมด (ไม่พิมพ์อะไรเลย)

`docs/GM_LANE.md`: เพิ่มหัวข้อ "รอบ ydlvtt" ต่อจาก "รอบ q3cde9" — เนื้อหาเดียวกับสรุปนี้

## pf-adversary (`COO-DECISION 20260903_2345` / `20260904_1428`)

**ไม่ได้เรียกรอบนี้.** เหตุผล: งานคือเพิ่มจุดพิมพ์คอนโซล 8 จุดในฟังก์ชันเดิมที่ผ่าน pf-adversary
ไปแล้วในรอบ `q3cde9` (ประตูเขียน/การอ่านกลับ/โครงสร้างควบคุมไม่เปลี่ยนเลยสักบรรทัด มีแต่ `_fail()`
คั่นก่อน `return`) 🔴 **เซสชันนี้ไม่มี Agent/Task tool จริงสำหรับเรียก pf-adversary** — บันทึกตรง ๆ
ตามที่ `AGENTS.md` §7 บรรทัด 105 กำหนด (ข้อยกเว้นรีวิวมือใช้ได้เฉพาะเซสชันที่ไม่มีเครื่องมือจริงเท่านั้น)
ทำรีวิวมือแทนแบบเจาะจง: ไล่ทุก `return` เทียบกับตารางเหตุผลในโมดูล docstring เดิม ยืนยันว่า
non-`OUTCOME_PERSISTED` non-`OUTCOME_NOT_A_TARGET` ทุกเส้นทางมี `_fail()` นำหน้าครบ (8/8)
และเทสใหม่ 6 ตัวข้างบนแดงถ้าลบ `_fail()` ออกจากจุดใดจุดหนึ่ง (วัดด้วยมือ ไม่ใช้เครื่องมือ)
**ไม่อ้างว่าผ่าน pf-adversary จริง**

## เทส

ระหว่างทาง (เฉพาะไฟล์ที่แตะ):
- `tests/test_gm_warp_scene_persist.py` — 38 passed (ก่อนเพิ่มเทสใหม่ครบ), 44 passed หลังเพิ่ม
- `tests/test_gm_chat_warp_way_out.py` + `tests/test_gm_warp_position_confirmed.py` (import
  โมดูลเดียวกัน) — รวม 168 passed, 9 subtests passed

ชุดเต็ม (ครั้งเดียวในรอบนี้ ตามกติกา `1428`/`0053`/`0149` — บนต้นไม้ที่ merge `origin/main` แล้ว):

**9943 passed, 327 skipped, 19288 subtests passed, exit 0** (495.33s) — เขียว(cloud sanity, local pytest)
รันบน commit `b982868` (docs) บนต้นไม้ที่ merge `origin/main` (`c9c65f2` = `#747`) แล้ว

- ไม่มีการรันชุดเต็มครั้งที่สอง: commit สุดท้าย (`docs/GM_LANE.md`) เป็นเอกสารล้วน ไม่แตะไฟล์ผลิต/เทส
  จึงไม่เปลี่ยนผลของชุดที่รันไปแล้ว

## ค้นแล้ว: เจอ/ไม่เจอ

`external/00_SEARCH_HERE_FIRST.md` · `gamedata/00_SEARCH_HERE_FIRST.md` — **ค้นแล้ว: ไม่เจอ**
(รอบนี้ไม่พึ่งข้อมูล client ใหม่ เป็นการเพิ่มบรรทัด log บนโมดูลที่มีอยู่แล้ว) ·
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` — **ค้นแล้ว: เจอ** (ที่ root ของ `pf_bridge`)

## กล่องจดหมาย (ADDENDUM v2 ข้อ B — ใครเปิดใบ คนนั้นบริโภคผล)

- `notes_to_chief/*` หาใบ `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt` คู่กัน — **ค้นแล้ว: เจอหนึ่งใบ**
  `20260904_1646_COO-DECISION-lane-gm-...md` (ตอบใบ `1620` ที่สาย GM เปิดในรอบ `q3cde9`)
  ⇒ บริโภครอบนี้ (คืองานหลักของรอบทั้งหมด) วาง `.CONSUMED.txt` แล้ว สำเนาต้นฉบับไป `consumed/` แล้ว
- ผลอื่น (`0554`/`1035` เก่า) ที่ grep ติด "ADDRESSEE: LANE-GM" เป็นการอ้างถ้อยคำการค้นในเนื้อใบ
  ไม่ใช่หัวจดหมายจริง — ไม่ใช่ใบที่ต้องบริโภคซ้ำ (`ADDRESSEE:` จริงของทั้งสองใบคือ `CHIEF`)
- `notes_to_chief/*CLAIM*` อายุ < 90 นาที — **ค้นแล้ว: ไม่เจอ**
- CORE-REQUEST/คำตอบ chief ที่อ้างเลข GM-0xx ยังไม่บริโภค — **ค้นแล้ว: ไม่เจอใหม่** (GM-053/GM-054
  บริโภคไปแล้วในรอบก่อนหน้า)

## P-3 (สารบัญปุ่ม GMUI — งานถัดไปตาม `COO 1646` ข้อ "ใครทำอะไร")

ตรวจซ้ำ `gm/gmui_catalog.py`: `BUTTONS` ยังว่างโดยตั้งใจ, `total_is_unknown()` = True
ติดที่เดิม — **ไม่มี client image ในคลาวด์** ไม่มี RE runner ตอบใบ `1328`
(`LANE-GM-RE-TICKET-gmui-three-pages-button-to-opcode-map.md`) กลับมา ไม่มีอะไรใหม่ให้ทำต่อ
ในหัวข้อนี้รอบนี้

## backlog / งานสำรอง (`COO-DECISION 20260904_1450`)

รอบนี้ไม่ว่าง (มีงานหลักครบตามที่ `1646` สั่ง) จึงยังไม่ต้องใช้กฎ F แต่บันทึกคิวถัดไปไว้ให้รอบหน้า:

1. **P-3 สารบัญปุ่ม GMUI** — ติดที่ RE runner ที่มี client image (ไม่มีในคลาวด์)
2. **P-2 สีชื่อมอน** — ติดที่ RE ใบที่สอง (`0306` GM ร่างส่งแล้ว) รอ chief ตั้งเลข
   (`COO 1650`: chief ต้องตั้งเลขเป็นงานแรกรอบถัดไปของ chief เอง ไม่ใช่ของ GM)
3. **D8 ของรอบ `q3cde9`** (ยังเปิด ไม่ใช่ regression ของรอบนี้): (ก) วาปครั้งแรกของล็อกอินใน
   dispatch เดียวกัน — บล็อก census รันทีหลังในเฟรมเดียวกัน (ข) หน้าต่างระหว่างเขียนแถวกับ
   ที่ซ็อกเก็ตส่งไบต์จริง (~2,200 บรรทัดถัดไปใน `runtime.py`)
4. **RE-238 body** (`0x430E10`) — ติดที่ RE runner เดียวกับข้อ 1

**ว่างเพราะรอใคร**: ไม่ว่าง (มีงานหลักของรอบนี้) — ข้อ 1/4 ข้างบนรอ **RE runner ที่มี client image**
ข้อ 2 รอ **chief** ตั้งเลขใบ

## จบรอบ

- `pirate-force-server` — PR PR_NUMBER_PLACEHOLDER (`[LANE-GM] ...`) เปิดแล้ว ไม่ draft
  marker `PF-AUTOMERGE: v4` ใส่ตั้งแต่เปิด ยืนยันด้วย GET แล้ว
- `pf_bridge` claim PR `#1177` — เติม `PF-AUTOMERGE: v4` ตอนจบไฟล์นี้ (หลัง push ครบทั้งสองรีโปแล้ว)
  = ปลดล็อก
- **push แล้ว รอ merge PR PR_NUMBER_PLACEHOLDER** — ไม่รอ gate ไม่รอ merge ตามกติกาจบรอบใหม่
  (ห้ามรอ ล็อกจะไม่ปลดถ้ารอ — เกิดจริงกับ `#862`)

## nonclaim

1. **GM ข้ามขั้นไหน**: ไม่มี — รอบนี้เป็นการเพิ่มบรรทัดคอนโซล (observability) ล้วน ไม่ใช้ GM
   ข้ามการทดสอบใด ๆ
2. **ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้**: `/warp` ที่เขียนแถวไม่สำเร็จตอนนี้พิมพ์
   `GM_WARP_SCENE_PERSIST_FAILED scene=<n> reason=<เหตุ>` ทาง stderr — เมื่อวานมีแต่
   `session.events` ที่ผู้เทสนั่งจอไม่เห็น
3. ไม่อ้างว่า `GT-172` F-3 ปิดแล้ว (เป็นงานของ chief ตามใบ attended `1452` ข้อ 5 — ยังไม่มีใบนั้น) ·
   ไม่อ้างว่าผ่าน pf-adversary จริง (รีวิวมือแทน บันทึกไว้ตรง ๆ ข้างบน) ·
   ไม่อ้างว่า M2/M3/M4/P-2/P-3 ขยับ · ไม่มีบัญชีใดได้หรือเสียสถานะ GM ·
   ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py` · ไม่แตะ canonical DB ·
   ไม่แตะเขตสาย A/B (`scenarios/world_*.json`, `scenarios/combat_*.json`)
