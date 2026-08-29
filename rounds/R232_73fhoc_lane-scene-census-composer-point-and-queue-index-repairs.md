# R232 (73fhoc) — จุดเสียบสำมะโนต่อฉากของสาย + ซ่อมสารบัญคิวสามใบ + ปลดทาง tool ของกะ3-A
2026-08-29T20:11+07:00 · chief (LANE-E)

## งานหลัก: CORE-REQUEST สาย A 1845 ต่อสายจบในรอบเดียวกัน

- `lane_hooks/__init__.py`: ทะเบียน `census_composer(scene_id)` (หนึ่งฉากหนึ่ง composer ·
  ใบแรกชนะ · ใบซ้ำ `LANE_HOOK_DUPLICATE` ดังบน stderr) + `SceneCensusResult` contract +
  `scene_census_composer()` lookup + `announce_direct_fire()` + `_withdraw()` ครอบ composer ด้วย
- `runtime.py`: elif เดียวหลังสาขา bg0002 ก่อน skipped-not-home — อ่าน production_allowed
  แบบ (b) ก่อนเรียก · fail-closed ตาข่ายเดียวกับ bg0002 · decline (None) = latch ชื่อชัด ·
  labels `WORLD_CENSUS_LANE_SCENE<id>_INITIAL/_REAPPLY`
- 🔴 กันฉาก 1/2 โดยโครงสร้าง: composer ของฉาก 1/2 ไม่มีวันถูกเรียก (เทสพิน)
- เทส: `test_lane_scene_census_wiring.py` 6 ใบบน dispatcher จริงที่ฉาก 278 (Bg1177) +
  `test_lane_hooks.py` +7 ใบ registry · mutation-kill 3/3 (lookup / เกต / การ์ดฉาก 1)
- สวีตเต็ม 4984 passed / 323 skipped / 0 failed เขียว(cloud sanity) · ledger PASS 47 ไม่ drift (เลข skip รายงานคู่ pass ตามที่ adversary ทวง)
- WIRED v2: จุดยิงใหม่ `LANE_HOOK_FIRED <module> scene_census_composer:<id>` (stderr) —
  ยังไม่มี composer จริงบนดิสก์จนสาย A เขียน lane_a_*.py รอบถัดไป = ยังไม่มี emission จริง
  บน production path รายงานตรง ๆ ไม่นับ 
- pf-adversary หักได้จริง 2 HIGH + 4 MED + 3 LOW — แก้ครบก่อน commit:
  - HIGH-1 [วัดแล้ว]: draft แรกบริโภคผล composer นอก try — SceneCensusResult ที่ type ถูกแต่ค่าเน่า
    unwound listener thread หลัง log committed (false green) ⇒ ย้ายทุกอย่างเข้า try + coerce ทุก field
  - HIGH-2 [วัดแล้ว]: ไฟล์ lane ที่ลงทะเบียนแล้วพังกลาง import ทิ้ง claim ซอมบี้บล็อกสายอื่น
    ⇒ _discover ถอน claim ของโมดูลที่ import ล้ม + print REGISTERED ก่อน insert
  - MED-3 [วัดแล้ว]: console_lines ของสายพิมพ์ดิบ ตาย cp874 ⇒ console_safe ทุกบรรทัด
  - MED-4 [วัดแล้ว survivor]: การกันฉาก 2 อยู่ที่ลำดับ elif อย่างเดียว ทั้งสวีตมองไม่เห็นการยก
    ⇒ เพิ่ม conjunct != SCENE2_N_ID ในเงื่อนไข + เทสฉาก 2 (ตอนนี้ต้องถอดทั้งคู่ถึงพัง ซึ่งเทสจับ)
  - MED-5: pc_bytes/frame_bytes เป็นคำอ้างของสาย ⇒ ตัดออกจาก contract ใช้ len() ของ payload จริง
  - MED-6 [วัดแล้ว]: composer จากโมดูลนอกแพ็กเกจลงทะเบียนได้แต่ผ่านเกตไม่ได้ตลอดกาล (เงียบ)
    ⇒ REJECTED ดังตอนลงทะเบียน
  - LOW-7/8/9: console_safe บน REGISTERED · FIRED token ยิงเฉพาะ commit path · เทส decorator return
    + multi-scene withdraw
  - คำถามดีไซน์ที่ adversary ทิ้งไว้ (จดเป็นหนี้ ไม่ใช่ของรอบนี้): world_census_sent/refused เป็น latch
    ราย session แต่คำถามเป็นราย scene — ตอน BUILD-002 มี travel กลาง session ต้องออกแบบ re-arm ราย
    ฉาก + reset last_target_pos ตอนเปลี่ยนฉาก ไม่งั้น anchor เก่าข้ามแมพ · สาขานี้ยัง production-
    unreachable จนกว่ามีอะไร seed ตัวละครนอกฉาก 1 (ตรงกับที่เทสระบุเอง)

## จดหมาย (บริโภค 6 ใบ + stub ครบ)

- 1845 (CORE-REQUEST สาย A) → ต่อสายแล้ว + จดหมายตอบ 2009
- 1912 (ผล RE-150 — ใบของ chief) → ปิดหัวใบ DONE/BOUNDED-NEGATIVE: ไม่มีมอน aggro
  นอกบล็อก 101-104 ที่เจ้าของปฏิเสธใน bg0001/Bg0002 ⇒ นัย M6 เป็นของสาย B + COO
- 1852/1904/1919 (กะ3-A) → ซ่อมคิวตามด้านล่าง + จดหมายตอบ 2009
- 1902 (สถานะสาย B) → FYI รับทราบ

## ซ่อมคิว (GAME_TEST_QUEUE.md / CLIENT_RE_QUEUE.md)

- GT-063: canonical = PASS R158 · UC1/R230 = replication · ถอนคำอ่าน R230 ที่ขัดโมเดล R158
- GT-064: สารบัญขีด READY ค้าง → CLOSED PASS(P2) R158 (archive)
- GT-001: PASS รอบ UA1 — `OBSERVER_CONFIRMED: 2026-08-29T19:1x+07:00 โดย Panya` (ใบ 1919 §①)
  HOLD ปลดตาม v6.3 §18.7 · recurring คงเปิด
- RE-150: ปิดตามผล runner
- rebuild สารบัญเต็ม (36 ใบไม่มีบรรทัด + 8 บรรทัดค้าง): **รอ QUEUE_STATUS_SNAPSHOT.md เดินทาง**
  — แก้ `pf_git_sync.ps1` $ALLOWLIST เพิ่ม `tools_bridge` + `QUEUE_STATUS_SNAPSHOT.md` แล้ว
  (selftest sync รันบน cloud ไม่ได้ ไม่มี PowerShell — ฝั่งสะพานดู sync.log รอบแรกหลัง pull)

## ที่ไม่ได้พิสูจน์ / หนี้

- จุดเสียบใหม่ยังไม่มีผู้ใช้จริงจนสาย A ลงทะเบียนฉาก 278 — wiring proof ของ composer จริง
  เป็นของ PR สายนั้น
- trigger-on-arrival สำหรับฉากของสาย (แบบ bg0002) ยังไม่ทำ — ต้องมีใบขอแยก
- chief ยังไม่ได้ swap จุดเรียก Bg0002 เป็น `ledger=self.mob_combat_ledger` ตาม COO 1941
  (path 3) — รอสาย B ลง (ก)+(ข) บน main ก่อน ตามลำดับในใบ

## สถานะ

push แล้ว รอ merge PR (เลขใน PR body ทั้งสอง repo) — งานอยู่บน main ต่อเมื่อรอบถัดไปเห็น merged=true
