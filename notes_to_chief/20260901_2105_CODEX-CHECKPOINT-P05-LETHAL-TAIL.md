# CODEX CHECKPOINT — P0-5 lethal-tail / handoff to P0-6

เวลา: 2026-09-01 21:05 +07:00  
สถานะ: `CHECKPOINT / PROVISIONAL`  
ผู้ทำ: Codex static RE lane (read-only ต่อ GameClient/Data/ServerProject; เขียนเฉพาะพื้นที่ส่งมอบที่อนุญาต)

## ผลรอบนี้

- สร้าง `PF_COMBAT_LETHAL_TAIL_DELTA` แบบ delta-only 15 แถว ทุกแถว `source=IMAGE`: EXACT 8 / BOUNDED 6 / PARTIAL 1
- ไม่คัด 34 lifecycle rowsเดิมมานับซ้ำ; duplicate claim/evidence/exact observation = 0 จากการเทียบ top-level TSV 99 ไฟล์
- ปิด bounded client contractเพิ่ม: actor/death reconcileมาก่อน TerrainThingPoolภายใน RuntimeRes handlerเดียว, target clearเกิดก่อน optional `TargetIsDead` panel event, runtime target qwordแยกจาก ActorAttr `+0x198`/NPCAttr `+0xA8`, observer fanoutมาก่อน death sync, dead taskมี reached-guard/allocation/queue/model-ready gatesและไม่ลบ actorเอง
- `BasicAttr+0x58` ไม่พบ local decrementerเฉพาะใน cited writer census; ข้อนี้ไม่ใช่ whole-programหรือ live-corpus negative
- `CFightMsgVital` ถูกข้ามตาม bounded stop rule; ไม่ได้พิสูจน์ว่าไม่มีหรือไม่เกี่ยวข้อง
- original packet grouping, cadence/hold, CHitResult↔actor-entry arrival order, transitive death→drop, actor/corpse removalและ pickup policyยัง `OPEN`
- Verdict: `P0-5_BOUNDED_CLIENT_CONTRACT_CLOSED / ORIGINAL_SEQUENCE_OPEN`; static RE laneย้ายไป P0-6

## Main Attr comparator

- Generation: `b96e420c290201ce60babec398fd2389ea36db2f2f30ce552d9d680f481f3fae`
- Field/status/scope change: `0`
- Semantic UNKNOWN: `42/490 = 8.57%`
- Scope UNKNOWN: `210`
- Standalone P0-5 rowsไม่ถูกนับเป็น field-status change และไม่มีการผสม sourceในแถวเดียว

## Wiring conflicts / สิ่งที่ Claudeควรใช้ทันที

1. Current full-census pathใช้ scalar dead timerกับทั้ง multi-corpse register; มอนใหม่ตายจึง re-armศพเก่าได้
2. Current per-session DropLedgerไม่มี scene termและ scene syncไม่ reset ledger; whole live ledgerจึงถูก republishในฉากใหม่ได้
3. Production pickup branchยังไม่เรียก transaction/removal helper; branch scenario-gatedที่มีอยู่ไม่ mutate ledgerและไม่ตอบกลับ
4. Empty DropLedgerไม่ emit frame และ count-zeroใน current decoderแปล PRESERVE ไม่ใช่ CLEAR; ห้ามใช้ guessed zero-countเป็น removal
5. Client handlerทำ actor/death reconcileก่อน TerrainThingPool; replacement orderควรมี actor stateพร้อมก่อนส่ง ground-drop state แต่ exact original packet groupingยังเปิด
6. Replacement `20.0`, `700 ms`, `120 s` และ separate framesเป็น reconstructed values ไม่ใช่ original timing
7. Current target clearเป็น client-local side effectที่ guardด้วย actor identity; optional panel eventถูก panel-null suppressได้แต่การ clearยังเกิด
8. CHitResult pathที่ปิดรอบนี้เป็น target-state side effects ไม่ใช่ direct HP write
9. Ordinary linked queue `manager+0x04`, manager flagsและ model-ready bit `0x40`เป็น gates; queue dead taskอย่างเดียวไม่พิสูจน์ว่า `_F_DIE_000`เริ่มทันที
10. Original removal/pickup carrierยังเปิด; P0-6ต้องปิด omission/clear consumerหรือ eligible original exchangeก่อนอ้าง authentic behavior

รายละเอียด current-code auditแบบ source-pinned: `CODEX_URGENT_20260901_2040_P05-CORPSE-DROP-STATE-SCOPE.md`

## Artifact pins

- `PF_COMBAT_LETHAL_TAIL_DELTA.tsv` — 43,449 B — `6f6cffddfc0d77d9853637051ef572576ceff9ba7bee50bb1a01eb21c7263170`
- `PF_COMBAT_LETHAL_TAIL_DELTA.md` — 12,538 B — `39695cf6c76b90ed6336efedbcadca09b477e057aa05d08cb709926b933d52b0`
- `PF_COMBAT_LETHAL_TAIL_DELTA.pair.json` — 1,269 B — `a92e8c41aaaefd759b9162b080594e3a2d5f87de60a86e3b44cb04872d6c7e35`
- `pf_rederive_combat_lethal_tail_delta.py` — 88,086 B — `eef9c1f2139bd4c4d6a01bb11b2edaa8c150d479cbdcfb5f9f6ccf5c4e1eeb5f`
- generation — `5839daedbb039165372ef69cdb22eee9b61a3c2d6da281673f3710da0b08cfd5`
- claim set — `f05036a5d74fd81782314af14d5792b2ea987e44118331bd927835f27ca722c1`
- root `--check`: PASS
- self-test: PASS, 7 mutation cases
- independent adversarial review: corrected PASS; 69 primary/support spansและ 41 prior referencesตรง
- Input IMAGE before/after: 14,759,424 B — `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`

## Authority / report / delivery

- Canonical report — 178,171 B — `6d28c79ff5c58c6e74874ff72aaacff602e800d3325a82344a2d1b46460ef1bc`
- `PF_CRITICAL_ARTIFACT_AUTHORITY.json` — 22,061 B — `bbc88fa2309d4794da1b1295bce77a4fee643f4f6086071d0f58eb1ba0764553`
- Pre-edit report snapshotคงแบบ byte-identicalที่ `audit_history/Pirate_Force_Codex_Audit_Recommendations.b96e420c2902_20260901_1324.byka1B.md`
- Externalทั้งสี่ไฟล์มี byte-identical local mirrorใต้ `pf_bridge/notes_to_chief/reference_codex_attr`
- Local mirrorยัง `untracked`; Codexไม่มีสิทธิ add/commit. Owner/chiefต้อง track generator+TSV+MD+pairพร้อมกันเพื่อให้ cloneอื่นเห็น
- Codexไม่ได้แก้ ServerProject, ไม่รัน tests/server/client, ไม่แตะ V141, Git, workflow, queueหรือ lease

