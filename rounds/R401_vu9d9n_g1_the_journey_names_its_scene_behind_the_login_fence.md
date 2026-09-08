# R401 · vu9d9n · 2026-09-08 12:22 → 12:37+07:00 +07:00 · [LANE-E]

ล็อกรอบ: `pf_bridge#1890` (`[LANE-E] round vu9d9n: claim`) · ไม่มีใบ `[LANE-E]` เปิดค้างตอน 12:22 (list ทั้ง 21 ใบ open ของ pf_bridge)
เวลาเทียบสะพาน: `_BRIDGE_HEARTBEAT.txt` บรรทัดล่าสุด 12:08:03 +07 · นาฬิกาผมอ่าน 12:22 ⇒ **ห่าง 14 นาที** ปกติ ไม่ต้องตรวจหลักฐานอิสระ
`VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง (11,388 ไบต์) · ไม่มี `LOCK_*.txt` โผล่ใน `git status` ทั้งสองรีโป

## รอบนี้ขยับ NOW ข้อไหน
**บันไดไมล์สโตน · ประตู M (`1825`/`1218`) โทเคน (ข)** = "chief G1 PR ย้ายจริง + เขียนถาวร บน main"
และบรรทัด **chief (1 งาน/รอบ)** ของ NOW: `PR แทน #1099 (R400 ✅) → G1 PR → adversary → undraft+marker`
ทำ G1 ครบในรอบนี้ · **ยังไม่ถึง main** — ใบเปิดแล้วเป็น draft ตามกติกา (ดูหัวข้อ "สถานะ PR ตามจริง")

## จดหมายที่บริโภครอบนี้
- `20260908_1218_PANYA-DECISION-...-ALL-LANES.md` หัวข้อ 2 (ADDRESSEE: chief) = โจทย์ทั้งรอบ · ใบ ALL-LANES **ไม่วาง `.CONSUMED.txt` ร่วม** ตาม NOW `0442` ⇒ อ้างเลข `1218` ที่นี่แทน
- `20260908_1142_LANE-GM-TO-CHIEF-R399-barred-login-set-is-derived-now.md` (ADDRESSEE: chief) — บริโภค + stub ในคอมมิตเดียวกัน
- `20260908_1214_SYNC-ALARM-4-letters-nobody-took-and-nobody-answered.md` (ไม่มีเจ้าของชัด ⇒ ของ chief) — บริโภค + stub

## สิ่งที่ทำ — G1 หนึ่งชิ้น หนึ่งใบ (2 ไฟล์ ไม่นับไฟล์รอบ/จดหมาย)
`runtime.py` ปลายทางของ echo OK (สาขาที่ตอบด้วย `encode_transport`) เรียกเมธอดใหม่
`_m2_transport_resync_selected_scene(order.pending)`:
1. อ่าน `world_m2_teleport_check.transport_relocation(pending)` (โมดูลของ LANE-A — ไฟล์นี้ไม่ derive อะไรเอง)
2. คืนก่อนพร้อม event ที่มีชื่อ ถ้าไม่มี position หรือฉากปลายทาง = ฉากปัจจุบัน
3. 🔴 **ปฏิเสธการ relabel เว้นแต่ `gm.warp_scene_persist.login_would_accept(scene_id)` = True**
4. ถ้าผ่าน: เขียน `selected.position.scene_id` (ฉากอย่างเดียว) · `scene_label_is_server_guess = True` · แล้วรัน **บล็อก KA1A-ROOTCAUSE ครบ**

`_checkpoint_exact_target` **ไม่ถูกแตะเลย** — แถวถาวรถูกเขียนที่ `TargetPos` แรกตามปกติของการเดิน ผ่านเกต
`is_position_persist_allowed` ที่อยู่ใน `lifecycle.checkpoint` อยู่แล้ว · **ไม่มีแฟล็ก ไม่มีกิ่ง VISIT ไม่มีการกันเขียนถาวร** ตาม `1218` ข้อ 2

## รั้ว: ทำไมใบนี้ลงก่อนหรือหลัง PR ของ LANE-A ก็ได้ (เบี่ยงจากลำดับที่ COO เขียน และนี่คือเหตุผล)
COO เขียนไว้ในใบ `1218` (ถึง A) ว่า "ถ้า chief G1 ลงก่อนคุณ = ช่อง brick เปิดชั่วคราว ดังนั้นคุณต้องไปก่อน"
**ผมไม่ได้ขอให้สลับลำดับ — ผมเอาช่องนั้นออกจากโค้ด**: เมธอดนี้ relabel เฉพาะฉากที่ล็อกอินรับกลับได้
⇒ วันนี้ (วัดเอง: `login_entry_allowed` ของ 17/126/304/305 ยังเป็น `false` บน origin/main) มันปฏิเสธพอดีสามฉากที่จะ brick
⇒ วันที่ PR ของ A ลง มันย้ายทั้งสามฉากทันที โดยผมไม่ต้องแก้อะไรอีก
รั้วนี้ **ไม่ใช่แฟล็กใหม่** — เป็น `login_would_accept` ตัวเดียวกับที่ `gm/warp_scene_persist.persist_warp_scene` ถามอยู่แล้ว
ที่ seam คู่ขนาน และเป็นกลไกที่ `1218` ข้อ 1 สั่ง **ให้คงไว้** เป็นรั้วของฉากไร้ spawn ในอนาคต

**และรั้วเดียวกันนี้จ่ายความเสียหายของ G2 ในบรรทัดเดียวกัน**: `login_would_accept` fail-closed ให้ปลายทางที่
ไม่ได้ pin / นอกช่วง wire / ไม่ใช่ int / ไม่มี spawn ⇒ `PendingCheck` ที่ถือปลายทางที่ไม่มีใคร resolve
ไม่สามารถส่งเลขฉากมั่วเข้า `Position` ได้อีก (R399 วัดได้ว่ามันทำได้ และตัวนอกช่วงไป raise
ออกจาก `is_position_persist_allowed` ที่เฟรมเดินถัดไป)

## หลักฐานสองชั้น — แยกกัน ไม่อ้างข้ามชั้น
- **ชั้น server state**: ปลายทางถูกปิด ⇒ ป้ายไม่ขยับ `scene_label_is_server_guess` ยัง False และการปฏิเสธ **มีชื่อ**
  (`lane_a_m2_transport_resync_refused_login_barred_<scene>`) · ปลายทางเปิด ⇒ ป้ายขยับ ธง guess ติด
  และ `lane_a_m2_transport_census_latch_cleared_<scene>` ยิง
- **ชั้น wire/DB**: บน registry ที่เปิด ล็อกอิน — เดินทาง + หนึ่งก้าว ⇒ `character_positions` ชี้ฉากปลายทาง ·
  บน registry อะไรก็ตามที่รันจริง — แถวที่เก็บได้ต้องเป็นฉากที่ `login_would_accept` รับ และ `StartGame` ยังตอบ
  (ข้ออ้างที่ relabel แบบไร้รั้วทำพัง)

## เทส + มิวแทนต์
`tests/test_m2_teleport_check_seam_wiring.py` — คลาส `SelectedSceneIsNotRelabelledTests` เดิมถูกเขียนใหม่เป็น
`SelectedSceneIsRelabelledOnlyWhenTheLoginCanTakeItBackTests` · **50 passed**
ครึ่ง "registry เปิด" พิสูจน์ด้วย registry ที่ดัดแทนการรอ PR ของ A (เทสที่รันได้ก็ต่อเมื่อใบคนอื่น merge = พิสูจน์ตามตารางของคนอื่น)
มิวแทนต์ที่ฆ่าได้รอบนี้ (วัดจริง ไม่ใช่คาด):
| มิวแทนต์ | ผล |
|---|---|
| ถอดรั้ว `login_would_accept` | 3 failed |
| ถอดบล็อก KA1A-ROOTCAUSE ทั้งก้อน | 1 failed |
| relabel x/y/z ด้วย | 1 failed |
| ตั้ง `scene_label_is_server_guess` ก่อน relabel | 1 failed |
| ไม่บวก `mob_combat_announced_membership_generation` | 1 failed |

🔴 **ความผิดของผมเองที่จับได้ในรอบ ไม่ใช่รอบหน้า**: ฉบับแรกของเทส census latch **วัดอะไรไม่ได้เลย** —
บนเซสชันใหม่ฟิลด์พวกนั้น falsy อยู่แล้ว ถอดบล็อกทั้งก้อนออกก็ยังเขียว 50/50 · แก้ด้วยการ latch เซสชันก่อน
(ตั้ง `world_census_sent=True` ฯลฯ) แล้วมิวแทนต์ถึงตาย — รูปเดียวกับที่ R399 เขียนไว้เองว่าเคยพลาด

## adversary
สั่ง `pf-adversary` **ต้นรอบพร้อมเริ่มงาน** ตาม COMMON (หลังคอมมิตแรกของโค้ด เพื่อให้ลูกมือมี diff จริงอ่าน)
พร้อมโจทย์ให้หักล้างสี่ข้ออ้างโดยตรง (ลำดับ merge · ความครบของบล็อก KA1A · ต้นทุนตอนปฏิเสธ · scene-only)
**ผลยังไม่คืนตอนปิดรอบ** ⇒ `ADVERSARY_PENDING pirate-force-server#1132` · **ห้ามอ่านใบนี้ว่า "ผ่าน adversary"**
รอบถัดไปของ chief: สั่ง adversary บนกิ่งนี้เป็นงานแรก แล้วจ่ายของที่เจอก่อน undraft

## สถานะ PR ตามจริง
- `pirate-force-server#1132` — **เปิดแล้ว draft ไม่มี marker** · draft เพราะ COMMON ข้อ 2: ใบที่แตะเส้นล็อกอินเป็น draft
  จนกว่า adversary คืน · **ไม่ได้อยู่บน main** และจะพูดได้ว่าอยู่ต่อเมื่อรอบถัดไปยืนยันด้วย `git merge-base --is-ancestor`
- `pf_bridge#1890` — ใบ claim ของรอบนี้ เติม marker ตอนจบรอบ = ปลดล็อก
- เกต: `pf_gate_preflight.py --repo <server>` = **PREFLIGHT PASS** (cp874 · ไม่มี skip ใหม่ · main อยู่ในกิ่ง · census ตรง)
  🔴 รอบแรกมันแดงที่ `[skips]` เพราะผมใส่ `self.skipTest` — NOW `2050` ห้าม skip/xfail/allowlist ทั้งสาม
  แก้ด้วยการ **ดัดแถวให้ปิด** แทนการ skip (fixture เดียวกันอ่านกลับด้าน) ⇒ สาขาปฏิเสธยังถูกเทสหลัง A ปลดธงด้วย
- ชุดเต็ม `pytest tests/` บนต้นไม้ที่ `git merge origin/main` แล้ว (main `a92086c` เป็น ancestor ของ HEAD): ผลอยู่ท้ายไฟล์นี้

## QUEUE_TRIAGE:
เลขใบ · เนื้อหัวใบ · การพับผล = **LANE-K** ตั้งแต่ NOW `1910` ⇒ รอบนี้ chief **ไม่แก้ `GAME_TEST_QUEUE.md` เอง** โดยเจตนา
สิ่งที่ต้องเปลี่ยนคือ **หัวใบ `GT-309`** (เงื่อนไขปลด: โทเคน (ก)(ข)(ค)) — โทเคน (ข) เกิดแล้วในรูป PR draft ยังไม่ถึง main
⇒ ส่งจดหมาย `*-to-LANE-K-*` ให้ K ขยับหัวใบ พร้อมประโยคที่ K วัดซ้ำเองได้ (`merge-base --is-ancestor`)
ไม่มีใบใหม่ที่ควรเปิดจากงานรอบนี้: G1 ไม่มีอะไรให้คนหน้าจอตัดสินจนกว่าโทเคน (ก) และ (ค) จะครบ — `GT-309` ครอบอยู่แล้ว
**READY/PENDING ที่ไม่อยู่ใน NOW รอเครื่องคุณ:** ไม่มีใบใหม่ที่ chief เปิดรอบนี้ · รายการรถบัสจริง = `QUEUE_STATUS_SNAPSHOT.md` ของ K
(`GT-288` ชุด 3 · `GT-304` · `GT-299`/`GT-307` · `GT-309` HELD) — ตรงกับ NOW "รอเครื่องคุณ" ทั้งสองข้อ ไม่มีใบตกหล่น

## หนี้แม่บ้าน (§9) ที่ผมวัดแล้วแต่ไม่จ่ายในรอบนี้ และบอกตรง ๆ ว่าทำไม
- `CHIEF_CONTINUATION.md` = **29,949 ไบต์** เพดาน 30,720 · ดัชนีมี **9 บรรทัด** (กติกาให้เก็บ 20) ⇒ **ตัดดัชนีไม่ช่วย** น้ำหนักอยู่ที่ §0
  บรรทัดของรอบนี้พาไปราว 30,4xx = ยังใต้เพดาน แต่เหลือที่ให้อีกแค่ ~1 รอบ · **นี่คืองานแรกของ chief รอบหน้า** (ใบเล็กแยก แก้ §0 ไม่ใช่ดัชนี)
- `GAME_TEST_QUEUE.md` = 975 KB (เพดาน 300 KB) — หนี้เก่า เจ้าของ archive = LANE-K ตาม `1910` ไม่ใช่ของผมที่จะไปตัด

## รอบหน้าทำอะไร (เรียงแล้ว)
1. 🔴 **adversary บนกิ่ง `claude/great-franklin-vu9d9n` เป็นงานแรก** → จ่ายของที่เจอ → undraft `#1132` + marker = โทเคนประตู M (ข)
2. `CHIEF_CONTINUATION.md` §0 ลงใต้เพดานอย่างมีที่เหลือ (ใบเล็กแยก)
3. **ใบ workflow ใบเดียว** (ค้างสามรอบ · COO `0642` ข้อ 1 + `0542` หัวข้อ 6): reportchars `fE` + tee `LANE_DB_SKIP_CENSUS`
4. จุดเสียบ presence ของ LANE-A (`20260907_2238` revision 2) · จุดเสียบสกิลของ LANE-CS ตามรูปใหม่ (`0623`)
5. กู้ `#1095` ด้วย cherry-pick (`0728`) → `#1084` D1/D3 → `AGENTS.md` ≤30,720 → `#1076`

## nonclaims
- **[วัดแล้ว] ฝั่งเซิร์ฟเวอร์เท่านั้น** — ไม่มีใครเห็นไคลเอนต์วาดการมาถึงหลังการแก้นี้ นั่นคือ `GT-309` จังหวะ (ค) ซึ่ง HELD
- ใบนี้เป็นโทเคน **(ข)** ของประตู M ไม่ใช่ตัวประตู · (ก) และ (ค) เป็นของ LANE-A
- ไม่เรียก `_mob_loot_cross_scene_boundary` โดยเจตนา ตามบรรทัดฐานที่ docstring ของมันเองวางไว้ให้ทางข้าม Columbus
- `TRANSPORT_DURABLE_WRITE_ALLOWED` ถูกอ่าน ไม่ถูกพลิก — `1218` ให้ LANE-A เป็นเจ้าของค่าคงที่นั้น
- **TWO_SESSIONS_SAME_SCENE:** เมธอดนี้แตะเฉพาะสถานะต่อ connection (`foundation.selected` · ฟิลด์ census latch ·
  generation ของ membership) ไม่เอื้อมถึง registry ของ A · สองเซสชันที่เดินทางไปฉากเดียวกันต่างคน relabel แถวของตัวเอง
  และต่างคน re-arm census ของตัวเอง ไม่มีอะไรใช้ร่วมกัน และไม่มีบรรทัดไหนเขียนลง world registry ของ A

## ชุดเต็ม (บนต้นไม้ที่ merge origin/main แล้ว)
FULL_SUITE: `pytest tests/` = **14657 passed · 450 skipped · 42240 subtests passed** ใน 690.67s (11:30) บนคอมมิต `5adeb1a251780da766c20b1bf2ebafb6e4c31f0b` ที่มี `a92086c` (origin/main) เป็น ancestor · ไม่มี skip ใหม่จากรอบนี้ (preflight `[skips]` PASS)

SCOREBOARD: COMING | ผู้เล่นที่เดินทางออกทะเลจะไม่ถูกเซิร์ฟเวอร์จำผิดฉากอีก และวันที่ประตูทะเลเปิด เขาจะล็อกอินกลับมาที่จุดเดิมแทนที่จะโผล่กลางเมือง โดยไม่มีช่วงเวลาไหนที่ตัวละครล็อกอินไม่ได้เลย | pirate-force-server #1132 (draft, ADVERSARY_PENDING) · GT-309 โทเคน (ข) · rounds/R401_vu9d9n_g1_the_journey_names_its_scene_behind_the_login_fence.md
