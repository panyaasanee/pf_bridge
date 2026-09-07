# R386 · รอบ `p8wwkv` · LANE-E (chief) — จ่าย `CORE-REQUEST-GM-064`: ประตูเดียวไปยังมิเรอร์คอนโซลตัวจริง

- เริ่ม 2026-09-07T10:52+07:00 · ล็อก `pf_bridge#1687` (list แล้วไม่มี `[LANE-E] round <id>: claim` ใบอื่นเปิดค้าง — ล็อกว่าง ไม่ใช่ takeover)
- `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 B)
- heartbeat สะพาน `2026-09-07T10:44:02+07:00` ห่างจากเวลาเริ่ม 8 นาที (ต่ำกว่า 60 = สะพานมีชีวิต) · ไม่มี `LOCK_*.txt` โผล่ใน `git status` ทั้งสองรีโป
- **ชะตา PR รอบก่อน**: `pirate-force-server#1014` (`0e19f6e`) **อยู่บน main แล้ว** ยืนยันด้วย `git merge-base --is-ancestor 0e19f6e origin/main` = จริง (merge commit `b302d55`)

## รอบนี้ขยับ NOW/M ข้อไหน
ขยับบรรทัด **LANE-GM (`0945`)** ของ `NOW.md` ตรง ๆ: "งานแรก = `CORE-REQUEST` จุดเสียบ `_Mirror` จริงให้เทส GM (chief คิว (4))"
GM ยื่นใบเวลา `10:15` รอบนี้จ่ายให้ครบ ⇒ ครึ่งของคิวผมข้อ **(4)** (ส่วน "จุดเสียบเทส GM") ปิด · ส่วน encoding/อะตอมมิกของข้อ (4) ยังไม่แตะ
**ไม่ขยับ M ข้อใดเลย** และไม่อ้างว่าขยับ — งานทั้งรอบคือประตูให้เทสของสายอื่น ไม่มีเฟรม ไม่มีจอ ผู้เล่นไม่เห็นอะไรใหม่
M2 ยังอยู่ที่ LANE-A (`0x1FB2` trigger 2/3) · M3 ที่ `GT-288` ของ LANE-B · ทั้งสองไม่ได้รอ chief

`WIRED = 0 โมดูลใหม่ที่มี emission จริงบน production path รอบนี้ / เลน production_allowed เท่าเดิม` — รอบนี้ไม่แตะ `runtime.py` ไม่แตะ `app.py` ไม่เพิ่มเลน · `runtime_console.py` เปลี่ยนแค่ **วิธีสร้าง**อ็อบเจกต์เดิม ไม่ใช่สิ่งที่ถูกสร้าง

## 1) `CORE-REQUEST-GM-064` — ให้ครบทุกข้อที่ใบขอ

ปัญหาที่ใบเปิดออกมา (ผมยอมรับตามที่เขาวัด ไม่ได้รันเอง): โทเคน GM ทุกตัวที่ผู้ปฏิบัติงานอ่าน เดินผ่านอ็อบเจกต์ที่ `RuntimeConsole` ติดตั้งเป็น `sys.stderr` ซึ่ง **ประกาศ `utf-8`** · แต่สตรีมตัวแทนในเทสของ GM encode `cp874` ซึ่ง **encode `U+0085` ไม่ได้เลย** ⇒ fold ให้ฟรี ⇒ เทสเขียวแม้ `_fold_line_breaking_controls` ถูกลบ (pf-adversary วัดบนมิวแทนต์ตัวเดียวกัน: cp874 = 0 บรรทัด · มิเรอร์จริง = 1 บรรทัดครบ)
และไม่มีทางสร้างอ็อบเจกต์นั้นได้เลยนอกจากผ่าน `RuntimeConsole.__init__` ซึ่ง `mkdir` + เปิดไฟล์ `"x"` สองใบ + เขียน `sys.stdout`/`sys.stderr` ระดับโปรเซส

ที่ลง (`src/pirateforce_foundation/runtime_console.py`):
```python
def build_console_mirror(console: TextIO, retained: TextIO) -> TextIO:
    return _Mirror(console, retained)
```
- **`RuntimeConsole.__init__` เรียกฟังก์ชันนี้** ทั้งสองบรรทัด (106-107) แทน `_Mirror(...)` ตรง ๆ — นี่คือส่วนที่กัน drift ไม่ใช่ตัวฟังก์ชัน
- **`encoding` ไม่เป็นพารามิเตอร์** ตามที่ใบขอเบี่ยงจากถ้อยคำ COO และผมเห็นด้วยกับเหตุผล: ค่าที่ `_Mirror` ประกาศต้องเป็นการตัดสินใจของโมดูล ไม่งั้นวันที่แก้ N1 เทสของ GM จะเขียวค้างอยู่กับคำตอบเก่า

เทสสามตัวใน `tests/test_runtime_console.py` (เขต chief) **ไม่มี mock บนสตรีมเลย**:
1. เขียนถึงปลายทั้งสอง · `encoding == "utf-8"` · `errors == "strict"` · หลังเรียกแล้ว tmp dir ยังว่าง และ `sys.stdout`/`sys.stderr` เป็นตัวเดิม (พิสูจน์ "ไม่เปิดไฟล์ ไม่แตะ sys")
2. `U+0085` กลางบรรทัดผ่านมิเรอร์แล้วยัง **หนึ่งบรรทัด** + assert คู่กันว่า encode `U+0085` ด้วย `cp874` โยน `UnicodeEncodeError` — เหตุผลทั้งใบของ GM เขียนเป็นเทสไว้ที่ประตู
3. สลับ `build_console_mirror` เป็นของปลอมแล้ว assert ว่า `sys.stdout`/`sys.stderr` เป็นตัวที่โรงงานคืน (พินกัน drift)

**มิวแทนต์ที่วัดแล้วว่าตาย** (ทั้งไฟล์ 8 เทส): `RuntimeConsole` กลับไปสร้าง `_Mirror(...)` ตรง ๆ ⇒ 1 failed · `_Mirror.encoding` คืน `"cp874"` ⇒ 1 failed

## 2) ชุดเต็มจับของที่ผมไม่ได้คิดถึง — re-pin ของ readiness audit (คอมมิตที่สอง)
`pytest tests/` รอบแรก **แดง 1 ใบ**: `test_pinned_impact_sets_match` `93 != 96` — `tests/test_runtime_console.py` เป็นหนึ่งใน 7 ไฟล์ pinned ของ package A ⇒ เพิ่มเทสสามตัวแล้วเลข pinned ต้องขยับในคอมมิตเดียวกัน (กฎของบล็อกนั้นเอง) · ลง re-pin พร้อมย่อหน้าเหตุผลตามขนบของไฟล์รายงาน
และเครื่องมือรายงาน **guard drift ข้อ L06**: มันพินสตริง `sys\.stdout = _Mirror` ซึ่งผมเพิ่งย้ายไปหลังโรงงาน ⇒ แก้ regex เป็น `sys\.stdout = build_console_mirror\(`
🔴 **ข้อเท็จจริงของ L06 ไม่เปลี่ยน** — `RuntimeConsole` ยังสลับ stdout/stderr ระดับโปรเซสเหมือนเดิม เปลี่ยนแค่การสะกด · วัดหลังแก้: `assumption_sites_total` = 40 เท่าเดิม · capture = 6 เท่าเดิม · `runtime_console.py` = 1 เท่าเดิม · เครื่องมือไม่รายงาน guard ใดดริฟต์อีกนอกจาก historical pin (`5cc0eda` ไม่มีบนโคลน shallow — **แดงบน main เหมือนกัน ไม่ใช่ของรอบนี้**)

## 3) คิว CORE-REQUEST — วัดทั้ง 8 ใบ ไม่ใช่ประมาณ (`CHIEF.md` §17 ข้อ 3)
`for f in notes_to_chief/*CORE-REQUEST*.md; do [ -e "$f.CONSUMED.txt" ] || echo "$f"; done` ⇒ **8 ใบค้าง** · grep จุดเสียบของแต่ละใบบน `origin/main` (`e4ae180`):
- ✅ `20260905_1352` (B, `class_id` เข้า composer ท่าโจมตี) — **ต่อสายแล้วจริง** `runtime.py:5197` `class_id=selected.class_id,` · ค้างแค่ stub ปิดรอบหน้า
- 🟡 `20260905_1650` (B, seed death register) — `mob_death_register` มีจริง (`1408`/`4730`) แต่ statement ที่ใบขอผูกกับ `#948` ที่อยู่ในคิวผมข้อ (6-11)
- ⬜ `20260905_1922` (GM-060) — ผู้อ่านมีจริงที่ `gm/chat_command_action.py:1060` · ผมยังไม่ได้อ่านใบให้จบ **จึงไม่ตัดสิน** (เขียนไว้แบบนี้ดีกว่าเดา)
- 🔴 `20260906_1029` (GM-062, inbound `0x6CEC`) — `gm/dispatch.py:615` เขียนเองว่า "Nothing calls it: there is no `runtime.py` call site for 0x6CEC" ⇒ ค้างจริง ต้องใช้ chief
- 🔴 `20260906_1215` (GM-063, ตัวนับ vital id ที่ไม่มีสาขารับ) — hook ประกาศตัวเองว่า `registered_but_not_fired = ("vital_inbound_unknown_id",)` ⇒ ค้างจริง
- 🔴 `20260906_1452` (DB, `ItemOperateVitalReq` op=5) — `runtime.py` ไม่มีสาขา op=5 (ที่ import อยู่คือ `item_operate_res_hypothesis` คนละเรื่อง)
- 🟡 `20260907_0907` (CS, ประตูคลาสของ `skill_attr`) — **ตอบแล้วรอบนี้ ดูข้อ 4**
- ✅ `20260907_1015` (GM-064) — **จ่ายรอบนี้**

ส่งใบถึง COO ขอเคาะหนึ่งเรื่อง: สามใบสีแดงอยู่ใน `runtime.py` ไฟล์เดียวกันคนละสาขา — นับเป็น "เรื่องเดียว (จุดเสียบ dispatch)" ได้ไหม ถ้าได้ผมจ่ายสามใบใน PR เดียว ถ้าไม่ได้คิวจะยาวขึ้นเพราะสายยื่นเร็วกว่าที่ผมจ่ายได้รอบละใบ · **ค่าตั้งต้นถ้า COO ไม่ตอบ = ไม่อนุญาต แล้วจ่าย GM-062 ก่อน** `[สมมติของสาย LANE-E - รอ COO ยืนยัน]`

## 4) ประตูคลาสของ CS — รับใบ ไม่ตีกลับ แต่ทำวันนี้ไม่ได้ และเหตุผลคือเงื่อนไขข้อ 3 ของใบเอง
วัดบน main: `SkillAttrHypothesisScenario` มีสี่ฟิลด์ (`scenario_id` · `hypothesis_id` · `step_order` · `spacing_seconds`) **ไม่มีคลาส** · `grep -rn "starting_skill_ids" src/` ⇒ `class_catalog.py:163` ที่เดียว
⇒ ข้อ 3 ("คลาสต้องมาจาก scenario/โมดูลที่บรรจุไอดี ไม่ใช่เลขที่พิมพ์ลง `runtime.py`") **ไม่มีค่าให้อ่าน** · ทางเลี่ยงสองทางผมปฏิเสธทั้งคู่ด้วยเหตุผลของใบเอง: พิมพ์ `1` ลง `runtime.py` = ผิดข้อ 3 · `getattr(..., None)` แล้วผ่านเงียบเมื่อไม่มี = รูเดียวกับที่ข้อ 1 สั่งห้าม
ขอกลับไปหนึ่งฟิลด์ (`character_class_id: int | None = None` บน dataclass เดิม, default `None` ⇒ ลงได้ทันทีไม่ต้องรอ `#1002` ปลดล็อก) และผม **ประกาศรูปประตูที่จะเขียนไว้ล่วงหน้าในจดหมาย** แล้ว จะได้ไม่ต้องเดินจดหมายอีกรอบเมื่อฟิลด์ลง main

## QUEUE_TRIAGE
รอบนี้ **ไม่แตะ `GAME_TEST_QUEUE.md`** และเหตุผลเป็นกติกาไม่ใช่ความขี้เกียจ: `PANYA 1910` + `NOW 0159` ย้าย **เลขใบ · เนื้อใบ · พับผล · archive · snapshot ไปเป็นของ LANE-K** · และรอบนี้ไม่ได้ผลิตสิ่งที่ผู้ดูเห็นบนจอเลย (ประตูให้เทสของสายอื่น ไม่มีเฟรม ไม่มีแฟล็กใหม่) ⇒ ไม่มีอะไรให้เทส
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ตาม `NOW.md` = `GT-288` (B) ใบแรก · ถัดไป `GT-276` (CS) · `GT-220`/`GT-223` — ทุกใบต้องมี `HEADLESS_PROOF:` · chief ไม่ได้ตั้งเลขใบ ไม่ได้ถอนใบไหนรอบนี้

## adversary
`ADVERSARY_PENDING pirate-force-server#1022` — สั่งไปต้นรอบพร้อมเริ่มงานบนกิ่ง `claude/adoring-turing-p8wwkv` ขอบเขตสองไฟล์ (`runtime_console.py` + `tests/test_runtime_console.py`)
🔴 **ห้ามอ่านว่า "ผ่าน adversary"** — ผลยังไม่คืนตอนเขียนบรรทัดนี้ · ถ้าคืนก่อนปลดล็อกผมจ่ายในรอบนี้ · ถ้าคืนหลัง = งานแรกของรอบหน้า ตาม COMMON

## รอบหน้าทำอะไร
1. **ผล `pf-adversary` ของรอบนี้** ถ้าคืนหลังปลดล็อก = งานแรก ไม่มีข้อยกเว้น
2. `20260905_1352` (B) ปิด stub — ต่อสายแล้วจริง แค่ยังไม่มีใครปิดใบ (งานกระดาษ ทำพร้อมข้ออื่นได้)
3. **GM-062 `0x6CEC`** (หรือทั้งสามใบสีแดงรวดเดียวถ้า COO อนุญาตตามข้อ 3)
4. ประตูคลาสของ CS **ทันทีที่ `character_class_id` อยู่บน main** (รูปประกาศไว้แล้วในจดหมาย ไม่ต้องถามซ้ำ)
5. หนี้เก่าที่ยังไม่จ่าย ตามลำดับ `0641`: ปิดคดี `#922` (อ่าน log ของรันที่ merge มัน) → กู้ `#997` (cherry-pick `df7c2b2` จาก `claude/eloquent-edison-3py8sa` เป็น PR ใบใหม่) → D3 preflight `[skips]` → `lane_hooks.fire()` ครอบ `BaseException` re-raise `KeyboardInterrupt`

## ชุดเต็ม
`pytest tests/` บนต้นไม้ที่ merge `origin/main` แล้ว รันครั้งเดียวต่อรอบเป็นคอมมิตสุดท้ายจริง: **13160 passed · 384 skipped · 36771 subtests passed · 0 failed** ใน 534 s = **เขียว (cloud sanity)** ไม่ใช่เกตเต็มบนสะพาน · `pf_gate_preflight.py --repo <server>` PASS (รวมด่าน `[prbody] stage=final` ของ body ใบ `#1022`)

## สถานะ PR (ตามจริง ห้ามเขียนว่าเสร็จ)
- **`pirate-force-server#1022`** (`0ec3302` · สี่ไฟล์: `runtime_console.py` · `tests/test_runtime_console.py` · `tools/pf_multiplayer_readiness_audit.py` · `reports/PF_MULTIPLAYER_READINESS_AUDIT001_*.md`): เปิดแล้ว ไม่ draft มี automerge marker ตั้งแต่เปิด — **รอ gate ยังไม่อยู่บน main** (รอบถัดไปยืนยันด้วย `git merge-base --is-ancestor <sha> origin/main`)
- `pf_bridge#1687` = claim ของรอบนี้ ปลดล็อกด้วยการเติม marker หลัง PR เซิร์ฟเวอร์เปิดครบ

SCOREBOARD: NONE | รอบนี้ผู้เล่นยังทำอะไรใหม่ไม่ได้ - งานทั้งรอบคือเปิดประตูให้ LANE-GM เทสมิเรอร์คอนโซลตัวจริงแทนสตรีมตัวแทนที่ปิดบังบั๊กของตัวเอง กับวัดคิว CORE-REQUEST ทั้งแปดใบให้ COO เห็นว่าคอขวดอยู่ตรงไหน | pirate-force-server#1022 + pf_bridge#1687
