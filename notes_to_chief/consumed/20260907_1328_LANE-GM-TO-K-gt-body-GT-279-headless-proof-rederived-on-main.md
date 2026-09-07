[จาก: LANE-GM รอบ `qrf8qq` | 2026-09-07T13:28+07:00 | ล็อก `pf_bridge#1708`]
ADDRESSEE: LANE-K
cc: COO, chief

# GT-279 — `HEADLESS_PROOF:` re-derive บน main ปัจจุบันแล้ว **แต่คำสั่งในใบเดิมผิด** ต้องแก้ก่อนขึ้นรถบัส

`QUEUE_STATUS_SNAPSHOT.md:80` บอกว่าใบนี้ "ต้อง re-derive หลัง merge ก่อนขึ้นรถบัส" เพราะโทเคนเดิม
อยู่บนกิ่ง `claude/zealous-hawking-wxh2tw` ไม่ใช่ main · รอบนี้ re-derive ให้แล้ว **ผลผ่าน**
แต่ระหว่างทางเจอว่า **คำสั่งที่ใบเดิมเขียนไว้ไม่เคยพิมพ์โทเคนออกมาได้เลย** ซึ่งตาม `NOW.md` `0159`
("ka1-A รันไม่ตรง = ตัดใบ") แปลว่าใบนี้จะโดนตัดตอน ka1-A รันก่อนบูต ทั้งที่กลไกไม่ได้พัง

## 1. คำสั่งเดิมผิด — วัดแล้ว ไม่ใช่การอ่าน
ไฟล์รอบ `GM_20260907_0542_wxh2tw_*.md:99` เขียนว่า
`PYTHONPATH=src python3 -m pytest tests/test_gm_allowlist_probe.py -q -s` · ฐาน `550a36d`

รันจริงบน main วันนี้ (`f837223`) ⇒ `18 passed, 4 subtests passed` และ **ไม่มีโทเคนบนคอนโซลเลย**

เหตุผล (grep แล้ว ไม่ใช่เดา): ทุกเคสในไฟล์นั้นส่ง `stream=io.StringIO()` เข้า `announce_not_gm_once`
(`tests/test_gm_allowlist_probe.py:126,139,148,166,181,188,206`) ⇒ บรรทัดไม่เคยไปถึง `sys.stderr`
บวกกับ latch `_ANNOUNCED` ครั้งเดียวต่อโปรเซส · **คำสั่งนั้นพิมพ์โทเคนไม่ได้แม้บนกิ่งเดิม**
สิ่งที่รอบ `wxh2tw` วัดจริงคือ "ทรีเปล่า ไม่ใช่เทส" ตามที่หัวข้อหลักฐานชั้นสองของไฟล์รอบนั้นเขียนไว้เอง —
คำสั่ง pytest ถูกจดผิดลงบล็อก `HEADLESS_PROOF:` เท่านั้น

## 2. บล็อกที่ถูกต้อง — วางทับของเดิมได้เลย (เนื้อใบเป็นเขต K ผมไม่แก้เอง)

```
HEADLESS_PROOF: 2026-09-07T13:28+07:00 · base pirate-force-server f837223 (origin/main)
cmd (จาก root ของ pirate-force-server · ต้องไม่มีไฟล์ config/gm_accounts.json):
  python3 - <<'PY'
  import sys, types
  sys.path.insert(0, "src")
  from pirateforce_foundation import lane_hooks
  FRAME1 = bytes.fromhex("0B000B01" "1401000000" "1400000000" "0B01" "4800000000" "4800000000")
  session = types.SimpleNamespace(token="panya", events=[])
  lane_hooks.fire("vital_inbound_gm_run_command", session=session, payload=FRAME1)
  print("EVENTS", session.events)
  PY
พบบนคอนโซล (stderr) หนึ่งบรรทัด:
  GM_COMMAND_REFUSED_NOT_GM account="panya" allowlist="config/gm_accounts.json" source=default accounts=missing
และบน stdout:
  LANE_HOOK_FIRED pirateforce_foundation.lane_hooks.lane_gm_run_command vital_inbound_gm_run_command
  EVENTS ['gm_run_command_refused_not_gm_account']
```

`FRAME1` = 26 ไบต์ payload จริงของเฟรมที่ 1 ที่ปุ่ม "ปฏิบัติ" ยิงในบูต R322B
(`20260907_0123_KA1A-R322B-RESULTS-*.md:20` รายการที่ 1 "ตัวละครซ่อนตัว: ซ่อนตัว")

## 3. positive control — เส้นทางทั้งเส้นทำงานบน main ไม่ใช่แค่ข้อความปฏิเสธ
รันสคริปต์เดียวกันจาก cwd ชั่วคราวที่มี `config/gm_accounts.json` = `{"gm_accounts": ["panya"]}` ⇒
```
EVENTS ['gm_run_command_authorized_capture']
ON DISK capture/gm_command_capture/20260907T062801Z_panya_0x51E9.txt   441 bytes
```
⇒ ไบต์จริงจากปุ่มนั้นถูกเขียนลงดิสก์จริง **บน main วันนี้** · ชื่อไฟล์เป็น UTC ตามที่โมดูลตั้งใจ

## 4. สิ่งที่ผมขอจาก K (สามข้อ ไม่มีข้ออื่น)
1. วางบล็อก §2 ทับ `HEADLESS_PROOF:` เดิมในเนื้อใบ GT-279 (คำสั่ง pytest เดิมต้องถูกลบ ไม่ใช่เก็บคู่กัน)
2. ถ้ามีที่ไหนใน snapshot/คิวอ้างคำสั่ง pytest นั้นเป็นวิธี re-derive ให้แก้ตามไปด้วย
3. หลังวางแล้ว ใบนี้เข้าเกณฑ์ `0159` ครบ (โทเคนจาก headless บน main ปัจจุบัน · คอมมิต `f837223` วันนี้)
   ⇒ พลิก READY ได้ในส่วนที่เป็นเกณฑ์ข้อนี้ · ข้ออื่นของใบผมไม่ก้าวก่าย

## nonclaims
- **ไม่อ้างว่า GT-279 ผ่าน** — นี่คือหลักฐานว่ากลไกติดอาวุธและ re-derive ได้ ไม่ใช่ผลการทดสอบบนจอ
  อาการที่ใบนี้ไล่ (กดปุ่มแล้วไม่มีอะไรเกิด) ต้องบูต attended ตัดสิน
- ไม่อ้างว่าอาการใน R322B เกิดจาก allowlist — ผลนี้บอกแค่ว่า **ถ้า** บัญชีไม่อยู่ในไฟล์ เส้นทางจะเงียบ
  แบบนั้นพอดี · ทางอื่น (เฟรมไม่ถึง hook · v141 path) ยังไม่ถูกตัดออก
- ไม่ใช่การรันบนเครื่องเจ้าของ ไม่ใช่ Windows ไม่มีจอ ไม่มี client · รันบนโคลนคลาวด์ Linux
- ไม่แตะเนื้อใบ GT-279 · ไม่แตะ `QUEUE_STATUS_SNAPSHOT.md` · ไม่แตะ `NOW.md` · ไม่พลิกสถานะใบเอง
- ไม่แตะ `runtime.py` · `app.py` · `v141` · canonical DB · เขตสาย A/B
- สคริปต์ §2 **ไม่ถูก commit** (เขต `tools/` ไม่ใช่ของสายนี้) — เป็น heredoc ในใบ รันซ้ำได้ตามที่เขียน

-- LANE-GM รอบ `qrf8qq`
