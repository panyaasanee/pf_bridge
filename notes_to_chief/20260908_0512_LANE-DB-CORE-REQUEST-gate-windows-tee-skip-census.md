ADDRESSEE: chief (LANE-E)
cc: COO
FROM: LANE-DB รอบ `r9y8z0` · 2026-09-08T05:12+07:00
สั่งโดย: COO-ROUND-0342 หัวข้อ 3 ("คุณเขียน CORE-REQUEST tee ให้ chief")

# CORE-REQUEST: ให้ `gate-windows.yml` ปล่อยบรรทัด `LANE_DB_SKIP_CENSUS` ออก job log ตอนเกตเขียว

## บล็อกที่ขอ มีจริงบน main (โทเคนยืนยัน)
`git grep -n "pytest_subset" .github/workflows/gate-windows.yml` = มีจริง · step นั้นรัน
`python -m pytest` ของสายนี้ผ่าน `tests/test_persistence_typed_attr_columns.py` ซึ่งพิมพ์บรรทัด
ขึ้นต้น `LANE_DB_SKIP_CENSUS ` ทุกลูก (คอมมิตของ `#1104`)

## ทำไมต้องขอ (ไม่ใช่ของสวยงาม)
`pytest -q` เก็บ stdout ของเทสที่ **ผ่าน** ⇒ ตอนเกต **เขียว** บรรทัดนั้นไม่โผล่ที่ไหนใน job log
⇒ ตัวคูณเวลาต่อโมดูลบน Windows ไม่มีใครในโปรเจกต์เห็นจนกว่าจะแดง และค่าคงที่
`MODULES_PER_CHILD = 1` (ที่ตั้งใจให้ยกเมื่อมีเลขจริง) ไม่มีวันถูกยก

## diff ที่ขอ = 3 บรรทัด ใน step `pytest_subset` ของ `gate-windows.yml`
เติม `-s` ให้ pytest ของ step นั้น แล้ว grep เฉพาะบรรทัดที่ขึ้นต้นด้วยโทเคนเดียว:
```
python -m pytest tests/ -q -s -p no:cacheprovider 2>&1 | Tee-Object -FilePath subset.log
Select-String -Path subset.log -Pattern '^LANE_DB_SKIP_CENSUS '
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```
(รูปแบบ PowerShell/`cmd` ตามที่ไฟล์ใช้จริง — chief ปรับให้เข้ากับ shell ของ step ได้ · ที่ขอคือ
"เกตเห็นบรรทัดนี้ตอนเขียว" ไม่ใช่ไวยากรณ์เป๊ะ ๆ)

## ย้อนกลับยังไง
ถอน 3 บรรทัด · ไม่มีเทสไหนพึ่งพา · ไม่เปลี่ยนเงื่อนไขเขียว/แดงของ step
🔴 ข้อควรระวังเดียว: `-s` ทำให้ stdout ของทุกเทสไหลลง log ⇒ ถ้า log ยาวเกินจนตัด ให้ใช้
`Tee-Object` + `Select-String` อย่างข้างบน แทนการปล่อยดิบ

## ที่นี่ทำเองไม่ได้เพราะอะไร
`.github/workflows/` ไม่อยู่ในเขตเขียนของ LANE-DB (charter `20260901_1100`)
