# PF Quest-Mark Resource Resolver

Artifact pair SHA-256: `c9c9e96ee67762cdaab18bf12d6cf22c1a4cf82c83270f50562a849c90985304`
Canonical final IMAGE route key: `79839063b5f2dad4f09c2c9022857ca6842763281547d762147f6939ccbb77cb`
Special DATA control key: `270ef783a275112122482e38259c62f2d7547e4627b239502623802fb8c925c3`

## Outcome

The static client route is closed only as a **conditional mechanism**: the eight already-owned selector literals reach the texture manager; `.tga` is compared case-insensitively and rewritten by replacing its last character (`.tga -> .tg_`, never appending); transformed-first/original fallback, the generic image entry, a registered TGA filter/header/decode reader, and the shared board binder all exist in the pinned IMAGE.

The result is deliberately not called a runtime success. Concrete file open, callback state, reader selection, asset-specific decode return, texture upload/bind, and visible pixels remain `OPEN` for all eight selectors.

Rows: 29 total (20 IMAGE, 9 DATA). Every TSV row carries exactly one source layer.

## Pinned inputs

- IMAGE: `GameClient.local.bin`, 14759424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- Selector reference: `PF_ATTR_QUEST_MARK_SELECTOR.tsv`, 52137 bytes, SHA-256 `3218d619a400dfcab52416489dcf8e6b85e6cbfd5a8bbd14d6ccad39dbfb9bf0`.
- DATA binding reference: `PF_ATTR_DATA_BINDINGS.tsv`, 53723 bytes, SHA-256 `67e7550a09b00a5243f4c084ff486d29e420c6d0687704a092f157dbce219cb2`.
- Generic packaged resolver reference: `PF_GROUND_DROP_LIFETIME.tsv`, 61979 bytes, SHA-256 `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710`; only `GDL-IMG-018/019` are cited.

## [COMPOSITION][IMAGE+DATA] Eight selector candidates

This table is the only cross-source join. It does not create mixed-source TSV rows or elevate runtime status.

| selector | owned selector key | IMAGE literal | IMAGE replacement candidate | DATA exact-case | DATA casefold | DATA census key |
|---:|---|---|---|---:|---:|---|
| 1 | `5464435ef50cdb99c6bdae1894455461970957c2294f7d1b23e7f12b1ab11439` | `%sQuest_begin.tga` | `Quest_begin.tg_` | 0 | 1 | `eb545b864f5de7cd85611febc984266eae20ade7495d2d5937cefef867217067` |
| 2 | `9eefcfa3f4c47b1c8aec68e788ec30b3e71cb7547953e905f602125738b74ea3` | `%squest_again.tga` | `quest_again.tg_` | 1 | 1 | `2a285916a2527036251cec952274078441b27c34fe37d53a3758bfe51066cf74` |
| 3 | `8e0a307d7d14bbd2a66916938320d9e2b4ed96d57e81e538a723137268663ede` | `%sQuest_end.tga` | `Quest_end.tg_` | 0 | 1 | `02f63349fa81361a0c78d54e7dd119511af9c1624ce682d33e579d2596bb872a` |
| 4 | `ce7016e63d533dd7ac87809df14e1cc8aa2e727178b8c1f6180e970551d83b13` | `%squest_againend.tga` | `quest_againend.tg_` | 1 | 1 | `0a6cb3cffe8be1cd6023ee204cbe0cab7ab7141941102184532eb575cbf88eb0` |
| 5 | `a23f05a8298f622f2942b57f14d26f8ed8c6e61af066157b0f6b538415edf43e` | `%sQuest_ing.tga` | `Quest_ing.tg_` | 0 | 1 | `e6ea2a2540ed4d7b0b744670703244fe48b8cec99ce30b45ae79df3cff8aa4bc` |
| 6 | `68c906aabaca780c17e7d796e56d965ad34a2c09debbc5cd53d38a6bbf9cea05` | `%squest_low.tga` | `quest_low.tg_` | 1 | 1 | `3772805898aa3c88db137fd7833505890f98fb55ed516c883e24adee81def197` |
| 7 | `719515671edf8347af6ced4ca86a7ec94c9aa29ef0f502fa4d8a609507023bd2` | `%squest_dungeon.tga` | `quest_dungeon.tg_` | 1 | 1 | `1b200ee58e0d948a51cc0019590a04714d85fd88006fbf08038b8b30bbcc5479` |
| 8 | `2e2a66518ed5fab2335da6e58e8e98b361edbc21610d05336816c76e080e1e4a` | `%sQuest_SpBegin.tga` | `Quest_SpBegin.tg_` | 0 | 1 | `0e30d5676391bfe0f1556042624a146e5faa273d0d2ba31ddc0137455f5ef017` |

Four formatted candidates retain uppercase spelling while the shipped filenames are lowercase, so their exact-case count is zero but their casefold count is one. That DATA census is not promoted to a runtime filesystem-open result.

## Special double-extension control

`quest_splend.tga.tg_` is a distinct DATA-only control: 5608 packaged bytes, SHA-256 `32c578abcce2dbf8b39bcfcc9153a6b2cff8908b1ad6bca29c2983366281462e`. It decodes in memory to 16428 bytes with SHA-256 `907238162d8d02676be8e09c9ba48d1964a3bfbc34b911cab917c88ec77782a9` and a 64x64x32 type-2 TGA structure. No bytes or pixels are emitted.

The exact IMAGE rewrite would map `quest_splend.tga` to `quest_splend.tg_`; it cannot produce `quest_splend.tga.tg_`. The pinned IMAGE also has zero exact UTF-16 occurrences of `quest_splend.tga` and `%squest_splend.tga`. These facts do **not** exclude dynamic construction or a separate loader path, but no selector association is proved.

## Exact static boundary

1. Selector identities, formatter call, and board binder are cited from `PF_ATTR_QUEST_MARK_SELECTOR.tsv`; their predicates are not duplicated.
2. The manager/cache/resource loader and exists/open callback machinery are exact static control flow, conditional on runtime state.
3. `_splitpath_s` plus `_stricmp` admits `.tga`, and the success tail overwrites the last character with `_`.
4. The converter's reader list dispatches virtual +0x04 filter, +0x0C header/type parse, and +0x08 decode. The registered TGA vtable maps those slots to `0x0092B340`, `0x0092B880`, and `0x0092BC60`.
5. The exact runtime bridge from the generic texture-source object to that converter instance is not proved for the eight quest resources; neither is a returned/bound/visible texture.

## Duplication and source policy

- Selector branch facts are imported by their eight selector keys and pinned artifact hash.
- Existing DATA pixel/shape rows are imported only by binding/evidence keys; this artifact adds filename-census facts and the missing special control, not duplicate pixel interpretations.
- The generic packaged resolver and `$pcz` wrapper are cited as `GDL-IMG-018/019`; their generic claims are not reissued.
- IMAGE and DATA never share one TSV row. Cross-source inference is confined to explicitly tagged composition prose/table here.

## Measurement labels, methods, and controls

Every TSV row has nonempty `measurement_label`, `method`, and `control` fields. Their accepted combinations are fixed by source and row kind, are included in each evidence key, and are enforced by schema plus mutation checks.

| boundary | measurement_label | reproducible method | required controls |
|---|---|---|---|
| Local IMAGE spans/censuses | `MEASURED` | pinned-image hashed-span/control-flow assertions, virtual-slot/vtable assertions, or whole-image exact UTF-16LE census | image size/hash, exact span hashes, decisive operands/calls, explicit runtime-open ceiling |
| Local DATA filename/special control | `MEASURED` | immediate-directory exact/casefold census and in-memory `$pcz` structural validation | file size/hash, fixed queries/counts, structural hashes, no raw-byte or pixel output |
| Imported selector/resolver/binder facts | `REFERENCE` | pinned artifact size/hash plus exact key join | key existence, no local primary evidence, no claim reissue |
| Aggregate static ceiling | `COMPOSED_BOUND` | IMAGE-only composition of hashed local rows and pinned IMAGE reference keys | single IMAGE source, no DATA fields, all runtime states remain OPEN |

The `[COMPOSITION][IMAGE+DATA]` table above remains Markdown-only and therefore is not mislabeled as a measured single-source TSV row.

## Runtime blockers / required evidence

A source-separated trace must record, per selector: formatted path; rewrite input/output; installed callback targets; transformed and fallback open results; selected reader vtable; header/decode returns; created texture identity; board binder return/state; and client-visible presentation. Until then `runtime_open_status`, `runtime_bind_status`, and `runtime_pixels_status` remain `OPEN` in every row.

## Reproduction

Run `py -3 pf_rederive_quest_mark_resource_resolver.py --check` beside these artifacts. Check mode reads all pinned inputs, reconstructs both outputs, verifies their embedded pair key and stable publication state, and performs no writes. Run `--self-test` separately to perform the same read-only published-pair check plus memory-only mutations covering missing/blank labels, wrong source methods, reference/composition promotion, and a decisive IMAGE span byte.
