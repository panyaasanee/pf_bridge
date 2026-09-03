ADDRESSEE: LANE-A
cc: chief, COO, เจ้าของ
ประเภท: ผลเทส attended — สองใบของสาย A ในบูตเดียว ทั้งคู่ตอบแล้ว

`OBSERVER_CONFIRMED: 2026-08-31T10:0x-10:25+07:00` · เจ้าของขับ UI เองทั้งหมด
`BOOT_COMMIT 38b009f61acfd9c09ed3737412fa75ec427b0f87` = main HEAD ไร้แฟล็ก · code-delta 0
วิดีโอเต็มรอบ 3,160 วิ + เฟรมพิสูจน์ 3 ภาพ · canonical DB ไม่ขยับ · teardown PASS

# ① `GT-148` — ไม่มี actor ของ Port Royal ค้างมาในทะเล กลไก clear ทำงาน

## client-observable
เจ้าของออกทะเลกับ Columbus ไปฉาก 17 แล้วรายงานว่า **"ในแมพนั้นไม่มี npc อะไรอยู่"**
⇒ ไม่มี actor ของ Port Royal ค้างข้ามมาแม้แต่ตัวเดียว

## wire — สี่บรรทัดที่ใบขอ ครบทั้งสี่ + บรรทัดที่ chief เพิ่มรอบ R250
```
WORLD_SCENE scene_id=17 seq=0 model=Bg1001 name=a_ship_at_sea spawn=(0.000,0.000,0.000)
            sent_before=NO population=none save=0 marker=0 return_ticket=REQUIRED
SCENE_ENTRY scene=17 xyz=0.000,0.000,0.000 source=PROVISIONAL-OWNER-DECREE-20260827-1445
COLUMBUS_QUEST3021_NO_VEHICLE_DISPATCH scene=17 source=M2-NO-VEHICLE-OWNER-20260827-1525
WORLD_M2_CROSSING_HANDOFF scene=17 kind=clear held=108 composed=YES dispatched=YES
            pc=17B frame=27B slot=before_teleport
            reason=scene_17_left_empty_on_purpose_sea_scene_no_cline_type_mob_set_placements_unresolvable_gt078
WORLD_POP_STOWAWAYS anchor=(0.000,0.000,0.000) held=108 radius=2000.0 within=4
            nearest=Legend_Jack@1226.6 names=Legend_Jack@1226.6,Plato@1646.7,Qina@1915.8,Betula@1935.9
```
🔴 หมายเหตุสำคัญ: `WORLD_POP_STOWAWAYS` ออกมาเป็น **แบบที่มีตัวเลขจริง** (`held=108 within=4 nearest=...`)
ไม่ใช่แบบ `unmeasured reason=call_site_passed_no_legacy` ที่หัวใบเขียนว่าอาจเจอ
⇒ ของ chief ที่ต่อสายไว้ **ลง main แล้วและทำงานจริง**

## สรุป
กลไก clear ยิงก่อน teleport (`slot=before_teleport`) และฉากปลายทางว่างจริงตามที่ตั้งใจ
**สาย A เป็นเจ้าของใบ ปิดหัวใบเองได้**

## 🔴 แต่เจอของใหม่ที่ไม่ใช่ชั้นที่ใบนี้ถาม
**ภาพ/หน้าต่างบทสนทนาของ Columbus ค้างบนจอข้ามฉากมาด้วย** — actor ถูกล้างหมด แต่ชั้น UI ไม่ถูกรีเซ็ต
ยกไปเป็นใบใหม่แล้วในจดหมายถึง chief ฉบับเดียวกันรอบนี้ **ห้ามนับเป็น FAIL ของ `GT-148`**

# ② `GT-165` — 🟢 PASS ทั้งสองชั้น เกาะตลาดทาสมีสิ่งมีชีวิตจริง

## client-observable (สิ่งที่ใบนี้ต้องการ)
เจ้าของเข้าฉาก 4 จริง (แบนเนอร์มุมขวาบน `Slave Market Island`, X=-10,439 Y=22,199) เดินสำรวจแล้วรายงาน:
**"มีสิ่งมีชีวิตหลายตัว ทุกตัวดูเหมือนจะเป็นสิ่งมีชีวิตของที่นี่จริง ๆ · object ดูถูกต้องดี"**
ชื่อที่อ่านได้จากจอ: `Vagabond Messenger` · `Mori Hiroko` · `Mirage reel` · `Slave Market Bulletin Bo...`
**ทุกตัวชื่อสีเขียว เป็นมิตร**

## wire — ตรงกับเกณฑ์ในใบเป๊ะ
```
WORLD_SCENE scene_id=4 seq=0 model=BG0004 name=Slave_Market_Island
            spawn=(-19076.000,17634.000,1440.000) sent_before=NO population=bg0004_roster
WORLD_CENSUS_BG0004 assembled=109/116 shippable=109 wire=109 bodies=ok
            pc=18983B frame=18997B source=bg0004_full_roster shortfall=identity_unresolved=7
WORLD_POP_HANDOFF scene=4 kind=census actors=109 wire=109 slot=after_teleport
```
ใบเขียนไว้ว่าต้องเห็น `assembled=109/116` — **ได้ตรงตัวเลข**

## สองอย่างที่ใบทำนายไว้ล่วงหน้าและเกิดจริง (ไม่ใช่ FAIL)
1. **ชื่อเขียวทุกตัว ไม่ก้าวร้าว** → `MOB_CENSUS_HOSTILITY scene_id=4 scene=? roster=0 backed=0`
   ฉากนี้ไม่มี combat roster เลย ตรงกับ docstring ของ `world_population_bg0004.py` ที่ตั้งใจไม่ส่ง faction bit
   **ช่องว่างเดียวกับฉาก 14** (`GT-134`) — ถ้าจะให้ตีได้ ต้องมีคนต่อ roster ให้ทั้งสองฉาก
2. **ไม่ตกพื้น ไม่หลุดขอบ** → `WORLD_SCENE_RELOCATED scene_id=4 reason=no_pinned_ground_for_scene
   stored=(684.221,-598.593,746.000) used=(-19076.000,17634.000,1440.000)`
   ระบบย้ายจุดเกิดให้เอง จุด `MARKER[4]` ที่ใบเตือนว่าห่าง 777.5 หน่วยไม่ได้ถูกใช้

## 7 ตัวที่ไม่ได้ส่ง — มีเหตุผลระบุครบทุกตัว
`placement=0` ไม่มีแถว `CONSTDATA_MOBS` (MOBS_TIP เรียกมันว่า Port_transportation) ·
`placement=84..89` (set 101-106, n_ID 10014-10019) แถว MOBS ไม่มี `s_OUTFIT` avatar template

# nonclaims
1. ไม่นับจำนวน actor ให้ครบ 109 — ใบเขียนเองว่านับคร่าว ๆ พอ
2. ไม่อ้างว่าตัวไหนคือ n_ID ไหน — ไม่ได้คลิกตรวจ identity สักตัว
3. ไม่อ้างว่าตีได้/ตีไม่ได้ — `roster=0` เป็นข้อเท็จจริงฝั่ง wire ไม่ได้ทดลองโจมตี
4. 🔴 ระหว่างอยู่ฉาก 4 ไคลเอนต์ขึ้น "ยังไม่สามารถรับข้อมูล Server ได้ 17/18/19 วิ" เป็นระยะ แต่ยังเล่นต่อได้
   เฟรมสำมะโนของฉากนี้ = **18,997 ไบต์** ⇒ เป็นข้อมูลจุดที่สามของอาการเฟรมใหญ่
   (รายละเอียดในจดหมายถึง chief รอบเดียวกัน) — **ไม่กระทบผล PASS ของใบนี้** แต่ต้องจดไว้

— กะ1-A (ผู้เทส attended)
