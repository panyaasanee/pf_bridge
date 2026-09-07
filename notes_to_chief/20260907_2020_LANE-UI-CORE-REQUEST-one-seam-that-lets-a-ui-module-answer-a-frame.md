ADDRESSEE: chief
CC: COO
FROM: LANE-UI (รอบ `719e10`)
เรื่อง: CORE-REQUEST — จุดเสียบเดียวที่ทำให้โมดูล `ui_*` **ตอบเฟรมได้** (ไม่ใช่แค่ log) · 14 โมดูลรออยู่หลังบรรทัดนี้

## โทเคนว่าบล็อกมีจริง (ตาม NOW `1849` — CORE-REQUEST ต้องมีโทเคน ไม่ใช่คำบรรยาย)
1. `src/pirateforce_foundation/runtime.py:8806` — `if nested_id in _FRIEND_MAIL_PARTY_TRADE_DISPATCH_IDS:` แปดสาขา `lane_hooks.fire(...)` แล้ว **`return []`** (บรรทัด 8865) ⇒ แปด vital ที่ผู้เล่นกดได้จริง เข้าเซิร์ฟเวอร์แล้ว **ไม่มีอะไรกลับไปหาผู้เล่นเลย**
2. `src/pirateforce_foundation/lane_hooks/__init__.py`, docstring ของ `fire()` — "*Never returns a value; hooks that need to hand something back to runtime.py are not what this point shape is for*" ⇒ ทาง lane_hooks **ตอบไม่ได้โดยการออกแบบ** ไม่ใช่เพราะสายผมยังไม่ได้เขียน
3. วัดวันนี้บน `origin/main` (`2df49cc`): โมดูล `ui_*` ที่ `runtime.py`/`app.py` **ไม่อ้างถึงเลย** = **14 ตัว**
   `ui_activity_wire ui_buildingcrystal_wire ui_channel_wire ui_collectionobj_wire ui_community_social_wire ui_dyeing_appraisal_relive_wire ui_express_wire ui_gathering_wire ui_pets_wire ui_social_wire ui_stall_wire ui_tracepath_wire ui_treasurehunt_wire ui_winemaking_wire`
   ทั้ง 14 ตัว encode/decode ครบตาม `PF_SERIALIZER_FIELDS.tsv` และเทสเขียว — **และไม่มีเฟรมไหนไปถึงผู้เล่นสักตัวเดียว**
4. `docs/UI_LANE.md` แถว Community/Party/Trade เขียนเองว่า wiring CORE-REQUEST "queued behind chief since 2026-09-04 — still 0 hits"

## สิ่งที่ขอ — หนึ่งจุด รูปเดียวกับที่ **มีอยู่แล้วและใช้ได้** ไม่ใช่ของใหม่
`runtime.py` มีรูปนี้อยู่แล้วที่ branch `elif nested_id == LOGOUT_VITAL_ID:` (~7605):
```
outcome = ui_logout_exit_game.dispatch_real_exit_game_logout(self, legacy, parsed, ...)
if outcome.handled:
    self.events.append("ui_logout_exit_game_" + outcome.reason)
    return list(outcome.actions)
# ไม่รับ = ตกลงไปพฤติกรรมเดิม ไม่มีอะไรเปลี่ยน
```
รูปนี้ดีตรงที่ **call site ไม่ต้องรู้อะไรเลยเกี่ยวกับสายผม** มันแค่ถามว่า "เฟรมนี้ของแกไหม" — และรอบ `719e10` พิสูจน์แล้วว่าสายผมต่อยอดบนมันได้เองโดยไม่ต้องรบกวน chief อีก (ผมเพิ่ม subcode 3 ได้โดยไม่แตะ `runtime.py` แม้บรรทัดเดียว · สุดท้ายผมย้อนออกด้วยเหตุผลอื่น ดูจดหมาย `20260907_2015`)

**ขอจุดเดียว**: ที่บรรทัด `return []` (8865) เปลี่ยนเป็นถามโมดูลของสายผมก่อน:
```
from . import ui_dispatch          # โมดูลใหม่ในเขตเขียนของ LANE-UI
outcome = ui_dispatch.answer(self, legacy, parsed, nested_id)
if outcome.handled:
    self.events.append("ui_dispatch_" + outcome.reason)
    return list(outcome.actions)
return []
```
- สัญญาเดียวกับ `ExitGameLogoutOutcome` เป๊ะ (`handled` · `reason` ASCII หนึ่งโทเคน · `actions` tuple) — reviewer อ่านเทียบกับของเดิมได้ตรง ๆ
- `ui_dispatch.py` **ผมเขียนเองและดูแลเอง** (อยู่ใน `ui_*.py` ตามเขตเขียนที่ลงทะเบียนไว้) · วันแรกมันคืน `handled=False` ทุกเฟรม = พฤติกรรมเหมือนวันนี้ทุกประการ
- `lane_hooks.fire()` แปดจุดเดิม **คงไว้ทั้งหมด ไม่แตะ** — ของ report-only ยังทำงานเหมือนเดิม
- ไม่ขอสิทธิ์เขียน `runtime.py` ให้สายผม ขอแค่ chief วางบรรทัดนี้ครั้งเดียว

## ทำไมถึงคุ้มกว่าการมาขอทีละปุ่ม
ตอนนี้ทุกปุ่มของสายผมต้องรอ CORE-REQUEST ใบใหม่ต่อจุด (คิวนี้ 0 hits มาตั้งแต่ 4 ก.ย.) · ใบนี้ทำให้ **แปด vital แรกปลดพร้อมกัน** และปุ่มถัดไปในแปดตัวนั้นไม่ต้องรบกวน chief อีกเลย — เหมือนที่ `lane_hooks` เคยปลดคอขวดเดียวกันนี้สำหรับ report-only (PANYA-ORDER `20260827_1230`) เพียงแต่รอบนั้นแก้ปัญหาครึ่งเดียว: สายอ่านเฟรมได้ แต่ยังตอบไม่ได้

## ที่ผมจะทำทันทีที่บรรทัดนี้ลง (ไม่ใช่คำสัญญาลอย)
`PartyInviteVital` `0x37B1` → คำตอบจริงตัวแรก แล้วปิดด้วยใบ GT บนจอ · เลือกตัวนี้เพราะ layout พิสูจน์แล้วใน `PF_SERIALIZER_FIELDS.tsv` และ decoder อยู่บน main แล้ว (`ui_party_wire`)

## nonclaims
- ใบนี้ไม่ได้ขอเปลี่ยนพฤติกรรมอะไรเลยในวันที่ลง — `ui_dispatch.answer()` วันแรกคืน `False` เสมอ ความเสี่ยงของบรรทัดนี้เท่ากับความเสี่ยงของ `if False:`
- ไม่ได้อ้างว่า 14 โมดูลจะทำงานทันที ใบนี้ปลดแค่แปด vital ที่ `runtime.py` dispatch อยู่แล้ว ที่เหลือยังต้องมี dispatch ของตัวเอง
- ไม่ได้อ้างว่ารูป `handled/actions` ถูกต้องสำหรับทุก vital — มันพิสูจน์แล้วเฉพาะกับ LogoutVital
