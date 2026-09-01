[ถึง: chief, COO, เจ้าของ | ADDRESSEE: CHIEF | cc: COO, เจ้าของ | จาก: LANE-GM รอบ `ku3jz6` · 2026-09-01T21:32+07:00]

# RE-164-RESULT — ข้อ 3 ปิดด้วย static (committed sync), ข้อ 1 ได้ write-site, และธง GameMaster.dll สำหรับ P-3

## ค้นแล้ว: เจอ

`pf_bridge/external/00_SEARCH_HERE_FIRST.md`, `pf_bridge/gamedata/00_SEARCH_HERE_FIRST.md` ตรวจแล้วก่อน
เริ่ม (กฎ "ค้นก่อนถอด") — คำตอบจริงไม่ได้อยู่ใต้ดัชนีสองไฟล์นั้น แต่อยู่ใต้
`notes_to_chief/reference_codex_attr/` ซึ่งเป็นไดเรกทอรีที่ sync จากเครื่องบริดจ์เข้ามาเมื่อ 19:54+07 วันนี้
(commit `a0909b1`, "sync: 19 file(s) from the Windows bridge") — **หลังจาก** รอบ `20260901_0626`
เคยตรวจสามไฟล์นี้ตรง ๆ แล้วเขียนไว้ว่า "ค้นแล้ว: ไม่เจอ" (`notes_to_chief/20260901_0626_LANE-GM-STATUS-
p3-gmui1-hypothesis-stub-gm-a-merge-confirmed-gm-b-still-blocked.md:47`) — ไม่ใช่ไฟล์ที่หายไป เป็นไฟล์
ที่ยังไม่ถูก sync มาตอนนั้น

## สรุปสั้น

`RE-164` (`CLIENT_RE_QUEUE.md`) มี 4 ข้อค้าง 2 ข้อ (#1 connection-context write-site, #3 current-UI
object-key) ตั้งแต่รอบ `1q7nxu` ทั้งคู่ถูกแปะป้าย STATIC-ON-BRIDGE (ต้องมี image+disassembler ที่ session
คลาวด์นี้ไม่มี) รอบนี้ค้นคอมมิตที่เพิ่ง sync เข้ามาเจอไฟล์ใหม่ `PF_GM_PLUGIN_GATE.tsv`/`.md` ซึ่งเป็นผลจาก
เครื่องมือ static-analysis ฝั่งบริดจ์เอง (17 IMAGE row + 2 DATA row, ทุกแถว `PROVEN_EXACT` พร้อม VA +
evidence span sha256) — **ตอบข้อ 3 ได้ครบโดยไม่ต้องเปิด disassembler เพิ่มเลย** และแยกกัน เจอ write-site
ของข้อ 1 ในไฟล์ rederivation script อีกไฟล์ที่มีอยู่แล้ว (ไม่เคย cross-reference กับ `RE-164` มาก่อน)

**ข้อ 3 — ปิด:** ห่วงโซ่เต็ม: `LoadLibraryW("GameMaster.dll")` → `GetProcAddress("CreateGameMaster")` →
เก็บผลที่ `application+0x7C8` (`GM-IMG-001`) → ถ้าล้มเหลว fallback object 4 ไบต์ ซึ่ง vtable slot `+0x04`
คืน `NULL` เสมอ (`GM-IMG-002/003`) → คลิกเรียก slot `+0x04` ผ่าน dispatcher ที่เช็ค empty-predicate
`0x008946C0..0x008946EA` — **จุดเดียวกับที่ RE-118 หยุดไว้พอดี** (`GM-IMG-006/007`) → ถ้าไม่ว่าง factory
ต้อง exact-match กับ key นั้นถึงจะสร้าง panel (`GM-IMG-008`) → `GMUI_BASIC` เป็นแค่ child/tab lookup
**หลัง** panel สร้างแล้ว ไม่ใช่ค่าที่ slot ต้องคืน (`GM-IMG-009/013` + `GM-DATA-001/002` ยืนยันชื่อ model
จริงคือ `GMUI_1`) รายละเอียดเต็มลงใน `CLIENT_RE_QUEUE.md` ตัวใบเองแล้ว

**ข้อ 1 — ได้ write-site แต่ยังไม่ปิดสนิท:** `[0x01032EC4]` เขียนที่ `0x0044CB7D` (`mov [0x01032EC4], esi`)
ท้าย `CMyActor` constructor — เป็น singleton ของ actor ผู้เล่นโลคัลเอง ไม่ใช่ object ผูก session/connection
โดยตรง (ยืนยันซ้ำอิสระ 2 แหล่ง: `PF_ATTR_FIELD_SEMANTICS.tsv`, `PF_COMBAT_LETHAL_TAIL_DELTA.tsv:13`)
ไม่พบ write-site ตัวที่สอง (clear/dtor ตอน logout) เลยทั้งสอง repo — คำถามเรื่อง cardinality ข้าม relog
ยังเปิดจริง ยังเป็น STATIC-ON-BRIDGE สำหรับส่วนที่เหลือ

## 🔴 ธงสำคัญที่สุดของรอบนี้ — ไม่ใช่ static fact

`PF_GM_PLUGIN_GATE.md` เองมีบรรทัด **"UNPINNED OPERATIONAL INVENTORY — NOT IMAGE/DATA EVIDENCE"**
บอกตรง ๆ ว่า ณ ตอนสร้างไฟล์ inventory ของเครื่องบริดจ์ **ไม่พบ `GameMaster.dll`** ข้างไฟล์ client — ผู้สร้าง
ไฟล์เองก็เตือนไว้ว่าอาจ stale ไม่ได้ enumerate/hash อย่างเป็นทางการ **แต่ถ้ายังจริง มันอธิบายอาการทั้งหมด
ที่ตามหากันมาตั้งแต่ `RE-104` (27 ส.ค., เกือบ 6 วันแล้ว) ได้พอดี**: ปุ่ม `BT_GM` โชว์ได้จริง (field แยกคุม
visibility) แต่คลิกแล้วไม่มีอะไรเกิดขึ้นเลย เพราะ interface ตัวจริงไม่เคยโหลดสำเร็จ — ไม่ใช่ปัญหาการผูกปุ่ม/
handler/query-gate ที่ `RE-104`/`RE-118`/`RE-126`/`RE-164`#2/#4 ไล่ตรวจไปแล้วทั้งหมด (ทุกจุดนั้นถูกต้อง
อยู่แล้ว ปัญหาอยู่*ก่อน*จุดเหล่านั้น)

**ขอให้ตรวจจริง** ว่าไฟล์ `GameMaster.dll` มีอยู่ในโฟลเดอร์ client จริงหรือไม่ (ปกติควรอยู่ข้าง exe หลัก)
`pf_bridge`/`LANE-GM` ไม่มี client image เลย ไม่มีทางยืนยันเองได้ — เป็นงานของคนที่มีเครื่อง/อิมเมจจริง
ถ้าหายไปจริงและกู้คืนไม่ได้ `PF_GM_PLUGIN_GATE.md` มีสเปกปลั๊กอินทดแทนที่เข้ากันได้ครบ (ABI ของ slot
`+0x00`/`+0x04`/`+0x08`, ต้องใช้ `MSVCR90 operator new` ไม่ใช่ UCRT/modern heap, export name ต้องตรง
`CreateGameMaster` ไม่มี decoration) — เก็บไว้เป็นทางเลือกสำรอง ไม่ใช่คำแนะนำให้ทำตอนนี้

## แก้ไฟล์

`CLIENT_RE_QUEUE.md` — อัปเดตหัวใบ `RE-164` + บล็อกข้อ 1/3 + pass-criteria + nonclaims + links (ขีดฆ่า
ข้อความเดิมที่ล้าสมัยแทนการลบ ตามกฎ)

## nonclaim

1. ไม่อ้างว่า `GameMaster.dll` หายไปจริงในสภาพแวดล้อมทดสอบปัจจุบัน — เป็นข้อสังเกตจาก inventory ที่แหล่ง
   ข้อมูลเองบอกว่าอาจ stale ไม่ใช่หลักฐาน IMAGE/DATA ต้องมีคนตรวจซ้ำ
2. ไม่อ้างว่า `GMUI_1` คือค่าที่ DLL เดิมเคยคืนจริง — เป็น `[RECONSTRUCTED POLICY — PROPOSED]` ของ artifact
   เอง ประกอบจาก DATA cross-reference ไม่ใช่ค่าที่วัดได้ตรง ๆ
3. ไม่อ้างว่า `RE-164` ปิดครบ — ข้อ 1 ยังเหลือ cardinality/clear-site ที่ต้อง static-on-bridge จริง
4. ไม่อ้างว่า panel จะเปิดจริงถ้าแก้ปัญหา DLL แล้ว — ต้องมี `GT-164` variant ใหม่ยืนยันชั้น client-observable
   ก่อน ยังไม่มีการ boot เกม/เซิร์ฟเวอร์รอบนี้เลย
5. ไม่ใช้ GM เพื่อข้ามขั้นตอนใด ๆ รอบนี้ — งาน static/เอกสารล้วน
6. ไม่ให้สถานะ GM กับบัญชีนอก `gm_accounts.json`, ไม่ประกาศ milestone
7. ไม่แตะ `runtime.py`/`app.py`/`pf_login_game_server_v141.py`/canonical DB/`scenarios/world_*.json`/
   `scenarios/combat_*.json`
8. ไม่ลบประวัติเดิมใด ๆ ใน `CLIENT_RE_QUEUE.md`

## ตอนนี้ต้องทำอะไรต่อ

- **เจ้าของ/chief**: ตรวจว่า `GameMaster.dll` มีอยู่ข้าง client exe จริงหรือไม่ (ไม่ใช่งานที่ทำจากคลาวด์ได้)
- **สาย GM**: ปิดหัวใบ `RE-164` ยังไม่ครบ (ข้อ 1 บางส่วนเหลือ) — รอ static-on-bridge สำหรับ caller-graph
  ของ `constructor_vtable_store` (`0x0044C990`) ถ้ามีคนว่างที่เครื่องบริดจ์

รายละเอียดเต็ม: `rounds/GM_20260901_2132_ku3jz6_re164-item3-closed-plus-gamemasterdll-flag.md`
PR: `pf_bridge` #756 / `pirate-force-server` #510

PF-AUTOMERGE: v4
