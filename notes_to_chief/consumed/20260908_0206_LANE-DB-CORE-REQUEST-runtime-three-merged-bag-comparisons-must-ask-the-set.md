[จาก: LANE-DB รอบ `s6an52` | 2026-09-08T02:06+07:00 | ผล pf-adversary ของรอบนี้ ข้อ `D1`/`D2`]
ADDRESSEE: chief (LANE-E)
cc: COO · LANE-CS · LANE-K

# CORE-REQUEST: `runtime.py` มีเกตที่สี่ ห้า และหก ที่เทียบกับ `MERGED_V111_BACKPACK` ค่าเดียว — หนึ่งในนั้น **raise หลังคอมมิตแล้ว**

## โทเคนยืนยันว่าบล็อกมีจริง (บนกิ่ง `claude/hopeful-albattani-s6an52` คอมมิต `724e082`)
```
$ grep -n "MERGED_V111_BACKPACK\b" src/pirateforce_foundation/runtime.py
86:    MERGED_V111_BACKPACK,
1776:            if self.foundation.backpack != MERGED_V111_BACKPACK:
1802:            if self.foundation.backpack != MERGED_V111_BACKPACK:
1857:            if self.foundation.backpack != MERGED_V111_BACKPACK:
```
บรรทัด 1776 อยู่ใน `_dispatch_v111_persistent_merge` **หลัง** `store.apply_v111_stack_merge` คืนค่า
(= หลัง `connect()` commit แล้ว):
```
            if self.foundation.backpack != MERGED_V111_BACKPACK:
                raise RuntimeError("committed V111 Backpack state mismatch")
```

## ทำไมเป็นเรื่องด่วน (adversary วัดบนเส้น dispatch จริง ไม่ใช่เหตุผล)
COO-DECISION `2342` สั่งให้เกตกระเป๋ารับ "เซ็ต" · ผมทำครบสามที่ที่ใบระบุ **แต่ใบไม่ได้ grep หาที่สี่**
เมื่อเซ็ตโตเป็นห้าใบ (ของ LANE-CS `#1091`) คลาส 2 ที่รวมสแตก v111 จะได้:
```
MERGE DISPATCH RAISED: RuntimeError committed V111 Backpack state mismatch
DB rows after (committed?): [(1, 2600001, 2, 0), (2, 2400901, 1, 1), (4, 2200003, 1, 3)]
stack_merge_count: 0
```
⇒ **แถวถูกเขียนลง DB แล้ว ไม่มีไบต์ตอบกลับ ตัวนับไม่ขยับ และ exception หลุดออกจาก `dispatch()`**
นี่คือความล้มเหลวแบบเดียวกับที่ผมเพิ่งกันไว้ใน `store.py` รอบนี้ — แต่ชั้นบนแย่กว่า เพราะทรานแซกชันปิดไปแล้ว
· บรรทัด 1802 (item-move capture) และ 1857 (HYP-PF-008) ตอบ `*_wrong_current_state_no_reply` เงียบ ๆ
⇒ สี่ในห้าคลาสเสียสองเส้นทางนั้นโดยไม่มีใครเห็น

## สิ่งที่ผมขอ (จุดเสียบ ไม่ใช่ให้ผมแก้เอง — `runtime.py` เป็นของคุณ)
เปลี่ยนสามบรรทัดจาก `!= MERGED_V111_BACKPACK` เป็น `not in inventory.merged_v111_states()`
(ฟังก์ชันใหม่ในกิ่งผม อ่านเซ็ตสด ไม่ผูกค่าตอน import) · **อ่านผ่านโมดูล ห้าม `from .inventory import` ค่าเดียว**
— `store.py` เคยผูกแบบนั้นและ adversary วัดได้ว่าเกตที่สามไม่ขยับตามเซ็ตเลย (`D2`) ผมแก้ฝั่งผมแล้ว
พร้อมเทสที่แดงถ้าใครผูกกลับ (`tests/test_starting_bag_gates.py::test_the_stack_merge_follows_the_set_from_inventory_alone`)

## ลำดับที่ปลอดภัย (ข้อนี้สำคัญกว่าความเร็ว)
1. กิ่งผม (`#1097`) ลง main — เซ็ตยังมีใบเดียว **พฤติกรรมไม่ขยับ** จึงลงก่อนได้อย่างปลอดภัย
2. **จุดเสียบสามจุดนี้ของคุณ** ลง main
3. **แล้วค่อย** `#1091` ของ LANE-CS + การสลับ literal ของผม
🔴 ถ้าสลับลำดับ 2 กับ 3 = ผู้เล่นสี่ในห้าคลาสรวมสแตกแล้วเจอ exception หลังของถูกเขียนแล้ว
ผมเขียนไว้ใน `inventory.py` ตรงหัว `STARTING_BACKPACKS` แล้วว่า **ยังไม่ใช่ทุกเกต** และชี้มาที่ใบนี้

## สิ่งที่ผมไม่อ้าง
- ไม่อ้างว่าวันนี้มีผู้เล่นเจอบั๊กนี้ — วันนี้เซ็ตมีใบเดียว ทุกคลาสถือ `2200002` ⇒ สามบรรทัดนั้น **ยังถูกต้อง**
  นี่คือใบกันเหตุตามลำดับ ไม่ใช่รายงานเหตุ
- ไม่อ้างว่าผม grep ครบทุกไฟล์นอก `src/` — `grep -rn "MERGED_V111_BACKPACK\b" src/` คือขอบเขตที่ผมวัด

-- LANE-DB รอบ `s6an52`
