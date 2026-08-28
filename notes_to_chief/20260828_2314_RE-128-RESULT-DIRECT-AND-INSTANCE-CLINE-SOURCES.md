[ถึง: LANE-A · COO · chief · cc Panya | จาก: RE runner local · 2026-08-28T23:14+07:00]

# RE-128 RESULT — PASS/DONE · ปิดเส้นเลือก CLINE ทั้ง `SCENE_NAME` และ `INSTANCE`

- ใบ: `RE-128 SCENE-ORDINAL-TO-MOBS-NID-TABLE-LOCATION-001 [STATIC-ON-BRIDGE]`
- START: `2026-08-28T23:02:29.759+07:00`
- เหตุที่หยิบซ้ำ: หลังผลเดิม 19:12 หัวใบถูกแก้เป็น “ยังไม่ปิด” + ส่งมือให้ RE runner และ COO 22:50 ระบุเป้าหมาย “crosswalk ของฉากอื่นนอกฉาก 2” ชัดเจน จึงเข้าเงื่อนไข objective/jobs เปลี่ยนหลัง result เดิม
- วิธี: static/read-only เท่านั้น; ไม่เปิดเกม/เซิร์ฟเวอร์, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB/source/queue/git
- verdict: **PASS/DONE** — ตัว client เลือก `n_CLINE_TYPE` สองทางจริง: ฉากปกติอ่านจาก `SCENE_NAME`; ฉาก instance อ่านจาก `INSTANCE` ด้วย instance id ที่ active อยู่ แล้วใช้ `(n_CLINE_TYPE,n_CREATURE_TYPE)` เข้า `CLINE` เหมือนกัน

## ค้นก่อนถอด + input pins

- **ค้นใน `pf_bridge\external\` แล้ว: ไม่เจอ CLINE crosswalk.** ค้น `PF_PROTOCOL_REGISTRY.tsv` และ `PF_SERIALIZER_FIELDS.tsv` ด้วย `CLINE|n_CLINE_TYPE|n_CREATURE_TYPE|SCENE_NAME|INSTANCE`; เจอเพียงตระกูล wire `Instance*`/`NavigationEx_EnterInstanceVital` ที่ไม่ใช่ table selector นี้. ขอบเขตทั้ง tree = 30 ไฟล์ / 29,900,221 ไบต์ / fingerprint `9c18df7c...2d882`.
- **ค้น `gamedata` แล้ว: เจอคำตอบ.** `PF_GAMEDATA_INDEX.tsv`/`PF_GAMEDATA_COLUMNS.tsv` พิน `SCENE_NAME.n_CLINE_TYPE`, `CLINE.(n_CLINE_TYPE,n_CREATURE_TYPE)` และ `INSTANCE.(n_SCENE_ID,n_CLINE_TYPE)`. ขอบเขตทั้ง tree = 1,109 ไฟล์ / 15,319,585 ไบต์ / fingerprint `d3031fac...63549`.
- SHA หลัก: image `96272114...8b623`; `SCENE_NAME` `e38114a8...5d60b`; `CLINE` `aa4a55b8...dc40`; `INSTANCE` `e3b54a19...58f4`; `MOBS` `3c0d33d6...3916b`; `MOBS_TIP` `e25ac667...ce38f`.
- ผลเดิม `20260828_1912_RE-128-RESULT-CLINE-CROSSWALK-PINNED.md` SHA `f6bb419e...49a89` ตรง; rerun verifier เดิม PASS 41/41 ก่อนต่อยอด

## T1 — เส้นเลือก CLINE นอกฉาก 2

ช่วง binary `[0x0043AA16,0x0043AAA4)` SHA `b0b453fb...96117` แยกสอง branch:

1. ถ้า active instance pointer เป็นศูนย์: เปิด literal `SCENE_NAME`, อ่าน literal `n_CLINE_TYPE` ที่ `0x0043AA51..0x0043AA67`.
2. ถ้ามี active instance id ที่ `[...+0x40]`: เปิด literal `INSTANCE` ที่ `0x0043AA72`, lookup แถวด้วย id นั้น แล้วอ่าน literal `n_CLINE_TYPE` ที่ `0x0043AA89..0x0043AAA0`.

นี่ไม่ใช่การจับคู่เพราะเลขเท่ากัน: `SCENE_NAME` มี direct selector ที่มี CLINE rows 19 ฉาก; อีก **240 ฉาก** ที่ `SCENE_NAME.n_CLINE_TYPE=0xFFFFFFFF` มี selector จริงผ่าน `INSTANCE`. ตัวคุมที่อยู่นอกฉาก 2:

- scene 1 ใช้ direct `SCENE_NAME.n_CLINE_TYPE=1` (ผลเดิมพิสูจน์ native consumer แล้ว)
- scene 17 / `Bg1001` ใช้ instance-specific selectors: instance `109→CLINE 801`, `122→814`, `124→816`; จึงห้าม flatten scene 17 เป็น CLINE type เดียวโดยไม่รู้ active instance

artifact สำรวจครบ 271 scene rows: `staged/re128_scene_cline_sources.tsv` SHA `b95ede96...ca22`.

## T2 — หนึ่ง definition/placement ให้ leader หรือ crew

ช่วง loop `[0x0043A83E,0x0043A968)` SHA `42cf0ab8...b0bd2` iterate **9 field** ตรง ๆ (`n_LEADER_BK1..3` + `n_CREW1..6`) และสร้าง output record แยกต่อค่า nonzero ที่ผ่าน helper; ไม่ได้เลือก leader ช่องเดียวตายตัว. ตัวอย่าง scene 1 template 88 มี candidate 7 ตัว: leader `899` + crew `8601,8611,8617,8626,8629,8647`.

ขอบเขตสำคัญ: output นี้คือ **map-NPC/list consumer** ที่พิสูจน์ใน image ไม่ใช่หลักฐานว่า original server spawn actor runtime กี่ตัวหรือมองเห็นกี่ตัว.

## T3 — `Port transportation`

ค่า `155` มีใน `MOBS_TIP` แต่ไม่มีใน `CONSTDATA_TH__MOBS.tsv`; helper `[0x0043A120,0x0043A356)` SHA `49cd24c7...f6315` ต้อง resolve MOBS row ก่อนสร้าง output ⇒ **155 ไม่ผ่านและไม่ถูกเพิ่มใน map-list path นี้**.

นี่ตัดได้เฉพาะ consumer นี้: ไม่ประกาศ semantic ระดับโลกว่า 155 เป็น “ตัวคั่น” และไม่พิสูจน์ว่า runtime spawn path อื่นสร้าง/ไม่สร้างมัน.

## verifier / integrity

- `staged/re128_scene_cline_sources_static.py` SHA `256dabed...1e387`: PASS 22/22 สองรอบ, output byte-identical `b95ede96...ca22`, source pins หลังงานตรงก่อนงานทั้งหมด
- verifier เดิม `re128_scene_ordinal_crosswalk_static.py` PASS 41/41; image span/field literals/scene 1+2 controls ตรงเดิม

## nonclaims

1. ไม่ claim ว่า CLINE output ทุกตัว spawn หรือ visible ใน runtime; วัด static map-list consumer เท่านั้น.
2. ไม่ claim ว่า scene id เดียวเลือก instance ใดโดยอัตโนมัติ; scene 17 มีอย่างน้อยสาม instance selectors และต้องมี runtime/call-site context จึงเลือกค่าถูก.
3. ไม่ claim ว่า 240 ฉากทั้งหมดมี raw `.npc` definition ที่เข้ากับ selector ทุก instance; artifact พินเฉพาะ table crosswalk/branch ที่วัดได้.
4. ไม่ claim ว่า `Port transportation` เป็น separator ในทุกระบบ; รู้เพียงถูกกรองใน path นี้เพราะไม่มี MOBS row.
5. สูตร/เลขคณิตที่โปรเจกต์ใช้ประกอบ roster เป็นดีไซน์ของเรา ไม่ใช่ข้อเท็จจริงของเซิร์ฟเวอร์ต้นฉบับ.

## BUILD_IMPACT

**BUILD_IMPACT:** สาย A สร้าง roster/map-list ได้โดยเลือก selector ตาม branch จริง: direct scene ใช้ `SCENE_NAME.n_CLINE_TYPE`; instance scene ใช้ `INSTANCE.n_CLINE_TYPE` ของ active instance แล้ว join CLINE. สำหรับ scene 17 ต้องเก็บ instance id เป็น input ห้าม hardcode CLINE type เดียว; actor-spawn policy ยังเป็นใบ/หลักฐานคนละชั้น.

`BUILD_IMPACT_NONE: 0/1`

สถานะที่ควรกรอก: `RE-128 PASS/DONE — DIRECT+INSTANCE CLINE SELECTORS PINNED`.
