งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้
ADDRESSEE: สายอุปกรณ์ GT-272, CORE, LANE-B, LANE-K, chief และ Panya · จาก Codex static RE
B1k · ปิด 2026-09-09T12:37:48.861458+07:00 · IMAGE A / composition D · NEWPROGRESS: alternate hand replacement failure gates

Answer: the alternate request edits the existing actor80 model, rather than requiring a newly assembled request48 root. CURRENT resident AvatarAttr34C is copied into comparison350 BEFORE those part edits. For an ordinary hand record, a null loaded-model pointer or failed insertion reaches slot removal. Therefore comparison350, callback completion and the local changed-record counter cannot certify successful hand replacement.

ค้นชุดส่งมอบแล้ว: ไม่เจอ78A9F0/45B400 in protocol registry/serializer fields or bounded reference/external/orders search. Reuse B1i's verified alternate selection/vtables/record loader and B1j's conditional DDS preference; source manifests pinned.
ค้น gamedata แล้ว: เจอ EQUIPMENT_BASE index/columns; four B1h hand fixtures remain references, no new table/asset decoding. FUNCTIONAL_COVERAGE.json still has equip_unequip and appearance_and_avatar_binding in_progress; bounded docs/reports search found no result for these two entrypoints. Full search log: staged/standing_b1k_search.log.

Route (IMAGE A):
- Unless query39 supplies a request, actor80 nonnull AND actor39E==0 selects456800; otherwise4566F0 (B1i). Alternate vtF0DA88.v14=78A9F0; .v10=454850->78DF80. The pump calls .v14 before .v10.
- 78A9F0 rejects the typed-owner70 bit100000 path; otherwise callsB01990 at78AA27 to run record.v10, then app+20.vB8. It does not construct an aggregate48. A null/untyped owner does not cause this processor's early rejection, but the later78DF80 callback requires a valid typed owner with bit100000 clear before owner.v5C. Do not conflate these gates.
- Both NetActor and MyActor v5C resolve45B400. At45B444..45B45A it copies resident34C.v24 into350. It then invokes owner.v54 and, via getter459D90, calls78E050(owner,request) at45B46E. This copy precedes part application and is not conditioned on its success.
- 78E050 requires nonnull actor, request, actor80 and actor80+8. It iterates request records against that EXISTING actor80. It does not substitute request48 as the base model. Failure of these initial conditions returns after the earlier comparison copy already happened.

Per ordinary part record, after typed-record validation (slot+9C, flagsA4/A5, loaded modelB0):
| branch, in priority order | effect in78E050 |
|---|---|
|A4 nonzero|call actor-related cleanup442890, then slot removal881BA0; increment local counter|
|A4 zero, A5 nonzero|call880E50 texture update; ignore its boolean; increment counter|
|A4=A5=0, B0 null|call881BA0 for this slot; increment counter|
|A4=A5=0, B0 nonnull,8825C0 false|jump78E2C1->78E1B4, call881BA0; increment counter|
|A4=A5=0, B0 nonnull,8825C0 true|call880E50; ignore texture boolean; then442890 and443C60(slot,ItemID+A8); increment counter|
Counter at stack+18 later gates root-update calls; removal and texture failure can increment it, so it is not a successful-model count. The loop continues across records; no rollback of earlier part effects appears in this function. That is a bounded function statement, not a global transaction guarantee.
RH slot0B additionally clears270E/270F related entries before the A4/A5/B0 tests (78E131..196). The selected B1h ordinary fixtures avoid their special creation branches; do not infer that all hand types have identical side effects. Calls442890/443C60 are actor-related attachment/effect work, not an inventory bag/slot mutation proof.

Why removal and insertion are meaningful, but still not pixels:
- For ordinary hand slots0B/0C,881BA0 uses880DB0 in model+0C, calls part.v10, then key erase881850->881440. Its per-node path8808B0 releases/frees the node and decrements count at880B61/62; full-range path calls880610 and resets head/count at881494..AE. Special270E bypasses this ordinary path. If slot absent,881BA0 returns false. Callers above do not turn that into a visual-success observation.
- Ordinary8825C0 validates nonempty model path and nonnegative slot. Existing slot with the same model path by _wcsicmp returns true without replacing the part. Otherwise, for a nonempty attachment-node name (the hand fixtures), it calls87FB30. That helper needs a loaded model/root and a matching typed attachment node; missing node at87FCBA/BC returns null. More clone/resource gates exist; nonnullB0 alone is insufficient.
- If part construction returns null,8825C0 returns false. Its caller then removes the old slot as shown above. If construction succeeds,8825C0 removes the old slot at8827EE and inserts the new part into model+0C via880520 at882873, then returns true. Same-path short-circuit and successful insertion are distinct true outcomes.
- Texture handling remains separate: both A5-only and post-insertion880E50 booleans are ignored. B1j provides conditional .tga->.dds->.dd_ selection, not a decoder or rendered-texture pass.

BUILD_PROPOSED: Extend the existing B1h staged hand trial with route-specific observations of recordA4/A5/B0,8825C0 result and resulting slot presence; pair those with visible right/left-hand changes | GT-272 equipment owner / CORE, LANE-K to assign | exact packet stage and observed alternate route; failure classification for missing model vs failed attachment vs texture failure, plus native screenshots/observations; keep instrumented grade C separate from uninstrumented B
BUILD_IMPACT: Do not mark success from comparison350 advancing or callback/count completion. A failed model replacement can remove the previous hand part. Any recovery/retry strategy needs its own proof; this letter does not assert that resending the same mask will retry or repair it. Next bounded B1 question: producer conditions for A4 clear versus A5 texture-only records, tied to a concrete same-model/different-map fixture; avoid a broad renderer audit.
nonclaims: No native/client/server execution, observed disappearance, original-server behavior, all attachment types, actual texture decode/pixels, concurrency ordering, global atomicity/automatic retry, inventory legality/absolute slot, stats, persistence/reconnect or runtime promotion. No changes to ServerProject, assets, queue, lease, reference files or Git.

Evidence: image14759424bytes SHA9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623. All ranges [start,end), exact file offset/SHA; remaining spans/source hashes in staged/standing_b1k_manifest.json.
- alternate_process: VA0078A9F0..0078AA43; file389DF0; 83bytes; SHAdbe20a940589c2822027a5d449bc0e1ff9d6f554f706c85764e71fa6d0e1ed8e.
- alternate_owner: VA0045B400..0045B767; file5A800; 871bytes; SHAf5499084644023e7e3a6773afc8c22fb4fda037ae7874359fa4430789c68a932.
- inplace_parts: VA0078E050..0078E534; file38D450; 1252bytes; SHA643a753e81de908258db5845207eebab8ee130ef32ff6353343088129e83ca7d.
- part_insert: VA008825C0..008829A4; file4819C0; 996bytes; SHA849785506584e46e89bef5696a7ecb6f1852803cc5258527c78c0f1be85e555f.
Manifest SHA1386a0b2a0ccb4c1f72749fe2b39e8c2e1eb186e4102c33901f951e289a884ca; verifier standing_b1k_verify.py SHA64a501684236a9d399e387bff9caaa4cbad73664a17fd6790b4d9cc14f494660; log SHA9f580f0ecd457ca782a462b3c0e0d522324f565afa7cf72c2df01d04c5114840. PASS26spans/22code ranges/2736instructions/10sources/176calls/356pins/4vslots/53independent anchors/1import/7branch controls; inputs checked before/after. Python branch controls are abstraction, not client execution.
Actual frozen pf-adversary review /root/a6f_review: verifier exit0; ordinary-hand claims held. Applied its two qualifications: per-node versus full-range erase, and special270E excluded.
SCOREBOARD: NONE | Standing B1 IMAGE evidence | no runtime promotion
