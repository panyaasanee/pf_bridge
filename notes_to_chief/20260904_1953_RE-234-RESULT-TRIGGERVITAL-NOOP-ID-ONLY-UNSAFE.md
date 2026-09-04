To: LANE-A; CC: Chief

# RE-234 — TriggerVital response is a success no-op; id-only island classification is unsafe

- Status: **DONE / MIXED PASS + BOUNDED-NEGATIVE**
- Started: `2026-09-04T19:48:16.299+07:00`
- Method: static-only on bridge; no client/server boot and no live-game claim
- Ticket block SHA-256: `715b28483409de35e03ad4a07ad29741c35ba024c13ca3c79c91164206987552`
- Repro verifier: `pf_bridge/staged/re234_static_verify.py` — `PASS 18/18`, SHA-256 `e54989a69cfb6ff64d7ed993ee1d61cd27b0bf89fc0f64515ffe66dd97f3d292`

## Mandatory search pass

### `pf_bridge/external/`

Searched once across the full current tree (2,683 files, 930,201,065 bytes; manifest fingerprint `2374c325ff9d2b12567a1e388f8c90c1eba1b86dfc61e00180d11604b575cf20`) for `TriggerVital`, `0x1FB2`, its getter/serializer/handler addresses, `AddSurveyData`, survey/report-window paths, and prior RE/GT evidence.

Found:

- `PF_PROTOCOL_REGISTRY.tsv`: TriggerVital getter `0x006007A0`, id global `0x01082844`, serializer `0x006007C0`, natural handler `0x00710440`.
- `PF_SERIALIZER_FIELDS.tsv`: symmetric W/R codec descriptions for the TriggerVital payload.
- Earlier RE-227 static evidence pins the AddSurveyData-provision → local distance `<=500` → prompt/window path; its result SHA-256 is `dcdaa4e5261286d6a1128b9dfd93cc7145dc1ba609c05b7496c2f87ffbdfc80d`.
- GT-228 observed TriggerVital id 2 at Prison Exile and id 3 at Spice Paradise, but no response/window; the same id 3 also appeared during ordinary sailing. Result SHA-256 `91547a7063ef7d73c0bfa9e04c0fce952e431b4b4fe728bcccd9ed3b51ea6e29`.

Not found in this scoped pass: an explicit field-level crosswalk from TriggerVital payload `+0x14` to the gamedata `n_ID`, or another client consumer attached to the natural TriggerVital response handler.

### `pf_bridge/gamedata/`

Searched once across the full current tree (1,109 files, 15,319,585 bytes; manifest fingerprint `9bab763d8d8b70fae5843e725426406f2ff37f12a8cf90c16f5f0ea575700fd1`) for trigger tables, ids 2/3, island names, report/survey terms, and explicit crosswalk columns.

Found:

- `CONSTDATA_TH__Trigger.tsv` ids 2 and 3, both with `n_MESSAGE_TYPE=3`.
- `TEXTDATA_TH__Trigger_TIP.tsv` id 2 = `Edmund Hidden Treasure`, id 3 = `Seafood Cargo`.

Not found in this scoped pass: a foreign-key/crosswalk column connecting either table's `n_ID` to TriggerVital wire field `+0x14`, nor a gamedata declaration that ids 2/3 mean island ids 153/154.

## Q1 — What does the client do on a TriggerVital response?

The protocol family is **not proven one-way by absence of a decoder**: the registry has a natural handler and the codec table contains W and R branches. However, the actual natural handler at `0x00710440` is exactly five bytes:

`B0 01 C2 04 00` → return success (`AL=1`) and discard the one stack argument.

It does not read the decoded object, open UI, dispatch another client handler, or mutate visible state. Therefore a server TriggerVital response, if one is ever sent and routed normally, is accepted as a **success no-op** by this image.

Pinned image evidence:

- `GameClient.local.bin` SHA-256 `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- TriggerVital codec `[0x006007C0,0x0060082B)` / file `[0x001FFBC0,0x001FFC2B)`: SHA-256 `2f30bd87df466c5df7df89818704ab636c9b875f4b5c74c01b62553a92791a12`
- Natural handler `[0x00710440,0x00710445)` / file `[0x0030F840,0x0030F845)`: SHA-256 `f4c6d7ae520f88aecb3ea65952e885437fa4a6ce4b5c3439a161d1c5d8e42863`
- Field validation currently records TriggerVital W observations but no R observation; that is capture coverage, not proof the server never responds.

## Q2 — How many of the proposed paths open the captain-report prompt/window?

Of the **two routes named in this ticket**, exactly one is statically proven:

1. **AddSurveyData provision + local distance `<=500`: yes.** RE-227 pins the local proximity gate and subsequent prompt flow.
2. **TriggerVital response: no through its natural handler.** The handler is the success no-op above and has no window/UI consumer.

This also explains why GT-228 could observe island-contact TriggerVital sends without a prompt: that run had neither AddSurveyData provisioning nor a captured response. It does not establish server policy.

## Q3 — Are TriggerVital ids 2/3 the `TEXTDATA_TH__Trigger_TIP` namespace?

**BOUNDED-NEGATIVE: identity cannot be established from the available static sources.** Both sides have small integer ids, but equality of numeric values is not a crosswalk. The gamedata schemas have no wire-message or foreign-key field, and the client response handler never consumes the decoded id to provide a linkage.

The current hook is additionally unsafe as a semantic classifier:

```text
M2_OBSERVED_ISLAND_TRIGGER_IDS = {2: 153, 3: 154}
dock_trigger_id = M2_OBSERVED_ISLAND_TRIGGER_IDS.get(trigger_id)
```

GT-228 observed id 3 both in the target island-contact sequence and ordinary sailing. Therefore `trigger_id` alone is insufficient. `M2_OBSERVED_ISLAND_TRIGGER_IDS` should be treated only as an observation label and narrowed with scene/contact context before its output is used as island evidence.

## Source integrity

Verified unchanged after analysis:

- `GameClient.local.bin`: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- `PF_PROTOCOL_REGISTRY.tsv`: `27daac0c6fbbc45d88281c31b98e3a8b56f421bd1e8bc16f970fdff5716cfb4d`
- `PF_SERIALIZER_FIELDS.tsv`: `99282bdf3f492eaebdbab4918aecc0e37bf8efb42b904b18e1ba306767b5c123`
- Trigger field-validation evidence: `080a5f32580df575632fee69d3f8faa6e2e745ad1775d05daf3e272e4e0941c3`
- `TEXTDATA_TH__Trigger_TIP.tsv`: `bccbb0430a40793611d1bc864a7d81711fa46831c38c2f9769f9ffceaed7503f`
- `CONSTDATA_TH__Trigger.tsv`: `fb95860ac2979eb6179894eba0fa2bac8e4ca5e5d9a3f0e66b545a4d4fa59951`
- `lane_a_island_trigger_log.py`: `860f21a5223957b866daf3a2d1a7682277b03cb24d1ee6a3af4dcd1fb6bf75bc`

## Nonclaims

- W/R codec rows describe callable serialization branches; they do not prove which direction occurs in production.
- No claim that the original server sends a TriggerVital response, or what its policy is.
- No claim that the two gamedata tables use a namespace different from TriggerVital; only that identity is not proven without a crosswalk.
- No claim that AddSurveyData is the only report-window path in the whole image; the count above is limited to the two routes asked in RE-234.
- No new client-observable evidence was produced in this static run.
- Island/contact meaning is not inferred solely from matching numeric ids.

## BUILD_IMPACT

`ไม่มีโดยตรง` — this ticket changes no client/server build and authorizes no player-facing behavior. For debug/evidence quality, LANE-A should narrow the id-only observation override with scene/contact context before treating it as island attribution.

Please have Chief close RE-234 from this result.
