[ถึง: chief · cc: COO · Panya | จาก: LANE-GM (pirate-force-server session 8791h3) | 2026-08-27T15:24+07:00]

ตอบ: `notes_to_chief/20260827_1425_PANYA-ORDER-GM-warp-to-other-maps-two-paths.md` ทาง ก ("GM login-scene
override") — เพดานเวลาที่ระบุคือ "ใบแรกรอบถัดไปของสาย GM" นี่คือใบนั้น

**เกี่ยวข้องกัน แต่คนละเรื่อง**: ใบนี้ไม่แตะ `GM_UpdateGMStateVital` (`0x5A19`) เลย — override ที่ใบนี้ขอต่อสาย
คือ scene ที่ client ล็อกอินเข้าไป (ผ่าน `START_GAME_RES` เดิม) ไม่ใช่การส่งเฟรมสถานะ GM ใด ๆ เพิ่ม จึงไม่ถูกบล็อก
โดย `CORE-REQUEST-016`/`RE-105` (ดูใบแยก)

# CORE-REQUEST-015 (เสนอ · รอ chief เขียนแถวลงทะเบียน `CHIEF_CONTINUATION.md`) — GM login-scene override: สอง
จุดต่อสาย

## เลขที่เสนอ
ทะเบียนล่าสุดที่พบใน `notes_to_chief/` มีถึง **CORE-REQUEST-014** (chief, M2 deadline risk) — เลขถัดไปที่ว่างคือ
**015** (ใบพี่น้องรอบนี้ที่เขียนพร้อมกันใช้ **016** — grep ยืนยันก่อน push ทั้งสองใบว่าไม่ชนเลขกัน)

## ① โมดูล
`src/pirateforce_foundation/gm/login_scene_override.py` (ใหม่รอบนี้) ฟังก์ชัน `get_login_scene_override`

## ② ฟังก์ชันที่ต้องเรียก — จุดที่ 1 (login, บังคับ)
```python
from pirateforce_foundation.gm.login_scene_override import get_login_scene_override

override_scene_id = get_login_scene_override(self.token)
# None -> เดินเส้นทางเดิมทุกอย่าง ไม่มีอะไรเปลี่ยน (นี่คือ default สำหรับทุกบัญชีที่ไม่ตั้งค่า)
# int -> ใช้ scene_id นี้แทนค่าเริ่มต้นตอนประกอบ START_GAME_RES/สนาม spawn ของ session นี้
```
- คืน `None` เสมอ เว้นแต่บัญชีนั้น **ทั้ง** อยู่ใน `gm_accounts` (เช็คซ้ำภายในฟังก์ชันเอง ไม่ต้องเช็คซ้ำฝั่ง
  caller) **และ** มีรายการใน `config/gm_login_scene.json` (env override `PF_GM_LOGIN_SCENE_CONFIG`) ที่ตั้งชื่อ
  scene_id ที่มีจริงใน `gm/scene_catalog.py` — ไฟล์ config เปล่า/ไม่มีไฟล์ = ไม่มี override สำหรับใครเลย
  (ค่าเริ่มต้นปลอดภัย)
- config ที่เพี้ยน (top-level ไม่ใช่ object, `gm_login_scene` ไม่ใช่ dict, scene_id ไม่ใช่ int, scene_id ไม่รู้จัก)
  โยน `ValueError` ทันที — **ทั้งไฟล์**, ไม่ใช่แค่บัญชีที่พิมพ์ผิด (blast radius นี้ตั้งใจ ไม่ใช่บั๊ก ดู
  `docs/GM_LANE.md` "Known, accepted blast radius" — chief ตัดสินใจเองได้ว่าจะ catch แบบ per-account ที่จุดเรียก
  หรือปล่อยให้ทั้งไฟล์ fail-loud เหมือนที่ `gm/accounts.py` ทำกับ `gm_accounts.json` เองอยู่แล้ว)

## ② ฟังก์ชันที่ต้องเรียก — จุดที่ 2 (census ของฉากที่ override ไป, ยังไม่มีของให้เรียกจากเขตนี้)
เมื่อ `override_scene_id is not None`: ประกอบ census ของฉากนั้นจาก `Data\Scene\Save\bgXXXX\bgXXXX.npc` ด้วย
parser เดิม `gamedata/pf_decode_lua_npc.py` (สาย A/B ใช้ทางนี้อยู่แล้วสำหรับ `bg0001`) บวก roster hostile ของ
สาย B ถ้ามีสำหรับฉากนั้น (คำสั่งเดิมอ้างว่า `bg0015` มี) — **จุดนี้ไม่มีฟังก์ชันในเขตของสาย GM ให้เรียก** เพราะ
เป็นการผสมข้อมูลข้ามสาย (A ให้ scene registry, B ให้ mob roster) ที่กฎ "ห้ามก๊อปตรรกะของสายอื่นมาไว้ในเขตตัวเอง"
ห้ามสายนี้ทำเอง — ส่งต่อให้ chief ตัดสินใจว่าจะเรียกของสาย A/B ตรง ๆ จากจุดนี้ใน `runtime.py` อย่างไร

## ③ ตรงไหนของ runtime
1. **login**: จุดที่ `runtime.py` ตัดสินใจ scene_id เริ่มต้นสำหรับ session ใหม่ (ก่อนประกอบ `START_GAME_RES`) —
   สายนี้ไม่รู้เลขบรรทัดปัจจุบัน (ไม่ใช่เขตเขียน) แต่ควรอยู่ใกล้บริเวณเดียวกับที่ `is_gm_account`/GM state frame
   ถูกเรียก (`runtime.py:4746` ปัจจุบัน) เพราะทั้งคู่ต้องใช้ `self.token` ตัวเดียวกัน
2. **census**: จุดที่ scene census ปกติถูกประกอบสำหรับ session (เทียบเคียงกับ `world_scene_liveness`/
   `WORLD_SCENE ... population=bg0001_census` ที่เห็นในคอนโซลทดสอบปัจจุบัน) — ต้อง branch ตาม
   `override_scene_id` แทนที่ scene_id ปกติเมื่อไม่ใช่ `None`

จุดเกิด (spawn position) ที่ scene override: ใช้ placement index 0 ของ `.npc` ฉากนั้นตามคำสั่งเดิม ("ไม่ต้องถูก
ขอให้ยืนบนพื้น")

## ④ เทสที่พิสูจน์
- `tests/test_gm_login_scene.py` (15 เทสใหม่): default-empty, gating (GM+entry / GM-ไม่มี entry /
  ไม่ใช่-GM-มี-entry / ไม่อยู่ในรายชื่อเลย), malformed config ครบ (non-object top level, non-dict
  `gm_login_scene`, non-int scene_id, `bool`-เป็น-int, scene_id ไม่รู้จัก), revocation-มีผลทันที
- `tests/test_gm_*.py` ทั้งชุด: 203/203 (200 เดิม + 3 ใหม่ — 2 จาก non-object top-level ที่พบระหว่าง
  pf-adversary ทั้งไฟล์นี้และ `gm/accounts.py`, 1 revocation test)
- เกณฑ์ก่อนเรียกเจ้าของ (ตามคำสั่งเดิม, ยังไม่ทำรอบนี้ — เป็นของ chief หลังต่อสาย): บูต headless ไร้แฟล็ก + env
  config → grep คอนโซล เห็น `START_GAME_RES scene_id=<N>` (N = ค่า override) และ census ของฉาก N > 0 actor →
  ค่อยเปิดใบ GT ให้ผู้เทส

## ⑤ ค้นแล้ว
ค้น `pf_bridge/external/00_SEARCH_HERE_FIRST.md`/`pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` แล้ว: ไม่มีของใหม่
ที่ต้องถอดเพิ่ม (ใบนี้ใช้ตาราง `SCENE_NAME_TIP` เดิมของ GM-004 ทั้งหมด) ค้นใน `pirate-force-server` เองด้วย: grep
`gm_login_scene`/`login_scene_override`/`PF_GM_LOGIN_SCENE_CONFIG` ใน `runtime.py` = 0 hit ก่อนรอบนี้ ยืนยันว่า
ไม่มีจุดต่อสายเดิมให้ชนกัน

## ⑥ pf-adversary
รอบเดียว พบ 3 ข้อจริง (แก้ครบก่อน push): (1) top-level JSON ที่ไม่ใช่ object โยน `AttributeError` แทน
`ValueError` ที่เอกสารสัญญาไว้ — ช่องเดียวกันมีอยู่ใน `gm/accounts.py` เดิมด้วย แก้ทั้งคู่พร้อมกัน (2) blast radius
ของการ validate ทั้งไฟล์ (บันทึกไว้เป็น known/accepted ข้างบน ไม่แก้) (3) เทสไม่เคยพิสูจน์ revocation จริง (เพิ่ม
เทสใหม่แล้ว) — รายละเอียดเต็มใน `rounds/GM_20260827_1524_login-scene-override-plus-gt101-safety-guard.md`

## ⑦ nonclaim
ใบนี้ไม่ได้อ้างว่าเจ้าของเห็นแมพอื่นได้แล้ว — ฟังก์ชันที่สร้างยังไม่ถูกเรียกจากที่ไหนใน `runtime.py` เลย
(0 call site) จนกว่า chief ต่อสายทั้งสองจุดข้างบน ไม่มีอะไรเปลี่ยนสำหรับผู้เล่นทั่วไปหรือบัญชี GM ใด ๆ จากรอบนี้
