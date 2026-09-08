งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B (GT-224), chief, LANE-K; cc COO

# A3 PARTIAL — omission, queued erase and same-identity re-entry

[MEASURED][IMAGE] Registry removal is a distinct operation from the dead-task pose. The useful ordering boundary for re-entry is **completion of queued erasure**, not simply receipt of an omission packet. This joins prior RE-092/MCG-IMG-050 to the existing lookup/factory path; it does not establish an authentic corpse timer or visible respawn.

ROUND: codex-a3-20260908-2359-static; START=2026-09-08T23:59:49.2664133+07:00.
No eligible RE ticket. Panya directed continued standing work for the expected 12-hour queue gap. Master v3's M3-closed statement conflicts with NOW/COO status; no milestone is promoted.

## Sequence

1. [MEASURED][IMAGE; reused CL-IMG-014/015/017, LT-IMG-010/011/013/014] A registered identity takes the existing-actor vslot +0x20 path, reaching death sync. First creation takes init +0x10 instead. For CNetNPC, HP=0 with BasicAttr+0x58 >0 selects DYING; HP=0 with ordered +0x58 <=0 selects DEAD. The dead task additionally needs the actor+0x30 exclusion branch to allow creation and allocation to succeed. Pending task promotion, higher-priority ordinary tasks, manager flags and model-ready bit 0x40 remain separate gates. A constructed task is not proof of a played pose.
2. [MEASURED][IMAGE; reused LT-IMG-014] While the dead predicate remains true, the bounded dead-task update can stay active and request `_F_DIE_000`; the false/unavailable branch marks task completion bit 0x08. This is task state. No duration in milliseconds or complete transitive absence of removal is inferred from that body.
3. [MEASURED][IMAGE; reused MCG-IMG-006/050, RE-092] When an actor collection invokes reconcile, it increments manager+0x04 and stamps incoming actors at actor+0xD0. A registered stale-generation actor, except the dynamic-type token 0x0102CB04 exemption, is queued by POINTER at manager+0x2C. The same path calls 0x441C40 and ORs actor+0x70 with 0x100000. This is not a death-only condition: omitting another nonexempt member can remove that member too.
4. [MEASURED][IMAGE] 0x441C40 passes actor+0x318 to a routine with receiver `[0x01093198]+0x180`, then performs list/cleanup operations. The later manager frame method 0x446750 dispatches actor vslot +0x18 before calling 0x4463D0. The queued eraser reads each pointer's identity at +0x78/+0x7C, finds its node in manager+0x0C, erases the matching node and clears the queue. Registry removal and these cleanup calls alone do not prove when pixels disappear or object destruction completes.
5. [MEASURED][IMAGE; A3 join] Lookup 0x446170 returns the matching node payload. Reconcile branches on that result: nonnull -> existing actor +0x20; null -> factory 0x446990. On successful factory return it stamps the new result; factory can reject or fail and its +0x10 initialization has its own requirements. Thus a subsequent nonzero identity whose old node has actually been erased reaches lookup-miss/create, conditional on no other insertion and a successful valid factory path. This proves a re-entry route, not a respawn timer or visible success.

## The same-identity ordering hazard

[MEASURED][IMAGE] The incoming generation stamp at 0x446FC1 and the eraser at 0x446452..0x4464AB operate on different conditions. The eraser derives a qword key from the queued pointer and erases the found node without a generation test in that pinned consumer segment. The lookup returns a node payload, rather than rejecting it by the removal flag.

[PROPOSED][COMPOSITIONAL HYPOTHESIS] If a queued old pointer and its identity remain valid, the old node remains registered, and no intervening callback drains/cancels that pending removal, an immediate same-identity re-entry can update the old actor; a later drain can still erase the node. A generation refresh alone is not sufficient proof of resurrection. This conditional hazard is not a measured packet-pump ordering or a claim about all transitive callbacks.

BUILD_PROPOSED: Use the normal mob lifecycle to retain the complete intended actor roster through death, omit only expired corpses, and prove erasure has completed before claiming a same-identity return as respawn; preserve task/model readiness checks | LANE-B with chief runtime integration, existing GT-224 | acceptance evidence: actor key + old/new pointer, enqueue, erase and factory order correlated with one visible death/disappearance/return and a second kill; token absent until measured

[PROPOSED] A guessed one-frame delay or fixed sleep cannot replace that evidence. Stop on stale-pointer access, unrelated actor disappearance, or missing factory/erase evidence; return the discrepancy to LANE-B. No new ticket, runtime flag or server patch is made here.

## Provenance

IMAGE: GameClient/GameClient.local.bin, 14,759,424 bytes; SHA-256 before=after:
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
All ranges below are half-open, VA then file offsets:

| Role | VA | File | SHA-256 |
|---|---|---|---|
| reconcile | 446F30..4470E5 | 46330..464E5 | c47bc46a06d6ffe95bee17b572f9ccb7e03442cdd27f04807c1161c03642d880 |
| early cleanup | 441C40..441C91 | 41040..41091 | f7b9b6afd070ed2a9082675109224ee20a830595eefa54899614562927061861 |
| queued eraser | 4463D0..446517 | 457D0..45917 | 7b77c2af7329311d9d17b5e18c34a7e1729e1318677fb714e56f3e2f2c9f52a9 |
| frame | 446750..44680B | 45B50..45C0B | 35a15297378ef5c7f22927b40fbaf0f59b8268e98659521fa3eb05163045b408 |
| lookup | 446170..4461E6 | 45570..455E6 | 9aca8f9a7b933faf54502943e8474362617f3c703cb82750990ba7a9488960e7 |
| factory | 446990..446B2C | 45D90..45F2C | 5f68239f8661419da2ea9bea4e4a2cb9bcdcaa37fe6e4cd53b701116aeeb697d |

Reuse: MCG-IMG-050 evidence_key `d0dd8b09315992903f6fd8a8ef1652a359d8713653ae0afb74ca9ab52a51dc39`; LT-IMG-014 `e6de8522b5b065a33fc1202ddce322cb9c30d2811ef7bdb802b58cc14804118f`. All 10 reused rows, their evidence keys, source hashes and all primary/support spans are checked and printed by the verifier (100% of selected rows, above the 20% sample floor). The log supplies all 31 span records, including the death predicates and animation/queue support.

[MEASURED][TOOL] `staged/standing_a3_lifecycle_verify.py`: PASS rows=10 spans=31 calls=8 branches=6 anchors=13 mutation_traps=58. Actual in-memory altered spans, call displacements, branch displacements and opcode anchors are rejected. This is hash/site verification of manually interpreted x86, not native execution or automatic semantic derivation.

Re-run from pf_bridge in PowerShell:
```powershell
& 'C:\Users\Panya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B .\staged\standing_a3_lifecycle_verify.py
```

Search before decoding: external registry -> RuntimeRes; reference_codex_attr -> MCG/lifecycle/lethal-tail; archive/consumed -> RE-092/107/161. Examined gamedata MOBS/STANDARD_STATUS/GET_SHIPCORPSE labels supplied no corpse-timer crosswalk. No inference from names/IDs, global absence claim or new whole-image census.

## Remaining boundary

PARTIAL / method ceiling: original hold duration, packet-pump separation, model readiness during the lag, presentation teardown and live respawn. Needed: same-build original death/omit/re-entry sequence for policy; attended actor/task/model/erase ordering for the symptom. No repeated pose/queue investigation without new evidence/objective; A4 is next.

[NONCLAIM] No diagnosis that next-target attacks cause promotion; no guarantee that every factory call creates a visibly new mob; no generic ReliveVital contract; no equivalence between ground-drop and actor lifetime. No client/server launch, database access, ServerProject edit, queue edit or Git operation. No new runtime acceptance grade; exact IMAGE facts are grade A, the scheduling hazard is grade D.

SCOREBOARD: NONE | Corpse disappearance and respawn still await game evidence | standing_a3_lifecycle_verify_20260909.log; next=A4
