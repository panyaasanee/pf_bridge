# R391 (`ammtv3`) — ถอนตัวตรวจ GM-063 ออกจาก main

เริ่ม 2026-09-07T18:23+07:00 · claim = `pf_bridge#1767` · กิ่ง `claude/ecstatic-cray-ammtv3` / `claude/eloquent-edison-ammtv3`
เลขรอบ: `rounds/R390_*` มีอยู่บน main แล้ว (รอบ `fr81hi`) ⇒ ใช้ **391** ตาม §4 "ชนเลขห้ามทับ +1"

## รอบนี้ขยับ NOW/M ข้อไหน
ขยับ **หนี้ที่ R390 ทิ้งไว้บน main** ไม่ใช่ข้อใหม่ใน NOW — NOW "chief ลำดับ 1-13" ข้อ (2) จ่ายไปแล้วในรอบก่อน
แต่จ่ายผิดหนึ่งในสามส่วน และส่วนที่ผิด **merge ขึ้น main ไปแล้ว** (reaper merge `#1054` เวลา `10:41:51Z`
chief ดึง marker ออกเวลา `11:13:25Z` = ช้าไป 31 นาที) · ไฟล์รอบ R390 เขียนไว้เองว่า "รอบหน้า งานแรก
ไม่มีข้อยกเว้น = ถอดตัวตรวจ GM-063" รอบนี้จ่ายข้อนั้น · **ข้อ (3) `gate-windows` 9b เลื่อนไปรอบหน้า**
(กฎ PR หนึ่งเรื่องต่อใบ — คนละเรื่องกัน)

## สิ่งที่ทำ (หนึ่งเรื่อง สามไฟล์ในรีโปเซิร์ฟเวอร์)
`pirate-force-server` กิ่ง `claude/eloquent-edison-ammtv3` คอมมิต `1b73610` + merge `origin/main`
1. `runtime.py` — ถอด **เฉพาะ GM-063**: ค่าคงที่ `_UNCLAIMED_VITAL_REASON` / `UNCLAIMED_VITAL_ONLY_EVENT`
   + ตัวนับก่อน `_dispatch_with_lanes` + บล็อก `if not actions and all(...)` ที่ยิง hook
   **เก็บ GM-062 (0x6CEC) และ seam op=5 ของ LANE-DB ไว้ทั้งคู่** — รีวิวของ `#1054` วัดแล้วว่าสะอาด
2. `lane_hooks/lane_gm_unknown_vital_counter.py` — **คืน** `registered_but_not_fired` ในคอมมิตเดียวกับที่ถอดจุดเรียก
3. `tests/test_core_request_dispatch_seams_wiring.py` — พินสามข้อของ R390 ถูก **แทนที่ ไม่ใช่ลบ**
   ด้วยคลาส `UnclaimedVitalSeamWithdrawnTests` ที่พิน "การถอน" เอง

🔴 **ไม่มี skip / xfail / allowlist ที่ไหนเลย** — พิน relation ที่ R390 ย้ายไว้
(`test_declares_never_fired_exactly_while_nothing_fires_it`) เขียว **เพราะ**คืนบรรทัดประกาศ ไม่ใช่เพราะปิดปากมัน

## ทำไมถึงถอน ไม่ใช่แก้เงื่อนไข [วัดแล้ว — โดยรีวิวของ `#1054` รอบก่อน]
ตัวตรวจอยู่จุดเดียวใน `dispatch()` ซึ่งมองเห็นแค่สองอย่าง: "การเรียกคืน actions ว่าง" กับ "ทิ้ง event อะไรไว้"
ทั้งสองอย่างไม่ตอบคำถามที่จุด hook ถาม (มีสาขาใดในโซ่ ~5,000 บรรทัดอ่าน id นี้หรือไม่)
- เรียก **65,483 จาก 65,536 id** ว่า unclaimed
- ชี้ **สิบ id ที่มีสาขารับจริง** ว่าไม่มีใครรับ
- บนเฟรม batch บันทึก **id ผิดตัว** จาก id ที่สาขาอ่าน
⇒ ปรับเงื่อนไขไม่ได้ ข้อมูลที่ต้องใช้ไม่มีอยู่ ณ จุดนั้น · และ "report-only" ที่พิมพ์ id ผิดลงคอนโซล
ที่รอบ attended ใช้ตัดสิน **ไม่ใช่ report-only**

## หลักฐานของรอบนี้เอง (สองมิวแทนต์ วัดเอง)
| มิวแทนต์ | ผล |
|---|---|
| M1 เอาตัวตรวจกลับเข้า `dispatch()` โดยคงบรรทัดประกาศไว้ | **แดง 3 พิน** (สองพินใหม่ + พิน relation) |
| M2 ถอดบรรทัดประกาศออกโดยไม่มีจุดเรียก | **แดง 3 พิน** (พินใหม่ + relation + `DeadHookPointTests`) |
ชุดที่แตะ: `27 passed, 9 subtests` · audit+GM+lane_hooks: `119 passed, 48 subtests`
`pf_gate_preflight.py --repo .` = **PREFLIGHT PASS** · ASCII ล้วนทั้งสามไฟล์ (0 บรรทัดที่มีไบต์ > 127)
ชุดเต็ม `pytest tests/` บนต้นไม้ที่ merge `origin/main` แล้ว = ดูตัวเลขใน body ของ PR (เขียว(cloud sanity) python 3.11)

## ผลลบ / nonclaims
- **ไม่อ้าง**ว่า id ที่เคยไปถึงจุดที่ถอนไม่มีสาขารับ — นั่นคือคำถามที่ยังไม่มีคำตอบ
- **ไม่อ้าง**ว่าคำถาม "ฝั่งไหนของ seam เป็นเจ้าของบันทึกว่า id นี้มีคนรับแล้ว" ถูกตอบแล้ว
  = ใบ `20260907_1816_LANE-E-ASK-COO-which-side-of-the-seam-owns-the-claimed-record.md` ยังเปิดอยู่
- `vital_walk.py` **ไม่ถูกแตะ** (`git diff origin/main -- vital_walk.py` ว่าง) ⇒ โทเคน
  `VITAL_WALK_REFUSED reason=unknown_vital_id vital_count=2` ที่ `tickets/GT-299.md` ใช้เป็น `HEADLESS_PROOF:`
  **ยังพิมพ์เหมือนเดิม** — เป็นบรรทัดของ `vital_walk` คนละตัวกับจุด hook ที่ถอน
- ไม่มีอะไรในสองรีโป import ค่าคงที่ที่ถอด (grep แล้วทั้งคู่)

## CORE-REQUEST ค้าง (ขั้นที่ 3 ของรอบ)
| ใบ | สถานะรอบนี้ |
|---|---|
| GM-062 · GM-063 · LANE-DB op=5 | จ่ายไปแล้วรอบ R390 · **รอบนี้ถอนคืนเฉพาะ GM-063** จดหมายแจ้ง GM แล้วสองใบ (`R390b`/`R390c`) + ใบรอบนี้ |
| `20260907_1641_LANE-B-CORE-REQUEST-dispatch-edge-swallows-only-half-the-death-refusals` | **เจ้าของใบถอนความเร่งด่วนเอง** (`1744` CORRECTION): เหตุผล `already_dead` ที่ใบอ้าง `_commit_death_core` สร้างไม่ได้ · เข้าคิวเป็น "defence in depth" ไม่แซง · ของจริงที่คุ้มกว่า = `fire_mob_death_hook` ใช้ `except Exception` ไม่ครอบ `BaseException` |
`WIRED = 10 / 18` [วัดแล้ว · วิธี: โมดูล `lane_hooks/lane_*.py` ที่ `production_allowed = True` เทียบกับจุด `@hook("...")`
ที่ชื่อโผล่เป็นสตริงตรงใน `src/`] · **nonclaim: วิธีนี้นับต่ำกว่าจริง** — โมดูลที่ถูกเรียกตรง ๆ ไม่ผ่านชื่อจุด
(`lane_b_mob_ai_tick` ไม่มี `@hook` เลยและถูกเรียกจาก `runtime.py:6776`) มองไม่เห็นด้วยวิธีนี้

## QUEUE_TRIAGE
`QUEUE_TRIAGE:` ไม่เพิ่ม/ไม่ถอนใบรอบนี้ · ตรวจจุดเดียวที่การถอนของรอบนี้กระทบคิวได้: ใบ READY ใบไหนพึ่งบรรทัด
`unknown_vital_id_*` ของ hook GM-063 บ้าง — **ไม่มีใบไหนพึ่ง** · `GT-299` เป็นใบเดียวที่มีสตริงนั้น และเป็นโทเคน
ของ `vital_walk` ที่ไม่ถูกแตะ (ดูผลลบข้างบน) ⇒ ไม่ต้องวัด `HEADLESS_PROOF:` ใหม่ · จดหมายแจ้ง LANE-K/LANE-GM แล้ว
`READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ:` ตาม `QUEUE_STATUS_SNAPSHOT.md` ของ K รอบ `k7q3mv` —
NOW ระบุ `GT-288` (ชุด 1+2) แล้ว `GT-276`/`GT-220`/`GT-223` · นอกนั้น `GT-279` (GM) และ `GT-299` (CS)
ยังเป็นใบของสายเจ้าของ **เลขใบ/เนื้อใบ/สแนปช็อต = LANE-K ตาม PANYA `1910`** chief ไม่แตะ

## จดหมายที่บริโภครอบนี้ (stub ครบในคอมมิตเดียวกัน)
`1641` COO-ROUND · `1641` COO-DECISION chief1600 · `1641` COO-DECISION k1618 tsv owner ·
`1641` LANE-B CORE-REQUEST · `1744` COO-ROUND · `1744` COO-DECISION ui1712 · `1744` COO-TO-CHIEF section7 addendum2 ·
`1744` LANE-B CORRECTION · `1746` LANE-DB preflight path separators

## รอบหน้าทำอะไร (เรียงแล้ว)
1. 🔴 **ยก §7 ลง `AGENTS.md` หนึ่งคอมมิต** พร้อมสามอย่างที่ COO สั่งให้ไปด้วยกัน:
   บล็อก `section7-block` ทั้งสองฉบับ (`1541` + `1744` addendum2 ข้อ ก/ข) ·
   สองบรรทัดเจ้าของ `external/PF_PROTOCOL_PRIORITY.tsv` (รูปแบบ = chief · ค่าป้าย = สายเจ้าของโปรโตคอล) ·
   และเจ้าของ `external/PF_SERIALIZER_FIELDS.tsv` + คำสั่ง "ห้ามแก้แถวให้เครื่องมือเขียว"
2. NOW ข้อ (3) `gate-windows` 9b (`1441`) → ข้อ (4) `write()` atomic ข้ามสอง sink (`1641`)
3. **ข้อเสนอของ LANE-DB (`1746`) เข้าคิวเครื่องมือ**: `pf_gate_preflight.py` ยังจับ `str(x.relative_to(y))`
   ที่ไม่ตามด้วย `.as_posix()`/`.replace` ไม่ได้ — 8 จุดในเทสของสายอื่นรออยู่ ทุกจุดแดงได้เฉพาะบนเกต = เสียหนึ่งรอบต่อจุด
4. D4 ของรีวิว `#1054`: `lane_hooks.fire()` พิมพ์ `LANE_HOOK_FIRED` ไม่มีเงื่อนไข **ก่อน**เรียก hook ⇒ เพดาน
   `MAX_UNKNOWN_IDS_PER_SESSION` อยู่ลึกไปหนึ่งชั้น · การถอน GM-063 ปิดทางที่ peer ยังไม่ล็อกอินเอื้อมถึงหรือยัง
   = คำถามที่สั่ง adversary ไว้แล้วรอบนี้ ผลอยู่ในไฟล์รอบถัดไปถ้าคืนไม่ทัน

`ADVERSARY_PENDING pirate-force-server` กิ่ง `claude/eloquent-edison-ammtv3` (สั่งต้นรอบตาม COMMON คราวนี้ ไม่ใช่ก่อน commit)

SCOREBOARD: COMING | ถอดตัวตรวจที่พิมพ์ id ผิดลงคอนโซลออกจากเซิร์ฟเวอร์ ทำให้รอบเทสในเกมเชื่อบรรทัด "เฟรมนี้ไม่มีใครรับ" ได้อีกครั้งแทนที่จะต้องข้ามมันทิ้ง | pf_bridge#1767 + pirate-force-server PR ของรอบนี้ (1b73610)
