งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: สายอุปกรณ์ GT-272, CORE, LANE-B, LANE-K, chief และ Panya · จาก Codex static RE
B1i · ปิด 2026-09-09T12:27:39.962620+07:00 · IMAGE A / reused DATA A / composition D · PARTIAL NEWPROGRESS

Answer: B1h's four hand keys have exact nominal model paths. The normal request callback can accept an aggregate model without proving that every selected hand or texture loaded. Actor dirty250=0 is submission bookkeeping, not a visual completion token.

1. Path initialization and selected files (IMAGE A)
In full resource_request78EBF0..790766, nonnull request is required. First-use flag108B75C bits1/2/4 initialize globals: 78EC71/76/86 converts ASCII F0DA30 ".\\Data\\GC\\M\\" through88E270 into wstring108B740; 78ECAF/B4/C0 initializes108B724 from UTF16 F18034 ".nif"; 78ECED/F2/78ED02 initializes108B708 from F0DE64 ".tga". These are conditional initialization instructions, not an observation of live BSS. 88E270 imports MultiByteToWideChar and wstring wchar-pointer ctor.
RH concatenates base+key+model suffix at78FB92/9A and base+aux+texture suffix at78FC0B/13; LH equivalents are78FD91/99 and78FE0A/12. Normal part records place model path at+10, attachment node at+2C, aux path at+64, slot at+9C and ItemID at+A8. Nonempty aux is conditional.

Under directory .\Data\GC\M\:
| ItemID | nominal model filename | nominal aux filename |
|---|---|---|
|2200201|WR_SWORD_003.nif|WR_SWORD_003_002.tga|
|2200203|WR_SWORD_004.nif|WR_SWORD_004_002.tga|
|2200601|WL_SHIELD_001.nif|WL_SHIELD_001_000.tga|
|2200603|WL_SHIELD_003.nif|WL_SHIELD_003_004.tga|
B1h's exact original table/key derivation and eight file hashes are reused. In the canonical installed resource callback described by PF_GROUND_DROP_LIFETIME, extension helperB7A780 compares .nif/.tga/.dds and replaces the final character with '_' atB7A8B4: .nif->.ni_, .tga->.tg_, .dds->.dd_. Therefore selected .ni_ model files match that route; same-basename .dd_ existence does NOT yet close nominal .tga resolution. Current working directory, live callback installation, cache state, decoding and successful native loading remain conditions.

2. Submitted, processed and accepted are separate (IMAGE A)
- 441710 requires dirty250 and a nonnull generated request. The app+180.v1C submission branch keeps dirty on rejection; accepted branch appends owner318. Other branch enqueues throughB10D70 then calls pumpB110C0. 44183C clears dirty250 afterward. B110C0 itself returns without processing when manager28=0 or GetCurrentThreadId()!=manager0C; so the caller's dirty-clear alone is insufficient.
- Normal pool4566F0 constructs4546F0 with vtableF0DA70 and callback78DE90. Its v14=78D810; v10=454780 wrapper->78DE90. B110C0 calls v14 atB1115B before v10 atB11174. The alternate pool456800 uses F0DA88, processor78A9F0 and callback78DF80/owner.v5C; do not apply normal aggregate checks to that alternate path. Absent a query39-provided request, actor80 nonnull AND actor39E==0 selects alternate456800 at45A281..45A2B6; otherwise normal4566F0. Later trial stages can therefore use the alternate route even after a normal seed; observations must identify the actual route.
- 78D810 invokesB01990, which calls each record.v10. Ordinary record vtableF4B870.v10=78EB00: nonempty+10, A4=0 and A5=0 gate model load. Getter409F20 returns the manager; 887A30 handles cache/uncached load and writes its result through the output holder. Uncached path calls8AD740 at887BF7. The retained per-record result is+B0 (store78EBA1), not a rendered-pixel proof.
- Processor78D810 skips an ordinary record when B0 is null AND A5 is zero (78D98E..78D99E). Other accepted records can still build request48. It calls8825C0 for part insertion; nonempty aux goes through880E50->88B820. 88B820 can return false, including texture load886600 returning null; caller78DA97 does not inspect that boolean. Aggregate root absence also triggers a fallback insertion at78DB3A; if request48+8 remains null it clears48 at78DB81. No selected-hand completeness check is established by these aggregate tests.
- Normal callback78DE90 requires the appropriate request/owner types and owner state, then nonnull request48 and48+8 (78DF20..2B) before owner.v58 at78DF35. Owner0C is dereferenced before a later null check: this is not a general malformed-pointer safety claim. Early rejection skips the owner318 removal in this callback; success path removes via78D7A0 at78DF50.
- NetActor.v58=45AEC0; MyActor.v58=44A6C0 delegates to it. Base444730 assigns request48 to actor80 at4447B7 after nonnull aggregate/root checks. NetActor then copies CURRENT resident AvatarAttr34C into comparison350 via resident.v24 at45AF04..16; it does not read a request-local AvatarAttr snapshot there. This establishes the copy point, not race freedom or proof that all copied appearance values were rendered.

BUILD_PROPOSED: Extend B1h RH201/LH601 -> RH203 -> LH603 staged appearance trial with distinct submission, per-hand model and visible-result observations; retain full identity/kind/cache basis and wait for each visible stage | GT-272 equipment owner / CORE, LANE-K to assign | exact packets + ordered native observations of RH/LH model changes and unchanged opposite hand, recorded failures if absent; no pass from dirty250 alone
BUILD_IMPACT: .ni_ filename route can support fixture selection. Texture .tga->.dds/.dd_ is still OPEN; next bounded static question is the texture resolver after886600->8A21D0. Do not retry masks or reinterpret inventory slots to compensate for an unresolved resource path.
nonclaims: No native/client/server execution, pixels, legal equip class/level, authentic inventory slot, complete texture loading, concurrency ordering, original-server behavior, stats, persistence/reconnect or runtime promotion. No ServerProject, queue, lease, reference, source asset or Git writes. B1h fixtures remain composition D until native evidence.

Evidence: image14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. All ranges below are [start,end), exact file offsets and SHA256; remaining spans and every source hash are in staged/standing_b1i_manifest.json.
- resource_request: VA0078EBF0..00790766; file38DFF0; 7030bytes; SHA52d10e879f01805310d3e9f4a25bc15108e7658cacca7b362e1b1caa8c262696.
- request_process: VA0078D810..0078DE87; file38CC10; 1655bytes; SHA742523e2b08cd8a0f599d1e92b798a72c03260a6ac1aab4361b937f89e5dbe13.
- callback_normal: VA0078DE90..0078DF7D; file38D290; 237bytes; SHA530a2eee51b40a0bec6663b8037a37a5024e6fb3a698f4d24cd6a5c4b4ac8733.
- accept_netactor: VA0045AEC0..0045B1DE; file5A2C0; 798bytes; SHA18b64e835d75993fc22d317967e3be079e455b84c7046a24c622458708d9610f.
Manifest SHA5cc706132ace139b2db42012dd2439f37ad8a8916fdf7a4348ba5e6ab9f94e30; verifier standing_b1i_verify.py SHA13845167d32889be375672f37c106f03d01c6bc9c00b9eebd74bd6ae99ed3ab3; log SHA680aca61ad603f9a3a9bef9145d62c67d0edb39ada1b00850c4a8ef55e650b24. PASS42spans/29code ranges/4799instructions/13sources/285calls/622pins/6strings/7vslots/54independent anchors/3imports/4nominal path pairs; inputs checked before/after.
Actual frozen pf-adversary review /root/a6f_review: verifier exit0; no material defect. Challenged path substitution, skipped hand/texture failures, pump gating, copy direction/timing and normal/alternate scope. Added reviewer-confirmed selector condition above. Remaining texture-resolution question retained.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
