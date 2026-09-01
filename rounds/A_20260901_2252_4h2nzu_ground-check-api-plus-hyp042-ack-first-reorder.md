# LANE-A (WORLD) round `4h2nzu` -- 2026-09-01T22:52+07:00

## 0. NOW.md

อ่านก่อนเสมอ. สถานะ "มีงานด่วน 3 ข้อ" (P-1 ของดรอป, P-2 สีชื่อมอนสเตอร์, P-3 ปุ่ม GM) แต่ไม่มีข้อ
ไหนระบุ LANE-A โดยตรง -- GM-A ("สาย A/GM เดินคิวปกติต่อได้") ยืนยันชัดว่าไม่บล็อกสายนี้ จึงเดินคิว
ปกติต่อตาม addendum v2 (mailbox first)

## 1. Section A -- ชะตา PR รอบก่อนของสายนี้

- `pf_bridge` #757 ("[LANE-A] round 2134: GT-194 pre-written...") -- `merged_at` มีค่าจริง (field
  `merged` ในผล tool คืน `false` แต่ `merged_at`/`closed_at` ตรงกันและ diff อยู่บน `main` แล้ว --
  ยึด `merged_at` เป็นหลักฐาน ไม่ใช่ boolean `merged`) => งานอยู่บน `main` แล้ว ไปต่อ
- `pirate-force-server` #505 ("[LANE-A] structural LogoutVital request classifier...") --
  `merged: true` ตรงไปตรงมา => งานอยู่บน `main` แล้ว ไปต่อ

ไม่ต้อง cherry-pick อะไร

## 2. Section B -- กล่องจดหมาย (ขั้นที่สอง)

`grep -l "ADDRESSEE: LANE-A"` แล้วกรองไฟล์ที่ไม่มี `.CONSUMED.txt` sibling เจอ 3 ใบ:

1. `20260901_1928_CHIEF-REPLY-re189-branch3-wired-hyp041-registered.md` -- chief ต่อสาย routing
   branch 3 (`ack_first_reorder`) ใน `runtime.py` แล้ว, ลงทะเบียน `HYP-PF-041` แล้ว, ส่งต่อให้สายนี้
   ทำ allowlist profile + scenario file + hypothesis_id
2. `20260901_2028_LANE-GM-TO-LANE-A-warp-coordinate-bound-needs-a-public-ground-check.md` -- ขอ
   public function `is_position_within_scene_ground()` (ไม่เร่ง, เสนอไว้)
3. `20260901_2152_COO-DECISION-hyp-pf-040-path1-confirmed.md` -- ยืนยันทางที่ 1 ของ HYP-PF-040 ให้
   สายนี้ (ไม่เร่ง, ตอบ CORE-REQUEST เดิมของสายนี้เอง)

ทั้งสามบริโภคแล้วรอบนี้ (อ่าน + ลงมือ/ตอบ + วาง `.CONSUMED.txt` + สำเนาเข้า `consumed/`) --
ข้อ 3 ไม่มีโค้ดต่อ (เป็นการยืนยันล่วงหน้า) ข้อ 1 กับ 2 มีโค้ดจริงตามหัวข้อ 3 ด้านล่าง

**แก้ไขสมมติสำคัญ**: ใบ 1928 ชวนให้เข้าใจว่าใช้ `HYP-PF-041` สำหรับ `ack_first_reorder` แต่ตรวจโค้ด
แล้วพบว่า `HYP-PF-041` ผูกกับ RE-189 branch 2 (teardown timer sweep) ไปแล้วเต็มรูปแบบ -- เปิด
`HYP-PF-042` แทน รายละเอียดเต็มใน `LANE-A-CORE-REQUEST-026`

## 3. งานที่ทำ (pirate-force-server, PR `#514` [เสนอ])

### 3a. `is_position_within_scene_ground()` (บริโภคใบ 2028)

`src/pirateforce_foundation/world_scene_entry.py`: รีแฟกเตอร์ `_within_ground()`'s logic เป็น helper
กลาง `_ground_evidence(target, x, y) -> bool | None` (`None`=ไม่มี ground evidence เลย,
`False`=มี evidence แต่ disqualify/นอกพื้น, `True`=ในพื้น) `_within_ground` เปลี่ยนเป็น delegate
(`_ground_evidence(...) is True`) รักษาพฤติกรรมเดิมของ `resolve_entry` เป๊ะ (ยืนยันด้วย adversary
ในหัวข้อ 5) เพิ่มฟังก์ชันสาธารณะ:

```python
def is_position_within_scene_ground(scene_id: int, x: float, y: float, *, registry=None) -> bool | None
```

รักษากติกา `PROVISIONAL-OWNER-DECREE`-ไม่นับ-evidence เป๊ะ -- scene 17 (decree + ground block จริง
พร้อมกัน) คืน `False` ทั้งจุด spawn และจุดนอก block ไม่มีทางคืน `True` จาก decree เพียงอย่างเดียว

`tests/test_world_scene_entry.py` -- เพิ่มคลาส `PublicGroundCheckTests` (9 เทส) รวม 71 passed,
38 subtests (62 เดิม + 9 ใหม่)

### 3b. `HYP-PF-042` ack_first_reorder profile (บริโภคใบ 1928)

`src/pirateforce_foundation/logout_hypothesis.py` -- profile ที่เจ็ด `_PROFILE_ACK_FIRST_REORDER` /
`_EXPECTED_ACK_FIRST_REORDER` ผูก chief's routing branch (`runtime.py`, ไม่แตะรอบนี้) เข้า allowlist
`require_logout_hypothesis_scenario` เป็น entry ใหม่ (เพิ่มเท่านั้น, 6 profile เดิมไม่เปลี่ยน)

`scenarios/logout_hypothesis_ack_first_reorder.json` -- ใหม่, `production_allowed: false`,
`test_only: true`, ใช้ byte pin เดิมของ `HYP-PF-012`/`HYP-PF-028` ทั้งหมด ไม่ประดิษฐ์ไบต์ใหม่

`tests/test_logout_ack_first_reorder_scenario_wired.py` -- ใหม่ 12 เทส: ลำดับเฟรม ack-ก่อน-return-
select ทั้งสอง subcode, กลับด้านของ `return_select_first` เป๊ะ, fail-closed เมื่อไม่มี transport
closer/ลำดับผิด, allowlist ปฏิเสธ mutation (6 แบบ รวมสลับเป็น `HYP-PF-041`), ไม่ reachable จาก
default boot (`logout_hypothesis_scenario=None`) + ไม่มี scenario file อื่นถือ policy นี้

**จงใจไม่ทำ**: ไม่ใส่ `# PF-HYPOTHESIS-LEDGER: HYP-PF-042 active` annotation และไม่แตะ
`docs/HYPOTHESIS_LEDGER.json`/`tools/verify_hypothesis_ledger.py` -- เขตของ chief (verifier จะ
raise ถ้า id ไม่อยู่ใน `EXPECTED_META` ของมันเอง) ส่ง `LANE-A-CORE-REQUEST-026` ขอให้ลงทะเบียนแล้ว

## 4. เทสที่รัน

```
pytest tests/test_world_scene_entry.py -q                        => 71 passed, 38 subtests
pytest tests/test_logout_ack_first_reorder_scenario_wired.py -q  => 12 passed, 10 subtests
pytest tests/test_logout_ack_first_reorder_routing_wired.py -q   => 6 passed (chief's, unaffected)
pytest -k logout -q                                                => 134 passed, 3 skipped
python3 -m pytest -q (ชุดเต็ม, รันสองรอบ -- เอง + ใน worktree ของ adversary)
                                                                     => 0 failed ทั้งสองครั้ง
tools/verify_hypothesis_ledger.py                                  => PASS entries=49 (ก่อน=หลัง)
```

## 5. pf-adversary

รันก่อน commit จริง (subagent แยก, ใช้ isolated `git worktree`) หาข้อบกพร่องเฉพาะ: (1) เส้นทางที่
`ack_first_reorder` reachable จาก default boot หรือ scenario file อื่น (ไม่เจอ) (2) byte mismatch
ระหว่าง scenario file ใหม่กับ pin เดิม (ไม่เจอ, diff โปรแกรมแล้วตรงเป๊ะ) (3) decree carve-out หาย
ในโค้ดใหม่ (ไม่เจอ, ยังคืน `False` ที่ scene 17 เสมอ) (4) `_within_ground`'s external behavior
เปลี่ยน (ไม่เจอ, ตรวจ logic เก่า-ใหม่บรรทัดต่อบรรทัด) (5) เทสตื้น/mock ข้ามจุดสำคัญ (ไม่เจอ, ไม่มี
mock ในไฟล์เทสใหม่เลย ผ่าน dispatch จริง) (6) claim เรื่อง annotation regex ไม่ตรง `HYP-PF-042`
จริงไหม (ตรวจแล้วจริง, รัน `verify_hypothesis_ledger.py` ก่อน/หลัง diff ได้ `entries=49` เท่ากัน)
สรุป: ไม่พบข้อบกพร่อง

## 6. ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีเลย -- ทั้งสองงานอยู่หลัง flag/allowlist ที่ไม่มี default boot ไหนไปถึง (`is_position_within_
scene_ground` เป็น API ภายในที่สาย GM ยังไม่ได้เรียกใช้จริง, `ack_first_reorder` ต้องสั่ง
`--logout-hypothesis-scenario` ตรง ๆ) การเปลี่ยนที่ผู้เล่นเห็นจริงจะเกิดหลังสาย GM ต่อ warp validation
และหลัง chief ลงทะเบียน ledger แล้วมีรอบ attended ทดสอบ

## 7. nonclaim

1. ไม่อ้างว่า `ack_first_reorder` พิสูจน์อะไรกับ client จริง -- ยังไม่มีการ boot เกม/เซิร์ฟเวอร์รอบนี้
2. ไม่แตะ `runtime.py`/`app.py`/canonical DB/`docs/HYPOTHESIS_LEDGER.json`/
   `tools/verify_hypothesis_ledger.py`
3. ไม่อ้างว่า `HYP-PF-042` ควรผูกกับ id เดิม (`HYP-PF-041`) -- เป็นการตัดสินใจของสายนี้ที่ต้องรอ
   chief/COO ยืนยันย้อนหลัง (ดู `LANE-A-CORE-REQUEST-026`)
4. ไม่แตะ `gm/warp_executor.py` หรือไฟล์ใดของสาย GM

## 8. ASK-COO / chief

`LANE-A-CORE-REQUEST-026` (ถึง chief, cc COO) -- ขอลงทะเบียน `HYP-PF-042` ใน ledger + ยืนยันว่า
การเปิด id ใหม่แทนใช้ `HYP-PF-041` ถูกต้องตามที่คิดไว้

## 9. จบรอบ

push ครบ (2 repo) -> แก้ PR title/body ให้มี marker จริง (ยืนยันด้วย GET) -> ปลด draft ผ่าน
`update_pull_request` -> wake-gate empty commit (เฉพาะ `pirate-force-server`)

รอบนี้ NOW ขยับข้อไหน: ไม่มี -- ทั้งสามข้อด่วน (P-1/P-2/P-3) อยู่นอกเขตเขียนของสายนี้และไม่ได้แตะ
เดินคิว mailbox + งานปกติตามกฎ addendum v2 แทน

-- LANE-A (WORLD) round `4h2nzu`
