# R146 (session naepog) — root-cause ของ "หน้าต่างสกิลเปิดไม่ได้" + เปิด RE-061

**เวลา:** 2026-08-24 ~11:5x (+07:00) · commit เป็น UTC ตามระบบ
**ล็อกรอบ:** draft PR pf_bridge #47 (head `claude/exciting-goldberg-naepog`, marker `PF-AUTOMERGE: v4`)
**เลขรอบ:** R145 เป็นเลขสูงสุดใน `rounds/` ก่อนรอบนี้ ⇒ N=146

---

## ผล PROBE (ยิงก่อนงานอื่น หลังการ์ด PR)

1. **GitHub API/tool อ่านได้** ✅ — `list_pull_requests` ทั้งสอง repo คืน `[]` (ไม่มี PR เปิดค้าง) ⇒ ใช้ API เป็นทางหลัก
2. **ทาง D (`ci-status`)** — บน `pf_bridge` ไม่มี branch `ci-status` (repo นี้ไม่มี gate workflow · ci-status อยู่ฝั่ง `pirate-force-server` ซึ่ง fetch เจอจริง) ⇒ N/A ฝั่ง bridge, ไม่กระทบเพราะ API ทางหลักใช้ได้

## การ์ด PR (ทำเป็นอย่างแรก)

- ไม่มี PR `claude/*` เปิดค้างทั้งสอง repo ⇒ จับล็อกได้
- empty commit `round claim: naepog` → push `claude/exciting-goldberg-naepog` → เปิด draft PR #47 (`draft:true` ยืนยันแล้ว) พร้อม marker `PF-AUTOMERGE: v4`

## กล่องจดหมาย (เคลียร์ก่อนงานอื่น)

บริโภค 2 ใบเข้าใหม่ (สำเนาไป `consumed/` + stub ข้างต้นฉบับ ไม่ลบไม่ย้าย):
- `20260824_1119_AUDIT-4-findings-skill-lane-may-be-disabled-and-git-bloat.md`
- `20260824_1147_CORRECTION-skill-lane-is-not-disabled-server-never-feeds-it.md`

ใบ `FROM_CHIEF_*` เป็น outbound ของ chief เอง ไม่นับเป็นของที่ต้องบริโภค

---

## เรื่องหลักของรอบ: สมมติฐานต้นเหตุ "หน้าต่างสกิล (K) เปิดไม่ได้" (GT-058) + prerequisite ที่หายไป

**ที่มา:** จดหมาย CORRECTION 1147 เสนอ **สมมติฐาน (ยังไม่พิสูจน์)** ว่า GT-058 (หน้าต่างสกิลเปิดไม่ได้ · กด K ไม่มี request วิ่ง) ไม่ได้เกิดจาก build ถูกปิด — ไคลเอนต์ขนข้อมูลสกิลมาครบ (SKILL_CONTEXT 2165 แถว + ไอคอน) — แต่อาจเกิดจาก **เซิร์ฟเวอร์เราไม่เคยส่ง "สถานะสกิล" (`CSkillModule`/`CSkillAttr`) ให้ไคลเอนต์** ⇒ หน้าต่างอาจไม่มีอะไรจะเปิด. 🔴 ยังไม่มีใครเห็นโค้ดที่ตัดสินใจไม่เปิดหน้าต่าง (จดหมายเองก็ nonclaim ไว้) · ถ้าสมมติฐานถูก งานแก้เป็น **เลนโค้ด (cc)** แต่ **เขียน encoder ไม่ได้ถ้ายังไม่มีรูปไบต์ที่พิสูจน์แล้ว** (ท่า GT-050)

**ยืนยัน derivability ด้วย pf-static-re (อ่าน committed artifacts ล้วน) — verdict: NEEDS-BRIDGE-IMAGE**

หลักฐาน (provenance เต็มในผล agent):
- `CSkillModule`/`CSkillAttr` **ไม่ใช่ wire vital** — ไม่มีใน `VITAL_REGISTRY_*.tsv` และไม่มีใน `PF_VITAL_NAMES.json` · id `0x1F7B`/`0x1661` เป็น **name-hash candidate** (FACTPACK L4: *"wire_id is DERIVED from the name by the round-62 hash. It is NOT read from any table in the image"*) ไม่ใช่ opcode ที่พิสูจน์แล้ว
- serializer field rows ใน `external/PF_SERIALIZER_FIELDS.tsv` = **EMPTY stub**: `CSkillModule` serializer `@0x00710440` = `write_al_1_then_ret_4` (ตั้ง AL=1 แล้ว ret เฉย ๆ — ไม่ปล่อยฟิลด์) · `CSkillAttr` `@0x0043BB80` = empty arg copier ⇒ ท่าที่ทำให้ `0x673C`/`0x36AA` derive ได้ (row ที่ไม่ EMPTY + span sha256) **ใช้ไม่ได้กับสองตัวนี้**
- capture: `external/PF_FIELD_VALIDATION.tsv` = `NOT_OBSERVED` 0 เฟรม ทั้ง W/R · `PF_CAPTURE_CORPUS.json` 0 hit ⇒ ไม่มีเฟรม S→C ให้เทียบ (ตรงกับที่ GT-052 จดว่า EMPTY W/R span)
- **แต่มีรูปบางส่วนอยู่:** `CSkillAttr` chains `DBAttribute` → bind กับ `CMyActor` ที่ `actor+0x3E8`, vtable `0x00F48B78`, Serialize `0x7520B0`; `EXPERIMENT_LEDGER` SKILL-001 จดรูป `u16 count` + container ของ `(key u16, opaque u16, opaque u32)` **แต่ไม่มี opcode และไม่มี object offset** ⇒ ประกอบเฟรม byte-exact ไม่ได้

**ข้อสังเกตที่สำคัญกว่าเดิม (จาก static-RE):** เพราะ `CSkillAttr` แขวนใต้ `DBAttribute` เหมือน `ActorAttr` (ที่ STATS-PROG-001 ทำอยู่แล้ว) — สถานะสกิลอาจไม่ใช่ "vital เดี่ยว" แต่เดินทางใน **ActorAttr collection** ⇒ RE-061 ต้องตอบด้วยว่าตัวพา (carrier) คืออะไร ไม่ใช่แค่หา opcode

## สิ่งที่ทำจริงในรอบนี้ (เอกสาร/ประสานงาน · ไม่แตะ repo โค้ด)

1. เปิด **RE-061 SKILLSTATE-WIRE-DIRECTION-001 [STATIC-ON-BRIDGE]** ใน `CLIENT_RE_QUEUE.md` (prerequisite ของเลนโค้ด skill-state sender) — two-tier pass, corrected facts, direction proof, negative=positive
2. บันทึก `IMAGE_ACCESS_COST.tsv` (อยากได้อิมเมจ · เลนโค้ด sender ถูกพัก · workaround=queue bridge)
3. บริโภคจดหมาย 2 ใบ · จดหมาย `FROM_CHIEF_R146_*` ถึงผู้เทส/Panya
4. pf-adversary ตรวจก่อน commit

## ที่ไม่ได้พิสูจน์ / nonclaim

- **ยังไม่พิสูจน์** ว่าไคลเอนต์ต้องได้ `CSkillModule`/`CSkillAttr` ก่อนเปิดหน้าต่าง — เป็น hypothesis · RE-061 Tier B เทสข้อนี้ด้วย **static จากอิมเมจ** (มี inbound decoder + skill-window-open ขึ้นกับ state ไหม) ไม่ใช่จาก corpus · 🔴 corpus ที่มีเป็น **emulator-only** (SCENE-013) ตอบ direction ของ server ต้นฉบับไม่ได้ ⇒ "ไม่เจอเฟรมใน corpus" = UNANSWERABLE ไม่ใช่หลักฐานว่า blocker มีสาเหตุอื่น · ผล RE-061 มีสามทาง (บวก/ลบ/UNANSWERABLE→รอ Panya) — adversary R146 จับจุดนี้ก่อน commit, แก้แล้วในใบ
- ตารางในไคลเอนต์ = สิ่งที่ไคลเอนต์รู้ ไม่ใช่กฎเซิร์ฟเวอร์ต้นฉบับ (ปิดแล้ว กู้ไม่ได้)
- serializer stub ในอิมเมจ = ความสามารถ serialize ฝั่งไคลเอนต์ ไม่ใช่หลักฐานว่าเซิร์ฟเวอร์ส่งอะไร
- ไม่แตะ repo `pirate-force-server` เลยในรอบนี้ (ยังไม่มีรูปไบต์ให้เขียน encoder — เขียน = เดา)

## audit 1119 ข้อ ②③④ (ไม่ใช่เลนโค้ด · แจ้ง Panya)

- ② git bloat 95MB จากภาพเต็มจอ: กฎใหม่แก้ที่ต้นทางแล้ว (AGENTS.md §5 · recorder เล็กลง 10 เท่า) · 95MB ในประวัติต้อง filter-repo = งานเสี่ยง **รอ Panya เคาะ** (chief แตะเครื่องสะพานไม่ได้)
- ③ ปี พ.ศ. ใน LOCK_GIT.txt: แก้แล้ว (AGENTS.md §3)
- ④ โฟลเดอร์ชั่วคราวบวม (boot_trees 227MB ฯลฯ): ข้อเสนอ retain-5-รอบ **รอ Panya เคาะ + ต้องลบบนเครื่องสะพาน**
⇒ ทั้งสามเป็น bridge/Panya decision ไม่ใช่เลนโค้ด cloud — chief แตะไม่ได้ บันทึกไว้ในจดหมาย
