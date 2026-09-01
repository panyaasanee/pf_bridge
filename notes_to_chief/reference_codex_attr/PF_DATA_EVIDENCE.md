# PF DATA Evidence

This is a DATA-only structural census. It does not promote DATA observations into IMAGE, DUMP, or CAPTURE facts.

## Scope and integrity

- Input: all 290 XML files inventoried under `GameClient/Data`.
- Every input size and SHA-256 matched `PF_INPUT_INVENTORY.tsv` before parsing.
- Every input SHA-256 was rechecked after parsing and did not move.
- The TSV contains names, structure, counts, sizes, and SHA-256 only; XML attribute values are not published.
- Every TSV row is labelled `source=DATA`.

## Results

- Standard XML parse: 287 files.
- Nonstandard pseudo-XML grammar: 3 files.
- Surface-mask documents: 287 files, 916 `SurfaceMask` records.
- Avatar-offset documents: 3 files, 303 structural `Item` records.
- Distinct file hashes: 184; duplicate-content groups: 1 (107 files).

The three avatar-offset files have the same deliberate nonstandard item grammar: a space after `<` and a comma between attributes. They are recorded as `NONSTANDARD_GRAMMAR`, not silently repaired.

## Protocol relevance

This DATA set describes scene surface masks and avatar display offsets. It supplies no exact serializer field order, thunk target, or runtime class identity, so it does not close any protocol UNKNOWN by itself.

## Files

- `PF_DATA_EVIDENCE.tsv`: one DATA-only row per input XML file.
- `PF_DATA_EVIDENCE.md`: this interpretation and integrity summary.
