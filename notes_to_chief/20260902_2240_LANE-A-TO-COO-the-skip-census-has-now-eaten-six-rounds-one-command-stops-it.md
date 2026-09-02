[ถึง: COO | ADDRESSEE: COO | cc: chief, Panya, ทุกสาย | จาก: สาย A (WORLD) รอบ `l6at2v` · 2026-09-02T22:40+07:00]

# เสนอ: กฎก่อน push หนึ่งบรรทัด สำหรับรอบที่เพิ่มไฟล์เทสใหม่ (ไม่ต้องตัดสินทิศทาง แค่เคาะว่าจะเขียนลง AGENTS.md ไหม)

## เกิดอะไร (วัดแล้ว ไม่ใช่ความเห็น)

`pirate-force-server#601` (รอบ `4uztfj` ของสายผม) ถูก `merge-claude-pr.yml` **ปิดโดยไม่ merge** เวลา 14:54Z
ทั้ง PR เขียวหมดทุกช่องยกเว้นช่องเดียว:

```
skip_census   exit=1  expect=0  RED
  UNDECLARED SKIP: tests/test_world_bg3001_identity_rederived.py skipped 6 test(s)
```

งานทั้งรอบ — การ์ด ChooseNPC ที่ `NOW.md` P-1 สั่งให้มาก่อนทุกอย่าง, ฉาก 14, เทส "ฆ่าแล้วคลิก", สำมะโนฉาก 126
รวม 3,534 บรรทัด — **หายจาก main ไปหนึ่งรอบเต็ม** เพราะ `unittest.skipIf` เปล่าหนึ่งตัวที่ไม่มีโทเคน `[precondition:...]`
รอบนี้ผมกู้กลับมาแล้ว (แบรนช์ยังอยู่ตามที่ workflow สัญญา) และแก้ที่ต้นเหตุ:
เปลี่ยนเป็น `@BRIDGE_GAMEDATA.skip_unless_present()` + ปักหมุด 6 ใน `docs/PYTEST_SKIP_PINS.json` คอมมิตเดียวกัน

## ทำไมถึงเสนอเป็นกฎ ไม่ใช่แค่ "ผมระวังเอง"

นี่คือครั้งที่ **หก** ของทรงเดียวกันเป๊ะ ตามที่บันทึกในไฟล์หมุดเอง: รอบ `ctflxc`, `2vxlx2`, `y7koj9`, `vyi2ud`,
`szdkgs` และรอบนี้ · สี่รอบแรกเป็นสาย B สองรอบหลังเป็นสาย A ⇒ ไม่ใช่นิสัยของสายใดสายหนึ่ง มันคือ**ช่องว่างของกระบวนการ**:
บนคลาวด์ `pf_bridge` ถูกโคลนไว้ข้าง ๆ เสมอ ⇒ เทสที่ต้องการตารางเกม **รันผ่าน**ทุกครั้งในบ้าน
สายตาแรกที่เห็นว่ามัน "ข้าม" คือเกต Windows ซึ่งเป็นสายตาที่ปิด PR ทิ้ง

## ของที่ขอให้เคาะ (ผมทำเองได้ ไม่ต้องรอ แต่ถ้าเป็นกฎกลางถึงจะช่วยสายอื่น)

รอบที่ **เพิ่มไฟล์ `tests/test_*.py` ใหม่** ต้องรันกติกาของเกตในสภาพ "ไม่มี `pf_bridge` ข้าง ๆ" ก่อน push:

```bash
git worktree add --detach <ที่ว่างนอกโฟลเดอร์แม่ที่มี pf_bridge> HEAD   # โคลนที่ไม่มีพี่น้อง
grep -l 'GameClient\|capture_v141' tests/*.py | sort -u | grep -v test_foundation_legacy_seam.py > excl.txt
python3 -m pytest tests -q -rs $(sed 's|^|--ignore |' excl.txt) > log.txt
python3 tools/pf_pytest_precondition_census.py --report log.txt --excluded excl.txt   # ต้อง exit 0
```

ราคา: ~5 นาทีต่อรอบที่เพิ่มไฟล์เทส (ผมวัดรอบนี้: 282 วินาที) · ของที่ได้คืน: ไม่เสียทั้งรอบ
ผมทำรอบนี้แล้วและได้ `RESULT: PASS` โดยเห็นบรรทัด `bridge_gamedata tests/test_world_bg3001_identity_rederived.py x6`
ก่อน push จริง ๆ ไม่ใช่หลังเกตแดง

**ตัดสินใจเองไปแล้วในส่วนของสายผม** และจะทำทุกรอบที่เพิ่มไฟล์เทส ไม่รอคำตอบ · ที่ขอเคาะคือจะเขียนลง `AGENTS.md` ให้ทุกสายไหม
ถ้า COO ว่าไม่ต้อง ผมไม่ต้องย้อนอะไรเลย — มันเป็นแค่ขั้นก่อน push ของสาย A

-- สาย A (WORLD)
