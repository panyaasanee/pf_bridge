# PF Actor Relation Interaction Graph

## Scope and result

This is an additive, IMAGE-only P0-4 artifact. It uses a neutral actor
relation/interaction title because the audited client decisions do not prove one
universal monster flag.

P0-4 has two different questions:

1. **Audited client-local IMAGE mechanisms.** This artifact closes the bounded
   surfaces listed below: kind-0x19 registration and its two typed target
   producers, the CNetNPC query-result gate, near-send versus approach attachment,
   the separately layered NPCConversation inbound/UI route, the ChooseNPC
   registered routine boundary, and the relation function's final result
   surfaces plus 31 per-site direct-call rows.
2. **Original-server assignment policy.** This remains **OPEN**. IMAGE does not
   reveal how the original server chose relation inputs, NPCAttr flags, parsed MOBS
   values, conversation responses, or attack eligibility. Those inputs must not be
   inferred from the client-local mechanisms.

## New measured IMAGE facts

- `ARIG-IMG-001`: the canonical general-registration control remains 140 direct
  registrations with digest `9f352999fc90400dcba1bda7899c4486eeff3f29ed8b57b7a0ba716f27622a01`. Filtering
  that same instruction-shape census yields exactly one direct kind-0x19 site,
  `0x00615B7A`, with subset digest `70db49876ca7df2198a6f856a7f8ec2db9f2dba92bc10158791be6b0eee01db1`.
- `ARIG-IMG-002` and `ARIG-IMG-003` separately record the two kind-0x19
  producer bodies. Both carry target identity and target pointer fields; numeric
  values 0x201 and 0x205 remain unnamed and the target class is UNKNOWN.
- `ARIG-IMG-004`: one typed CNetNPC interaction route additionally requires a
  synchronous query result byte at event +0x14 to be nonzero.
- `ARIG-IMG-005`: after that gate, native distance logic either reaches the
  already-canonical ChooseNPC send or attaches an UNKNOWN 0x50-byte approach
  object. Allocation size is not a class identity.
- `ARIG-IMG-006` is WIRE_CODEC only: the registered NPCConversation handler
  resolves QuestModule and forwards the inbound message. `ARIG-IMG-007` is
  UI_NATIVE only: it copies message +0x18/+0x1C to module +0x80/+0x84, chooses one
  of two quest-conversation UI models, and calls vslot +0x210 with InitQuestList.
  The composition is stated here; the TSV does not mix those evidence layers.
- `ARIG-IMG-008`: the registered ChooseNPC routine is only `mov al,1; ret 4`; no
  UI/service side effect exists inside that five-byte routine.
- `ARIG-IMG-009..011`: the relation predicate has final result surfaces returning
  constant 0, the prior-owned +0x68 comparator result, or constant 1. These rows
  index result production only and do not rename either boolean.
- `ARIG-IMG-012..042`: 31 file-backed executable-section
  E8+rel32 byte-pattern sites resolve to 0x0043C380. All 31 raw sites were
  independently validated by the generator itself as instruction-start
  `call 0x0043C380` in a pinned Capstone 5.0.6 x86-32 skipdata linear
  sweep anchored at `.text` 0x00401000. Every site has its own exact trusted local
  span/hash, source, layer, class-or-UNKNOWN, prior digest, and nonclaim. Partition
  digest `446026f8be4dfc475a95812b7974ada5635940add61c0e3d55569979f3e479ed` uses
  `SHA256(ASCII site lines joined by LF plus one terminal LF)`.

| Bounded surrounding-output family | Sites | Meaning ceiling |
|---|---:|---|
| talk/interact-adjacent | 4 | not talkable/role |
| target presentation | 3 | not actor class |
| enemy target / target state | 10 | not universal hostility |
| color/style/nameboard | 3 | not role or rendered pixels |
| unresolved | 11 | UNRESOLVED |

The five categories describe only bounded surrounding output. They are not
relation-domain labels. The 31-site census is not a CFG/runtime census and excludes
indirect calls, dynamic targets, aliases, and tail-call routes. A prior manual
consumer audit of MOBS +0x48 / BasicAttr +0x6C is deliberately not published as a
TSV negative because this re-deriver does not reproduce its function-body/alias
coverage.

## What remains non-implementable

- `NPCAttr +0x7A` remains a bounded gate in one CNetNPC route. Its original
  producer/policy and universal role meaning are not proved.
- `BasicAttr +0x6C` retains the prior `LOADED_COPIED_ONLY` ceiling. This artifact
  publishes no new deterministic consumer census for it.
- MOBS `n_AI_COMBAT` retains the prior `LOADER_ONLY` ceiling. This artifact
  publishes no new deterministic parsed-MOBS +0x48 consumer negative.
- The 0x50-byte approach object's class/completion callback is UNKNOWN.
- ChooseNPC-to-NPCConversation original response policy is absent from IMAGE.

No Attr semantic or scope status changes in this P0-4 pass. This is the second
no-delta checkpoint for the lane, so P0-4 must pause under the master anti-stall
rule after publication. The bounded verdict is:

`AUDITED_SURFACES_EXHAUSTED / ORIGINAL_POLICY_OPEN`

## Evidence discipline

- Rows: 42; source IMAGE: 42.
- Layers: STATIC_NATIVE=39, LUA_BRIDGE=0, UI_NATIVE=1, WIRE_CODEC=2.
- Every row has one source, an exact class or UNKNOWN, measurement method, control,
  negative scope, VA/file span, SHA-256, prior reference, and prior claim digest.
- Prior facts are cited rather than copied. For prior artifacts without an embedded
  `claim_sha256`, `prior_claim_digest` is SHA-256 of the selected complete TSV row
  serialized as sorted compact ASCII JSON.
- TSV SHA256: `630df0cdbaa1ce380f3040eb2304e2b0efdb602b614dacd8d6e1872600a1b6dc`.
- Image size: 14759424; image SHA256 before/after: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

## Re-derive

```powershell
py -3 pf_rederive_actor_relation_interaction_graph.py --check
py -3 pf_rederive_actor_relation_interaction_graph.py --self-test
```

`--check` rebuilds exact bytes in memory, verifies every pinned input/span/anchor,
validates source/layer/class/prior/duplicate/site-list guards, and checks a stable
marker-before/files-twice/marker-after snapshot without writing outputs.
`--self-test` mutates source, layer, prior digest, site list, and a committed pair
in memory and requires every corruption guard to reject it.
