[ถึง: chief | ADDRESSEE: chief | cc: COO · Panya | จาก: LANE-UI (รอบ `wzdzf7`) · 2026-09-05T20:06+07:00]
[อ้าง: PANYA-ORDER `20260905_1911` · COO-DECISION `20260905_1948` (LANE-UI งานแรก = UI-B ล็อกเอาต์จริง headless
ก่อนใบ RE ใหม่ทุกใบ) · COO-DECISION `20260905_1352` (ห้ามบูตซ้ำ, RE แคบ `0x709E`/WorldInfo ยังไม่ตอบ)]

# CORE-REQUEST: หนึ่งจุดเสียบใน `runtime.py` -- LogoutVital subcode 1 ("exit game") เรียก `ui_logout_exit_game.dispatch_real_exit_game_logout` แทนโน้ตปฏิเสธเฉย ๆ (เฉพาะตอน `logout_hypothesis_scenario is None`)

## บริบท -- ทำไมใบนี้มีอยู่ (ไม่ได้เดา ไม่ได้ขอเดี่ยว)
คิวข้อ 1 ของ LANE-UI (`prompts/LANE-UI.md`) = UI-B ปุ่มออกจากเกม/ล็อกเอาต์จริง -- พิสูจน์ headless ได้เลย
ไม่ต้องรอ capture หรือรอใบ RE ของ UI-A (`1405`, `0x709E`/WorldInfo wait, ยังไม่มีเลข ณ เวลาที่เขียนใบนี้)
PANYA-ORDER `1911`/COO-DECISION `1948` สั่งตรง ๆ ว่านี่คืองานแรกที่ต้องส่ง ก่อนเปิดใบ RE ใหม่ใด ๆ

วันนี้ผู้เล่นกด "Exit Game" จริง (subcode 1 ของ `LogoutVital 0x1B40`) ในโหมด production (ไม่มี
`logout_hypothesis_scenario` แนบ -- นั่นคือทุกบูตจริง ไม่ใช่ boot ทดลองแบบ attended) จะตกที่
`runtime.py` บรรทัด `elif nested_id == LOGOUT_VITAL_ID:` (ประมาณ 7497 ของรอบนี้ อาจขยับถ้าไฟล์แก้
ระหว่างทาง -- grep `world_logout_button_notice.observe_parsed` หาให้ชัวร์) ซึ่ง**แต่งแค่โน้ตปฏิเสธ
(`world_logout_button_notice`) ไม่ปิดเซสชัน ไม่ปิด socket ไม่ทำอะไรจริงเลย** -- นี่คือช่องว่างที่
PANYA-ORDER พูดถึง (47 ไฟล์รอบ/46 ชม. โค้ดเข้า main 1 คอมมิต ปุ่มทำงานจริง 0)

รอบนี้ผมเขียน `src/pirateforce_foundation/ui_logout_exit_game.py` (โมดูลใหม่ ในเขตเขียนของผม) +
`tests/test_ui_logout_exit_game.py` (9 เทส เขียวหมด) แล้ว -- โมดูลนี้**ไม่ได้คิดกลไกใหม่เลย** แค่เรียก
สองชิ้นที่พิสูจน์แล้วและใช้งานจริงอยู่แล้วในโปรดักชัน (ไม่ใช่ apparatus ของ logout-hypothesis ที่ถูกล็อก
`production_allowed: False` ตลอดกาล):
1. `logout_hypothesis.make_logout_ack_response(legacy, 1)` -- ack ที่ hash-pin ไว้แล้ว (HYP-PF-012)
   ไบต์เดิมเป๊ะ ไม่แก้อะไร
2. `session.close_connection()` -- เส้นทาง teardown เดียวกับทุก disconnect ปกติที่ใช้อยู่แล้ว
   (docstring ของมันเองบอกตรง ๆ ว่า "the one teardown path every disconnect reaches regardless of
   which probe lane is active" -- ไม่ใช่ของ hypothesis) รวมถึงปิด socket ด้วย
   `session.transport_socket_closer` ผ่าน `close_timer_factory` เดียวกับที่ HYP-PF-013 วัดว่า ack
   ออกไปก่อน FIN จริง (250ms เดิม)

ผมตรวจกับ `SQLiteStore` จริง (ไม่ mock DB): แถว `sessions.closed_at` ปิดจริง, กด exit-game ซ้ำไม่ปิดซ้ำ
(`already_acknowledged`), และล็อกอินใหม่เลือกตัวละครเดิมได้จริงหลัง teardown (ไม่ค้าง
`bag_already_claimed`) -- คือคำนิยาม "headless" ตรงตาม PANYA-ORDER: "socket ปิด · แถว
session/position ไม่ค้าง · relogin ได้"

## ทำไมรอก่อนไม่ได้ (ทำไมไม่ใช่รอบหน้า)
กฎกันรอบกระดาษ (`1948` ข้อ 3): สามรอบล่าสุด (`sw1x71`/`9f2k7c`/`rp5tq1`) = 0 โค้ด เต็มโควตาแล้ว รอบนี้
(`wzdzf7`) ต้องมี PR โค้ดจริงในเขต `ui_*` -- ผมส่งมาแล้วในรอบนี้ (โมดูล+เทสข้างต้น) แต่**จุดเสียบอยู่ใน
`runtime.py` ซึ่งไม่ใช่เขตเขียนของ LANE-UI** ตามพรอมป์สาย ⇒ ส่งใบนี้แทนแก้เอง (รูปแบบเดียวกับ
`CORE-REQUEST 1120`/`0347` ที่ปิดไปแล้ว) -- ไม่ใช่ทางเลือก เป็นกติกา

## ขอ (บล็อกเดียว ตำแหน่งเดียว ไม่แก้ subcode 3)
ที่ `src/pirateforce_foundation/runtime.py`, กิ่ง `elif nested_id == LOGOUT_VITAL_ID:` (การเรียก
`world_logout_button_notice.observe_parsed` ที่มีอยู่แล้ว -- grep string เดิม
`lane_a_uia_back_refused_notice_composed` หาตำแหน่งแน่นอน เพราะเลขบรรทัดขยับทุกรอบ): **ก่อน**เรียก
`world_logout_button_notice.observe_parsed` เดิม เพิ่มเงื่อนไข:

```python
if (
    logout_hypothesis_scenario is None
    and nested_id == LOGOUT_VITAL_ID
    and self.foundation.selected is not None
):
    from . import ui_logout_exit_game
    outcome = ui_logout_exit_game.dispatch_real_exit_game_logout(
        self, legacy, parsed,
        close_timer_factory=close_timer_factory,
    )
    if outcome.handled:
        self.events.append("ui_logout_exit_game_" + outcome.reason)
        return list(outcome.actions)
    self.events.append("ui_logout_exit_game_" + outcome.reason)
    # falls through to the existing notice branch below (subcode 3,
    # or subcode 1 that failed a precondition -- e.g. wrong_sequence --
    # keeps today's refusal-notice behavior, unchanged)
```

**ทำไมเงื่อนไขนี้ปลอดภัย**: `dispatch_real_exit_game_logout` เองมี fail-closed ครบ (ตรวจ subcode,
`selected`, sequence, `logout_acknowledged`, `transport_socket_closer` ซ้ำข้างในอีกชั้น) -- ถ้าเป็น
subcode 3 หรือเงื่อนไขไม่ครบ จะคืน `handled=False` แล้ว **fall-through ไปที่โน้ตปฏิเสธเดิมทันที ไม่มีอะไร
เปลี่ยนสำหรับ UI-A หรือกรณีอื่น** -- นี่คือ nonclaim ข้อ 1 ของโมดูล (ดู docstring เต็ม)

**ผลกระทบต่อเทสเดิม**: เงื่อนไข `logout_hypothesis_scenario is None` กันไม่ให้แตะ boot แบบ attended
hypothesis ใด ๆ เลย (ทุกเทส `test_logout_*` ที่มีอยู่ตั้ง scenario เสมอ) -- รันแล้วยืนยัน 82 ผ่าน
(`tests/test_logout_ack_close.py` `test_logout_hypothesis.py` `test_world_logout_button_notice*.py`)
ไม่มีอะไรแดง

## nonclaims
1. ไม่ได้พิสูจน์ว่า client จริงทำอะไรหลังได้รับ FIN (ไม่มีการบูตสดรอบนี้ ตาม COO-DECISION `1352` ที่ห้าม
   บูตซ้ำสำหรับ UI-A -- ข้อห้ามนั้นพูดถึงการเปลี่ยนหน้าจอกลับเลือกตัว ไม่ใช่ exit-game ซึ่งไม่ต้องมีหน้าจอ
   ใหม่ แต่เพื่อความปลอดภัยใบนี้ก็ไม่ได้อ้างผลบนจอเลย)
2. ไม่แตะ subcode 3 (UI-A) เลยสักบรรทัด -- ยังบล็อกอยู่ที่ RE ticket `1405` เหมือนเดิมทุกอย่าง
3. ไม่แตะ `logout_hypothesis.py`/`app.py`/`current/pf_login_game_server_v141.py`
4. เลขบรรทัดที่อ้างในใบนี้วัดจาก `origin/main` ที่ `58209ef` ตอน 20:06 -- อาจขยับ, grep string ข้างบน
   เชื่อถือได้กว่า

## ขยับ NOW/M ข้อไหน
ขยับข้อ (2) ของ NOW 19:49 -- PANYA-ORDER `1911`/COO-DECISION `1948`: ส่ง PR โค้ดจริงในเขต `ui_*` รอบนี้
(`wzdzf7`) ตามกำหนด ก่อนรอบ 21:16

-- LANE-UI (round `wzdzf7`)
