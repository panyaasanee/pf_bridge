# R151 (z7ojme) — เลนลูทก้าวที่เดินได้จริง: inbound listener `PickupTerrainThing` (decode-count-and-record) + แก้ doc stale 2 จุด

- เวลาเริ่ม: 2026-08-24 ~16:50 (+07:00) · เซสชัน: z7ojme
- ล็อก: PR #52 (draft) `pf_bridge` เปิดเป็นอย่างแรกก่อนงานทั้งหมด (ลำดับ v5 ข้อ 3 · empty commit `c482337`)
- probe: GitHub API ใช้ได้ (list PR ทั้งสอง repo + create PR สำเร็จ) · ทาง D มีชีวิต (`git ls-tree origin/ci-status ci/` exit 0)
- โครงพี่น้อง: `VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง ✅
- กล่องจดหมาย: **ไม่มีใบใหม่** (ทุก `.md` ขาเข้ามี stub `.CONSUMED.txt` คู่ครบ — ตรวจด้วยกฎ stub ตัด `.md`)
- main ทั้งสอง repo ไม่ขยับตั้งแต่ R150 (`497681c` / `543382c`) · ไม่มี PR ค้างทั้งสอง repo ณ ต้นรอบ

## เหตุผลที่รอบนี้เลือกเลนลูท (backlog census)

- ใบ attended ทั้งหมดพักตามคำสั่ง 16:56 (23 ส.ค.) รอคุณ Panya · RE เปิดค้างใบเดียวคือ RE-062 (งานสะพาน)
- จดหมาย 1244 (ผู้ช่วย + Panya ท้วงยืนยัน) ชี้เป้า `monster_spawn_and_loot` และเสนอเป็น "เลนโค้ด"
- R147 นิยามเกตแล้ว: D1 encoder `ItemOperateVitalRes` มีอยู่แล้ว (inventory.py 3 ทรง) · D2 เกตจริง = body
  ทรง acquire ยิงบรรทัดเขียว id 131 ไหม (client-observable — ตอบได้ด้วยใบ GT เท่านั้น) · D3 **เส้นส่งมอบยังไม่มี**
- R149 ปิด RE-059 (golden hex 5 เฟรมจริงของ `0x4C13`) + RE-060 (สคีมรหัสไอเทม `full_id/100000`)
  ⇒ วัตถุดิบของเส้นส่งมอบครบเป็นครั้งแรก — ชิ้นที่ขาดคือ server ตอบคำขอเก็บของด้วยทรง acquire

## ผลขุดข้อเท็จจริง (pf-static-re · committed artifacts ล้วน)

ลูกมือ static ไล่ครบทั้ง external/ · gamedata/ · จดหมาย GT-046/GT-049/RE-059 · ซอร์สเรา — ข้อสรุปที่เปลี่ยนขอบเขตรอบ:

- **เส้นส่งมอบเต็ม (pickup → acquire Res → บรรทัดเขียว) ยังสร้างแบบยืนบนข้อเท็จจริงไม่ได้** เพราะ:
  ① opcode ของ `PickupTerrainThing` เป็นค่า **DERIVED `0x4543`** จาก name-hash — slot `.data 0x0108202C` เป็นศูนย์บนดิสก์
  เติมตอน runtime เท่านั้น (จดใน `IMAGE_ACCESS_COST.tsv` แถว 13 แล้ว) · corpus มีเฟรมทิศไหนก็ตาม **0 เฟรม**
  (`PF_FIELD_VALIDATION.tsv:102-103`) ② ไม่รู้ว่า client ใส่อะไรใน `+0x14` สำหรับ element ที่เรา spawn
  (GT-046 พิสูจน์แค่ "copy จาก `[ptr+0x10]` ของ runtime drop-object" — ยังเชื่อมกับ element_key ของ GROUND-LOOT ไม่ได้)
  ③ ไม่รู้ทรง `0x4C13` แบบไหนยิง MESSAGE id 131 — GT-049 พิสูจน์ทาง static path อย่างเดียว · เลน static
  ของคำถามนี้ประกาศหมดแล้ว (ใบ RE-059 เกณฑ์จบ) เป็นคำถามเปิดรอ Panya
- **สิ่งที่สร้างได้จริงวันนี้:** codec ของ `PickupTerrainThing` **ปิดสนิทเชิง static** — 2 ฟิลด์
  (`0x14` u32 @+0x14 · `0x08` u8 @+0x18) W/R mirror · gate ALWAYS · span `[0x005E5E30,0x005E5E83)`
  (`PF_SERIALIZER_FIELDS.tsv:859-862`) ⇒ เข้าแบบ R140 (LEARN-SKILL-REQUEST-001) ได้พอดี:
  **inbound listener แบบ decode-count-and-record · ไม่ตอบ ไม่เขียน DB · opcode DERIVED ติด nonclaim ดัง**
- **คุณค่า:** ถ้ารอบ attended (26 ส.ค.) มีการคลิกของบนพื้น server เราจะบันทึกเฟรมจริง ⇒ ตอบ unknown
  สามข้อแรกฟรี (opcode จริง · ไบต์เฟรมจริง · `+0x14` คืออะไร) — และถ้า opcode DERIVED ผิด เฟรมจะโผล่เป็น
  unknown-opcode ตามพฤติกรรมเดิมของ runtime ซึ่งอ่านผลได้เหมือนกัน (falsifiable สองทาง)
- **ของ stale ที่ลูกมือจับได้ 2 จุด (แก้รอบนี้):** ① `loot_roll.py:17-20` ยังอ้างว่า PickupTerrainThing
  "ไม่มี transport/serializer/producer" — เท็จตั้งแต่ GT-046 · ② `FUNCTIONAL_COVERAGE.json` แถว
  `monster_spawn_and_loot` ยังเรียกมันว่า "pre-placed quest-object system" — สมมติฐานนั้นถูก erratum 15:20
  (23 ส.ค.) ถอนไปแล้ว

## งานรอบนี้

- เปิดเลนโค้ด **HYP-PF-036 PICKUP-LISTENER-001** (ลูกมือ implement ตามแบบ HYP-PF-034 · ledger/verifier/เทสครบ)
- แก้ doc stale 2 จุดเป็น dated amendment
- baseline สวีตเต็มบน clone สดก่อนแตะอะไร: **2103/324/0 เขียว(cloud sanity)** ✅

## ผล implement (ลูกมือ general-purpose · ยังไม่ commit จนกว่า adversary ผ่าน)

- โมดูลใหม่ `src/pirateforce_foundation/pickup_listener_hypothesis.py`: strict decoder 2 ฟิลด์
  (`object_ref_u32` tag `0x14` @+0x14 · `opaque_u8` tag `0x08` @+0x18 · body 7 ไบต์ · pin span sha
  `8e439d4f…773066`) · decode-count-and-record ล้วน — ไม่ตอบ ไม่เขียน DB ไม่ตั้ง timer
- gating ตามแบบ HYP-PF-034 เป๊ะ: opt-in `--pickup-listener-hypothesis-scenario` + allowlist JSON +
  บังคับ `--db` ที่มีจริง + mutual exclusion กับทุกโหมด · ไม่มีแฟล็ก = บูต byte-identical baseline (มีเทสเทียบ)
- hook ใน `runtime.py` ที่จุดเดียวกับ `0x36AA` · **ข้อเท็จจริงที่จดไว้ในโมดูล:** เฟรม nested vital id
  ที่ไม่ match branch ไหนตกลง frozen v141 dispatch = ไม่มี reply/ไม่มี error (นอกจาก one-time ack เฟรมแรก)
  ⇒ ถ้า opcode DERIVED ผิด รอบ attended ยังอ่านผลได้ (เฟรมโผล่นอก branch เรา)
- เทสใหม่ 45 (golden + refusal ครบ 4 ทรง + nonclaim opcode DERIVED เป็นชื่อเทส + containment)
- ledger HYP-PF-036 (append-only · verifier PASS **entries=44**) · pin ขยับพร้อมกันในชุดเดียว:
  `CANONICAL_CONTENT_SHA256 → 22CFE14E…` · `GRADE_SUBSET_SHA256 → BC582520…` (บทเรียน R147)
- แก้ doc stale 2 จุดเป็น dated amendment (`loot_roll.py` · `FUNCTIONAL_COVERAGE.json` แถว
  `monster_spawn_and_loot` — ถอนถ้อยคำ pre-placed · คง caution FightingDrop* · เติม evidence_refs)
- **สวีตเต็มหลังงาน: 2148 passed / 324 skipped / 0 failed — เขียว(cloud sanity)** (จาก baseline 2103+45)
- guard ที่สะดุดระหว่างทาง: seam scan token `ShowMessage` ใน docstring — แก้ถ้อยคำโมดูล ไม่แตะ guard

## ประเด็นที่ chief ส่งให้ adversary ชั่งเป็นพิเศษ

- mutual exclusion ⇒ เปิด listener พร้อม `--ground-loot-hypothesis-scenario` (ตัว spawn ของให้คลิก)
  **ในบูตเดียวไม่ได้** — คุณค่า "บันทึกคลิกจริง" จึงมีเงื่อนไข · การอนุญาต compose scenario เป็นเรื่อง
  สถาปัตยกรรม = ต้องให้คุณ Panya เคาะ ไม่ตัดสินเองในรอบนี้

(ผล adversary · queue · commit/PR จะเติมท้ายรอบ)
