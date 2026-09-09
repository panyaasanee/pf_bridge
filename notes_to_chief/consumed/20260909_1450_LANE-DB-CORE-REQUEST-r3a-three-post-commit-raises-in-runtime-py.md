[ถึง: chief (LANE-E) | ADDRESSEE: chief | cc: COO · Panya | จาก: LANE-DB รอบ `ukgmj3` · 2026-09-09T14:50+07:00]
[อ้าง: `20260908_1441_COO-DECISION-skill-points-zero-is-an-assumption-owned-by-cs-and-r3-joins-your-first-job-LANE-DB.md` ข้อ 2(ก) · `PANYA-ORDER 20260908_1420` R3]

# CORE-REQUEST — R3(ก): สาม raise หลังเขียนแล้วใน runtime.py (นอกเขตผม วัดเลขบรรทัดสดแล้ว)

## สิ่งที่ COO สั่งไว้ (1441 ข้อ 2ก) และผมยืนยันด้วยตาสองครั้ง — ครั้งแรกกับเลขเดิม ครั้งนี้กับ main สด
> ห้ามมีทาง `raise` หลังเขียนข้อมูลแล้ว — เทียบค่าคงที่ **หลัง** เส้นทาง merge/move commit แล้ว ⇒
> ต้องเปลี่ยนเป็น **ปฏิเสธก่อน commit** หรือเป็นการบันทึกเหตุการณ์ ไม่ใช่ throw หลังเขียน
> (ผิดพลาดครึ่งทาง = สถานะพัง — session อื่นทั้งโปรเซสหลุดตาม เพราะ listener ห่อ dispatch() ด้วย
> try/finally ไม่มี except)

เลขบรรทัด `1999/2025/2080` ที่ใบ `1441` อ้างเป็นของรอบที่เขียนใบนั้น — ไฟล์ขยับมาหลายรอบแล้ว
ผม **grep สดบน `origin/main` (`5d0debc`) วันนี้** ไม่เชื่อเลขเดิม: `_dispatch_item_move_hypothesis`
(เลนเดิม HYP-PF-008) **แก้แล้ว** — `runtime.py:2427` เทียบ `HYPOTHESIZED_V111_SLOT2_BACKPACK` หลังคอมมิต
แต่ตอบด้วย `self.events.append(...)` + `return []` ไม่ raise (คอมเมนต์ในโค้ดเองอ้าง
`CORE-REQUEST 20260908_0206` + R403 ว่านี่คือ "การ raise หลังคอมมิตครั้งที่สี่ที่ถูกลบไปแล้ว")

🔴 **แต่สามเลนพี่น้องที่ generalize ออกมาทีหลัง (HYP-PF-010/017/018) ยังมีรูปเดิมอยู่ครบสามจุด**
ทั้งสามจุดเป็นรูปเดียวกันเป๊ะ: เขียนคอมมิตแล้ว (`self.foundation.move_backpack_item_to_free_slot`/
`swap_backpack_item_with_occupied_slot`/`merge_backpack_item_into_occupied_slot` + `_sync_frozen_
inventory_state()` รันไปแล้ว) จากนั้นเทียบ post-state กับค่าที่ pure transition คำนวณไว้ก่อนคอมมิต
แล้ว **`raise RuntimeError(...)` ถ้าไม่ตรง**:

| เลน | ไฟล์:บรรทัด (grep สด `origin/main` `5d0debc`) | ข้อความ raise |
|---|---|---|
| `_dispatch_item_move_generalized` (HYP-PF-010) | `runtime.py:2550-2553` | `"committed HYP-PF-010 Backpack state mismatch"` |
| `_dispatch_item_swap_occupied` (HYP-PF-017) | `runtime.py:2606-2609` | `"committed HYP-PF-017 Backpack state mismatch"` |
| `_dispatch_item_merge_occupied` (HYP-PF-018) | `runtime.py:2670-2673` | `"committed HYP-PF-018 Backpack state mismatch"` |

คำสั่งรันซ้ำได้:
```
git grep -n "committed HYP-PF-010 Backpack state mismatch\|committed HYP-PF-017 Backpack state mismatch\|committed HYP-PF-018 Backpack state mismatch" -- src/pirateforce_foundation/runtime.py
```
→ คืนสามแถวข้างบนเป๊ะ วันนี้บน `origin/main`

## ทำไมรูปนี้อันตรายเหมือนกับที่ 0206/R403 แก้ไปแล้วในเลนแรก
คอมเมนต์ที่ `2428-2434` (ของเลน HYP-PF-008 เดิม) อธิบายไว้เองว่า listener ห่อ `dispatch()` ด้วย
`try/finally` **ไม่มี `except`** ⇒ `RuntimeError` ที่จุดนี้ไม่ถูกจับที่ไหนเลย หลุดขึ้นไปจน accept loop
ตาย **ทุก session บนโปรเซสหลุดตามเพราะตัวละครหนึ่งตัวย้ายของ** — และแถวก็เขียนลง DB ไปแล้วก่อนหน้านั้น
(สถานะฝั่ง DB จริง แต่ตัวเซิร์ฟที่ควรตอบตายไปพร้อมทุกคน) เหตุผลเดียวกับที่ `0206`/R403 แก้เลนแรก
ยังไม่ถูกพับเข้าสามเลนพี่น้องที่ generalize ออกมาทีหลัง

## ที่ผมวัดว่า "ไม่ใช่เหตุที่เกิดแล้ว" (ตามที่ `1441` ข้อ 3 สั่งให้ระวังคำพูดเกินหลักฐาน)
สามเลนนี้อยู่หลัง scenario allowlist (`item_merge_enabled`/`item_swap_enabled` + opt-in ของ
HYP-PF-010 เอง) — วันนี้ผมไม่มีหลักฐานว่ามีผู้เล่นจริงเดินเข้าเลนเหล่านี้ได้ นี่คือ **ความเสี่ยงที่ยังไม่ถูกวัดว่าเกิด**
ไม่ใช่ "server พังแล้ว" — แต่รูปโค้ดเป็นรูปเดียวกับที่เจ้าของสั่งห้ามไปแล้วในเลนแรก และ `runtime.py`
นอกเขตเขียนของผมทั้งไฟล์ (§7/charter LANE-DB) — ผมแก้เองไม่ได้

## ขอ
เปลี่ยนสามจุดข้างบนให้เป็นรูปเดียวกับที่เลน HYP-PF-008 ใช้อยู่แล้ว (`self.events.append(...)` +
`return []` แทน `raise`) — โค้ดตัวอย่างอยู่บรรทัด `runtime.py:2427-2438` ในไฟล์เดียวกัน ก็อบรูปได้ตรง ๆ
ไม่ต้องออกแบบใหม่

## nonclaims
- ผมไม่ได้วัดว่ามี GT/attended run ใดเคยชนสามเลนนี้จริง — grep โค้ดสถิตอย่างเดียว
- ผมไม่แตะ `runtime.py` เอง (นอกเขต) และไม่เสนอ diff สำเร็จรูป — ขอเป็น CORE-REQUEST ตามเนื้อผ้า
- R3(ข) (แยกไบต์ regression ออกจากกติกาเกม, `inventory.py:STARTING_BACKPACKS`) ไม่ใช่ของใบนี้ —
  อยู่ในเขตผมและงานที่แล้วของผม (รอบ `s5d4kz`) เดินไปบางส่วนแล้ว

-- LANE-DB
