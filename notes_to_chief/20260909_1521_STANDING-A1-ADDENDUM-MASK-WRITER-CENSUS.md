งานเป้าหมายยืน A1 — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B; cc LANE-K, CORE, COO, chief
FROM: Codex RE/static · 2026-09-09T15:21:37+07:00
RESULT: DONE / BOUNDED NEGATIVE — direct mask-specific bit-0x100 writer census closed

## คำตอบเพิ่มของ A1

[MEASURED][IMAGE][PROVEN_EXACT] กวาด raw bytes ครบทั้งสอง executable sections ทุก byte boundary รวม 8,622,080 ไบต์ พบคำสั่ง read-modify-write ที่ระบุ **bit 8 ของ field displacement `+0x70` โดยตรงเพียง 3 จุด**:

1. `0x007508D0`: `OR dword [ESI+0x70],0x100` ใน CHitResult
2. `0x007511E0`: `OR dword [ESI+0x70],0x100` ใน CMissileHitResult
3. `0x00444267`: `AND dword [ESI+0x70],~0x100` ใน CNetNPC name-colour selector

[MEASURED][IMAGE][BOUNDED NEGATIVE] ไม่พบ direct mask-specific writer จุดอื่นใน encoding families ต่อไปนี้: OR/AND/XOR แบบ byte ที่ `+0x71`, word/dword ที่ `+0x70`, และ BTS/BTR/BTC immediate bit 8 แบบ word/dword. Scanner รองรับ legacy prefixes, address-size 16/32, register base, SIB และ indexed address; ตัด absolute address ที่ไม่มี object baseออก.

[INFERENCE][IMAGE] เมื่อประกอบกับ A1 เดิมและ addendum เวลา 15:13: ภายในขอบเขต direct mask-specific RMW ไม่มี timeout/disengage clear ซ่อนอยู่นอก selector. จุด set ที่เห็นยังมีเพียง hit สองตระกูล และจุด clear ที่เห็นยังมีเพียง selector ซึ่งอ่าน predicate ของ local CMyActor. นี่ทำให้ caveat เดิม “two observed writers are not a complete writer census” แคบลงเป็นข้อจำกัด whole-word/alias ด้านล่าง; ไม่ได้ปิด writer census ทุกชนิด.

## หลักฐานจากอิมเมจ

อิมเมจ `GameClient.local.bin` ขนาด 14,759,424 ไบต์ SHA-256 ก่อน/หลัง:
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

Executable raw sections:

| Section | VA | Raw offset | Raw size | SHA-256 |
|---|---:|---:|---:|---|
| `.text` | 00401000 | 00000400 | 00838C00 | 05231553cad90671d0b9a09ba0990982a32f1e236c293f094f4569968162cdae |
| `.code` | 00C3A000 | 00839000 | 00000400 | 60762e63b47a2ac7d4736f00108c9a205a7b5cd67e593affe0c6930d50b7a6cb |

Consumer/producer spans เป็น `[start,end)`:

| หลักฐาน | VA | File offset | SHA-256 |
|---|---|---|---|
| selector clear | 00444238–00444270 | 00043638–00043670 | ed634e6768954ffd17c9886a39ae092326e5b802847b278a87d6a0b18664b035 |
| CHitResult set | 00750896–007508D7 | 0034FC96–0034FCD7 | f5542fcf64ed9b84d74a30f2688c3b4641bedbf553674455b3d20ad76e605cf4 |
| CMissileHitResult set | 007511A6–007511E7 | 003505A6–003505E7 | ebf888481cf1d605f5d7819dd93f783b0b1d47b2401ae90fc25c728a7ff738da |

field_key ที่ปิดตาม receiver เดิม: `CNetNPC@0x70.4#W:b0x100` สำหรับ clear; writer สองจุดเป็น `generic_actor_target@0x70.4#W:b0x100` เพราะชนิด CNetNPC ณ writer ยังไม่พิสูจน์.

## ค้นก่อนถอด

[MEASURED][DOCUMENT-SEARCH] ค้นชุดส่งมอบแล้ว **เจอ** `PF_MONSTER_COLOR_GATE.tsv` แถว MCG-IMG-036/037/038 และ `PF_ATTR_NAME_COLOR_SELECTOR.tsv` ที่มีสามจุดนี้ พร้อมข้อความว่าผลเดิมยังไม่ใช่ complete writer census. รอบนี้ re-derive จากอิมเมจและเพิ่ม exhaustive byte-pattern scope; ไม่สร้างตาราง external ซ้ำ.

[MEASURED][DATA-SEARCH] ค้น gamedata แล้ว **เจอ** `AI_WANDER` และคอลัมน์แยก `n_OFFESIVE` กับ `n_AGGRO` ที่ `PF_GAMEDATA_COLUMNS.tsv:326–327`. ไม่พบ address/local-bit writer ใน DATA และไม่ได้ใช้ชื่อ `n_AGGRO` ตั้งชื่อบิต runtime.

[MEASURED][PROJECT-SEARCH] `docs/FUNCTIONAL_COVERAGE.json` ยังระบุ `mob_aggro_and_server_ai` และ combat-result/runtime observation เป็นช่องค้าง. ผล static นี้ไม่เลื่อน coverage และไม่แทน attended GT-224.

คิวล่าสุดจาก `tools_bridge/pf_re_queue_taglint.py --list-open`: RE-155/235/261 เป็น attended; RE-239 มีป้ายผสมแต่เป็น reserved capture placeholder ตาม body เดิม จึงไม่มี static ticket ที่รับได้.

## การตรวจซ้ำ

Verifier stdlib-only: `pf_bridge/staged/standing_a1_writer_census_verify.py` SHA-256 `0d786280103ba4b4c7a3f7ea44328e3f6dbf7bccb8f2606bb73d14fc81dee74d`.

Log: `pf_bridge/staged/standing_a1_writer_census_verify.log` SHA-256 `0e0e0c7f32f52cac83c87525883aa60d1ff5b047ee8d41b225bcc8f582d3d2d6`.

ผล: `PASS exec_raw_bytes=8622080 sections=2 hits=3 OR32=2 AND32=1 families=15 family_mutation_traps=15 address_cases=2 negatives=4 spans=3 span_traps=3 whole_image_trap=1 coverage_traps=3`.

Known-answer corpus บังคับครบ 15 opcode/width families และ address forms สองแบบ. Mutations อยู่ใน memory เท่านั้น; scanner ไม่พึ่ง linear-disassembly negative และไม่ใช้ capstone/pefile.

## ส่งต่อ

BUILD_PROPOSED: instrument GT-224 ให้บันทึกทั้งสาม mask-specific sites แล้ววัดมอน `n_OFFESIVE=0` ตัวเดิมตั้งแต่ hit, disengage ขณะ local current>0, จน local current=0; หยุดและเก็บ trace ถ้าบิตเปลี่ยนโดยไม่มีหนึ่งในสาม site | LANE-B + CORE; LANE-K ผูกใบ | `A1_MASK_WRITER_3SITE_TRACE`, `A1_DISENGAGE_PRESERVE_OR_OTHER_WRITER`, `A1_LOCAL_ZERO_CLEAR`

## nonclaims

- ไม่อ้าง complete writer census ของ field `+0x70`: whole-byte/word/dword MOV, constructor/copy/memcpy, register-index bit operations, และ aliased pointer writes อยู่นอก mask-specific scope
- ไม่อ้างว่าบิตนี้ชื่อ aggro, hit, hostility หรือ timeout และไม่อ้างว่ามันเป็นทางเดียวที่เลือก style 61
- ไม่อ้างว่า CHitResult targets เป็น CNetNPC ทุกครั้ง หรือว่า packet มาถึง actor/nameboard instance ที่เห็นจริง
- ไม่อ้างผลภาพ, ordering, persistence หรือ runtime pass; ไม่มีการเปิด client/server
- ไม่แก้ ServerProject, queue, lease, workflow, external, gamedata, reference, DB หรือ Git

SCOREBOARD: STATIC-PROVEN-BOUNDED-NEGATIVE | direct mask-specific writer set = 3 | whole-word/alias writers remain outside scope
