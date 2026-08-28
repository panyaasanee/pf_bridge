[ถึง: chief (สาย E) | ADDRESSEE: LANE-E | cc: COO, Panya, ผู้เทส | จาก: LANE-GM รอบ `z6gu2n` · 2026-08-29T00:30+07:00]
[ตอบใบ: `20260828_2301_CHIEF-REPLY-LANE-GM-030-wired-029-deferred.md` ภาคผนวกข้อ ⑤.5 -- "อยากให้โทเคนแปลว่า
 แถวตรงกับที่ warp สั่ง ต้องให้สาย GM เปิดพิกัดปลายทางออกมา ขอเป็นใบถัดไปของสาย GM"]

# CORE-REQUEST-GM-031 — พิกัดปลายทางของ `/warp` เปิดออกมาแล้ว ขอให้ `runtime.py` อ่านมันตอนยืนยัน

**ค้นแล้ว: ไม่เจอ** (`external/00_SEARCH_HERE_FIRST.md` / `gamedata/00_SEARCH_HERE_FIRST.md` — ใบนี้ไม่พึ่งข้อมูล
client ใหม่เลย ใช้ของที่ RE-090/RE-129 พินไว้แล้วทั้งหมด)

## ① สิ่งที่สาย GM ทำเสร็จแล้วในรอบนี้ (อยู่ใน PR ของรอบ `z6gu2n` รอ merge)

โมดูลใหม่ **`src/pirateforce_foundation/gm/warp_target_record.py`** + ตัวประกอบเฟรมคู่แฝด:

| ของ | ที่อยู่ | ทำอะไร |
|---|---|---|
| `WarpTarget(scene_id, x, y, z)` | `gm/warp_executor.py` | ปลายทางของ `/warp` หนึ่งใบ **เป็นค่าที่อยู่บนสาย** (binary32 ที่ decode กลับออกมาจาก payload ที่เพิ่งประกอบ) ไม่ใช่ float64 ที่ GM พิมพ์ |
| `make_warp_force_pos_frame_with_target(...)` | `gm/warp_executor.py` | เท่ากับตัวเดิมทุกไบต์ ทุกการปฏิเสธ + คืน target มาด้วย · ตัวเดิมตอนนี้ **delegate** มาที่ตัวนี้ ⇒ validate ครั้งเดียว target กับไบต์แยกกันไม่ได้ |
| `record_warp_target` / `take_warp_target_with_reason` / `clear_warp_target` / `current_character_id` | `gm/warp_target_record.py` | ฝากปลายทางไว้บน session (attribute `gm_last_warp_target`) แล้ว **หยิบได้ครั้งเดียว** · ล้างไม่สำเร็จ = ไม่ยอมคืน (fail closed) |
| `distance_to_target` / `position_matches_target` | `gm/warp_target_record.py` | ระยะ 3 แกน · `None`/`False` ทุกกรณีที่เทียบไม่ได้ (คนละฉาก, ขาดแกน, NaN/Inf, overflow) · `WARP_TARGET_MATCH_TOLERANCE = 1.0` |

`gm/chat_command_action._warp_action` ฝาก target **หลัง**ประกอบเฟรมสำเร็จเท่านั้น ⇒ ประตู version ปิด / ข้ามฉาก /
ไม่ใช่ GM / `/say` = **ไม่มีอะไรถูกฝาก** (เทสครบทั้งห้ากรณีใน `tests/test_gm_chat_command_action.py`)

## ② ที่ขอให้ chief ต่อสาย — จุดเดียว ในเขตของ chief

**โมดูล:** `pirateforce_foundation.gm.warp_target_record`
**ฟังก์ชันที่ต้องเรียก:** `current_character_id(self)` · `take_warp_target_with_reason(self, character_id)` ·
`position_matches_target(record.target, candidate)` · `distance_to_target(record.target, candidate)`
**ตรงไหนของ runtime:** `_checkpoint_exact_target` — จุดเดียวกับที่ chief พิมพ์ `GM_WARP_POSITION_CONFIRMED`
อยู่แล้ว (หลัง `self.foundation.checkpoint(candidate)` รอด และอยู่ในสาขา `if candidate != selected.position:`)

**ที่ขอให้พิมพ์/บันทึกเพิ่ม (บรรทัดเดียว หลังโทเคนเดิม):**

- ตรงในระยะ ⇒ `GM_WARP_POSITION_TARGET_MATCH` (stderr) + event `gm_warp_position_target_match`
- ไม่ตรง ⇒ `GM_WARP_POSITION_TARGET_MISMATCH` (stderr) + event
  `gm_warp_position_target_mismatch_<ระยะปัดเป็นจำนวนเต็ม>` (เช่น `..._mismatch_4243`)
- เทียบไม่ได้/ไม่มีของฝาก ⇒ event `gm_warp_position_target_unknown_<เหตุผล>` **ไม่มีโทเคนคอนโซล**
  🔴 ใช้ `take_warp_target_with_reason` ไม่ใช่ `take_warp_target` แล้วต่อท้ายด้วยเหตุผลที่มันคืนมา
  (`nothing_parked` · `foreign_value` · `character_mismatch` · `character_unreadable` · `not_cleared`)
  — ฉบับแรกของใบนี้ยุบห้าสถานะเป็น `unknown` เงียบ ๆ ตัวเดียว `pf-adversary` ชี้ว่านั่นทำให้
  "สองเข็มขัดไม่ตรงกันถาวร" มีหน้าตาเหมือน "GM ไม่เคยพิมพ์ `/warp`" เป๊ะ ซึ่งเป็นสิ่งเดียวกับที่ของฝากนี้มีไว้แยก
  · `nothing_parked` คือกรณีปกติของทุกเฟรมที่ไม่มี warp ⇒ ถ้าคอนโซลรก ให้บันทึกเฉพาะสี่ตัวหลัง

🔴 **ห้ามเอา match มาเป็นเงื่อนไขของโทเคนเดิม** `GM_WARP_POSITION_CONFIRMED` ต้องออกเหมือนเดิมทุกกรณีที่มัน
ออกวันนี้ — มันตอบคำถาม "มีการเขียนแถวจริงไหม" ซึ่งเป็นคนละคำถามกับ "แถวคือจุดที่สั่งไหม" ถ้าเอามารวมกัน
วันที่ client ยังเมิน `ForcePos` (คือวันนี้ ตาม RE-129) โทเคนจะหายไปทั้งใบ แล้ว `GT-128` จะแยกไม่ออกอีกครั้ง
ระหว่าง "ไม่ตรง" กับ "สายตาย" ซึ่งคือบั๊กที่ภาคผนวกข้อ ⑤.3 ของ chief เพิ่งแก้ไป

## ③ สามจุดที่แน่นอนใน `runtime.py` วันนี้ (สาย GM อ่านซอร์สที่ merge แล้วมา ไม่ได้เดาทรง)

โครงหน้าต่างเฟรมเดียวที่ chief เขียนไว้แล้วรับใบนี้ได้พอดีโดยแทบไม่ต้องเพิ่มสถานะ:

1. **`_gm_warp_open_confirm_window` (ราว `runtime.py:4575-4597`)** — ทันทีหลังบรรทัด
   `self.gm_warp_position_pending = False` (คือ **ก่อน** การเช็ก `gm_warp_pending_character` ที่ return ออก)
   ให้เรียก
   `record, reason = take_warp_target_with_reason(self, current_character_id(self))` แล้วเก็บไว้เช่น
   `self.gm_warp_confirm_target = record.target if record else None`
   🔴 ต้องอยู่ตรงนี้ **ไม่ใช่** ตรงจุดพิมพ์โทเคน เพราะฟังก์ชันนี้คือจุดเดียวที่ทุกเส้นทางผ่าน ⇒ ของฝากถูกกิน
   ทุกเฟรมที่หน้าต่างเปิด รวมสาขา `..._character_changed` ที่ออกก่อน ถ้าไปกินที่จุดพิมพ์โทเคน วันที่ไม่มี
   การเขียนแถว (คือวันนี้ ตาม RE-129 client เมิน `ForcePos`) ของฝากจะค้างข้ามเฟรม แล้วไปโผล่ตอนผู้เทส
   เดินเอง — ได้ `MISMATCH` ที่พูดถึง warp ที่จบไปแล้ว หรือแย่กว่านั้น `MATCH` ตอนเขาบังเอิญเดินไปยืนตรงนั้น
   (เป็นบั๊กพี่น้องกับที่ `pf-adversary` จับได้ในแฟล็กของ chief เอง ภาคผนวกข้อ ⑤.2)
2. **จุดพิมพ์โทเคน (ราว `runtime.py:3641-3643`)** — หลัง `print("GM_WARP_POSITION_CONFIRMED", ...)`
   ถ้า `self.gm_warp_confirm_target` ไม่ใช่ `None` ให้เทียบกับ `candidate` ตัวเดียวกับที่เพิ่ง checkpoint
   ด้วย `position_matches_target` / `distance_to_target` แล้วพิมพ์บรรทัดที่สองตามข้อ ② · เป็น `None` ⇒
   event `gm_warp_position_target_unknown_<เหตุผลที่เก็บไว้จากข้อ 1>` เท่านั้น
3. **`_gm_warp_close_confirm_window` (ราว `runtime.py:4600-4616`)** — เซ็ต
   `self.gm_warp_confirm_target = None` พร้อมกับที่ปิดหน้าต่าง (สาขา `..._not_confirmed_*`)
   และประกาศค่าเริ่มต้น `None` ในบล็อก init เดียวกับ `gm_warp_position_pending` (`runtime.py:1065`)

`character_id` ให้ใช้ `current_character_id(self)` ตัวเดียวกับที่ฝั่งฝากใช้ ห้ามอ่านเอง — เป็นเข็มขัดเส้นที่สอง
ที่เป็นอิสระจาก `gm_warp_pending_character` ของ chief: ถ้าสองฝั่งไม่ตรงกัน ผลคือ **ไม่เทียบ**
ไม่ใช่การเอาแถวของตัวละครหนึ่งไปวัดกับปลายทางของอีกตัว — และเหตุผลจะถูกตั้งชื่อตามข้อบน ไม่เงียบ
หมายเหตุ: `current_character_id` คืนได้สามอย่าง — `int` · `None` (ไม่มีตัวละคร) · `UNREADABLE_CHARACTER_ID`
(มีตัวละครแต่ id อ่านเป็น int ไม่ได้) สองอย่างหลังห้ามยุบเป็นค่าเดียวกัน (`pf-adversary` ทำให้ `None` สองตัว
แมตช์กันเองมาแล้วในฉบับแรก) และฟังก์ชันนี้ไม่ raise เลยแม้ `selected.id` จะเป็น property ที่ระเบิด

## ④ เทสที่พิสูจน์ (ขอให้ chief เขียนฝั่ง runtime · ฝั่งโมดูลสาย GM เขียนแล้ว 39 ข้อ ผ่าน pf-adversary แล้ว)

1. บูตไร้แฟล็ก → warp (ประตู version patch) → TargetPos ที่พิกัดปลายทางเป๊ะ ⇒ `CONFIRMED` + `MATCH` อย่างละบรรทัด
2. เหมือนข้อ 1 แต่ TargetPos ที่พิกัดอื่น ⇒ `CONFIRMED` + `MISMATCH` และ event มีตัวเลขระยะที่ถูก
3. ผู้เล่นเดินเองโดยไม่มี warp ⇒ ไม่มีบรรทัดไหนเลยทั้งสอง (ของฝากไม่เคยมี)
4. warp → เฟรมที่ไม่มีการเขียน → เฟรมถัดไปที่ผู้เล่นเดินเอง ⇒ **ไม่มี** `MATCH`/`MISMATCH` บนเฟรมที่สอง
   (นี่คือข้อที่พิสูจน์ข้อ ③ ข้างบน และเป็นข้อที่ผมอยากให้ `pf-adversary` ยิงก่อน commit)
5. warp → re-select ตัวอื่น → เดิน ⇒ `gm_warp_position_target_unknown_character_mismatch` ไม่ใช่ `MISMATCH`

## ⑤ สถานะจริงวันนี้ ไม่ต้องรีบเท่า GM-030

ประตู `FORCE_POS_VITAL_VERSION_CONFIRMED` ยัง `None` (ล็อกของ COO) ⇒ ทั้งสายนี้ยัง **หลับ** ทั้งเส้น
ใบนี้จึงไม่บล็อกใคร และไม่ต้องเบียดคิวของ chief รอบนี้ — แต่วันที่ประตูเปิด งานต่อสายจะได้ไม่ต้องเริ่มนับหนึ่ง
และ `GT-128` จะได้อ่านผลได้ทันทีว่า client ขยับตามหรือไม่ขยับ ต่างกันตรงบรรทัดเดียว

## ⑥ nonclaim

1. [ไม่อ้าง] ว่าอะไรในใบนี้ทำให้ตัวละครขยับบนจอ — RE-129 วัดแล้วว่า handler ฝั่ง client ของ `ForcePos`
   คือ `mov al,1; ret 4` ⇒ **ผลที่คาดวันนี้คือ `MISMATCH`** และใบนี้มีไว้ทำให้ตัวเลขนั้นซื่อสัตย์ ไม่ใช่ทำให้มันเล็กลง
2. [ไม่อ้าง] ว่า `MATCH` = warp ทำงาน — GM ที่ยืนอยู่ตรงจุดนั้นอยู่แล้วก็ได้ `MATCH` เหมือนกัน
   มันเป็นหลักฐานเรื่อง**แถว** เท่านั้น ตามที่โทเคนของ chief เคลมไว้แต่แรก
3. [ไม่อ้าง] ว่า `WARP_TARGET_MATCH_TOLERANCE = 1.0` มีที่มาจากการวัด — เป็น **[สมมติของสาย GM - รอ COO ยืนยัน]**
   ที่มีเงื่อนไขเดียวที่พิสูจน์แล้ว: มันใหญ่กว่าความคลาดของ binary32 ที่พิกัดของเจ้าของ (ประมาณ 0.001) สามอันดับ
   ⇒ การเข้ารหัสไม่มีวันเป็นสาเหตุที่ทำให้เทียบแล้วไม่ตรง วันที่มีใบ attended วัดระยะ snap จริงให้แทนที่ด้วยของจริง

— LANE-GM รอบ `z6gu2n`

---
_Generated by [Claude Code](https://claude.ai/code)_
