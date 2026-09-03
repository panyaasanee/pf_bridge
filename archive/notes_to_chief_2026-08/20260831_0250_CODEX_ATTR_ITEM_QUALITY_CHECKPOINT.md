# CODEX Attr ItemAttr quality checkpoint

- Scope: read-only IMAGE + DATA analysis; each layer is a separate result row.
- Pinned IMAGE SHA-256 stayed `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
- ItemAttr `+0x38` is now `PROVEN_EXACT` as the XML `quai` item-quality tier.
- Exact IMAGE path: `quai` parser -> bounded setter (0..10) -> ItemAttr `+0x38` -> `Label_ItemName` style selector.
- Exact IMAGE selector for values 1..5: FontStyle IDs 15,16,17,18,19.
- Separate DATA rows pin the five declarations in `GameClient/Data/GUI/Model/BigFontStyle.fsl`, SHA-256 `77798599c203d36e11282633d4a91ac098b0e1e03aa2482fede6fcfca161fc10`.
- Both ItemAttr schemas and W/R remain separate: four field rows promoted plus four DATA delta rows.
- Attr semantic-delta rows: 58; unresolved rows: 144; frozen conflict census remains 616.
- Frozen A1-A6 artifacts were not edited. No server/client/runtime/test/lease/Git action was taken.
