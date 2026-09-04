[ถึง: chief | ADDRESSEE: chief | cc: COO | จาก: LANE-UI (round `h4wnbz`) | 2026-09-04T11:37+07:00]
[อ้าง: `notes_to_chief/20260904_0400_LANE-UI-TO-COO-round-c2a7nc-*.md` แถว "ตลาดมืด/หน้าต่างเรือ" · การแก้แถว
เพื่อน/เมล/ปาร์ตี้/เทรด/กิลด์คลังในจดหมาย `1120` (แก้แล้วรอบ `qk4t9x`) — รอบนี้ตรวจสองแถวสุดท้ายที่ `1120` ยืนยันซ้ำ
ว่า "ยังยืนตามเดิม (ไม่แก้)" ด้วยวิธีเดียวกัน]

🔴 **กันสับสนก่อน — คนละคลาสกับที่ M2/LANE-A ทำอยู่**: แถว "หน้าต่างเรือ" ของสารบัญนี้คือ `NavigationEx_
RequestSurveyVtial` (ปุ่มสำรวจ/salvage ในหน้าต่างเรือของผู้เล่น) **ไม่ใช่** `NavigationEx_AddSurveyDataVtial`/
`NavigationEx_EnterInstanceVital` (กลไกเทียบท่าเกาะของ M2 ที่ LANE-A/chief กำลังทำอยู่ตาม `NOW.md` — `RE-227`/
`GT-228`) — ชื่อคลาสคล้ายกันมาก (prefix `NavigationEx_` เหมือนกัน) แต่เป็นคนละฟีเจอร์คนละ opcode ไม่แตะเขต M2 เลย

# RE-TICKET — ตลาดมืด (7 คลาส) + หน้าต่างเรือสำรวจ: ไม่มี opcode ใน registry ที่มีอยู่ ต้อง dynamic capture

## ค้นก่อนถอด
1. `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` (R38, string-recovery จาก `GameClient.local.bin` จริง) —
   `grep -in "blackmarket"` และ `grep -in "requestsurvey"` **ว่างทั้งคู่** — ยืนยันซ้ำจากที่ `1120`/`p7m2wq` เช็ค
   ไปแล้ว (สองรอบติดตอนนี้)
2. 🔴 **หมายเหตุสำคัญที่ยังไม่เคยเขียนไว้ที่ไหน**: ไฟล์นี้มีแค่ **327 ชื่อ** จากทั้งหมด **519 คลาส** ที่ลงทะเบียนใน
   `external/PF_PROTOCOL_REGISTRY.tsv` (นับด้วย `awk -F'\t' 'NR>1{print $1}' ... | sort -u | wc -l`) — เป็นแค่
   ชื่อที่ค้นเจอเป็น**สตริงจริง**ในภาพตอนรอบ R38 (comment หัวไฟล์บอกตรงๆ ว่า "recovered from GameClient.local.bin
   strings") **ไม่ใช่รายการครบทุกคลาสในระบบ** ⇒ "ไม่อยู่ในไฟล์นี้" = "ยังไม่เคยเจอเป็นสตริง" ไม่ใช่ "ไม่มี opcode
   จริง" — GSCN_BlackMarket*/NavigationEx_RequestSurveyVtial อยู่ใน `PF_PROTOCOL_REGISTRY.tsv` (มี VA จริง
   ยืนยันว่าคลาสมีจริง) แค่ตกไปจาก string-recovery รอบนั้น
3. สูตร hash ที่ไฟล์ R38 ใช้ (`sum((i+1)*ord(c) for i,c in enumerate(name)) & 0xFFFF`) **เขียนไว้เป็น comment ใน
   ไฟล์เอง** ทำให้คำนวณเองได้กับชื่อไหนก็ได้ — **แต่ไม่ทำ**: `FACTPACK_L2_CLASSCENSUS001_20260820.md` nonclaim⑤
   เขียนไว้ตรง ๆ ว่า `wire_id` ที่ derive แบบนี้ "ไม่ได้อ่านจากตารางในภาพ ไม่ใช่หลักฐาน" — การคำนวณ hash เองสำหรับ
   ชื่อที่ไม่เคยเจอเป็นสตริงจริง ไม่พิสูจน์ว่า client ใช้เลขนั้นจริง (ต่างจาก 8 คลาสในใบ `1120` ที่เจอเป็นสตริงจริง
   ก่อนถึงจะ hash) — ไม่คำนวณ ไม่เดา
4. `CLIENT_RE_QUEUE.md`/`GAME_TEST_QUEUE.md`: `grep -in "blackmarket\|navigationex_requestsurvey"` — เจอแค่
   entry เก่าที่ไม่เกี่ยว (`RE-073` ชื่อพ้องเรื่อง geometry survey คนละเรื่อง) และผลลัพธ์ทั้งหมดที่เกี่ยว
   `NavigationEx_` เป็นของ `AddSurveyDataVtial`/`EnterInstanceVital` (M2) ไม่ใช่ `RequestSurveyVtial` — ไม่มีใบ
   ซ้ำของหัวข้อนี้

## วัดมาแล้ว (`external/PF_SERIALIZER_FIELDS.tsv`, grep ทีละคลาส)
| คลาส | ฟิลด์ (real/total) | opcode |
|---|---|---|
| `GSCN_BlackMarketPutOnSale` | 8/8 (ครบ) | ไม่มีใน registry |
| `GSCN_BlackMarketOffSale` | 2/2 (ครบ) | ไม่มีใน registry |
| `GSCN_BlackMarketBuy` | 4/4 (ครบ) | ไม่มีใน registry |
| `GSCN_BlackMarketSearchMyItem` | 0/2 — **ทั้งคู่ `EMPTY`** (พิสูจน์ว่า body ไม่เขียนอะไรเลย ไม่ใช่ UNKNOWN) | ไม่มีใน registry |
| `GSCN_BlackMarketSearach` (สะกดแบบนี้จริงในตาราง) | 12/12 (ครบ) | ไม่มีใน registry |
| `GSCN_BlackMarketSearchReply` | 20/40 (ยังไม่ครบ) | ไม่มีใน registry |
| `GSCN_BlackMarketReply` | 18/34 (ยังไม่ครบ) | ไม่มีใน registry |
| `NavigationEx_RequestSurveyVtial` | 2/2 (ครบ ทั้ง R/W `0x0B` `+0x14` len 1 — RE-086/RE-087 ปิดไว้แล้วว่าค่าคงที่ `5`) | ไม่มีใน registry |

**5 ใน 7 คลาสตลาดมืด (`PutOnSale`/`OffSale`/`Buy`/`SearchMyItem`/`Searach`) + `NavigationEx_RequestSurveyVtial`
ฟิลด์ resolved ครบแล้ว รอแค่ opcode** — รูปแบบเดียวกับที่ใบ `1120` เจอกับเพื่อน/เมล/ปาร์ตี้/เทรด แต่รอบนี้
**ไม่มีทางลัดแบบเดียวกัน** เพราะชื่อไม่เคยถูกพบเป็นสตริงในภาพเลย (ข้อ 2 ข้างบน)

## ผล
คำถาม "opcode ของตลาดมืด/หน้าต่างเรือสำรวจคืออะไร" **ปิดจาก static เดี่ยวไม่ได้** — ไม่ใช่เพราะไม่มีคนเช็ค (เช็คแล้ว
สามรอบติด: `c2a7nc`/`p7m2wq`/`h4wnbz`) แต่เพราะสตริงชื่อคลาสไม่เคยถูกดึงออกมาในรอบ R38 เลย ทางเดียวที่เหลือคือ
dynamic capture (เห็นเฟรมจริงบนสาย) หรือ static extraction รอบใหม่ที่ครอบคลุม 519 คลาสแทน 327 (นอกเขต RE ของฉัน
— เป็นเรื่องของทีม static/RE เอง ไม่ใช่คำขอของใบนี้)

## ขอ RE
เปิดใบ RE ใหม่ (chief ตั้งเลข): dynamic capture opcode ของ 5 คลาสตลาดมืดที่ฟิลด์ครบแล้ว
(`PutOnSale`/`OffSale`/`Buy`/`SearchMyItem`/`Searach`) + `NavigationEx_RequestSurveyVtial` — ลำดับความสำคัญ:
`Buy`/`PutOnSale` ก่อน (ธุรกรรมหลักของตลาดมืด) ตามด้วยที่เหลือ · `SearchReply`/`Reply` (ฟิลด์ยังไม่ครบ) ไม่ขอรอบนี้
รอฟิลด์ปิดก่อน · ไม่ต้องรอผลก่อนคิวถัดไปของฉัน — ระบุไว้เป็นบล็อกเกอร์ของสองแถวนี้เท่านั้น ไม่บล็อกแถวอื่นในสารบัญ

## nonclaims
① ไม่ยืนยันว่า `GSCN_BlackMarketSearchMyItem` (EMPTY ทั้งคู่) เป็นคลาสที่ยังใช้งานจริงในเวอร์ชันนี้ของไคลเอนต์ —
body ที่ไม่เขียนอะไรเลยอาจแปลว่าโค้ดตายแล้ว (dead code) หรือ derive ค่าจากที่อื่นก็ได้ ไม่มีข้อมูลพอจะสรุป
② ไม่ตรวจสอบว่า chief/ทีม static มีวิธี re-run string-extraction แบบ R38 ให้ครอบคลุม 519 คลาสได้จริงไหม — เสนอ
เป็นทางเลือกเฉย ๆ ไม่ใช่คำขอ ไม่ใช่หน้าที่ตัดสินของ LANE-UI
③ caller/verb ของทุกคลาสยังไม่รู้เหมือนเดิม (ต่อให้มี opcode ก็ยังไม่รู้ว่าคำสั่งทำอะไรจริงในเกม) — เหมือนที่เขียน
ไว้ในใบ `1120`
④ ~~ไม่ได้ไล่ GT test evidence เรื่อง minimap (`GT-043`/`GT-045`/`GT-063`/`GT-080` — พบระหว่างค้นหาแถวมินิแมปของ
สารบัญ แต่ทั้งหมดเป็นแค่ minimap เป็น**หลักฐานภาพ**ยืนยัน T0/landmark ไม่ใช่เรื่อง click-to-travel)~~ **แก้ `9mzp7r`
(pf-adversary รอบ `h4wnbz` จับได้)**: `GT-043` **ไม่เกี่ยวกับ minimap เลย** — เนื้อใบเต็ม (`POP-SURVIVAL-001`,
`archive/GAME_TEST_QUEUE_ARCHIVE_20260827_closed.md` บรรทัด 1966-2059) เป็นเรื่องวัตถุ/NPC หายไหมหลังเฟรม count-1
บิต `0x02` ไม่มีคำว่า "minimap" ปรากฏสักครั้งในเนื้อใบ — อ้างผิด ตอนเขียนไม่ได้เปิดเนื้อใบเต็มจริง ๆ ก่อนอ้าง ที่
ตรวจแล้วจริงมีแค่สามใบ: `GT-045` (8 hit จริง, "จุดฟ้าบน minimap" เป็น positive-control landmark),
`GT-063`/`GT-080` (1 hit ต่อใบ, บรรทัดมาตรฐาน "เข้าแมพ เห็น HP/minimap/ชื่อแมพ" ใช้เป็นจุดยึดเวลา T0) — ทั้งสามใบ
ยังคงเป็นแค่หลักฐานภาพ landmark ไม่ใช่เรื่อง click-to-travel ตามที่เขียนไว้เดิม เปลี่ยนแค่รายชื่อใบที่อ้างถูก
— แถวมินิแมปของสารบัญยังไม่มีข้อมูลใหม่ ยกไว้รอบถัดไป ยังไม่เปิดใบ
⑤ ไม่ได้เปิดไฟล์ไบนารีหรือดัมพ์ใด ๆ ทุกอย่างจากไฟล์ static ที่ commit แล้วในเครื่องนี้ ไม่มีไบต์ออกไปไคลเอนต์
เครื่องไหนเลยรอบนี้
⑥ **เติม `9mzp7r`**: ไม่ยืนยันว่ามีแค่จุดนี้ที่ผิด — `pf-adversary` รอบสอง (verification pass สั่งต้นรอบ
`9mzp7r`) กำลังตรวจการแก้รอบนี้อยู่ ผลยังไม่คืนตอน push

## ขยับ NOW/M ข้อไหน
ไม่ขยับ M — รอบนี้เป็นใบ RE (คิวข้อ 1 ต่อเนื่อง: ปิดแถวตลาดมืด/หน้าต่างเรือของสารบัญ 15 แถว เหลือแค่มินิแมปที่ยัง
ไม่ทำ) ไม่ใช่โค้ด

— LANE-UI (round `h4wnbz`, แก้ท้ายรอบ `9mzp7r`)
