# R381 (`ky8m6j`) — แถวหุ่น RE-155 ไปกับ census **เฟรมเดียว** (แก้ของที่รอบก่อนทำผิด ก่อนที่มันจะไปถึงเครื่องเจ้าของ) + ด่าน `.claude/` ตาม PANYA-ORDER `0316` ข้อ 4

เริ่ม 2026-09-07T03:21+07:00 · claim `pf_bridge#1617` · ไม่มี `[LANE-E] round *: claim` เปิดค้างตอนล็อก
(ใบที่เห็นตอนล็อก: `#1616` UI · `#1615` K · `#1614` CS · `#1613` B · `#1610` Q · `#1595`/`#1583`/`#1493` addendum)
สะพานมีชีวิต (`_BRIDGE_HEARTBEAT.txt` 03:18:02 · ห่างจากเวลาเริ่มรอบ 3 นาที)
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 B) — โครงพี่น้องไม่พัง

## รอบนี้ขยับ NOW/M ข้อไหน
- **M3 (P-2 สีชื่อ) — ขยับตรง ๆ**: `GT-288`/`RE-155` เป็นใบที่ NOW วางไว้อันดับ 1 ของ "รอเครื่องคุณ" และรอบก่อน
  ต่อสายให้แล้ว **แต่ต่อผิดจนใบนั้นบูตแล้วจะได้ผลลวง** รอบนี้แก้ให้บูตได้จริง ก่อนที่ K จะเอาขึ้นรถบัส
- **PANYA-ORDER `0316` ข้อ 4 (chief)** — ปิดในรอบที่คำสั่งมาถึง
- ไม่ขยับ: ลำดับ NOW ข้อ (2) `gate-windows` failure-detail · ข้อ (3) `AGENTS.md` ≤30 KB · ข้อ (4) `#948` seed
  เหตุผลเขียนไว้ท้ายไฟล์ "รอบหน้าทำอะไร" ไม่ใช่เพราะลืม

## งานที่ 1 — sweep ไปกับ census เฟรมเดียว (`pirate-force-server` PR ของรอบนี้)

**ทำไมมันเร่งด่วนกว่าลำดับใน NOW**: `rounds/R380_52u95a_addendum_adversary_after_unlock.md` (D2) เขียนไว้เองว่า
"ทางแก้ที่ถูก และเป็นงานแรกของรอบหน้า" และผมส่งจดหมาย `0345` บอก LANE-K ให้หยุดจัดคิวจนกว่าจะแก้
ใบที่ค้างแบบนั้นคือใบที่กันเวลาเครื่องเจ้าของไว้ทั้งกอง

**ของเดิมผิดยังไง (หลักฐานในบ้าน ไม่ใช่ความเห็น)**: `RE-092` (2026-08-26 22:23) วัดว่า remote-actor consumer
ของไคลเอนต์เป็น **replace-by-omission ระดับ collection** ⇒ เฟรมหุ่น 8 ตัวที่ส่งเป็น collection ใบที่สอง
ไม่ได้ "เพิ่มหุ่นเข้าเมือง" แต่ **แทนที่เมืองด้วยหุ่น** ⇒ `N-BASE` ที่เป็นตัวควบคุมเทียบกับ NPC จริงไม่ได้อีก
(ขัดเจตนา PANYA `2142` ที่ให้วางในเมืองก็เพื่อการเทียบนี้)

**สิ่งที่ลงไปจริง** (3 ไฟล์ src + 1 ไฟล์เทส):
1. `world_population.append_census_entries()` — พี่น้องสาธารณะของ `apply_identity_override`:
   อันนั้น **แทนที่** ไบต์ของ identity ที่ census มีอยู่แล้ว อันนี้ **ต่อท้าย** ร่างที่ census ไม่เคยมี
   เดินด้วย `WIRE_HEADER_BYTES` + `generation.entry_bytes` ชุดเดียวกัน เข้ารหัสด้วย encoder ตัวเดียวกัน
   🔴 **ไม่ขยาย `generation`**: `actor_count` ถูกส่งกลับเข้า `build_world_population` ทุกครั้งที่ recompose
   ซึ่งปฏิเสธค่าเกิน `CENSUS_COUNT` — ขยายตรงนั้น = ทุกการตีครั้งแรกกลายเป็น compose failure = RE-092 บอกว่าเมืองหาย
2. `name_colour_sweep.sweep_entries()` — ลูป entry ที่เคยอยู่ใน `build_sweep_population` ยกออกมา ไม่เปลี่ยนพฤติกรรม
   (`build_sweep_population` เรียกมันต่อ ผลไบต์ต่อไบต์เท่าเดิม เทสของ LANE-B เขียวครบ 58 เคส)
3. `name_colour_sweep.unrecognised_env_value()` + บรรทัด `NAME_COLOUR_SWEEP_UNARMED value=<ascii>` (D7):
   `PF_NAME_COLOUR_SWEEP=true` เคยบูตเงียบสนิท **แยกไม่ออกจาก "บิลด์นี้ไม่มี sweep"**
4. `runtime.py` ผนวก entry เข้า `census_pc/census_frame` ⇒ ทั้ง INITIAL และ REAPPLY ถือแถวนั้น
   ⇒ **คำถามจังหวะ 3.5 vs 0.0 ที่รอบก่อนเถียงทั้งย่อหน้า หายไปทั้งหมด** (D1 ปิดโดยไม่ต้องแก้เลข)
   label เติมท้าย `_SWEEP_<n>` เพื่อให้บรรทัด **ตอนส่ง** ของ v141 (`[G>] <label> (N bytes)`) พิสูจน์ว่าแถวออกไปจริง
   ไม่ใช่แค่ประกอบเสร็จ (D9)
5. ทุก refusal จับ `Exception` ไม่ใช่ `NameColourSweepError` (D3): สองคลาสนั้นเป็น **พี่น้อง** (subclass ของ `ValueError`
   คนละสาย) การจับแบบเดิมไม่เคยครอบ `load_roster`/`hostile_npc_attr` ที่เส้นทางนี้เดินผ่าน และหลุด = เธรด listener ตาย
   (v141:7440 ไม่มี except) · เพิ่มการปฏิเสธเสียงดังเมื่อ diag_multi_object เปิดอยู่พร้อมกัน (ไม่งั้นการผนวกจะลบร่าง diag ทิ้งเงียบ ๆ)

**หลักฐาน (ชั้น wire/headless — ไม่ใช่จอ)**
- `WORLD_CENSUS_INITIAL_108_SWEEP_8` + `WORLD_CENSUS_REAPPLY_108_SWEEP_8`, **collection เดียว**,
  pc 21,877 B เทียบกับ census ล้วน 20,446 B · `NAME_COLOUR_SWEEP_ARMED actors=8 census_actors=108`
- เทส 21 เคส (15 wiring + 6 บน helper ใหม่) · เคสที่สำคัญที่สุดคือ `test_no_second_collection_is_ever_queued`
- **มิวแทนต์**: ตัด `merged.extend(entries)` ออกจาก `append_census_entries` ⇒ **10 เคสแดง** (คืนค่าแล้ว 21 เขียว)
- เส้นทาง refusal **ถูกรันจริง** ไม่ใช่เขียนไว้เฉย ๆ (D5): มิวแทนต์ `FieldMobContractError` ผ่าน `sweep_entries`
  ⇒ census สองใบยังคิว ไม่มี suffix มี event `name_colour_sweep_refused_FieldMobContractError` และเธรดไม่ตาย
- `pf_gate_preflight.py --repo <server>`: **PREFLIGHT PASS**
- ชุดเต็ม: ดูบรรทัด "ชุดเต็ม" ท้ายไฟล์

**สิ่งที่ยังผิดอยู่และเขียนลงใบ attended แทนที่จะเงียบ**: การตีที่ถูกรับจะ recompose census ใหม่ที่ไม่มีหุ่น ⇒ แถวหาย
· `/warp` ออกแล้วกลับ ปลดล็อก census ใหม่ · หุ่นยืนที่ anchor แช่แข็ง (`V135_PLAYER_*`) ไม่ใช่ `last_target_pos` ของ census (D4)
⇒ จดหมาย `0341` ถึง LANE-K สั่งว่า "อย่าตีระหว่างเก็บผล · อ่านแถวที่จุดเกิด"

TWO_SESSIONS_SAME_SCENE: **ถูก** — `sweep_entries` เป็น pure function ของ (anchor แช่แข็ง, env) ไม่เขียน registry
สอง session ในฉากเดียวกันประกอบไบต์ชุดเดียวกัน · **NONCLAIM**: เป็นสำเนาคนละชุดที่ตรงกัน **ไม่ใช่**แถวเดียวใน registry ของ LANE-A
· หุ่นถูกกันออกจาก `mob_combat_announced_membership` โดยตั้งใจ (อ่านสีอย่างเดียว ตีไม่ได้) — อะไรที่จะทำให้ตีได้
ต้องผ่าน registry ของ A ตามกฎ shared world (PANYA `1057`/`1140`) ไม่ใช่เติมบรรทัด membership

## งานที่ 2 — ด่าน `.claude/` (PANYA-ORDER `0316` ข้อ 4 · `pf_bridge` PR ของรอบนี้)
`.claude/settings.json` ตั้ง `bypassPermissions` ให้ทุกเซสชัน ⇒ **`permissions.deny` คือตาข่ายชั้นเดียวที่เหลือ**
ระหว่างรอบหนึ่งรอบกับ `git push --force` ไฟล์ที่ทำหน้าที่นี้แก้โดย "ใครก็ได้ที่บังเอิญเปิดรอบอยู่" ไม่ได้
- `tools_bridge/pf_gate_preflight.py`: ด่าน `[claudecfg]` — แดงเมื่อกิ่งแตะ `.claude/` **ในรีโปใดก็ตาม**
  โดยไม่มีหลักฐานว่าเป็นรอบ chief/COO · ต่อสายทั้งโหมด `--bridge-only` (ที่ workflow ของ R378 ใช้) และโหมดเต็ม
- 🔴 หลักฐาน = **ไฟล์รอบ ไม่ใช่ป้ายใน title ของ PR** (title พิมพ์มือตอนท้ายรอบ เขียนอะไรก็ได้)
- `--self-test` +6 เคส รวม "LANE-A แก้ deny list ⇒ False" และ "base ไม่ resolve ⇒ None (ไม่ใช่ผ่าน)" · **74/74 เขียว**
- `PROCESS_GATES.md` ข้อ 27 = เอกสารครึ่งหลังของคำสั่ง
- **ไม่แตะ `AGENTS.md` โดยตั้งใจ**: main ถือ 44,385 B เทียบเพดาน 30 KB — เกตวัด "โตขึ้นบนกิ่งนี้ไหม" หนี้เก่าจึงนั่งเงียบได้
  เติมบรรทัด = ทำให้กิ่งตัวเองแดง และถูกแล้วที่แดง ⇒ ส่งเป็นคำถามให้ COO (ตัด หรือยกเพดาน — ผมเสนอให้ตัด)
- ข้อ 1-3 ของใบ `0316` (เนื้อ deny list · ถอด `enableAllProjectMcpServers` · พิสูจน์สองข้อ) = **ของ COO** ไม่ทำแทน

## กล่องจดหมาย
- บริโภค: `20260907_0148_COO-DECISION-chief0057-...` (stub ในคอมมิตเดียวกัน) — ไม่มีงานค้างจากใบนั้น
- อ่านแล้วไม่ใช่ของ chief รอบนี้: `0316` (ADDRESSEE: COO cc chief — ทำเฉพาะข้อ 4 ที่ระบุชื่อ chief),
  `0039` SYNC-ALARM (4 ใบไม่มีใครรับ · หนึ่งในนั้น `1215` GM-063 อยู่ในลำดับ NOW ข้อ (5) ของผมแล้ว)
- เขียนใหม่ 3 ใบ: `0341` ถึง K (บล็อก `ATTENDED:` ใหม่ แทนของใน `0250`/`0345`) · ถึง B (แตะโมดูลตรงไหนบ้าง) · ถึง COO (ข้างบน)

QUEUE_TRIAGE: ไม่แตะไฟล์คิวรอบนี้ (เจ้าของ = LANE-K ตาม PANYA `1259`) · chief ส่ง **เนื้อใบ** ให้ K ทางจดหมาย `0341` ตามช่องทางที่ NOW กำหนด
READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ: ไม่มีเพิ่มจากรอบนี้ — `GT-288` ยังเป็นใบเดิมของ NOW ข้อ 1 และรอบนี้ทำให้มันบูตได้จริง
`WIRED = 1 โมดูลที่มี emission จริงบน production path (name_colour_sweep ผ่าน append_census_entries ที่ arrival census) / เลน production_allowed: ไม่เพิ่มเลนใหม่ ทั้งก้อนอยู่หลัง env PF_NAME_COLOUR_SWEEP ที่ปิดโดยปริยาย`
BYTECODE_PURGED: ล้าง `__pycache__` ด้วย `find -exec` (ไม่มี `rm -r` ในรอบนี้ ตาม PROCESS_GATES ข้อ 26)

## ลูกมือ
`pf-adversary` สั่งต้นรอบพร้อมเริ่มงาน (ตาม COMMON) บนกิ่ง `claude/eloquent-edison-ky8m6j` — คำถาม A-E เขียนไว้ให้หักล้าง
การผนวกเข้า census, membership, ความปลอดภัยของ helper ใหม่, ระยะวาดของ anchor แช่แข็ง และทางที่ใบ attended จะได้ผลลวง

## รอบหน้าทำอะไร
1. ผล `pf-adversary` ของรอบนี้ (ถ้าคืนหลังปลดล็อก = งานแรกของรอบถัดไป ตามกฎบ้าน)
2. NOW ลำดับ (2): `gate-windows.yml` — บล็อก `--- pytest_subset failure detail ---` ของ R350 **ไม่พิมพ์เลย**
   ใน run `34045847454` (COO วัดเอง ใบ `0148` ข้อ 2 + GM `0123`) และ `FAILED/ERROR` ท้าย job (`1921`)
3. NOW ลำดับ (3): ตัด `AGENTS.md` ลงใต้เพดาน (รอคำเคาะ COO ตามจดหมาย `0341`) + กฎ `2241`/`2345`/`0039`
4. NOW ลำดับ (4): `#948` seed แขน (ข) + conftest · (5) ตอบ GM `1215` GM-063
5. ส่งใบยืนยันให้ K เมื่อ PR ของรอบนี้ merge ("เฟรมเดียวอยู่บน main แล้ว" = สัญญาในจดหมาย `0345`)

SCOREBOARD: COMING | ผู้เทสที่บูต PF_NAME_COLOUR_SWEEP=1 จะเห็นแถวหุ่นติดป้าย 8 ตัวยืนอยู่ในเมืองที่ NPC ยังอยู่ครบ แทนที่จะเห็นเมืองว่างเปล่า (ซึ่งคือสิ่งที่โค้ดเมื่อวานจะทำ) | pirate-force-server PR ของรอบ ky8m6j · pf_bridge#1617 · GT-288
