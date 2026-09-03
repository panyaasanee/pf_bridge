# LANE-GM รอบ `re222v` — RE-222 ยืนยันว่ารูปเฟรม /speed ไม่ malformed กลไกคือของเดิมที่บันทึกไว้แล้ว

- รหัสรอบ: `re222v` · เริ่ม 2026-09-03T23:48+07:00 · เขียนไฟล์นี้ 2026-09-04T00:2x+07:00
- claim PR: `pf_bridge#1030` (ไม่ draft · ไม่มี marker จนกว่าจะจบรอบ)
- กิ่ง: `pf_bridge/claude/lane-gm-round-re222v` · `pirate-force-server/claude/lane-gm-round-re222v`

## รอบนี้ขยับ NOW ข้อไหน
**ไม่ขยับข้อไหนของ NOW โดยตรง** — งานรอบนี้คือบริโภคจดหมาย `RE-222-RESULT-PARTIAL` ที่ backlog ของ
รอบก่อน (`spt6fv`) ทิ้งไว้เป็นข้อ 1 ("บล็อกที่: สาย RE") RE-222 ตอบกลับมาแล้ว (static-only) และ
**ไม่ปลดล็อกอะไร** — ล็อก `/speed` ทั้งสองตัว (`SPEED_LOGIN_READ_LANDED` /
`SHAPES_CLEARED_BY_A_REAL_CLIENT`) ยังปิดเหมือนเดิม เพราะ RE-222 เป็น static ไม่ใช่การวัดบนจอ
สิ่งที่เปลี่ยนคือความสงสัยเรื่อง "รูปเฟรมอาจผิด" ใน NOW.md ถูกปิด (ดูหัวข้อ "สิ่งที่ทำ")

## ต้นรอบ — ล็อกและชะตา PR รอบก่อน
- list PR open ทั้งสองรีโป: `[LANE-GM]` = **ศูนย์ใบ** (มี `[LANE-E] #1026`/`[LANE-B] #684` ของสายอื่น
  ไม่แตะ) ⇒ เลนว่าง เปิด claim `pf_bridge#1030` แล้ว list ซ้ำ ไม่มีใบสายเดียวกันที่เก่ากว่า ⇒ ถือล็อก
- **ชะตา PR รอบก่อน (ข้อ A)**: `pirate-force-server#682` `merged=true` (วัดด้วย API) — งานของรอบ
  `spt6fv` อยู่บน main ครบ ไม่มีอะไรต้อง cherry-pick กลับ `pf_bridge#1027` ก็ `merged=true` เช่นกัน

## กล่องจดหมาย
- จดหมาย `ADDRESSEE: LANE-GM` ที่ไม่มี `.CONSUMED.txt`: ตรวจแล้ว **ไม่เจอใบใหม่** (สามใบจากรอบก่อน
  `2035`/`2050`/`2152` มี stub ครบแล้ว) — ใบที่หยิบมาทำงานรอบนี้ (`RE-222-RESULT-PARTIAL`) ไม่ได้ขึ้นต้น
  ด้วย `ADDRESSEE: LANE-GM` (เป็นผลของ RE lane ถึง chief) แต่เป็นคำตอบตรงต่อ backlog ข้อ 1 ของรอบก่อน
  จึงหยิบตามลำดับ "งานตามลำดับ" ข้อ 2 (คำตอบของ chief/RE ที่อ้างเลขของสายนี้)

## สิ่งที่ทำ

### บริโภค `RE-222-RESULT-PARTIAL`
Q0 ถอด 30 ไบต์ของ `ActorAttr` payload จริงจากเฟรม GT-218 เทียบกับตัวอ่านที่ถอดแอสเซมบลีแล้ว:
โครง tag/length **ถูกต้อง** ไม่ malformed · เส้นทาง apply `[0x00464F30,0x004652AC)` เขียนทับทั้ง
อ็อบเจกต์ (BasicAttr ที่สืบทอด + ทุกฟิลด์ ActorAttr) จากอ็อบเจกต์ที่สร้างใหม่ทุกครั้ง ซึ่ง constructor
zero HP/MP/cash **ก่อน** decode แตะมันด้วยซ้ำ — full-copy ไม่ใช่ merge

**นี่คือการยืนยันของเดิม ไม่ใช่ข้อมูลใหม่**: `gm/attr_wire.py` อ้างกลไกเดียวกันนี้มาตั้งแต่รอบ R281
("v141 note on 0x464F30") และ `gm/speed_wire.py` (คอมเมนต์ GT-193) ก็ให้เหตุผลจากมันอยู่แล้ว
RE-222 ยกระดับจากบันทึกที่ไม่เคยตรวจเป็นผล static RE ที่ SHA-pin แล้วชี้ที่อยู่เดียวกันเป๊ะ

### ตรวจ `CORE-REQUEST-GM-044` ก่อนเข้าใจผิดว่าเป็นของค้าง
แรกอ่าน `attr_wire.py` เห็นว่าอ้างถึง `CORE-REQUEST-GM-044` และเดา (ผิด) ว่ายังไม่มีคำตอบ เพราะ
`grep -rli` ในรอบแรกไม่เจอ (มันย้ายไป `archive/notes_to_chief_2026-08/` แล้ว) ตรวจซ้ำก่อนเขียนจดหมาย
**พบว่ามีคำตอบแล้ว NEGATIVE ตั้งแต่ 2026-08-31**: `characters.actor_wire` เป็น BLOB คนละตัว
(`AvatarAttr`/`CreateActorDataEx`) ไม่ใช่คอลเลกชัน DBAttribute ที่ `attr_wire.FIELDS` ใช้ ⇒ ไม่มี
แหล่ง raw-block สำเร็จรูปจาก DB ทางนั้น — **ไม่เปิดจดหมายเปล่าตามที่เกือบเข้าใจผิด**

## หลักฐาน / เทส
- ไฟล์ที่แตะ: `src/pirateforce_foundation/gm/speed_wire.py` ·
  `src/pirateforce_foundation/gm/attr_wire.py` (คอมเมนต์/docstring เท่านั้น — ไม่มีเกต ค่าคงที่
  หรือลายเซ็นฟังก์ชันไหนถูกแก้) · `docs/GM_LANE.md` — **ไม่มีไฟล์เทสใหม่ ไม่มี skip ใหม่**
  ⇒ ไม่เข้าเงื่อนไขซ้อม `pytest_subset`/`skip_census` (`COO 2344`)
- เทสของไฟล์ที่แตะ: `test_gm_speed_wire.py` + `test_gm_speed_shape_hold.py` + `test_gm_attr_wire.py`
  + `test_gm_speed_action.py` + `test_gm_speed_denied_notice.py` + `test_gm_speed_trial_gate.py`
  + `test_gm_speed_denied_nine_paths.py` + `test_gm_speed_deferred.py` + `test_gm_source_is_cp874_safe.py`
  → **348 passed, 233 subtests**
- `test_gm_source_is_cp874_safe.py` ผ่านตั้งแต่แรก (ข้อความใหม่เป็น ASCII ล้วน ตรวจ `.encode('cp874')`
  ด้วยมือก่อน commit)

## 🔴 nonclaim (G-OBS) — ใช้ GM ข้ามขั้นอะไรไปบ้าง
- **ไม่ใช้เลย** ไม่มีสถานะ GM ให้บัญชีไหน ไม่มีคำสั่ง GM ถูกยิง ไม่มีไบต์ออกจากซ็อกเก็ต ไม่มีจอเกี่ยวข้อง
- รอบนี้แก้เฉพาะคอมเมนต์/docstring สองไฟล์ + บันทึกไฟล์รอบหนึ่งไฟล์ — ไม่มีอะไรที่ผู้เล่นหรือผู้เทส
  ที่ไคลเอนต์เห็นเปลี่ยน
- **ไม่ได้อ้าง**ว่า `/speed` ปลอดภัยจะส่งแล้ว ทั้งแบบ sparse หรือ full — ล็อกทั้งสองตัวยังอยู่ที่เดิม
  ที่รอบ attended (`GT-193`) ทิ้งไว้ RE-222 เป็น static-only ปลดล็อกด้วยตัวเองไม่ได้

## backlog — อะไรบล็อกอยู่ที่ใคร
1. **`/speed` ยังต้องการแหล่งค่าฟิลด์สด** (HP/MP/cash ฯลฯ) ณ จุด dispatch เพื่อสร้าง full-object write
   ที่ปลอดภัย — **บล็อกที่: ไม่มีใครสั่ง** (`GM-044` ตอบ negative แล้วว่าไม่มีแหล่งจาก DB BLOB)
   สายนี้ไม่เปิด CORE-REQUEST เอง เพราะไม่มีคำสั่งให้สร้างประตูนี้ ถ้า COO/เจ้าของต้องการเดินหน้า
   /speed ต่อ ขั้นถัดไปคือสั่งให้เปิด CORE-REQUEST ขอจุดอ่านค่าสดจาก runtime.py
2. **`RE-222` resume checkpoint ข้อเดียวที่เหลือ** (selector-scene population path สำหรับ Q3/name-color)
   — **บล็อกที่: สาย RE** (ไม่ใช่ของรอบหน้าสายนี้โดยตรง P-2 ยังบล็อกที่เครื่องเจ้าของอยู่ดี)
3. **P-2 สีชื่อมอนสเตอร์ · P-3 ปุ่ม GM** — **บล็อกที่: เครื่องเจ้าของ** (`COO 1046`)
4. รอบถัดไปเริ่มจากเช็คกล่องจดหมายใหม่ตามปกติ ถ้าไม่มีของใหม่และ backlog ข้อ 1-3 ไม่ขยับ ให้ใช้กฎ F

## จดหมายที่ออกในรอบนี้
- `notes_to_chief/20260903_2348_LANE-GM-REPORT-COO-re222-confirms-the-frame-is-not-malformed-and-gm044-is-already-answered-negative.md`
- stub `.CONSUMED.txt` หนึ่งใบ + สำเนาต้นฉบับเข้า `consumed/` (`RE-222-RESULT-PARTIAL`)

## จบรอบ
- ชุดเต็มรันครั้งเดียวในรอบนี้ (ไม่มีการแก้หลังรันเต็ม): ผลลง `docs/GM_LANE.md`/PR ของเซิร์ฟเวอร์
- `tools_bridge/pf_gate_preflight.py --repo <server>`: รันแล้ว ผลลงบันทึกจบรอบของ PR เซิร์ฟเวอร์
- push ครบทั้งสองรีโปแล้ว
- **PR pirate-force-server** — เปิดตอนจบรอบ ไม่ draft `PF-AUTOMERGE: v4` อยู่ใน body ตั้งแต่เปิด
  GET ยืนยันแล้วว่า marker อยู่จริง — สถานะ: เปิดแล้ว รอ gate
- claim PR `pf_bridge#1030`: เติม `PF-AUTOMERGE: v4` ตอนจบรอบนี้ = ปลดล็อก
- ไม่รอ gate Windows ไม่รอ PR เซิร์ฟเวอร์ merge — ส่งมอบให้ reaper แล้วคือจบหน้าที่ของรอบ
