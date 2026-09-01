# LANE-A round `ztl2u5` -- RE-189 branch 2 (teardown timer variant) built

## NOW.md (read first, per house rule)

Checked `pf_bridge/NOW.md` before anything else, per the standing rule that it overrides
everything else in the prompt, including CHARTER-02's milestone table.

**รอบนี้ขยับ NOW ข้อไหน**: ไม่มีข้อไหนของ NOW.md ขยับรอบนี้ -- P-1/P-2/P-3 เป็นของสาย GM/UI/DB,
GM-A/GM-B/UI-A/UI-B/census-latch ทั้งหมดเป็นของสายอื่นหรือรอ Panya รันเทส attended (ไม่ใช่ตัวบล็อก
สายตามกฎ 60-บรรทัดข้อ 🔴 ที่บอกว่าโค้ด+เทสฝั่งเซิร์ฟเวอร์เสร็จแล้วไม่ใช่ตัวบล็อก) ไม่มีข้อไหนจ่าหน้าถึง
LANE-A โดยตรง `NOW.md` เขียนไว้ตรง ๆ ว่า "ห้ามทำจนกว่า P-1 กับ P-2 จะปิด" เฉพาะ `GT-146` และใบเทสตีมอน
ทุกใบ -- ไม่ใช่งานของสายนี้เลย (logout hypothesis เป็นคนละเรื่อง) รอบนี้จึงกลับไปทำคิวปกติของ LANE-A
ตาม NOW.md's ข้อความ ("สาย A/GM เดินคิวปกติต่อได้") **ทำไม่ขยับข้อไหน เพราะไม่มีข้อไหนอยู่ในเขตเขียนหรือ
ความรับผิดชอบของสายนี้รอบนี้**

## Section A -- prior PR fate

ไม่มี PR `[LANE-A]` ค้างเปิดต้นรอบทั้งสองรีโป (`list_pull_requests(state=open)` เจอแค่ `[LANE-GM]`
draft placeholder ทั้งสองรีโป -- ไม่ใช่ล็อกของสายนี้ ไม่แตะ) ตรวจ PR รอบก่อนของสายนี้ด้วย
`list_pull_requests(state=closed, head=...)` บน branch เดิมที่เคยใช้ -- ไม่พบ (สภาพแวดล้อมรอบนี้ได้
branch ใหม่ `claude/epic-turing-ztl2u5`/`claude/dazzling-volta-ztl2u5` ที่ไม่เคยใช้มาก่อน ไม่มีอะไรต้อง
กู้คืน) งานรอบก่อนของสายนี้ (`njkvcc`) ยืนยันแล้วว่า merged=true ทั้งสอง PR (#490/#730) จากเนื้อหาจดหมาย
ที่อ่านในหัวข้อถัดไป

## Mailbox

สองใบค้าง (`ADDRESSEE: LANE-A` ไม่มี `.CONSUMED.txt`): `20260901_1658` (อนุมัติกิ่ง 2/3 ของ RE-189)
และ `20260901_1807` (chief แก้ overclaim tag-byte เอง) -- ทั้งสองบริโภคแล้วรอบนี้ รายละเอียดเต็มใน
`notes_to_chief/20260901_1844_LANE-A-CORE-REQUEST-re189-branch2-built-branch3-needs-runtime-py-hyp041-ledger.md`

## งานที่สร้าง: RE-189 กิ่ง 2 (`_PROFILE_TEARDOWN_TIMER_VARIANT`)

ใบ `1658` อนุมัติให้สาย A แก้ `logout_hypothesis.py` อีกครั้งเพื่อเพิ่มกิ่ง 2 (teardown timer variant:
`close_delay_ms` เป็น 0/2000/10000/None) และกิ่ง 3 (ack-first reorder) สเปกเต็มอยู่ในใบ `1635`

**ตรวจก่อนสร้าง (ห้ามเดา)**: กิ่ง 2 เป็น pure parameter variation ของ lever ที่ `HYP-PF-013` มีอยู่แล้ว
(`close_delay_ms`/`post_ack_action`, ทั้งคู่ generic อยู่แล้วใน `runtime.py:1876-1955` ไม่ต้องแก้ chief's
file) แต่กิ่ง 3 (สลับลำดับ ack->0x709E) ตรวจ `runtime.py:1901-1928` แล้วพบว่า **ไม่ใช่ pure addition**:
`LOGOUT_RESPONSE_POLICY_RETURN_SELECT_FIRST`'s dispatch ฮาร์ดโค้ดลำดับ 0x709E-ก่อน-ack ไว้ ไม่มีทางเดินสาย
ทั่วไปให้สลับแบบกิ่ง 6 -- เปิด CORE-REQUEST ให้ chief แทนที่จะเดา (ดูจดหมายรอบนี้)

**สร้างเฉพาะกิ่ง 2 รอบนี้**: 4 profile ใหม่ใน `logout_hypothesis.py` (`_PROFILE_TEARDOWN_TIMER_VARIANT_
{0MS,2000MS,10000MS,NEVER}`), 4 scenario JSON ใหม่ใน `scenarios/`, เทส wired ใหม่ 13 ตัวใน
`tests/test_logout_teardown_timer_variant_scenario_wired.py` -- reuse `LOGOUT_ACK_PC_SHA256`/
`LOGOUT_ACK_FRAME_SHA256` เดิมทุกจุด (ไม่มี SHA ใหม่ ไม่มีไบต์ wire ใหม่ที่ถูก "ประดิษฐ์") hypothesis_id
ใหม่ `HYP-PF-041` (grep ยืนยันว่างก่อนใช้) **ไม่ได้ลงทะเบียนใน `docs/HYPOTHESIS_LEDGER.json`** -- ตั้งใจ
ปล่อยให้ chief ทำ (ดูเหตุผลในจดหมาย, ยืนยันด้วย `verify_hypothesis_ledger.py` ว่าไม่จำเป็นสำหรับความเขียว
ของ verifier ตอนนี้)

### pf-adversary จริง (ไม่ใช่ manual checklist)

เซสชันนี้มี Agent tool ใช้งานได้จริง เรียก subagent `pf-adversary` จริงกับ diff (เวิร์กทรีแยก อ่านอย่างเดียว
ไม่แตะเช็คเอาต์จริง -- ยืนยันด้วย `git worktree list` หลังจบ) ผลตรง: ไม่พบ divide-by-zero/race จาก
`close_delay_ms=0`, ไม่พบ allowlist bypass, ไม่พบ escalation path ไป default boot, `verify_hypothesis_
ledger.py` PASS entries=48 ไม่ขยับ พบสองจุดจริงที่แก้ก่อนส่ง: (1) พรอมป์ที่สั่งงาน agent เผลอเขียนจำนวนเทส
ผิด (16 vs 12 จริงตอนนั้น) -- ไม่ใช่บั๊กโค้ด แก้คำพูดในจดหมาย (2) ช่องว่างเทสจริง: allowlist mutation
test ของไฟล์ 2000ms ไม่เคยถูกเขียน -- เพิ่มแล้ว (`test_2000ms_variant_allowlist_is_exact`) รวม 13 เทส
ยืนยันซ้ำ 13/13 ผ่านหลังแก้

**คำถามเชิงญาณวิทยาที่ pf-adversary ทิ้งไว้** (ไม่ใช่บั๊ก แต่บันทึกไว้ก่อนมีใครเปิดใบเทส attended ให้กิ่งนี้):
`GT-008` วัดแล้วว่าไคลเอนต์ไม่สังเกตการปิด socket ที่ 250ms เลย -- ผลลบที่ทั้งสี่จุดสวีป (0/2000/10000ms/
never) จะพิสูจน์อะไรเพิ่มจาก `GT-008` จริง หรือแค่ยืนยันซ้ำสิ่งเดียวกัน? รอบนี้ไม่มีใบเทส attended ใหม่จึง
ไม่ต้องตอบตอนนี้ แต่ chief/COO ควรเห็นก่อนมีคนเปิดใบ

## เทสที่รัน

```
pytest tests/test_logout_teardown_timer_variant_scenario_wired.py -q  => 13 passed
pytest -k logout -q                                                   => 97 passed, 3 skipped
pytest -q (ชุดเต็ม)                                                    => 6395 passed, 327 skipped, 0 failed
tools/verify_hypothesis_ledger.py                                     => PASS entries=48
```

## CORE-REQUEST เปิดให้ chief (สองเรื่อง แยกกัน)

1. กิ่ง 3 (ack_first_reorder) ต้องการ routing branch ใหม่ใน `runtime.py` -- ขอให้ chief เลือกทำเอง
   หรืออนุมัติให้สาย A แก้ครั้งเดียว
2. ลงทะเบียน `HYP-PF-041` ใน `docs/HYPOTHESIS_LEDGER.json` -- สาย A ไม่เดาวิธีคำนวณ
   `CANONICAL_CONTENT_SHA256` เอง (ความเสี่ยงพังทั้งโปรเจกต์ถ้าคำนวณผิด) ตามธรรมเนียมที่ chief ทำมาตลอด

## ไฟล์ที่แตะ

**pirate-force-server** (3 ไฟล์เนื้อหา + 4 scenario json):
- `src/pirateforce_foundation/logout_hypothesis.py`
- `scenarios/logout_hypothesis_teardown_timer_variant_{0ms,2000ms,10000ms,never}.json`
- `tests/test_logout_teardown_timer_variant_scenario_wired.py`

**pf_bridge** (5 ไฟล์):
- `notes_to_chief/20260901_1658_CHIEF-REPLY-*.md.CONSUMED.txt` + สำเนาต้นฉบับใน `consumed/`
- `notes_to_chief/20260901_1807_CHIEF-REPLY-*.md.CONSUMED.txt` + สำเนาต้นฉบับใน `consumed/`
- `notes_to_chief/20260901_1844_LANE-A-CORE-REQUEST-*.md` -- ใหม่
- `rounds/A_20260901_1844_ztl2u5_re189-branch2-teardown-timer-variant-built.md` -- ไฟล์นี้เอง

-- LANE-A (WORLD) round `ztl2u5`
