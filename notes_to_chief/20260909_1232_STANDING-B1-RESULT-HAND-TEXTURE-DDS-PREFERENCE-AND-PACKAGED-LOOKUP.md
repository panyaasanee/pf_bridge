งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: สายอุปกรณ์ GT-272, CORE, LANE-B, LANE-K, chief และ Panya · จาก Codex static RE
B1j · ปิด 2026-09-09T12:32:47.407154+07:00 · IMAGE A / reused DATA A / composition D · NEWPROGRESS: conditional DDS preference

Answer to B1i's open texture-path question: YES, the equipment texture loader can choose a same-basename .dds in place of nominal .tga. The substitution is inside8A21D0, before the generic packaged extension rewrite. It requires the .dds candidate's exists callback to return true. This closes the conditional path mechanism, not native decode/upload/pixels.

ค้นชุดส่งมอบแล้ว: เจอ prior quest-mark resource resolver's generic8A21D0 and existsB01DD0 spans; exact SHA rechecked from original IMAGE and reused. Protocol registry/serializer fields have no match for886600/8A21D0/NiSourceTexture. The prior quest report did not establish this equipment-specific DDS preference; do not repeat its TGA reader registry.
ค้น gamedata แล้ว: เจอ EQUIPMENT_BASE index/columns and B1h's four selected item/map keys. Reuse B1h original table proof and four exact .dd_ hashes; no new asset decoding or table census. FUNCTIONAL_COVERAGE.json still marks equip_unequip and appearance_and_avatar_binding in_progress; bounded docs/reports search found no886600/8A21D0 result. Search log/source hashes are pinned in the manifest.

IMAGE path and gate chain:
1. 88B820 reaches88BA36->886600 after nonempty wide-path test8946C0; its earlier material/property gates remain B1i's ceiling. Manager comes from409F20. 886600 rejects null input, a failed _wsplitpath_s or empty basename. If manager+18=0 it uses incoming path; otherwise formatF0EBF0 "%s%s%s" combines manager+4 prefix with extracted basename and original extension. Thus a configured prefix can change the directory; the table below assumes the resulting input is B1i's nominal directory.
2. 88674B calls8A21D0. That function parses the narrow source at8A2202->92E850. _splitpath_s stores extension at parsed+103, basename+203, directory+0 and drive+100. At8A2227 it compares the extension case-insensitively with ASCII F5AAE4 ".dds" through793EE0->_stricmp.
3. If already .dds (any case), branch8A2231 skips this preference probe. Otherwise8A2233/2245 writes ".dds" into the parsed extension via strcpy_s;8A225F->92EA40->92E8A0 recomposes the candidate with directory/basename preserved. The four short ASCII paths fit; no general malformed/oversize path guarantee.
4. 8A226B pushes mode0 and8A226E calls exists dispatcher790F20 (slot1027B90). False at8A2278 preserves the original source path. True reaches8A2286->7E0B30 and replaces the selected fixed-string source with the .dds candidate. This happens before normalization/cache lookup; on the uncached constructed-object path,8A2347/4D copies the selected source to object+30 through790D80. A cache hit can return an existing object instead.
5. The canonical static bootstrap callsite40AFA6/AB installsB01DD0 through790F30. Under this installed callback, mode0 takes GENERIC_READ/FILE_SHARE_READ. It rewrites the candidate throughB7A780, then CreateFileA atB01E68 tests the packaged path first (OPEN_EXISTING). On failed transformed open and a successful rewrite, B01E84 tries the original .dds. Successful handle is closed atB01EAA and returns true. For this read mode, failure of both attempts returns false. Live callback slot/CWD/file permissions/sharing and races remain runtime conditions.
6. B7A780's existing extension rule only changes the last character: .dds->.dd_. Therefore the two distinct stages compose as nominal.tga -> candidate.dds -> packaged.dd_. The original .dds fallback can succeed even without a packaged .dd_.

Under .\Data\GC\M\ (same directory after any manager prefix handling):
| nominal texture | preference candidate | packaged first attempt |
|---|---|---|
|WR_SWORD_003_002.tga|WR_SWORD_003_002.dds|WR_SWORD_003_002.dd_|
|WR_SWORD_004_002.tga|WR_SWORD_004_002.dds|WR_SWORD_004_002.dd_|
|WL_SHIELD_001_000.tga|WL_SHIELD_001_000.dds|WL_SHIELD_001_000.dd_|
|WL_SHIELD_003_004.tga|WL_SHIELD_003_004.dds|WL_SHIELD_003_004.dd_|
DATA A: all four matching packaged files exist locally with B1h's exact hashes. This read-only existence/hash check is not an execution of the game's CreateFileA probe or a proof that DDS content decodes. When the DDS probe is false, nominal .tga remains selected and the later generic packaging route may try .tg_; original .tga fallback belongs to that separate open path.

Return-value ceiling: source ctor8A2090 sets vtableF5AA88; its+58 slot points to8A1DA0. Generic entry's global10281D8 gate can skip eager validation, and8A1DA0 delegates conditionally to renderer108D0C8.v118. If eager validation is attempted and false, the new source is released and factory returns null; a nonnull factory result still does not establish selected fixture pixels. No renderer, converter or DDS reader completeness claim is made here.

BUILD_PROPOSED: Add the selected nominal/candidate path distinction to B1h's existing staged RH/LH appearance trial and observe the actual normal/alternate request route; classify DDS preference failure separately from model/texture acceptance | GT-272 equipment owner / CORE, LANE-K to assign | exact packet stage + selected path/probe result when instrumented (grade C), paired with visible RH/LH result; retain separate uninstrumented grade B observation
BUILD_IMPACT: Binary contains the conditional DDS preference; native success remains open. Next bounded question: B1i's alternate processor78A9F0 / owner callback45B400, because post-seed hand changes can select that route; do not expand into a global texture census.
nonclaims: No game/server/native code run; no file open by the game's callback, decoded proprietary pixels, upload/bind proof, original-server behavior, legal equipment class/slot, stats, persistence/reconnect or runtime promotion. No asset, queue, lease, reference, ServerProject or Git writes. B1i's previously open mechanism is advanced by this new evidence; its historical letter is unchanged.

Evidence: image14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. Ranges are [start,end); exact file offset and SHA256. Full span/source inventory: staged/standing_b1j_manifest.json.
- equipment_texture_load: VA00886600..008867C4; file485A00; 452bytes; SHAef706883968062e1f147b6faeeeda597da945aefa8f75ff91b89b49745a9c9e0.
- generic_source_factory: VA008A21D0..008A2401; file4A15D0; 561bytes; SHA7c2e90f233a2aade00be5d0f09dbf19ae269b245b4ffdb9abe804c20331681c1.
- split_path: VA0092E850..0092E895; file52DC50; 69bytes; SHAc7bea37ae7c909109b47ddc33badd917a988464cee059876e31335b3284ae00f.
- exists_callback: VA00B01DD0..00B01ECB; file7011D0; 251bytes; SHAce3491e3c5b839efd1d54d6fc6e066178bfc0e670e560b5317c4eab0d9a15197.
Manifest SHAb69aa52be55e5378614cc964a166c1d4a73595ca2dbc41a4da6809df3b98aaa8; verifier standing_b1j_verify.py SHAd255c8e45dd238285cd8403fcea4aab8f1685a3d4f666caeb94ae235d1e4b964; log SHA342f6b61f55838cd5db212564d5cde186a17de4cda8e4ff50a29fa1d407d0ec4. PASS27spans/21code ranges/1183instructions/14sources/71calls/221pins/4strings/2vslots/45independent anchors/6imports/4pathtriples/6branch controls; source hashes checked before/after. Branch controls are Python abstraction, not execution of client functions.
Actual frozen pf-adversary review /root/a6f_review: verifier exit0; no material defect. Checked parsed component offsets, conditional substitution, mode0 fallback, prefix relocation, selected-source field and decode/pixel ceiling.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
