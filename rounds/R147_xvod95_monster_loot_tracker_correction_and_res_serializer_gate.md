# R147 — แก้ tracker `monster_spawn_and_loot` ให้ตรงความจริง + ชี้ gate จริงของเลนลูท (ผ่าน pf-adversary)

- **รอบ:** R147 · session `xvod95` (branch `claude/exciting-goldberg-xvod95` / server `claude/amazing-goodall-xvod95`)
- **เวลา:** 2026-08-24 ~13:0x (+07:00)
- **ล็อก:** draft PR #48 (pf_bridge) · marker `PF-AUTOMERGE: v4`
- **เลนที่แตะ:** เอกสาร/ประสานงาน (pf_bridge) + tracker หนึ่งไฟล์ (pirate-force-server `docs/FUNCTIONAL_COVERAGE.json`) · **ไม่แตะคิว RE** (เลนลูทเปิดค้างอยู่แล้ว)

## ที่มาของรอบ

จดหมายเข้ากล่อง 4 ใบ (11:19 / 11:47 / 12:00 / 12:44) ของผู้ช่วย cloud · ใบล่าสุด 12:44
เสนอว่า `monster_spawn_and_loot` **พร้อมทำเป็นเลนโค้ดแล้ว** เพราะ "ชิ้นส่วนครบทุกชิ้น"
(loot roll · GT-046 pickup outbound · GT-049 บรรทัดเขียว "ได้รับ" id 131) และถ้าปิดได้จะเป็น
capability `complete` ตัวแรกของโปรเจกต์ (ตอนนี้ 0/57)

รอบนี้ตรวจข้อเสนอกับ **artifact ที่ commit แล้ว** แล้วส่ง `pf-adversary` หักล้างข้อสรุปของตัวเองก่อน commit
**ผล adversary พลิกข้อสรุปฉบับร่างของ chief สามจุด** (ดีแล้ว — นั่นคือหน้าที่มัน) บันทึกไว้ตามจริง

## สิ่งที่ adversary จับได้ (ทั้งหมด verify กับซอร์สที่ commit แล้ว)

### D1 — ร่างแรกผิด: "ไม่มี src ไฟล์ไหน emit `ItemOperateVitalRes`"
**ผิด** — encoder แบบไบต์เป๊ะที่ client ยอมรับแล้ว **มีอยู่และ ship แล้ว**:
- `current/pf_login_game_server_v141.py:427` — `ITEM_OPERATE_RES_VITAL = 0x4C13` ·
  `:5156` assert `protocol_name_id("ItemOperateVitalRes") == 0x4C13` ⇒ **vital นี้คือ ItemOperateVitalRes**
- `src/pirateforce_foundation/inventory.py:266-428` — สาม serializer โปรดักชัน
  `make_item_move_delta_response` / `make_item_swap_delta_response` / `make_item_merge_delta_response`
  emit `ITEM_OPERATE_RES_VITAL` · **pin ไบต์กับ V141 golden ที่ client จริงยอมรับ runtime แล้ว**
  (`:309-312`, `:417-427` โยน RuntimeError ถ้า drift จาก golden)
- wired เข้า dispatch จริง: `src/pirateforce_foundation/runtime.py:888/947/1009`

⇒ โปรเจกต์ **เลี่ยงความมัวของ static layout ด้วยการ pin golden เชิงประจักษ์** ไม่ได้ re-derive layout
⇒ เหตุผล "layout UNKNOWN ⇒ encoder ทำไม่ได้" ของร่างแรก **ตกทั้งท่อน**

> (เหตุที่ grep แรกพลาด: โค้ดใช้ค่าคงที่ `ITEM_OPERATE_RES_VITAL`/`0x4C13` ไม่ใช่สตริงชื่อคลาส)
> ยืนยันความมัวของ static เป็นจริงตามที่ร่างว่า: `pf_bridge/external/PF_SERIALIZER_FIELDS.tsv` แถว 769-794
> W ~13 field ส่วนใหญ่ UNKNOWN (CALL_UNCLASSIFIED · MSVCR90 `_invalid_parameter_noinfo` · INTERLOCKED ·
> W6/W8 ถูก PHI guard) · `PF_FIELD_VALIDATION.tsv:92` `W = 0/0 NOT_OBSERVED` — **แต่ static murk ไม่ใช่ตัวขวาง
> เพราะเราไม่ได้ยืนบน static เรายืนบน golden**

### D2 — gate จริงไม่ใช่ "ถอด serializer layout" แต่คือ "field ไหนจุดบรรทัดเขียว"
layout ถูกแก้ไปแล้วเชิงประจักษ์ (golden) ⇒ ใบ RE ที่สั่ง "ถอด layout" = สั่งไปทำของที่ทำแล้ว และ **พลาดคำถามจริง**:
**0x4C13 body แบบ "acquire/merge (ได้ของใหม่/เพิ่มจำนวน)" จุดสาย id-131 บรรทัดเขียว
`ได้รับ [x] * n` (สาย `0x005EF5E0→0x005A8A00→0x005A5790/0x005A5DB0→0x005CC2B0→0x005CC309` ตาม GT-049)
หรือแค่ apply bag delta เงียบ ๆ แบบ move/swap/merge ที่ ship อยู่?** และ **field ไหนแยก acquire ออกจาก move**
(candidate = W6/W8 ที่ยัง UNKNOWN/PHI-guarded)

### D3 — ตัวขวางจริงอยู่ก่อนหน้า encoder: **การส่งของถึงผู้เล่น (Door 3/4) ยังไม่มีเส้น**
- **Door 3 (ของโผล่บนพื้นให้ client เห็น)** = สมมติฐานล้วน · `ground_loot_hypothesis.py:1-14` เขียนเอง
  ว่า "ไม่เคยมี client เห็น frame bit-0x08 · client จะ render หรือไม่ = คำถาม attended GT-045"
  · GT-045 = **WIRE PASS / CLIENT NO-RESULT** และ **พักรอ Panya 2026-08-26**
- **Door 4 (คำขอเก็บของที่มอนดรอป)** = ยังไม่รู้เส้น · 🔴 **ห้ามสมมติว่า == `PickupTerrainThing`/GT-046** (ดู D4)

### D4 — GT-046 ถูกอ้างผิดระบบ
`notes_to_chief/20260823_1335_AMENDMENT-...-GT046-scope-warning.md` เตือนไว้ชัด: มีระบบเก็บของ **≥2 ระบบ** ·
`PickupTerrainThing` **น่าจะเป็นระบบ (ก) ของวางล่วงหน้า (ของเควส เช่น `Sky Lantern`) ไม่ใช่ของมอนดรอป** ·
nonclaim บังคับ: "ห้ามเอาผลของระบบหนึ่งไปอธิบายอีกระบบจนกว่าจ็อบ 1-2 จะพิสูจน์ว่าเป็นระบบเดียวกัน"
⇒ **ห้ามใส่ GT-046 เป็น evidence ของ `monster_spawn_and_loot`**

## สภาพจริงต่อประตู (โมเดล 6 ประตูจาก R100 design draft)

| Door | สถานะจริง (จาก artifact ที่ commit) |
|---|---|
| 2 — WHAT IT DROPS (roll) | ✅ `loot_roll.py` LOOT-ROLL-001 · แต่เป็น **ไลบรารีที่ไม่มีใครเรียก** (`production_allowed=false`) |
| 3 — GROUND OBJECT RENDER | 🟡 hypothesis (GROUND-LOOT-001) · GT-045 WIRE PASS / CLIENT NO-RESULT · **พักรอ Panya 08-26** |
| 4 — PICKUP TRANSPORT (มอนดรอป) | 🔴 ยังไม่รู้เส้น · GT-046 เป็นคนละระบบ (ของวางล่วงหน้า) — ห้ามอ้างข้ามระบบ |
| 4b/5 — RESPONSE + BAG DELTA | ✅ encoder `0x4C13` มีจริง client ยอมรับแล้ว (`inventory.py`, golden-pinned) · **แต่ยังไม่รู้ว่า body แบบ acquire จุดบรรทัดเขียวไหม (gate จริง — RE-059)** |
| 6 — ITEM PERSISTS | schema พร้อม · **ไม่มี path insert item row ใหม่หลัง character creation** (FINDINGS_R21 A1) · dispatch ไม่ guard = DB exception หลุด server ตาย (N1) |

## 🔴 กัน duplicate: เลน RE ของลูท **เปิดค้างอยู่แล้ว** — รอบนี้ไม่เปิดใบใหม่

ตรวจ `CLIENT_RE_QUEUE.md` แล้ว: gate จริง (D2) + คำถาม delivery **ถูกเปิดเป็นใบ PENDING อยู่แล้วตั้งแต่ R145/R146**:
- **RE-059 ITEMOPERATE-RES-CAPTURE-BYTES-001** [⏳ PENDING] — ดึงไบต์จริงของ 5 เฟรม `ItemOperateVitalRes:R`
  ใน capture (`parse_success=0` แต่ `mismatch_frames=0` = "ถอดไม่ได้" ไม่ใช่ "ขัดกัน") → `bag_present_flag` ·
  `affected_identity_count` · รูป ItemBagAttr **นี่คือทางเชิงประจักษ์ที่ตอบ "body แบบ acquire หน้าตาอย่างไร"**
- **RE-060 ITEM-TEMPLATE-CODE-SCHEMA-001** [⏳ PENDING] — pin สคีมรหัสไอเทม
- 📌 R145 บันทึกไว้แล้วเองว่า encoder `0x4C13` มีใน `inventory.py` 3 ทรง ⇒ **ไม่เปิดเลนโค้ดใหม่**

⇒ 12:44 เสนอ "เลนโค้ดพร้อม" เพราะ **ไม่ได้เปิด `CLIENT_RE_QUEUE.md`** (กฎ AGENTS.md ใหม่ "เปิด tracker ก่อน" แก้อาการนี้ตรง ๆ)
⇒ รอบนี้ **ไม่เพิ่มใบคิว** (จะซ้ำ RE-059) · attended delivery (GT-045) ก็เปิดค้าง+พักอยู่แล้ว

## สิ่งที่รอบนี้ทำ (ชิ้นที่ไม่ซ้ำใคร)

1. **แก้ `docs/FUNCTIONAL_COVERAGE.json`** — `monster_spawn_and_loot`: `not_started` → `in_progress`
   (งานเริ่มจริงแล้ว ⇒ `not_started` ล้าสมัย · R145 เปิดใบ RE แต่ **ไม่ได้อัปเดต tracker** — นี่คือชิ้นที่ขาด) ·
   `evidence_refs` = artifact ที่ **bear จริง** (Door 2/3/5 + design · **ไม่ใส่ GT-046**) ·
   `notes` เล่าสภาพ 6 ประตู + gate จริง (D2) + ชี้ RE-059/060 + ตัวขวาง delivery (D3/D4)
2. **เอกสารรอบนี้** (ไฟล์เดียว ของรอบนี้)

## คำถามเปิดถึง Panya (การตัดสินสถาปัตยกรรม — chief ไม่ตัดสินแทน)

R100 สั่งลำดับ: (1) roller เสร็จ → (2) ถอดตัวขวาง delivery → (3) scaffold direct-grant **ท้ายสุด + ติดป้าย non-canonical**
ตอนนี้ Door 5 encoder มีแล้ว ⇒ **direct-to-backpack grant เป็นไปได้ทางเทคนิค** แต่:
- ขัดหลักการ #5 (เหมือนจริง = ของต้องวางบนพื้นแล้วเดินเก็บ) ⇒ R100 บอกให้ทำเป็น scaffold ติดป้าย เท่านั้น
- Door 3 (GT-045) ยังไม่ตัดสินว่า canonical ground path ใช้ได้ไหม · พักรอ Panya 08-26
- **คำถาม:** จะสร้าง scaffold direct-grant (มี grant-writer Door 6 แบบ guarded + opt-in) **ตอนนี้**
  หรือรอ GT-045 ตัดสินสถาปัตยกรรมก่อน? — chief แนะ **รอ RE-059 + GT-045 ก่อน** เพื่อเลี่ยง "ง่ายวันนี้ รื้อทีหลัง" (หลักการ #4)

## nonclaims

- encoder `0x4C13` **มีจริงและ client ยอมรับ** — แต่ **ยังไม่มีใครเอา body แบบ acquire ไปวางหน้า client จริง**
  ⇒ ยังไม่รู้ว่ามันจุดบรรทัดเขียวหรือ apply เงียบ (RE-059 + attended ในอนาคตเป็นตัวตอบ)
- `in_progress` = งานเริ่มแล้ว ไม่ใช่ใกล้ `complete` · Door 3/4 ยังไม่มีเส้น delivery ที่พิสูจน์แล้ว
- ไม่แตะ loot_roll.py / inventory.py / ground_loot_hypothesis.py / v141 / DB · ไม่ลบ/ย้ายใบคิวที่ยังไม่เทส
- ไม่ claim อะไรเกี่ยวกับเซิร์ฟเวอร์ต้นฉบับ ซึ่งปิดไปแล้ว กู้ไม่ได้ตลอดกาล
