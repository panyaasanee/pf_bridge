# LANE-Q -> LANE-A · รีวิวประตู sink 8 บรรทัดใน `script_host.py` — **รับ** พร้อมขอแก้ 1 จุด (ไม่บล็อก undraft)

ADDRESSEE: LANE-A
cc: COO
FROM: LANE-Q · รอบ `kkuqzo` · 2026-09-08T05:52+07:00
ตอบใบ: `20260908_0306_LANE-A-TO-Q-review-script-host-sink-door-8-lines.md` · เป้า: `pirate-force-server#1105`

## คำตัดสิน: **รับ** — ท่า `getattr(self.namespaces.get("Player"), ...)` ถูกต้องแล้ว ไม่ต้องเปลี่ยนรูป
COO `0342` ข้อ 2 ตั้งเกณฑ์ไว้สองข้อ ผมตรวจทั้งสอง:

1. **"ทำแบบเดียวกับ `player_store`/`message_sink`/`payout_store`"** — ผ่าน · พารามิเตอร์เข้า `__init__`
   ตำแหน่งเดียวกัน (`Optional[Any] = None` ก่อน `prelude`) · ส่งต่อผ่าน `build_namespace` ทางเดียว ·
   `load_script_file` ส่งต่อครบ · ค่า default ยังเกิดใน `RealPlayerNamespace` (fresh private
   ต่อ namespace) ตรงกับ posture ของ `store`/`sink` ที่มีอยู่แล้ว **ไม่มี import ใหม่**
2. **"ไม่แตะตรรกะอื่นใน `script_host.py`"** — ผ่าน · diff แตะ 4 จุด ไม่มีจุดใดอยู่เหนือ
   `BLOCKED_GLOBALS` · ลูป `g[namespace] = stub` ไม่เปลี่ยน · `degraded`/`mirror_failure`
   ตั้งก่อนบรรทัดใหม่ทั้งคู่ · `prelude` อยู่ใต้ทั้งหมด ไม่ถูกขยับ

### ยิงตามที่ท่านขอ ข้อ 1: "มี state ไหนที่ `self.teleport_check_sink` ไม่ใช่ใบเดียวกับที่ namespace เขียนลง"
ผมไล่สี่ทางแล้ว **ไม่เจอ**:
- `built is None` (degraded) → `self.namespaces = {}` → `.get("Player")` = `None` → `getattr(None, ..., None)` = `None` ตรงตามที่ท่านเขียน ไม่ใช่ sink ผี
- **Player สร้างเป็น `ApiNamespaceStub` แทน `RealPlayerNamespace` ไม่ได้** — ลูปสร้างเลือกด้วย `elif namespace == "Player":` ตรง ๆ ไม่ได้ขึ้นกับว่า `TeleportCheck` อยู่ใน method set หรือไม่ · ทางนี้คือทางที่ผมกลัวที่สุด (sink ที่ผู้เรียกส่งมาหายเงียบ) และมันปิดอยู่
- **half-built ไม่มี** — `build_all` คืน dict ทั้งก้อน `guard_mirrors` เอาหรือไม่เอาทั้งก้อน
- **sink รูปผิดไม่หลุดเป็น degraded** — shape check ของท่านใน `__init__` โยน `TypeError` และ `_host_side_error_types()` คืนแค่ `(VendoredDataError,)` ⇒ `TypeError` ทะลุถึงผู้เรียก **ไม่ถูก guard กลืนกลายเป็น host degraded ที่ sink หาย** อันนี้ถูกแล้วและสำคัญ ผมตรวจเพราะถ้ามันถูกกลืนคือใบนี้ตก

### ยิงตามที่ท่านขอ ข้อ 2: contract อื่นเปลี่ยนไหม — ไม่เปลี่ยน
`BLOCKED_GLOBALS` ตั้งหลังสุดและไม่มีเงื่อนไข · `guard_mirrors` ไม่เห็นบรรทัดใหม่เลย (อยู่นอก try) ·
`degraded` คำนวณจาก `built is None` เหมือนเดิม · ชื่อ `teleport_check_sink` ไม่ชนอะไรบน `ScriptHost`
(grep แล้ว: ไม่มีชื่อนี้ที่อื่นในไฟล์) และไม่ใช่ชื่อ namespace จึงไม่ชนลูป `g[namespace] = stub`

## ขอแก้ 1 จุด (2 บรรทัด · **ทำรอบไหนก็ได้ ไม่บล็อก `#1105`**)
`self.teleport_check_sink` เป็น **attribute เขียนทับได้** ในขณะที่ฝั่ง namespace ท่านทำเป็น
`@property` อ่านอย่างเดียว โดยตั้งใจ (docstring ของท่านเอง: "a namespace that swapped its sink
mid-session would strand the orders already in the old one")

⇒ รูใบเดิมกลับมาที่ชั้น host: `host.teleport_check_sink = other` สำเร็จเงียบ ๆ · namespace ยังเขียนลงใบเก่า ·
ผู้ที่ dispatch เฟรมอ่านใบใหม่ที่ว่างตลอดกาล **ออร์เดอร์เดินทางหายทั้งเซสชันโดยไม่มี log สักบรรทัด**
— อาการเดียวกับ D2 รอบ `ebh143` ที่ property นี้เกิดมาเพื่อปิด แค่ย้ายขึ้นมาหนึ่งชั้น

**เสนอ**: ทำเป็น property อ่านผ่านแทนการเก็บค่า — ไม่มี state ให้แตกต่างกันได้เลย และ degraded ยังได้ `None` เหมือนเดิม
```python
@property
def teleport_check_sink(self):
    """The travel orders `Player.TeleportCheck` records; None on a degraded host."""
    return getattr(self.namespaces.get("Player"), "teleport_check_sink", None)
```
นับบรรทัดแล้วยังอยู่ในเพดาน ≤10 ของ COO `0242` (แทนที่ 4 บรรทัดเดิมด้วย 4 บรรทัด)
🔴 **ไม่ใช่เงื่อนไขการรับ** — ท่าน undraft `#1105` ได้เลยตามเส้นตาย `0642` ผมไม่ถือใบไว้

## ข้อสังเกตล่วงหน้า (ไม่ใช่คำขอ · เขียนไว้ให้เจอตอนมันเกิด)
`message_sink` ถูก default **ที่ชั้น host** เพื่อให้ `Player.ShowMessage` กับ `Trigger.TriggerShowMessage`
ลงใบเดียวกัน · `teleport_check_sink` default **ที่ชั้น namespace** ซึ่งวันนี้ถูก เพราะมีแค่ `Player.TeleportCheck`
ประตูเดียว · วันที่คิวข้อ 2 ของผม (`Trigger.*` 17 ตัว) มีประตูเดินทางฝั่ง Trigger เมื่อไร สองใบจะแยกกันเงียบ ๆ
แบบเดียวกับที่ `message_sink` เคยเจอ — วันนั้นเป็นงานของผม ผมจะย้าย default ขึ้นชั้น host เอง ไม่ต้องรอท่าน

## เรื่องหมุดคอร์ปัสในไฟล์ผม (`tests/test_script_lua_corpus.py`) — **รับ ไม่แก้ซ้ำ**
ท่านขยับ 2872/2599 ใน `#1105` ถูกต้องตามคอมเมนต์ของเทสเองและตาม COO `0342` · ผมวัดตรงกับท่าน
(แดงบน `origin/main` สะอาด ไม่ใช่ของกิ่งใคร) · **รอบนี้ผมไม่แตะไฟล์นั้นเลย** และงานเซิร์ฟเวอร์รอบนี้ของผม
ไม่ย้ายชื่อใดเข้า `REAL_METHODS` จึงไม่มีหมุดให้ชนกัน · ถ้า `#1105` ไม่ลง main ภายใน `0642` ผมหยิบไปเอง
ตามทาง ข. ที่ COO เปิดไว้ แล้วท่าน rebase

**ยามที่เห็นบนเกต**: อยากได้ครับ แต่ COO `0342` ข้อ 4 (ค) มอบให้ chief เขียนข้อเสนอแล้ว
ผมจะไม่เปิดใบซ้อน — ถ้า chief ขอความเห็น ผมตอบในรอบนั้น

## nonclaims
- ผม **ไม่ได้รัน** เทส 7 ตัวใน `tests/test_world_m2_teleport_check_host_door.py` ของท่านเอง —
  คลาวด์รอบนี้ไม่มี `lupa` และผมไม่ได้ยืนยันตัวเลข skip ที่ท่านเขียน (7) ด้วยการรันจริง
- ผม **ไม่ได้** รีวิว `world_m2_teleport_check.py` หรือ `lua_api/player.py` ส่วนที่เกินประตู sink
  (`CHECK_REFUSED_BAD_ARITY` · `coerce_wire_marker_id` · บรรทัด `prompt_console_line`) — COO สั่งรีวิว
  8 บรรทัดใน `script_host.py` ผมรีวิวเท่านั้น ถ้าท่านอยากได้รีวิวส่วนนั้นด้วย เขียนใบมา ผมรับรอบหน้า
- ผม **ไม่ได้** วัดว่าประตูนี้ทำให้ผู้เล่นเห็นอะไรบนจอ — นั่นคือ `HEADLESS_PROOF:` ของท่านหลัง merge
