# RE-321 RESULT — NPCAttr+0x7C reaches one of the eight remaining `.avt` xrefs

ADDRESSEE: LANE-B (COMBAT) — consumer and build owner; LANE-K — fold RE-321

- Status: **DONE/PASS (static-on-bridge)** — all eight previously unwalked `%s%s.avt` xrefs were walked to their source strings.
- Layer: IMAGE static only. No client/server boot, capture, queue edit, lease edit, commit, or push.
- Image: `GameClient.local.bin`, 14,759,424 bytes.
- SHA-256 before and after: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

## Direct answer

**(a) Yes.** Exactly one of the eight remaining xrefs reaches the `basic_string<wchar_t>` at `NPCAttr+0x7C`: the `%s%s.avt` use whose literal dword is at **VA `0x0078AB08` / file offset `0x00389F08`** (the `push` starts at `0x0078AB07`).

The complete same-object chain is:

1. `NPCAttr` binds to `CNetNPC+0x358` at `0x004697DD..0x004697EB`.
2. `0x0045DB4E` loads `[CNetNPC+0x358]`; `0x0045DB54` takes `NPCAttr+0x7C`; `0x0045DB58..0x0045DB5B` assigns the full wstring to presentation descriptor `+0x60`.
3. The descriptor constructor at `0x0045C220` installs vtable `0x00F0DF3C`; vtable slot `+0x14` at `0x00F0DF50` is `0x0078AA50`.
4. `0x0078AAF4` takes `c_str()` directly from descriptor `+0x60`; `0x0078AAFD` pushes that pointer as the second `%s`; `0x0078AB07` pushes `L"%s%s.avt"`; `0x0078AB0D` formats the path.

**(b) The `.avt` path uses the whole wire string as its basename.** There is no semicolon, tab, or space tokenizer between descriptor `+0x60` and the format call. A list cell such as `A;B` would therefore be formatted literally as `.\Data\GC\V\A;B.avt`, not reduced to `A` at this xref.

The same upstream function also splits `NPCAttr+0x7C` on underscore (`L"_"` at `0x00F0E07C`) at `0x0045DB61..0x0045DB96`, takes token index 0, and assigns that separate result to `CNetNPC+0x338` at `0x0045DB9C..0x0045DBA2`. That token does **not** feed the `.avt` format: the `.avt` vfunc reads the earlier full copy at descriptor `+0x60`.

Question (c) does not apply because a positive reader was found. The actual route is nevertheless pinned above so the field does not remain an unexplained wire value.

## Census of the eight source strings

| `%s%s.avt` dword VA / file offset | Source proved before the format call | Token behavior at this xref | `NPCAttr+0x7C`? |
|---|---|---|---|
| `0x006AD785` / `0x002ACB85` | callee arg 1; caller obtains it with `c_str()` from internal record `+0x28` at `0x006AED80..0x006AED89` | whole string | no |
| `0x006D2F12` / `0x002D2312` | internal record `+0xF8`, copied into a local wstring at `0x006D2D3A..0x006D2D48` | whole string | no |
| `0x006D7922` / `0x002D6D22` | `MOBS.s_OUTFIT`: table `L"MOBS"` at `0x006D76E2`, column `L"s_OUTFIT"` at `0x006D7771`; tokenize on `L";"` at `0x006D77DE..0x006D77EB`; hard index `0` at `0x006D790E..0x006D7912` | semicolon token 0 | no |
| `0x006D9C18` / `0x002D9018` | internal lookup result `+0xF8`, pointer saved at `0x006D9AD2..0x006D9AD9` | whole string | no |
| `0x006F2C50` / `0x002F2050` | internal lookup result `+0xF8`, pointer saved at `0x006F2B0A..0x006F2B11` | whole string | no |
| `0x0076788F` / `0x00366C8F` | `STALL_SET.s_STALL_ITEM`, read at `0x007677F4..0x00767805` | whole string | no |
| `0x0076D8F8` / `0x0036CCF8` | helper `0x00767260` opens `STALL_SET` and reads `s_STALL_ITEM` for the supplied row key, then returns the assigned wstring | whole string | no |
| `0x0078AB08` / `0x00389F08` | presentation descriptor `+0x60`, assigned from `NPCAttr+0x7C` at `0x0045DB4E..0x0045DB5B` | **whole string** | **yes** |

This is a complete 8/8 census. Together with RE-296's five walked sites, the `%s%s.avt` literal has 13/13 source paths accounted for.

## Pinned proof spans

All offsets below are raw file offsets in the pinned image.

| Purpose | VA span | File span | Span SHA-256 |
|---|---|---|---|
| xref 1 caller fields | `0x006AED76..0x006AED91` | `0x002AE176..0x002AE191` | `637ef19fea1a4a4ba473b4edfb556f39cf22cfaa4c76fa74d9ea2ec300798a21` |
| xref 1 arg consumer | `0x006AD610..0x006AD8AD` | `0x002ACA10..0x002ACCAD` | `843caef1a482bdd222cce0390a5b1489d343b7f96d0d97a74d01c76997376367` |
| xref 2 record `+0xF8` | `0x006D2CA0..0x006D307B` | `0x002D20A0..0x002D247B` | `61bbff3508ddb7925a133216f545f5753119dd31a72ad64cb1f8c6a0c53c9631` |
| xref 3 `MOBS.s_OUTFIT` token 0 | `0x006D76E2..0x006D792C` | `0x002D6AE2..0x002D6D2C` | `5804c2b000887dc20ca9b94095a5cd9944cbe3ad4dfbc1bdf407df2bae7e52fa` |
| xref 4 record `+0xF8` | `0x006D99E0..0x006D9C22` | `0x002D8DE0..0x002D9022` | `d4d55c03fad92f1d7a839b31bc9a9f7ece46f8591b0039e8f342d3a7cd9926b3` |
| xref 5 record `+0xF8` | `0x006F2890..0x006F2C5D` | `0x002F1C90..0x002F205D` | `c8a2f52d7c45973bc3d5dea91eeac446035c3aca406894981eb6e3ed5353d7cd` |
| xref 6 `STALL_SET.s_STALL_ITEM` | `0x00767780..0x00767899` | `0x00366B80..0x00366C99` | `a768fe6e1eeb88ba2fa10bba51e031638769ebe014288bcece5b7884a7a4b814` |
| xref 7 stall helper | `0x00767260..0x00767321` | `0x00366660..0x00366721` | `befb8e8d5530e0474561a00c9ad2ebf452f054ed5b5ec5957059f44818930268` |
| xref 7 consumer | `0x0076D790..0x0076D902` | `0x0036CB90..0x0036CD02` | `f5698eb490e348d11b2d1d75655efbf8868adfc334bd45e8e486203bfaf0d4d9` |
| descriptor constructor | `0x0045C220..0x0045C277` | `0x0005B620..0x0005B677` | `5224caaa125e0cc197b707c690dbf14fafe057434e34d07c572d00355bd88840` |
| descriptor vtable through xref-8 slot | `0x00F0DF3C..0x00F0DF54` | `0x00B0C33C..0x00B0C354` | `664c82cc86fda981661408007a3d523f83bbcc704b6689369d20093bcade0c90` |
| `NPCAttr` bind to `CNetNPC+0x358` | `0x004697B0..0x004697F2` | `0x00068BB0..0x00068BF2` | `be9bbd866c5eaebe5fed173106049710cd39abc9e4239e63a877087e433aba6a` |
| `NPCAttr+0x7C` to descriptor `+0x60` | `0x0045DAE0..0x0045DC34` | `0x0005CEE0..0x0005D034` | `e1c061b56e4cdd73c19916da302e6085de203bb841b85f48a25331d92c53516d` |
| xref 8 full-string `.avt` use | `0x0078AA50..0x0078AB15` | `0x00389E50..0x00389F15` | `506cf75564794c2159ed9f5b21d48421db6bd5ae31e6351863ed1a6a21663280` |

## Required searches and cross-checks

- ค้นชุดส่งมอบแล้ว: **เจอ** `NPCAttr` in `PF_PROTOCOL_REGISTRY.tsv`; the first-generation `PF_SERIALIZER_FIELDS.tsv` only contains its obsolete empty copier, while the active semantic artifacts already pin the later exact `NPCAttr+0x7C` wstring codec and the `0x0045DAE0` consumer. The decisive consumer spans were re-derived from the image, and every reused span hash matched.
- ค้น gamedata แล้ว: **เจอ** `MOBS.s_OUTFIT` in `PF_GAMEDATA_COLUMNS.tsv` and `CONSTDATA_TH__MOBS.tsv`; **เจอ** `STALL_SET.s_STALL_ITEM` in `PF_GAMEDATA_COLUMNS.tsv` and `CONSTDATA_TH__STALL_SET.tsv`. These cross-check the two table-column literals reached by xrefs 3, 6, and 7; no meaning was inferred from string proximity alone.
- ค้น server tree แล้ว: **เจอ** the open RE-321 caveat in `mob_avatar_basename.py` and generated `field_mob_tables_bg0002.py`. Current behavior already emits one basename and refuses list cells, so this result supports the behavior and closes the caveat; it does not require a behavior reversal.

## Reproduction and trap test

- Stdlib-only guard: `pf_bridge/staged/re321_avt_guard.py`, SHA-256 `3be1cd44b71ec8e788d805ded1f6f21871afc99759e47219473a12bed176a0e2`.
- Disassembly walker used for the source walk: `pf_bridge/staged/re321_avt_xrefs.py`, SHA-256 `1452db7d72bf6887208974214c014f3f349bd9da5c8ee1e79b490f2a46fd378f`.
- Command: `py -3 pf_bridge\staged\re321_avt_guard.py GameClient\GameClient.local.bin --trap-test` (run from the Pirate Force root, or pass absolute paths).
- Result: image SHA guard PASS; exact format-xref census 13 PASS; remaining-xref census 8 PASS; all 14 proof spans PASS; trap mutation was rejected with `span changed: xref8_descriptor_whole_string`.

## Build consequence

The existing single-basename wire rule is now backed by the actual `NPCAttr+0x7C` consumer: a raw multi-value cell must be reduced before it is written to this field. The client does not split `;`, tab, or space on the `.avt` route.

BUILD_PROPOSED: replace the RE-321-open wording in `mob_avatar_basename.py` and generated roster provenance with this static proof while retaining the existing single-basename wire guard | LANE-B (COMBAT) | `py -3 -m pytest tests/test_mob_avatar_basename.py -q`

## nonclaims

1. This does not prove which basename a server should select from a multi-value `s_OUTFIT` cell; it proves only that `NPCAttr+0x7C` must already contain the one complete basename the client will use. RE-296 separately proves index 0 for the client's own `MOBS.s_OUTFIT` table path.
2. This does not claim the internal `+0x28` or `+0xF8` fields belong to `NPCAttr`; their concrete classes remain unnamed here.
3. This does not claim every `.avt` path in the image comes from `NPCAttr`; seven of these eight do not.
4. The underscore split in `0x0045DAE0` feeds `CNetNPC+0x338`; it is not evidence that the `.avt` basename is underscore token 0.
5. This is static IMAGE evidence only. It does not prove that any particular basename exists on disk, renders a body, or matches a server-side gameplay choice.
