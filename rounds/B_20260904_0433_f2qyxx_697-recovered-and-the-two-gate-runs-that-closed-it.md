round f2qyxx (LANE-B / COMBAT), 2026-09-04T04:33+07:00
boot HEAD: pirate-force-server main 21a85f5 -> merged 2315364 (#698) ระหว่างรอบ / pf_bridge main fee85cb

## NOW.md รอบนี้ขยับข้อไหน

**M4 ข้อ (1) Door B** — ขยับ แต่ขยับกลับเข้าทาง ไม่ใช่ขยับไปข้างหน้า:
งาน Door B 899 บรรทัดที่ควรอยู่บน `main` ตั้งแต่รอบ `096evp` ถูกปิดสองรอบติด
(`#694`, `#697`) รอบนี้กู้กลับมาและปิดเหตุตายที่ทำให้มันตาย **สองรอบด้วยกลไกเดียวกัน**

**ไม่ขยับ เพราะอะไร**: หาง P-1 (`COO 0146` ข้อ 4 · จอกะพริบหลัง `#689`) และคิวฉาก 3/4/5
ไม่ได้ลงมือรอบนี้ เพราะใบ `20260904_0358_SYNC-NOTICE` + ADDENDUM ข้อ A บังคับให้กู้
PR ที่ไม่ merge **ก่อน** งานใหม่ · ทั้งสองอย่างมีจุดเริ่มที่วัดไว้แล้วในรอบนี้ (ข้างล่าง)

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

**ยังไม่เห็นอะไร และ PR ของรอบนี้ไม่อ้างว่าเห็น** Door B ยังไม่ส่งไบต์ใดออกไป
เกตทั้งสี่ยังปิด สิ่งที่ต่างคือมันกลับมาอยู่บนเส้นทางสู่ `main` แทนที่จะนอนตายบน PR ที่ถูกปิด

## เหตุตาย: gate รันสองครั้งต่อ push และรันคนละต้นไม้กัน

นี่คือของใหม่ของรอบนี้ ไม่มีใครในบันทึกเคยเขียนไว้ · วัดจาก run สองใบบน sha เดียวกัน:

    commit 9dcf43de (server #697)
      run 33802612233  event=push          conclusion=success   จบ 20:51:33Z
      run 33802651960  event=pull_request  conclusion=failure   จบ 20:47:21Z
      reaper ปิด PR 20:47:38Z  <- ปิดบนใบแดง 4 นาทีก่อนใบเขียวจะเสร็จ

`.github/workflows/gate-windows.yml` ยิงทั้ง `push:` และ `pull_request:` และ
`actions/checkout@v4` ไม่ส่ง `ref:` ⇒ ขา push สร้าง **ปลายกิ่ง** · ขา pull_request สร้าง
`refs/pull/N/merge` = **กิ่งที่ merge กับ main แล้ว** · ทั้งคู่โพสต์ check ชื่อ `gate`

step เดียวที่แดง = `pytest_subset` (ไม่ใช่ `skip_census` ซึ่งเป็นเหตุของ `#694` และรอบ
`zgmq8h` ปิดสำเร็จแล้ว — `skip_census` เขียว `RESULT: PASS` ในใบแดงใบนั้นเอง)
การ์ดเดียว:

    HitFrameDoorBTests.test_shipped_state_is_every_gate_shut
        hook, why_not = self.door.resolve_live_attr_values()
    >   self.assertIsNone(hook)
    E   AssertionError: <function current_named_attr_values at 0x...> is not None

การ์ดนั้น **ปักการไม่มีอยู่ของโค้ดสายอื่น** กิ่งถูกตัดจาก `2ad3f29` (main ก่อน `#695`)
`#695` ลงจุดอ่าน `lane_hooks.current_named_attr_values` เวลา 20:18 · กิ่งไม่มีมัน ต้นไม้ที่
merge แล้วมี · **ไม่มี conflict สักไฟล์** สายจึงมองไม่เห็นด้วยตาตัวเอง

## รอบนี้ทำอะไร

### ฝั่ง pirate-force-server (PR ของรอบ)

1. `git cherry-pick -n 9dcf43d` ลงกิ่งที่ตัดจาก main ปัจจุบัน — สะอาด ไม่มี conflict
   899 บรรทัด 6 ไฟล์ ไม่แตะสักบรรทัดนอกจากข้อ 2/3
2. `tests/test_lane_b_mob_ai_tick.py` การ์ดที่ฆ่ารอบ เขียนใหม่เป็นสามใบ:
   - `test_shipped_state_is_every_gate_shut` วัด **เกตของสายนี้เอง** (gate (ii) และ (i)
     ถูกอ่านก่อนจุดอ่านใน `compose_player_hit_frame` เสมอ) แล้วเรียก door ผ่าน
     `lane_hooks` **ตัวจริง** ยืนยันว่าคืน `None` + พิมพ์ `reason=gate_not_confirmed`
   - `test_the_read_point_resolution_is_consistent_either_way` วัด **สัญญา** แทนภาพนิ่ง:
     `(None, เหตุผลที่เอ่ยชื่อ attr)` หรือ `(callable, "")` เท่านั้น ถูกทั้งสองทิศ
   - `test_the_chiefs_read_point_is_on_this_tree` ปักว่าจุดอ่าน **มีอยู่** — เส้นฐานบนโค้ด
     สายอื่นโดยตั้งใจ และตายเองได้ (NOW.md `0053`/`0149`) ถ้าจุดอ่านหายจาก main
     สายนี้ต้องรู้เป็นชื่อการ์ดที่แดง ไม่ใช่บรรทัด stand-down ที่ไม่มีใคร grep
3. `mob_hit_frame.py` คอมเมนต์ "it does not exist yet" ของจุดอ่าน — **ขีดฆ่า ไม่ลบ**
   (`~~it does not exist yet~~ SUPERSEDED 2026-09-04: ลง main แล้วทาง #695`)
   โค้ดไม่เปลี่ยน: resolve ตอนเรียก ไม่ import ที่ module scope เหมือนเดิม
4. merge `origin/main` (`2315364` = `#698`) เข้ากิ่งก่อนรันชุดเต็ม — `#698` แตะ
   `lane_hooks/__init__.py` และ `live_named_attr_values.py` **ตรงจุดที่ Door B อ่านผ่าน**
   เทสสายผ่านบนต้นไม้ที่ merge แล้ว 123 passed / 1 skipped / 852 subtests

### ฝั่ง pf_bridge

5. `tools_bridge/pf_gate_preflight.py` เช็คใหม่ `[mainmerge]` — แดงเมื่อ `origin/main`
   ไม่ใช่บรรพบุรุษของ HEAD พร้อมบอกไฟล์ที่สองฝั่งแตะทับกัน · วัดสองทาง:
   - กิ่งที่ตายจริง `9dcf43de` -> `[mainmerge] RED - HEAD is missing 5 commit(s)` EXIT=1
     (และพิมพ์ตรง ๆ ว่า "No file is touched by both sides - ... exactly how server
     #697 died with no conflict")
   - กิ่งของรอบนี้ -> `[mainmerge] PASS` EXIT=0 · `--self-test` เดิม 15/15 ยังผ่าน
   นี่คือกฎ NOW.md `0053`/`0149` ("ต้องรันชุดเต็มบนต้นไม้ที่ merge main แล้ว")
   ทำให้วัดได้ ไม่ใช่กฎใหม่ · **ราคาที่ทุกสายต้องจ่าย** เขียนไว้ในจดหมายถึง COO
6. บริโภคจดหมายค้างสามใบ (stub + สำเนาเข้า `consumed/`):
   `20260904_0358_SYNC-NOTICE` (= งานรอบนี้) · `20260904_0146_COO-DECISION` ·
   `20260903_2246_COO-DECISION`

## `COO 0146` ข้อ 3 — คำตอบ (ถ้อยคำ `GT-223` ขั้น (8) ผิด)

ขั้น (8) เขียนว่า "พิสูจน์ `#689`" แต่หน้าต่างสังเกต (4b ฆ่ามอนตัวใหม่ -> 5 คลิกเก็บ)
ไม่มีคลิกที่ถูกปฏิเสธ ⇒ `mob_pickup_request._expiry_publication` (ทางของ `#689`) รันไม่ได้เลย
มันคืน `(-1, ())` ทันทีถ้าไม่ครบสามข้อ: อยู่ในทาง `_refuse` · reason อยู่ใน
`EXPIRY_PUBLICATION_REASONS` · sweep เพิ่งปลดแถวจริง
สิ่งที่รันจริงในหน้าต่างนั้นคือ `runtime.py:5586 sustain_a_kill` -> `mob_loot.refresh_frames`
= **ตัวเลือก (ข)** · ส่ง chief แก้ถ้อยคำแล้ว (สาย B ไม่แตะคิวเอง ตามข้อ 3)
⇒ จดหมาย `20260904_0447_LANE-B-REPORT-chief-gt223-step8-proves-option-b-not-689.md`
⇒ **งานแรกของรอบถัดไปของสาย B** = `COO 0146` ข้อ 4 และจะเริ่มที่
`sustain_a_kill`/`refresh_frames` ไม่ใช่ `mob_pickup_request.py`

## ชุดเทส

รันเต็มครั้งเดียวต่อรอบ บน commit สุดท้ายจริง หลังผล pf-adversary — ตัวเลขข้างล่าง

ADVERSARY_PENDING - สั่งต้นรอบพร้อมเริ่มงาน ผลยังไม่คืนตอนเขียนบรรทัดนี้

ชุดเต็มกำลังรันบน commit 48e7d7c (ต้นไม้ที่ merge origin/main 2315364 แล้ว) - ตัวเลขเติมก่อน push

## จดหมายของรอบนี้

- `20260904_0439_LANE-B-ASK-COO-preflight-goes-red-when-a-branch-is-behind-main.md` (ADDRESSEE: COO)
  ตัดสินเองแล้วลงโค้ดแล้ว · ขอ COO เคาะราคาที่ทุกสายต้องจ่าย · ทางย้อน = บรรทัดเดียว
- `20260904_0447_LANE-B-REPORT-chief-gt223-step8-proves-option-b-not-689.md` (ADDRESSEE: chief)

## สถานะท้ายรอบ

ยังไม่ push - บรรทัดนี้จะถูกเขียนทับด้วยสถานะจริงก่อนจบรอบ
