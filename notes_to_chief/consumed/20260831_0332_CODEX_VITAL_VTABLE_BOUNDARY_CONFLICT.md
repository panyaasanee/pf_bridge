# CODEX VITAL VTABLE BOUNDARY CONFLICT - 2026-08-31 03:32 +07:00

Immediate correction notice for the active Attr census. Read-only IMAGE review found that two rows in the 03:22 remaining-codec checkpoint cross a concrete vtable boundary.

- `UpdateAttrVital` vtable starts at `0x00F303E0`. Its paired wire codec is the actual entry at `+0x18 = 0x005E42C0`. A second vtable starts at `0x00F30408`; therefore the dword at nominal first-table `+0x34 = 0x005E5F70` is the getter of the adjacent table, not a slot of UpdateAttrVital.
- `Express_ClientGetExpressItemAttrsVital` vtable starts at `0x00F40CBC`. Its paired wire codec is the actual entry at `+0x18 = 0x006E8920`. A second vtable starts at `0x00F40CE4`; therefore nominal first-table `+0x34 = 0x006E5740` is the adjacent-table getter, not a slot of this Vital.
- Both concrete Vital tables are 9 dwords (`0x24` bytes) before the next table metadata/boundary. Treating every linked class as having a valid `+0x34` slot is invalid.
- The active `PF_ATTR_REMAINING_CODEC_CENSUS.tsv` classification/count from the 03:22 checkpoint must not be consumed until regenerated with table-length-aware slot logic.
- A broader adversarial boundary audit is in progress to determine whether any other rows have the same failure mode.

This is an IMAGE-to-IMAGE correction. No server/client/runtime/test/Git/lease action was performed. The prior checkpoint note is preserved rather than edited.
