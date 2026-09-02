ถึง chief / LANE-A / Panya

# RE-210 RESULT — DONE / PASS: client does not wait for COnLandVital or TargetPosVital response before exit

- Ticket: `RE-210 EXIT-BUTTON-ONLAND-RESPONSE-EXPECTATION-001 [STATIC-ON-BRIDGE]`
- Ticket START: `2026-09-02T14:54:12.497+07:00`
- Ticket block: UTF-8 5,651 bytes; SHA-256 `df98df71ccadcada996c222f1f517a46733ba19d10fb76c0918f611824e70e94`
- Method: static/read-only only; did not open game/server, touch `LOCK_GAME`, canonical DB, source, queue, external, gamedata, or git.

## Direct answer

**No.** In the measured client image, neither `TargetPosVital` nor `COnLandVital` has a response-side state transition that can release an exit wait. Both classes bind their inbound-handler vtable slot to the same exact no-op handler at `0x00710440`, whose complete body is `mov al,1; ret 4`. It accepts the dispatch and returns without reading the message object, writing a field/flag, calling another routine, or scheduling a continuation.

Therefore there is **no response field/flag to name** for either companion vital. The static result is not based on equal numeric IDs: class identity, ID getter, serializer, vtable, and handler are independently cross-walked in the protocol registry and pinned to the image.

## Evidence and provenance

Client image: `GameClient.local.bin`, 14,759,424 bytes, SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

Protocol crosswalk from `external/PF_PROTOCOL_REGISTRY.tsv`:

- `TargetPosVital`: ID global `0x01081FE0`, getter `0x005E50A0`, vtable `0x00F30230`, serializer `0x005E50E0`, handler `0x00710440`.
- `COnLandVital`: ID global `0x010820A8`, getter `0x005E6EA0`, vtable `0x00F30548`, serializer `0x005E6EB0`, handler `0x00710440`.
- Contrast only: `LogoutVital` has its own handler `0x005EF930`; it is not routed to the no-op handler.

Measured spans:

- Shared inbound handler `[0x00710440,0x00710445)`: bytes `B0 01 C2 04 00`; SHA-256 `f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863`.
- `TargetPosVital` vtable `[0x00F30230,0x00F30250)`: final slot `0x00710440`; SHA-256 `359909f9070ba1f4a88560648668b2e299c40c08439ba15cd7ddaa99a97db467`.
- `COnLandVital` vtable `[0x00F30548,0x00F30568)`: final slot `0x00710440`; SHA-256 `65065d883f6b9fa0794b0c2f901b1861d4e1d26917d91159af0f3a8d831230b8`.
- `TargetPosVital` ID getter `[0x005E50A0,0x005E50A7)` SHA-256 `7d33d07e3e693368c74cd209deea9396a2ecc3e88dcaade5e8a2bad0e473ba76`; its ID-global initializer `[0x00BEE392,0x00BEE398)` SHA-256 `78a9277cd32547666a9a64d994e45ea91e7d1eaf168e2a6d022a3b0d7058e9a7`.
- `COnLandVital` ID getter `[0x005E6EA0,0x005E6EA7)` SHA-256 `dbe74f22966e162bade1405c47de704046efbefaca945e101ab34d3d9efa525c`; its ID-global initializer `[0x00BEE9D2,0x00BEE9D8)` SHA-256 `331a04d9c2f14801cac60f09384dda0437d10a2e4cc432db79d6d5efb9d2620b`.

Bounded absolute-reference census over the image found exactly two raw references to each companion ID global: its getter and its registration-time initializer. No separate response-state flag or consumer is attached to either ID global. This census is supporting evidence; the decisive positive evidence is the complete no-op inbound handler.

For contrast, `LogoutVital` vtable `[0x00F304B8,0x00F304D8)` points to handler `0x005EF930`, SHA-256 `2fe10d7b6bd111dc631eecafe99a94d254ca49f97aed23dc34e3855281e0e990`. The complete short handler span `[0x005EF930,0x005EF94D)` reads response-object fields `+0x14/+0x18/+0x1C` and calls client routines before returning; SHA-256 `bcf5b7fa4046e32146361aafd7620b01b6ee88a714eaaa2cecf6a2de10400888`. This is a real response path and materially differs from the two companion-vital no-ops.

RE-189 result was re-verified at SHA-256 `eaa4fb0ba2c61f0664c0ba0e6d3b62da0d2a14b470d005086a3919b7f3830701`: within its complete bounded `SystemSetting_LogoutConfirm` class graph, `[object+0x18]` is populated by local UI binding to `BUTTON_CANCEL`, not by an inbound network response. This independently rules out treating that known gate as an acknowledgement bit for either companion vital.

RE-197 result was re-verified at SHA-256 `d946b231f7773dca0d7bd85fb10744f6eeb73ac501f54d4b98cca7de0c1ca875`: observed TargetPos bundles are position/movement traffic and carry no button field/subcode. This is wire/capture context only; it is not used to prove the client-side no-wait conclusion.

## Mandatory searches

- **Searched `pf_bridge\external\`:** full-tree inventory 2,683 files / 930,201,065 bytes; metadata fingerprint SHA-256 `6177ba3220e97616ec8b560900b449f61e14963c0e0765527f6de4ca1ed5fad4`. Search scope included `COnLandVital|TargetPosVital|LogoutVital|ON_LAND_VITAL|0x1EB4|1EB4|exit game|logout.*wait|wait.*logout|on.land`. Relevant hits were the protocol registry, field-validation tables, protocol catalogs, and prior RE artifacts. They identify serializers/handlers and show inbound-read counts of zero for TargetPos/COnLand in the measured validation corpus; no wait flag/ack state was found.
- **Searched `pf_bridge\gamedata\`:** full-tree inventory 1,109 files / 15,319,585 bytes; metadata fingerprint SHA-256 `e6ef0efd2f321fba41e1e967facd24fc790106faf87fa73404431889ddc6cb4a`. Same term family produced only unrelated numeric/text substring collisions such as placement value `0x1EB4` and `Landmine`; no class, protocol crosswalk, exit-wait flag, or response expectation was found.

## Evidence-layer separation

- **Client static:** the two companion-vital inbound handlers are complete no-ops; this supplies the answer.
- **Wire/capture:** prior TargetPos bundle observations describe traffic shape only and do not prove UI behavior.
- **Client-observable:** not tested in this round; no game was opened.
- **DB:** not inspected or touched.

## Nonclaims

1. This does not claim the server may omit parsing or processing the client's outbound `COnLandVital` / `TargetPosVital`; it answers only whether the client blocks exit awaiting a response to them.
2. This does not claim all exit mechanisms, OS shutdown paths, disconnect handling, or UI timing are wait-free.
3. This does not elevate wire ordering into client-observable behavior.
4. The absolute-reference census does not exclude every conceivable pointer alias in the whole program; the complete inbound handler itself establishes that these response dispatches perform no acknowledgement write.
5. No original-server semantic claim is made.

## BUILD_IMPACT

`BUILD_IMPACT: LANE-A should not add COnLandVital or TargetPosVital response frames as an exit-unblock fix. They have no client response-side state transition. Keep investigation/fixes on LogoutVital's actual response path, local logout-confirm UI lifecycle, socket closure, or another independently proven trigger. No source/build change was made by the RE runner.`
