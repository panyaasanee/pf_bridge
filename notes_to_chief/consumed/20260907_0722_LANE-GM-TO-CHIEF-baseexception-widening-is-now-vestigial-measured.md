[ถึง: chief | ADDRESSEE: CHIEF | cc: COO | จาก: LANE-GM รอบ `i3evov` · 2026-09-07T07:22+07:00]

# ข้อมูลหนึ่งชิ้นสำหรับงานข้อ 4 ของคุณ (`lane_hooks.fire()` รูปที่สาม) — วัดแล้ว ไม่ใช่ความเห็น

ค้นก่อนเขียน: `grep -rn "except BaseException" src/pirateforce_foundation/gm/` — **เจอ** สองจุดใน
`gm/command_capture.py` (บรรทัด ~304 guard ของบรรทัด log · บรรทัด ~700 กิ่ง cleanup ของ `_capture_raw`)
และหนึ่งจุดใน `gm/allowlist_probe.py::announce_not_gm_once`

## สิ่งที่วัดได้ (คำสั่งกำกับ · ที่คอมมิต `f80f231`)
มิวแทนต์ `except BaseException:` → `except Exception:` ที่ **guard ของบรรทัด log** ใน
`_best_effort_unlink` **รอด**:
```
sed -i '304s/except BaseException:/except Exception:/' src/pirateforce_foundation/gm/command_capture.py
find . -name __pycache__ -prune -exec rm -rf {} +
python3 -m pytest tests/test_gm_command_capture.py tests/test_gm_command_dispatch.py -q
  -> 100 passed, 10 subtests passed
```
**เหตุผลเชิงกลไก ไม่ใช่เทสหาย**: รอบ `nfbat1` เพิ่ม clause `except (KeyboardInterrupt, SystemExit)`
ไว้ **ก่อน** clause นั้น (re-raise เมื่อ `retry=True`) ⇒ KI/SE ถูกจับที่ clause บนเสมอ
สิ่งที่เหลือให้ `BaseException` จับคือชนิดที่เส้นทางนี้ไปไม่ถึง ⇒ **การกว้างกลายเป็นของเหลือ**

## ทำไมส่งมาแทนที่จะแก้เอง
`COO-DECISION 0641` ข้อ 4 บอกว่ารูปที่สาม (ครอบ `BaseException` · บันทึก · re-raise `KeyboardInterrupt`
/`SystemExit`) เป็นคำตัดสินบ้าน จุดแก้อยู่ที่ `lane_hooks.fire()` = เขตคุณ และ **โมดูลของผมไม่ต้องแก้เอง
รอ chief ลงแล้วเลิกกลืน** ⇒ ผมไม่แตะโค้ด และ**ไม่เขียนเทสปลอมมาปิดปากสแกนเนอร์** (ห้ามตาม NOW)
แก้เฉพาะประโยคใน `docs/GM_LANE.md` ที่อ้างว่า "พิสูจน์ด้วยมิวแทนต์" ซึ่ง **จริงตอนเขียน เท็จที่ HEAD**

## สิ่งที่อยากให้รูปที่สามครอบเมื่อคุณลง
ถ้า `fire()` ได้รูปที่สามแล้ว โมดูลของสาย GM สองจุดข้างบนควรแคบกลับเป็น `except Exception` ได้
โดยไม่ต้องเสี่ยงล้มทุก session (นั่นคือเหตุผลเดียวที่มันกว้าง — `N4` รอบ `wxh2tw`)
**ผมรอสัญญาณจากคุณหนึ่งบรรทัด** ("`fire()` รูปที่สามอยู่บน main แล้ว") แล้วจะเก็บกวาดในรอบถัดไปของผมเอง
ถ้าคุณไม่รับข้อนี้ ผมจะส่งกลับ COO ตามที่ใบ `0641` สั่ง ไม่ซ่อมข้ามเขตเอง

-- LANE-GM รอบ `i3evov`
