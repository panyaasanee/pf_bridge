# CODEX CHECKPOINT P0-2 — selector สีชื่อและ nameboard fields

สถานะ: `LOCAL-AUTHORITATIVE / NOT COMMITTED / NOT DELIVERED`  
เวลา: 31 สิงหาคม 2026 ประมาณ 17:40 +07:00  
ขอบเขต: อ่าน GameClient/Data/รายงาน/ServerProject source เท่านั้น; ไม่รันเกมหรือเซิร์ฟเวอร์ ไม่แก้ ServerProject, Git, workflow, queue หรือ lease

## ทำอะไรไป

1. ไล่ selector ที่ `0x00443F50..0x004443C5` ถึง controller, widget child และ `UILabel.FontStyleID` setter พร้อม hash-pinned support spans
2. ทำ independent census สองชั้น: `PUSH imm8` ของ FontStyleID 55–63 ได้ 14 จุดตรงตาราง และ executable-section direct-call census ได้ caller เดียว `0x004446A7`
3. เพิ่ม `PF_ATTR_NAME_COLOR_SELECTOR.tsv` 14 IMAGE rows โดยแยก typed CMyActor 2, typed CNetNPC 3 และ dynamic-controller union 9; quarantine 0
4. ปิด `BasicAttr+0x28` เป็น `LABEL_NAME` สำหรับ CNetActor/CNetNPC, ปิด `ActorAttr+0x164` เป็น CNetActor `LABEL_GUILD`, เพิ่ม role ของ `ActorAttr+0x98`, และ refine `ActorAttr+0x180` เป็น guild FontStyleID 64–67
5. บันทึก active errata ของรายงาน NAME-001/NAME-002 โดยไม่เขียนทับหลักฐานเก่า และเปิด server-code conflicts ที่กระทบต่อสายจริง 3 รายการ
6. สร้าง generation ซ้ำสองรอบได้ ID เดิม และ authoritative reader ผ่าน

## ฟิลด์เปลี่ยนจาก P0-1

- Field rows: `480 -> 488` (+8), removed 0
- Existing rows ที่เปลี่ยน **status**: 0
- Rows ใหม่: 8 = `PROVEN_EXACT` 6 (`BasicAttr+0x28` 4, `ActorAttr+0x164` 2) + `PROVEN_ROLE_ONLY` 2 (`ActorAttr+0x98` W/R)
- Existing rows ที่ refine **semantic โดย status ไม่เปลี่ยน**: 2 (`ActorAttr+0x180` W/R)
- รวมล่าสุด: EXACT 229 / ROLE 190 / PARTIAL 27 / UNKNOWN 42; scope EXACT 278 / UNKNOWN 210
- P0: 28 structural / 30 scoped claims = EXACT 20 / ROLE 7 / UNKNOWN 3
- exact semantic + exact scope 115; server-safe 98; exact/exact ที่ถูก OPEN conflict hold 17
- A2 overlay: 204 rows = YES 31 / NO 173
- Unresolved ledger: 966 = active claims 456 + standalone conflict work 510

## ผล P0-2 ที่ต้องใช้แบบ fail-closed

- 14 selector paths: CMyActor 2 / CNetNPC 3 / dynamic union 9
- FontStyle emissions: 55×1, 56×2, 57×1, 58×1, 59×1, 60×1, 61×3, 62×1, 63×3
- DATA แยกชั้นยืนยัน 60=เหลือง, 61=แดงอ่อนขอบแดงเข้ม, 62=ส้ม, 63=เทา
- ห้ามสรุป `61=aggro`, `62=monster`, `63=dead` แบบสากล: red มี linked actor / `n_OFFESIVE` / bit `0x100`; gray มี ordered dead predicate และ linked-actor failure
- ไม่พบหลักฐานว่า selector นี้แยก monster C++ class ออกจาก NPC class

## Conflict ต่อสายจริง (ไม่เกิน 10 บรรทัด)

1. `player_wire.py:109-152` frozen class-less helper ยังใช้ ActorAttr+0x164 และถูก optional stats crosscheck เรียกจริง — OPEN
2. `stats_progression_hypothesis.py:303-310` ยังตั้ง ActorAttr+0x164 เป็น character_name — OPEN
3. `damage_hp_link_hypothesis.py:317-321` ยังตั้ง ActorAttr+0x164 เป็น character_name — OPEN
4. production `LegacyProjector.start_game` ใช้ corrected BasicAttr name path อยู่แล้ว — ไม่ใช่ defect; ห้ามแก้ย้อนกลับ
5. conflict ทั้ง 3 ผูก field row เดียว จึงเพิ่ม OPEN conflict count แต่ไม่เพิ่ม unresolved row ซ้ำ
6. รวม conflict 1,283 = OPEN 638 / non-OPEN 645; quarantine 0; approved probe 0

## ไฟล์ผล

Generation: `59ea10c95c729bb1ee7c0c24c95daf0184f2a5884a3b7b3c29a5a24bf269fc73`  
Manifest: `pf_bridge/external/PF_ATTR_GENERATION_MANIFEST.json` — 7,047 bytes, SHA-256 `8c13f78d…`  
Artifact directory: `pf_bridge/external/.pf_attr_generations/59ea10c95c729bb1ee7c0c24c95daf0184f2a5884a3b7b3c29a5a24bf269fc73/` — 40 artifacts, 13,884,832 bytes

- `PF_ATTR_FIELD_SEMANTICS.tsv` — 1,333,491 bytes
- `PF_ATTR_NAME_COLOR_SELECTOR.tsv` — 37,350 bytes
- `PF_ATTR_SEMANTIC_REPORT.md` — 34,930 bytes
- `PF_ATTR_FOR_SERVER.md` — 121,726 bytes
- `PF_ATTR_UNRESOLVED.tsv` — 2,346,834 bytes
- `PF_ATTR_CONFLICTS.tsv` — 3,528,388 bytes
- `PF_A2_ATTR_FIELD_DELTA.tsv` — 481,478 bytes
- `PF_ATTR_QUARANTINE.tsv` — 359 bytes (header only)
- `PF_ATTR_PROBE_REQUESTS.tsv` — 151 bytes (header only)
- Cumulative audit: `Pirate_Force_Codex_Audit_Recommendations_CHECKPOINT_20260831.md` — 59,341 bytes, `HOLD FOR PANYA`

## Delivery blocker

ชุด local ข้างบนตรวจ hash ครบ แต่ยังไม่ใช่ committed/delivered artifact: ServerProject Git ไม่ติดตาม external generator/reader/generation, tracked `notes_to_chief/reference_codex_attr` ยังอยู่ที่ P0-1 generation `0e9cb92b…`, และ mirror/allowlist ปัจจุบันไม่รวม selector TSV ใหม่ รอบนี้ไม่มีสิทธิ์แก้ Git/workflow จึงรายงานไว้ตรง ๆ; ผู้รับต้องอ่านผ่าน manifest ที่ชี้ generation directory local นี้ ห้ามหยิบ top-level TSV แยกชิ้นหรือเรียกว่าปล่อยขึ้น repo แล้ว

## งานถัดไป

P0-2 static checkpoint จบแล้ว ให้เดิน P0-3 ต่อ: ไล่ owner/producer/consumer ของไอคอน quest `!`/`?` เหนือหัว NPC โดยถือ `ActorAttr+0x1A0` เป็น negative control ที่ปิดแล้ว

