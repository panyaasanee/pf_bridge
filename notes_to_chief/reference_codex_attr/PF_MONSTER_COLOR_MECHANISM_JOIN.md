# PF Monster Color Mechanism Join

## [COMPOSITION][IMAGE+DATA] Result

**[MEASURED][IMAGE] Mechanism join.** The static join is closed: the `FACTION`
membership comparator is an upstream input to the same CNetNPC name-style
selector and controller/UILabel renderer path.  It is not a separate color
renderer.

**[MEASURED][DATA] Membership and palette.** The shipped DATA row keyed by `1`
contains `6` in `s_ENEMY`.  Existing source-separated palette evidence
MCG-DATA-001@7e247e4ca3b7c6b1f81c7aeddd46e8feb0e50d30c68214861de20029d04782d1 defines Style56 as FontColor `(255, 62, 255, 255)` with
outline `(136, 2, 5, 255)`, descriptively magenta/pink.

**[COMPOSITION][IMAGE+DATA] Conditional Style56 explanation.** For live local
value `1` and target value `6`, if `0x0043C380` reaches its FACTION fallback,
the IMAGE call direction is `(local, target)`, `0x004A1D50` returns false for
that DATA membership hit, and a signed-positive target identity makes the
audited selector request FontStyleID **56**.  This conditional
`(1,6) + fallback + positive identity` composition is a sufficient static/data
explanation for a Style56 request.  It is **not** the measured cause of
`SCENE-005`.  That cause remains **OPEN** until one same-actor trace proves the
fallback, relation result, requested ID, applied ID, and resulting pixels.

The composition does **not** make `(1,6)` an unconditional screen-color rule.
The relation function has earlier exits and overrides, loading must succeed,
selector and UI gates must pass, and final pixels are runtime facts.

## Direction and boolean proof

- **[MEASURED][IMAGE]** `MCMJ-IMG-004`: local actor is the `this` receiver; target actor is the
  stack argument.  The fallback resolves each actor's attribute object, reads
  `+0x68`, pushes target then local, and calls the manager as
  `arg1=local+0x68, arg2=target+0x68`.
- **[MEASURED][IMAGE]** `MCMJ-IMG-003`: the comparator returns false only when the row keyed by
  arg1 exists, its record is nonnull, and arg2 is present in that row's set.
- **[MEASURED][DATA]** `MCMJ-DATA-001`: row 1 is exactly `6;11;12;17;18;26`.
- **[MEASURED][DATA]** `MCMJ-DATA-002`: row 6 also contains 1, but that reverse row is not the
  row selected by the audited `(local=1,target=6)` call direction.

These are separate rows because IMAGE control flow and DATA values are separate
evidence layers.  **[COMPOSITION][IMAGE+DATA]** The conditional conclusion above
is their explicit composition, not a mixed-source TSV row and not measured
SCENE-005 causation.

## Selector and renderer join

**[MEASURED][IMAGE]** `MCMJ-IMG-005` adds only the missing upstream edge: the exact result of
`0x0043C380` is consumed inside `0x00443F50`; false in the signed-positive
identity lane pushes ID 56 and reaches the common controller vslot `+0x34`
sink.  The downstream controller store, `LABEL_NAME`/UILabel setter, style
registry, color apply, and renderer ceiling are not copied as new facts.  They
are referenced by their prior keys:

- selector/style edge: MCG-IMG-025@ee873e584b31215b2bd872784efacb3d72d9280d37e5cde439d4f913fc8d6f36
- controller style store: MCG-IMG-045@61c77d4a1ae4530008e9042db6799600def4c3b405e342f6db97e758920e4964
- UILabel/style apply/render: MCG-IMG-051@5eb4fb255371e1f0697518f50069695fb2d3d90bcb70a144456c814e2a4dc89a, MCG-IMG-052@3da1d093ad7df399f38b54f9dd02f38906e19da3a6035de72481fe3772286cf8, MCG-IMG-053@1a2981dff0a1a5a1927b9efe0c35ed5ae3d1a3ba75dc1b9e5e4d009a6d7ecadb
- BigFontStyle startup/load/color parse: MCG-IMG-054@05aec8e3de35ba77ead5cb5ce006660b72e22a211a07014df48fa848901d164d, MCG-IMG-055@7a676f4fe8acf4748105ff6b5dffb337997b7dde695c414d60e4cf823d7e56e2, MCG-IMG-057@c57eb03ef90d339cea95ffa47bcc6f519b726b7e7629666d6bbdb922920b9706, MCG-IMG-058@3a4a5aef9ed8a22cc9671e57e3c422a13b12f6bbdc3cec9667bd5d92ed3126d3

## Why faction alone is not enough for orange/red/gray

**[MEASURED][IMAGE]** Within the audited `0x00443F50` selector path, IDs 61, 62, and 63 occur after
entry into the signed-nonpositive identity lane and depend on additional death,
offensive, unnamed bit `0x100`, linked-actor, and local-state conditions.  The
exact pre-existing branch references are MCG-IMG-030@e0f7eb4cdc83679959adcacfacf222122c169fed803586c6b951906b4dda031e,
MCG-IMG-031@7782bb41255484f1ba482a911f2f3800744d3434f9f3c8fd6c566053635ad1a6, MCG-IMG-032@6a20794931b4d0d8cb70ad9d1cf45cbb2ab8f87a2badadb08cb7e7f4480ed23c, and MCG-IMG-033@0ff5dd0011ac742373f643770fa72031c9adb657f11fe9c272e2cd2ca6f9b935.

**[MEASURED][DATA]** Their source-separated palette references are:

- Style61: MCG-DATA-006@b204ce72068ec5b55d8425681dd9ca7fa2987e74be1de900e725090519fc5812, descriptive label `red_or_pink_red`, exact
  FontColor `(255, 100, 100, 255)`.
- Style62: MCG-DATA-007@c8f8ef6a1e8d049f96e8005b609fd717391bee844e2ae9ba0da25aa020b6847f, descriptive label `orange_or_salmon`, exact
  FontColor `(255, 159, 113, 255)`.
- Style63: MCG-DATA-008@01cddd7bccb4f3d1b98c31d3131d92c914d552c870845591edb43c459e0579e3, descriptive label `gray`, exact FontColor
  `(179, 179, 179, 255)`.

**[MEASURED][IMAGE]** The signed-nonpositive boundary is asserted only for this audited selector; it
is not a global claim about every color path in the client.

## Implementation decision and exact blocker

**[COMPOSITION][IMAGE+DATA]** The conditional `(1,6) + fallback + positive
identity` path is a sufficient static/data explanation for the selector to
request Style56.  It is **not** the measured cause of `SCENE-005`.

**[OPEN][RUNTIME]** The `SCENE-005` cause remains **OPEN** until one same-actor
trace proves the fallback, relation result, requested FontStyleID, applied
UILabel FontStyleID/style pointer, draw dispatch, and resulting pixels.  It is
therefore **not yet safe** to implement the intended orange/red/gray behavior
by changing faction alone.

The narrow remaining blockers are:

1. Prove the original actor-entry identity/state carrier that can enter the
   selector's signed-nonpositive lane without breaking actor registry lookup,
   same-object retention, or lifecycle.
2. Prove same-actor runtime transitions for the death predicate, offensive
   predicate, unnamed bit `0x100`, and local-state gates that distinguish IDs
   61/62/63.
3. In one same-actor `SCENE-005` trace, prove fallback, relation result,
   requested FontStyleID, applied controller `+0x34` and UILabel FontStyleID/style
   pointer, draw dispatch, and observed pixels.  This static task did not run
   client, server, dump, or capture.

## Evidence discipline

- New TSV rows: 8 (6 IMAGE, 2 DATA).
- Every row has exactly one `source` value.
- IMAGE rows carry file offsets, span hashes, image size, and image SHA256.
- DATA rows carry decoded in-memory offsets and span hashes; decoded bytes are
  never written.
- No new evidence key or exact claim tuple duplicates
  `PF_MONSTER_COLOR_GATE.tsv`; reused facts are cited through `prior_reference`.
- Pair generation SHA256: `40bee0ae06ec8fd710b768b25e029b775cd7eb157f8e75f3047900ff81e14ccc`.
- TSV SHA256: `dfaf5f31380c3ce6a0cfffd6b8778e1a28154b6438f5f404067b402c3d324190`.
- The pair generation covers normalized full TSV and Markdown bytes. Both files
  are staged before per-file atomic replacement under an exclusive byte-range
  lock. A stop between replacements is detectable as a pair/hash mismatch.

## Pinned inputs

| Input | Size | SHA256 |
|---|---:|---|
| GameClient.local.bin | 14759424 | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623` |
| B_CONSTDATA_TH.pc_ | 426944 | `496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8` |
| decoded B_CONSTDATA_TH (memory only) | 8443000 | `496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d` |
| BigFontStyle.fsl | 28144 | `77798599c203d36e11282633d4a91ac098b0e1e03aa2482fede6fcfca161fc10` |
| PF_MONSTER_COLOR_GATE.tsv | 110234 | `8d236351d827a39a74fe9b5e1b9ac694f5f51af5328fcedc1d9f207720bcbaa0` |

## Re-derive

```powershell
py -3 pf_rederive_monster_color_mechanism_join.py --check
```

`--check` holds the publication lock, reads both outputs twice in opposite
orders, verifies their shared normalized pair generation and TSV hash, then
verifies every pinned input, PE layout, span hash, direct-call anchor, import
name, in-memory CONSTDATA parse, palette reference, prior reference, source
separation, duplicate guards, and exact output bytes without writing.
