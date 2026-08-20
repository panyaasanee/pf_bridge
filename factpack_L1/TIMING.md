# TIMING -- measured, not estimated

Measured with `time.perf_counter()` around each step of
`make_factpack_l1.py`, single run, on the session Linux sandbox
(2 CPU visible, Python 3.10.12). Image: 14759424 bytes, sha256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
Run finished 2026-08-20T00:10:08+0700.

| # | step | seconds | output |
|---|---|---|---|
| 1 | read_and_sha256 | 1.1 | 14759424 bytes sha256=9627211412ac60d5 |
| 2 | pe_parse_sections | 5.2 | 6 sections |
| 3 | pe_imports | 0.3 | 702 import entries, 26 dll descriptors |
| 4 | pe_exports | 0.1 | 1 export entries |
| 5 | strings_ascii | 9.0 | 97989 strings, 3885594 bytes |
| 6 | strings_utf16 | 4.8 | 6314 strings, 312457 bytes |
| 7 | blocks_256_sha256 | 5.6 | 57654 blocks, 4716891 bytes |
| 8 | entropy_and_census | 10.3 | whole-file entropy 5.3649 bits/byte |
| - | **TOTAL** | **36.4** | 8990236 bytes of pack |

Run-to-run variance: earlier runs of this same script on this same image
in this same sandbox finished end-to-end in 21.6 / 26.0 / 27.2 / 29.6 /
42.8 / 44.1 seconds; the table above is one more sample. The spread is sandbox CPU
contention and page-cache state, not input-dependent. Treat the figure as
'tens of seconds, under a minute', not as a constant. The dominant costs
are the two regex sweeps, the 57654 sha256 calls and the byte histograms,
all linear in file size. Data output is byte-identical across runs.

## Which steps must be re-verified, and why

Project rule in force: *never trust a "scanned the whole image" claim
coming from a linear disassembler.* This pack contains NO disassembly --
no instruction was decoded, no code flow was followed -- so that rule is
not violated here. It becomes live again the moment anyone feeds these
offsets into a linear sweep.

| step | needs recheck? | why |
|---|---|---|
| read_and_sha256 | NO | self-verifying: rehash the image and compare one number. |
| blocks_256_sha256 | NO | self-verifying by construction -- rehash any 256-byte window and compare to its row. Verified byte-identical across two runs. |
| strings_ascii / strings_utf16 | YES -- coverage only | the rows present are exact (a regex over raw bytes cannot hallucinate). What needs rechecking is the COVERAGE claim: this is a byte-class filter, not a text extractor. Thai/cp874 single-byte text and non-ASCII UTF-16 fall outside it, and compressed or encrypted blobs contribute nothing. Never argue 'the client has no such concept' from an absent string. |
| pe_sections | LOW | pure struct decode at fixed offsets, no heuristics. Recheck only if a second tool disagrees on the section count. |
| pe_imports / pe_exports | YES | these walk RVA chains, so they depend both on the RVA->file-offset mapping being right and on these being the tables the loader actually uses. A protected or self-modifying image can carry a decoy import table. Cross-check with a second parser (dumpbin /imports, pefile) before building on these rows. |
| va_hex column (all files) | YES -- spot-check | VA is COMPUTED (ImageBase + VirtualAddress + delta), not read from the file. Verify a few rows in a debugger before trusting a VA. A '-' means the byte is not mapped at all; it is not a zero. |
| entropy_and_census | LOW | histogram plus Shannon formula. The interpretation is the risky part, not the number. |

## Output sizes

| file | bytes | data rows |
|---|---|---|
| strings_ascii.tsv | 3885594 | 97989 |
| strings_utf16.tsv | 312457 | 6314 |
| pe_sections.tsv | 1223 | 6 |
| pe_imports.tsv | 73742 | 702 |
| pe_exports.tsv | 329 | 1 |
| blocks_256.tsv | 4716891 | 57654 |

## End-to-end

The table above is written *by* the last step, so that step cannot
appear inside it. Measured separately:

| 9 | write_manifest_and_timing | 1.3 | MANIFEST.md + TIMING.md |

**End-to-end wall clock for the whole run: 37.7 s.**

So: this extraction is a sub-minute job on a 2-CPU sandbox, not a
"order of minutes" job. Any schedule built on the minutes estimate was
guessing; these numbers are measured.
