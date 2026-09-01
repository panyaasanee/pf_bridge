# เลนทดลอง ad-hoc ActorAttr probe — สำเนาอ้างอิงเท่านั้น

วางที่นี่ 2026-08-31T08:24+07:00 โดย กะ1-A **ตามคำสั่งเจ้าของ** เพื่อให้สายที่รันบนคลาวด์ (โดยเฉพาะสาย GM)
มองเห็นตารางฟิลด์และตัวส่งจริงได้ — ก่อนหน้านี้ของพวกนี้อยู่นอก repo ทั้งสองใบ
(`Desktop\Pirate Force\adhoc_actorattr_probe\`) สาย GM จึงค้นไม่เจอและรายงานผลลบมาอย่างถูกต้อง
(ใบ `notes_to_chief/20260831_0330_LANE-GM-ASK-COO-attr-wire-py-premise-does-not-verify-*`)

## 🔴 กฎการใช้ไฟล์ในโฟลเดอร์นี้

1. **อ่านอย่างเดียว** ห้าม import ห้ามรัน ห้ามให้เทสอ้างถึง โฟลเดอร์นี้ไม่ใช่แพ็กเกจ ไม่มี `__init__.py`
2. **นี่ไม่ใช่โค้ดที่ผ่าน gate** ไม่เคยผ่าน pf-adversary ไม่มีเทส ไม่ได้อยู่ในสวีตของใคร
   ถ้าจะเอาไปใช้จริงต้องเขียนใหม่ในเขตของสายตัวเอง พร้อมเทส ไม่ใช่ copy-paste
3. **ยังไม่ปลดล็อกอะไร** `UpdateAttrVital` ยังไม่มี version-confirmation constant และตาราง
   `characters` ยังไม่มีคอลัมน์ level/hp/class — ทั้งสองข้อที่สาย GM ยกมายังจริงทุกตัวอักษร
   `gm/attr_wire.py` ยัง shelve ตาม `COO-DECISION 20260831_0350`

## มีอะไรบ้าง

| ไฟล์ | คืออะไร |
|---|---|
| `adhoc_attr_probe.py` | ตัวส่งจริง: parse แชท `0xAC52` -> ตั้งค่าฟิลด์ -> ส่ง **ทั้งบล็อก** เป็น `UpdateAttrVital` (`0x309A`) · ตาราง `FIELDS` มี 55 แถว (43 ActorAttr + 12 BasicAttr) ครบ offset/kind/mask bit |
| `ACTORATTR_PROBE_TABLE_x_y.md` | ตารางช่อง x/y ที่เจ้าของใช้ยิงทีละฟิลด์ |
| `ADHOC_PROBE_ROUND1_FINDINGS_20260827.md` | ผลรอบแรก 266 คำสั่ง 2 ชม. 20 นาที ในการเชื่อมต่อเดียว (เจ้าของขับเอง) |

## ทำไมถึงตอบข้อ (a) ของ COO ได้

สาย GM ติดว่า `stats_progression_hypothesis.ACTOR_ATTR_FIELDS` รองรับแค่ 23 จาก ~47 ฟิลด์
⇒ "ส่งทั้งบล็อกเสมอ" ทำไม่ได้ · ตาราง `FIELDS` ในไฟล์นี้มี 55 แถว ซึ่งคือส่วนที่ขาด
docstring ของมันเขียนเหตุผลข้อ (a) ไว้เองก่อน COO สั่งด้วยซ้ำ:

> "Every send carries the FULL block because the client's ActorAttr apply copies the incoming
>  object whole (v141 note on 0x464F30) -- a sparse delta would zero what it omits."

## สิ่งที่ **ไม่ได้** ย้ายมา และจะไม่ย้าย

`adhoc_actorattr_probe\tree\` — สำเนาเซิร์ฟเวอร์ทั้งต้นไม้ **18 MB · 320 ไฟล์ .py**
ย้ายเข้ามาจะซ้ำกับโมดูลจริงทั้งโปรเจกต์ และมีโอกาสทำ pytest collection / gate พังทั้งระบบ
ต้นฉบับยังอยู่ครบบนเครื่องเจ้าของ ไม่มีอะไรถูกลบหรือย้ายออกจากที่เดิม (คำสั่งที่ใช้คือ copy ไม่ใช่ move)
