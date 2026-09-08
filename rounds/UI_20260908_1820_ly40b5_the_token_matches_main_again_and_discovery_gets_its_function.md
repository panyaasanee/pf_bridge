# UI รอบ `ly40b5` — โทเคนกลับมาตรงกับ main และ discovery ได้ฟังก์ชันที่มันรออยู่

เริ่ม 2026-09-08T18:20+07:00 · claim `pf_bridge#1938` · ไม่ใช่ takeover
ล็อกว่างจริง: PR เปิดใน pf_bridge ที่ชื่อ `[LANE-UI] round ...: claim` = **0 ใบ** ก่อนเปิดใบตัวเอง
(`[LANE-UI]` ที่เปิดอยู่สองใบ `#1676`/`#1659` เป็น **addendum ไม่ใช่ claim** · claim ของสายอื่นที่มีชีวิต
`#1931` DB `#1932` GM `#1933` A `#1934` Q `#1936` B `#1937` CS)
กิ่งทั้งสองรีโปตัดจาก `origin/main` สด ไม่พึ่ง PR ที่ยังไม่ merge ใบใด (`pirate-force-server` base = `48eaf82`)

🔴 **สะพานค้าง ไม่ใช่นาฬิกาผิด** (COO `1245`): บรรทัดล่าสุดของ `_BRIDGE_HEARTBEAT.txt` = `2026-09-08T16:08:01+07:00`
ห่างจากเวลาเริ่มรอบ **132 นาที** (เกิน 60) ⇒ ตรวจนาฬิกาตัวเองกับหลักฐานอิสระตามกฎ: `created_at` ของ
`pf_bridge#1937` (claim ของ LANE-CS) = `2026-09-08T11:09:31Z` = **18:09 +07** ห่างจากเวลาที่นาฬิกาสายนี้อ่านได้
ตอนเริ่มรอบ 11 นาที ⇒ นาฬิกาถูก สะพานเป็นฝ่ายค้าง · **push ต่อตามกฎ ไม่หยุดรอบ**

## รอบนี้ขยับ NOW/M ข้อไหน

- **NOW บรรทัด LANE-UI ข้อแรก** = "`HEADLESS_PROOF` `GT-308` วัดบน main หลัง `#1158` merge" (คำสั่งเจ้าของ `1520`
  ผ่าน COO `1642`) — **จ่ายแล้วรอบนี้** และเจอของที่ใบสั่งให้หา: `#1158` ลง main จริง (`61f01d1`) และมันทำให้
  **บรรทัดโทเคนเปลี่ยนรูป** (มีฟิลด์ `head=`/`code=` เพิ่ม ตรงตามที่จดหมาย `0031` เตือนไว้ว่า "เตรียมไว้")
  ⇒ ถ้าไม่วัดรอบนี้ ka1-A จะรันซ้ำก่อนบูตแล้วไม่ตรงกับบรรทัดในใบ และ **ตัดใบทิ้งตามกฎ `0159`**
  ทั้งที่กลไกไม่ได้เสียอะไรเลย · จดหมาย `1820_*-gt308-headless-proof-remeasured-on-main-48eaf82-*` ถึง K
- **CORE-REQUEST `1553`** (NOW: "จุดเสียบ = CORE-REQUEST ใบเดียวต่อจุด") — chief อนุมัติทั้งใบ (`1703`) และผูก
  `_discover()` เป็นคิวข้อ 1 ของรอบ chief ถัดไป **โดยรอฟังก์ชันของสายนี้อยู่** ⇒ รอบนี้ลง
  `ui_dispatch.adopt_answerer()` + 11 เทส = ครึ่งที่ chief รอ ไม่ใช่กระดาษ
- **M ที่ขยับ: ไม่มี** — M2 เป็นของ LANE-A · แต่ไม่ใช่รอบเปล่าตามเกณฑ์ PANYA `1846`: มีบรรทัด `src/` ใหม่
  ที่เป็นเงื่อนไขปลดของอีกสาย (chief) และมีโทเคนที่ปลดใบ attended ของเจ้าของจริง
- จดหมายที่เขียนรอบนี้ 3 ใบ: ถึง K สองใบ (โทเคน `GT-308` · สถานะโทเคนสามปุ่ม) · ถึง chief หนึ่งใบ (ฟังก์ชันลงแล้ว)
- จดหมายที่บริโภครอบนี้ (วาง `.CONSUMED.txt` + สำเนาไป `consumed/`): `1642` COO-DECISION (GT-308 งานแรก) ·
  `1742` COO-DECISION (สายโซ่ลง main + เกณฑ์ draft ทั่วไป) · `1703` FROM_CHIEF R404 (อนุมัติ CORE-REQUEST)

## 1. งานแรก: โทเคน `GT-308` วัดใหม่บน main — และมันเปลี่ยนจริง

รันบนทรี `origin/main` เปล่า ๆ ก่อนคอมมิตใด ๆ ของรอบ (`git rev-parse HEAD` = `git rev-parse origin/main` = `48eaf82ad493...`):

```
UI_LOGOUT_EXIT_GAME_ARMED subcode=1 ack=1 lease_closed=1 close_scheduled_ms=250 closer_called=1 relogin_after=ok head=48eaf82ad493 code=4f12559dcdd4 RESULT=PASS
UI_LOGOUT_EXIT_GAME_ARMED_CONTROL subcode=3 ui_actions=0 lease_still_open=1 close_scheduled=0 head=48eaf82ad493 code=4f12559dcdd4 RESULT=PASS
UI_LOGOUT_EXIT_GAME_ARMED_SUMMARY cases=2 failed=0 head=48eaf82ad493 code=4f12559dcdd4 RESULT=PASS
```

ต่างจากบรรทัดที่ K พับไว้เมื่อรอบ `splep7` (วัดบน `e782549`) ตรงฟิลด์ `head=`/`code=` ที่เพิ่มเข้ามาพร้อม `#1158`
สายนี้ขอให้ K ใช้ **`code=` เป็นเกณฑ์เทียบก่อนบูต ไม่ใช่ `head=`** — `head` ขยับทุกครั้งที่สายอื่น merge อะไรก็ตาม
ส่วน `code` ขยับเมื่อกลไกเปลี่ยนเท่านั้น (เขียนไว้ในจดหมายถึง K แล้ว)

- โทเคนปุ่มที่หนึ่งของซีมแปด vital วัดบน main ได้ด้วยในรอบเดียวกัน:
  `UI_PARTY_INVITE_ANSWER_ARMED answered=1 label=UI_PARTY_INVITE_ANSWERED frame_bytes=58 frame_matches=1 echo_is_the_players_bytes=1 junk_refused=1 RESULT=PASS`
- 🔴 **ที่ยังไม่มีและไม่แสร้งว่ามี**: `grep -rn "UI_TRADE_INVITE_ANSWER_ARMED\|UI_PARTY_CMD_ANSWER_ARMED" src/` บน main
  = **0 hit** — มีตัวรัน headless ตัวเดียว (`ui_party_invite_answer_headless.py`) ⇒ ปุ่มที่สองและสามยังไม่มีโทเคน
  แม้โค้ดตอบจะอยู่บน main แล้ว ⇒ **ยังไม่ส่งเนื้อใบ GT สามปุ่มรอบนี้** และขอ K อย่าเพิ่งตั้งเลข (ใบที่มีโทเคน
  ปุ่มเดียวแล้วบูตไปเจอสองปุ่มเงียบ = รถบัสเสียเที่ยว ซึ่งเป็นเหตุผลที่กฎ `0159` มีอยู่)

## 2. งานที่สอง (โค้ด): `adopt_answerer()` — ครึ่งที่ chief รออยู่

`src/pirateforce_foundation/ui_dispatch.py` (+129) · `tests/test_ui_dispatch.py` (+274 · 11 เทสใหม่) · `docs/UI_LANE.md` (+39)

- `_install_answerer(module_name, gating, vital_id, fn)` = ท้ายของ `register_answerer()` ที่แยกออกมา (first-wins ·
  incumbent ที่ถูก gate ยอมสละช่อง · การเขียน dict คำสั่งเดียว · โทเคน `UI_DISPATCH_ANSWERER`) ⇒ สองทางเข้าสู่
  รีจิสทรีตอบคำถาม "ใครถือ id นี้" ด้วยโค้ดชุดเดียว ไม่ใช่สองชุดที่ค่อย ๆ เพี้ยนออกจากกัน
- `adopt_answerer(qualified_name, vital_id, module)` ลายเซ็นตรงกับที่ chief ผูกไว้เป๊ะ ⇒ สนิปเปตของ chief เสียบได้เลย
  และ `getattr` ตัวที่สองของเขาทำให้ลำดับ merge สลับกันได้โดยไม่มีหน้าต่างที่บูตพัง
- ปฏิเสธและ **พิมพ์เหตุผลบน stderr ทุกครั้ง** (`UI_DISPATCH_ADOPT_REFUSED id=... reason=... by=...`) ตามข้อ 4 ของ
  ใบ chief: `not_routed_here` · `not_a_discoverable_lane` · `name_is_not_that_module` · `no_reviewed_owner` ·
  `not_the_reviewed_owner` · `id_is_not_the_declared_one` · `no_declared_callable` — เพราะ `_discover()` ไม่อ่านค่าคืน
  ถ้าเงียบ "ผู้ปลอมที่ถูกปฏิเสธ" กับ "เลนที่ยังไม่ประกาศ" จะแยกกันไม่ออกจากคอนโซล
- สัญญาฝั่งเลน = **สองบรรทัด** `ANSWERS_VITAL_ID` + `ANSWERS_WITH` · `ANSWERS_WITH` ต้องประกาศตรง ๆ ไม่เดาจากชื่อ
  `answer_*` (ไม่งั้นการเปลี่ยนชื่อฟังก์ชันเปลี่ยนได้ว่าไบต์ของใครออกสาย)
- กลุ่ม gating มีชื่อเลนที่ประกาศเสมอ: บนเส้นทางนี้ไม่มีเฟรมของเลนอยู่บนสแตกเลย (คนเรียกคือ `_discover()`)
  ⇒ ถ้าพึ่ง `_gating_module_names()` อย่างเดียว กลุ่มอาจว่าง แล้ว `answer()` จะตัดสินจากชื่อผู้ลงทะเบียนอย่างเดียว
- **ยังไม่แปลงสามเลนให้ประกาศ**: แปลงก่อน `_discover()` เรียก = ถอดปุ่มที่ทำงานอยู่สามปุ่มออกจากผู้เล่น
  ⇒ ลำดับคือ chief เสียบ `_discover()` ก่อน แล้วสายนี้แปลงเลนในรอบถัดจากนั้น
- `docs/UI_LANE.md` เขียนสิ่งที่ chief ขอในข้อ 5 **วันที่มันยังจริง ไม่ใช่วันที่มันเลิกจริง**: จนกว่า `_discover()`
  จะเป็นคนเขียน `_ANSWERERS` ด่านเจ้าของปิดได้เฉพาะผู้ปลอมที่ยืมชื่อเจ้าของ ไม่ใช่ผู้ปลอมใต้ชื่อตัวเอง

## หลักฐาน

- `tests/test_ui_dispatch.py` เฉพาะไฟล์: **107 passed, 91 subtests** (มี 11 เทสใหม่ของ `adopt_answerer`)
- ชุดเต็ม `pytest tests/` รันบนทรีของคอมมิตสุดท้ายจริง (หลัง `git merge origin/main`) — ผลอยู่ในบอดี้ PR
- `python3 tools_bridge/pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS**
- 🔴 `ADVERSARY_PENDING pirate-force-server` กิ่ง `claude/festive-shannon-ly40b5` — สั่ง `pf-adversary` ต้นรอบพร้อมเริ่มงาน
  ผลยังไม่คืนตอน push ⇒ push ตามกฎ · **ยังไม่มีใครเขียนได้ว่า "ผ่าน adversary"** · ถ้าผลคืนของที่ต้องแก้
  = งานแรกของรอบถัดไป
- ไม่ได้แตะ: `runtime.py` · `app.py` · `store.py` · `gm/` · `lane_hooks/__init__.py` (เขตของ chief ตามใบ `1703`) · `v141`

## สถานะ PR เซิร์ฟเวอร์

`pirate-force-server` PR ของรอบนี้ **เปิดแล้ว ไม่ draft มี `PF-AUTOMERGE: v4` ตั้งแต่เปิด รอเกต** —
ยังไม่อยู่บน main จนกว่ารอบถัดไปจะยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`
ไม่เข้าเงื่อนไข draft ของ `1742`: ไม่แตะเส้นบูต/ล็อกอิน/ตัวตน actor และไม่ประกอบเฟรมใหม่ส่งไคลเอนต์
(`adopt_answerer` ยังไม่มีผู้เรียกในโปรดักชันจนกว่า `_discover()` จะเสียบ)

## รอบหน้าทำอะไร (ตามลำดับนี้)

1. **ผล `pf-adversary` ของรอบนี้** — อ่านก่อนอย่างอื่น จ่ายข้อวิกฤตในกิ่งใหม่ (ถ้าคืนแล้ว)
2. **ตัวรัน arming ให้ครบสามปุ่ม** (`0x37B1` มีแล้ว · `0x3700` · `0x2466` ยังไม่มี) โครงเดียวกัน ต่างที่ id/version/
   payload → แล้วส่งเนื้อใบ GT **ใบเดียวคลุมสามปุ่ม** พร้อมโทเคนครบสามบรรทัด (ค้างมาห้ารอบเพราะโค้ดไม่อยู่บน main
   ซึ่งตอนนี้ไม่ใช่เหตุผลอีกแล้ว)
3. **D13** — สามปุ่มไม่มีแถวใน `docs/FUNCTIONAL_COVERAGE.json` · **บันทึกไว้ว่าราคาของมันคืออะไร ครั้งเดียว**:
   ไฟล์นั้นถูกพินด้วย digest ใน `tests/test_foundation_legacy_seam.py` ⇒ เพิ่มแถว = ต้องคำนวณ digest ใหม่ +
   เขียนบล็อกร้อยแก้วอธิบายการขยับตามธรรมเนียมของไฟล์นั้น (ไม่ใช่แค่เติม JSON) รอบนี้จึงไม่หยิบ เพราะจะกินเวลา
   ที่เป็นของโทเคน `GT-308` ซึ่งเจ้าของรอบูตอยู่
4. **เนื้อใบ `GT-186`/`GT-184`** ที่ K พลิกป้ายมาให้ (`NEEDS-NEW-BODY: LANE-UI` · ใบ K `1723` ยังไม่บริโภค)
5. **แปลงสามเลนเป็น `ANSWERS_VITAL_ID` + `ANSWERS_WITH`** — เมื่อ `_discover()` ของ chief อยู่บน main แล้วเท่านั้น
   (ยืนยันด้วย `git merge-base --is-ancestor` ก่อน ห้ามเชื่อจดหมาย)

SCOREBOARD: COMING | ปุ่ม "ออกจากเกม" บน main วันนี้พร้อมให้ผู้เทสกดบนจอจริงแล้ว - โทเคนของใบ GT-308 กลับมาตรงกับโค้ดที่อยู่บน main (ก่อนหน้านี้ใบถือบรรทัดเก่าและจะถูกตัดตอนบูต) และ discovery ได้ฟังก์ชันที่มันต้องใช้เพื่อเลิกให้เลนลงทะเบียนปุ่มของตัวเอง | pirate-force-server PR ของรอบ ly40b5 (adopt_answerer + 11 tests, preflight PASS, ADVERSARY_PENDING) - โทเคน head=48eaf82ad493 code=4f12559dcdd4 RESULT=PASS วัดบน main 48eaf82 - pf_bridge#1938
