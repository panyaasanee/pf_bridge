# CODEX CHECKPOINT — P0-3 QUEST MARK STATIC CLOSURE

เวลา: 2026-09-01 17:51 +07:00
สถานะรายงาน: `RELEASED TO TEAM 2026-09-01 (เจ้าของเคาะ)` / `CHECKPOINT / PROVISIONAL`

## ทำอะไรเสร็จ

- ปิด bounded direct/static event census ของ quest-mark query channel โดยแยก general channel ที่ reuse เลข `0x0A`; ห้ามเรียก `0x0A` ว่า quest event แบบ global
- ปิด conditional `.tga -> .tg_` resolver/TGA reader machinery และ DATA filename censusครบ selector 1–8; `quest_splend.tga.tg_` เป็น DATA-only control ไม่ใช่ selector target
- ปิด static `QuestIconBoard` lifecycle ตั้งแต่ pool/constructor, CNetNPC ownership/update, manager admission/withdrawal, destruction ถึง submission call `0x00A9E6C0`
- Runtime concrete open/reader/decode/bind, transition timing, final renderer/GPU/pixels, computed/runtime-only listeners และ original-server quest-state sourceยัง `OPEN`
- selector 0 ยังไม่มี semantic name; ไม่เรียก hidden/no-icon

## Integrity / review

- Root `--check` ทั้งสามผ่านและ hash/mtime ของไฟล์ทั้งเก้าไม่เปลี่ยน; resource `--self-test` ผ่าน 8 mutation cases
- Adversarial reviewพบและแก้ defect 2 จุด: lifecycle publisher race และ resource evidenceที่ขาด `measurement_label/method/control`
- Final cross-audit: 66 rows = IMAGE 57 / DATA 9; duplicate row/evidence keys 0; collisionกับ existing TSV 0; exact duplicated DATA claim 0; source leakage 0
- IMAGE ก่อน/หลัง: 14,759,424 bytes; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Main Attr generationคง `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`; field rows 490; semantic UNKNOWN 42; scope UNKNOWN 210; unified unresolved 977; delta ทุก vector = 0
- Canonical report pre-edit ตรงทุกไบต์กับ snapshot ล่าสุด `audit_history/Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_1019.byka1B.md` จึงข้ามการคัดลอกซ้ำตามกฎ

## Files

- `pf_bridge/external/PF_QUEST_MARK_EVENT_CENSUS.tsv` — 29,193 B — `40127e6410c1aa6405efada640c60b72663eb9e35537c8011cdeede47d0a0b35`
- `pf_bridge/external/PF_QUEST_MARK_EVENT_CENSUS.md` — 8,833 B — `e1de566825b6d60e5ac747df3f53e4975cd49dd36f3584441039c49820247c4e`
- `pf_bridge/external/pf_rederive_quest_mark_event_census.py` — 75,639 B — `5c6e6ea3558b4c8efebfa1f20ae7126bd9e39575b041acddba33bc485af11fda`
- `pf_bridge/external/PF_QUEST_MARK_RESOURCE_RESOLVER.tsv` — 44,435 B — `de491977008f1b3a0ab75da4a45bbba9cd35504350ecfbff95cfbec69a8641ab`
- `pf_bridge/external/PF_QUEST_MARK_RESOURCE_RESOLVER.md` — 8,165 B — `f39f41cc91a5f6a7f1748933853e7d7ef0db393008588abf6fa73927421b71cc`
- `pf_bridge/external/pf_rederive_quest_mark_resource_resolver.py` — 74,855 B — `afe9f7694bb6bda28804aac7869a686c1e44f29e36ecd7d20e694be0ccedbc38`
- `pf_bridge/external/PF_QUEST_MARK_LIFECYCLE.tsv` — 23,289 B — `45d7a21d8e340faede88f8f745651a4d44a24fbb50c262f6907e40063a71f517`
- `pf_bridge/external/PF_QUEST_MARK_LIFECYCLE.md` — 13,715 B — `561d2d0ab1219c95df72cad6371c7ca294d7fb56efad710a0afeb50572e6e5a2`
- `pf_bridge/external/pf_rederive_quest_mark_lifecycle.py` — 56,022 B — `e26ad423b3b2da0df72c6c5eba97f83e36ccb9e211f223b8eca80fc7192646ff`

## Conflict / nonclaim (ไม่เกิน 10 บรรทัด)

1. Static conditional route ไม่เท่ากับ runtime success หรือ visible pixels
2. Numeric `0x0A` ถูก reuse ระหว่างคนละ channel; global quest name เป็นข้ออ้างผิด
3. selector 0 พิสูจน์เพียง branch effect ไม่พิสูจน์ hidden/no-icon
4. `quest_splend.tga.tg_` ไม่เกิดจาก replace-last-character rule และไม่มี selector join
5. Runtime trace requestยังไม่ผ่าน Attr probe intake สี่ด่าน จึงไม่สร้าง random `probe x y`
6. Standalone artifactsอยู่นอก canonical ServerProject worktree; cloneอื่นต้อง owner-approved packaging/ingest

## ถัดไป

เดิน P0-4 ต่ออย่างเคร่งครัด: แยก role/state/traits ที่ทำให้ CNetNPC เป็น monster, NPC หรือ training dummy และพิสูจน์ talk-vs-attack decisions โดยไม่ยก DATA clusterหรือ replacement serverเป็น original law

Codexไม่ได้แก้ ServerProject, ไม่แตะ lease/workflow/queue/Git, ไม่รัน client/server/dump/capture และไม่แก้ frozen V141
