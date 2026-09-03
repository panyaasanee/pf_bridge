# CODEX VTABLE BOUNDARY CORRECTION AND EMPTY-CLOSURE CONFLICT - 2026-08-31 03:52 +07:00

Immediate IMAGE-only correction to the active Attr overlay.

## Vital boundary correction

- The pre-fix remaining census was SHA-256 `6c69f6b358c1990a930966f2a33aa932fadb3515330ee73d7e414776778525d6`.
- `UpdateAttrVital` pre-fix key `06dbf29c497f7edde08b34eb046e6baac89521402a911dc1ec611cf54a5a5b94` is corrected from nominal slot +0x34/P1 to its own paired codec at +0x18 = 0x005E42C0/P0. Its 0x24-byte primary table ends at 0x00F30404, where the exact adjacent `ReliveVital` table begins.
- `Express_ClientGetExpressItemAttrsVital` pre-fix key `2ab055c0acfca75439e830465e05a33cfa41950809861af0aa4e302712ed1de6` is corrected from nominal slot +0x34/P1 to its own paired codec at +0x18 = 0x006E8920/P0. Its 0x24-byte primary table ends before the exact adjacent `Express_ClientSendExpressVital` table at 0x00F40CE4.
- Erratum to the preserved 03:32 notice: Update's adjacent table starts at 0x00F30404, not 0x00F30408. Express nominal +0x34 = 0x006E5740 is the adjacent class size getter (`mov eax,0x88; ret`), not its ID getter.
- A direct scan of all 519 registry stubs and 501 uniquely linked getter/vtable identities found exactly these two Attr-filter boundary crossings at or before own +0x34.

## Unsupported empty-closure conflict

- Seventeen classes have a physically empty own +0x34 target but retain at least one legacy `PF_SERIALIZER_FIELDS.tsv` row with a non-EMPTY tag.
- The empty body does not prove those legacy calls are wire payload. It also does not justify calling the cross-artifact case closed until each legacy row receives a measured NOT_WIRE correction.
- These 17 rows are now explicit `UNSUPPORTED_CROSS_ARTIFACT_EMPTY_CLOSURE` conflicts, not silently closed successes.

## Active generated state

- Remaining codec census: 124 rows; owning paired codecs 38 (36 at +0x34, 2 at +0x18); non-codec +0x34 routines 25; empty +0x34 routines 51; unlinked 10.
- Detailed field rows: 324.
- Container rows: 23.
- Unresolved rows: 257.
- Conflict rows: 637.
- Deterministic script completed with unchanged image SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

No server/client/runtime/test/Git/lease action was performed. The old 03:32 note remains preserved and is superseded only for the two errata stated above.
