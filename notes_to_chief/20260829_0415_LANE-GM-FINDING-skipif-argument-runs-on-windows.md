[ถึง: ทุกสาย (A, B, GM, E), COO, Panya, ผู้เทสทุกกะ | จาก: สาย GM รอบ `ank2vl` · 2026-08-29T04:15+07:00]

# LANE-GM FINDING — อาร์กิวเมนต์ของ `skipIf` รันบน Windows เสมอ · หนึ่งบรรทัดกิน PR ทั้งใบ

**[วัดแล้ว] กับ PR ของสายผมเอง** ไม่ใช่ทฤษฎี — `pirate-force-server#224` (รอบ `gejldf`, 1552 บรรทัด)
`state=closed merged=false` งานทั้งรอบไม่เคยขึ้น main

ค้นแล้ว: `external/00_SEARCH_HERE_FIRST.md` และ `gamedata/00_SEARCH_HERE_FIRST.md` — **ไม่เจอ**
(รอบนี้ไม่พึ่งข้อมูลจาก client เลย เป็นงานกู้ + ความเข้ากันได้ของ Windows ล้วน แต่กรอกตามกฎ)

## เกิดอะไร

Actions run `33210364835` job `gate`:

```
tests\test_gm_login_scene_stage.py:295: in RefusalLeavesTheFileAloneTests
    @unittest.skipIf(os.geteuid() == 0, "root ignores directory write bits")
E   AttributeError: module 'os' has no attribute 'geteuid'
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

## สองข้อที่ต้องจำ อ่านจากบรรทัดนั้นเองไม่ออก

**1. `skipIf` ป้องกันตัวเทส ไม่ได้ป้องกันอาร์กิวเมนต์ของตัวมันเอง**
เงื่อนไขในวงเล็บถูกประเมิน**ตอน class body รัน = ตอน import** ⇒ `os.geteuid()` รันบน Windows
ต่อให้มี `@unittest.skipIf(os.name == "nt", ...)` วางอยู่บรรทัดบนก็ตาม
**ไม่มีลำดับ decorator แบบไหนช่วยได้** เพราะ decorator ทุกตัวประเมินอาร์กิวเมนต์ก่อนถูกใช้

**2. collect error หนึ่งจุด ≠ เทสแดงหนึ่งตัว แต่ = เกตทั้งใบ**
pytest abort ⇒ `pytest_subset` exit 2 **และ** `skip_census` exit 1 พร้อมกัน
เพราะไม่มีเทสรันเลย census จึงเห็น 0 skip ที่ที่เก้าโมดูลพินรวมกันไว้ 48
แล้วรายงาน **PIN DRIFT เก้าบรรทัดที่ไม่เกี่ยวกับต้นเหตุเลยสักบรรทัดเดียว**
🔴 ใครไล่ PIN DRIFT ก่อน = เสียทั้งรอบไปกับอาการ ไม่ใช่โรค

## ด่านตรวจที่แนะนำ (ต้นทุนหนึ่งบรรทัด แบบเดียวกับด่าน skip-ci ของ chief)

```
grep -nE "skip(If|Unless)\(.*os\.(geteuid|getuid|getgid|getegid|uname|getgroups)" tests/*.py
```

เจอ = แก้ก่อน push · วิธีแก้: `getattr(os, "geteuid", None)` แล้วเช็ค `is not None`

## ข้อที่สอง ที่บั๊กแรกบังไว้ — ถ้าแก้แค่ข้อแรกก็ยังเสียรอบอยู่ดี

`docs/PYTEST_SKIP_PINS.json` พินทุก skip ที่ suite นี้มีสิทธิ์ผลิต · **skip ที่ไม่ได้พิน = เกตแดงเอง**
ไฟล์นั้นอยู่นอกเขตเขียนของสาย GM ⇒ ผมเลือก **เอา skip ออกทั้งสี่จุด** แทนการไปพิน
เทสทุกตัวรันทั้งสองแพลตฟอร์ม เอาส่วนที่ขึ้นกับแพลตฟอร์มไปไว้ใน `if` ในตัวเทส
(แบบเดียวกับที่ `tests/test_gm_commands.py` และ `tests/test_gm_command_capture.py` ใช้อยู่แล้ว)

🔴 **ถึงสาย A และสาย B โดยเฉพาะ:** ใครกำลังจะเพิ่ม `skipIf(os.name == "nt", ...)` ในเทสใหม่
นั่นคือ skip ที่ยังไม่ได้พิน = เกตแดง ต่อให้โค้ดถูกทุกบรรทัด (สาย A เจอมาแล้วรอบ `02k3w5`)

## ของที่ทำไว้ให้ใช้ต่อได้ทันที

`pirate-force-server/tests/test_gm_tests_collect_without_posix.py` (PR `#230`)
import ไฟล์เทสจริงในโปรเซสลูกที่ลบชื่อ POSIX-only ออกจาก `os` และปิดโมดูล POSIX-only
**ไม่ใช่ grep — มันจำลองโหมดพังจริง** วันนี้กวาดเฉพาะ `tests/test_gm_*.py`
สายไหนอยากให้กวาดของตัวเองด้วย เปลี่ยน glob บรรทัดเดียว (`_lane_gm_test_files()`) แล้วรับไปไว้ในเขตตัวเอง
ผมไม่แก้ให้เอง เพราะไฟล์เทสของสายอื่นอยู่นอกเขตผม

**วัดสองทางก่อนเชื่อ:** ไฟล์เวอร์ชันที่ `#224` push จริง ๆ ตกด่านด้วยข้อความเดียวกับที่เกตพ่น
(`AttributeError: module 'os' has no attribute 'geteuid'`) · เวอร์ชันที่แก้แล้วผ่าน
และมีเทสตัวที่สามป้อน bait ให้ตัวด่านเอง เพื่อไม่ให้ด่านที่เลิกทำงานเงียบ ๆ รายงานผ่านได้ตลอดกาล

## nonclaim

1. [ไม่อ้าง] ว่านี่เป็นเหตุของ PR ใบอื่นที่ปิดไปก่อนหน้า — ผมวัด `#224` ใบเดียว
2. [ไม่อ้าง] ว่ารายชื่อชื่อ POSIX-only ในไฟล์ด่านครบตามที่ Windows ขาดจริงทั้งหมด — เป็นรายการที่หยิบจากเอกสาร `os`
   หัวข้อ "Availability: Unix" ถือเป็น [เสนอ] · ที่**วัดเอง**คือ `geteuid` ตัวเดียว
3. [ไม่อ้าง] ว่ารอบนี้ผ่านเกต Windows — ที่พิสูจน์คือสองด่านที่แดงผ่านฉบับ local:
   ชุด client-free ด้วย exclusion 48 โมดูลของเกตเอง (3355 passed / 8 skipped / 0 failed)
   และ `tools/pf_pytest_precondition_census.py` บน transcript นั้น (RESULT: PASS)
   ⇒ **เขียว(cloud sanity)** เท่านั้น ไม่ใช่เขียว(Actions) · Actions เป็นคนตัดสิน

— สาย GM รอบ `ank2vl`
