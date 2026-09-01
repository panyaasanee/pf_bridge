# PF combat lethal-tail delta (IMAGE only)

This is a delta-only re-derivation over pinned canonical artifacts. It does not copy 
or replace any `PF_COMBAT_LIFECYCLE.tsv` row. Every delta row cites one or more 
prior rows by exact row identity, prior artifact SHA-256, and prior claim digest.

## Result

- Rows: 15/15; every row has `source=IMAGE`.
- IMAGE: `PF_ROOT://GameClient/GameClient.local.bin`, size `14759424`, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- TSV SHA-256: `6f6cffddfc0d77d9853637051ef572576ceff9ba7bee50bb1a01eb21c7263170`.
- Ordered claim-set SHA-256: `f05036a5d74fd81782314af14d5792b2ea987e44118331bd927835f27ca722c1`.
- Publication unit: TSV + Markdown, with the pair marker published last.

## New bounded claims

| delta_id | kind | status | exact bounded result | blocker |
|---|---|---|---|---|
| LT-IMG-001 | INTRA_RESPONSE_ORDER | PROVEN_EXACT | Call 0x005E4085 to actor reconcile 0x00446F30 completes before call 0x005E40D5 to typed terrain bridge 0x005F53A0. Actor/death reconciliation therefore precedes terrain/drop reconciliation inside one RuntimeRes handler invocation. | Original-server lethal-tail emission policy is not present in IMAGE. |
| LT-IMG-002 | BOUNDED_DIRECT_EDGE_NEGATIVE | PROVEN_EXACT_BOUNDED | The exact death-sync span contains 26 raw E8+rel32 encodings. None targets 0x005F53A0, 0x006AF970, 0x005F41E0, 0x00B0E4A0, 0x00B0EE40, or 0x006B03F0. | No direct death-to-drop edge exists in the bounded body; transitive ownership remains open. |
| LT-IMG-003 | TARGET_CLEAR_ORDER | PROVEN_EXACT | On the reached subpath after the actor+0x30 exclusion guard, the death path requires a nonnull CMyActor singleton and compares the dead actor qword at +0x78/+0x7C with current target +0xC8/+0xCC. On equality it pushes qword zero to 0x0043E1D0. It then looks up Main_Panel_Target_Enemy_New; only a nonnull lookup result constructs TargetIsDead and invokes vslot +0x210. The clear therefore precedes the optional panel event. | Original arrival timing of the lethal actor entry remains open. |
| LT-IMG-004 | RUNTIME_TARGET_CLEAR | PROVEN_EXACT | Setter 0x0043E1D0 detaches prior-target side effects only when prior-target resolution succeeds. On the singleton path it zeros CMyActor +0x408/+0x40C, and it invokes enemy-panel vslot +0x20C only when panel lookup is nonnull. The final stores of its two arguments at +0xC8/+0xCC are unconditional on those two optional operations. Thus the death-path arguments 0,0 are an actual runtime current-target identity clear. | None for the bounded runtime clear; serialized target-field producers remain separate. |
| LT-IMG-005 | TYPED_FIELD_SEPARATION | PROVEN_EXACT_BOUNDED | ActorAttr+0x198 is a separate typed qword: its constructor zeros it, copy and Merge move it, and the ActorAttr codec reads it under mask 0x20000000. Manual typed-base audit of the death clear and CMyActor setter finds no ActorAttr+0x198 store there. | Original nonzero ActorAttr+0x198 producer is not identified. |
| LT-IMG-006 | TYPED_FIELD_SEPARATION | PROVEN_EXACT_BOUNDED | NPCAttr+0xA8 is a separate typed qword: its constructor zeros it, copy and Merge move it, and the NPCAttr codec reads it under mask 0x10. Manual typed-base audit of the death clear and CMyActor setter finds no NPCAttr+0xA8 store there. | Original nonzero NPCAttr+0xA8 producer is not identified. |
| LT-IMG-007 | HIT_TARGET_SIDE_EFFECT | PROVEN_EXACT_BOUNDED | Under the numeric structural guards, CHitResult calls relation predicate 0x0043C380, compares CHit target +0x18/+0x1C with one of the CMyActor target qwords, clears old target state, selects setter 0x0043E010 or 0x0043E1D0, applies 0x0043CDA0(0) then 0x0043CDC0(1), and one branch sends TargetEnemyIsFocused to Main_Panel_Target_Enemy_New with actor +0x78/+0x7C. | Runtime branch choice and original-server CHitResult field policy remain open. |
| LT-IMG-008 | BOUNDED_DIRECT_EDGE_NEGATIVE | PROVEN_EXACT_BOUNDED | The full handler contains 50 raw E8+rel32 byte-pattern candidates. None targets 0x0051F150, 0x0051F2F0, 0x0051F920, or 0x0051E890. A separate manual instruction audit of the same pinned body found no non-stack +0x44/+0x48 operand. | The observer or transitive route that refreshes name/HP is not bound. |
| LT-IMG-009 | OBSERVER_BEFORE_DEATH | PROVEN_EXACT | The known-actor entry method calls observer fanout 0x005DF080 first and death sync 0x004437C0 second. The fanout iterates its vector in index order and invokes observer vslot +0x38 before death predicates and target clear run. | Observer vector membership and cross-message arrival order are unproved. |
| LT-IMG-010 | DEAD_TASK_CONSTRUCTION | PROVEN_EXACT | On the reached subpath after the actor+0x30 exclusion guard, death sync requests a 0x24-byte allocation. Only a nonnull allocation is passed to CActorTask_Dead constructor, which stores vtable 0x00F0F048, clears latch +0x20, and sets flags 0x80000005. The returned pointer, including null on allocation failure, is passed to wrapper 0x004843C0; the wrapper returns immediately on null. For the constructed task, flag 0x40000000 is clear, so the wrapper selects the owner+0x20 task-manager lane. | Original timer transition remains open, not task construction. |
| LT-IMG-011 | TASK_MANAGER_PROGRESS | PROVEN_EXACT | Mode 0 stores the incoming task at pending +0x14. Manager flags +0x1C or +0x1D defer immediate update; +0x1E destroys an incoming task. Otherwise manager_add calls queue_update, and with current +0x10 null queue_update calls promote/start 0x004A09C0. That routine gives the ordinary linked queue at +0x04 priority; only when +0x04 is empty does it move pending +0x14 to current +0x10 and invoke its start vslot +0x08. Thus current null alone is insufficient for immediate dead-task start. | Live task-manager flags, +0x04 queue state, and model readiness are not observed in IMAGE. |
| LT-IMG-012 | EVENT_BEFORE_POSE_GATE | PROVEN_EXACT | CActorTask_Dead start tests the CMyActor singleton. When it is nonnull, the task calls general dispatcher 0x005F9C70 before testing actor+0x70 bit 0x40 and before requesting _F_DIE_000. When the singleton is null, the dispatcher block is skipped, but control continues to the later actor/model checks and pose bit gate. | Live general-listener membership is unmeasured. |
| LT-IMG-013 | MODEL_READINESS_GATE | PROVEN_EXACT | Both dead-task start and update gate _F_DIE_000 on actor+0x70 bit 0x40; update retries while latch +0x20 is clear. The separately pinned CNetNPC model callback sets bit 0x40 only after its callback/resource gates complete. | Live model callback completion relative to lethal actor-entry arrival is unmeasured. |
| LT-IMG-014 | DEAD_TASK_PERSISTENCE | PROVEN_EXACT_BOUNDED | When the actor dead predicate remains true, dead-task update can request the pose and run its per-frame helpers without setting task flag bit 0x08. When the predicate becomes false or the actor is unavailable, it ORs bit 0x08 to complete the task. The bounded update body performs no actor-map erase. | Authentic actor removal/despawn carrier and timing remain open. |
| LT-IMG-015 | TIMER_AUTHORITY_BOUNDARY | PARTIAL | The pinned R102 IMAGE census found the bounded BasicAttr+0x58 writers to be constructor, copy, Merge, and wire load, with zero local frame-delta decrementers. Combined with the mutually exclusive timer>0 DYING and timer<=0 DEAD predicates, the proved path needs a later write/snapshot to cross the boundary; IMAGE does not determine original hold duration. | No eligible original actor-entry sequence is supplied or established by the cited inputs. |

## Closures added by this delta

- Within one RuntimeRes handler invocation, actor/death reconciliation returns before the typed terrain/drop lane is called.
- The death-sync body has no direct E8 edge to the six pinned typed terrain/drop functions; indirect and transitive paths stay open.
- On the reached guarded subpath, a dead actor that is the current CMyActor target is cleared before the optional `TargetIsDead` panel event; a null panel lookup suppresses the event, not the clear.
- CMyActor current-target storage is distinct from the typed ActorAttr+0x198 and NPCAttr+0xA8 qwords; their original nonzero producers remain open.
- CHitResult has bounded target-state side effects, but no direct edge to the four pinned name/HP/open refresh consumers in its full handler.
- Actor-entry observer fanout returns before death sync; observer membership and cross-message arrival order remain unknown.
- Dead-task construction requires the actor+0x30 exclusion guard to pass and allocation to succeed; a null allocation reaches the null-safe wrapper without construction.
- Pending dead-task promotion requires current +0x10 null and the higher-priority ordinary linked queue +0x04 empty; current null alone is insufficient.
- The general event precedes the pose gate only when the CMyActor singleton is nonnull; a null singleton skips that dispatcher block while the later pose path continues.
- The dead task retries the pose behind model bit 0x40 and remains active while IsDead is true.
- The timer boundary still has no proved local decrementer in the pinned R102 writer census; no eligible original actor-entry sequence is supplied or established by the cited inputs, so original hold duration and emission policy remain unknown.

## Critical nonclaims

- No claim is made about original-server co-emission, packet cadence, timer value, or hold duration.
- No claim binds the pinned dispatcher/wrapper as a member of the actor-entry observer vector.
- CHitResult-versus-actor-entry arrival order remains UNKNOWN.
- Actor removal, authentic corpse duration, terrain omission, and drop creation ownership remain open.
- The original nonzero producers for ActorAttr+0x198 and NPCAttr+0xA8 remain open; no whole-program arbitrary-alias absence is claimed.
- Direct-edge negatives do not exclude indirect, virtual, tail, alias, or transitive paths.
- The semantic names of bit 0x40000, the relation predicate polarity, and panel vslots are not guessed.
- `CFightMsgVital` was deliberately not followed in this bounded delta.
- No current replacement-server code/runtime/capture/dump was used as evidence in these IMAGE rows or read by this generator.

## Prior canonical pins

- `PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv`: `0192050fab1df86346a8aac069a3f0f3fbe90620589879a89890461780e812ad`
- `PF_ATTR_FIELD_SEMANTICS.tsv`: `1418b7559f5b05feef585490e76d33e8f72cd82c1ff854941d7faf37878c7f2f`
- `PF_ATTR_ROLE_DISCRIMINATOR.tsv`: `3e8d99dd9fd9c8717e27d3ec8d43e2599a6037fc366e58637aff3a5cc8d5ec73`
- `PF_COMBAT_LIFECYCLE.tsv`: `305b7bdc12e9b638e3c3f37f996af8bb0e2d1877241aaf171885b8fae106b658`
- `PF_GROUND_DROP_LIFETIME.tsv`: `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`
- `PF_MONSTER_COLOR_GATE.tsv`: `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0`
- `PF_QUEST_MARK_EVENT_CENSUS.tsv`: `40127e6410c1aa6405efada640c60b72663eb9e35537c8011cdeede47d0a0b35`
- `FACTPACK_R102_DYING_COUNTDOWN_UI_FIELD_STATIC.md`: `642dc3ba52c00e93798d0434d618def1b8fe4d95172470187746e74d3b67c0cd`

## Evidence keys

- `LT-IMG-001`: `ed9af0efb1ac9ae531553345bec7c9d01e37347db508149bf87c9222c73f1a68`
- `LT-IMG-002`: `5f3cd2a49575f2d340c62767df369253cc34c3704caae3dc1c189892b57d27c4`
- `LT-IMG-003`: `41837f0014c6351b42a73e4885c6b5731ff1af14e069aecdd17a7b5693ee43aa`
- `LT-IMG-004`: `f77367678471bf006c8e56c1e9b5240582eb548ee4133d887a05f7753d1a0bdb`
- `LT-IMG-005`: `bdbc8f1f4dc38c59a49712835ed05a81c9a9829807277f13a66b6eb86c5076a1`
- `LT-IMG-006`: `ffc4edf3a1c126f916681c8f5e6523f3adfc53e4ced4dbabf00234062cd8663d`
- `LT-IMG-007`: `ff950f62304dd84c3e49279211cb1b456a62fc455458ec45be421a3f0b81e4be`
- `LT-IMG-008`: `6da1ae19c4840684d488d316c24e331af69051f64dfb40b717ba649482edb5f7`
- `LT-IMG-009`: `9883b92b7bfcbb27db4ba26e7b5c25dba442dbfa8909b45de56674bec5be00f6`
- `LT-IMG-010`: `ad000140272a4a5d6918d42b364ec20ff21e8bb56b564991922bbc65b50fe6db`
- `LT-IMG-011`: `a97dc7b487230562661d790122ed3946aae392f52e894623b98afc8a51d55014`
- `LT-IMG-012`: `03bbd965a701a83e4920d8e234b24160081529104b30738151a8392837746ad3`
- `LT-IMG-013`: `2a64d1abc14b3b9ccad28b6452c09f91011d5f57ba4ce30daa156733b87aebd3`
- `LT-IMG-014`: `e6de8522b5b065a33fc1202ddce322cb9c30d2811ef7bdb802b58cc14804118f`
- `LT-IMG-015`: `42ba6cfc5ac9447121475c303d6a7a622a0aaa2a94fb5a6c133c844affa863de`

## Deterministic verification

```powershell
py -3 pf_rederive_combat_lethal_tail_delta.py --check
py -3 pf_rederive_combat_lethal_tail_delta.py --self-test
```
