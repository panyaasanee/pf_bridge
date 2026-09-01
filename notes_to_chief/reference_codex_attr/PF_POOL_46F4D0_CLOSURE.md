# PF pool 0x0046F4D0 closure overlay

[MEASURED] IMAGE-only additive result. V1 remains immutable.

## Result

The four requested Priority-1 messages are structurally CLOSED in this isolated overlay:

- `ActorInspectVital`
- `StorageResultVital`
- `ItemMallBagUpdate`
- `CollectionObj_UpdateCollectionObjBagVital`

Isolated priority effect: **+4 CLOSED**. No combined project headline is claimed here because independent overlays may be applied in either order.

The A2 overlay contains 40 exact V1 directives: 8 `CHANGED` indirect rows become `SUBCALL:0x0046F180`; 32 rows are removed (8 cross-direction artifacts and 24 pool/refcount lifecycle artifacts). The priority overlay contains 4 exact V1 `OPEN -> CLOSED` directives. Unchanged rows copied: 0. Duplicate delta keys: 0. Duplicate base keys: 0. Existing-overlay base-key overlap: 0.

The current post-V1 priority overlay is pinned at sha256 `69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51` and touches none of these four base rows. The string-wire correction is pinned at sha256 `e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2` and has zero base-key overlap with these A2 directives; its rows are not duplicated here.

## Fixed pool identity

- Helper `0x0046F4D0` has 87 reachable instructions in exact span `0x0046F4D0..0x0046F5DB` (sha256 `b9308abc49969ded9194d369823de1f29207ca8addcfe22f838a4b3d1ea45885`). Both allocation/reuse arms call constructor `0x0046F3F0`; the constructor has 36 reachable instructions and stores vtable `0x00F0ECB8`.
- Vtable `0x00F0ECB8` has destructor slot `+0x04 -> 0x0046F470` and serializer slot `+0x34 -> 0x0046F180`. The serializer body is pinned at `0x0046F180..0x0046F3E9`, sha256 `29e38267ab54c852e3f1338c2fb833e3b9d1a41903544a390489c264c09fa813`.
- The exact teardown walk contains 23 internal CFG nodes. It reaches no wire primitive. Every indirect call is either a pinned non-wire import or a register loaded from `_invalid_parameter_noinfo`; refcount recursion is stopped at the separately pinned `InterlockedDecrement` helper because no stream alias is passed.

## Serializer roots and call sites

| message | member | exact root span | span sha256 | W subcall | R subcall |
|---|---:|---|---|---:|---:|
| `ActorInspectVital` | `+0x20` | `0x005EAC90..0x005EADCA` | `04c9bf8a126dbea9013a9578688f6d4b07dfdef13537da0cffe48f3c6da7168e` | `0x005EACFB` | `0x005EAD88` |
| `StorageResultVital` | `+0x1C` | `0x00699820..0x00699904` | `3e473b3e5a0e1ba60ca67a2ff8f2f2913e47fa2de3ccd91e5db923f8bc0b9c0b` | `0x0069987C` | `0x006998FC` |
| `ItemMallBagUpdate` | `+0x14` | `0x006B9C80..0x006B9D1D` | `2d5e2820834ad57bdf4e26ef71364cffb255bb99b709f9d2fb3682f3ad4e27ec` | `0x006B9CBA` | `0x006B9D15` |
| `CollectionObj_UpdateCollectionObjBagVital` | `+0x14` | `0x006E1120..0x006E11C4` | `5f8071ac25254d83f9403fd96253ab2bfc22d7cf5c93a4e94d3f5e7be13ca226` | `0x006E115D` | `0x006E11BC` |

Each writer path loads the member, its vtable, and slot `+0x34`, then passes the root stream and writer mode. Each reader path calls `0x0046F4D0`, stores that exact result into the same member, increments its reference, reloads the member, and calls the same `+0x34` slot with reader mode zero. Constructors initialize each member to null; the corresponding destructor path decrements that same member. All four message-vtable reference censuses and vtable-to-root mappings are exact.

Root reachable-instruction counts: `actor_root`=100, `collection_root`=63, `itemmall_root`=61, `storage_root`=88.

## Evidence boundary

This closes static wire structure only. `0x0046F180` is referenced as a nested serializer and is not flattened into these four message rows. Runtime semantics, current object contents, and capture agreement are not promoted. Every emitted TSV row is `source=IMAGE`; no DUMP, CAPTURE, or DATA fact is mixed into the overlay.

Publication is atomic per file, not as a multi-file set. The final V2 manifest remains the set-level commit point.

## Reproduction

```powershell
py -3 pf_build_pool_46f4d0_closure.py --check
```
