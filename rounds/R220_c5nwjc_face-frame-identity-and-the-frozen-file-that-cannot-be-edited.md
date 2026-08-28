# R220 · สาย E (PLATFORM) · เซสชัน `c5nwjc` · 2026-08-29T03:0x+07:00

## ชะตา PR ของรอบก่อน (บังคับ ตาม COO-DECISION 20260829_0247 ข้อ 3)

| รีโป | PR | ผล |
|---|---|---|
| pf_bridge | #349 (R219) | **merged** 2026-08-28T19:18:47Z |
| pf_bridge | #351 (R219 2/2) | **merged** 2026-08-28T19:22:08Z |
| pirate-force-server | #222 (R219) | **merged** — ยืนยันซ้ำจาก merge commit `85820ba` บน main |

⇒ งานรอบก่อน **อยู่บน main ครบทั้งสองฝั่ง** ไม่มีอะไรต้อง cherry-pick กลับ

## หนึ่งประโยคของรอบนี้

ต่อสาย CORE-REQUEST ของสาย A (เฟรมหน้าตอนคลิก NPC ส่งตัวตนผิดคน) **สำเร็จที่ชั้น wire แต่ไม่ได้แก้ตรงที่สาย A ขอ**
เพราะวัดแล้วว่าไฟล์ที่มีบั๊กแก้ไม่ได้จริง ๆ — ถูกพินแช่แข็งไว้ 7 จุดอิสระ

## ① CORE-REQUEST ของสาย A — ทำอะไรไป

**อาการที่เจ้าของเห็น** (`OBSERVER_CONFIRMED: 2026-08-29T00:17+07:00`, บูตไร้แฟล็ก): คลิก Columbus
→ หน้าต่างขึ้นชื่อ **Sebastian** เสียงพากย์ Sebastian บท "Prison Exile Island" ของ Sebastian
แต่แผงเป้าข้าง ๆ อ่านว่า **Columbus** ⇒ สองเฟรมในบูตเดียวกัน พูดคนละคนเรื่อง actor ตัวเดียวกัน

**ต้นเหตุ** (สาย A หาเจอ ผมยืนยันซ้ำจากซอร์ส): `make_v98_conversation_face_state` ส่ง **เลข Mob-Set**
(ฟิลด์ที่ 2 ของแถวแช่แข็ง) ลงพารามิเตอร์ที่ 1 ของ `make_npc_attr` ซึ่ง docstring ของมันเองระบุว่าคือ
"the MOBS/template u16 at +0x78" · เลข Mob-Set ไม่ใช่ MOBS n_ID · placement 1 ชนกันที่เลข `2` พอดี
⇒ บั๊กไม่โผล่เป็นเลขผิด แต่โผล่เป็น **คนผิด**

**สิ่งที่ทำ:** โมดูลใหม่ `src/pirateforce_foundation/world_face_frame.py` + wiring หนึ่งจุดใน `runtime.py`
(ทันทีหลัง `actions = super().dispatch(parsed)`) ประกอบเฟรมใหม่ผ่าน `world_port_royal_identity.resolve()`
— call เดียวกับที่ `world_population._entry` ใช้ ⇒ เฟรมสำมะโนกับเฟรมคลิกอ่านตารางเดียวกันแล้ว

- ใช้ serializer ของ v141 ทั้งหมดแบบอ่านอย่างเดียว **ไม่คัดลอกรูปร่างเฟรมสักไบต์**
- ตัวที่ resolve ไม่ได้ → **ตัดออก** (เหมือน `census_order` ตัด 7 ใน 115 รวม P0)
- ตัวที่ **ถูกคลิก** resolve ไม่ได้ → **ไม่ส่งเฟรมเลย** + event token · ห้าม fallback เป็นเลข Mob-Set เด็ดขาด
- ฟังก์ชัน total + additive: dispatch ที่ไม่มีเฟรมหน้า ได้ของเดิมกลับครบ ลำดับเดิม (มีเทสพิน 5 ข้อ)

## ② ทำไมไม่แก้ตรงที่ขอ — และนี่คือของที่ต้องจำ

สาย A ขอแก้ 3 บรรทัดใน `current/pf_login_game_server_v141.py` และเขียนว่า
"[สมมติของสาย A - รอ COO ยืนยัน] ว่าไฟล์นี้เป็นของ chief"

**ผมลองแก้จริงก่อน แล้วรันสวีตเต็มวัดผล** ได้ของแดง 12 ใบ ในนั้น **7 จุดพังเพราะไฟล์ขยับโดยตรง** [วัดแล้ว]:

1. `tools/verify_hypothesis_ledger.py` — ค่าคงที่ `IMMUTABLE_V141_SHA256`
2. `docs/HYPOTHESIS_LEDGER.json` — `entries[2].source_refs[0].sha256`
3. `tests/test_foundation.py::test_v141_characterization_hash`
4. `tests/test_item_move_capture.py::test_v141_is_still_the_exact_immutable_source`
5. `tests/test_second_password_bypass.py::test_v141_is_immutable`
6. `tests/test_server_shutdown.py::..._and_v141_is_preserved`
7. `tests/test_runtime_console.py::test_self_test_only_is_the_console_exception` — ห้ามโมดูลนี้ `print()` นอก self-test
   (ล้มแม้แต่ token บอกเหตุผลที่ผมพยายามใส่)

⇒ **"v141 immutable" ไม่ใช่ธรรมเนียม แต่เป็นการบังคับ** และเข้าข้อ "เปลี่ยนของที่พิสูจน์แล้ว" (prompt หัวข้อ 14 ข้อ 3)
ซึ่งกันไว้ให้เจ้าของ ⇒ **ผมถอย คืนไฟล์กลับเป๊ะ** (แฮช `2EB05ED2...4C22` ตรงค่าพินทุกตัวอักษร) แล้วส่ง ASK ให้ COO

🔴 **ผลข้างเคียงที่ต้องพูดตรง ๆ:** builder ที่มีบั๊ก **ยังมีบั๊กอยู่บน main โดยเจตนา** ผมแก้ปลายทาง
เทสคลาส `FrozenBuilderStillCarriesTheDefectTests` พินไว้ว่ามันยังส่ง Sebastian อยู่ —
ถ้าวันไหนคลาสนั้นแดง แปลว่ามีคนขยับไฟล์แช่แข็ง ให้หยุดอ่านก่อนทำอย่างอื่น

## ③ ด่าน CI-skip ของ COO — ลง `EVIDENCE_GATES.md` แล้ว (ทันกำหนด)

หัวข้อ 7 ใหม่: คำสั่ง grep · เจอ = ห้าม push · วิธีหักคำ · วิธีสังเกตว่าโดนแล้ว
("ไม่มี run เลยหลัง 2-3 นาที = โดน **ห้ามแปลว่ากำลังจะมา**") · nonclaim ว่า 4 ใน 5 โทเคนเป็น [เสนอ]
รอบนี้รันด่านนี้กับทุก commit ของตัวเองก่อน push

⚠️ ข้อสังเกตงานแม่บ้าน: `EVIDENCE_GATES.md` เขียนเพดานตัวเองไว้ 15 KB แต่ตอนนี้ **24.3 KB**
(เกินมาก่อนรอบนี้แล้ว: 20.8 KB) ผมไม่ตัดเองในรอบเดียวกับที่เพิ่มกฎ — บทเรียน R215 (ตัดครั้งแรกกินกฎหาย 12 ข้อ)
เสนอเป็นใบแยกรอบหน้า

## ④ ที่ COO ขอแล้วผมยัง **ตอบไม่ได้** — รายงานตามจริง

COO ขอหลักฐานว่า job `decide` เดินเส้น skip จริงเมื่อ head ขยับ (นับ `::warning::`)
**ยังไม่มีเหตุการณ์ให้วัด** — ตั้งแต่ #222 merged (02:25+07:00) ไม่มี PR ใบไหนที่ head ขยับระหว่าง merge
ทุก run ของ `merge-claude-pr` หลังจากนั้น conclusion = success ทั้งหมด
⇒ นี่คือ "ยังไม่มีเคส" **ไม่ใช่ "ยืนยันแล้ว"** · GT-140 (kill switch บน main) ยังรอสะพานเหมือนเดิม

## ⑤ พินที่ต้องขยับเพราะโมดูลใหม่ (ทำครบในคอมมิตเดียวกันตามที่เทสสั่ง)

โมดูลใหม่สร้าง actor entry ⇒ สำมะโนตัวเลข 3 ตัวขยับ และถูกพินไว้ **3 ที่** ซึ่งเทสไล่ให้ครบ:
`reports/PF_RUNTIMERES_ACTOR_ENTRY001_STATIC_20260819.md` · `tests/test_runtimeres_actor_entry_static.py` ·
`tools/pf_runtimeres_actor_entry_static.py`
- `src_actor_entry_call_sites` 16 → **17**
- `src_actor_stream_call_sites` 24 → **25**
- `src_modules_building_actor_entries` 15 → **16** (+ รายชื่อเรียงแล้ว: เพิ่ม `world_face_frame.py`)

หมายเหตุ: กลไก "พินรายชื่อเรียงแล้วข้างตัวเลข" ที่ prompt หัวข้อ 18 ข้อ 5 สั่งไว้ **มีอยู่แล้วและทำงานจริง** —
มันจับได้ทันทีว่าโมดูลไหนเข้ามาใหม่ ไม่ใช่แค่ว่า "เลขขยับ" ⇒ ถือว่าข้อ 5 ปิดได้

## ⑥ หลักฐานของรอบนี้

- สวีตเต็ม: **เขียว(cloud sanity)** — ดูตัวเลขในจดหมายผลของรอบ
- `python3 tools/verify_hypothesis_ledger.py` → `HYPOTHESIS_LEDGER PASS entries=47` **ไม่มี drift**
  (ขั้นบังคับข้อ 7 ก่อน commit ตาม prompt หัวข้อ 7)
- `tools/pf_runtimeres_actor_entry_static.py` **รันบนคลาวด์ไม่ได้** ต้องมี `GameClient/GameClient.local.bin`
  ⇒ ตัวแทนบนคลาวด์คือ `tests/test_static_verifier_pins_cloud.py` ซึ่งเขียวแล้ว · ตัวเต็มเป็น STATIC-ON-BRIDGE
- `pf-adversary` รันบนงานชิ้นนี้

## ⑥.5 WIRED (บังคับตาม prompt หัวข้อ 17 ข้อ 3)

`WIRED = ไม่เปลี่ยนจากรอบก่อน` — รอบนี้ **ไม่ได้เพิ่มโมดูลใน `lane_hooks/`** จึงไม่มีการนับใหม่ตามนิยาม WIRED v2

แต่โมดูลใหม่ `world_face_frame` **ผ่านเกณฑ์ WIRED v2 เต็ม** (emission จริงบน production path ไม่ใช่แค่ import):
- `tests/test_face_frame_identity_wiring.py` (6 ข้อ) ขับ `runtime.make_state_class` ตัวจริง ผ่าน
  login → create → start-game → TargetPos (ติดสำมะโน) → **ChooseNPC จริง** แล้วอ่าน **ไบต์ของ action ที่ dispatcher คืนกลับ**
- **mutation kill [วัดแล้ว]:** patch `rebuild_face_actions` ให้เป็น identity function (= runtime ไม่แก้เฟรมเลย)
  ⇒ **แดง 3 ข้อ** รวมข้อที่อ่านไบต์ (`test_the_face_frame_a_click_returns_names_columbus`)
  ⇒ ยืนยันว่าโค้ดนี้ **ถูกเรียกจริงบนเส้นทางผู้เล่น** ไม่ใช่โค้ดประดับ
- ตรวจ encoding: ไฟล์ที่ผมเพิ่ม/แก้ทั้งหมดเป็น **ASCII ล้วน** (ผ่าน cp874) ยกเว้นอักขระที่มีอยู่ก่อนแล้วในไฟล์รายงาน

## ⑥.6 งานค้างของกล่องจดหมาย ที่รอบนี้ **ไม่ได้ทำ** และไม่แกล้งทำ

`notes_to_chief/` มีใบ `*CORE-REQUEST*` **9 ใบ (26-27 ส.ค.) ที่ยังไม่มี `.CONSUMED.txt`**
ทั้งที่เนื้องานของหลายใบลง main ไปแล้ว (GM-029/030, CORE-REQUEST-014 ฯลฯ)
🔴 ผมจงใจ **ไม่ stub ย้อนหลังแบบเหมาเข่ง** เพราะกฎคือ "อ่านเมื่อไหร่ stub เมื่อนั้น" —
stub ที่เขียนโดยไม่ได้อ่านคือการโกหกว่ากล่องถูกอ่านแล้ว ซึ่งแพงกว่ากล่องที่ดูค้าง
เสนอ COO: ให้เป็นงานหนึ่งรอบเต็มของสาย E (อ่านทีละใบ → ยืนยันว่าเนื้อลง main จริง → stub) ไม่ใช่งานแถมท้ายรอบ

## ⑦ ที่ยังไม่ได้พิสูจน์ (nonclaims)

1. **ทั้งรอบเป็นชั้น wire/DB** ไม่มี `OBSERVER_CONFIRMED` · ที่ว่าเจ้าของจะเห็นชื่อ/ได้ยินเสียง Columbus **ยังไม่มีใครเห็น**
2. ป้ายชื่อ NPC หายหลังขยับ — เฟรมใหม่ส่ง `basic_name` แล้วจริง [วัดแล้ว ชั้น wire] แต่ไคลเอนต์จะวาดใหม่ไหม **[เสนอ] ยังไม่วัด**
3. บทของ **เควสต์ 3021** ซึ่งเป็นคำถามหัวใบ GT-102 **รอบนี้ไม่ได้แตะ** ⇒ ชื่อถูกแล้วก็ยังไม่ปิดใบ
4. เขียวที่อ้างทั้งหมดเป็น **เขียว(cloud sanity)** · gate เต็มบนสะพานกับ Actions เป็นคนตัดสิน
   ที่นี่ไม่มี cp874 ไม่มีพฤติกรรม 3.14
5. เส้นทางที่ไม่ผ่าน `runtime.dispatch` (ถ้ามี) จะยังเห็น Sebastian — **ยังไม่ได้พิสูจน์ว่าไม่มีเส้นทางแบบนั้น**

## ⑧ ต่อไปทำอะไร

1. รอ COO ตัดสินว่า `current/pf_login_game_server_v141.py` แก้ได้ไหมและด้วยขั้นตอนใด (ใบ `20260829_0303_CHIEF-ASK-COO-*`)
2. เรียกผู้เทสกับ GT-102 **หลัง PR รอบนี้ merge แล้วเท่านั้น**
3. ใบแยกรอบหน้า: ตัด `EVIDENCE_GATES.md` ให้เข้าเพดาน 15 KB
