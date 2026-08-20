# Pirate Force -- Layer-1 Fact Pack (client image)

Generated 2026-08-20T00:10:08+0700 by `make_factpack_l1.py` (Python 3.10.12, stdlib only, no third-party packages).
The generation timestamp above and in TIMING.md are the only
non-deterministic bytes in this pack; everything else is a pure
function of the image.

## What this is

The Pirate Force server was shut down years ago and was never published.
The only first-hand evidence that exists is the shipped game client.
This pack is a flat-text extraction of that client, made so the facts
outlive access to the binary itself.

## Source of truth

| field | value |
|---|---|
| image path (sandbox) | `/sessions/intelligent-adoring-lovelace/mnt/Pirate Force/GameClient/GameClient.local.bin` |
| file name | `GameClient.local.bin` |
| size (bytes) | 14759424 |
| sha256 | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| md5 | `dd89fd483e48fa3a2b6219bcc58c0395` |
| format | PE32 (32-bit) |
| machine | IMAGE_FILE_MACHINE_I386 (0x14C) |
| ImageBase | 0x00400000 |
| AddressOfEntryPoint (RVA) | 0x00783122 |
| entry point file offset | 0x00782522 |
| COFF TimeDateStamp | 1420722568 (0x54AE8188) = 2015-01-08 13:09:28 UTC |
| linker version | 9.0 |
| Subsystem | WINDOWS_GUI (2) |
| SizeOfImage | 0x00E87000 |
| SizeOfHeaders | 0x00000400 |
| sections | 6 |

Data directories present (non-zero):

| # | name | RVA | size |
|---|---|---|---|
| 0 | EXPORT | 0x00C19340 | 78 |
| 1 | IMPORT | 0x00C12DD8 | 540 |
| 2 | RESOURCE | 0x00C9C000 | 362904 |
| 5 | BASERELOC | 0x00CF5000 | 558372 |
| 6 | DEBUG | 0x00B090B0 | 28 |
| 10 | LOAD_CONFIG | 0x00BBC570 | 64 |
| 12 | IAT | 0x0083B000 | 2912 |
| 14 | COM_DESCRIPTOR | 0x00B95528 | 72 |

## Files in this pack

| file | bytes | lines | data rows |
|---|---|---|---|
| `strings_ascii.tsv` | 3885594 | 98000 | 97989 |
| `strings_utf16.tsv` | 312457 | 6320 | 6314 |
| `pe_sections.tsv` | 1223 | 11 | 6 |
| `pe_imports.tsv` | 73742 | 707 | 702 |
| `pe_exports.tsv` | 329 | 6 | 1 |
| `blocks_256.tsv` | 4716891 | 57663 | 57654 |
| `MANIFEST.md` | (this file) | - | - |
| `TIMING.md` | measured wall clock | - | - |
| `make_factpack_l1.py` | generator, rerunnable | - | - |

Total pack size: 8990236 bytes.

## Column semantics (read this before using any offset)

* `file_offset_hex` -- offset inside the .bin on disk. Use with a hex
  editor or `dd`.
* `va_hex` -- virtual address the loader maps that byte to,
  = ImageBase + section.VirtualAddress + (file_offset - PointerToRawData).
  Use with a disassembler/debugger. `-` means the byte is NOT mapped
  (it lives in file-alignment padding past VirtualSize, or in a gap).
* `virtual_address_rva_hex` in `pe_sections.tsv` is an RVA, not a VA;
  the `va_hex` column next to it is the absolute one.
* The two are NEVER interchangeable. A file offset pasted into a
  debugger points at unrelated code.

## What this pack can be used for

* Grepping for handler / table / opcode / field names without the image.
* Turning a string hit into a VA you can look up in a disassembler later.
* Byte-guard verification: `blocks_256.tsv` pins every 256-byte window
  by sha256, so a future claim "these bytes at offset X are unchanged"
  can be checked against this pack alone.
* Proving that a proposed server behaviour has (or has not) a matching
  literal in the client.

## What this pack CANNOT be used for (nonclaims)

* It is NOT a disassembly. No instruction was decoded. Nothing here
  says which code reads which string.
* A string being present proves the literal exists in the image. It does
  NOT prove it is reachable, used, or sent on the wire.
* `strings_utf16.tsv` only matches the ASCII subset of UTF-16LE. Thai
  and other non-ASCII wide text is absent from it.
* `strings_ascii.tsv` only matches bytes 0x20-0x7E, so any single-byte
  cp874/tis-620 Thai text would be missing from it. Measured: 61884 runs of
  >=4 bytes in the 0xA1-0xFB range exist, but 61621 of them (99.6%) are
  inside `.text`, i.e. x86 opcode bytes, not text. See the localization
  note below before reading anything into that number.
* Strings split across a non-printable byte are reported as two rows.
* TAB (0x09) is treated as non-printable because it is the TSV separator.
  Cross-check on this image: GNU `strings -a -n 4` reports 98704 runs,
  this file reports 97989. The delta is TAB handling, not missed regions.
* Import entries for WS2_32.dll are ordinal-only in this image. Mapping an
  ordinal to a winsock name requires ws2_32.dll's own export table, which
  is NOT part of this pack. Do not treat any ordinal->name guess as proven.
* Compressed or encrypted regions yield no readable strings, so absence
  of a string is NOT evidence the concept is absent from the client.
* Import/export tables are parsed statically. Anything resolved at
  runtime (GetProcAddress, packed thunks) does not appear.
* `blocks_256.tsv` proves identity of bytes, not meaning of bytes.

## Localization observation (measured, negative)

Direct probe for Thai text in the image, five of the most common Thai
words encoded in cp874/tis-620:

| probe | occurrences |
|---|---|
| `kaan` (A1 D2 C3) | 0 |
| `kem` (E0 A1 C1) | 0 |
| `mai` (E4 C1 E8) | 0 |
| `phuu` (BC D9 E9) | 0 |
| `thii` (B7 D5 E8) | 0 |
| UTF-16LE runs in U+0E01..U+0E5B, >=3 chars | 3 |

Every probe is zero or near-zero, and the high-byte runs counted above
sit almost entirely in `.text`. Conclusion supported by these bytes: the
executable itself carries essentially no Thai UI text -- localization
lives outside the image (the `Data\` tree). What this does NOT prove:
that no Thai exists anywhere in the client install, or that text is not
stored in some encoding this probe does not cover.

cp874-range runs (>=4 bytes) per section:

| section | runs |
|---|---|
| .text | 61621 |
| .code | 5 |
| .rdata | 250 |
| .data | 2 |
| .rsrc | 6 |
| .reloc | 0 |

## Packing / entropy observation

Whole-file Shannon entropy: 5.3649 bits/byte. Zero bytes: 37.70% of file.

| section | entropy (bits/byte) | raw size |
|---|---|---|
| .text | 6.6301 | 8621056 |
| .code | 5.0394 | 1024 |
| .rdata | 1.7903 | 4056064 |
| .data | 4.8838 | 73216 |
| .rsrc | 3.9712 | 363008 |
| .reloc | 3.1314 | 1644032 |

Reference points: 8.0 = incompressible (encrypted/compressed),
~6.0-6.8 = normal x86 code, <5.5 = plain data/text.

## Imports summary

702 import entries across 26 DLL descriptors:

* `ADVAPI32.dll`
* `COMCTL32.dll`
* `DINPUT8.dll`
* `GDI32.dll`
* `IMM32.dll`
* `KERNEL32.dll`
* `MSVCP90.dll`
* `MSVCR90.dll`
* `MSVFW32.dll`
* `OLEAUT32.dll`
* `RPCRT4.dll`
* `SHELL32.dll`
* `SHLWAPI.dll`
* `USER32.dll`
* `VCOMP90.DLL`
* `VERSION.dll`
* `WININET.dll`
* `WINMM.dll`
* `WS2_32.dll`
* `X3DAudio1_6.dll`
* `d3d9.dll`
* `d3dx9_41.dll`
* `gdiplus.dll`
* `mscoree.dll`
* `msvcm90.dll`
* `ole32.dll`

## Reproduce

```
python3 make_factpack_l1.py --image <path-to-GameClient.local.bin> --out .
```

The image is opened read-only. This script never writes to it.
