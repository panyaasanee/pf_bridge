# Monster name-color gate: RuntimeRes actor entry to CNetNPC

## [MEASURED] Result

This artifact re-derives 66 additive rows:
58 IMAGE rows and
8 DATA rows. Rows MCG-IMG-054 and
MCG-IMG-057 carry status `PROVEN_EXACT_MECHANICAL_CENSUS` and contain only
mechanically verified literal/immediate/vtable/direct-call facts. Rows
MCG-IMG-046..053, MCG-IMG-055..056, and MCG-IMG-058 carry status
`PROVEN_EXACT_MANUAL_HASH_ANCHORED`: their
predicate, branch-polarity, queue/dataflow and render-argument descriptions are
manual x86 interpretation anchored to exact pinned spans and byte checks. The
bounded conditional static path described by that manual review is:

RuntimeRes actor-entry wire qword -> record+0x18/+0x1C -> actor reconcile ->
actor type 4 factory -> CNetNPC vslot+0x10 -> CNetNPC+0x78/+0x7C -> same
manager registry node+0x18 -> same actor updater -> selector receiver -> that
actor's bound NPC nameboard controller -> controller+0x34 FontStyleID ->
typed LABEL_NAME UILabel interface -> label+0x90 ID -> style-registry lookup ->
style/text-component application -> conditional indirect glyph-render calls.

This is exact only under the named call gates. It does not say every spawned
CNetNPC reaches the selector or pixels: registry retention, controller allocation/
binding, live resource callback, actor+0x254, actor+0x258, actor+0x260, distance,
live selector predicates, style-registry population, UI traversal, visibility,
renderer dispatch, delivery, and device/framebuffer outcome remain runtime
conditions. Original-server identity policy and rendered screen color remain open.
Generator PASS is an integrity result; it does not symbolically derive or independently
prove the manual instruction semantics in MCG-IMG-046..053, MCG-IMG-055..056,
or MCG-IMG-058.

The output copies none of the 14 canonical rows in
PF_ATTR_NAME_COLOR_SELECTOR.tsv. Nine PROVEN_EXACT typed conditional
crosswalk rows reference canonical selector keys and add the same-instance
RuntimeRes/CNetNPC/controller path. Exact conditional RuntimeRes-to-selector
integration rows: 9. Canonical rows copied: 0. Canonical selector SHA-256:
d15864a21a7a124a23f6dffad174a55d376045a25a04814bbe6dc5f5632af82d.

## [MEASURED] Critical correction: the governing record is not CreateActorDataEx

The previous draft conflated two different records because both expose offsets
+0x18/+0x1C. Fresh IMAGE re-derivation proves that RuntimeRes CNetNPC spawn
uses the actor-entry record serialized at 0x005E21D0, not CreateActorDataEx
serialized at 0x005DFF60.

The exact incoming actor-entry field order is:

1. record+0x10: one byte, tag 0x0B, actor type.
2. record+0x18..+0x1F: one complete qword, tag 0x32, length 8. Its low
   dword is record+0x18; its high dword is record+0x1C.
3. one-byte Attr count, followed by each Attr id and Attr serializer.

On the READ branch, 0x005E230C..0x005E2316 passes length 8 and record+0x18
to 0x0089A640. Therefore every byte through record+0x1F, including that
record's +0x1B, is populated by the qword field.

## [MEASURED] Exact IMAGE pointer flow

- 0x005E4060 reads the RuntimeRes derived object at +0x1C, takes its list
  head at +0x10, and makes the direct actor-reconcile call from this handler
  to 0x00446F30. No whole-image sole-caller claim is made.
- 0x00446F87/0x00446F8A read the same entry's +0x18/+0x1C pair for the
  actor-registry lookup.
- On an unknown identity, 0x00446F9C..0x00446FA3 calls the factory.
- The factory reads actor type from the same record at +0x10. Type 4 selects
  the CNetNPC type node, whose registration is tied to RTTI .?AVCNetNPC@@.
- 0x00446A92..0x00446AB5 passes the same pointer-to-record to the new
  actor's vtable slot +0x10.
- CNetNPC slot +0x10 is 0x0045D200. 0x0045D23B..0x0045D244 copies
  actor-entry +0x18/+0x1C into CNetNPC +0x78/+0x7C.
- RuntimeRes reconcile and the periodic actor tick both receive the exact
  singleton address 0x0102C6C0 from getter 0x00402A20.
- Factory registration builds the value {identity low, identity high,
  CNetNPC pointer}. 0x006F4130..0x006F413E copies it to tree-node
  +0x10/+0x14/+0x18 and retains the actor pointer.
- Tick 0x00445480 reads the same node+0x18 pointer and calls 0x00444400 with
  it as ECX. The updater preserves ESI=ECX, then 0x004446A5 restores ECX=ESI
  and directly calls selector 0x00443F50.
- CNetNPC slot +0x7C creates controller vtable 0x00F2CD48, stores it at that
  actor+0x254, stores the actor back-pointer at controller+0x30, and binds
  LABEL_NAME at controller+0x50. Selector slot +0x34 resolves to 0x009F1A70,
  which stores the chosen FontStyleID at controller+0x34; the UI update reads
  +0x50 and +0x34 together.

This closes the bounded conditional same-instance selector/nameboard path. No
CreateActorVital alias is needed. The readiness, distance, lifetime and UILabel
consumers are pinned below; their live values remain conditions, not universal
runtime guarantees.

## [MEASURED] Exact readiness and distance gates

- CNetNPC vtable `+0x58` is `0x0045CD80`; its wrapper passes the callback
  argument directly to `0x00444730`. The common callback requires a nonnull
  argument, nonnull `argument+0x48`, and nonnull resource `+0x08`. On normal
  flow it installs `argument+0x48` at actor+0x80 and sets actor+0x70 bit 0x40
  at `0x004448B4`. IMAGE closes the conditional producer, not callback
  scheduling or resource completion.
- CNetNPC init sets actor+0x258 to one after the guarded nameboard-create
  vslot succeeds. That is not a permanent latch. Except when global mode is 6,
  common update subsequently forces +0x258 to zero when actor+0x10 bit 0x4000
  is set; otherwise it copies byte `[actor+0x80+0x74]`, using zero for a null
  actor+0x80. Mode 6 preserves the previous value by skipping this refresh.
- CNetNPC construction clears +0x260 and +0x264. While +0x260 is zero and bit
  0x40 is set, each CNetNPC update increments dword +0x264. The
  eleventh qualifying update makes the counter exceed ten and latches +0x260 to one.
  Clearing bit 0x40 pauses this body; it does not reset +0x264 here.
- Updater `0x00444400` first requires actor+0x254 and controller+0x10. CNetNPC
  takes the non-special-type branch. The reference vector comes from
  `[app+0x17C]` when nonzero, otherwise `[app+0x08]`; actor position comes from
  `0x0043BCE0`. The code computes squared xyz distance. Greater than
  `10000^2` returns before the selector. At or below `10000^2`, greater than
  `5000^2` calls `0x0043D7B0` and converges with the nearer lane. Both +0x258
  and +0x260 must then be nonzero before `0x004446A7` calls the selector.
  The integers are exact; the world unit is unnamed and is not claimed to be
  meters.

Concrete failures are therefore statically available: an unscheduled or null
resource callback leaves bit 0x40 clear; bit 0x4000, null actor+0x80, or zero
model+0x74 makes +0x258 zero; fewer than eleven qualifying updates leaves
+0x260 zero; missing controller state or distance greater than `10000^2`
returns before the selector. Whether any one occurs for a live actor is runtime.

An additional conditional same-CNetNPC zero path is now pinned. CNetNPC vtable
slot +0x38 resolves to `0x0045B770`. Under its global,
actor+0x35C and imported-result gates it calls
`0x00442340` with first argument
0. The shared routine requires actor+0x80 and a
model+0x74 byte different from the requested zero; on that path it stores zero
at the same actor+0x258. If model+0x74 is already zero it returns before this
store. IMAGE does not name the vslot event or connect it to a network Attr,
relation, combat or death message, so this is not called a death transition and
its live invocation remains open. Fixed-displacement writer candidates in
unrelated object layouts are not promoted into CNetNPC writers without a typed
receiver join; alias and whole-object writes remain outside this bounded census.

## [MEASURED] Exact registry lifetime/removal boundary

Registry membership, actor lifetime and rendered pixels are separate states.
The tree node stores the actor pointer at +0x18 and tick dispatches only retained,
valid node payloads.

- Sweep `0x004462F0` compares byte actor+0xD4 with 3. Equality jumps over
  erase; a valid actor node whose byte is **not 3** is advanced past and then
  erased through `0x00638AD0`. The pass also clears the pending vector. No
  gameplay name is assigned to state value 3.
- Reconcile increments manager+0x04. Incoming actors found or created in that
  generation receive the new value at actor+0xD0. During the second tree pass,
  a nonnull actor whose +0xD0 does not match is retained only by the special
  dynamic-type exception for token `0x0102CB04`; otherwise the actor pointer is
  appended to manager vector +0x2C. This is a
  pointer queue, not a qword-key queue.
- Manager frame update `0x00446750` first invokes actor vslot+0x18, then calls
  queued eraser `0x004463D0`. For each queued actor pointer, that eraser reads
  actor+0x78/+0x7C, resolves the matching manager+0x0C tree node, erases it,
  and clears the vector.
- Full clear `0x00446810` erases the whole tree and clears the vector whenever
  that method is invoked.

These paths prove loss of registry membership and therefore future tick
eligibility. They do not by themselves prove immediate actor destruction.
Which sweep/reconcile/clear path runs, and its ordering relative to a frame,
remains live scene state.

## [MEASURED] UILabel state, style application and render ceiling

The LABEL_NAME binder does more than store an untyped child. It looks up the
literal child, obtains its dynamic type, compares it through the token returned
by `0x00AA7010`, and stores the adjusted pointer only on success. Static token
initialization builds global `0x01090A04` from `.?AVUILabel@@`; thus
controller+0x50 is an exact conditional UILabel interface pointer.

Nameboard update requires controller+0x50 and its visibility gate
(`app+0x778` bit 0x20 or controller+0x44 greater than zero). It calls UILabel
vslot+0x138 to read the numeric FontStyleID and compares it with
controller+0x34. On mismatch it dispatches vslot+0x13C. The independent
`FontStyleID` property parser uses the same slot, and both pinned 0x220-byte
UILabel pool vtables resolve +0x138 to `0x004021F0`, +0x13C to `0x00AA37D0`,
and +0x144 to `0x00AA6EF0`.

`0x00AA37D0` stores the requested ID at UILabel+0x90 before looking it up in
the global style tree at `0x01090708`. A positive found ID returns node+0x10;
nonpositive or absent IDs return null. The setter still dispatches vslot+0x144.
`0x00AA6EF0` is a no-op for null. For a nonnull style it copies style fields,
invokes several UILabel setters, configures the UILabel+0x198 text component,
stores its returned resource handle at component+0x10, and marks component
and label state dirty.

The new mechanical census pins ASCII `.\Data\GUI\Model\BigFontStyle.fsl` at
`0x00F091F0`, wide attribute name `ID`
at `0x00F44BC4`, manager `0x01090708`, and
exactly one raw E8+rel32 byte-pattern site to loader
`0x00A9F860` at `0x004086E6` across
all 6 exact PE section-table entries, including `.rsrc` and
`.reloc`, using each section's `min(VirtualSize, SizeOfRawData)` file-backed
interval. It likewise finds exactly one raw rel32 site
to outer resource routine `0x00408530` at
`0x0040A2E9`. These are mechanical byte facts;
they do not themselves interpret execution or success.

Manual x86 review of the pinned loader span shows it clears manager+0xE4's
keyed tree, parses the supplied document, iterates its children, reads the
`ID` string, converts through `MSVCR90.dll!_wtoi`
and takes the mechanically pinned `signed_greater_than` branch relative
to 0. The accepted path allocates
0x78 bytes, calls `0x00A9D6B0`, inserts/resolves that integer key through
`0x006BC410`, stores the style pointer, and calls `0x00A9DAE0` with the same
child. The DATA document independently has root `FontStyleList` and exactly
186 unique ordered IDs 1..186; IDs
56,57,58,59,60,61,62,63 therefore meet the
positive-ID condition. That DATA-to-IMAGE composition is stated here, not
mixed into one TSV row.

The inner loader can return zero when document parsing fails, but outer routine
`0x00408530` does not test that inner return before continuing.
Therefore its caller's later AL test does not prove the style load succeeded.
This remaining failure still separates state from pixels: a missing live entry
leaves label+0x90 equal to the requested controller
ID while style application did nothing, and the next nameboard update can skip
a retry of that same ID. The remaining blocker is narrowed to live parse/
allocation/tree state rather than an unknown static registration path.

## [MEASURED] RE-191: exact conditional FontStyle 61/62/63 color route

The premise is corrected rather than repeated: `0x00AA488F` is not the RGB
property parser. It is the UILabel XML branch for numeric
`FontStyleID` (wide literal `0x00F8A4DC`).
When that property exists, a retrieved text value that is empty or equals the
empty sentinel `0x00F0930C` bypasses
`0x00894700` and dispatches explicit ID
0 through UILabel vslot+0x13C from
`0x00AA48DC`. The nonempty, nonsentinel lane reaches 0x00894700; IMAGE proves no digit validator, so arbitrary nonempty text (e.g. abc) may reach _wtoi and yield 0.
When the property itself is absent, UILabel vslot+0x140 resolves to
`0x006CEDF0`, returns UILabel+0x1A0, and the same
block calls `0x00A9DAE0` for embedded
`FontStyle` (wide literal
`0x00F89FB8`).

The registry loader independently calls `0x00A9DAE0` at
`0x00A9FA11` for each accepted positive-ID
child. An all-six-PE-section file-backed raw-byte E8+rel32 census finds exactly
2 direct
sites to that target: `0x00A9FA11`, `0x00AA490D`.
The scan covers `.text`, `.code`, `.rdata`, `.data`, `.rsrc`, `.reloc`, including
`.rsrc` and `.reloc`. It checks every byte position whose five-byte E8+rel32
encoding fits within the section's `min(VirtualSize, SizeOfRawData)`
file-backed interval; it is not a negative inferred from linear disassembly.
Exact scanned bounds: `.text` VA 0x00401000..0x00C39A2C, file 0x00000400..0x00838E2C, `.code` VA 0x00C3A000..0x00C3A2E1, file 0x00839000..0x008392E1, `.rdata` VA 0x00C3B000..0x0101938E, file 0x00839400..0x00C1778E, `.data` VA 0x0101A000..0x0102BE00, file 0x00C17800..0x00C29600, `.rsrc` VA 0x0109C000..0x010F4998, file 0x00C29600..0x00C81F98, `.reloc` VA 0x010F5000..0x012865F0, file 0x00C82000..0x00E135F0. The property-parser span is
`0x00A9DAE0..0x00A9DD9B`,
file `0x0069CEE0..0x0069D19B`,
SHA-256 `5f974da52ed482920db7a92285d6e61e6a40594d864a6d659791054db46525ef`.

Manual x86 interpretation of that pinned span establishes the color semantics.
Wide `FontColor` at `0x00F23608` is read through
`0x0053F7B0` and copied to UIFontStyle+0x30..+0x3C.
Wide `OutlineEffectColor` at `0x00F89EF0` uses the
same wrapper and is copied to UIFontStyle+0x4C..+0x58. The wrapper reaches
`0x0053F5E0`; each ordered integer component is converted
through `MSVCR90.dll!_wtoi`, divided by exact double 255
at `0x00F0C630`, clamped to [0,1], and stored as float32. That
normalizer span is `0x0053F5E0..0x0053F7AC`,
file `0x0013E9E0..0x0013EBAC`,
SHA-256 `b9e671dce7a39a3e746142e78e94b064bab287e3cdb9be5771b23fa958185809`.

For a nonnull numeric-ID lookup, `0x00AA6EF0` passes
UIFontStyle+0x30 to UILabel vslot+0xD8 ->
`0x006D0F40` and UIFontStyle+0x4C to vslot+0x224 ->
`0x006D0CF0`. Thus the static property-to-UILabel
route is closed conditionally. The exact per-ID tuples below remain DATA facts;
the normalized columns are an explicitly labelled DATA+IMAGE composition, not
new IMAGE rows.

| FontStyleID | DATA FontColor RGBA | conditional normalized float32 | DATA OutlineEffectColor RGBA | conditional normalized float32 |
|---:|---|---|---|---|
| 61 | (255, 100, 100, 255) | (1, 0.392156869, 0.392156869, 1) | (150, 0, 0, 255) | (0.588235319, 0, 0, 1) |
| 62 | (255, 159, 113, 255) | (1, 0.623529434, 0.443137258, 1) | (91, 30, 0, 255) | (0.356862754, 0.117647059, 0, 1) |
| 63 | (179, 179, 179, 255) | (0.701960802, 0.701960802, 0.701960802, 1) | (60, 60, 60, 255) | (0.235294119, 0.235294119, 0.235294119, 1) |

Therefore style 63 is distinct from controls 61 and 62: its DATA FontColor is
exactly `(179, 179, 179, 255)` and outline is
`(60, 60, 60, 255)`. This answers
RE-191 at the conditional static resource/property layer. It does not prove the
startup loader succeeded in a live process, that lookup returned a live node,
that the selector path ran for a particular actor, or that any framebuffer pixel
was produced.

The two pinned UILabel vtables resolve draw slot +0x38 to `0x00AA71A0`.
After visibility and optional handle gates, it tail-dispatches text-component
renderer `0x00A8AF50`. That renderer has further handle, line-count, size and
clipping gates, then reaches a global renderer vslot+0x20 call and per-line
object vslot+0x3C calls carrying position, glyph and color arguments. This is
the bounded static submission ceiling. Exact frame traversal for this instance,
concrete renderer receiver/vtable, culling/scissor/alpha, device success and
final framebuffer pixels require runtime evidence.

## [MEASURED] BasicAttr identity is a separate qword

BasicAttr inherits a DBAttribute identity subcodec at 0x00467790. That
subcodec conditionally serializes the Attr object's own +0x18/+0x1C qword
under its own mask byte at attr+0x20.

That is not the actor-entry qword, even when a sender chooses to put the same
numeric value in both places. CNetNPC init copies the actor-entry qword first,
then calls 0x005DF080 to bind the Attr vector. This proves the origin of
CNetNPC +0x78/+0x7C. The separate registry and updater rows prove the
conditional same-object selector invocation; the two qwords remain distinct
wire fields even when a sender chooses equal numeric values.

## [MEASURED] CreateActorDataEx and the +0x1B blocker

CreateActorDataEx remains a real, separately proved IMAGE type:

- its constructor establishes +0x18=0xFF, +0x19=0, +0x1A=0, and +0x1C=0;
- its 0x005DFF60 codec reads three one-byte fields into +0x18, +0x19,
  +0x1A, and one four-byte field into +0x1C;
- neither the complete pinned constructor nor codec establishes +0x1B;
- the visible allocation thunks provide no zero-fill contract.

Thus +0x1B is a genuine blocker only if someone tries to reconstruct a
CreateActorDataEx dword from those three adjacent bytes. It is not a blocker
for RuntimeRes actor identity and does not govern CNetNPC name color.

## [MEASURED] Selector-local signed identity gate and typed conditional style crosswalk

The selector treats receiver+0x7C as the signed high dword and receiver+0x78 as
the unsigned low dword. The gate and its bounded same-instance connection to a
RuntimeRes-spawned type-4 CNetNPC are exact under the invocation/readiness gates.

- Positive: high > 0, or high == 0 and low != 0.
- Nonpositive: high < 0, or both dwords are zero.

When the same-instance path reaches the selector and each listed canonical
condition holds, the crosswalk is:

| Conditional canonical selector condition | FontStyleID | Exact DATA FontColor |
|---|---:|---|
| positive identity and relationship predicate false | 56 | (255, 62, 255, 255) |
| positive identity, relationship true, local lookup succeeds | 58 | (140, 198, 255, 255) |
| positive identity, relationship true, style-58 lookup not selected, later secondary relation query true | 59 | (0, 255, 255, 255) |
| positive identity, positive-lane fallthrough | 57 | (83, 255, 83, 255) |
| nonpositive identity and relationship predicate true | 60 | (255, 255, 0, 255) |
| nonpositive, relationship false, receiver vslot+0x3C false, NPCAttr associated-actor lanes fall through, n_OFFESIVE nonzero | 61 | (255, 100, 100, 255) |
| same prior fallthroughs, n_OFFESIVE zero, bit 0x100 set, local vslots +0x3C/+0x40 both false | 61 | (255, 100, 100, 255) |
| same prior fallthroughs, n_OFFESIVE zero, bit 0x100 clear | 62 | (255, 159, 113, 255) |
| nonpositive, relationship false, CNetNPC vslot+0x3C true | 63 | (179, 179, 179, 255) |

Style 63 has other canonical causes, so gray is not equivalent to dead.
Style 61 has other canonical causes, so red is not equivalent to n_OFFESIVE or
bit 0x100. The n_OFFESIVE branch does not read n_AGGRO. This table is not proof
that a particular live actor passed the readiness/predicate gates or rendered
the color; it is exact conditional static reachability.

## [MEASURED] Distinct actor and nameboard-controller objects

- `0x00F0DF58` is the CNetNPC actor vtable. Actor slot `+0x3C` at
  `0x00F0DF94` resolves to death predicate `0x0043BD70`.
- `0x00F2CD48` is the NPC nameboard-controller vtable. Controller slot `+0x34`
  at `0x00F2CD7C` resolves to style store `0x009F1A70`.
- These are different objects and different vtables, not pointer-equal objects.
  IMAGE proves their bidirectional binding: actor+0x254=controller and
  controller+0x30=actor. Caller `0x004446A7` supplies the RuntimeRes-created
  CNetNPC as selector receiver; selector reloads that actor's +0x254 controller.

## [MEASURED] Exact DATA palette

| FontStyleID | FontColor RGBA | OutlineEffectColor RGBA | Descriptive label |
|---:|---|---|---|
| 56 | (255, 62, 255, 255) | (136, 2, 5, 255) | magenta or pink |
| 57 | (83, 255, 83, 255) | (3, 122, 78, 255) | green |
| 58 | (140, 198, 255, 255) | (0, 0, 213, 255) | light blue |
| 59 | (0, 255, 255, 255) | (80, 80, 80, 255) | cyan |
| 60 | (255, 255, 0, 255) | (80, 80, 80, 255) | yellow |
| 61 | (255, 100, 100, 255) | (150, 0, 0, 255) | red or pink red |
| 62 | (255, 159, 113, 255) | (91, 30, 0, 255) | orange or salmon |
| 63 | (179, 179, 179, 255) | (60, 60, 60, 255) | gray |

RGBA tuples are exact DATA facts. English color labels are descriptive.

## [MEASURED] [RECONSTRUCTED POLICY] Exhaustive pinned-snapshot Foundation writer census

**[MEASURED] [RECONSTRUCTED POLICY]** This section is deliberately not represented as a
TSV evidence row. It combines a separately pinned project-source check
with IMAGE selector facts and the DATA palette. It is not original-server
evidence, not a client-observed render result, and changes no IMAGE/DATA row.

ServerProject snapshot boundary: Git commit
`8a8afa7c6ad7f13af5ac7088ffca6fc743cae5fa`, commit time `2026-09-01T07:50:38Z`
(`2026-09-01 14:50:38 +07:00`). Later commits are outside this section's
scope; the generator reads this exact commit and does not claim that it remains
the checkout's present state.

Snapshot: current/pf_login_game_server_v141.py, size 382913,
SHA-256 2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22.

- Line 1132 packs qwords as unsigned little-endian <Q.
- Line 1259 writes the
  make_remote_actor_entry actor_identity as tag 0x32 qword.
- The pinned V141 Port Royal builder passes positive examples
  0x1001..0x1006 to actor type 4 at line
  1316.
- It also places the same numeric value in the nested NPCAttr identity at lines
  1311 and 1185; that is a
  separate Attr qword and is not the selector source.

The fail-closed AST census finds exactly 30 literal
`make_remote_actor_entry` calls under Foundation: 19 flagless/reachable writer
definitions below and 11 explicitly excluded scenario/hypothesis/helper or
production-gated sites.
Scope count, exactly: **19 Foundation direct writer definitions reachable
without scenario flag (18 default +1 diagnostic conditional), excludes frozen
V141 fallback/scenarios; not 19 simultaneously active.**

`P` means `0x2000 + placement_index + 1`. Every one of the 18 shipped sites
uses P. The diagnostic also uses P; its D3 slot is the special concrete result
`0x2000 + 9000 + 4 + 1 = 0x432D`. At every row, the same identity value is
passed to the outer actor entry and to NPCAttr and optional MovementAttr where
those Attrs exist. This is a pinned-snapshot dataflow result, not proof of the
original server's identity policy.

| Direct writer | Line | Class | Reachability anchor | Identity origin | Same-identity carrier lines |
|---|---:|---|---|---|---|
| `world_population.py` | 707 | SHIPPED | runtime.py:8170 | population.py:46 P | 668-710 |
| `world_population_bg0002.py` | 199 | SHIPPED | runtime.py:7691 | scene2_prison_exile_tables.py:411 P | 183-202 |
| `world_population_bg0003.py` | 203 | SHIPPED | lane handoff | world_bg0003_identity.py:346 P | 187-206 |
| `world_population_bg0004.py` | 201 | SHIPPED | lane handoff | world_bg0004_identity.py:388 P | 185-204 |
| `world_population_bg0005.py` | 205 | SHIPPED | lane handoff | world_bg0005_identity.py:401 P | 189-208 |
| `world_population_bg0006.py` | 204 | SHIPPED | lane handoff | world_bg0006_identity.py:327 P | 188-207 |
| `world_population_bg0007.py` | 204 | SHIPPED | lane handoff | world_bg0007_identity.py:347 P | 188-207 |
| `world_population_bg0008.py` | 199 | SHIPPED | lane handoff | world_bg0008_identity.py:332 P | 183-202 |
| `world_population_bg0009.py` | 204 | SHIPPED | lane handoff | world_bg0009_identity.py:349 P | 188-207 |
| `world_population_bg0010.py` | 219 | SHIPPED | lane handoff | world_bg0010_identity.py:359 P | 203-222 |
| `world_population_bg0011.py` | 219 | SHIPPED | lane handoff | world_bg0011_identity.py:357 P | 203-222 |
| `world_population_bg0015.py` | 289 | SHIPPED | lane handoff | world_bg0015_identity.py:461 P | 273-292 |
| `world_population_bg4001.py` | 224 | SHIPPED | lane handoff | world_bg4001_identity.py:365 P | 208-227 |
| `field_mobs.py` | 1708 | SHIPPED | hostile entry users | field_mobs.py:321 P | 1617-1625;1703-1711 |
| `mob_combat.py` | 1323 | SHIPPED | runtime.py:4228/4356 | field_mobs.py:321 P | 1311-1324 |
| `mob_death.py` | 1622 | SHIPPED | runtime.py:4517/4654/4664 | field_mobs.py:321 P | 1373-1375;1612-1623 |
| `world_face_frame.py` | 213 | SHIPPED | runtime.py:7271 | world_face_frame.py:197 P | 197-213 |
| `lane_hooks/lane_a_choose_npc_scene14.py` | 333 | SHIPPED | runtime.py:7157 | Bg0015Placement/FieldMob P | 309-335 |
| `mob_diag_multi_object.py` | 464 | OPERATOR_CONDITIONAL_DIAGNOSTIC | runtime.py:8366 | FieldMob P; D3=0x432D | 451-468 |

Excluded direct calls:

| Direct writer | Line | Why excluded from 19 |
|---|---:|---|
| `field_mob_hostile_bg0015.py` | 205 | proof/helper composer |
| `hostile_hp_link_hypothesis.py` | 1260 | hypothesis |
| `npc_hostile_hypothesis.py` | 520 | hypothesis |
| `npc_hp_link_hypothesis.py` | 1085 | hypothesis |
| `population.py` | 224 | explicit population scenario |
| `population.py` | 287 | explicit population scenario |
| `remote_player_hypothesis.py` | 876 | hypothesis with variable actor type |
| `runtimeres_death_hypothesis.py` | 729 | hypothesis |
| `scenario.py` | 121 | explicit scenario |
| `scene_object.py` | 34 | explicit scene-load scenario |
| `lane_hooks/lane_a_choose_npc_scene1.py` | 238 | safety-net responder explicitly gated by production_allowed=False |

The frozen V141 fallback is outside Foundation and is kept separate. A
`build_field_mob_population` helper with no direct runtime caller in the pinned
Foundation census is not
promoted into a live route. The lane handoff route is
`runtime.py -> lane_hooks/lane_a_scene_census.py ->
world_population_handoff.py`; combat/death recomposition is
`runtime.py -> mob_scene_recompose.py`; face and scene-14 ChooseNPC have their
own direct runtime routes; the multi-object diagnostic is gated by operator
configuration. The scene-1 ChooseNPC safety-net responder is also kept outside
the reachable census because its module explicitly declares
`production_allowed = False`.

Two comments at `lane_hooks/lane_a_scene_census.py:181-198` still say scenes 4
and 10 have `login_entry_allowed: false`. The separately pinned registry has
both booleans true, and `scene_is_open_to_players` at lines 367-383 reads that
registry. `world_scene_travel.py:243-256` also says all ten surveyed doors are
open. These are stale comments, not inactive writers and not original evidence.

**[MEASURED] [RECONSTRUCTED POLICY]** For the pinned legacy examples and the snapshot's
nonnegative placement indices, high dword is zero and low dword is nonzero.
The exact conditional crosswalk therefore puts those identities in the
positive selector family whenever the call/readiness gates pass. If the
relationship-false condition also holds, the canonical selector emits
FontStyleID 56 and DATA maps it to magenta
(255, 62, 255, 255). This is not proof that the original server chose these
identities or that the client rendered pink in a particular live frame.
Positive identity alone cannot guarantee pink.

**[MEASURED] [RECONSTRUCTED POLICY]** This is an exact static contract conflict under the
named invocation gates between the exhaustive pinned-snapshot Foundation writer census
and the client selector, not evidence of what the original closed server
emitted. Changing only legacy V141 cannot repair these separately shipped
Foundation composers.

At this pinned snapshot, no single Foundation seam enforces
`outer actor identity == NPCAttr identity == MovementAttr identity`.
`legacy.make_remote_actor_entry` receives already-serialized opaque Attr bytes,
while the override splicers in `runtime.py:323-358`,
`world_population.py:977-1078`, and `mob_scene_recompose.py:674-752` replace
whole entry byte strings without validating their nested identities.

### [PROPOSED] Replacement identity-mapping seam

**[PROPOSED]** The recommended implementation seam has two coupled parts. First, a mapping
candidate must be a session-, scene-, and generation-scoped **bijection** with
`resolve_wire(W) -> P` and `project_wire(P) -> W`; it must prove uniqueness
against the entire outgoing census and be invalidated whenever scene or
generation changes. Second, one typed NPC-style composer must accept the
projected W once and build/validate the same W in the outer entry, NPCAttr, and
optional MovementAttr. Every outbound **actor-identity** reference in CHitResult,
bar, death, recompose, face and conversation paths must call
`project_wire(P) -> W`; inbound actor references must call
`resolve_wire(W) -> P`. Ground-drop elements in the pinned snapshot use their own u32
`drop_key`, and pickup matches that object reference; neither value is actor P
and neither must be remapped. A high-negative W is only a
bounded reconstruction candidate. It must not be hard-coded or described as a
proven original-server identity policy. This is a recommendation about the
replacement, not a claim about original-server architecture.

**[PROPOSED]** Pinned-snapshot seam map: census writers populate outer/NPCAttr/optional
MovementAttr; inbound combat resolves a target before roster lookup; CHitResult,
bar, death, face and recompose project the same active generation; scene or
generation changes invalidate the bijection. The ledger, roster and
`GroundDrop.mob_identity` retain canonical P internally. This is a proposed
replacement design, not original-server evidence.

### [MEASURED] Bg0002 n_OFFESIVE limitation

The pinned generated Bg0002 table contains 17 hostile rows: 12 use
AI_WANDER 16 and 5 Orc Chief rows use AI_WANDER 11. The pinned DATA-derived table
values say AI_WANDER 16 has `n_OFFESIVE=0`, while AI_WANDER 11 has
`n_OFFESIVE=1`. However, the pinned production-configured
`field_mobs.load_roster("Bg0002")` projection filters owner-refused placements
92-96, so its post-filter projection is 12 rows, all AI_WANDER 16. This is a
static project-snapshot projection, not a runtime- or player-observed roster. Do
not call the five Orc Chiefs pinned production-configured combat rows.

**[PROPOSED]** For an AI_WANDER-16 target, a coherent nonpositive identity remains a staged
candidate for orange before hit, red after the runtime bit is set, and gray
after the separately proved death predicate. The same-instance static join is
now proved; runtime still must show that the readiness, relationship, NPCAttr,
bit-writer, death and UI gates pass for the chosen actor. If the five
AI_WANDER-11 Orc Chiefs are ever sent by an alternate producer or reintroduced,
the canonical selector-local branch can emit style 61 at idle; identity change
alone cannot make those five universally orange. That future or alternate-path
constraint must not be hidden by calling them production-configured today.

### [PROPOSED] Bounded runtime stop rules for the mapping candidate

**[PROPOSED]** These are stop rules, not predictions promoted to proof:

1. **STEP-A:** the chosen AI_WANDER-16 target must be orange before attack. If
   it is not orange, stop; do not proceed to interpret later colors.
2. **STEP-B:** require a matched CHitResult whose target identity is the same
   projected W and require the screen to turn red. If either the addressed W or
   the red screen result is absent, stop.
3. Evaluate gray only after a matched corpse/recompose frame addressed to the
   same W carries HP=0 and timer<=0. A gray result before that does not prove
   the death lane.

Each step must retain, rather than assume away, the other IMAGE gates: resolved
target, target+0x10 bit 0x10000, source cast to CMyActor, relationship predicate,
NPCAttr fallthroughs, and the relevant receiver/local vslot predicates.

## [MEASURED] Runtime bit 0x100 boundary

The common actor constructor clears the containing +0x70 dword. Two direct
explicit set writers are proved: CHitResult and CMissileHitResult. Their
targets are not typed as CNetNPC at the writer sites, and no gameplay noun is
assigned to the bit. The typed CNetNPC selector consumes and can clear it.

IMAGE proves that both writers require a resolved target whose identity high
dword is signed-negative, plus their other pinned guards. **[MEASURED]
[RECONSTRUCTED POLICY]** At the pinned snapshot, the replacement combat path is connected:
`mob_combat.py:1201` composes CHitResult and
`runtime.py:4306` queues it as `MOB_COMBAT_ANNOUNCE`.
The pinned snapshot's P identities have high dword zero, so they fail the IMAGE writer's
negative-target gate before the bit can be set. This route statement is about
the replacement; the negative-target requirement is the separate IMAGE fact.

Crucially, this bit affects style 61 versus 62 only after the actor-entry
identity takes the nonpositive lane. A positive actor-entry identity bypasses
that typed tail first.

## [MEASURED] Nonclaims

- No original-server policy for choosing actor identities is claimed.
- Actor type 4 is proved to construct CNetNPC; IMAGE does not rename every type
  4 actor as monster.
- A positive identity is not, by itself, proof of pink; the relationship
  predicate remains part of the style-56 condition.
- BasicAttr identity and actor-entry identity may be numerically equal without
  being the same field or producer.
- CreateActorDataEx field meanings do not transfer to RuntimeRes actor entries.
- The unnamed runtime bit is not called aggro, hostile, or monster state.
- Direct bit writers are not a proof against alias or whole-dword writers.
- Generator PASS does not mechanically prove the manual x86 semantics recorded in
  MCG-IMG-046..053, MCG-IMG-055..056, or MCG-IMG-058.
- CNetNPC vtable slot +0x38 is not assigned a gameplay, combat or death noun.
- The exact startup loader wiring and DATA ID census do not prove a live style
  node, requested-to-applied style transition, or rendered pixel.
- The fail-closed pinned-project census covers direct literal Foundation
  `make_remote_actor_entry` call sites. It does not prove that dynamically
  obtained callables or raw authored frames cannot encode actor type 4.

## [MEASURED] Deterministic census

- Total rows: 66
- IMAGE rows: 58
- DATA rows: 8
- Mechanical-census IMAGE rows: 2 (`MCG-IMG-054`, `MCG-IMG-057`)
- Manual/hash-anchored IMAGE rows: 11 (`MCG-IMG-046..053`, `MCG-IMG-055..056`,
  `MCG-IMG-058`)
- BigFontStyle DATA census: root `FontStyleList`, 186 unique ordered
  IDs 1..186
- Canonical selector rows copied: 0
- Canonical selector rows referenced: 9 PROVEN_EXACT typed conditional crosswalk rows
- Exact conditional RuntimeRes-to-selector integration rows: 9
- Unique evidence keys: 66
- Ordered evidence-key digest: da15334224f67520c4401da4f8e83f8d31dc176db6e6821c444534c05fe1c082
- Row kinds: ACTOR_ENTRY_IDENTITY_LOOKUP=1;ACTOR_ENTRY_WIRE_READ=1;ACTOR_ENTRY_WIRE_WRITE=1;BRIDGE_COPY=2;CONTROLLER_STYLE_STORE=1;DATA_PALETTE=8;DEATH_PREDICATE=1;DELAYED_READY_LATCH=1;DISTANCE_SELECTOR_GATE=1;FACTORY_POINTER_FLOW=1;FACTORY_REGISTRY_JOIN=1;FONTSTYLE_COLOR_PARSE_APPLY=1;FONTSTYLE_COLOR_PROPERTY_ANCHORS=1;LABEL_FONTSTYLE_APPLY=1;LABEL_FONTSTYLE_SETTER=1;LABEL_RENDER_CEILING=1;MANAGER_TICK_DISPATCH=1;MODEL_READY_BIT_PRODUCER=1;NAMEBOARD_CONTROLLER_BIND=1;NAMEBOARD_READY_BYTE=1;NAMEBOARD_READY_ZERO_PATH=1;NON_ALIAS_BOUNDARY=1;RECORD_SEPARATION=1;REGISTRY_LIFETIME_REMOVAL=1;REGISTRY_NODE_LAYOUT=1;RUNTIMERES_DISPATCH=1;RUNTIME_BIT_CONSUME_CLEAR=1;RUNTIME_BIT_INIT=1;RUNTIME_BIT_WRITER=2;SAME_RECEIVER_SELECTOR_CALL=1;SEPARATE_ATTR_CHAIN=1;SEPARATE_ATTR_IDENTITY=1;SEPARATE_RECORD_ALLOCATOR_BOUNDARY=1;SEPARATE_RECORD_DEFAULT=1;SEPARATE_RECORD_PADDING_BLOCKER=1;SEPARATE_RECORD_TYPE=1;SEPARATE_RECORD_WIRE_READ=4;SIGNED_IDENTITY_GATE=2;SINGLETON_MANAGER_JOIN=1;STYLE_REGISTRY_CHILD_LOAD=1;STYLE_REGISTRY_STARTUP_WIRING=1;TYPED_SELECTOR_CROSSWALK=9;TYPE_FACTORY=1;TYPE_IDENTITY=1;VTABLE_BRIDGE=1
- Foundation direct writer calls: 30 (19 reachable, 11 excluded)
- Reachable direct writer definitions: 19 (18 default, 1 diagnostic conditional;
  not simultaneously active)
- Foundation Python snapshot: 157 files,
  manifest SHA-256 77fc5f7959fffee68ea6320bb32e29086ba1750b6bf301159bafb12198ed6ddd
- Separately pinned project inputs: 51 files,
  manifest SHA-256 43fddf2446cb75cc28c0dfb9eeab30e43c0892639ebb59673abcfd691c03c79b
- Bg0002 generated/live-after-filter hostile rows:
  17/12

## [MEASURED] Pinned inputs

| Input | Size | SHA-256 |
|---|---:|---|
| GameClient.local.bin | 14759424 | 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623 |
| BigFontStyle.fsl | 28144 | 77798599c203d36e11282633d4a91ac098b0e1e03aa2482fede6fcfca161fc10 |
| PF_ATTR_NAME_COLOR_SELECTOR.tsv | 14 rows | d15864a21a7a124a23f6dffad174a55d376045a25a04814bbe6dc5f5632af82d |
| legacy V141 source | 382913 | 2eb05ed2fdbdd5ee3d91f7fbb8c1d16a4c7a02a843bc97169b16a389e4ea4c22 |
| population.py | 11593 | df7bedb387963b67c0e4438479b057e8023a2a63efa1016000994982de18d52f |
| field_mobs.py | 103451 | 67c0467493f1bac36e374d24f86c5257001f1a57456b8ea77f739d7126008ecf |
| world_population.py | 58851 | 83d05df46cd26ae6fa38790650e8b20d9cd74ae4e04c369603ef2c18649c276b |
| runtime.py | 472447 | d683299d86853896304cf92ea0e0a738d1dfb5a2647d68b32a3a1c179e31efe5 |
| pinned-project pin manifest | 51 files | 43fddf2446cb75cc28c0dfb9eeab30e43c0892639ebb59673abcfd691c03c79b |
| Foundation Python snapshot | 157 files | 77fc5f7959fffee68ea6320bb32e29086ba1750b6bf301159bafb12198ed6ddd |

The exact-commit replacement-server snapshot above is a separately verified project check,
not a TSV evidence source. Generator PASS mechanically verifies pinned input
hashes, exact IMAGE span hashes, enumerated byte/RTTI/type-node/vtable/direct-call
anchors, exact DATA attributes, source separation, row order/content keys,
canonical-selector references, zero copied canonical rows, the two explicit
mechanical-census rows, the eleven explicit manual/hash-anchored status labels and
method nonclaims, the raw rel32 loader/outer-init/property-parser call censuses, the exact ordered
BigFontStyle ID census, all 30 direct Foundation
call sites, all 19 reachable writer-manifest rows, project-source anchors, and
output-pair bytes/hashes. It does not disassemble or symbolically execute the
image. Predicate meaning, branch polarity, pointer/dataflow joins, queue element
type, and render-call argument interpretation are manual review anchored to those
pinned bytes, not conclusions mechanically established by PASS. Runtime readiness
and pixel rendering remain outside both methods.

These files under `pf_bridge/external` are local-only and Git-ignored by the
workspace policy. Another clone will not receive the script/table/report until
owner-approved packaging. Git allowlisting/publication is outside this lane's
authority, so delivery remains local-only. `PF_MONSTER_COLOR_GATE.pair.json` is the commit marker:
the TSV and Markdown are a valid pair only when a marker-before/files/marker-after
read has identical marker bytes and both file size/hash entries match. Publication
stages both files, replaces them, then atomically replaces the marker last. A crash
before that final step is fail-closed and requires a later locked repair; fixed
filenames alone are not an indivisible filesystem object. This generator does not
modify Git.
