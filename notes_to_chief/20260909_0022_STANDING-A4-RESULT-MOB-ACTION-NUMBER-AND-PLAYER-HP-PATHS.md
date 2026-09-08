งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: LANE-B (GT-224), chief, LANE-GM; cc LANE-K/COO

# A4 PARTIAL — mob attack, player hit number and resident HP are distinct routes

[MEASURED][IMAGE] Mob action, numbers on the player and resident HP have distinct routes. This round joins the UpdateAttr destination to the HP reader; synchronized visible attack remains unproved.

ROUND=codex-a4-20260909-static; START=2026-09-09T00:10:07.1269465+07:00. No eligible RE ticket; Panya directed continued standing work. No milestone promotion.

## Three received surfaces

| Effect | Logical vital | Concrete contract and remaining gates |
|---|---|---|
| Mob action task | ActionVital `0x1AEA` | +0x18 qword performer; +0x30 u32 behavior selector -> lookup 0x702A10 -> allocation/UseBehavior ctor 0x47AB30. RE-065 admits CNetNPC on the ordinary path; 0xEA80 has a separate type branch. Behavior/resource, task/queue readiness and clip remain separate gates. |
| Player hit number | CHitResult `0x16F7` | Header +0x18 qword performer; entry +0x00 qword target, +0x08 signed i32 value, +0x1C u16 flags. Resolved target -> suppression helper keyed by header +0x20 -> 0x43FDE0, target as receiver. |
| Player HP | UpdateAttrVital `0x309A` | ActorAttr key `0x12AD`; inherited BasicAttr current/max +0x44/+0x48, bits 0x0004/0x0008, tag 0x14, width 4. Handler 0x5F2400 resolves resident type at local-player+0x130, then incoming CopyTo +0x24. Full replacement, not sparse merge. |

[MEASURED][IMAGE] Named registration/getter/vtable binds each route. These memory offsets are not wire positions. Three logical messages do not imply three transport packets or a proved arrival order.

## Mob-to-player number admission

[MEASURED][IMAGE; CL-IMG-006/008, R102] The independent number pass 0x750D12..0x750DAF is not gated by the earlier CMyActor-source bit-0x100 side effect.

0x43FDE0 first requires localplayer != null and localplayer+0x420 != 0. It then compares BOTH dwords: performer==localplayer jumps at 0x43FE86; independently, target==localplayer jumps at 0x43FE8E. Both go to 0x43FEFB and bypass the six relationship filters. Thus mob performer + local-player target has an exact conditional admission path. Target existence, suppression/readiness/resource and camera/presentation conditions still apply.

[MEASURED][IMAGE] Ordinary flags 0x0001 and non-local performer select number type 1. Entry +0x08 passes through the two's-complement abs idiom before decimal formatting: -7 -> 7; INT32_MIN is excluded because abs overflows. This flag value is a branch example, not original policy or a complete flag audit. Header +0x24's local-performer resource readout is separate.

## New closure: update destination and HP reader share the pointer

[MEASURED][IMAGE] Follow-up beyond the previous encoder guard, which ended before insertion:

1. CMyActor constructor 0x44C990 calls CNetActor constructor 0x457340. At 0x4573BC it obtains an ActorAttr; 0x4573C1..0x4573D5 caches the SAME pointer at actor+0x348 and passes it to 0x5F8C10 on actor+0x130.
2. Insertion thunk adds 0x50, then reaches 0x463930 -> 0x463720. For a nonnull Attr and absent class key, 0x46379C builds a pair containing the original pointer. Tree insertion 0x731280 -> 0x731090 -> node builder 0x767EA0 copies the u16 type key to node+0x0C and the exact pointer to node+0x10. It does not clone the Attr in that copy. A duplicate class key takes the false-return branch; the claim requires successful insertion.
3. UpdateAttr lookup thunk 0x5F8C30 adds the SAME 0x50; 0x463800 searches the same u16-key tree and returns node+0x10 at 0x463849. With that attachment retained, CopyTo therefore writes the object also cached at localplayer+0x348. Later replacement/detachment is outside this construction-time join.
4. ActorAttr +0x24 -> 0x464F30 -> BasicAttr CopyTo 0x464B40. Stores at 0x464B8F copy incoming +0x44/+0x48 into resident state. Omitted fields can be zeroes; full-state preservation is required.

[MEASURED][IMAGE] HUD block 0x53F18B..0x53F1E4 reads that cached +0x348 pointer. Local-player byte +0x358 selects the pair: zero -> BasicAttr +0x44/+0x48; nonzero -> ActorAttr +0x1A8/+0x1AC. This byte is NOT CNetNPC's +0x358 Attr pointer. The latter pair needs its own high-mask bits 0x40/0x80 (overall bits 38/39), so changing only BasicAttr HP cannot establish a bar change for every player state.

The binder at 0x53ED28..0x53EDA4 identifies `PROGRESSBAR_HP` -> controller+0x18 and `NUMBERLABEL_HP` -> +0x1C. Actual call 0x53F1DF -> 0x53EED0 passes current/max. The helper requires nonnull widgets and nonzero max, computes the ratio for the progress control and stores current at number-label+0x220. Refresh scheduling, later state changes and rendered pixels remain runtime facts. Reread addresses correct the older prose's call-at-0x53F1DD; 0x53F180 is inside an instruction, not this method's entry.

BUILD_PROPOSED: Connect an admitted mob ActionVital and player-target CHitResult to the existing full-state player UpdateAttr path, keeping original timing/behavior/flag assumptions explicit and honoring current runtime gates | LANE-B with chief and LANE-GM | acceptance: one identifiable mob action, number over the same player, corresponding resident HP and HUD reduction, preserved unrelated fields, then a second attack; token absent until game evidence

[PROPOSED] Observe task, number and resident/HUD values separately. Stop on unresolved behavior, changed attachment, reset fields or wrong HP pair. Floating digits do not prove an HP write. No encoder or runtime flag is created.

## Evidence and reproducibility

IMAGE SHA-256 before=after: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` (14,759,424 B).

New join ranges are half-open; file offsets follow the VA ranges:

| Span | File start | SHA-256 |
|---|---|---|
| 00457340..004573D5 | 00056740 | 3cb3eea087754fa3ed7048bb831da4e67e96deda063699474712184ef0b71c7d |
| 00463720..004637F6 | 00062B20 | 1a9279dd7589c6e1b48a27044434274565212220daae4c34f0b4c6928a6840b3 |
| 00767EA0..00767F36 | 003672A0 | b56eacf2cd26449575a06763e9dbcb49a14106553d74d621331c8c4de343b565 |
| 0053F150..0053F1E4 | 0013E550 | eba82d39fb9362e0552ad53aa9bfb5ff662101225da0f4c8bdef13d1a9be2b70 |

`staged/standing_a4_wire_manifest.json` records all 37 spans with VA/end/file/SHA, eight source hashes and five reused CL-IMG-001/002/006/008/009 evidence keys. All selected rows and support spans are sampled (100%, above 20%). Reuse key CL-IMG-008: `7a9fe8b9bc4b11841beac0a53da6c595ab2ccec6b4d1eb37fb5f598c8ea9c780`.

[MEASURED][TOOL] `standing_a4_wire_verify.py`: PASS spans=37 rows=5 edges=22 branches=10 pins=33 fields=20 mutation_traps=122. It verifies manually interpreted bytes/calls, not native execution. Actual in-memory mutations of spans, branch/call displacements and pins are rejected.

From pf_bridge:
```powershell
& 'C:\Users\Panya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B .\staged\standing_a4_wire_verify.py
```

Search: external registry, reference_codex_attr, root/archive/consumed R102/RE-065/222/314 and tools/reports HP/HUD guards. Examined gamedata MOBS/AI_COMBAT do not supply a proved mob-specific behavior-to-clip crosswalk here. ORD-001 was read; its no-HP-mutation premise exceeds bounded direct-edge evidence. No global negative or full ORD-001 completion is claimed.

PARTIAL: routes/join established; original choreography, selected mob clip and visible result unproved. Need same-build behavior/resource binding and an attended three-surface observation. Next A5; do not repeat the route census.

[NONCLAIM] No original recipe, multiplayer/persistence, cadence, universal absence of indirect HP effects or gameplay acceptance. IMAGE facts are grade A; integration is proposed. No game/server/DB/ServerProject/lease/queue/external/gamedata/Git mutation.

SCOREBOARD: NONE | Mob attack, hit number and HP reduction still await one game observation | standing_a4_wire_manifest.json; next=A5
