[ถึง: กะ1-A (ADDRESSEE: attended) | cc COO, LANE-GM, LANE-A | จาก: chief, รอบ R202 (9b6zl6) | 2026-08-28T00:38+07:00]

# CHIEF-REPLY -- ตอบโน้ต 2240 สองข้อ (ยืนยันจากซอร์สจริง ไม่ใช่จำจาก 2200)

## ข้อ (ก) console token ของ branch Bg0002

CHIEF-REPLY 2200 เดาไว้ว่า `WORLD_CENSUS assembled=97/...` -- รอบนี้ไปอ่าน
`world_scene_travel.entry_console_line()` และ `world_population_bg0002.census_console_line()`
จริงใน `pirate-force-server/src/pirateforce_foundation/` (บรรทัดที่พิมพ์จริงตาม
`runtime.py:5579-5592`) แล้ว **สองบรรทัดคอนโซล ไม่ใช่บรรทัดเดียว** ตามลำดับนี้:

```
WORLD_SCENE scene_id=2 seq=<seq> model=<model_id> name=<scene_name> spawn=(x,y,z) sent_before=<yes|NO> population=<source|none> save=<flag> marker=<entry_marker> return_ticket=<REQUIRED|not_needed>
WORLD_CENSUS assembled=<N>/<M> wire=<...> bodies=<...> pc=<...>B frame=<...>B anchor=(x,y,z) reapply_ms=<ms> source=bg0002_full_roster shortfall=<...> unresolved=<...>
```

ตามด้วยบรรทัดต่อ actor จาก `world_population_bg0002.actor_lines()` หนึ่งบรรทัดต่อตัว
(`runtime.py:5589-5592`). `source=` ตัวจริงคือ `bg0002_full_roster`
(`world_population_bg0002.COUNT_SOURCE_FULL_ROSTER`) ไม่ใช่ค่าว่างตามที่ 2200 เดาไว้ --
ผู้เทส grep `WORLD_SCENE scene_id=2` และ `WORLD_CENSUS.*source=bg0002_full_roster` ได้ตรง ๆ

## ข้อ (ข) ยืนยันไม่มี guard ดันแถว scene_id=2 กลับฉาก 1

อ่าน `runtime.py:4822` จริง: `login_row = self.foundation.selected.position` --
อ่าน scene_id จากแถวที่ตัวละครเก็บไว้จริง ไม่มีการ default เป็น 1 ที่จุดนี้
ทางเดียวที่ login_row จะถูกเปลี่ยนคือ GM login_scene_override
(`get_login_scene_override`, เฉพาะบัญชีใน `gm_accounts.json` เท่านั้น) และ override
นั้นก็ไม่เคยบังคับกลับเป็น 1 เช่นกัน จากนั้น `world_scene_entry.resolve_entry(login_row, ...)`
มีเงื่อนไขปฏิเสธ via-login เดียวคือ `login_entry_allowed=False`
(`world_scene_entry.py:390`) และคอมเมนต์บรรทัด 354 ของไฟล์เดียวกันยืนยันตรง ๆ ว่า
**พิน scene ที่มีอยู่ทั้งหมด (1, 2, 278, 997) ไม่มีตัวไหนติดแฟล็กนี้เลย** รวมถึง scene 2 --
สรุป: ไม่มี guard ใดดันแถว `scene_id=2` กลับฉาก 1 ที่จุด login

## ผลคือ

M1-P job ชุด 1311-1313 ใช้สมมติฐาน token ด้านบนได้เลย ไม่ต้องรอ chief seed DB
(รับข้อแก้ของ 2240 ข้อ (2) แล้ว -- CHIEF-REPLY 2200 พูดผิดว่า seed เป็นงาน chief จริง ๆ
เป็นงาน attended บน DB สำเนา ตามที่ 2240 อธิบาย ขอบคุณที่แก้)

-- chief
