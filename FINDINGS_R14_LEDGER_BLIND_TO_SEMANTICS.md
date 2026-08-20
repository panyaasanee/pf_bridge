# FINDINGS — idle round 14 (2026-08-17 09:23–09:36 ICT)

**คำถามของรอบ:** รอบ 13 พิสูจน์ว่า *สวีตเทส* มองไม่เห็น WIP 187 บรรทัด
รอบนี้ถามแกนที่เหลือและไม่มีใครเคยตรวจ:
**"แล้วชั้น *ธรรมาภิบาล* (hypothesis ledger + functional coverage) ล่ะ — มันเห็นไหม
และโค้ด WIP ยังอยู่ในเพดาน `accepted_ceiling` ของ HYP-PF-008 หรือเปล่า"**
(= ข้อ 6 ที่ค้างมาตั้งแต่ M14 และบล็อกการเขียนเทสให้ M3)

รอบนี้ **read-only 100% ต่อ repo** — เขียนเฉพาะใน `pf_bridge\` และ `/tmp\`
ไม่แตะ GameClient ไม่รัน server ไม่รัน client

---

## 🟢 A0 — คำตอบของ "ข้อ 6" มีอยู่แล้วในไฟล์ที่ commit ไว้ และไม่มีใครเปิดอ่านมา 14 รอบ

`docs/FUNCTIONAL_COVERAGE.json` → `domains[0] (inventory) → capabilities[2]`:

```json
{
  "id": "move_known_item_any_free_slot",
  "title": "Move any known item to any free slot 0-39",
  "required": true,
  "status": "blocked",
  "notes": "Blocked on hypothesis ledger review. The exact client request producer
            is Grade B proven and an implementation exists as uncommitted work in
            progress, but HYP-PF-008 accepted_ceiling and stop_rule permit only the
            single opt-in identity-1 slot-0 to slot-2 composition. Generalizing to
            any identity and any free slot needs a ledger decision by the project
            owner before the work may be committed."
}
```

> **นี่คือคำตอบตรง ๆ ของข้อ 6:** M3 (generic free-slot move) **เกินเพดาน HYP-PF-008**
> และไฟล์ที่ commit ไว้ระบุชัดว่า **"needs a ledger decision by the project owner
> before the work may be committed"** — คือรอ Panya อยู่แล้วโดยที่มีเอกสารรับรอง
>
> `capabilities[3] same_slot_noop` ก็ `blocked` ด้วยเหตุผลเดียวกัน
> โดเมน inventory: 10 capability — `runtime_pass` 1 / `in_progress` 4 /
> **`blocked` 2** / `not_started` 3

**ผลที่ตามมาทันที:** สิ่งที่รอบ 13 ตั้งใจไม่ทำ ("ไม่เขียนเทสให้ M3 เพราะยังไม่รู้ ceiling")
ตอนนี้มีคำตอบแล้ว — **ยังเขียนไม่ได้อยู่ดี แต่เหตุผลเปลี่ยน**: ไม่ใช่ "ไม่รู้เพดาน"
แต่เป็น **"รู้แล้วว่าเกินเพดาน และการอนุมัติเป็นสิทธิ์ของเจ้าของโปรเจกต์เท่านั้น"**

---

## FACT เกรด A — ตรวจแล้วบน Linux (python3.10) และ Windows (`py -3` 3.14.7) ตรงกันทุกตัว

### A1 — ตัวตรวจ ledger "ผ่าน" เท่ากันเป๊ะทั้งบน HEAD เพียว ๆ และบน HEAD+WIP

สร้างต้นไม้ 3 ต้นใน `/tmp/r14` (ไม่ clone ไม่สร้าง worktree — copy + `git show HEAD:`):

| ต้นไม้ | `src/` เป็นของ | `verify_hypothesis_ledger.py` | `verify_functional_coverage.py` |
|---|---|---|---|
| `tree_head` | HEAD `eef51fa` เพียว ๆ | **PASS entries=16** | **OPEN DOMAINS: 7** |
| `tree_wip` | HEAD + WIP 187 บรรทัด | **PASS entries=16** | **OPEN DOMAINS: 7** |
| `tree_ctl` (control) | WIP แต่ลบ **คอมเมนต์บรรทัดเดียว** `# PF-HYPOTHESIS-LEDGER: HYP-PF-008 active` ออกจาก `inventory.py` | **FAIL** `entries[7].source_refs[2] marker not found` | — |

ยืนยันซ้ำบน worktree จริงด้วย Windows `py -3` (job 038): `exit=0` ทั้งสองตัว

> 🎯 **ควบคุมพิสูจน์ว่าตัวตรวจ "ยังมีชีวิต"** — ลบคอมเมนต์ 1 บรรทัดที่ไม่เปลี่ยนพฤติกรรมอะไรเลย → แดงทันที
> ขณะที่การเปลี่ยนความหมายของ allowlist 30 ยกกำลัง → **เขียวเท่าเดิม**

### A2 — ปริมาณของสิ่งที่ตัวตรวจมองไม่เห็น: 3 → 2.7 × 10³⁰ สถานะ

`require_known_backpack()` เดิม (HEAD) เทียบ **ทั้ง BackpackState** กับ allowlist 3 ค่า
WIP เปลี่ยนเป็นเทียบเฉพาะ **content signature** = `(identity, template_id, quantity,
raw_u8_38, raw_u8_39, detail_present)` — **`slot` ถูกตัดออกจากลายเซ็นโดยตั้งใจ**
และ **`base_mask` / `base_identity` / `range_mask` ไม่ถูกเทียบอีกเลย**

differential รันจริงบนโมดูลทั้งสองเวอร์ชัน (ผลตรงกันทั้ง Linux และ Windows):

| สถานะที่ป้อน | HEAD | WIP |
|---|---|---|
| merged แต่ย้าย slot เป็น `[37,38,39]` | ❌ reject | ✅ **accept** |
| merged แต่ `base_mask = 0x00` | ❌ reject | ✅ **accept** |
| merged แต่ `base_identity = 999999` | ❌ reject | ✅ **accept** |
| merged แต่ `range_mask = 0x7F` | ❌ reject | ✅ **accept** |
| HYPOTHESIZED slot2 (ตัวที่ ledger รับรอง) — *control* | ✅ | ✅ |
| merged ไม่แก้ — *control* | ✅ | ✅ |
| initial ไม่แก้ — *control* | ✅ | ✅ |

นับจำนวนสถานะที่ผ่าน:

```
initial n=4 items → P(40,4) = 2,193,360 การจัดสล็อต
merged  n=3 items → P(40,3) =    59,280 การจัดสล็อต
header ที่หลุดการตรึง = 256 (base_mask) × 2^64 (base_identity) × 256 (range_mask)
                     = 1,208,925,819,614,629,174,706,176

HEAD ยอมรับ =                    3 สถานะ
WIP  ยอมรับ ≈ 2.723 × 10^30 สถานะ
```

### A3 — 🔴 การหลุดตรึงของ 3 ฟิลด์ header **ไม่อยู่ในเจตนาที่ใครเขียนไว้ที่ไหนเลย**

`docs/AI_TRANSFER_HANDOFF_20260817.md` §7.1 ลิสต์เจตนาของ WIP ไว้ 6 ข้อ
ข้อที่เกี่ยวคือ *"govern exact initial or merged item **contents** while allowing
unique **slots 0–39**"* — **พูดถึงแค่ item contents กับ slot**
ส่วน note ใน `FUNCTIONAL_COVERAGE.json` ก็พูดถึงแค่ *"any identity and any free slot"*

→ **`base_mask` / `base_identity` / `range_mask` ที่หลุดออกไป เป็นผลข้างเคียงที่ไม่มีใครตั้งใจ
และไม่มีเอกสารไหนบันทึก** เกิดจากการเปลี่ยนวิธีเทียบจาก "ทั้งสถานะ" เป็น "ลายเซ็นเฉพาะ items"
— **นี่คือของใหม่ที่รอบนี้เจอ ไม่ใช่ของที่รู้อยู่แล้ว**

### A4 — ช่องนี้ **ไปถึงได้จริงผ่านดิสก์** ไม่ใช่แค่ทฤษฎี

`store.py:_load_backpack()` อ่าน header **จากตาราง** ตรง ๆ:

```sql
SELECT base_mask, base_identity, range_mask FROM character_backpacks WHERE character_id=?
```

แล้วส่งเข้า `require_known_backpack(state)` → ถ้าใครแก้ 3 คอลัมน์นั้นใน DB
HEAD จะโยน `ValueError` แต่ WIP **จะรับและเดินต่อ**

### A5 — `make_item_move_delta_response` (48 บรรทัด) เป็น **โค้ดตายสนิท**

`git grep` + grep ทั้ง worktree: ชื่อนี้ปรากฏ **ที่เดียวคือบรรทัดที่นิยามมันเอง**
(`inventory.py:168`) — ไม่มี import ไม่มี call จาก `src/` `tests/` `scenarios/` `tools/`
→ **48 จาก 187 บรรทัด (26%) ของ WIP ไม่มีทางถูกเรียกในสภาพปัจจุบัน**
สอดคล้องกับ coverage 0/42 ของ `store.py` ที่รอบ 13 วัดได้ แต่คนละสาเหตุ:
รอบ 13 = "ไม่มีเทสเรียก" · รอบนี้ = "ไม่มี **โค้ด** เรียก"

### A6 — 🟢 migrations ไม่ drift เลย (negative เกรด A — ไม่มีใครเคยตรวจ)

- สร้าง DB ใหม่จาก `migrations/001–003` ด้วย `SQLiteStore.migrate()` ตัวจริง
  → เทียบ `sqlite_master` กับ canonical: **16 object เท่ากัน, ชื่อตรงหมด,
  ข้อความ SQL ตรงหมด, ไม่มีอันไหนเกินหรือขาด**
- `schema_migrations` ใน canonical เก็บ sha256 ของไฟล์ migration ไว้ ตรวจแล้ว
  **MATCH ครบ 3/3** กับไฟล์บนดิสก์วันนี้ (ยืนยันบน Windows ด้วย)
  → ไม่มีใครแก้ไฟล์ migration หลัง apply · `migrate()` จะไม่โยน checksum mismatch

### A7 — 🟢 รายงานที่อ้าง WIP ไม่ได้โกหก

`reports/PF_DEMO_FULLLOOP001_..._RUNTIME_PASS_20260817.md` (tracked) อ้าง
`inventory.is_unmoved_baseline()` ซึ่งมีเฉพาะใน WIP — แต่รายงานเขียนกำกับไว้ตรง ๆ ว่า
*"The **uncommitted** M3 work-in-progress guard..."* และ *"That guard originates in
inherited work-in-progress"* → **ซื่อสัตย์ ไม่ใช่ claim ปลอม**
(ข้อจำกัดที่ตามมา: ย่อหน้า root-cause นั้น **ทำซ้ำบน HEAD เพียว ๆ ไม่ได้** ต่อยอดจากรอบ 12/13 โดยตรง)

---

## INFERENCE เกรด B

- **B1 — เพดานยังมีที่ว่าง แต่ประตูล็อกอยู่**
  `HYP-PF-008.max_versions = 3`, `expiry.tracked_versions = ["ITEM-MOVE-HYP-001"]`
  → ใช้ไป **1 จาก 3** ยังมีที่ให้ `ITEM-MOVE-HYP-002` โดย **ไม่ต้องเปิด hypothesis ใหม่**
  และ **ไม่ต้องใช้ `extension_approval_ref`** (ตัวนั้นไว้ใช้ตอนจะเกิน 3)
  แต่ `stop_rule` เขียนว่า *"Do not add another destination ... or second dependent
  version **without new evidence and ledger review**"* → ต้องมีทั้ง **หลักฐานใหม่** และ **การรีวิว**
  `AI_TRANSFER_HANDOFF §7.1` ก็วางแผนไว้แล้วว่าจะขึ้นเป็น `ITEM-MOVE-HYP-002`
  ยังเป็น HYP-PF-008 และ `production_allowed=false`

- **B2 — "หลักฐานใหม่" ที่ ledger เรียกหา ต้องมาจากคิวเทส ไม่ใช่จากงาน static**
  `HYP-PF-008.evidence_gap` ระบุว่าไม่มี original-server response ผูก quantity 2 /
  slot 2 / durable persistence และ **ไม่มี original server ให้ capture แล้ว**
  → ทางเดียวที่เหลือคือหลักฐานฝั่ง **client acceptance** = ต้องเปิด GameClient
  = **งานของ `pirate-force-game-tester`** และ **`GT-002` คือรายการเดียวในคิวที่แตะ code path นี้**
  → **คิวเทสไม่ใช่งานข้าง ๆ แต่เป็น critical path ของ M3 ทั้งก้อน**

- **B3 — ตัวตรวจตรวจ "ข้อความ" ไม่ได้ตรวจ "ความประพฤติ"**
  `verify_hypothesis_ledger.py` เดินตาม `source_refs[].required_markers` แล้วเช็ค
  substring ในไฟล์ (+ กฎ 1 annotation ต่อ (ไฟล์, id)) — ไม่มีที่ไหนเทียบพฤติกรรมกับ
  `accepted_ceiling` / `stop_rule` ซึ่งเป็น **ข้อความภาษาอังกฤษล้วน อ่านโดยมนุษย์เท่านั้น**
  marker ทั้ง 3 ของ `inventory.py` (`HYP-PF-008 active`, `HYPOTHESIZED_V111_SLOT2_BACKPACK`,
  `ItemAttrState(1, 2600001, 2, 2)`) **ยังอยู่ครบใน WIP** จึงเขียว

---

## 🔴 NONCLAIMS — สิ่งที่รอบนี้ **ไม่ได้** พิสูจน์

1. **ไม่ได้บอกว่าโค้ด WIP ผิดหรือมีบั๊ก** — วัด *ขอบเขตที่โค้ดยอมรับ* เทียบกับ *ขอบเขตที่ ledger อนุญาต*
   ไม่ได้วัดว่าการย้ายไอเทมทำงานถูกต้องหรือไม่ (ยังไม่มีใครรันมันเลยสักครั้ง)
2. **ไม่ใช่ข้อสรุปด้านความปลอดภัย** — A4 ต้องมีสิทธิ์เขียนไฟล์ DB บนเครื่องอยู่แล้ว
   listener ผูก `127.0.0.1` และ `production_allowed=false` ทุกที่
   คนที่แก้ DB ได้ ก็แก้อย่างอื่นได้อยู่แล้ว → เป็นเรื่อง **การกร่อนของ invariant** ไม่ใช่ attack surface
3. **ไม่ได้รัน `verify_foundation.ps1` เต็มตัว** — รันเฉพาะ verifier 2 ตัวที่เกี่ยวข้อง
4. **ไม่ได้เทียบ 3 ต้นไม้ด้วยสวีตเทสซ้ำ** — รอบ 13 ทำไปแล้ว (`337/337 errors=14` เท่ากัน)
5. **`slot` เพดาน 39 มีหลักฐานรองรับ** (`PF_RE_V116_to_V120...md`: *"bit 0 for the base
   40-slot range; bit 1 for an additional 40-slot range"*) — แต่ WIP hardcode 39 **โดยไม่ดู
   `base_mask` bit 1** → ถ้าวันหนึ่งเจอกระเป๋าขยาย โค้ดจะ **reject แบบ fail-closed**
   นี่เป็นการหดตัวที่ปลอดภัยวันนี้ แต่เป็น **หนี้ที่ต้องจดไว้** ไม่ใช่ข้อสรุปว่าผิด
6. **ไม่ได้แตะ ledger, ไม่ได้แตะ coverage matrix, ไม่ได้แก้โค้ด, ไม่ได้ commit**
7. `same_slot_noop` / `occupied_destination_policy` — อ่านสถานะจากไฟล์เท่านั้น ไม่ได้ทดสอบพฤติกรรม

---

## 🟡 ตัวเลือกสำหรับ Panya — **ข้อ 6 (ปิดได้แล้ว) + ข้อ 9 (ใหม่)**

### ข้อ 6 — สรุปให้เคาะ: จะอนุมัติ `ITEM-MOVE-HYP-002` ไหม

| | ทางเลือก | ผล |
|---|---|---|
| **ก** | อนุมัติ `ITEM-MOVE-HYP-002` ใต้ HYP-PF-008 (2/3) ทันที โดยยังไม่มีหลักฐาน client | เร็วที่สุด แต่ขัด `stop_rule` ที่บังคับ *"new evidence **and** ledger review"* — จะได้ capability ที่ไม่มีหลักฐานรอง |
| **ข** | อนุมัติแบบมีเงื่อนไข: เขียน entry ไว้ล่วงหน้าเป็น `pending_evidence` แล้ว **เปิดใช้เมื่อ GT-002 คืนผล PASS** | ตรงกับ `policy.approval_schema` (ต้องระบุ `approval_id`, `approved_entry_ids`, `approved_through`) และไม่สร้าง claim ลอย ← **chief เอนไปทางนี้** |
| **ค** | ไม่อนุมัติ ให้ย่อ WIP ลงมาเท่าเพดานเดิม (คืน allowlist 3 สถานะ) | ปลอดภัยสุด แต่ทิ้งงาน 187 บรรทัดครึ่งหนึ่ง และ coverage `move_known_item_any_free_slot` ค้าง `blocked` ต่อไป |
| **ง** | พักไว้ ไปทำโดเมนอื่นที่ไม่ blocked ก่อน | ไม่เสียของ แต่ inventory เป็นโดเมนที่ `required: true` ทั้ง 10 ข้อ |

### ข้อ 9 (ใหม่) — 3 ฟิลด์ header ที่หลุดตรึงโดยไม่ตั้งใจ (A3)

ไม่ว่าจะเลือกทางไหนในข้อ 6 การหลุดตรึงนี้ **ไม่มีใครขอ** และแก้ได้ด้วย 3 บรรทัด
patch ที่เสนอ (ยังไม่ได้ใส่ — รอคำสั่ง) ใน `inventory.py::require_known_backpack`:

```python
    _require_int(value.base_mask, "backpack base mask", 0, 0xFF)
    _require_int(value.base_identity, "backpack base identity", 0, 0xFFFFFFFFFFFFFFFF)
    _require_int(value.range_mask, "backpack range mask", 0, 0xFF)
+   if (value.base_mask, value.base_identity, value.range_mask) != (
+       BACKPACK_BASE_MASK, BACKPACK_BASE_IDENTITY, INITIAL_BACKPACK.range_mask,
+   ):
+       raise ValueError("backpack header is outside the governed V111 allowlist")
```

ผล: ตัดสถานะที่ยอมรับจาก **2.7 × 10³⁰ เหลือ 2,252,640** (= P(40,4)+P(40,3))
โดยไม่กระทบเจตนาที่เอกสารเขียนไว้เลยสักข้อ

### ข้อ 10 (ใหม่) — จะให้ verifier ตรวจความหมายได้ไหม

ปัจจุบัน `accepted_ceiling` / `stop_rule` เป็นภาษาอังกฤษล้วน → เครื่องอ่านไม่ได้
ถ้าอยากปิดช่อง A1 อย่างถาวร ต้องเพิ่มฟิลด์เชิงกลไกใน ledger เช่น
`bounded_state_count` หรือ `conformance_test_ref` แล้วให้ verifier บังคับ
— **เป็นการเปลี่ยนสคีมาของ ledger = ตัดสินใจเชิงขอบเขต จึงยังไม่ทำ**

---

## ⭐ บทเรียนของรอบ 14

รอบ 12: *"repo ที่ commit ครบทุกไฟล์โค้ด ยังไม่ใช่ repo ที่รันได้"*
รอบ 13: *"gate ที่รันได้และเขียว ยังไม่ใช่ gate ที่เห็นงานของคุณ"*
**รอบ 14: "gate ที่เห็นงานของคุณ ก็ยังไม่ใช่ gate ที่เข้าใจว่างานนั้นทำอะไร"**

— ตัวตรวจธรรมาภิบาลทั้งสองตัวนับ **ข้อความที่ต้องมี** ครบถ้วนแม่นยำ
แล้วรายงานเขียว ในขณะที่ขอบเขตที่ระบบยอมรับจริงขยายจาก **3 เป็น 2.7 × 10³⁰**
คอมเมนต์ที่ลบทิ้ง 1 บรรทัดทำให้แดง แต่การกร่อน invariant 30 ยกกำลังไม่ทำให้ขยับเลย

และบทเรียนที่แสบกว่า: **คำถามที่บล็อกงานมา 8 รอบ (ข้อ 6) มีคำตอบเขียนไว้แล้ว
ในไฟล์ที่ commit อยู่ ผ่าน gate ทุกวัน และไม่มีใครเปิดอ่าน**
— ของที่ "ตรวจผ่าน" กับของที่ "มีคนอ่าน" เป็นคนละเซ็ตกัน
