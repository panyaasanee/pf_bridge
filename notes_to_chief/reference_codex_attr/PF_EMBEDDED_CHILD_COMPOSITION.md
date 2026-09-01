# PF embedded-child composition closure

[MEASURED] This IMAGE-only additive overlay resolves two parent serializers through exact this+0x18 constructor composition and exact child-vtable slot +0x34 targets.

## Outcome

- ActorActivity_UpdateDailyActivityStateVital: both coarse R/W indirect-jump rows become references to DailyActivityState. The pinned effective child has 6 R + 6 W rows and 0 UNKNOWN. Parent status changes OPEN to CLOSED.
- DBSS_GuildStorageInitialVital: the E4 branch is W and the F3 branch is R. Two impossible coarse-direction rows are removed; the two valid rows become references to CGuildStorageAttr.
- DBSS remains OPEN. Its old indirect-jump blocker is replaced by the pinned CGuildStorageAttr blocker set; the primary group is DYNAMIC_DISPATCH_OR_SUBCALL_UNRESOLVED.
- The A2 delta contains 4 changed references and 2 removals. It contains zero child field rows and zero unchanged copied rows.

## Duplicate control

All six targets are exact frozen V1 line/full-row-hash pairs. The generator scans every pre-existing TSV for those pairs before publication and fails on any prior target. The child tables are dependencies referenced by hash and delta key, not materialized again.

## Effective projection after Daily plus composition

- P1: 255/365 CLOSED, 110 OPEN. P2: 8/16 CLOSED. P3: 71/138 CLOSED. Overall: 334/519 CLOSED.
- Stored canonical A2 rows: 8657. Embedded-child reference rows: 4. UNKNOWN A2 rows: 3963. Generic CALL/JUMP UNKNOWN: 1312. Direct invalid-parameter UNKNOWN: 881.
- P1 blocker groups: call/effect 14, dynamic 78, indirect jump 0, object/graph 7, registry identity 11.

## Verified IMAGE spans

| role | start VA | end VA exclusive | file offset | SHA-256 |
|---|---:|---:|---:|---|
| actor_parent_ctor | `0x006A0FE0` | `0x006A1044` | `0x002A03E0` | `518da7bf9b8cd319022ad373e9b5f208679dcbaf4133426fef3babeb9ed10024` |
| daily_child_ctor | `0x0069CCF0` | `0x0069CD56` | `0x0029C0F0` | `423f46497dba4785787b7174bf6b571677e6ff6443e2c4b280867022f54dc64f` |
| daily_child_vtable | `0x00F3C510` | `0x00F3C548` | `0x00B3A910` | `6e7c3bac1c80aba92afb3d6ecdab7b740971fd7b02efe2fc876c628b163a8f7d` |
| actor_parent_serializer | `0x0069F700` | `0x0069F716` | `0x0029EB00` | `25accf437e846ede788f403ada721771b2629f1f2adb393f4bee3d0bc2f6c9c7` |
| dbss_parent_ctor | `0x00672940` | `0x006729A4` | `0x00271D40` | `ed42b5893e95f369ce9f2e22ae28ffe1a412d96d3a14a1ac5246e729fae43a34` |
| guild_child_ctor | `0x006720F0` | `0x00672106` | `0x002714F0` | `58072a2d6fa0328e9e3201ab5fbaa60a6c847c56ecccb2267aaeda4eb553b1c6` |
| guild_child_vtable | `0x00F39108` | `0x00F39140` | `0x00B37508` | `6c910b23ab9e924cab8669b9e6d53129ddfc47a7558300d77a604cdeea3f2ff9` |
| dbss_parent_serializer | `0x006723D0` | `0x00672491` | `0x002717D0` | `3429135c0f917857db707bb8f6fdf362cbef42f4ff1d22f75e64aae919cec588` |
| guild_child_serializer | `0x00469FA0` | `0x00469FD8` | `0x000693A0` | `828554cb9ece35a2316ffc9e8bf44be3b2ef033bd189cb9b15400ecd3b48c63f` |

## Pins

- image SHA-256 before/after: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Daily A2 dependency: `10b54ee781ad0147d5bd18c0171b88132d9fd61dc39e0adf6fa4055bc7b7890d`
- Daily priority dependency: `395b1776d3351304612ceb36eade9003b929fb8bb914986b4873f0737e60a5e3`
- slot34 A2 dependency: `1778728a2d4ec53562a51ea0361bca530942f48d0f49af18b295f1ff6a49c334`
- V3 status predecessor: `37eb9ca4ebc25f0fdcd4e9e56d8458c031beee9b98640cb95a84be3a8a7553c6`
- `PF_A2_EMBEDDED_CHILD_COMPOSITION_DELTA.tsv`: `b81c7a5590d60c44f10e4171a722feb680e0e83865e6c5c033121e9dccffbe00`
- `PF_PRIORITY_EMBEDDED_CHILD_DELTA.tsv`: `048216205e1a99a1b4561bf643e1ad80bcf1a29283a4b526ee048654fac82d44`
- generator: `a8963458bc15fa13e7a60adf79fc75ae5183937af88ffa9a05602fbc9f8f7bba`

## Bounds

This proves static embedded-child identity and the exact slot target only. It does not copy child fields, claim runtime capture validation, name an UNKNOWN runtime class, or resolve CGuildStorageAttr internal dynamic calls. No server, runtime, dump, capture, workflow, queue, Git, or GameClient file is changed.

## Reproduction

Run `py -3 -B pf_build_embedded_child_composition.py --audit-only`, then `--self-test`, the normal publish, and `--check`. The self-test injects KeyboardInterrupt after target-to-backup, proves a second actor cannot unlink/replace a held lock, and preserves a pre-existing foreign lock. Windows publication holds a CREATE_NEW kernel handle with READ-only sharing through the transaction; success marks FileDispositionInfo on that same handle, while failure closes without disposition and leaves lock/recovery. No pathname check-then-unlink is used. Daily closure uses the canonical full tag/offset/length/order/gate/unflattened-subcall predicate with built-in mutations.
