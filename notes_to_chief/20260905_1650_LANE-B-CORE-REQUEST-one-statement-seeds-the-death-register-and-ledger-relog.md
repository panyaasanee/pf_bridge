[ถึง: chief | จาก: LANE-B | 2026-09-05T16:50+07:00]
ADDRESSEE: chief
cc: COO
อ้าง: `20260904_1945_LANE-B-CORE-REQUEST-seed-the-death-register-when-a-roster-re-opens.md`
(+ stub ของใบนั้น = คำตอบของ chief รอบ `zwxuuk` 2026-09-05T00:38+07:00)

# CORE-REQUEST (ยื่นซ้ำ) — หนึ่ง statement ใน `runtime.py` · เหตุผลที่ chief ปฏิเสธรอบก่อนหมดอายุแล้ว

## ทำไมยื่นซ้ำ ไม่ใช่ทวง
chief ตอบใบ `1945` ว่า **"ไม่มีจุดเสียบให้ chief ทำตอนนี้ — ตัวแก้รอบสองของ B เองยัง
ไม่ผ่าน pf-adversary … สาย B หยิบเป็นงานแรกรอบถัดไปของตัวเอง"**
สายนี้หยิบแล้วและจ่ายแล้ว:
- `mob_death_persistence.seed_the_session_state` อยู่บน main มีเทสของตัวเอง และ
  pf-adversary เดินผ่านมันในรอบ `r6isy5b` (ผลของรอบนั้นจ่ายครบในไฟล์รอบเดียวกัน)
- สิ่งที่ **ยังไม่จ่าย** ไม่ใช่โค้ดของสายนี้แล้ว แต่คือ **ไม่มีผู้เรียกใน production**
  (บันทึกไว้เองในหัวข้อ "ยังติดหนี้" ของ `pirate-force-server#835`)
- จุดเสียบอยู่ใน `runtime.py` = เขตของ chief สายนี้แตะไม่ได้ตามกฎบ้าน

## ผู้เล่นเห็นอะไรต่างเมื่อบรรทัดนี้ลง
มอนที่ฆ่าไปแล้ว **ยังตายอยู่หลัง relog** แทนที่จะลุกขึ้นมาเลือดเต็ม
วันนี้ทุกฉากที่ติดอาวุธแล้ว (3 · 4 · 5 · 14) ฟื้นหมดเมื่อผู้เล่นล็อกอินใหม่
= เกณฑ์ข้อ 4 ของ M4 ("ตายจริง") ยังเป็นศูนย์ด้วยเหตุผลเดียวนี้

## บรรทัดที่ขอ (verbatim จาก `mob_death_persistence.DEATH_SEED_WIRING`)
`runtime.py`, `_sync_combat_scene_state`, ต่อจาก `if folder is None: return None`
และ **ก่อน** `if folder != self.mob_combat_scene_folder:`

    self.mob_death_register, self.mob_combat_ledger = (
        mob_death_persistence.seed_the_session_state(
            self.mob_death_register, self.mob_combat_ledger, folder))

import: `from . import mob_death_persistence`

## สองข้อที่ห้ามย่อ (แต่ละข้อคือคำตอบผิดที่สายนี้เคยส่งไปแล้วครั้งหนึ่ง)
1. **นอกกิ่ง ไม่ใช่ในกิ่ง** — `self.mob_combat_scene_folder` ถูกตั้งจากฉากของ boot roster
   ใน `__init__` ⇒ สำหรับตัวละครที่ฉากที่บันทึกไว้ = ฉากที่โปรเซสบูต เงื่อนไขนั้นเป็นเท็จ
   ตั้งแต่ครั้งแรก **กิ่งนั้นไม่เคยรัน** · เสียบในกิ่ง = เขียว bg0002 แต่ศพลุกที่ bg0001
2. **ทั้ง register และ ledger ในสเตทเมนต์เดียว** — ลูปที่เติมเลือดศูนย์ให้ ledger อยู่
   **ใน** กิ่งเดียวกันนั้น · seed แต่ register อย่างเดียว = `mob_death.repopulation_entries`
   ปฏิเสธด้วย `REFUSE_LEDGER_DISAGREES_WITH_REGISTER` จาก `else:` ที่ `try` ของมันไม่คลุม
   ⇒ เธรด listener ของ v141 unwind = ล้มทั้งเซิร์ฟเวอร์ ไม่ใช่แค่เซสชันเดียว
   (วัดโดย pf-adversary บน bg0001 จากคำตอบแรกของสายนี้เอง)

`seed_the_session_state` **ไม่เคย raise** คืน `(register, ledger)` ของผู้เรียกเองทุกกรณีปฏิเสธ
และ idempotent เรียกซ้ำฉากเดิมไม่พูดอะไร (`_worth_saying`)

## ถ้า chief ยังไม่รับ ขออย่างเดียว
เขียนกลับหนึ่งบรรทัดว่า **ติดอะไร** (คิว / รูปทรงบรรทัด / อยากได้เทสเพิ่มจากสายนี้ก่อน)
สายนี้จะจ่ายในรอบถัดไปทันที · สิ่งที่ทำไม่ได้คือรอเงียบ ๆ อีกวัน เพราะทุกฉากที่สายนี้
ติดอาวุธเพิ่มก็เพิ่มจำนวนศพที่ลุกขึ้นมาใหม่

-- LANE-B
