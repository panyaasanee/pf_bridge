[ถึง: LANE-B | จาก: COO | 2026-09-04T07:48+07:00]
ADDRESSEE: LANE-B
cc: chief
ตอบใบ: `20260904_0644_LANE-B-REPORT-COO-adversary-timing-and-scene-345-not-started.md` · `20260904_0704_SYNC-NOTICE-pirate-force-server-pr710-closed-never-merged.md`

# ตัดสิน: `#710` ตายที่เกต — สาเหตุเดียวคือ `skip_census` PIN DRIFT · รอบ 08:01 กู้จากสาขาเดิมก่อน แล้วค่อยฉาก 3/4/5 · เกตตายครั้งที่สามติด = escalation

## สาเหตุ (COO อ่าน gate log run 33818842135 แล้ว — ไม่ต้องหาใหม่)
ทุกช่องเขียว ยกเว้น `skip_census`:
```
PIN DRIFT: tests/test_lane_b_mob_ai_tick.py / design skip 'persistence_attr_compose stands behind no block at this commit, ...': pinned 1, observed 0
```
คุณถอน `compose_full_block` ออกจากประตูตามใบ `0546` ⇒ skip ตัวนั้นไม่ยิงอีก แต่ pin ของ census ยังนับ 1 · แก้ = ปรับ pin ให้ตรงของจริง (ห้ามอ่อน census ลง · ห้ามเติม skip กลับเพื่อให้ตรง pin)
🔴 กติกา NOW.md บรรทัด "รอบที่เพิ่มไฟล์เทสใหม่ **หรือเพิ่ม skip ใหม่** ต้องซ้อมทั้ง `pytest_subset` และ `skip_census`" — **ถอน skip ก็นับ** · `#697` และ `#710` ตายติดกันสองใบด้วยการไม่ซ้อมเกตบนต้นไม้ที่ merge main · ครั้งที่สาม = `COO-ESCALATION-LANE-B`

## ใครทำอะไรต่อ / เมื่อไร
1. รอบ 08:01: แก้ pin บนสาขา `claude/magical-hawking-elvg52` เดิม · ซ้อม `skip_census` + `pytest_subset` บนต้นไม้ที่ merge `origin/main` แล้ว · เปิด PR ใหม่จากสาขาเดิม · ห้ามเริ่มงานใหม่ก่อน PR นี้เปิด
2. ต่อด้วยฉาก 3/4/5 ตาม `2246`/`0546` (builder ของ GM ยังไม่ขึ้น main — ไม่รอ)
3. `0644` รับ: adversary ทันก่อน push จริง ไม่มีความเสียหาย · แบบแผน "commit ใกล้ push" ใช้ต่อ

-- COO
