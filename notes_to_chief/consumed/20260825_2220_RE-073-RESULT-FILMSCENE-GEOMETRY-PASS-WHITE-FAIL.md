[ถึง: chief cloud (cc) และ Panya · จาก: RE runner LOCAL]

# RE-073 TEST-STAGE-GEOMETRY-SURVEY-001 — DONE / FILMSCENE-GEOMETRY-PASS-WHITE-FAIL

- เวลา: `2026-08-25T22:20+07:00`
- โหมด: static read-only เท่านั้น · ไม่เปิดเกม/เซิร์ฟเวอร์ · ไม่จับ `LOCK_GAME` · ไม่อ่าน/แตะ canonical DB · ไม่ทำ git operation
- คำตอบสั้น: **ในสามตัวเลือก ไม่มีฉากไหนตรงคำขอ “พื้นขาวล้วน เรียบ ไม่มีเอฟเฟกต์” ครบทุกข้อ**
  - `FilmScene` ชนะขาดด้านเรขาคณิต: เป็นห้องกล่องโล่ง พื้น flat จริง ไม่มี placement และไม่มี named water object
  - แต่ **มันเป็น green-screen สีเขียวล้วน ไม่ใช่สีขาว** และ scene graph เปิด fog/environment ไว้ จึงห้ามรายงานว่า effect-free
  - `Bg1181` มี `DefaultWater 01` + scene-graph object 20 ตัว
  - `Bg2033` มี scene-graph object 829 ตัว จึงไม่ใช่เวทีโล่ง
- จุดยืนที่เสนอถ้า Panya ยอมรับ green-screen: **`X=1000, Y=1000, Z=0`** (static candidate เท่านั้น) — อยู่ในกล่อง `±3000` ทั้ง X/Y และหลบ trigger ที่ origin ซึ่งประกาศ `Contact Range=500`

## ช่องค้นบังคับ

`ค้นใน pf_bridge\external\ แล้ว: เจอ`

- `PF_DATA_EVIDENCE.tsv` / `PF_INPUT_INVENTORY.tsv` มีแถว `surfaces.xml` ของทั้งสามฉากและตัวคุม:
  - `FilmScene`: `Block=1`, `SurfaceMask=0`, sha `75925f6e...b09a58`
  - `Bg1181`: `Block=9`, `SurfaceMask=8`, sha `3eb66332...3e76c`
  - `Bg2033`: `Block=8`, `SurfaceMask=7`, sha `aac300a5...a606`
  - `bg0001` control: `Block=3`, `SurfaceMask=2`, sha `8bbe4e58...024e`
- ไม่เจอชื่อคอลัมน์ `s_HK_VER/s_TC_VER/s_JP_VER/s_TH_VER` ในอิมเมจทั้ง ASCII/UTF-16LE; positive controls ของวิธีค้นผ่าน (`n_SCENE_TYPE` UTF-16LE ที่ VA `0x00F0C48C`, `SCENE_NAME` 4 จุด)

`ค้น gamedata แล้ว: เจอ (chief R169 ทำ crosswalk ไว้แล้ว; รอบนี้ verify แถวเป้าหมายและใช้ต่อ ไม่ทำ crosswalk ซ้ำ)`

- `SCENE_NAME`: `997 -> FilmScene`, `291 -> Bg1181`, `328 -> Bg2033`, control `1 -> BG0001`
- `PF_GAMEDATA_SCENE_INDEX.tsv`: placements `FilmScene=0`, `Bg1181=0`, `Bg2033=0`, `bg0001=149`; definition counts `0/5/26/113`
- version: `FilmScene=0.00.0000` ครบ 4 locale; `Bg1181 TH=1.07.0000`; `Bg2033 TH=1.20.0000`

## T0 — image/control PASS

- image size `14,759,424` · sha256 ก่อน/หลัง `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- first-256 sha `3ef4c116...123dd6` · last-256 sha `5341e6b2...05af1` ตรงก่อน/หลัง
- recursive-CFG positive control `0x00446F30`:
  - span `[0x00446F30,0x004470DE)` · file offset `0x00046330` · len `430`
  - sha `9c1157d3109c27c41783d6eed630a6eb46511ef6789a4e121306944ec1271d7d`
  - instructions `154` · gap `0` · indirect `0` · decode errors `0` — ตรง GT-040

## T1/T2 — รายการไฟล์ทุกตัว + positive control

### `FilmScene` — 13 files / 4,218,134 bytes

```text
filmscene_block.bm_                         428
filmscene_Dynamic.dmc                        8
filmscene.gat                               10
filmscene.gs_                            4,932
filmscene.gsa.scene.settings           209,975
filmscene_height.s_                        544
filmscene.npc                                6
filmscene.tgr                              462
filmscene_tile.bm_                         428
filmscene.tmpkg                            597
Sector_0_0/0.tg_                            85
Sector_0_0/quadtree.dof              4,000,624
Sector_0_0/surfaces.xml                     35
```

### `Bg1181` — 13 files / 4,278,934 bytes

```text
bg1181_block.bm_                         1,390
Bg1181_Dynamic.dmc                          8
Bg1181.gat                                 10
bg1181.gs_                             11,669
Bg1181.gsa.scene.settings             210,868
bg1181_height.s_                       49,412
Bg1181.npc                                 206
Bg1181.tgr                               1,932
bg1181_tile.bm_                          1,390
Bg1181.tmpkg                               552
Sector_0_0/0.tg_                           111
Sector_0_0/quadtree.dof              4,000,624
Sector_0_0/surfaces.xml                    762
```

### `Bg2033` — 20 files / 17,703,353 bytes

```text
bg2033_block.bm_                         2,144
Bg2033_Dynamic.dmc                          8
Bg2033.gat                                 68
bg2033.gs_                            268,887
Bg2033.gsa.scene.settings             210,962
bg2033_height.s_                      703,327
Bg2033.npc                               1,046
Bg2033.tgr                                 965
bg2033_tile.bm_                          2,144
Bg2033.tmpkg                             3,775
Sector_0_0/0.tg_                        20,429
Sector_0_0/1.tg_                        93,696
Sector_0_0/2.tg_                       275,962
Sector_0_0/3.tg_                       260,798
Sector_0_0/4.tg_                       369,378
Sector_0_0/5.tg_                       221,675
Sector_0_0/6.tg_                       308,612
Sector_0_0/7.tg_                        46,279
Sector_0_0/quadtree.dof             14,912,624
Sector_0_0/surfaces.xml                    574
```

### `bg0001` positive control — 14 files / 5,510,429 bytes

```text
bg0001_block.bm_                         2,912
bg0001_Dynamic.dmc                          8
bg0001.gat                                 10
bg0001.gs_                            807,686
bg0001.gsa.scene.settings             210,930
bg0001_height.s_                      412,754
bg0001.npc                              27,607
bg0001.tgr                              41,573
bg0001_tile.bm_                          3,371
bg0001.tmpkg                             1,049
Sector_0_0/0.tg_                           854
Sector_0_0/1.tg_                           854
Sector_0_0/quadtree.dof              4,000,624
Sector_0_0/surfaces.xml                    197
```

## T3 — `0.00.0000`: BOUNDED NEGATIVE ต่อ semantic แต่ตัด “ไฟล์ไม่เคย ship” ได้

- ใน `GameClient.local.bin` ค้น `s_HK_VER`, `s_TC_VER`, `s_JP_VER`, `s_TH_VER`, `0.00.0000`, `FilmScene`, `Bg1181`, `Bg2033` ทั้ง ASCII และ UTF-16LE = **0 hits**
- positive control ของ byte search ผ่านตามด้านบน ⇒ ไม่ใช่เครื่องมือค้นตาบอด
- จึง **ไม่พบ direct named consumer** ของคอลัมน์ version ในอิมเมจ; ยัง exclude generic/schema-driven หรือ ordinal access ไม่ได้
- แต่ `FilmScene` ไม่ใช่ asset ที่หายจาก TH client: มีโฟลเดอร์ฉากครบ 13 ไฟล์ และมี palette/model/texture จริง:
  - `Data/Palettes/filmscene.pa_` 729 B sha `27cbe127...82cff`
  - `Data/Scene/Model/filmscene.ni_` 570 B sha `70d66d9c...477fa`
  - `Data/Scene/Model/filmscene.dd_` 68 B sha `19abfa37...3cf25`
- ดังนั้น `0.00.0000` **ห้ามแปลว่า “content ไม่ได้ ship อยู่ใน client นี้”**; แต่ยังไม่พิสูจน์ว่า runtime ยอม enter scene 997

## T4 — เรขาคณิต / สี / น้ำ / เอฟเฟกต์

### `FilmScene` — geometry PASS, white/effect-free FAIL

- `filmscene_height.s_` decode ด้วย `gamedata/pf_decode_lua_npc.py`: header `800 x 800`; payload `3,200,000` bytes และ **nonzero bytes = 0** ⇒ stored height/material payload แบนเป็นศูนย์ทั้งหมด
- scene graph: entities `11`; `NiSceneGraphComponent=1`; trigger `1`; NPC placements `0`; `SurfaceMask=0`
- scene mesh ตัวเดียว resolve ผ่าน palette จริงไป `filmscene.nif` ชื่อ `Box01`:
  - decoded NIF sha `7536ed76...6d3f2`
  - vertex stream offset `0x3D6`, len `768`, sha `d2444e53...5b369`, `24` vertices
  - POSITION bounds local: X `[-3000,3000]`, Y `[-3000,3000]`, Z `[0,6000]`
  - entity translation Z `-218.5809` ⇒ box bounds ในฉาก Z `[-218.5809,5781.4191]`
- texture `filmscene.dds` เป็น DXT1 `32x32`; 64/64 blocks เหมือนกัน (`0x07E1,0x07E0,0x55555555`) และทุก pixel เลือก endpoint `0x07E0` = **RGB `(0,255,0)`**
- terrain component เองก็ประกาศ Ambient/Diffuse/Specular/Emittance `(0,1,0)` และ bitmap block/tile `800x800` uniform
- ไม่พบ named water/effect entity; control ใช้วิธีเดียวกันเจอ `DefaultWater 01` ใน `Bg1181` และ `waterWave01` ใน `bg0001`
- แต่ `UseFog=TRUE`; active environment `Day`; `Following Effect=Palettes\\None` ⇒ เขียนได้แค่ **ไม่มี following-effect asset / named water object** ไม่ใช่ “ไม่มีเอฟเฟกต์ทุกชนิด”
- จุด `(0,0,0)` มี `Trigger Ent[01]` (`Contact Range=500`) จึงเสนอ `(1000,1000,0)` แทน

### ตัวเลือกอื่น

| ฉาก | entities | scene-graph objects | trigger | height payload nonzero bytes | ข้อชี้ขาด |
|---|---:|---:|---:|---:|---|
| `Bg1181` | 32 | 20 | 4 | 1,985,201 | มี `DefaultWater 01`; ไม่ใช่ dry blank stage |
| `Bg2033` | 839 | 829 | 2 | 2,159,310 | วัตถุ 829 ตัว; ไม่ใช่ฉากโล่ง |
| `bg0001` control | 2,415 | 2,144 | 85 | 5,738,503 | ท่าเรือมี clutter/water ตามที่รู้; control แยกออกชัด |

### T5

ไม่ได้รันต่อ: เป็น optional (`ถ้าเหลือแรง`) และ objective ปิดด้วย T1-T4 แล้ว · `n_SCENE_TYPE` มี direct named users จริง แต่ใบนี้ **ไม่พิสูจน์ว่า type 2/256 gate การ enter scene**

## integrity ก่อน/หลัง

| ชุดอ่านอย่างเดียว | files | bytes | manifest sha256 ก่อน = หลัง |
|---|---:|---:|---|
| `pf_bridge/external` | 30 | 29,900,221 | `3b742370...4e811` |
| `pf_bridge/gamedata` | 1,109 | 15,319,585 | `e8e44669...28e5b` |
| `FilmScene` | 13 | 4,218,134 | `0cbe4216...f64af` |
| `Bg1181` | 13 | 4,278,934 | `2c1344eb...8312` |
| `Bg2033` | 20 | 17,703,353 | `5c53e2b4...df40` |
| `bg0001` | 14 | 5,510,429 | `a2470547...0187` |

หมายเหตุเครื่องมือ: การ import ตัวถอดครั้งแรกทำให้ CPython สร้าง `gamedata/__pycache__/pf_decode_lua_npc.cpython-314.pyc` 46,119 B อัตโนมัติ ทั้งที่ไม่มีตอน baseline; ลบเฉพาะ artifact ที่รอบนี้สร้างเอง แล้ว rehash `gamedata` กลับเป็น **1,109 files / sha baseline เดิมตรงเป๊ะ** ก่อนเขียนจดหมายนี้

## nonclaims (บังคับ)

1. `0 placements` ไม่เท่ากับฉากว่าง — ข้อสรุป FilmScene ใช้ scene graph + terrain + model จริงเพิ่ม ไม่ได้ใช้ placement อย่างเดียว
2. “addressable” ยังแปลเพียงมี `n_ID`; ไม่พิสูจน์ว่า server/client จะยอม enter · server ปัจจุบันยัง fail-closed ที่ scene 1/2 ตามหัวใบ
3. ไม่เปิดเกม จึง **ไม่ยืนยัน client-observable** ว่าฉาก render สี/แสง/หมอกตรง static asset, เดินได้, spawn ได้ หรือกล้องเหมาะจริง
4. จุด `(1000,1000,0)` เป็น static candidate จาก bounds/trigger เท่านั้น ต้อง verify runtime หลัง Panya เคาะเลน scene-id ใหม่
5. การไม่พบชื่อ water/effect เป็น bounded negative ที่มี positive controls; ยัง exclude generic component/asset ที่ไม่ตั้งชื่อ semantic ไม่ได้
6. ไม่มีข้อสรุปใดอ้างพฤติกรรมของเซิร์ฟเวอร์ต้นฉบับ
7. ไม่เสนอ/เปิดใบใหม่เอง: ถ้า Panya ต้องการ **ขาวจริง** แทน green-screen หรือยอมรับ FilmScene สีเขียว ให้ chief เป็นคนออกแบบ/ตีราคาสล็อต scene-id หลังคำเคาะ

## ข้อเสนอให้ chief บันทึก

- สถานะ `RE-073`: **DONE / FILMSCENE-GEOMETRY-PASS-WHITE-FAIL**
- คำตอบเจ้าของ: **ไม่มี exact match ในสามฉาก; `FilmScene` คือ green-screen stage ที่เรขาคณิตดีที่สุด**
- การตัดสินถัดไปเป็นของ Panya: ยอมรับ green-screen แล้วค่อยออกแบบ entry lane หรือขอเวทีสีขาวจริง (ซึ่งหมายถึง asset/scene ใหม่ ไม่ใช่ของที่ค้นพบในสามตัวนี้)
