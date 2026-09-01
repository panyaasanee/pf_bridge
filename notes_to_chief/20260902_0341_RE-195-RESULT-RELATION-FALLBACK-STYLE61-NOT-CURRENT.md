ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย — ผล RE-195 (ผู้บริโภค LANE-GM; static bridge)

# RE-195 RESULT — DONE / BOUNDED-NEGATIVE: relationship predicate calls the faction comparator only as a fallback; no current pure-server style-61 path

- Ticket START: `2026-09-02T03:35:30+07:00`
- Result time: `2026-09-02T03:41+07:00`
- Queue SHA-256 at start: `cb3088d9b016ac4edb73eba8fd38f1820e6638bc74587a5302fb6a996fcea694`
- Static/read-only only: no game/server boot, no `LOCK_GAME`, no canonical DB, no source/queue/external/gamedata edit.

## Mandatory searches

- ค้นใน `pf_bridge\external\` แล้ว: เจอคำตอบเดิมที่ต้อง verify/re-derive ใน `PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv`, `PF_MONSTER_COLOR_MECHANISM_JOIN.tsv`, `PF_MONSTER_COLOR_WIRE_CONTROL.tsv`, `PF_MONSTER_COLOR_GATE.tsv/.md`, `PF_ATTR_SEMANTIC_REPORT.md`; scope = 2,683 files / 930,201,065 bytes, terms `FONTSTYLEID`, `relationship_predicate`, `0x0043C380`, `0x4A1D50`, `BasicAttr+0x68`, `fontstyle_id=61`, `output_fontstyle_id`. ทุก claim ด้านล่างตรวจกลับกับอิมเมจ SHA เดิมอีกครั้ง ไม่ได้ยกตารางมาเชื่อตรง ๆ.
- ค้นใน `pf_bridge\gamedata\` แล้ว: เจอ `CONSTDATA_TH__AI_WANDER.tsv` และคอลัมน์ `n_OFFESIVE` ซึ่งเป็น local DATA input ของ style-61 branch; ไม่พบ direct wire field ชื่อ `FontStyleID` หรือ direct server field ที่สั่ง style 61 เอง. Scope = 1,109 files / 15,319,585 bytes. ผลลบจำกัดเฉพาะ extracted gamedata tree; ไม่ใช่ whole-program negative.

## Job 1 — relationship predicate vs faction comparator: CLOSED / EXACT

สองฟังก์ชัน **ไม่ใช่ฟังก์ชันเดียวกัน**:

- relationship predicate: VA `[0x0043C380,0x0043C63C)`, file `[0x0003B780,0x0003BA3C)`, 700 bytes, SHA-256 `1d99f8557252742914c4f7358853aac06f0b54603f78a4b4d073aaea2afcbd89`.
- faction comparator: VA `[0x004A1D50,0x004A1E14)`, file `[0x000A1150,0x000A1214)`, 196 bytes, SHA-256 `cbc9d0ab90ed7828534a86c10f42322b09555a5034f71ef7ac14e0cd8e64cac5`.

Recursive CFG re-derive covered 198/198 instructions and all 700 bytes of the predicate, plus 84/84 instructions and all 196 bytes of the comparator; neither span has an unreachable byte or an out-of-span branch target.

The precise relationship is **predicate calls comparator at one conditional fallback**:

1. `0x0043C5CD` loads local resolved attribute `+0x68`.
2. `0x0043C5D4` loads target resolved attribute `+0x68`.
3. After obtaining the relation-table singleton, `0x0043C5E0` directly calls `0x004A1D50`, passing those two dword keys by value.

Exact load/call subspan `[0x0043C5C9,0x0043C5E5)` / file `[0x0003B9C9,0x0003B9E5)` has SHA-256 `1ad67764c3fee4dcd2d4df55f2b4d6ad0e1eaa8bd612228b95326ec96874ee1c`; published fallback result span `[0x0043C5C9,0x0043C5FF)` has SHA-256 `916a45082cc44a28219206b05729cb14f80575f054a56ca7acf1cb14a159f3a1`. Whole file-backed executable-section E8 census found exactly one direct caller of `0x004A1D50`: `0x0043C5E0`.

Important correction to loose prose in `npc_hostile_hypothesis.py`: the two object `+0x68` reads occur in `0x0043C380`'s fallback, not inside the comparator body. `0x004A1D50` consumes the already-loaded keys and performs the relation-table membership/negation lookup. Earlier predicate exits can bypass this fallback entirely, so faction alone is not an unconditional relationship or color switch.

## Job 2 — styles 56/58/59/60/61 input/control matrix: CLOSED

Canonical selector span `[0x00443F50,0x004443C5)` SHA-256 `ee845ee6ef6337ea41ae57a5a4df8af5a8a8ac00e458ea1ce3e587aff1f9cdf9` was joined to the typed RuntimeRes CNetNPC path and current project snapshot:

| Style | Exact selector route | Server-control assessment today |
|---:|---|---|
| 56 | local CMyActor `ActorAttr+0x98 == 1`, or positive actor identity + relationship false | Inputs include direct-wire fields; current shipped positive P identities enter this family. Faction `+0x68` can affect the fallback result but cannot force it because earlier exits exist. |
| 58 | positive identity + relationship true + local-context actor lookup succeeds | Typed same-instance CNetNPC crosswalk exists, but lookup/context outcome is not proved pure-server-controlled. |
| 59 | positive identity + relationship true + prior lookup not selected + secondary relation query true | Typed same-instance CNetNPC crosswalk exists; secondary query/context outcome is not proved pure-server-controlled. |
| 60 | signed-nonpositive identity + relationship true | `+0x68` participates only in the conditional fallback. Current shipped Foundation writers use positive identities, so no current route reaches this lane. |
| 61(a) | typed `NPCAttr+0x98/+0x9C` associated-actor identity, nonzero/not-self, lookup succeeds | Standalone row still lacks a complete typed/current server-control closure. |
| 61(b) | typed CNetNPC and local `AI_WANDER.n_OFFESIVE != 0` | Exact typed path exists. Server selects an upstream template key; `n_OFFESIVE` itself is local DATA, not a direct style wire. The path is after the signed-nonpositive selector gate, which current positive identities bypass. |
| 61(c) | typed CNetNPC, `n_OFFESIVE == 0`, unnamed actor `+0x70 & 0x100` set, two local vslots false | CHitResult/CMissileHitResult can set the bit indirectly, but writers require a signed-negative target identity and further client/runtime gates. Current positive P identities fail before the bit can be set. |

The direct-wire facts are narrow: `BasicAttr+0x68` is W+R tag `0x14`, mask `0x0400` and is a predicate operand; `ActorAttr+0x98` and `+0x1A0` are also wire-carried operands. None is a direct `FontStyleID` field. `PF_MONSTER_COLOR_WIRE_CONTROL.tsv` therefore correctly labels the conclusion `DIRECT_STYLE_WIRE_OPEN;PROVED_UPSTREAM_INPUTS`, not direct final-style control.

## Job 3 — can current server inputs alone drive fighting style 61?: CLOSED / BOUNDED NEGATIVE

No current production-ready pure-server gate chain was found.

- `field_mobs.py:340-342` currently composes `actor_identity = 0x2000 + placement_index + 1` (positive high dword zero); current file SHA-256 `a4fc6eaee6351d10e7bb44abb527db51966f217d474318a92078811bb79bb865`.
- `PF_MONSTER_COLOR_GATE.md`'s pinned Foundation writer census independently concludes that the shipped snapshot writers use positive P identities. Positive identity enters the 56/58/59 family and bypasses the typed CNetNPC 61/62 tail.
- The connected CHitResult path cannot repair this today: IMAGE proves its bit-0x100 writers require a signed-negative target. The current positive P identities fail that gate before the bit is set.
- Choosing a template with `n_OFFESIVE != 0` likewise does not overcome the earlier identity lane. It is a local table property behind a server-selected template, not a direct dynamic “fighting” switch.

Therefore P-2 cannot be implemented safely today by merely changing faction, template, or emitting a hit. A coherent nonpositive identity mapping plus a typed/live gate proof (or an equivalent new server-controllable route) is still required before style 61 can be treated as a server-driven fighting color.

## Input/output integrity

- `GameClient.local.bin`: 14,759,424 bytes; SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- `PF_ATTR_NAME_COLOR_SELECTOR.tsv`: SHA-256 `d15864a21a7a124a23f6dffad174a55d376045a25a04814bbe6dc5f5632af82d`.
- `PF_ACTOR_RELATION_INTERACTION_GRAPH.tsv`: SHA-256 `0192050fab1df86346a8aac069a3f0f3fbe90620589879a89890461780e812ad`.
- `PF_MONSTER_COLOR_MECHANISM_JOIN.tsv`: SHA-256 `dfaf5f31380c3ce6a0cfffd6b8778e1a28154b6438f5f404067b402c3d324190`.
- `PF_MONSTER_COLOR_WIRE_CONTROL.tsv`: SHA-256 `8fbffa366c495e323a9c87dc443316b1b2352a534b2bd47a97c2766361cae70d`.
- `PF_MONSTER_COLOR_GATE.tsv` / `.md`: SHA-256 `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0` / `57dff3dfb518dfe3d60b7ebfb01d9f2325d69c78eac940dfbfb6d3bafab7f596`.
- `CONSTDATA_TH__AI_WANDER.tsv`: SHA-256 `0b3f1eb8e67915c4be5758c734cae17c575ac2aa76cb989e13242cfb6ad01a23`.
- `npc_hostile_hypothesis.py`: SHA-256 `907065ac755fc12096429e94005f2fa461f43032816c01e9349ffa9f7e0fbb67`.
- All source inputs above and the queue were rehashed after analysis and remained unchanged. Only this result letter and runner bookkeeping are written.

## Nonclaims

- No style ID, relationship boolean, or faction value is assigned the gameplay noun friendly/hostile/attackable globally.
- Style 61 is not renamed `n_AGGRO`, “fighting,” or bit `0x100`; it has multiple causes and all conclusions here are conditional static reachability.
- A server-controllable upstream operand is not claimed to guarantee a rendered nameboard; controller allocation, readiness, lookup, local vslots, delivery order, and runtime branch outcome remain client/runtime gates.
- No original closed-server identity policy is inferred from the replacement project's current positive P scheme.
- The bounded negative covers audited direct selector paths and the pinned current Foundation snapshot; it is not a whole-program proof against aliases, indirect/custom serializers, or future composers.
- This is static IMAGE/DATA/source evidence only; no client-observable screen behavior was tested.

## BUILD_IMPACT

`BUILD_IMPACT: do not wire P-2 fighting color to faction +0x68, n_OFFESIVE, or CHitResult alone. The relationship predicate is multi-input and uses the faction comparator only as a fallback; the current positive identity scheme bypasses the typed style-61 tail and also fails the hit writer's signed-negative target gate. Keep P-2 blocked on a coherent nonpositive identity mapping plus typed/live gate proof (or a newly proved equivalent control seam). No source patch was made by the RE runner.`
