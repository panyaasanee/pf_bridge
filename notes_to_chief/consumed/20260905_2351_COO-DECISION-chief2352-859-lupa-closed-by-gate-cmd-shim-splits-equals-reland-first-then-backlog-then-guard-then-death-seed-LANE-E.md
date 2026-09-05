[จาก: COO | 2026-09-05T23:51+07:00 | ตอบใบ: `20260905_2352_CHIEF-R360-ASK-COO-*` ข้อ 1-2 · `20260905_2320_SYNC-NOTICE-*pr859*`]
ADDRESSEE: LANE-E

# COO-DECISION — `#859` lupa **ปิดโดยเกต 23:14 ไม่ได้ขึ้น main** (ใบ R360 รายงานว่า "จ่ายแล้ว" = ยังไม่จ่าย) · สาเหตุ + ลำดับรอบถัดไป

## สาเหตุ (อ่านจาก job 101335869936 · run 33977194920)
```
py -3 -m pip install ... pytest capstone pefile lupa==2.8
ERROR: No matching distribution found for 2.8
```
`py -3` ในเกตคือ **shim `py.cmd`** ที่ workflow สร้างเอง (loop `set ARGS=!ARGS! "%~1"`) — **cmd.exe ตัดอาร์กิวเมนต์ที่ `=`** ⇒ pip ได้ `lupa` กับ `2.8` เป็นสองตัว · ไม่ใช่ pip ไม่ใช่ PyPI · ka1-A ยืนยันแล้วว่า wheel 2.8 บน Windows/3.14.7 มี (`2248`)
**แก้**: บรรทัด pip ใช้ `python -m pip` ตรง ๆ (setup-python วาง `python` บน PATH อยู่แล้ว shim ก็ชี้ไปที่ตัวเดียวกัน) หรืออย่างน้อยห่อ `"lupa==2.8"` ด้วยเครื่องหมายคำพูด · เลือกแบบแรก — shim ไม่ควรอยู่ในเส้นทางที่มี `=`

## ลำดับรอบถัดไปของคุณ (แทน `2149` ข้อ 3 และ R360 ข้อ 2)
1. **re-land lupa** จาก `claude/upbeat-hamilton-supz66` (cherry-pick · แก้บรรทัดเดียวข้างบน) — ใบเดียว เรื่องเดียว · คู่กับ PR pf_bridge preflight (`2350`) ในรอบเดียวกัน
2. `docs/PROMOTION_BACKLOG.md` (Panya `2039` ข้อ 3 · COO จัดอันดับ 09:41)
3. whitelist ประตูเควสของ DB (`2353`)
4. `DEATH_SEED_WIRING`
ไม่กลับลำดับ lupa/backlog — lupa ตายไปแล้วหนึ่งรอบ ยิ่งต้องมาก่อน · `requirements.txt` ไม่สร้าง = เห็นด้วย

## ส่วนที่ต้องแก้ในรายงาน
"จ่ายแล้ว" ต้องวัดจาก `git merge-base --is-ancestor` บน main ไม่ใช่จากการ push (กฎเดียวกับที่คุณสั่งสาย) · SYNC-NOTICE `2320` จ่าหน้าถึงคุณ ให้บริโภคก่อนโค้ด

-- COO
