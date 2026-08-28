# CORE-REQUEST-GM-029 2026-08-28T18:24+07:00 — ขอจุดเรียก **หนึ่งจุดที่คืนค่า action** ที่สาขา `0xAC52` (แชท) แทน `fire()` ของ GM-028

ถึง: **chief (ADDRESSEE: chief)** · cc COO, เจ้าของ, กะ1-A, สาย A, สาย B, RE runner
จาก: LANE-GM รอบ `gr2q9j` · **ใบนี้แทนที่ `CORE-REQUEST-GM-028` ทั้งใบ** (หนึ่งใบ = หนึ่งจุด = หนึ่งสาย)

**ค้นแล้ว: ไม่เจอ** — `grep -inE "0xAC52|LocalTalk|ForcePos|vital_version" external/00_SEARCH_HERE_FIRST.md` = 0 แถว ·
`grep -inE "chat|talk|GM" gamedata/00_SEARCH_HERE_FIRST.md` = 0 แถว (กฎ "ค้นก่อนถอด")
ของที่ใบนี้พึ่ง มาจากซอร์สบน main + capture ที่ commit แล้ว (GT-006/GT-009) ไม่ได้ถอดใหม่

---

## 🔴 ก่อนอื่น: GM-028 ที่ส่งไปเมื่อ 17:12 **ผิดรูป** และสายนี้เป็นคนพบเอง

GM-028 ขอ `lane_hooks.fire()` ที่สาขา `0xAC52` **ซึ่งจะไม่มีวันทำให้อะไรขยับบนจอได้เลย** —
ไม่ใช่เพราะเขียนโค้ดผิด แต่เพราะสัญญาของ `fire()` เอง (docstring ของมันเอง):

> *"Never returns a value; hooks that need to hand something back to runtime.py are not what this point shape is for"*

และไบต์ออกสู่ client มี**ทางเดียว**ในเซิร์ฟเวอร์นี้: list ของ `(label, pc, frame, delay)` ที่
`dispatch()` **คืนค่า** แล้ว serve loop ของ legacy ดูดไปส่ง · ตรวจแล้วรอบนี้: `connection.py`
เป็น socket plumbing ล้วน ไม่มีคิว action · และ `gm/dispatch.py` docstring ของสายนี้เองเขียนไว้ตั้งแต่แรกว่า
*"this lane has no send path outside a CORE-REQUEST wiring point"*

⇒ ถ้า chief วาง GM-028 ตามที่ขอ ผลคือ `GT-127` ผ่านได้ (อ่านบรรทัดได้จริง ตัดสินที่ ndjson) **แต่เจ้าของจะ
พิมพ์ `/warp` แล้วไม่เห็นอะไรบนจอ** และนั่นคือสิ่งที่เจ้าของถามหาตั้งแต่ใบ 1105
**ขออภัยที่ต้องให้ chief อ่านสองใบ — แต่วางใบผิดแล้วค่อยรู้ตอนเจ้าของบูต แพงกว่ามาก**

---

## สิ่งที่ขอ: จุดเดียว รูปเดียวกับที่ `runtime.py` ทำอยู่แล้ว

ที่สาขา nested vital `0xAC52` (`Channel_LocalTalkMessageVital`) — **จุดเดียวกับที่ GM-028 ระบุ** —
ขอรูปนี้แทน ซึ่งเป็นรูปเดียวกับ `gm_state_action` (CORE-REQUEST-006) ที่ประกอบที่ `runtime.py:5122`
แล้ว `append` ที่ `5331` อยู่แล้ววันนี้:

```python
from .gm.chat_command_action import make_gm_chat_command_action   # ข้างๆ import gm อื่นที่มีอยู่แล้ว (บรรทัด 28-32)

# ...ที่สาขา 0xAC52:
self.rx_frames += 1
gm_chat_action = make_gm_chat_command_action(
    self, bytes(parsed.nested_payload), legacy,
)
if gm_chat_action is not None:
    actions.append(gm_chat_action)
```

- **โมดูล:** `src/pirateforce_foundation/gm/chat_command_action.py` (ใหม่รอบนี้ · 24 เทส + 5 subtests เขียว)
- **ฟังก์ชันที่ต้องเรียก:** `make_gm_chat_command_action(session, payload, legacy)` — คืน tuple 4 ช่อง
  หรือ `None` · `None` แปลว่า "เฟรมนี้ไม่ใช่ของเรา ทำตัวเหมือนก่อนสายนี้มีอยู่ทุกประการ"
- **ตรงไหนของ runtime:** สาขา dispatch vital id `0xAC52` — **ไม่ใช่** login, ไม่ใช่ START_GAME_REQ
- **เทสที่พิสูจน์:** `tests/test_gm_chat_command_action.py` (ใหม่) + `tests/test_gm_chat_command.py` (เดิม)
  · `pytest -k "gm or lane_hook"` = 365 passed, 4 skipped, 32 subtests (รอบนี้ บน cloud clone)

### 🔴 wire ได้จุดเดียวเท่านั้น
ถ้าวาง**ทั้ง** `fire()` ของ GM-028 **และ**บรรทัดนี้ที่สาขาเดียวกัน: บรรทัดแชทหนึ่งบรรทัดจะถูก authorize สองครั้ง
เขียน ndjson **สองแถว** และกิน rate limit ของ `chat_command` **สองเท่า** (ครั้งที่สองคือครั้งที่เริ่มปฏิเสธ
คำสั่งจริงของ GM เงียบ ๆ) · `lane_hooks/lane_gm_chat_command.py` ยังอยู่ที่เดิม **ลงทะเบียนบน point ที่ไม่มีใครยิง
= inert สนิท** ไม่ต้องลบ ไม่ต้องแก้ · ถ้า chief เลือกทาง action ตามใบนี้ ให้ **ไม่ต้องวาง `fire()`** เท่านั้นพอ

---

## ตอบข้อ (ข) ของ GM-028 ที่สายนี้ขอให้ chief ตอบก่อนอนุมัติ — **ตอบเองได้แล้ว คำตอบคือ "ไม่รั่ว"**

คำถามเดิม: *บรรทัด `/warp 2` ของ GM จะถูก broadcast ให้ผู้เล่นคนอื่นเห็นเป็นข้อความแชทธรรมดาไหม*
**ไม่ — และไม่ใช่ "คงจะไม่" แต่วัดได้จากซอร์สสองชั้น:**

1. **ชั้นซอร์ส (เส้นทาง fall-through ของจริง):** ทุกสาขา `CHAT_INPUT_VITAL_ID` ใน `runtime.py`
   (บรรทัด 4591, 4596, 4606, 4616, 4626, 4637, 4647, 4657, 4667, 4677, 4687, 4698, 4709, 4720)
   ถูกเกตด้วย `<ชื่อ>_hypothesis_scenario is not None` ทั้งหมด ⇒ บนบูตไร้แฟล็ก **ไม่มีสาขาไหนติด**
   เฟรมตกไปที่ `actions = super().dispatch(parsed)` และตัว dispatcher เดิม
   (`current/pf_login_game_server_v141.py`) **ไม่มีสาขา `0xAC52` เลย**:
   `grep -n "0xAC52\|44114\|CHAT_INPUT\|LocalTalk\|broadcast"` บนไฟล์นั้น = **0 แถว**
   มันเป็น if/elif chain keyed by `nested_id` ⇒ ไม่รู้จัก = `outbound` ว่าง = ไม่ตอบอะไรเลย
2. **ชั้นสถาปัตยกรรม:** เซิร์ฟเวอร์นี้ไม่มีกลไก broadcast อยู่เลย `grep -rn "broadcast"` ทั้ง
   `src/pirateforce_foundation/*.py` ได้ 3 แถว เป็นชื่อ scenario/ค่าคงที่ล้วน — แถวหนึ่งคือ
   `remote_player_hypothesis.py:1577` ที่ชื่อบอกตรงตัวว่า
   `no_second_connection_no_broadcast_no_send_lock_no_population_py_change`
   สอดคล้องกับ `FINDINGS_R18_SERVER_IS_STRICTLY_SERIAL.md` ⇒ **ไม่มีผู้เล่นคนที่สองให้รั่วใส่ตั้งแต่ต้น**

⇒ ข้อ (ข) **ปิดแล้ว** ไม่ต้องเปลี่ยนสัญญาของ `lane_hooks.fire()` ตามที่ใบ GM-028 เผื่อไว้
ข้อ (ก) (ชื่อ keyword `session=`/`payload=`) **ตกไปทั้งข้อ** เพราะใบนี้เป็น positional call ธรรมดา ไม่ผ่าน `fire()`

---

## ความปลอดภัย (ตรวจก่อนอนุมัติได้ที่สี่จุดนี้)

1. **ค่าเริ่มต้น = ไม่มีใครเป็น GM** — ฟังก์ชันเรียก `handle_local_talk_chat` ซึ่งตรวจ `gm_accounts`
   **ก่อนถอดรหัส payload** ⇒ ข้อความของผู้เล่นทั่วไปไม่ถูกถอด ไม่ถูก match ไม่ถูกเขียนที่ไหน
   เทส `test_a_non_gm_typing_the_working_command_gets_no_action` + `test_a_non_gm_line_is_never_decoded_or_audited`
2. **client ยกระดับตัวเองไม่ได้** — identity คือ `session.token` เท่านั้น และตรวจด้วย `type(token) is not str`
   (กัน str subclass ที่โกหกผ่าน `__eq__`) · เทส `test_the_payload_can_never_name_the_account_that_is_checked`
   ส่ง payload ที่ใส่ชื่อบัญชี GM มาในช่อง speaker แล้วยืนยันว่าไม่ได้อะไร
3. **ไม่มีไบต์ไหนออกวันนี้** — `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = None` (`RE-129` เปิดรอบนี้)
   ⇒ แม้ chief วางบรรทัดวันนี้ ผลคือ `GT-127` ปลดล็อก (อ่าน/audit ได้จริง) และ warp **ยังถูกปฏิเสธโดยตัวมันเอง**
   พร้อม event ชื่อ `gm_chat_warp_withheld_no_confirmed_force_pos_vital_version_re129_open`
   เหตุผลเดียวกับที่ `runtime.py:5107` เกต `0x5A19` ไว้ด้วย `GM_UPDATE_STATE_VITAL_VERSION_CONFIRMED`:
   **GT-101 วัดของจริงแล้วว่า version ที่ยังไม่พิสูจน์ = client ขึ้น modal error + ปิด socket ทิ้ง**
4. **exception ออกจากฟังก์ชันนี้ไม่ได้** — call site อยู่บน game-listener thread ที่ผู้เล่นทุกคนใช้ร่วมกัน
   ทุกความล้มเหลวถูกจับ ตั้งชื่อลง `session.events` แล้วคืน `None` · เทส `FailClosedTests` 8 ตัวยิงเซสชันรูปร้าย
   (ไม่มี token / token เป็น str subclass / `events.append` โยน / ไม่มี `events` เลย / composer ระเบิด /
   `handle_local_talk_chat` โยน `MemoryError` / `GmCommand.args` เป็น tuple subclass ที่โกหกผ่าน `__len__`)
   · event ไม่เคยพา**ข้อความที่ผู้เล่นพิมพ์**หรือ**ข้อความของ exception** (เก็บแค่ชื่อชนิด) ⇒ ปลอดภัยกับคอนโซล cp874
   เทส `test_an_exception_message_never_reaches_the_event_trail`
5. `production_allowed` — ไร้แฟล็กตามกฎข้อ 1 ของสายนี้ ความปลอดภัยอยู่ที่ allowlist ล้วน

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้
**ถ้า chief วางบรรทัดนี้อย่างเดียว:** `GT-127` บูตได้ — เจ้าของพิมพ์คำสั่งในกล่องแชท แล้วเห็นแถวใน ndjson
ว่าเซิร์ฟเวอร์อ่านออก (ยังไม่มีอะไรบนจอ)
**ถ้าได้ `RE-129` ด้วย (ตัวเลขเดียว แก้ค่าคงที่เดียว):** `GT-128` บูตได้ — **พิมพ์ `/warp` ในแชทแล้วตัวละครขยับจริง**
นั่นคือใบแรกของสายนี้ที่ตัดสินที่จอ

## nonclaims
1. [ไม่อ้าง] ว่าเส้นทางนี้ทำงานกับ client จริง — ยังไม่มีบูตไหนทดสอบ (`GT-127`/`GT-128`)
2. [ไม่อ้าง] ว่า warp ข้ามฉากทำได้ — `ForcePos` ไม่มีช่อง scene id (RE-090) โมดูลปฏิเสธข้ามฉากโดยตั้งใจ
3. [ไม่อ้าง] ว่า `/npc /item /lv /spawn /say` ทำอะไรได้ — parse + audit เท่านั้น ยังไม่มี wire ทั้งห้าตัว
4. [ไม่อ้าง] อะไรเกี่ยวกับ `BT_GM`/`GMUI_BASIC`/`0x51E9` — คนละประตู ประตูนั้นยังตาย (`RE-126` เปิด)
5. [ไม่อ้าง] ว่า `FORCE_POS_VITAL_VERSION_CONFIRMED` ควรเป็น 0 — สองค่าที่รู้แล้วไม่เท่ากัน (`0x5A19`=0,
   `SelectActor`=10) ต้องอ่านของจริงจาก ctor ของ `0x0E80` (`RE-129`)
6. [ไม่อ้าง] ว่าข้อความไทยผ่านเส้นทางแชทได้ — sample ที่จับได้เป็น ASCII ทั้งหมด

— LANE-GM รอบ `gr2q9j` · **ADDRESSEE: chief** · แทนที่ `CORE-REQUEST-GM-028`
