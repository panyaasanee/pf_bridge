[ถึง: chief cloud (cc) และ Panya · จาก: ผู้เทส LOCAL / คนหน้าเครื่องสะพาน]

# GT-053 SCENE2-NATIVE-IDENTITY-CROSSCHECK-001 — RESULT

- เวลา: 2026-08-24 00:38:45 +07:00
- สถานะที่เสนอ: `[PASS]` / `[DONE]`
- ลักษณะงาน: static read-only เท่านั้น; ไม่เปิดเกม, ไม่บูต server/client, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB

## ช่องค้นบังคับ

- ค้นใน `pf_bridge\external\` แล้ว: **เจอ** inventory/capture ของ scene 2 และ `PF_DATA_EVIDENCE.tsv` ที่กล่าวถึงไฟล์ประกอบใต้ `Bg0002`; **ไม่เจอ** native placement roster ที่ตอบ N/index 60 ได้
- ค้น gamedata แล้ว: **เจอ** `tables\CONSTDATA_TH__SCENE_NAME.tsv` แถว `n_ID=2 -> s_MODLE_ID=BG0002` และ `tables\CONSTDATA_TH__MOBS.tsv` แถว `n_ID=34`; แต่ **ไม่พบ** `pf_bridge\gamedata\scene\` และไม่พบ `*.placements.tsv` จึงไม่มีผลถอด `.npc` สำเร็จรูปให้ใช้

## คำตอบ objective หนึ่งประโยค

**ไฟล์ฉาก scene 2 `Data\Scene\Save\Bg0002\Bg0002.npc` มี N=106 placements (>=61); index 60 อยู่ที่ record `0x1CAE`, f32 triple ที่ `0x1CCA` ตรง P60 authentic แบบ bit-exact จึงยืนยันว่า `0x203D` อยู่ใน band ของ index 60 และ H1 รอด**

## Resolve โฟลเดอร์โดยไม่เดา

เส้นทาง crosswalk โดยตรง:

```text
scenario.entry.scene_id = 2
  -> SCENE_NAME.n_ID = 2
  -> SCENE_NAME.s_MODLE_ID = BG0002
  -> GameClient\Data\Scene\Save\Bg0002\Bg0002.npc
```

- `GT044_SCENE_NAME_007.tsv` และ `gamedata\tables\CONSTDATA_TH__SCENE_NAME.tsv` byte-identical (`sha256 e38114...`) และให้แถวเดียวกัน: `n_ID=2`, `s_MODLE_ID=BG0002`, `s_IMAGENAME=Bg0002_air`, `s_MUSIC_FILE=Scn0002`
- `MAP_SCENE_LIST` ไม่มี field crosswalk ไป `SCENE_NAME`; ไม่ได้ join `MAP_SCENE_LIST.n_ID=2` ด้วย numeric coincidence
- ไม่ได้สมมติชื่อ `bg0002`; ชื่อ path มาจาก `SCENE_NAME.s_MODLE_ID` โดยตรง

## Native placement evidence

- ไฟล์: `GameClient\Data\Scene\Save\Bg0002\Bg0002.npc`
- size: `11,652` bytes (`0x2D84`)
- sha256: `a649f4afab701df3698b9ffebbb83b77863531a9113c40b6f12f056b7f030b16`
- header collection: 46 `MOBSET` definitions
- placement-count field: offset `0x6E0`, bytes `6A 00` = **106**
- first placement record: `0x6E2`
- guarded sequential read: records parsed = 106; final offset `0x2D84` = exact EOF

index 60 (นับตัวแรกเป็น 0):

| field | evidence |
|---|---|
| record span | `[0x1CAE,0x1D0B)` |
| instance | `MOBSET_34 03` |
| base | `MOBSET_34` (base-length field `0x1CF3`; text starts `0x1CF7`) |
| XYZ offset | `0x1CCA` |
| XYZ raw bytes | `03 5A A7 46 73 F4 10 46 71 AB 13 44` |
| XYZ decoded f32 | `21421.005859375 / 9277.1123046875 / 590.67877197265625` |
| scenario values cast to f32 | bit-identical = `true` |
| local suffix evidence | record attrs at `0x1CEE` contain `3D 00` (=61 = index+1 for this record) |

ท่าอ่านเดียวกัน re-derived prior GT-048 anchor ของ `bg0001.npc` ถึง index 30 แล้วได้ XYZ offset `0x1D46` และค่า `1747.5244/-7837.6978/931.0413` ตรงหลักฐาน GT-048; ใช้เป็น cross-check ของแนวแกน/offset ไม่ใช่หลักฐานแทน `Bg0002.npc`.

## Template / preset crosswalk

เส้นทางที่วัดได้ ไม่ได้ join ด้วยเลขลอย ๆ:

1. placement index 60 มี base literal `MOBSET_34`
2. definition `MOBSET_34` ในไฟล์เดียวกันเริ่ม `0x4EA`; tail เริ่ม `0x500`, raw `00 22 00 00 00 00 00 00 00 00 00 64 00 00 00 00`; u32 ที่ tail+1 (`0x501`) = `34`
3. `CONSTDATA_TH__MOBS.tsv` มี explicit key `n_ID=34`; แถวนั้นให้ `s_OUTFIT=M025_001_000_N` (และ `s_ID_MODEL_CLASS=M025`, `n_ID_MODEL=1`)

ดังนั้น native record ที่ P60 ผูกกับ template key 34 และ cross-check preset ได้ `M025_001_000_N` ตรง scenario. Identity `0x203D` คือ band expression `0x2000 + index 60 + 1`; ใบนี้ยืนยัน membership ด้วย N=106 และพบ suffix `0x003D` ใน record เดียวกัน แต่ไม่ได้ยกสูตรนี้เป็นกฎสากลของทุก scene.

## คำตัดสิน H1

- `N=106 >= 61`
- P60 parse ถูกไฟล์/ถูกแกน เพราะ f32 triple ตรง bit-exact
- ดังนั้น `0x203D` **in-band** สำหรับ placement index 60 ของ scene 2
- **H1 รอด**; ผลนี้ไม่ฆ่า H1

## SHA256 ก่อน -> หลัง

| ไฟล์ | ก่อน | หลัง |
|---|---|---|
| `outbox\GT044_SCENE_NAME_007.tsv` | `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b` | เหมือนเดิม |
| `outbox\GT044_MAP_SCENE_LIST_101.tsv` | `9564867136111fd8655aa40acb14aeaf84b8e586070e7bb78db21841cc6c63b9` | เหมือนเดิม |
| `gamedata\tables\CONSTDATA_TH__SCENE_NAME.tsv` | `e38114a802576266ce37b2abcf8ebce3f105d7d5abaf4bc5ca066e7848c5d60b` | เหมือนเดิม |
| `gamedata\tables\CONSTDATA_TH__MAP_SCENE_LIST.tsv` | `9564867136111fd8655aa40acb14aeaf84b8e586070e7bb78db21841cc6c63b9` | เหมือนเดิม |
| `gamedata\tables\CONSTDATA_TH__MOBS.tsv` | `3c0d33d68f832eefda56c845495008338dcef56f4277584b9ca479b7e1b3916b` | เหมือนเดิม |
| `scenarios\scene2_fighting_fish_soldier_hp3857_player_faction1.json` | `6a4863bbb4def0f4e693512d67cc2fc4d58ceac4f9a8893b2983f4591d9880c8` | เหมือนเดิม |
| `Bg0002\Bg0002.npc` | `a649f4afab701df3698b9ffebbb83b77863531a9113c40b6f12f056b7f030b16` | เหมือนเดิม |
| `bg0001\bg0001.npc` (supplementary GT-048 offset check) | `026bbe32ca2b69853b1433d585de7e80bb67e7f713e086b9347fd10ad1dc2070` | เหมือนเดิม |

## ชั้นหลักฐานและ nonclaims

- ชั้น static: ผล N/offset/f32/SHA ข้างบน
- ชั้น client-observable: ว่างเปล่าโดยเจตนา; ใบนี้ไม่มีเกมและไม่มีภาพหน้าจอ
- `N>=61` ไม่พิสูจน์ว่า native path รันจริงใน SCENE-005 และไม่ตัดสินว่า client อัปเดต entity เดิมหรือสร้างตัวที่สอง
- ผลนี้บอกเพียง H1 รอดที่ระดับ band membership; ไม่พิสูจน์ causal render บนจอ
- พิกัด entity P60 เป็น authentic ตาม scenario; ตำแหน่งสังเคราะห์คือ player offset เท่านั้น
- ไม่ claim สูตร `0x2000+p+1` เป็นกฎของทุก scene และไม่ claim พฤติกรรมเซิร์ฟเวอร์ต้นฉบับ
- ไม่ได้เขียน parser/file ใหม่; การอ่านเป็น in-memory read-only พร้อม guard count/length/exact-EOF
