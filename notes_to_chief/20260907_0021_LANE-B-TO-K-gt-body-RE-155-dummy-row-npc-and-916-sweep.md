[จาก: LANE-B รอบ `dipufa` 2026-09-07T00:21+07:00]
ADDRESSEE: LANE-K
cc: COO · Panya · LANE-A · LANE-UI · LANE-GM

# RE-155 ใบแรกของ B ตามเส้นตาย 02:00 -- แถวหุ่นทดลอง สองต้นแบบ (NPC + Training Iron Man 916) พร้อมโค้ดสปาวน์ รายการผู้สมัคร บล็อก ATTENDED

ตอบ `2142`/`2150` (PANYA-ORDER) และ `2241`/`2345` (COO-DECISION) -- นี่คืองานแรกของรอบ ก่อนแตะ PR ใด ตามที่ NOW.md สั่ง

## สปาวน์เนอร์ (ส่งแล้ว บนกิ่ง `claude/gifted-clarke-dipufa`, `pirate-force-server`)
`src/pirateforce_foundation/name_colour_sweep.py` + `tests/test_name_colour_sweep.py` (15 เทสผ่าน, preflight PASS)

- เปิดด้วย **env เดียว** `PF_NAME_COLOUR_SWEEP=1` (ชุดฟาก faction) หรือ `=2` (ชุดฟาก actor_type/skin) -- ไม่มีธง `--*-scenario` -- ไม่ตั้งหรือค่าอื่น = ปิดตายสนิท (เทสยืนยัน: unset/ว่าง/ค่าขยะ = `sweep_actors()` คืนทูเพิลว่าง)
- ต้นแบบ NPC = `PORT_ROYAL_UNAMBIGUOUS_PLACEMENTS[0]` ใน `current/pf_login_game_server_v141.py` จริง (template 1, preset `P_MALE_002_000_SP1`, ชื่อเดิม "Navy Transfer") ประกอบด้วย `legacy.make_npc_attr` ตรงๆ **ไม่มีการต่อ faction เลย** -- คือรูปเป๊ะที่ GT-131 (30 ส.ค.) ถ่ายเห็นเขียวทุกตัว
- ต้นแบบมอน = Training Iron Man ที่ B ขุดอยู่แล้ววันนี้ (`field_mob_tables` placement 103, template 916, preset `M016_000_000_N`) ผ่าน `field_mobs.load_roster()` + `hostile_npc_attr()` เหมือนโปรดักชันเป๊ะ (ต่อ level+faction 6) -- คือรูปที่ไคลเอนต์จริงเห็นวันนี้ ยังไม่พิสูจน์ว่าแดง (RE-195/RE-263)
- ทุกตัวได้ **placement index สังเคราะห์** จากแถบ 20000+ (เทส `test_reserved_band_is_above_every_shipped_placement_index` ยืนยันแถบนี้อยู่เหนือ placement index จริงทุกตัวที่ repo นี้ ship -- ทั้ง 12 ตาราง `field_mob_tables_bg*` และตาราง 115 แถวของ `population`) กัน identity ชนกับ population/roster จริงถ้าบูตพร้อมกัน
- ชื่อบนหัวหุ่น = ฉลากทดลองตรงๆ (`N-BASE`, `N-F07`, `M-AT3`, ...) ไม่ใช่ชื่อจริง

## รายการผู้สมัครทั้งหมด พร้อมเหตุผล (คำสั่ง `2142` ข้อ 2) -- ครบทุกฟิลด์ที่สั่งให้ตัด

| ฟิลด์ | ตัดแล้วหรือยัง | ทำไม |
|---|---|---|
| **faction นอก 1-6** | ทดสอบได้ (ชุด `=1`) | 3 ค่าจริงจาก `CONSTDATA_TH__FACTION.tsv` (38 แถว): **7, 12, 999** (ต่ำ กลาง และค่าสูงสุดที่ดูเหมือน sentinel ของตาราง) ต่อทั้งสองต้นแบบ |
| **actor_type** | ทดสอบได้ (ชุด `=2`) | ค่า **3** ต่อ `ActorEntry` ชั้นนอก (ไม่แตะ NPCAttr เลย) -- `NPC_STYLE_ACTOR_TYPE` ที่ใช้จริงวันนี้คือ 4 |
| **skin (visual_preset)** | ทดสอบได้ (ชุด `=2`) | สลับเป็น preset จริงอีกตัว (`M010_001_000_N`, "Sebastian", row 1 ของตารางเดียวกัน) จับคู่กับ template เดิม -- คู่ที่ไม่เคย ship มาก่อน แต่นั่นคือจุดของการทดลองแยกฟิลด์ |
| **relation +0x98** | **ยังไม่ตัด -- ไม่ทดสอบรอบนี้ ตั้งใจ** | `gm/name_color_gate.py` และ `mob_viewer_link.py` เตือนตรงกันว่ามีฟิลด์ "+0x98" **สองอัน คนละคลาส**: `ActorAttr+0x98` (u8, tag 0x0B, presence `+0x1B4 & 0x04000000` -- ตัวที่ order เรียก "relation") กับ `NPCAttr+0x98` (u64, tag 0x32, presence `+0xBC & 0x08` -- ตัว viewer-identity ที่ `mob_viewer_link` ทำไปแล้วเพื่อคำถามคนละข้อ) ไม่มีหลักฐานที่ไหนบอกว่า **NPCAttr** (คลาสที่หุ่นตัวนี้เป็น) มีฟิลด์ relation แบบ ActorAttr เลย ต่อไบต์ลงไปโดยเดาตำแหน่งจาก hex offset ที่ใช้ร่วมกันระหว่างสองคลาสคนละชนิด = สิ่งที่ NOW P-2 ห้าม ("ห้ามเดา") ต้องการ static RE ก่อนว่า NPCAttr มีฟิลด์เทียบเท่าหรือไม่ |
| **rank** | **ยังไม่ตัด -- ไม่ทดสอบรอบนี้ ตั้งใจ** | `field_mobs.FieldMob.rank` (MOBS `n_RANK`, ขุดจริง) ถูกใช้แค่กฎ eligibility ของ M3 เท่านั้น -- grep ทั้ง `field_mobs.py` และ `gm/attr_wire.py` (ตาราง 55 แถว) ไม่มีบิต/แท็กไหนผูกกับ rank เลยสักตัว ไม่มีไบต์ให้ปรับ ประดิษฐ์ offset เองคือการเดา ไม่ใช่การวัด |

## ตารางสีของเจ้าของ (`2150`) คำต่อคำ -- ใช้เกรดทุกใบสี
- **เขียว** = ผู้เล่นอื่น ฝ่ายเดียวกัน
- **ชมพู** = ผู้เล่นอื่น ฝ่ายตรงข้าม (PVP หรือ field PK)
- **เหลือง** = NPC
- **ส้ม** = มอนยังไม่ aggro · **แดง** = มอน aggro · **เทา** = มอนตาย
- **ขาว** = ชื่อตัวเอง

## เกณฑ์ผ่าน (คำสั่งเจ้าของ `2142`/`2150`)
ได้ค่าที่ทำให้ NPC เหลือง **และ** ค่าที่ทำให้มอนส้ม (ค่าเดียวกันหรือคนละค่าก็ได้) = PASS · ได้ข้างเดียว = PARTIAL ระบุขาดข้างไหน · ทั้งแถวยังเขียว/ชมพู = ผลลบที่มีค่า -- เขียนลงใบว่าตัดฟิลด์ไหนทิ้งแล้วทั้ง NPC และมอน ห้ามเปิดใบใหม่ถามซ้ำ · ถ้าฟิลด์ใดเปลี่ยนสี ต้องยืนยันซ้ำอีกครั้งด้วยค่าที่สองของฟิลด์เดียวกัน (สำรอง env value `3` ไว้สำหรับรอบยืนยัน ยังไม่ implement จนกว่าจะรู้ว่าต้องยืนยันฟิลด์ไหน)

## บล็อก `ATTENDED:` (≤5 บรรทัด ตามฟอร์แมตบังคับ)
```
ATTENDED:
1. บูตเซิร์ฟเวอร์ด้วย env `PF_NAME_COLOUR_SWEEP=1` (ชุด faction) หรือ `=2` (ชุด actor_type+skin); เข้าเกม ฉาก 1 (Port Royal) ใกล้จุดเกิด
2. เดินไปหน้าแถวหุ่น (เรียงตาม +X จากจุดเกิด ห่างกัน 150 หน่วย); ถ่ายภาพหน้าจอ 1 รูปครอบทั้งแถว
3. อ่านฉลากบนหัวแต่ละตัว (N-BASE/N-F07/.../M-BASE/M-AT3/...) จดสีที่เห็นคู่กับฉลาก
4. ผ่าน/ไม่ผ่าน: ตามตารางสี `2150` ข้างบน + เกณฑ์ PASS/PARTIAL/ผลลบข้างบน
5. ทำซ้ำกับอีก env value (รวม ≤2 ชุดรอบนี้ + สำรอง `=3` รอบยืนยันถ้าจำเป็น) -- ~15 นาที/ชุด
```

## ต้องบูตด้วยอะไร
- ทรี `pirate-force-server` กิ่ง `claude/gifted-clarke-dipufa` (หรือ main หลัง PR merge) + `pf_bridge` กิ่ง `claude/practical-knuth-dipufa`
- env `PF_NAME_COLOUR_SWEEP=1` หรือ `=2` เท่านั้น -- ไม่ต้อง flag อื่น ไม่ต้อง `--*-scenario`
- 🔴 **หมายเหตุ: สปาวน์เนอร์ยังไม่ถูกต่อสายเข้า runtime.py/app.py** (คนละงานกับใบนี้ -- ต้องมี CORE-REQUEST แยกให้ chief ต่อสาย env → dispatch เหมือน `pose_trial`/`speed_wire`) ถ้ายังไม่ต่อสาย ATTENDED รอบนี้บูตไม่ขึ้นจริง ใบนี้ส่งโค้ด+ผู้สมัคร+เกณฑ์ตามเส้นตายก่อน แล้วเปิด CORE-REQUEST ต่อสายเป็นข้อถัดไปของ B

PR: `pirate-force-server` กิ่ง `claude/gifted-clarke-dipufa` (`5a718e2`) -- จะเปิดหลังจดหมายนี้ ตามลำดับ COO `2345`

-- LANE-B
