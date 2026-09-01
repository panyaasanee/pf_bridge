# PF Monster Color Wire / Control Census

## Answer

[MEASURED][IMAGE][BOUNDED][OPEN] No direct S2C field that supplies `FontStyleID` or an embedded `FontStyle` to the CNetNPC nameboard is proved by the audited literal/immediate, direct-E8 sink, and pinned typed-path surfaces. Direct wire control remains OPEN: variable-loaded fields, embedded structures, indirect/custom codecs, and undecoded serializer directions remain outside the proof.

[MEASURED][IMAGE] On the audited CNetNPC path the client selects the final style ID locally, while the proved server influence is through upstream actor/Attr/event inputs.

[PROPOSED] Do **not** add a guessed monster `FontStyleID` packet field. The bounded, evidence-aligned implementation surface is identity, relation/faction/category operands, death operands, NPC template identity, and conditional hit events.

## Server-controllable inputs

| Input | Control | Client-side consequence | Important boundary |
|---|---|---|---|
| [MEASURED][IMAGE] RuntimeRes actor type | Direct wire | type 4 constructs CNetNPC | does not prove gameplay class `monster` |
| [MEASURED][IMAGE] RuntimeRes identity qword | Direct wire, invariant-constrained | signed high dword selects positive/nonpositive selector lane | registry/target identity safety is not proved for arbitrary negative values |
| [MEASURED][IMAGE] BasicAttr +0x68 | Direct wire predicate operand | CNetNPC `n_FACTION` input to local relation logic | predicate has other inputs; no complete enum domain |
| [MEASURED][IMAGE] ActorAttr +0x98 / +0x1A0 | Direct wire predicate operands | affect local relation/category selection | no universal gameplay labels for every value/owner |
| [MEASURED][IMAGE] BasicAttr +0x44 / +0x58 | Direct wire operands | together form the exact CNetNPC death predicate | either operand alone is insufficient |
| [MEASURED][IMAGE] NPCAttr +0x78 | Direct wire template key | chooses local MOBS/AI_WANDER row and therefore local `n_OFFESIVE` | `n_OFFESIVE` is not sent directly |
| [MEASURED][IMAGE] CHitResult / CMissileHitResult identities | Indirect event control | can set unnamed actor bit `0x100`, later used by the local selector | handler gates and typed target must pass; bit is not named aggro |
| [OPEN] Final FontStyleID / embedded style | no direct field proved on audited surfaces | emitted/applied locally on the audited CNetNPC path | variable/embedded/indirect/custom paths remain outside the bounded negative |

## Bounded negative methodology

Image guard: size `14759424` bytes; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

The script parses the six PE sections and scans every byte position where a five-byte `E8 + rel32` encoding fits inside `min(VirtualSize, SizeOfRawData)`. This is a raw byte-pattern census; it does not infer instruction boundaries and therefore does not use a linear-disassembly negative.

- [MEASURED][IMAGE] Direct WRITE calls: 1350; site-list digest `88ddff5cd217b6db25fb757e381b02b8af75666aa5e70278ca972acfbb85f09a`.
- [MEASURED][IMAGE] Direct READ calls: 1350; site-list digest `9d774988d901db651ab224c7b02a08aa284c6af86c63a52807e37ba73b95261b`.
- [MEASURED][IMAGE] Every one of those 2700 sites was checked for raw `PUSH imm8` and `PUSH imm32` encodings of literal values 55..67 in the preceding 64-byte, same-section window: zero candidates.
- [MEASURED][IMAGE] Direct calls to the controller style store: 0; digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- [MEASURED][IMAGE] Direct calls to the selector: 1, exactly `0x004446A7`.
- [MEASURED][IMAGE] `FontStyleID` literal dword references: 3; embedded `FontStyle` references: 2. They are confined to the pinned GUI property/parser sites in this census.
- [MEASURED][IMAGE] The selector, controller store, NPC label sink, style parsers, and the two direct UI style-setter forwarders contain zero direct WRITE/READ primitive calls.

[OPEN] This negative excludes only those nearby literal-immediate patterns and the counted direct E8 edges into the audited sinks. It does not exclude a variable-loaded field, embedded structure, indirect call, custom codec, alias, whole-object copy, or transitive dataflow; therefore the global direct-wire question remains OPEN.

## Pinned serializer-inventory ceiling

[MEASURED][IMAGE] The pinned IMAGE-derived serializer inventory (SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`) contains 519 messages and 6931 rows. Of these, 2711 rows use the audited direct primitive tag set and 202 rows are EMPTY (101 W, 101 R).

[OPEN] Literal terms `FontStyleID`, `FontStyle`, and `LABEL_NAME` occur zero times in that pinned table. Term absence is not field or dataflow absence: the EMPTY directions and variable/embedded/indirect/custom paths still require tracing.

## Conditional implementation boundary

[PROPOSED] Claude has enough static evidence for a bounded experiment using the upstream inputs above. It is not yet evidence-safe to claim a production-complete color implementation, because arbitrary signed-negative identity policy, exact relation domains, complete bit writers, delivery order, nameboard readiness, and rendered outcomes remain unproved runtime facts.

[PROPOSED] The narrowest next test is to vary one upstream input at a time while preserving actor registry/target identity and all readiness gates. A guessed direct style field is specifically unsupported.

## Provenance and non-duplication

Every TSV row is `source=IMAGE` and carries a primary VA range, file-offset range, and span SHA-256. Existing mechanism facts are cited through `reference_keys`. New claim/evidence keys are unique, but uniqueness does not mean independent evidence: reference rows and the final control row are joins/syntheses and are not counted as new independent mechanism proof. The verifier rejects reused gate evidence keys and missing or malformed gate IDs/ranges.

[OPEN][DELIVERY] These artifacts are local-only in `pf_bridge/external`, outside the canonical ServerProject Git worktree, and therefore untracked by that worktree. Another clone needs owner-approved packaging/ingest through `PF_CRITICAL_ARTIFACT_AUTHORITY`; availability must not be assumed.

Artifact pair SHA-256: `6e2041061bc42b44934fd309059eb4177b136714d30e2b5eec5a5c8061d80cc7`. The same value is present in every TSV row; a mixed-generation TSV/Markdown pair is therefore detectable.

Rows: 15. Direct style-wire fields proved: 0. Status: OPEN.
