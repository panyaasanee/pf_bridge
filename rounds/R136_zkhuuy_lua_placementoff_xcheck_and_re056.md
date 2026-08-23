# R136 (session zkhuuy) — 2026-08-24 (+07:00)

**สภาพแวดล้อม:** Routine cloud · fresh clone ทั้งสอง repo · โครงพี่น้องยืนยันแล้ว (`../pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv` มีจริง 11,388 bytes)

## การ์ด PR + probe
- PR เปิดค้าง `claude/*` + marker: **ไม่มีทั้งสอง repo** (list_pull_requests คืน `[]` × 2) => จับล็อกได้
- จับล็อก: empty commit `round claim: zkhuuy` (`3aaec84`) push ขึ้น `claude/exciting-goldberg-zkhuuy` => PR **#37 draft** (body มี `PF-AUTOMERGE: v4`)
- probe ① GitHub API/tool: ✅ อ่านได้ (list_pull_requests สำเร็จ) — ใช้เป็นทางหลัก
- probe ② ทาง D `ci-status`: ✅ มีชีวิต (`git ls-tree origin/ci-status ci/` คืนไฟล์ `ci/<sha>.json` หลายใบ · d_exit=0)

## เลขรอบ
เลขสูงสุดใน `rounds/` = R135 => รอบนี้ **R136** (ไม่ชน)

## กล่องจดหมาย — บริโภค 2 ใบใหม่
1. `20260824_0124_GAMEDATA-LUA-API-SPEC-160-*` — whitelist gamedata + สเปก API 160 ชื่อ · 0/160 อยู่ใน server src (ชั้นสคริปต์ยังไม่สร้าง)
2. `20260824_0126_RE055-DRAFT-outbound-census-is-blind-*` — ร่างใบ direction ของ `TriggerCastSkillVital` + ผลวัดเพดาน census
(ที่เหลือในกล่องเป็น `FROM_CHIEF_*` ของ chief เอง + หลุมศพเก่า — ไม่ใช่ใบเข้าใหม่)

## งานที่ทำ
### ① ปรับหัว CLIENT_RE_QUEUE.md ให้ตรงความจริง
`gamedata\lua\`+`scene\`+API spec **เข้า git แล้ว** (commit `0801541`) — หัวไฟล์เดิมยังเขียน "ยังไม่เข้า git" => แก้เป็นเข้าแล้ว
(external ยังค้าง 5/8 ตามเดิม ไม่แตะ)

### ② cross-check Lua PlacementOFF ↔ .npc index (ลูกมือ pf-static-re) — หักล้างสมมติฐาน
จดหมาย 0124 เสนอใบเชื่อม `Scene.PlacementOFF` เข้า band placement ของ GT-053 บนสมมติฐาน "เลข = index ตรง ๆ"
ลูกมือขุดแล้วพบ **counterexample**: literal 42/112 หลุดช่วง index ของฉากตัวเอง (0-based) · 40/112 (1-based)
=> **ไม่เปิดใบเชื่อมบนสมมติฐานนั้น** · รายละเอียด `FINDINGS_R136_LUA_PLACEMENTOFF_XCHECK.md`
เก็บคำถามเปิด (namespace ของ literal — ต้องเครื่องสะพาน) ไว้ ไม่เปิดใบรอบนี้
แถมแก้คำในจดหมาย 0124: "173 จุดเป็นเลขตรง" จริงคือ 112 literal / 61 `Trigger.VarN`

### ③ เปิดใบ RE-056 SKILLCAST-DIRECTION-002 (ลูกมือ pf-queue-author) — เข้า CLIENT_RE_QUEUE.md
ตามร่างจดหมาย 0126 · เลขขยับจาก RE-055 (055 ถูก GT-055 ใช้แล้ว) · จ็อบ 0 บังคับผ่านด่านตัวควบคุม `PickupTerrainThing` ก่อน ·
แนวใหม่: ไล่ registrar `0x5F3DF0` · มีเกณฑ์จบ (ตก => ย้าย observe-only probe `PF_SKILL001_...20260816.md`)

## คิวเทสเกม (กฎ ⑤)
รอบนี้ **ไม่เพิ่มใบเทสเกม (attended)** — งานทั้งหมดเป็นเลน STATIC-ON-BRIDGE (เลน attended พักตามคำสั่ง Panya 16:56)
ใบใหม่ RE-056 เข้า `CLIENT_RE_QUEUE.md` (เลน static · ไม่ต้องเปิดเกม) · ใบ static ที่เหลือเปิดจริง: GT-055 + RE-056
ไม่มีอะไรใหม่ที่ต้องใช้หน้าจอเกมในรอบนี้

## ลูกมือที่เรียก
- `pf-static-re` — cross-check PlacementOFF (findings)
- `pf-queue-author` — ร่าง RE-056
- `pf-adversary` — ตรวจ findings + RE-056 ก่อน commit (กฎบังคับ ④)

## ไม่ได้พิสูจน์
- ไม่แตะ repo โค้ด (`pirate-force-server`) เลย — รอบนี้เอกสาร/คิวล้วน
- runtime ของ PlacementOFF/skill-cast — เลน static พิสูจน์ไม่ได้
