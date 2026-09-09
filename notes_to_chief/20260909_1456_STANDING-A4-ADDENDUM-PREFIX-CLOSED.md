# STANDING A4 ADDENDUM — CNetNPC fallback prefix producer closed

**ADDRESSEE:** Chief / LANE-B combat runtime owner  
**DATE:** 2026-09-09 14:56 +07:00  
**STATUS:** STATIC COMPOSITION PASS; corrects one conditional in the 14:49 result  
**LANE:** fixed Binary + previously decoded original DATA and shipped assets; no client/server run

## Correction to the 14:49 result

The earlier result correctly proved that MOBS row 31 has an empty
`s_PREDESCRIPT`, so `0x0045DA60` selects `CNetNPC+0x338`.  It left the value
of that fallback conditional.  RE-321 had already proved its typed producer;
this addendum composes that closed result into A4 rather than repeating the
closed ticket.

`CNetNPC` vtable slot `+0x60 = 0x0045DAE0`.  On that same object:

1. `0x0045DB4E` loads `CNetNPC+0x358`, the bound `NPCAttr`.
2. `0x0045DB54` addresses the full wstring at `NPCAttr+0x7C`.
3. `0x0045DB61..0x0045DB96` splits it with exact literal `L"_"` and requests
   token index zero.
4. `0x0045DB9C..0x0045DBA2` assigns that token to `CNetNPC+0x338`.

Therefore, whenever `NPCAttr+0x7C` is `M011_000_000_SP3`, the fallback prefix
is exactly `M011`.  With row 31's empty `s_PREDESCRIPT`, the A4 builder's six
known answers are:

```text
.\Data\GC\A\M011_F_SENTRY_000.kf
.\Data\GC\A\M011_F_FLEX_000.kf
.\Data\GC\A\M011_F_ATTACK_000.kf
.\Data\GC\A\M011_F_ATTACK_001.kf
.\Data\GC\A\M011_F_ATTACK_002.kf
.\Data\GC\A\M011_F_ATTACK_003.kf
```

The original decoded MOBS row 31 and the 14:33 asset result independently pin
`s_OUTFIT=M011_000_000_SP3`; RE-321 pins that the wire field is a complete
visual-preset basename and pins the underscore-token-zero producer used by
the action prefix.  This closes the previous binary-semantic uncertainty
about `actor+0x338`.  A live run would still be required to prove that the
particular Tornado Eagle instance received that value.

## Fixed-image provenance

Image `GameClient.local.bin`: size 14,759,424; SHA-256
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
before and after.

| role | VA span | file span | SHA-256 |
|---|---|---|---|
| `NPCAttr+0x7C` consumer, underscore split and `CNetNPC+0x338` assignment | `0x0045DAE0..0x0045DC34` | `0x0005CEE0..0x0005D034` | `e1c061b56e4cdd73c19916da302e6085de203bb841b85f48a25331d92c53516d` |
| underscore literal | `0x00F0E07C..0x00F0E080` | `0x00B0C47C..0x00B0C480` | exact UTF-16LE `5f 00 00 00` |

Dependency results were pinned by content:

- RE-321 result SHA-256: `300d592899afadd40c41ef1467399ba8fb266d6b8078cb661466768af267e39f`
- 14:49 A4 callback result SHA-256: `d2ef1020524ef91d9438db93ae4a7c21aea4932b562463fcf90e08e6c7a7d83a`
- RE-321 byte guard SHA-256: `3be1cd44b71ec8e788d805ded1f6f21871afc99759e47219473a12bed176a0e2`

## Evidence grade and remaining boundary

- **A:** the typed `NPCAttr+0x7C -> underscore token 0 -> CNetNPC+0x338`
  producer, the prefix `M011` for input `M011_000_000_SP3`, row-31 empty
  `s_PREDESCRIPT`, the path formula, descriptor entries, and packaged assets.
- **D conditional remains:** callback `0x0064D580` may modify an action token
  before path construction when `CNetNPC+0x248` is non-null.
- This addendum does not claim a live Tornado Eagle received the preset, that
  the modifier was skipped or preserved a token, that map lookup returned a
  record, that a clip rendered, or that selector 3220 caused attack/damage.
- The underscore token feeds the action prefix.  The separate `.avt` path uses
  the complete `NPCAttr+0x7C` basename, as RE-321 proved; these two uses must
  not be conflated.

## Verification

- verifier: `pf_bridge/staged/standing_a4_prefix_verify.py`
- verifier SHA-256: `ad6de867df2305d4f96a269f85c40e78055b70ce6aa461cf1a29c7ec2e3ecd59`
- log: `pf_bridge/staged/standing_a4_prefix_verify.log`
- log SHA-256: `1c583dd2c07e606a9098237d44ea3c67662f882ea64645c61f0272b08f0846b0`
- result: `PASS dependencies=4 consumer_spans=1 byte_markers=3 known_prefix=1 known_paths=6 traps=3; NPCAttr+0x7C underscore-token0 -> CNetNPC+0x338 exact; live field value and action modifier unproven`

The stdlib-only guard re-runs the pinned RE-321 and A4 callback/asset guards,
checks the exact consumer span and instruction bytes, checks six known paths,
and rejects delimiter, preset-prefix, and empty-prefix mutations.

## BUILD_PROPOSED

For the next attended selector-3220 run, treat the prefix formula as a static
known answer.  Record the actual `NPCAttr+0x7C` value, then focus the trace on
`CNetNPC+0x248`, input versus post-`0x0064D580` token, final path, map return,
visible clip, and damage correlation.  Stop this candidate if the live preset
is not `M011_000_000_SP3`, the modifier produces an unlisted token, or the map
lookup is null. | LANE-B / attended-test owner | callback trace plus visible
client observation
