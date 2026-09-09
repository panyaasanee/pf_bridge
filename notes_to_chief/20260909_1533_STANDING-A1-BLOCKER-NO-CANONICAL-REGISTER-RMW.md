งานเป้าหมายยืน A1 — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B; cc LANE-K, CORE, COO, chief
FROM: Codex RE/static · 2026-09-09T15:33:35+07:00
RESULT: BLOCKER / BOUNDED NEGATIVE — canonical register RMW ไม่มีใน executable image; จบ static รอบ A1 และขยับ A2

## คำตอบเพิ่มของ A1

[MEASURED][IMAGE][BOUNDED NEGATIVE] กวาด raw bytes ครบ `.text` และ `.code` ทุก byte boundary รวม 8,622,080 ไบต์แบบ over-approximation ไม่พบแม้แต่ candidate ของชุดต่อไปนี้ภายในหน้าต่าง 48 ไบต์:

1. load จาก object displacement `+0x70` แบบ word/dword หรือ `+0x71` แบบ byte
2. OR/AND/XOR immediate ที่ตั้ง/ล้าง/สลับ bit `0x100` เดิม หรือ BTS/BTR/BTC immediate bit 8 บน register เดียวกัน
3. store register กลับ effective address เดิม

ช่องว่างระหว่างสามคำสั่งอนุญาต byte ใดก็ได้ จึงไม่พลาดเพราะมี conditional branch หรือคำสั่งอื่นคั่นภายใน 48 ไบต์. รูปแบบ load ครอบ `MOV`, `MOVZX`, `MOVSX`; mask ครอบ group-immediate, accumulator-special และ bit-test-immediate; address ครอบ base, SIB/index, displacement 8/16/32 และ address-size 16/32. ผลเป็น `canonical_hits=0`.

[MEASURED][IMAGE][PROVEN_EXACT] whole-dword writer ที่รู้แน่ยังมี constructor เดิม: common actor constructor ตั้ง `[ESI+0x70]=EBX` ที่ `0x00443199` หลัง `xor EBX,EBX`; CNetNPC constructor เรียก constructor นี้ที่ `0x0045CC29` ก่อนติดตั้ง vtable `0x00F0DF58`. ดังนั้น CNetNPC สดเริ่มด้วย bit `0x100` ล้างอยู่.

[INFERENCE][IMAGE] เมื่อประกอบกับจดหมาย 15:21 ซึ่งปิด direct mask-specific census เป็น 3 จุด ไม่มี compiler sequence แบบ load-mask-store ซ่อนเป็นเส้นทางที่สองในขอบเขตข้างบน. หลักฐาน static ที่เหลือยังบอกเพียง: constructor ล้างทั้ง dword; CHitResult/CMissileHitResult ตั้ง bit โดยตรง; selector ล้าง bit โดยตรงตามสถานะ local CMyActor. ยังตั้งชื่อ bit ว่า aggro ไม่ได้ และยังปิด arbitrary whole-value/alias/copy writer ไม่ได้.

## หลักฐานจากอิมเมจ

อิมเมจ `GameClient.local.bin` ขนาด 14,759,424 ไบต์ SHA-256 ก่อน/หลัง:
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

ช่วงหลักฐานเป็น `[start,end)`:

| หลักฐาน | VA | File offset | SHA-256 |
|---|---|---|---|
| common actor constructor และ whole-dword zero writer | `00443180–00443450` | `00042580–00042850` | `274a44e8b1ac932c548cbe10b9144696e988d9b1e8eb9c640322e2fe80f10a31` |
| CNetNPC constructor และ inherited-constructor call | `0045CC00–0045CD09` | `0005C000–0005C109` | `2edd9c047892a820b410a2f346320db84e08453089bdde4e20d6098b0662a0cf` |
| `.text` census | `00401000–00C39C00` | `00000400–00839000` | `05231553cad90671d0b9a09ba0990982a32f1e236c293f094f4569968162cdae` |
| `.code` census | `00C3A000–00C3A400` | `00839000–00839400` | `60762e63b47a2ac7d4736f00108c9a205a7b5cd67e593affe0c6930d50b7a6cb` |

field_key: `CNetNPC@0x70.4#W:b0x100` เฉพาะ constructor clear ที่ typed ผ่าน CNetNPC constructor chain; census ลบไม่เพิ่ม field writer ใหม่.

## ค้นก่อนถอดและตรวจซ้ำ

- [MEASURED][DOCUMENT-SEARCH] พบของเดิมใน `external/PF_MONSTER_COLOR_GATE.tsv` แถว MCG-IMG-035–038: constructor, hit writers สองจุด และ selector clear. รอบนี้ไม่สร้างตาราง external ซ้ำ.
- [MEASURED][DATA-SEARCH] พบ `AI_WANDER.n_OFFESIVE` และ `AI_WANDER.n_AGGRO` เป็นคนละคอลัมน์ที่ `gamedata/PF_GAMEDATA_COLUMNS.tsv:326–327`; ชื่อข้อมูลไม่ใช้ตั้งชื่อ runtime bit.
- [MEASURED][PROJECT-SEARCH] `docs/FUNCTIONAL_COVERAGE.json` ยังเก็บ combat-result และ mob-aggro runtime gaps; static result นี้ไม่เลื่อน coverage.

Verifier stdlib-only: `pf_bridge/staged/standing_a1_reg_rmw_verify.py` SHA-256 `2066263cd91b1afe7f683092899edad08254ab98b96bbca3599b3fa9ea510137`.

Log: `pf_bridge/staged/standing_a1_reg_rmw_verify.log` SHA-256 `75693bbbf9cdf451f7b71ceedf5e8f8453a5387807008aeee711d2dbf13f7ef8`.

ผล: `PASS exec_raw_bytes=8622080 sections=2 canonical_hits=0 cases=10 mutations=10 window=48 spans=2 span_traps=2 whole_image_trap=1 coverage_traps=2`.

Known-answer corpus บังคับ native byte/word/dword, accumulator opcodes, MOVZX/MOVSX, BTS/BTR/BTC family, SIB/indexed, address16 และ conditional-branch gap; ทุก case มี mutation trap. Verifier ไม่ใช้ capstone/pefile และ mutation ทั้งหมดอยู่ใน memory.

## blocker และส่งต่อ

Static A1 หยุดตรงนี้ตามกฎกันจม. หลักฐานที่ปลดช่องสุดท้ายคือ attended data watchpoint บน CNetNPC instance `+0x70` ตั้งแต่ constructor จนสีเปลี่ยน พร้อม instruction pointer ของ writer ทุกครั้ง; ถ้า writer IP อยู่นอกสาม mask-specific sites ให้ส่ง span นั้นกลับเข้า RE. ถ้าไม่มี writer อื่นและสีไม่เปลี่ยนเอง ผล runtime จะปิดคำตอบ A1 ว่าต้องส่ง entry/state ใหม่จากฝั่งเซิร์ฟเวอร์.

BUILD_PROPOSED: เพิ่ม GT-224 watchpoint ledger ที่บันทึก CNetNPC identity, old/new `+0x70`, writer IP และ rendered colour ตั้งแต่ spawn → hit → disengage → local-current-zero | LANE-B + CORE; LANE-K ผูกใบ | `A1_CNETNPC_70_WATCHPOINT_LEDGER`, `A1_OTHER_WRITER_OR_NONE`, `A1_RENDERED_COLOUR_JOIN`

## nonclaims

- ไม่อ้าง complete writer census ของ `CNetNPC+0x70`: arbitrary whole-value MOV, memcpy/copy, register-index bit operations, pointer aliases, sequenceยาวเกิน 48 ไบต์ และ self-modifying/unbacked code อยู่นอกขอบเขต
- ไม่อ้างว่า absence ของ canonical sequence แปลว่าไม่มี writer แบบอื่น และไม่อ้างว่า constructor clear เป็น gameplay transition
- ไม่อ้างชื่อ/ความหมาย gameplay ของ bit `0x100`, ไม่อ้างว่า hit target เป็น CNetNPC ทุกครั้ง และไม่อ้างว่า bit นี้เป็นทางเดียวสู่ style 61
- ไม่อ้างผลภาพ, ordering, persistence หรือ runtime pass; ไม่มีการเปิด client/server
- ไม่แก้ ServerProject, queue, lease, workflow, external, gamedata, reference, DB หรือ Git

SCOREBOARD: STATIC-BLOCKER-BOUNDED | direct mask writers=3 | canonical register RMW=0 | constructor whole-zero=1 | final proof requires attended watchpoint
