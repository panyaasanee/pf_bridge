# CLIENT_RE_QUEUE.md - ARCHIVE 2026-09-06 (chief LANE-E round u2o8d7 / R368)

Verbatim bodies of a SHORT, HAND-CHECKED allowlist of closed tickets, moved out of the live
queue file.  Each block is byte-identical to what stood in the live file and the live file keeps a
one-line stub pointing here.  Selection was NOT done by status regex: pf-adversary proved that
regex-driven selection cut two OPEN tickets (GT-133, GT-178) out of the live file and archived six
tickets whose own headers say they are not closed.  This file therefore carries only tickets whose
H2 header was read by hand and whose closure is unambiguous, and only those closed well over 24h
ago.  Round file R368 records the full finding.


## 🔬 RE-256 ADDSURVEYDATA-OUTER-PRESENCE-BYTE-VALUE-001  [✅ **DONE -- ตอบแล้ว 2026-09-05 10:07 +07:00** · ปิดหัวโดย chief (LANE-E) รอบ `pv4zg1`/R352 ตามใบผล `notes_to_chief/20260905_1007_RE-256-RESULT-PRESENCE-ONE-SINGLE-RECORD-VERSION-ZERO.md` · คำตอบ: outer byte tag `0x0B` = **pointer-presence boolean** (`cmp dword ptr [esi+0x14],0` / `setne al` ที่ `0x00733586-0x0073358E`) ⇒ หนึ่ง record = `0B 01` · ไม่มี record = `0B 00` · **ไม่ใช่ record count** · `vital_version` ของคลาสนี้ต้องเป็น `0` แบบ exact equality (`0x005F3EFC/0x005F3F01`) · BUILD_IMPACT ลงโค้ดแล้วโดย LANE-A รอบ `vwekfq` = server `#810` (`c3454949`) บน main `b49a4e45` [วัดแล้ว `--is-ancestor` exit 0 · chief `pv4zg1`] · ผู้บริโภคผล = LANE-A (บริโภคแล้ว) ⇒ `GT-233` ปลดหัวเป็น READY ในรอบเดียวกัน · เดิม: 🟠 **OPEN** -- 🔴 `[STATIC-ON-BRIDGE]` (ต้องเปิด client image = RE runner บนเครื่อง Panya · LANE-A บนคลาวด์ไม่มีไบนารี `LANE-A 0435` · `COO-DECISION 20260905_0645` รับทาง 2) · เลขใบตั้งโดย chief (LANE-E) รอบ `rs8uyz`/R350 ตาม `LANE-A-RE-TICKET 20260905_0430` (ฉบับแก้ทับ 05:15 หลัง pf-adversary) + `COO-DECISION 20260905_0645`/`0646` · ผู้ทำ = **RE runner (local)** สายเดียว · **เจ้าของใบ/ผู้บริโภคผล = LANE-A** · ตัวบล็อกของ `GT-233` (BLOCKED-ON-LAYOUT) และของบันได **M2**]

> 🔢 ตัวนับร่วมสองคิว + `archive/*QUEUE*ARCHIVE*` คืนสูงสุดที่ `255` (`GT-255`) => ใบนี้ `256` · `RE-256`/`GT-256` = 0 hit ทั้งสามที่ก่อนวาง

## ค้นแล้วก่อนเปิดใบ (ผลการ grep -- กติกาใหม่ `AGENTS.md` §7 · `COO 0646` ข้อ 2)
- `external/PF_SERIALIZER_FIELDS.tsv:6377-6388` -- **เจอ** สแปน+SHA ตรงกับที่ `RE-227` อ้าง (`[0x00733570,0x00733614)` · `f8c7510018...af178c`) ให้ **tag/ยาว/gate** ของ presence byte `0x0B` (1 ไบต์ · ALWAYS) แต่ **ไม่ให้ค่า**
- `archive/notes_to_chief_2026-08/20260827_0115_RE-086-RESULT-*` -- **เจอ** ร้อยแก้วตรงกัน: outer serializer ส่ง presence byte แล้วเรียก nested vtable slot `+0x10` (63 คำสั่ง · gap/error 0/0)
- ⇒ **สิ่งที่ค้นเจอถูกตัดออกจากใบนี้แล้ว** ฉบับ 04:30 ถามข้อที่ commit อยู่แล้ว สาย A แก้ทับเอง เหลือเฉพาะข้อที่ยังไม่มีใครวัด

## คำถาม (สี่ข้อ ทั้งหมดตอบด้วย static)
1. **ค่า** ของ presence byte ชั้นนอกเมื่อ collection มี record หนึ่งตัว -- `1` · จำนวน record · หรืออย่างอื่น (ห้ามเดา)
2. ลำดับ **อ่าน** ต่างจากลำดับ **เขียน** ไหม (ตาราง W ให้ไบต์ก่อน call · R ให้ call ก่อนไบต์ เรียงตาม file offset) -- ฟังก์ชันเดียวสองทิศ หรือคนละทาง
3. `CALL 0x0072EC50` และช่อง `INDIRECT(DEREF(DEREF(DEREF(OBJ+0x14))+0x10))` เขียน/อ่านอะไรลงสาย · ตัวไหนคือ nested record serializer `[0x0072e590,0x0072e691)` ที่ `RE-227` พิน · มีอะไรคั่นกลางอีกไหม
4. คลาสนี้อ่าน record ได้กี่ตัวต่อข้อความ และ `vital_version` ที่ผู้อ่านยอมรับคือค่าใด (เราส่ง 0)

## เกณฑ์ปิดใบ (ชั้นเดียว -- static IMAGE เท่านั้น)
ค่า/ลำดับ พร้อม SHA ของสแปนที่อ่าน (recompute ได้) · **bounded-negative รับเป็นคำตอบปิดใบ**: "ค่าไม่ได้ถูกกำหนดตายตัวในโค้ด" ปิดใบได้ แล้ว LANE-A เดินทาง "ลองสองค่า" ในรอบ attended แทน

## ใบนี้ไม่ขอ
ชั้น client-observable ไม่อยู่ในใบนี้ · ห้ามบูตไคลเอนต์เพื่อปิดใบนี้ · ถ้าคำตอบทำให้ตั้งค่าได้ LANE-A จะขอบูตหนึ่งครั้ง**พ่วง** `GT-233` ไม่ใช่บูตแยก

## ห้ามสรุปสิ่งเหล่านี้ (กติกาหลักฐาน)
- `0xC4AF` **มีหลักฐานบนจอหนึ่งชิ้น** (`ErrorData=50351` = id ของคลาสเอง · R313 02:07 · `navigationex_survey_record.py:116-211`) ⇒ **ตั้งต้นว่า `msg_id` ถูก** ใบนี้ไม่ได้เปิดมาตรวจ `msg_id`
  🔴 **แต่ห้ามเขียนว่า "พิสูจน์แล้วสองชั้น"** (แก้ตาม pf-adversary D9 รอบ `rs8uyz`/R350 · ถ้อยคำเดิมของ chief ผิด): ครึ่งที่สองของคู่คือ **เฟรมที่เราส่งเอง** ซึ่งเป็น *ตัวกระตุ้น* ไม่ใช่พยานอิสระ มันขัดกับตัวเองไม่ได้ ⇒ มี **หนึ่งการสังเกต + หนึ่งข้อโต้แย้ง (name hash)** ไม่ใช่สองชั้นตาม G5
  ⇒ ถ้าผลของใบนี้ทำให้สงสัย `msg_id` ขึ้นมาจริง **ให้เขียนมา ไม่ใช่กลืนไว้** · control ที่ยังไม่มีใครรัน = ส่ง id ผิดโดยตั้งใจ แล้วดูว่ากล่อง error ยังขึ้นชื่อคลาสนี้ไหม (ถ้าขึ้น = 50351 ไม่ได้ระบุ id ของเรา)
- ห้ามยก `0306` ("encoder ตรง capture ⇒ layout ไม่ใช่ตัวผิด") เป็นฐาน -- **ถอนแล้ว** (`LANE-A 0555` · adversary D2 · `COO 0645`/`0646` ข้อ 1)
- ห้ามเหมาค่าที่วัดได้จากคลาสอื่นมาใช้กับคลาสนี้ (กฎ PER-CLASS)
- G8: ทุกแถวในผลติดป้าย `[วัดแล้ว]`/`[เสนอ]`

## แยกจากใบไหน
`RE-227` (กลไก provisioning · ยังไม่ถูกหักล้าง) · `RE-086`/`RE-087`/`RE-090` (ผลเดิม commit แล้ว ห้ามขอซ้ำ) · `#797` วางโค้ดรองรับไว้แล้ว (`outer_leading_byte` · `None` = ไบต์เดิมเป๊ะ ไม่มีอะไรบนสายเปลี่ยนจนกว่าใบนี้จะตอบ)

## ถ้าผลออกทางลบ
ปิดเป็น bounded-negative พร้อมระบุว่า static อ่านไม่ได้เพราะอะไร · LANE-A เปิดรอบ attended "ลองสองค่า" พ่วง `GT-233`

## ผลไปถึงใคร
จดหมายผลจ่าหน้า **LANE-A** (cc chief, COO) · LANE-A บริโภคเองและปิดหัวใบนี้ในรอบของตัวเอง (§5 "ใครเปิดใบคนนั้นบริโภค") · ถ้าผลขอ attended capture ⇒ LANE-A เปิดใบ GT ในรอบเดียวกัน (`COO 2142`)

---

---

