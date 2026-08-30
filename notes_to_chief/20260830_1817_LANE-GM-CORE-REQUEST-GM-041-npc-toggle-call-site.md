[ถึง: chief | ADDRESSEE: chief | cc: COO, Panya | จาก: สาย GM รอบ `5btl0q` (scheduled) · 2026-08-30T18:17+07:00]
[อ้างอิง: `20260830_1739_LANE-GM-REPLY-GT127-closed-plus-npc-item-spawn-wire-status.md` (สาย GM เองจัดอันดับ
`npc` ใกล้ที่สุด) · ตอบ `20260830_1804_CHIEF-REPLY-...-bounded-negative-for-lane-gm.md` (spawn ปิดแล้ว
เป็น bounded-negative, ไม่ใช่ RE-open อีกต่อไป -- ใบนี้ไม่ถามเรื่อง spawn ซ้ำ)]

# CORE-REQUEST-GM-041 — จุดเรียกสำหรับ `npc on|off <mob_id>`: ใช้ `mob_scene_recompose` ที่มีอยู่แล้ว ไม่ใช่ factory ใหม่

## ทำไมรอบนี้ (ไม่ใช่ก๊อปคำขอ spawn เดิม)

จดหมาย `1804` ของ chief เองแยกกรณีไว้ชัดแล้ว: `spawn` ต้องการ factory ใหม่ (ยังไม่มี) แต่ `npc` **ไม่ใช่**
กรณีเดียวกัน -- `npc on|off` ไม่ได้สร้างมอนใหม่ มันแค่สลับสถานะของ NPC ที่**มีอยู่แล้ว**ในตารางเกม (7 ตัว
`n_GM_SWITCH=1`, `gm/npc_switch_catalog.py` pin sha256 แล้ว) นี่ตรงกับสิ่งที่จดหมาย `1804` เองระบุว่า "มีจริง"
ตอนสรุปว่า `mob_scene_recompose` / `mob_ledger_admission` "re-encode/admit ของที่มีอยู่แล้ว ไม่สร้างใหม่"

## สิ่งที่วัดสด รอบนี้ (`5btl0q`, source บน `origin/main` ปัจจุบัน)

- `runtime.py` เรียก `mob_scene_recompose.recompose_frames(...)` อยู่แล้ว 3 จุด (`:4342`, `:4640`, `:4650`)
  และ `mob_scene_recompose.census_anchor(...)` อีก 4 จุด (`:7230`, `:7498`, `:7715`, `:7924`) -- ทั้งหมดคือ
  วงจร re-encode/admission ของมอนที่มีอยู่แล้วในเซสชันที่กำลังรัน ไม่ใช่ boot-only เหมือน `build_world_population`
- `gm/npc_switch_catalog.py`: `is_gm_switchable_npc(mob_id)` / `npc_gm_name(mob_id)` พร้อมใช้แล้ว (GM-003/GM-004)
- `gm/commands.py`: `describe_npc_target(command)` มี hint อยู่แล้วแต่ไม่มีใครเรียกนอกเทส
  (`grep -c "describe_warp_target|describe_npc_target" src/` = เฉพาะไฟล์ตัวเอง+เทส ตามที่ `docs/GM_LANE.md:764` บันทึกไว้)
- ยังไม่มี CORE-REQUEST เลขใดถามเรื่อง `npc` มาก่อน (`grep -rli "core-request.*npc" notes_to_chief/` เจอแต่
  เรื่อง `ChooseNPC` ของสาย A ซึ่งเป็นคนละกลไก)

## คำขอ

จุดเสียบหนึ่งจุด (แบบเดียวกับ `CORE-REQUEST-011` ให้ `warp`): ให้ `gm/`-side อ่านสัญญาณได้ว่า
mob_id ที่ผ่าน `is_gm_switchable_npc()` แล้วถูกสั่ง on/off จะกระตุ้นรอบ re-encode/admission รอบเดียวกับ
ที่ `mob_scene_recompose`/`mob_ledger_admission` ทำอยู่แล้วสำหรับมอนที่มีอยู่จริงหรือไม่ -- วิธีเลือก (เรียก
`recompose_frames` ตรงจากจุดใหม่ vs. ผ่าน callback แบบเดียวกับ `CORE-REQUEST-GM-040`) เป็นของ chief ฝั่งนี้
ต้องการแค่จุดอ่านผลลัพธ์หนึ่งจุดที่ `gm/` เรียกได้จากในเขตตัวเอง

## ทำไมยังไม่ทำเอง

`runtime.py` และ `mob_scene_recompose.py`/`mob_ledger_admission.py` ไม่อยู่ใน `src/pirateforce_foundation/gm/`
-- นอกเขตเขียนของสายนี้ตามกฎบ้าน ฝั่งนี้ทำได้แค่ระบุจุดที่มีอยู่แล้วและขอจุดเสียบ

## nonclaim

ใบนี้เป็นคำขอจุดเสียบ ไม่ใช่หลักฐานว่า `npc` ทำงานในเกม -- `npc on|off` ยังคง parse+log เท่านั้นจนกว่าจุดเสียบนี้
จะลง และมีเทส end-to-end พิสูจน์ ไม่มีการเปิด client ไม่มีการวัดกับไคลเอนต์จริงในใบนี้ ทั้งหมดวัดจาก grep/read
บนซอร์สที่ commit แล้วบน `origin/main`

— สาย GM รอบ `5btl0q`
