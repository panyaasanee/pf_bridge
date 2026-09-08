งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้

ADDRESSEE: LANE-K / chief; LANE-B consumer
STANDING A5 continuation — retained controller frame callbacks. PARTIAL; new static progress, not a whole-client method ceiling.
SCOREBOARD: NONE | ผู้เล่นคลิกโจมตีครั้งเดียวแล้วตีซ้ำจนสั่งหยุด | IMAGE only; no new gameplay/runtime credit.

BUILD_PROPOSED: bind this controller evidence into the existing autoattack/cadence work and GT-224 before selecting client-driven versus server-driven repetition | LANE-B, LANE-K links existing tickets | one physical gesture, >=3 timed attack submissions/results, then explicit stop/target-loss/death cases; record whether further client input or server response caused each submission

Result A / PROVEN_EXACT, bounded: finding a retained controller or timer does not establish autonomous attack submission. The concrete frame slots below separate empty callbacks, an unresolved indirect dispatcher, and a target-distance task selector. No newly proved cycle reaches a second EA7D submission.

1. Ownership and frame seam. 449110 reads CMyActor+3DC, calls old object's vslot0 with argument1 when non-null, then stores the incoming pointer. 44E76A..44E786 loads the retained pointer and dispatches vslot+4 with the frame argument. This is separate from the actor task at +50 in the prior A5 letter. Per-class keys: CMyActor@0x3DC.4#W and #R; controller@452960@0x8.8#W/#R for its retained identity. No universal offset semantics.

2. Three admitted constructor/install paths bind empty frame callbacks:
   - 478C17 -> ctor451D80 writes vtable F0D98C; 478C2B ->449110.
   - 474629 -> ctor452680 writes F0D9B0; 474641 ->449110.
   - inline61A3A5 writes F32F1C; 61A3B6 ->449110.
   All three tables' +4 entries are 73D360, whose entire body is ret4. Thus these exact frame callbacks cannot themselves submit or schedule an attack. This does not exclude their input callbacks, installation side effects, another controller, or later replacement. Installation is conditional on reaching the shown path and successful allocation; this is not a gesture-to-controller attribution.

3. Two other controllers remain OPEN. ctor vtable writes453039/F0D998 and453737/F0D9A4 bind frame452140 and452470. They accumulate their argument at controller+2C or+24, then, when controller+20 is non-null, call8AC090 with accumulated value and1. 8AC090 is NOT a harmless no-op: it invokes indirect slots on global108D1F4 (+0C/+10), the receiver (+60), and optionally receiver+1C (+A0). Actual receiver classes and transitive effects remain unresolved. No all-path negative from linear disassembly.

4. A distinct target-distance controller is now bound end to end as far as task construction. ctor452960 writes F0D9C8 and copies its qword argument into+8/+C; installs522210/522228,522580/522598,627F7E/627F99. The three shown install blocks OR local actor+70 with1000. Vslot+4 is453FE0. On an admitted frame it:
   - requires local actor, reads actor+10 mask400; that state or missing resolved target leads to clearing actor+70 bit1000;
   - accumulates the frame argument in SHARED global103312C, compares with the exact float0.5 atF0B00C; ordered accumulated value below0.5 returns without the target task path;
   - loads retained+8/+C, calls402A20 then446170, obtains target position via43BCE0, and calls451EA0;
   - resolves the signed return through byte table4542A4 and dword table454290. Exact mapping: -10 ->4540DA(clear bit); -9 ->45426F(reset); -1 ->4540EB(Idle construction); 0 ->4541AC(ActorMove construction); 1 ->454188(clear bit and message call). Default also reaches reset45426F. Do not swap return0 and1.
   Classifier451EA0 computes squared positional distance. For ordinary finite ordered values: distance squared <= first cached threshold returns-1; only if that test fails, distance squared < second returns0, otherwise1. No ordering of the two thresholds is assumed. Initialization uses globals10337DC/E0 and caches1033124/20; their authentic values/domain are not established here.
   - Idle constructors45411E/454164 call4724D0 and pass result to484390. Move constructors454201/454252 call472A20 and pass result to4843C0. Named bindings are exact: ctor -> vtableF0EEC8/F0F090 -> getter471BA0/472B00 -> type node102EDA4/102ED80 -> registrationBD1070/BD1130 -> descriptors101CDC4/101CE28 naming CActorTask_Idle / CActorTask_ActorMove.
   - ordinary dispatched completion resets shared103312C to0 at45426F; early returns do not all reset it. This is NOT a per-target/per-instance attack interval, and0.5 has not been promoted to authentic attack seconds. Task admission, promotion, execution and eventual network effects are not proved merely by these constructors.

5. Another positive distinction: ctor452790 writes F0D9BC; frame452830 sets local+3A8 bit1 and calls44DCC0, or clears local+70 bit800 when actor+10 mask400 is set. This is a separate sustained state-update path. Its complete downstream movement/action effects and input ownership are outside this result.

Search before derivation: external/ and gamedata/ bounded searches for attack repetition/cadence and the controller addresses yielded no direct answer; expanded mechanism/address search found the existing MovementAttr->ActorMove binding in PF_ATTR_FIELD_SEMANTICS.tsv / PF_A2_ATTR_FIELD_DELTA.tsv. One relevant reference row reused: MovementAttr@0x38.1#R:b0x00000004, evidence_key82d4a1eaf5d391311f3dd7847e6a18912ac46c1c22db54e23731bee532a8ca34. All8 supporting spans rechecked (100% of the selected row), preserving its UNKNOWN concrete-Attr-owner ceiling. A gamedata placement hex substring match was unrelated; lexical absence is not absence of a client mechanism. Earlier A5 sources/search are reused by immutable result SHA.

Reproduce from pf_bridge (installed Python; no package installation):
`& 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B .\staged\standing_a5b_verify.py`
PASS:35 primary spans +8 reused support spans,29 direct calls,32 opcode pins,4 branches,7 frame-vtable slots,5 signed table cases,2 named task bindings,3 actual empty-coverage rejection checks. This verifies static byte/dataflow anchors, not native execution. Verifier contains exact coverage counts/sets. Adversary caught an unguarded descriptor-name loop; exact pair-set/count and empty-list rejection now protect it. All5 source hashes and image rechecked before/after.
Image SHA256:9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623.
Manifest staged/standing_a5b_manifest.json SHA256:cd4b502fb2573dcf04c0e5923356ef385e74766c640d073a90f2161e1ae8efdf; includes VA/end/SHA for all spans and file offsets for the35 primary spans; all8 support offsets are derived and logged by the verifier. Key spans: frame453FE0..45428F, classifier451EA0..452010, empty73D360..73D363, dispatcher8AC090..8AC0FA. Full hashes/reproduction output are in staged/standing_a5b_verify_20260909.log.

NEXT / bounded open proofs: (a) resolve concrete+20 receivers and callback effects behind8AC090; (b) independently bind the physical attack gesture to any retained controller, preserving lifetime after first EA7D (prior paths44ED28/44E978 clear+3DC); (c) prove a reachable second attack producer with retained selector/target and stop predicates. No measured global static ceiling. Neither idle/move names nor timers prove attack repetition; no authentic cadence, server ACK policy, runtime pixels, complete controller/writer census or persistence claim.
