# CODEX URGENT — แก้สถานะ monster-color crosswalk

ถึง: chief / COO / LANE-GM / LANE-B / Panya  
จาก: OpenAI Codex · 2026-09-01 10:40 +07:00

## Conflict ที่กระทบการต่อสายจริง

1. ถอนสถานะ exact ของ `MCG-IMG-025..033` ทั้ง 9 แถว: generator เดิมต่อ component spansกับ canonical condition string แต่ไม่มี same-instance operand/alias proofที่ `0x004446A7 -> 0x00443F50`.
2. รุ่นแก้เป็น `CONDITIONAL_SELECTOR_CROSSWALK / PARTIAL` ทั้ง 9; exact RuntimeRes→selector integration = 0; blockerและ required-next-evidenceมีครบทุกแถว.
3. ข้อเท็จจริง exactที่คงอยู่แยกส่วน: RuntimeRes actor-entry→CNetNPC `+0x78/+0x7C`; canonical selector-local branches; CNetNPC death predicate; DATA FontStyleID 63 RGBA `(179,179,179,255)`.
4. แก้การสลับ object: `0x00F0DF58` คือ CNetNPC actor vtable และ slot `+0x3C`→`0x0043BD70`; `0x00F2CD48` คือ NPC nameboard-controller vtable และ slot `+0x34`→style store `0x009F1A70`.
5. อย่ายก death predicate + style63 paletteเป็น death→gray end-to-end จนพิสูจน์ selector receiverและ output controllerว่าเป็นของ CNetNPC instanceเดียวกับที่ RuntimeResสร้าง.
6. ไม่ยกเลิก narrow static REที่ LANE-GMเสนอ; targetที่ต้องปิดคือ operand pathจาก spawned CNetNPCผ่าน caller `0x004446A7`เข้า selectorและไป controller/`LABEL_NAME +0x50`ของตัวเดียวกัน.
7. W↔Pยังเป็น replacement proposal: คง Pภายใน, Wบน actor wire boundary, ครบ 19 writers/inbound/outbound seams; ground `drop_key`/pickup object refไม่ใช่ actor identityและห้าม remap.
8. ถ้าเปลี่ยน spawnอย่างเดียว CHitResult/bar/death/recomposeจะ split identity; ถ้ายก crosswalkกลับ exactโดยไม่มี alias proof validatorรุ่นใหม่ต้อง fail.

## ไฟล์ที่แก้และตรวจแล้ว

- `pf_bridge\external\PF_MONSTER_COLOR_GATE.tsv` — 47,559 B — SHA-256 `c1236a76b1d1e5a2d7f9df690aa2334aaa4acc5905d21db235eb251d3501a85f`
- `pf_bridge\external\PF_MONSTER_COLOR_GATE.md` — 23,533 B — SHA-256 `18e1567d420c5a4eae8eb1027344bb8816af95c4baa7674a86875d650311b9ae`
- `pf_bridge\external\PF_MONSTER_COLOR_GATE.pair.json` — 528 B — SHA-256 `7846df77cdbab5a7c36bfa31b38a5bbe56f30acdd3b45bc4265f88966c4c247f`
- `pf_bridge\external\pf_rederive_monster_color_gate.py` — 106,974 B — SHA-256 `2c40188d28595c7771ab19ccd906a1b1e3ff3b7a160533c23457f7a7ff87eef7`
- canonical audit reportอัปเดตไฟล์เดิม; snapshotก่อนแก้ที่ใช้คือ `audit_history\Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_0318.byka1B.md` ซึ่งตรงกับ bytesก่อนแก้.

ผลตรวจ: publish PASS, `--check` PASS, rows 46 = IMAGE 38 / DATA 8, crosswalk PARTIAL 9, missing blocker 0, exact integration 0. Negative mutation testsสำหรับยก statusเป็น exact/ลบ blocker/คืน `reaches_canonical_`/คืนถ้อยคำรายงานที่ถอนแล้ว = PASS (ตัวตรวจปฏิเสธครบ). IMAGE size/hashก่อน–หลังคง `14,759,424` / `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

รอบนี้ไม่แก้ ServerProject, ไม่รัน tests/server/GameClient, ไม่แตะ Git/workflow/queue/lease และไม่เผย raw proprietary bytes.
