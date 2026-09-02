ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย

ถึง chief / LANE-A / Panya

# RE-169 RESULT — DONE / PASS: `OpenCloseUI` มีเส้นทางปิด NPC dialogue จริง แต่ numeric wire opcode ยังไม่ยืนยัน

- Ticket: `RE-169 NPC-DIALOGUE-CLOSE-OPCODE-001`
- Ticket START: `2026-09-03T01:53:12.598+07:00`
- Ticket block: UTF-8 5,835 bytes; SHA-256 `abd9f74d9f176deb8efd1aef6e663f5e5337a9fcdb79a0475712ae39d0a1fc0f`
- Method: static/read-only only; ไม่เปิดเกม/server, ไม่จับ `LOCK_GAME`, ไม่แตะ canonical DB, source, queue, external, gamedata หรือ git

## Direct answer

**มีคำตอบแบบ bounded-positive.** `OpenCloseUI` เป็น protocol class ของเกมจริงและ handler มีแขนงปิด UI จริง:

- สตริงแรกที่ object `+0x14` คือ **UI target name**
- byte ที่ `+0x30` เป็น **open/close selector**: nonzero ไปเส้นเปิด; zero ไปเส้นปิด
- เส้นปิด lookup UI ด้วยชื่อ `+0x14` แล้วเรียก virtual slot `+0x20C` ของ UI object; ค่า `+0x34/+0x38/+0x58` ไม่ถูกใช้ในแขนงปิด
- `NPCConversation` ผูกหน้าต่างบทสนทนาเข้า UI manager เดียวกันด้วยชื่อ exact `Quest_NPC_Conversation_New` หรือ `Quest_NPC_Conversation` ตามผล feature predicate

ดังนั้น body-level close request ที่พิสูจน์จาก image คือ `OpenCloseUI` ที่ใส่ UI-name เป็นหนึ่งในสองค่านี้, ตั้ง `+0x30=0`, และให้ฟิลด์ที่เหลือเป็น empty/zero. นี่เป็น named-field crosswalk ผ่าน UI manager เดียวกัน ไม่ใช่การจับคู่เพราะ ID เท่ากัน

**ข้อจำกัดที่ยังเหลือ:** numeric wire opcode ของ `OpenCloseUI` ยังไม่ได้จาก static image. Getter `0x005E4750` อ่าน word จาก global `0x01082034`; initializer `0x00BEE620` เรียก name registry แล้วเก็บ AX ที่ runtime. Capture corpus ยังเป็น `NOT_OBSERVED` ทั้ง W/R จึงยังห้ามเดาตัวเลข opcode หรือต่อ production call site ด้วยเลขที่ยังไม่วัด

## `OpenCloseUI` evidence

Client image: `GameClient.local.bin`, 14,759,424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

Protocol identity from `PF_PROTOCOL_REGISTRY.tsv:54`: name `OpenCloseUI`, registration `0x00BEE620`, ID global `0x01082034`, getter `0x005E4750`, vtable `0x00F30080`, serializer `0x005E5E90`, handler `0x005F02C0`.

Measured spans:

- vtable `[0x00F30080,0x00F300A0)`, final slots serializer/handler `0x005E5E90/0x005F02C0`; SHA-256 `c7b347684fabad8b5adf618348bae935871c7e1e84a2f6f798295d11f88fc68b`
- serializer `[0x005E5E90,0x005E5F2D)`, 157 bytes; SHA-256 `358ac52152c4a60e834c6f6cb249e5a729430ab28c3e1a94feea3de67421862b`
- complete handler `[0x005F02C0,0x005F040F)`, 335 bytes; SHA-256 `aac5d47e777dc7c7f3327ee1ced384222260366079852b79dc3f4b57cc4e1d62`
- false/close branch `[0x005F039D,0x005F03D1)`, 52 bytes; SHA-256 `ea7281095ba2af290bbf88fedd75674f936e825397409492c74318c789c2842e`
- bounded close helper CFG `[0x005BEE70,0x005BEF50)`, 224 bytes, two terminal returns; SHA-256 `8069b4d60150c55be37bc0a0770323385554e58412f9e689dfae79c6ea16287f`
- ID getter `[0x005E4750,0x005E4757)` SHA-256 `9e27e40ec810475c5f39c6ce31f07dcd0d40310a939d8c764549f1c2559b3cf7`; runtime registration `[0x00BEE620,0x00BEE638)` SHA-256 `38f1957dd5fefd4d346dce2f56b8ebe8732a84ddf583989f86dc48c20c65074d`

Handler facts:

- `0x005F02FA` takes the first string from object `+0x14`.
- `0x005F030B` compares byte `[object+0x30]` with zero. The constructor writes default `1` at `0x005E470C`, so a close request must explicitly carry zero.
- Nonzero enters the open path and consumes the other argument fields. Zero jumps to `0x005F039D`, constructs the close-operation object from the first UI-name only, and calls `0x005BEE70`.
- The close helper rejects an empty name, looks up the UI object by that exact name through `0x00A9EF00`, then calls the target object's virtual slot `+0x20C`. The optional secondary string branch is not populated by `OpenCloseUI`'s close path.
- The outer protocol handler always returns `AL=1`; therefore this is dispatch acceptance, not a close acknowledgement. If the named UI is absent, the inner helper can fail without producing a network-visible error.

Serializer/body order from `PF_SERIALIZER_FIELDS.tsv:865-874`:

| order | object field | measured wire form | close-path role |
|---:|---|---|---|
| 1 | `+0x14` | `UNTAGGED_STRING8_LEN32LE` | exact UI target name |
| 2 | `+0x30` | tag `0x05`, 1 byte | zero selects close |
| 3 | `+0x34` | tag `0x14`, 4 bytes | serialized but ignored by close branch |
| 4 | `+0x38` | `UNTAGGED_STRING8_LEN32LE` | serialized; empty in close operation |
| 5 | `+0x58` | tag `0x32`, 8 bytes | serialized but ignored by close branch |

Tag names above preserve the corpus notation; no additional numeric semantics are inferred from width alone.

## NPC-dialogue target crosswalk

`NPCConversation` is independently bound in `PF_PROTOCOL_REGISTRY.tsv:111` to vtable `0x00F3404C`, serializer `0x00622F10`, and handler `0x00623090`.

- NPCConversation vtable `[0x00F3404C,0x00F3406C)` SHA-256 `bdc15a3e0e6351b32e9a251096b64b01d4d292852efcf05155d815cc7bab7e32`
- complete handler `[0x00623090,0x006230E2)`, 82 bytes; SHA-256 `d9f7fda8c6c686daa677259d5fd0d653c0500ec0b14278840d99919e170a45a7`
- NPCConversation-success branch in the Quest dispatcher `[0x0061A99D,0x0061AA88)`, 235 bytes; SHA-256 `09cea49ca864234ce4845edfd86e64a4bcb4144e291862945427538a08095099`

The NPCConversation handler resolves `QuestModule`, checks the message through the class-specific slot, and forwards it to the Quest dispatcher. On that exact successful branch the client selects one of these UI-manager keys:

- UTF-16 literal `Quest_NPC_Conversation_New` at `0x00F25580`, including terminator SHA-256 `dec8c04a69476255f32e6c649b9139aa0eda07d4de805b3417419c1c70e419eb`
- UTF-16 literal `Quest_NPC_Conversation` at `0x00F25600`, including terminator SHA-256 `989e83416135edaa0657d9a5b8870e72b874e7690cf312cb83fc83cc6ecead5b`

It then resolves the selected key through the same UI-manager family and invokes `InitQuestList`. This is the missing named-field bridge from `OpenCloseUI.+0x14` to the NPC dialogue window. Static alone does not say which old/new variant is active in a particular live session because that choice follows a runtime feature predicate.

## `WindowClose*` disposition

The three RTTI names are **not game protocol candidates** in the measured image/corpus:

- `PF_RUNTIME_CLASSMAP.tsv:412,649,655,3534,3771,3777` marks every occurrence `TYPE_DESCRIPTOR_UNBOUND`, class/vtable `UNKNOWN`, source `DUMP`, namespace `UIAutomationCoreProto`, repeated in two crash dumps.
- Exact ASCII and UTF-16 searches found zero occurrences of `WindowClosedPayloadMsg`, `WindowCloseResponseMsg`, `WindowCloseRequestMsg`, and `UIAutomationCoreProto` in all three current executable inputs: `GameClient.local.bin`, `GameClient.bin`, and `dbghelp.dll`.
- The same three names have zero rows in `PF_PROTOCOL_REGISTRY.tsv`, `PF_PROTOCOL_PRIORITY.tsv`, `PF_FIELD_VALIDATION.tsv`, and `PF_SERIALIZER_FIELDS.tsv`.
- Their dump type-info vtable VA `0x64432074` is shared with a large contiguous family of WinRT/protobuf/UI-automation RTTI records. The bounded conclusion is that these are dump-layer Windows UI Automation artifacts with no captured binding into the game's protocol registry; they cannot supply a game opcode/vtable/handler.

This does not claim the Windows component's own code is dead. It claims only that the current game image and RE deliverable contain no game-network binding for these names.

## Mandatory searches

- **Searched `pf_bridge\external\`:** full-tree scope 2,683 files / 930,201,065 bytes; one-pass inventory fingerprint `705e543ae456fc6fbadeb7dd5b71d0b81507f3d903fb8c0d6bf1c3492447cf84`. Terms included `OpenCloseUI|NPCConversation|WindowClosedPayloadMsg|WindowCloseResponseMsg|WindowCloseRequestMsg|UIAutomationCoreProto|Quest_NPC_Conversation`. Relevant hits were the four protocol/runtime tables above; `OpenCloseUI` remains `NOT_OBSERVED` for both W/R in `PF_FIELD_VALIDATION.tsv:106-107`.
- **Searched `pf_bridge\gamedata\`:** full-tree scope 1,109 files / 15,319,585 bytes; one-pass inventory fingerprint `78a7de73997957acbf94592f4146e8a4172cf2a111f25791d0343ad3340d0962`. The same term family produced zero hits; no independent table/Lua/scene crosswalk or opcode value exists there.

Pinned input files:

- `PF_PROTOCOL_REGISTRY.tsv` SHA-256 `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_RUNTIME_CLASSMAP.tsv` SHA-256 `c53a6eaf23911765ebabd5e86ccaecf827ffdd88a1f514fc3f0f3ea2c3484985`
- `PF_SERIALIZER_FIELDS.tsv` SHA-256 `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- `PF_FIELD_VALIDATION.tsv` SHA-256 `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- Queue SHA-256 `86d51b29d932cdb1d51d2fccaa9dd9f31ddaf1390b6f31050fc4c10454e42177`
- Correction note `20260902_1027_KA1B-CORRECTION-re136-was-already-answered-and-i-broke-the-lint-tool.md` SHA-256 `3cb7816f945b14bdd734da4bad5bc5db73d938c5576c5d422fa736f93d7b6a42`; it correctly warns that RE-169 must not be treated as closed merely from the inline heading.

## Evidence-layer separation

- **Client static:** proves `OpenCloseUI` close semantics and the two exact NPC-dialogue UI keys. This closes the bridge/image jobs.
- **Wire/capture:** proves only `NOT_OBSERVED`; numeric opcode and an original-server frame remain unconfirmed.
- **Client-observable:** not tested in this round; no game was opened.
- **DB:** not inspected or touched.

## Nonclaims

1. This does not claim a numeric opcode value; the ID is runtime-registered and capture has no observation.
2. This does not claim the original server ever emitted `OpenCloseUI` for NPC dialogue.
3. This does not claim which of the legacy/new UI keys is active in a given live session.
4. This does not claim handler return `AL=1` proves the window visibly closed; the target may be absent and no attended test was run.
5. This does not promote `WindowClose*` dump RTTI into game-network evidence, nor claim the Windows component itself is dead.
6. This does not infer any field relationship from equal numeric IDs; the bridge uses class vtables, exact field consumers, and shared UI-manager keys.

## BUILD_IMPACT

`BUILD_IMPACT: The missing client-side mechanism is now characterized: OpenCloseUI + UI-name Quest_NPC_Conversation[_New] + selector byte 0 is the close path. Do not patch runtime.py with a guessed numeric opcode yet. The remaining unblock is a capture/attended observation that resolves OpenCloseUI's runtime uint16 ID and identifies the active old/new UI key; after that, the serializer order above is sufficient to build the frame. WindowClose* must be removed from the game-protocol candidate list. No source/build change was made by the RE runner.`
