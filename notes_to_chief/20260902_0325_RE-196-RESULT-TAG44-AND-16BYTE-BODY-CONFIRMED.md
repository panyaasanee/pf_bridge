ถึง: chief — ผล RE-196 (static bridge)

# RE-196 RESULT — DONE / PASS: field 3 carries helper-emitted `0x44`; minimal body stays 16 bytes

- Ticket START: `2026-09-02T03:17:54.859+07:00`
- Result time: `2026-09-02T03:25+07:00`
- Queue input SHA-256: `2443e5d19563b7c8933238f6821f7b65f419a8073e13a9adb857524a5fb413ce`
- Mode: static/read-only only; no game/server boot, no `LOCK_GAME`, no canonical DB, no source/queue/external/gamedata edit.

## Mandatory searches

- ค้นใน `pf_bridge\external\` แล้ว: **เจอคำตอบตรง**ใน `PF_A2_STRING_WIRE_TAG_DELTA.tsv` และรายงาน `PF_A2_A3_STRING_WIRE_CORRECTION.md`; scope ที่ค้น = 2,683 files / 930,201,065 bytes ด้วย `ReturnSelectServerVital`, `DeleteActorVital`, `0x709E`, `0x005E6A2B`, `0x005E4E52`, และ `UNTAGGED_STRING8_LEN32LE`. ตาราง delta pin ทั้ง caller span และ common string-helper span พร้อม tag instruction. รัน generator แบบ read-only `--check` แล้ว PASS: 408/408 overlay rows, outputs byte-identical.
- ค้นใน `pf_bridge\gamedata\` แล้ว: **ไม่เจอ** identifier/address ข้างต้นใน 1,109 files / 15,319,585 bytes. ขอบเขตผลลบนี้หมายถึง extracted gamedata tree เท่านั้น; ไม่ใช่ผลลบของ client image/capture.

## Job 1 — ReturnSelectServerVital field 3: CLOSED / POSITIVE

Pinned image: `GameClient\GameClient.local.bin`, size 14,759,424, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

- Message serializer span VA `[0x005E69F0,0x005E6AE7)`, file `[0x001E5DF0,0x001E5EE7)`, SHA-256 `1fd3684282291e2accb94171f0d532e239d38f736e1cb1455a633e7ad567774a`.
- W caller at VA/file `0x005E6A2B / 0x001E5E2B` calls `0x0089A6D0` after loading object `+0x20`.
- R caller at VA/file `0x005E6A65 / 0x001E5E65` calls `0x0089A740` after loading object `+0x20`.
- There is no caller-local inline `push 0x44`. The tag is emitted/validated **inside the exact common helper called by this field**:
  - W helper VA `[0x0089A6D0,0x0089A733)`, file `[0x00499AD0,0x00499B33)`, SHA-256 `a0674fb3366720314e20ef5f5dbfa010330b12a73ed4e56e6c43e9d310dce9f1`; at VA/file `0x0089A6F1 / 0x00499AF1`, instruction bytes decode as `push 0x44`. The downstream routine loads that argument at `0x0089A537` and writes it to the stream at `0x0089A53B`.
  - R helper VA `[0x0089A740,0x0089A806)`, file `[0x00499B40,0x00499C06)`, SHA-256 `90c8c73b3b3c7158af57e374c694730763ab28292130b4f128a4754dec54e76a`; at VA/file `0x0089A75C / 0x00499B5C`, instruction decodes as `push 0x44`. The downstream routine loads the expected tag at `0x0089A5BB` and compares it with the stream byte at `0x0089A5BF`.

Conclusion: field 3 full-wire form is `44 <u32le byte_count> <N bytes>`, length `5+N`, even though the old A2 label stopped at helper payload scope and said `UNTAGGED_STRING8_LEN32LE`.

## Job 2 — DeleteActorVital field 4 control: CLOSED / SAME METHOD

- Message serializer span VA `[0x005E4E10,0x005E4EB4)`, file `[0x001E4210,0x001E42B4)`, SHA-256 `d844e2f98dd7e9b195224cab817e6142ec7c4ca14e2b779599473936dbf4ce9c`.
- W caller `0x005E4E52 / 0x001E4252` loads object `+0x1C` and calls the same W helper `0x0089A6D0`.
- R caller `0x005E4E85 / 0x001E4285` loads object `+0x1C` and calls the same R helper `0x0089A740`.

Thus the control case and ReturnSelect use the same tag-bearing helpers. This independently explains why DeleteActor had a real `0x44` despite the same old `UNTAGGED_*` label; matching message IDs were not used as a crosswalk.

## Job 3 — 16-byte versus 15-byte body: CLOSED / 16 BYTES

The all-zero minimal body is:

`08 00 | 32 00 00 00 00 00 00 00 00 | 44 00 00 00 00`

- Size: 16 bytes; body SHA-256 `ee43726ad11d050dfd1588db21a4f9a852de2aff6fe2aec7cae80801400a9b45`.
- `logout_hypothesis.py` SHA-256 `17d5e9280fd86cf6abc8780a0668998bbacd625574ea4dd9005b186c3b709b70` already contains exactly this body and size.
- `verify_logout_return_select_encoder.py` SHA-256 `c90a68cf2c12eadd18a96634f031688e4c93029bd93d92a94e3723a9b10b75d7` passed all 34 current guards. Its textual `UNCONFIRMED` qualifier is now stale, but its bytes/size are correct.

The 15-byte alternative is rejected because it omits the helper-emitted `0x44`.

## Job 4 — raw capture search: CLOSED / TWO REAL FRAMES EXIST

The premise “no raw capture exists” is false. Two independent client-to-server request captures each contain one byte-identical `0x709E` nested vital with the same 16-byte body:

1. `GameClient\capture_demo_fullloop_20260817_035212\capture_v141\GAME_20260817_035430_388049_52451.txt`, size 700,425, SHA-256 `2a43616bac2370cd68297ff533c9ef0c84498d1ea35e6d81957af81391efa3ab`, evidence lines 1011-1019.
2. `GameClient\capture_gt011_20260818_170121\capture_v141\GAME_20260818_170347_645157_52155.txt`, size 176,353, SHA-256 `b79b22f9c69519a7baf560470af2e2248985ed648c8d3a2c7c1bf81053d53ee3`, evidence lines 263-271.

Each decompressed 36-byte login-protocol PC has SHA-256 `55f01f38a90fa44797c315636faaa435938c628bcb22d966af25d362881490c2`; its nested body is the exact 16-byte value above. `PF_FIELD_VALIDATION.tsv` SHA-256 `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3` records `W observed=2 / parsed=2 / files=2 / VALIDATED` and `R observed=0 / NOT_OBSERVED`. This is wire evidence, not client-observable evidence.

## Input/output integrity

- `PF_SERIALIZER_FIELDS.tsv` SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`.
- `PF_A2_STRING_WIRE_TAG_DELTA.tsv` SHA-256 `e1f4f987c31f53d4dd87845aab01857c8415a8dbcd750af12df9c4cde208b3a2`.
- `PF_A2_A3_STRING_WIRE_CORRECTION.md` SHA-256 `182c350bec27c71fd76469953da1c5fcc848ea98804bc0080df42e89b44dbde9`.
- Generator SHA-256 `4b6d3660db23bcf9cbc363e22a53c76906d99833c6f530548b9d082c6bcd0303`; `--check` PASS and made no writes.
- `PF_INPUT_INVENTORY.tsv` SHA-256 `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1` points to both bridge-local capture inputs.
- All source/input SHAs were rechecked after analysis and matched the values above; only this result letter and the runner bookkeeping are written by this round.

## Nonclaims

- The captures are client -> server (`W`) requests inside `GSCN_LoginProtocol`; they do **not** prove a server -> client `0x709E` response is consumed, changes scene, or matches original-server policy.
- This result proves the field framing/tag, not nonzero field values or the semantic meaning of field 3.
- It does not promote any hypothesis to production. `production_allowed` remains `False`.
- No client-visible behavior was tested or claimed; the game was not opened.
- No generic ID-equality mapping or cross-message semantic inference was used.

## BUILD_IMPACT

`BUILD_IMPACT: keep RETURN_SELECT_SERVER_BODY and BODY_SIZE=16 unchanged; chief may remove the stale UNCONFIRMED wording for field3 and restamp the paired verifier/fixture comments, while preserving all direction/client-consumption/production nonclaims. No source patch was made by the RE runner.`
