# PF pool 0x00638690 closure overlay

[MEASURED] IMAGE-only additive result. V1 remains immutable.

## Result

The four requested Priority-1 messages are structurally CLOSED in this isolated overlay:

- `Community_AddFriendVital`
- `Community_AddBlackListVital`
- `Community_RequestSoulMateMatchVital`
- `Community_ReplyPenpalLetterVital`

Isolated priority effect: **+4 CLOSED**. This report intentionally does not state a combined project headline because other independent overlays may be applied before or after it.

The A2 overlay contains 40 exact V1 directives: 8 `CHANGED` indirect rows become `SUBCALL:0x00637FC0`; 32 rows are removed (8 cross-direction artifacts and 24 pool/refcount lifecycle artifacts). The priority overlay contains 4 exact V1 `OPEN -> CLOSED` directives. Unchanged rows copied: 0. Duplicate delta keys: 0. Existing-overlay base-key overlap: 0. The current post-V1 priority overlay is pinned at sha256 `69dae68b987d8102355eed3c1684f1a1829d0bb70d69b56010ace3d21b87bf51` and touches none of these four base rows.

## Serializer roots and call sites

| message | member | exact root span | span sha256 | W subcall | R subcall |
|---|---:|---|---|---:|---:|
| `Community_AddFriendVital` | `+0x48` | `0x006448A0..0x0064498F` | `645560a112bc5938b11bea612cf90299958cc15b57fe1adb30fffddfde8231cf` | `0x0064491C` | `0x00644987` |
| `Community_AddBlackListVital` | `+0x48` | `0x006448A0..0x0064498F` | `645560a112bc5938b11bea612cf90299958cc15b57fe1adb30fffddfde8231cf` | `0x0064491C` | `0x00644987` |
| `Community_RequestSoulMateMatchVital` | `+0x2C` | `0x00644A50..0x00644B29` | `c90a027c309ab7e20f0f9b63840ef4149774ccccb9ac2aff7d43e3ef1150f1ca` | `0x00644AB6` | `0x00644B21` |
| `Community_ReplyPenpalLetterVital` | `+0x34` | `0x00644C10..0x00644D51` | `78fcc7ddb3cca5009ff13cac567977efaef2825c20e260c6ea3fe61f4954ee83` | `0x00644CDE` | `0x00644D49` |

Each writer site loads the member, then its vtable and slot `+0x14`, and passes the root stream plus the writer mode. Each reader site calls `0x00638690`, stores that exact result back to the same member, then reloads the member and calls the same vtable slot with reader mode zero. The V1 cross-product row for the opposite direction at each site is therefore removed, not re-labelled.

## Fixed pool identity

- Helper span: `0x00638690..0x006387D9`, file offset `0x00237A90`, sha256 `cc56e669d0f3c5c714f2f00780b946c7ab9930407d0d8a324380dc3fbbcfecbd`.
- Its two successful construction arms write vtable `0x00F3568C` at `0x0063870C` and `0x0063879C`. The only function return is `0x006387D6`; zero-allocation paths throw or fault before it.
- Vtable prefix: file offset `0x00B33A8C`, sha256 `c63c641d579e046481fce29c3c61d5356abe89ba227e60a4cb87e656e7580325`; slot `+0x04 = 0x00638370`, slot `+0x14 = 0x00637FC0`.
- Slot `+0x14` span: `0x00637FC0..0x00638035`, sha256 `66073191421eb2b758f27584a3d4ea96a2712ce1011725f73de1c792a373e240`. It calls base serializer `0x00637CC0` and proves both write/read primitive families; the base span is sha256 `7037b86c221f423f84e056820a7b72d7772d27b4b36acb0cd409c54dea05586b`.

The root call passes only pool-this `0x0102FB94` and constants `0x00F0A90C`/zero. The helper has no wire-primitive call and does not receive the root stream register. Its direct calls are lock/unlock, allocation, construction, accounting, and a non-returning exception path. Therefore the helper row is lifecycle, not a wire field.

## Member provenance and atomic identity

The four concrete constructors write their message vtables and zero the exact members `+0x48`, `+0x48`, `+0x2C`, and `+0x34`. Each matching message destructor loads that same member and calls `0x0088D060`. In the reader root, EAX from `0x00638690` is copied to EBX, compared with the old member, the old object is decremented if different, EBX is stored to the member, and that same EBX is incremented. The subsequent subcall reloads the same member. This proves old/new identity rather than inferring it from proximity or naming.

## Destructor full reachable CFG

| function | reachable instructions | exact span | sha256 |
|---|---:|---|---|
| `pool_dtor` | 27 | `0x00638370..0x006383CE` | `7b848f45d7cb2a79f793fd3b600058c820da42c27afcd59299095f1bd2605f3a` |
| `pool_base_dtor` | 34 | `0x00637830..0x006378B3` | `5fe2bc775355de8b676f44c55f693a45786ef5bff4f795e1ad98453c67557d0c` |
| `base_object_dtor` | 31 | `0x0088D280..0x0088D2F0` | `d914c8eaef424f2988c6b76b6954acbb9247bd4309a2c8f0e09439cc64f1104a` |
| `pool_lock` | 4 | `0x0088D5B0..0x0088D5BA` | `281bb0603facf9b7c61c87c0241b74e59ff6488057f979782e4d08ea4e4e9ee8` |
| `pool_unlock` | 4 | `0x0049DA40..0x0049DA4A` | `91f8bd361459e6514e2c53ca4bac3bd9d76baddaf75ee1b1562afecee8d96366` |

The complete reachable chain is fixed to the pool destructor, four `basic_string<wchar_t>` destructors, base-object cleanup (its sole diagnostic leaf is `USER32!MessageBoxW`), `EnterCriticalSection`, `LeaveCriticalSection`, and `MSVCR90!free`. It has no stream formal, no stream alias from the caller, no unresolved register call, and no wire primitive. Thus the dynamic decrement row resolves to a nonwire destructor, while the increment helper is the already pinned `InterlockedIncrement` at `0x0088D050`.

## Boundaries

- `source=IMAGE` on every row; no DUMP, CAPTURE, or DATA fact is mixed into this overlay.
- Closure means the indirect serializer target and lifecycle effects are statically resolved. The nested serializer is referenced as a subcall; its child fields are not duplicated or flattened into parent offsets here.
- This result does not claim a runtime RTTI class name or capture validation.
- No raw client, dump, or capture bytes are emitted.

## Reproduction

Run `py -3 pf_build_pool_638690_closure.py --check`. It re-hashes the image and V1 inputs, verifies all pinned spans/imports/CFGs and registry roots, checks existing-overlay overlap, applies a residual-UNKNOWN guard, and runs independent mutations of the vtable slot, member store, helper target, and destructor call target.
