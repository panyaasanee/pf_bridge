# PF field validation

ผลนี้เป็น `source=CAPTURE` แยกจากตาราง A2 `source=IMAGE` และไม่ส่งออก payload, ค่า field หรือ hexdump แม้แต่ไบต์เดียว

## Coverage

- capture files hashed/scanned: 1772 (595134426 bytes)
- text files inspected for PC blocks: 918
- files containing blocks: 277
- PC blocks: 10462; DECOMPRESSED blocks: 41432; total: 51894
- capture block/envelope errors: 0
- outer message instances: 51894
- nested instances declared by collection counts: 13220
- nested instances reached without heuristic scanning: 12785
- nested instances after a static-open boundary and therefore deliberately not guessed: 435

## A2 comparison

- parse success: 11904 message instances
- A2 static-open (not counted as mismatch): 52775 message instances
- mismatch: 0 instances, 0 distinct message/direction/field/reason point(s)
- nested frames with at least one successful validation: 11427
- nested frames reaching a static-open message: 881
- nested frames with a field mismatch: 0

## Framing kept separate from A2 fields

- collection ended with no extra tail: 1939 frame(s)
- `GSCN_RunTimeProtocolRes` collection ended with its exact zero derived change-mask: 9481 frame(s)
- other outer framing left unresolved: 0 frame(s)
- The runtime-response change-mask follows the complete VitalData collection. It is not assigned to the last nested message and therefore cannot create a false A2 mismatch.

## Observed messages

| message | dir | frames | instances | pass | static-open | mismatch |
|---|:---:|---:|---:|---:|---:|---:|
| `ActionVital` | R | 15 | 15 | 15 | 0 | 0 |
| `ActionVital` | W | 45 | 57 | 57 | 0 | 0 |
| `CBlockPointHelpVital` | W | 1 | 1 | 1 | 0 | 0 |
| `CHitParadeReqVital_JP` | W | 1 | 1 | 1 | 0 | 0 |
| `CHitResult` | R | 38 | 38 | 0 | 38 | 0 |
| `COnLandVital` | W | 155 | 375 | 375 | 0 | 0 |
| `CTracePathReqVital` | W | 1 | 1 | 1 | 0 | 0 |
| `Channel_ActorBoardcastMessageVital` | R | 1 | 1 | 1 | 0 | 0 |
| `Channel_GMGlobalMessageVital` | R | 1 | 1 | 1 | 0 | 0 |
| `Channel_GuildMessageVital` | R | 1 | 1 | 1 | 0 | 0 |
| `Channel_LocalTalkMessageVital` | R | 6 | 6 | 6 | 0 | 0 |
| `Channel_LocalTalkMessageVital` | W | 46 | 46 | 46 | 0 | 0 |
| `Channel_PartyMessageVital` | R | 1 | 1 | 1 | 0 | 0 |
| `CheckSecondPwdVital` | R | 9166 | 9166 | 9166 | 0 | 0 |
| `CheckSecondPwdVital` | W | 3 | 3 | 3 | 0 | 0 |
| `ChooseNPC` | W | 49 | 65 | 65 | 0 | 0 |
| `CreateActorVital` | R | 2 | 2 | 0 | 2 | 0 |
| `CreateActorVital` | W | 2 | 2 | 0 | 2 | 0 |
| `DeleteActorVital` | R | 3 | 3 | 3 | 0 | 0 |
| `DeleteActorVital` | W | 3 | 3 | 3 | 0 | 0 |
| `GSCN_LoginProtocol` | R | 389 | 389 | 0 | 389 | 0 |
| `GSCN_LoginProtocol` | W | 413 | 413 | 0 | 413 | 0 |
| `GSCN_RunTimeProtocolReq` | W | 40747 | 40747 | 0 | 40747 | 0 |
| `GSCN_RunTimeProtocolRes` | R | 10073 | 10073 | 0 | 10073 | 0 |
| `GetWorldInfoVital` | R | 1 | 1 | 0 | 1 | 0 |
| `GetWorldInfoVital` | W | 15 | 15 | 0 | 15 | 0 |
| `ItemOperateVitalReq` | W | 27 | 28 | 28 | 0 | 0 |
| `ItemOperateVitalRes` | R | 5 | 5 | 0 | 5 | 0 |
| `LSCN_LoginVitalReq` | W | 142 | 142 | 142 | 0 | 0 |
| `LSCN_Protocol` | W | 272 | 272 | 0 | 272 | 0 |
| `LSCN_SelectServerReq` | W | 130 | 130 | 130 | 0 | 0 |
| `LoginVerifyVital` | R | 135 | 135 | 135 | 0 | 0 |
| `LoginVerifyVital` | W | 135 | 135 | 135 | 0 | 0 |
| `LogoutVital` | R | 10 | 10 | 10 | 0 | 0 |
| `LogoutVital` | W | 19 | 19 | 19 | 0 | 0 |
| `MiscNotifyVital` | W | 2 | 2 | 2 | 0 | 0 |
| `MusicControlVital` | R | 125 | 125 | 125 | 0 | 0 |
| `NPCConversation` | R | 17 | 17 | 0 | 17 | 0 |
| `NotifyEnterCreateActor` | W | 143 | 143 | 143 | 0 | 0 |
| `QuestOperateVital` | R | 19 | 19 | 19 | 0 | 0 |
| `QuestOperateVital` | W | 19 | 19 | 19 | 0 | 0 |
| `ReturnSelectServerVital` | W | 2 | 2 | 2 | 0 | 0 |
| `SelectActorVital` | R | 135 | 135 | 0 | 135 | 0 |
| `ShowMessageVital` | R | 125 | 125 | 125 | 0 | 0 |
| `StartGameReq` | W | 128 | 128 | 128 | 0 | 0 |
| `StartGameRes` | R | 126 | 126 | 0 | 126 | 0 |
| `TargetPosVital` | W | 912 | 912 | 912 | 0 | 0 |
| `TargetVital` | W | 65 | 65 | 65 | 0 | 0 |
| `TeleportCheckVital` | R | 9 | 9 | 9 | 0 | 0 |
| `TeleportCheckVital` | W | 8 | 8 | 8 | 0 | 0 |
| `TeleportVital` | R | 132 | 132 | 0 | 132 | 0 |
| `TeleportVital` | W | 132 | 132 | 0 | 132 | 0 |
| `TradeCmdVital` | W | 8 | 8 | 0 | 8 | 0 |
| `TradeItemResultVital` | R | 1 | 1 | 0 | 1 | 0 |
| `TradeZoomVital` | R | 1 | 1 | 0 | 1 | 0 |
| `TriggerVital` | W | 2 | 2 | 2 | 0 | 0 |
| `UpdateAttrVital` | R | 69 | 69 | 0 | 69 | 0 |
| `UserSetting_UpdateServerSettingVital` | W | 197 | 197 | 0 | 197 | 0 |

## Evidence bindings

- PF_INPUT_INVENTORY.tsv SHA-256: `729b5e73383de8fd6e0008875d4b9b685de2ad8d72a55118aa862093f10259d1`
- PF_PROTOCOL_REGISTRY.tsv SHA-256: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- PF_SERIALIZER_FIELDS.tsv SHA-256: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- PF_TAG_CENSUS.tsv SHA-256: `63bc9a039b5b35e5b2e1f08ce99e91b05da6e6959b5b4f173eac66b88aea337a`
- Direction mapping: `DECOMPRESSED` = client serializer W; `PC` = client serializer R.
- Message IDs are resolved with the collision-free 16-bit registry-name algorithm over the frozen 519-name census; no proximity/string guess is used.
- `UNTAGGED_*_LEN32LE` A2 rows are validated through their stream primitive tags (`0x44` string8, `0x48` wstring16) plus uint32 byte length, without exporting the length or contents.
