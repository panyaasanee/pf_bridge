# GM round 2026-08-27 ~04:1x-04:4x (+07:00) — RE-090 teleport wire codec + RE-089 docstring fix

ยึดล็อกด้วย draft PR ทั้งสอง repo ก่อนเริ่ม (`pf_bridge#159`, `pirate-force-server#87`) — ตรวจ GitHub API (MCP tool ต่อติดปกติรอบนี้) ก่อนยึดล็อก: ไม่มี PR หัวข้อขึ้นต้น `[LANE-GM]` เปิดค้างในทั้งสอง repo (pf_bridge มีแค่ `[LANE-E]` #157, pirate-force-server มีแค่ `[LANE-E]` #86 — ไม่ใช่ล็อกของสายนี้ ไม่แตะ) · fast-forward `pf_bridge` branch เข้า `origin/main` ก่อนเริ่ม (ตามหลังอยู่ 1 commit sync จาก bridge ไม่เกี่ยวกับสาย GM)

## ตรวจสถานะก่อนเริ่มงานจริง

ยืนยัน `pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (ขั้นแรกบังคับของทุกรอบ) · อ่านจดหมาย order 1630 ซ้ำ · อ่านกล่องจดหมายที่เกี่ยวกับสาย GM ที่ยังไม่เคยพับเข้า `docs/GM_LANE.md`: **`RE-089`/`RE-090`/`RE-091` ทั้งสามใบมีผลมาแล้ว** (chief ปิดหัวใบใน `CLIENT_RE_QUEUE.md` ไปแล้วที่รอบ `kdx85r` R184) แต่ยังไม่เคยถูกพับเข้าเนื้อโค้ด/เอกสารของสายนี้เอง — นี่คืองานของรอบนี้ ตามกฎ "ค้นก่อนถอด"

**ค้นแล้ว: เจอ** — อ่านทั้งสามใบเต็มฉบับจาก `notes_to_chief/`:
- `20260827_0016_RE-089-RESULT-STATE-PROPAGATION-PINNED-BMGM-FALSE-LEAD.md` — DONE/BOUNDED-NEGATIVE
- `20260826_2346_RE-090-RESULT-TELEPORT-FORCEPOS-WARP-FIELDS-PINNED.md` — PASS/DONE
- `20260826_2322_RE-091-RESULT-DEDICATED-GM-UI-NO-CHAT-PREFIX.md` — PASS/DONE

## สร้าง/แก้ (`pirate-force-server`, เขตเขียนของสายนี้ทั้งหมด)

- **ใหม่** `gm/teleport_wire.py` (GM-003 support) — encode/decode สำหรับ `ForcePos`/`CWarpResult`/`TeleportVital` ตาม byte layout ที่ RE-090 พิสูจน์แล้ว ปิดช่องว่าง "ยังไม่มี wire codec ให้ `warp`" ที่ `gm/commands.py` เขียนสโคปไว้ตั้งแต่รอบแรก — `warp` **ยังไม่ execute** รอบนี้แค่ทำให้ไบต์ที่ต้องส่งมีตัวสร้าง/ตัวอ่านจริงแทนที่จะไม่มีอะไรเลย ชื่อฟิลด์เป็น positional ล้วนสำหรับของที่ RE-090 ไม่ปิด semantic (แบบเดียวกับ `gm/command_wire.py`) ยกเว้น `scene_id`/`scene_seq` ที่ใช้ชื่อเดิมจาก `player_wire.py`/`npc_wire.py` (RE-077 crosswalk)
- **แก้** `gm/state_wire.py` docstring — ลบเบาะแส `bm_gm.tga` "ไอคอนบอลลูนแชท GM" ที่ RE-089 หักล้างแล้ว (จริง ๆ คือ glyph ลบเขียวของตัวเลขความเสียหายใน `FxNumberCache` คนละเรื่อง) เติมผล RE-089 ว่าตอบ `CORE-REQUEST-GM-001` แบบ DONE/BOUNDED-NEGATIVE (pin propagation ได้ แต่ไม่เจอ UI consumer) — พฤติกรรมโมดูลไม่เปลี่ยน สามฟิลด์ยังเป็น opaque integer เหมือนเดิม
- **แก้** `docs/GM_LANE.md` — เพิ่มแถว wire-facts ของ `ForcePos`/`CWarpResult`/`TeleportVital`, ปิดหัวข้อ "RE requests open" ทั้งสี่ข้อเดิมเป็น "RE requests closed", เพิ่มหัวข้อ "Modules delivered (RE-089/090/091 follow-up round)" อธิบายว่า RE-091 ทำให้ชัดว่า design การอ่าน chat text เป็นคำสั่ง GM ของสายนี้เป็น **นโยบายของโปรเจกต์เอง ไม่ใช่พฤติกรรม client ต้นฉบับ** (client จริงใช้ dedicated GM editor widget แยกจาก chat ปกติ)
- **ใหม่** `tests/test_gm_teleport_wire.py` (29 เทสหลังแก้ตาม adversary)

## `pf-adversary` (บังคับก่อน commit)

รอบแรกพบ 7 ข้อ (เรียงตามความรุนแรงจาก agent): 1 **HIGH**, 1 **MEDIUM-HIGH**, 2 **MEDIUM**, 2 **LOW-MEDIUM**, 2 **LOW** — แก้ครบทุกข้อก่อน commit แล้วส่งรอบสองยืนยัน (ผลรอบสองยังไม่กลับมาตอนเขียนใบนี้ ดูหมายเหตุด้านล่าง):

1. **HIGH** — docstring อ้างว่า `PF_FIELD_VALIDATION.tsv` เป็น "zero real frames" ทั้งสามข้อความ ผิด: `TeleportVital` มี 132 candidate frame ต่อทิศที่สถานะ `A2_STATIC_OPEN` (ตรวจซ้ำเองจาก tsv จริงยืนยันตรงกับที่ agent ชี้) — แก้ข้อความให้ตรง
2. **MEDIUM-HIGH** — ลำดับฟิลด์ `TeleportTarget` เขียน/อ่านตาม ascending object-offset (`field_0x10, field_0x11, scene_id, scene_seq, vec3`) แต่ข้อความ RE-090 ที่อ้างจริงเรียงเป็น `scene_id, scene_seq, field_0x10, field_0x11, vec3` — ลำดับสตรีมจริงตามที่ผลเดียวกันพิสูจน์แล้วว่า **ไม่ใช่** ascending offset เสมอ (top-level `+0x18` มาก่อน presence `+0x14`, aux `+0x40` มาก่อน `+0x38`) แก้ให้ตรงลำดับที่ RE-090 เขียนไว้ + เพิ่มเทสอิสระ (`test_target_payload_matches_re090_listed_stream_order`) ที่สร้างไบต์เองจาก `legacy.xxxtag()` ตรง ๆ ไม่ผ่านฟังก์ชันของโมดูล เพราะเทส round-trip เดิมจับบั๊กแบบนี้ไม่ได้ (encode/decode ผิดตรงกันเองก็ยัง round-trip ผ่าน)
3. **MEDIUM** — encoder อื่นนอกจาก `make_cwarp_result_payload` ไม่มีการตรวจช่วงค่า ตัวเลขนอกช่วงจะโดน mask เงียบ ๆ (`v & 0xFF` เป็นต้น) แทนที่จะ raise — เพิ่ม `_require_u8/u16/u32/u64` แล้วเรียกในทุก encoder ที่มีฟิลด์จำนวนเต็ม (`ForcePos` ไม่มีฟิลด์จำนวนเต็ม ไม่ต้องแก้)
4. **MEDIUM** — `decode_cwarp_result` ไม่มีเทสฝั่ง negative เลย (truncate/wrong-tag/trailing) ต่างจาก `ForcePosTests` — เพิ่มสามเทส
5. **LOW-MEDIUM** — กิ่ง hostile-input ของ `_read_untagged_wstring` (odd byte length, invalid UTF-16LE) และ `_write_untagged_wstring` (non-str) ไม่มีเทส — เพิ่มสี่เทสให้ `TeleportVitalTests`
6. **LOW** — สูตรคำนวณ vital id ของ `ForcePos`/`CWarpResult` (จากสูตร hash ที่มีอยู่แล้วในไฟล์ registry ไม่ใช่จากการถอดโค้ดตรง) เขียนด้วยความมั่นใจเท่าข้อเท็จจริงที่ RE พิสูจน์ตรง — ติดป้าย `[สมมติของสาย GM - รอ RE]` แยกชั้นความมั่นใจ
7. **LOW** — ตาราง wire-facts ใน `docs/GM_LANE.md` เขียน "direction NOT_OBSERVED" เหมือนกันทั้งสามแถว ทั้งที่ `TeleportVital` มี 132 candidate frame ต่างจาก `ForcePos`/`CWarpResult` ที่เป็นศูนย์จริง — แก้ให้แยกชั้นหลักฐาน

## ผลตรวจ

`test_gm_*.py` ทั้งหมด: **129 เทส ผ่านทั้งหมด** (จากเดิม 100 ก่อนรอบนี้ + 29 ใหม่ในไฟล์เดียว) · สวีตเต็มรันไม่สำเร็จบน container นี้ (`ModuleNotFoundError: capstone` — 18 error เดิมไม่เกี่ยวกับรอบนี้ เป็นเทส static-RE ที่ต้องมีเครื่องมือ disassembler ซึ่ง cloud clone นี้ไม่มี ยืนยันด้วย `grep -oE "^ERROR.*"` ว่าไม่มีชื่อทดสอบไหนพาดพิง `gm`)

## ยังไม่ทำ (ตั้งใจ)

- ยังไม่ execute หรือ dispatch คำสั่งใด ๆ — เหมือนเดิมทุกรอบ `warp` ยังแค่ parse+log
- ยังไม่ยื่น `CORE-REQUEST` ใหม่สำหรับต่อสาย warp execution เข้า `runtime.py` — ต้องมีจุดตัดสินใจที่ใหญ่กว่าจดหมายบรรทัดเดียว (inbound dispatch ของ `0x51E9` ไม่เคยมีมาก่อนเลยในเซิร์ฟเวอร์นี้, ต้องเลือกจุด gate สิทธิ์ GM ก่อน execute, ต้องเลือกว่าจะส่ง `ForcePos` หรือ `TeleportVital` ก่อน) เสนอเป็นรอบถัดไปที่ทำเฉพาะเรื่องนี้
- `TeleportTarget` field order (ข้อ 2 ข้างบน) เป็นการอ่านข้อความ RE-090 เอง ยังไม่ยืนยันกับเฟรมจริง — `PF_FIELD_VALIDATION.tsv` มี 132 candidate frame ของ `TeleportVital` ที่ `A2_STATIC_OPEN` รอรอบ RE ถัดไปนำมาทดสอบกับ codec นี้ก่อนใช้กับ client จริง (ระบุไว้ใน docstring/เอกสารแล้ว ไม่ใช่ของใหม่ที่ปิดลับ)

## ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้

**ยังไม่มี** — รอบนี้เป็นโค้ด/เอกสารฝั่งเซิร์ฟเวอร์ล้วน (unit test, ไม่มี client, ไม่มี wiring เข้า runtime) ผู้เทสยังไม่มีอะไรทำในเกมต่างจากเมื่อวาน

## nonclaim

โค้ดรอบนี้เป็น wire codec เท่านั้น ไม่มีการ execute warp จริง ไม่มีการอ้างว่าไบต์ที่สร้างได้จะถูก client จริงยอมรับ (field ส่วนใหญ่ semantics ยังไม่พิสูจน์, ลำดับฟิลด์ `TeleportTarget` เป็นการอ่านข้อความ ยังไม่ยืนยันกับเฟรมจริง) และไม่มีการอ้างว่า RE-089 ปิดคำถามความหมายของ `GM_UpdateGMStateVital` — ปิดแค่ propagation ไม่ใช่ semantics

## ค้าง

- ผลตรวจ `pf-adversary` รอบสอง (ยืนยันการแก้ทั้ง 7 ข้อ) ยังไม่กลับมาตอนบันทึกใบนี้ — ถ้าพบข้อใหม่จะแก้เป็นคอมมิตต่อท้ายก่อนจบรอบ ถ้าไม่พบจะจบรอบตามขั้นตอนปกติ
- `CORE-REQUEST` สำหรับต่อสาย warp execution เข้า `runtime.py` — เสนอเป็นรอบถัดไป (เหตุผลด้านบน)
- `TeleportTarget` field order รอยืนยันกับ 132 candidate frame ของ `TeleportVital` (`A2_STATIC_OPEN`) — รอบ RE ถัดไป
