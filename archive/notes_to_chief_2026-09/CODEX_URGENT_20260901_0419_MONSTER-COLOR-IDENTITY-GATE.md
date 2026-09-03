[ถึง: chief · LANE-A · LANE-B · COO | จาก: Codex static RE | 2026-09-01T04:19:09+07:00]

# ด่วน: actor-entry identity เป็นประตูก่อนถึงสีชื่อมอนสเตอร์

## คำตัดสินที่ปิดได้จากของเดิม

- **[ORIGINAL EVIDENCE: IMAGE]** RuntimeRes อ่าน actor-entry ซึ่งมี actor type และ identity แบบ qword คนละส่วนกับ BasicAttr identity จากนั้นส่ง record เดิมเข้า actor reconcile → factory actor type 4 → `CNetNPC` → selector สีชื่อ
- selector ตัดสิน identity ก่อน: high dword แบบ signed มากกว่า 0 หรือ high=0/low!=0 เข้ากลุ่ม positive; high<0 หรือศูนย์ทั้งคู่เข้ากลุ่ม nonpositive
- positive lane ข้าม FontStyleID 60/61/62/63 ทั้งกลุ่ม ดังนั้น orange/red/gray ไม่ได้เกิดจากการเปิด `n_OFFESIVE` หรือ bit อย่างเดียว หาก actor-entry identity ยังเป็น positive
- style 63 ไม่ได้แปลว่า dead เสมอ และ style 61 ไม่ได้แปลว่า offensive/bit อย่างเดียว เงื่อนไข relationship, vslot, NPCAttr fallthrough และ runtime bit ต้องคงครบตามตาราง
- **[ORIGINAL EVIDENCE: DATA]** สีจริงของ 56..63 ปิดจาก `BigFontStyle.fsl`; แต่สีบนจอของ runtime ใด runtime หนึ่งยังไม่ปิด เพราะยังไม่มี live branch/context/render evidence

## ผลต่อ replacement ปัจจุบัน — ขอบเขตจำกัด

**[RECONSTRUCTED POLICY]** ห้าไฟล์ที่ตรวจตรึงไว้มีตัวอย่าง legacy `0x1001..0x1006` และสูตร `0x2000 + placement_index + 1` ที่ `population.py:46`, `field_mobs.py:321`; writer ที่ `world_population.py:707`, `field_mobs.py:1708`; active call ที่ `runtime.py:8021`. สำหรับ placement index ไม่ติดลบ ค่าเหล่านี้มี high=0/low!=0 จึงเข้า positive family ตาม IMAGE และหาก relationship predicate เป็น false จะเป็น style 56 สี magenta/pink

นี่เป็น **conditional conflict ของ producer ที่ตรวจตรึงไว้** ไม่ใช่สำมะโนครบทุก production producer และไม่ใช่หลักฐานว่า original server ใช้ identity แบบใด ห้ามแก้เป็นเลขติดลบที่เดาขึ้นเอง เพราะยังไม่ปิด uniqueness, registry/reference safety และ original identity policy

## สิ่งที่ต้องทำก่อนแก้ runtime

1. หา original actor-entry identity policy หรือหลักฐานที่จำกัด candidate ได้โดยไม่ชน registry/reference
2. ทำ fail-closed census ของ production-reachable actor-type-4 producers ทั้งหมด แล้วแยก producer ที่ยังไม่ตรึง
3. ยืนยัน live relationship/NPCAttr/vslot/bit prerequisites พร้อมสีบนจอ โดยไม่ยก observation ครั้งเดียวเป็น original policy
4. ห้ามแก้ frozen V141 และห้ามย่อ orange/red/gray เป็น boolean `monster` ตัวเดียว

## Artifact ที่รับรองแล้ว

- `pf_bridge/external/pf_rederive_monster_color_gate.py` — 79,217 bytes; SHA-256 `62c5d78903d797400f32625f3bff5a3193d607efdd4a895f65eda6cbd2c22fe1`
- `pf_bridge/external/PF_MONSTER_COLOR_GATE.tsv` — 40,636 bytes; 46 rows = IMAGE 38 / DATA 8; SHA-256 `c094f9f4ff6e39648ecffb2f0c8d8edf9b3338c94860afdd264f3c32d599552f`
- `pf_bridge/external/PF_MONSTER_COLOR_GATE.md` — 12,770 bytes; SHA-256 `d5dbd71b2d08a9f2e8a18b2eccfe8accc1a812d89fafc7a53cda6947dbb8d151`
- `pf_bridge/external/PF_MONSTER_COLOR_GATE.pair.json` — 528 bytes; commit marker SHA-256 `d8af858d9e78a55afa22681fb84c57217e65390dc8c2ac2dd53bcba49fce3fe2`

ผู้ตรวจอิสระโจมตี semantic substitution, manifest ว่าง, row/reference drift, CRLF, split pair และตำแหน่ง PASS แล้วรับรอง `ACCEPT`; publish และ `--check` ผ่านโดย IMAGE hash ก่อน/หลังคง `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

ไฟล์ใน `pf_bridge/external` เป็น local-only/Git-ignored; Claude บนเครื่องเดียวกันอ่านได้ แต่ clone อื่นจะไม่ได้รับจนกว่าเจ้าของอนุมัติ packaging. รอบนี้ไม่ได้แก้ ServerProject, Git, workflow, queue หรือ runtime และไม่ได้รัน GameClient/server/capture
