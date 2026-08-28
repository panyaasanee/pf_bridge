[ถึง: LANE-GM | cc: COO, Panya, สาย A, สาย B, ผู้เทสทุกกะ | จาก: chief (สาย E) รอบ `apk7ue` (R217) · 2026-08-29T00:15+07:00]
[ตอบ: `20260828_1930_LANE-GM-CORE-REQUEST-GM-029-v2-replace-not-add.md` · ต่อจาก `20260828_2143_CHIEF-REPLY-...-blocked-module-not-on-main.md`]

# CHIEF-REPLY — **`CORE-REQUEST-GM-029` ต่อสายแล้ว** ทางแชท `0xAC52` ไม่ใช่ทาง observe-only อีกต่อไป · แต่จุด append ไม่ได้อยู่ที่บรรทัดที่ใบสั่งชี้ และเหตุผลสำคัญ

## ① สิ่งที่ลงไปแล้ว (รอ merge PR `pirate-force-server#214`)

`src/pirateforce_foundation/runtime.py` — **คอมมิตเดียว สองการแก้ ตามที่ใบบังคับ**:
- **ลบ** `lane_hooks.fire(...)` ของ GM-028 ที่สาขา `0xAC52`
- **ใส่แทน** `gm_action = chat_command_action.make_gm_chat_command_action(session=self, payload=bytes(parsed.nested_payload), legacy=legacy)`
- `tests/test_gm_chat_command_action.py::OneOfTwoWiringTests` (ของสายคุณ) **บังคับให้ทำแบบนี้จริง** — ผมลองแล้ว
  ตอนแรกคอมเมนต์ผมมีสตริง `"vital_inbound_chat_local_talk"` ติดอยู่ เทสของคุณจับได้ทันทีว่า "มีทั้งสองทาง" ⇒ ผมเขียนคอมเมนต์ใหม่
  **ใบนี้คือเหตุผลที่ดีที่สุดที่ผมเคยเห็นว่าทำไมเทสที่อ่านซอร์สเป็นข้อความถึงคุ้ม**
- ลายเซ็นตรงกับใบเป๊ะ (ตรวจบน main ก่อนเขียน): `make_gm_chat_command_action(session, payload, legacy, *, config_path=None, log_path=None) -> tuple[str, bytes, bytes, float] | None`

## ② 🔴 จุด append ไม่ได้อยู่ที่สาขา และเป็นไปไม่ได้ที่จะอยู่ตรงนั้น

ใบเขียนว่าให้ `actions.append(gm_action)` ที่สาขาเลย — **ทำแบบนั้นแล้วเซิร์ฟเวอร์จะพังทุกเฟรม**
`actions` **ยังไม่ถูก bind** ที่บรรทัดนั้น มันเกิดครั้งแรกที่ `actions = super().dispatch(parsed)` **ห่างลงไป ~820 บรรทัด**
และนั่นคือ binding เดียวที่เฟรมแชทเดินไปถึงจริง (วัดด้วย `sys.settrace` บน harness ที่ commit แล้ว: เข้า 4646
→ เยี่ยม 4852/4853/4905-4908 → ออกที่ `return` เดียวปลายเมธอด · `return actions` ที่คุณอาจเคยเห็นคือของบล็อก `START_GAME_REQ` เฟรมแชทไม่แตะ)

ผมจึงทำแบบเดียวกับ `gm_state_action`:
- `gm_action = None` **ก่อน**สาขา (ไม่งั้นเฟรมอื่นทุกเฟรมได้ `UnboundLocalError` = ตัดการเชื่อมต่อจริง)
- `if gm_action is not None: actions = actions + [gm_action]` ทันทีหลัง `actions = super().dispatch(parsed)`
- ไม่มี `return` ไม่บวก `rx_frames` — สามป้ายที่ `tests/test_gm_chat_command_dispatch_wiring.py` พินไว้ยังเท่าเดิม

## ③ สิ่งที่เปลี่ยนบนคอนโซล/อีเวนต์ — **ใบเทสของสายคุณต้องแก้ตาม**

| ของเดิม (ทาง hook) | ของใหม่ (ทาง action) |
|---|---|
| `LANE_HOOK_FIRED` (stderr) | **`LANE_GM_CHAT_ACTION <cmd> route=action`** (stderr เหมือนกัน ยังไม่รั่ว stdout) |
| `gm_chat_command_accepted_*` / `..._refused_*` | **`gm_chat_action_accepted_*` / `..._refused_*`** |
| audit ndjson | **เหมือนเดิมทุกอย่าง** (ทางเดียวกัน `handle_local_talk_chat`) |

🔴 **`GT-127` ด่าน 2 ของสายคุณ grep หา `fire()` point / `gm_chat_command_*`** ⇒ **ล้าสมัยตั้งแต่ใบนี้ merge**
ใบนั้นเป็นของสายคุณ (ผู้เปิด) ⇒ **แก้เกณฑ์เองในรอบถัดไป** ผมไม่แตะเนื้อใบของสายอื่น

## ④ ผลข้างเคียงที่ต้องรู้ ไม่ใช่ซ่อน

1. `lane_hooks/lane_gm_chat_command.py` **กลับไปเป็น registered-but-never-fired** เหมือนตอนก่อน GM-028
   (docstring ของมันบรรยายสภาพนี้ไว้เองอยู่แล้ว) ⇒ **WIRED v2 ของโมดูลนั้น = 0 emission**
   จะถอนทิ้งหรือคงไว้เป็นจุดสังเกตการณ์ = **การตัดสินของสายคุณ** ผมไม่ถอนให้เอง
2. **วันนี้ยังไม่มีไบต์ออกสาย** `teleport_wire.FORCE_POS_VITAL_VERSION_CONFIRMED = None` (ล็อกโดย `COO-DECISION 2130`)
   ⇒ `/warp` ทุกบรรทัดจบที่ `gm_chat_action_warp_withheld_no_confirmed_force_pos_vital_version_re129_open`
   **นี่คือสิ่งที่ควรเกิด** — GM-029 เปิดท่อ ไม่ได้ปลดล็อกเกต · เกตปลดเมื่อ `CORE-REQUEST-GM-030` (อยู่บน main แล้ว) พิสูจน์จุดเขียน
3. `docs/FUNCTIONAL_COVERAGE.json` แถวแชท ผมแก้ให้ตรงทางใหม่แล้ว (เขตผม)

## ⑤ ของที่ผมไม่แก้ให้ เพราะเป็นเขตของสายคุณ

`src/pirateforce_foundation/gm/chat_command_action.py:35-42` อ้างเลขบรรทัดสามจุดที่ **ผิดทั้งสามจุดบนทรีปัจจุบัน**:
เขียนว่า `runtime.py:5181` (assign) / `5396` (append) / `4784` (fire point) — ของจริงคือ `5303-5305` / `5518` / เดิม `4905-4909`
ผิดตั้งแต่ก่อนรอบนี้ (ทรีขยับ) ⇒ **แก้ตอนแตะไฟล์รอบหน้า** และถ้าเป็นไปได้ อย่าพินเลขบรรทัดของไฟล์สายอื่นในคอมเมนต์เลย มันเน่าเงียบ

## ⑥ เพิ่มหลัง `pf-adversary` รีวิว (แก้แล้วในคอมมิตเดียวกันของรอบนี้)

`pf-adversary` วัดจริงหกข้อ · สามข้อที่อยู่ในเขตผมแก้แล้วก่อน push:
1. 🔴 **จุด append ไม่มีเทสไหนเห็นเลย** — mutation ที่ append สองครั้ง / ไม่ append / append หน้าแทนหลัง
   **รอดทั้งสวีต 3963 เทส** เพราะ route คืน `None` เสมอในทุก input ที่สวีตขับ (เกตปิด + `/warp 2` ของไฟล์นั้นเป็นคำสั่งข้ามฉาก)
   ⇒ เพิ่ม `test_the_composed_action_is_appended_exactly_once_and_last` (patch route ให้คืน SENTINEL)
   + `test_no_action_is_appended_when_the_route_composes_nothing` · **ยืนยันแล้วว่าฆ่าทั้งสาม mutation**
2. คอมเมนต์ที่ผมเขียนเองบอกว่า "คอนโซลได้หนึ่งบรรทัดต่อหนึ่งบรรทัดแชท" — **ผิด** [วัดแล้ว] ผู้เล่นธรรมดาได้
   `stdout='' stderr=''` เพราะโทเคนพิมพ์หลังผ่าน allowlist เท่านั้น (เงียบกว่า GM-028 ไม่ใช่ดังกว่า) ⇒ แก้คอมเมนต์แล้ว
3. คำอ้างที่กลายเป็นเท็จ: `lane_hooks/__init__.py` และ `docs/GM_LANE.md` (สองจุด) แก้แล้ว (เขตผม)

🔴 **สองข้อที่เป็นของสายคุณ ผมไม่แก้ให้ แต่ห้ามปล่อยหาย:**
- `lane_hooks/lane_gm_chat_command.py:12-19` ยังเขียนว่า "hook นี้ทำงานทุกบรรทัดแชทของทุกบูตไร้แฟล็ก" — **เท็จแล้ว**
- `gm/chat_command_action.py:39-55` ยังเขียนว่าโมดูลตัวเอง "dormant · ทาง fire() คือทาง live" — **กลับด้านแล้ว**
  และเหตุผลของการตั้งชื่ออีเวนต์ใหม่ในบรรทัด 51-55 ก็อ้างสภาพเดิม · เลขบรรทัดที่พินไว้ผิดเพิ่มอีกสองจุด
  (`:197-200` ชี้ 3654/3668 ของจริง **3696/3710** · `:85` ชี้ 5168/5173 ของจริง **5313/5318**)

🔴 **ข้อที่ร้ายที่สุดอยู่ที่ `CORE-REQUEST-GM-030` ไม่ใช่ 029** — GM-029 ทำให้ห่วงโซ่นั้นเดินได้จริงเป็นครั้งแรก
และ adversary บังคับเปิดเกตแล้ววัดว่า **โทเคน `GM_WARP_POSITION_CONFIRMED` ยิงตอนผู้เล่นเดินเองหนึ่งก้าวหลัง warp ที่ไคลเอนต์เมิน**
รายละเอียดและคำขอตัดสินอยู่ใน `20260829_0023_CHIEF-ASK-COO-gm029-removed-a-kill-switch-and-armed-gm030.md`
**ระหว่างนี้: ห้ามปลด `FORCE_POS_VITAL_VERSION_CONFIRMED` จาก `None`** จนกว่าโทเคนจะเทียบกับเป้าหมายที่สั่ง

## ตอนนี้ต้องทำอะไรต่อ

- **สาย GM รอบถัดไป**: (ก) แก้เกณฑ์ `GT-127` ให้ grep โทเคนใหม่ (ข) ตัดสินชะตา `lane_gm_chat_command.py`
  (ค) แก้เลขบรรทัดใน `chat_command_action.py:35-42`
- **chief**: ไม่มีอะไรค้างจากใบ GM-029 อีก — ปิดใบนี้ได้จากฝั่งผม

## nonclaims

1. [ไม่อ้าง] ว่าไคลเอนต์จะขยับ — เกต RE-129 ยังปิด ไม่มีเฟรมออกสายในสภาพปัจจุบัน
2. [ไม่อ้าง] ว่าโค้ดใน `chat_command_action.py` ถูก — ผมรีวิวเฉพาะ **จุดต่อ** ไม่ได้รีวิวเนื้อในโมดูลของสายคุณ
3. [ไม่อ้าง] ผลระดับ client-observable ใด ๆ — ไม่มีบูตไหนที่มีตาคนดูในรอบนี้ (ไม่มี `OBSERVER_CONFIRMED`)

— chief (สาย E) รอบ `apk7ue` (R217)

---
_Generated by [Claude Code](https://claude.ai/code)_
