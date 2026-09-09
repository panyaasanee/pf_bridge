งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: สายอุปกรณ์ GT-272, CORE, LANE-B, LANE-K, chief และ Panya · จาก Codex static RE
B1l · ปิด 2026-09-09T12:44:19.227473+07:00 · IMAGE A / DATA A / composition D · NEWPROGRESS: same-model hand texture fixture

Answer: changing ordinary RH2200201 to2200202 selects the same WR_SWORD_003 model but a different map. It does NOT automatically create an A5 texture-only record. The ordinary hand producer retains constructor A5=0, so its record still passes through model loading and the B0 gate. If the existing same-path part is found,8825C0 returns true without reconstruction and the caller then applies the new texture. Clearing ordinary RH to ItemID0 instead sets A4=1 and follows removal.

ค้นชุดส่งมอบแล้ว: ไม่เจอ78E1CB/texture-only in bounded registry/fields/docs/reports/reference searches. Reuse exact B1c resource_request, B1h model-key proof, B1i record construction/load, B1j DDS preference and B1k alternate application; each reused span's SHA checked against IMAGE. No new global flag census.
ค้น gamedata แล้ว: เจอ EQUIPMENT_BASE rows201/202. Select only the existing RH201 model family; reparse the original PCZ table to its exact end, then compare these two rows' seven selected columns with the TSV. Current coverage source hash unchanged from B1k: equip_unequip and appearance_and_avatar_binding remain in_progress. Full search/source record is pinned.

IMAGE producer facts:
- Both fresh/reused record pool78B0E0 call ctor78A590, which zeros A4 and A5 at78A63F/645 (EBX zero78A5BA). Ordinary RH assembly78FAFE onward sets slot0B, model path/node/aux and ItemID+A8; A4=(ItemID==0) at78FC68/6A/6D. LH ordinary slot0C uses78FE67/69/6C. A5 is not changed by these bounded hand assembly paths.
- In comparison mode, RH current fullID atresident54 is compared to old54 at78FA5E. A changed ID enters construction via78FA61 even if the derived model basename is identical. The selected old/new equiptype1 avoids special RHtype10/8/20 branches and their LH rewrite effects (B1h). This is not a claim about every equiptype or a component-provided request override.
- The explicit A5=1 stores found in THIS resource_request function belong to other part paths: 78F577 targets slot3 (slot store78F4F1), after the +34 part path did not build a record and the +38 path is selected;790317 targets slot6 or7 (79027D/280/288). The latter derives its key from+50 and carries additional mode/presence gates. These offsets are recorded per AvatarAttr consumer, without guessing body/job semantics. Do not transplant A5 onto RH/LH simply because it is called texture-only downstream. This bounded statement does not claim that no other function or runtime participant can write A5.
- 78EB00 requires nonempty model path, A4=0 and A5=0 before887A30 load. In the alternate application, ordinary A5=0 additionally requires nonnullB0 before calling8825C0. If B0 is null, B1k's removal path applies even for same-model/different-map intent.
- With B0 nonnull and an existing slot whose model path compares equal by _wcsicmp,8825C0 returns true at8827A0 without constructing a new part. 78E2EC then invokes880E50 with the new aux path. Its boolean is ignored; a true insertion/same-path return is not a texture success token. DDS preference remains conditional as in B1j.
- For RH0 after old type1, A4=1 suppresses record model loading; alternate78E050 takes its A4 removal branch. This is an appearance-field clear proposal, not proof of a server inventory unequip transaction or legal equipment slot.

DATA A, original EQUIPMENT_BASE code22 (B1h producer/registration proof reused):
| fullID | type | model | map |
|---|---|---|---|
|2200201|1|WR_SWORD_003|WR_SWORD_003_002|
|2200202|1|WR_SWORD_003|WR_SWORD_003_003|
Both n_TAG_LOOT4168 and n_EQUIPSLOT16384. The latter is a table bitmask, not an absolute inventory slot. New row202 decoded range[5252766,5253046), SHA7396a4ba4cd93dbcd0de2e569dec8522a2adaf2b0bdfe27514206d97b299e520. Raw PCZ SHA496b5c7b5a7f4c1ab5e343937ca7278b3db5b4501250caa7da47f22dc2c9c3f8; decoded8443000bytes SHA496dfb2ef2cf517482a7b426c9dd5edf0278564fe11195b96f36df90607f0d2d. All974 rows traversed, only201/202 selected; no full data table republished.
Local .ni_ and both .dd_ files exist with exact hashes. New wr_sword_003_003.dd_:25499bytes SHA57ff840005b6792ee3040ee95d02890f391eb5ea16a3d20ab0c754b2b4de1ed7. No asset decoded for appearance or altered. Filename/type/map facts do not prove that the two textures have distinguishable visible colors.

BUILD_PROPOSED: Extend B1h staged appearance trial with RH2200201->2200202 using mask400, then RH0 using mask400, holding LH2200601 and the prior identity/kind/cache basis; wait and observe each stage | GT-272 equipment owner / CORE, LANE-K to assign | actual route and record flags/B0 when instrumented, exact packets, visible RH texture/model/clear observations with unchanged LH; no pass based solely on flags/callback/comparison350
BUILD_IMPACT: A same-model map change exercises the ordinary model-load/same-path-insertion/texture lane, not necessarily A5. A4 clear separates appearance removal from equipment-bag mutation. Fixture and clear sequence remain composition D. Native validation must report ambiguous texture appearance as such, not infer visual difference from filenames.
nonclaims: No native/client/server execution, observed texture difference/removal, all A5 producers, authenticity/legal item class/level, absolute bag/equipment slot, inventory state transition, stats, automatic retry, persistence/reconnect or runtime promotion. No queue, lease, ServerProject, reference, asset or Git changes.

Evidence: image14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. Ranges [start,end), exact file offset/SHA; full inventory staged/standing_b1l_manifest.json.
- resource_request: VA0078EBF0..00790766; file38DFF0; 7030bytes; SHA52d10e879f01805310d3e9f4a25bc15108e7658cacca7b362e1b1caa8c262696.
- record_ctor: VA0078A590..0078A698; file389990; 264bytes; SHA25a6b24351bfff25ba0b0227091f59c99aae137ee55cde850bd409213b7e7898.
- record_load: VA0078EB00..0078EBEE; file38DF00; 238bytes; SHA7702ca3191a7570a514a444736c1a1ac486cba5da215cfff9f8a9621477fed66.
Manifest SHA087d826cfd345216ebdacdec886eea15ce4ad07f00ee233ef01591d326d33d4a; verifier standing_b1l_verify.py SHA90355d64327bad1b7ee828b7acb0d7295258e3bf02876fd286f8d404c8540677; log SHA3fa317374b2854796a00db07e0bda4627310d1380ab99baf4d6a20cd2798c13a. PASS8fullspans/2894instructions/12sources/162calls/440pins/30independent anchors/2bounded A5 sites/2original row fixtures/3local resources. Inputs checked before/after.
ADVERSARY: a6f_review completed frozen review; verifier exit0. No material defect found in flag retention, full-ID comparison, same-path B0 prerequisite, RH0 clear or original row fixtures. Visible distinguishability of the two textures remains a native-test question.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
