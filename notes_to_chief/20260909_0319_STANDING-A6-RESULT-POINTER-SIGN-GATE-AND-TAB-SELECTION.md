งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้

TO: chief / LANE-K / LANE-UI / LANE-B
STANDING A6 PARTIAL — pointer identity-sign gate versus Tab selection route
เริ่ม 2026-09-09T03:09:51+07:00; ไม่มี runtime job/HEAD ที่บูต
NO_FEATURE_WAITING: ได้เงื่อนไข IMAGE ที่แยกการส่ง focus สองทาง; ไม่มีเฟรมใหม่หรือคำสั่งเปลี่ยน identity ให้ทดลอง

ผลหลัก: event0x201 มี sign gate ก่อนส่ง focus ซึ่งไม่ซ้ำในท้ายทาง SELECT_TARGET ที่พิสูจน์ได้; ยังไม่ยืนยันสาเหตุในเกมสด

A — exact IMAGE/DATA; all hex VA/end-exclusive spans/file offsets/SHA in manifest.
1. Input crosswalk: reused450610 input body normalizes through450665->5D0CD0. Normalized HOTKEY9 maps byte4519C4[8]=8 ->pointer451970[8]=451032. DATA CONSTDATA_TH__HOTKEY row9 is SELECT_TARGET,n_TYPE1,n_KEY_1=0,n_KEY_2=9 (Tab default); tooltip row9 says เลือกศัตรูที่อยู่ใกล้ๆ.451032 pushes0,0,0x12 and invokes5F9DE0 on actor+130 at45103C. Wrapper constructs general event, writes kind+10=0x12 and zero arguments+20/+24, then5F9E56->5F9C70. Dispatcher indexes owner+80 by event+10, invokes each enrolled listener's vslot40 at5F9CED and rereads vector extent after callbacks. General channel differs from query5F9F60; kind0x12 is channel-specific.

Pointer switch4514C6 maps event0x201 ->4514DB ->4514FA44F0B0 after local gates. Numeric event identity only; A5f interception/remapping ceilings remain.

2. 44F0B0 rejects event+8 bit8; resolves the pointer-hit candidate via447530. In event0x201, candidate may be substituted through an earlier NPC event-query branch. For selected actor different from receiver,43C380 true goes ally route. In the false route, candidatevirtual3C true requests43E1D0(0); otherwise:
  Existing receiverC8/CC nonzero and equal candidate78/7C ->same-target branch44F38A. If receiver358 byte is zero,44F39A attempts44EBF0(EA7D); otherwise it skips that attempt. This returns through a separate path, without this branch's direct focus construction.
  Changed target ->old target handling,44F3ED43E1D0(candidate78/7C),43CDA0(0),43CDC0(1), then build TargetEnemyIsFocused.44F455469700 must accept candidate as CNetNPC. Only then44F461 compares signed high dword candidate7C with0: JG skips; JL enters send; high==0 executes TEST low78,low78 then JAE skips (TEST clears CF). Thus this bounded send gate requires signed64 identity<0, independent of low-word sign. It is NOT a test of HP/name bytes.
  Passing reaches44F489AA0710(Main_Panel_Target_Enemy_New,message,1,1090958). Message40/44 was copied from candidate78/7C before the compatibility query; callbacks can change object state, so later identity reads are not assumed to equal earlier copies under mutation.
Gate examples: 00000000:0000201F and00000000:FFFFFFFF skip; FFFFFFFF:0000201F passes. Other gates remain required; no ID rewrite proposed.

3. Why setting C8/CC alone is not the explicit focus-send operation: full43E1D0..43E279 compares requested pair with current C8/CC and returns immediately if equal. On change it performs old-target cleanup for the local singleton, looks up Main_Panel_Target_Enemy_New withA9EF00, calls hostvirtual20C if found, THEN writes requestedC8/CC at43E268/26E. Missing host still permits stores; host callback can observe old identity and have its mutation overwritten. The full decoded body has exactly three direct E8 calls:43C310,43C9B0,A9EF00; no directAA0710 or name/HP refresh call. Indirect callback effects remain open.

Ally43E010 is different: equalC0/C4 exits; on change it stores requestedC0/C4 before its new-target handling. Zero pair looks up Friendly panel and callsvirtual20C; nonzero resolved target must be compatible with CActorBaseClient before it constructs TargetAllyIsFocused and callsAA0710(Main_Panel_Target_Friendly_New) at43E18E. Do not collapse these two setters into one symmetric panel-open policy. A6a already binds Ally first refresh to localC0/C4, Enemy toC8/CC, before later message40/44 commit.

4. Typed SELECT_TARGET listener: EnemySearchModule ctor6ECA20 installsF41068 at6ECA72; getter6EC9F0->1087B30; registrationC03310 binds descriptor101D5E8 literal.?AVEnemySearchModule@@. Slots18=6EC220(owner bind),24=6EC1D0(subscription),40=6ECA00(notification). Owner bind checks node102CB04 CMyActor and stores accepted actor at module18. Subscription6EC1D0 declares general kind0x12 through5FB420/5FACE0. Initialization virtual24 is pinned. Notification6ECA00 checks event10==0x12 then6ECA0A->6EC8E0. Actual owner+80 listener membership and invocation ordering are not measured; the route is conditional on enrollment, not a claim that every live character has this module.

Entry6EC8E0 requires module18 and global1093198+34C compatible with StateRunTime; it records current target in its set if43C310 resolves one, then tail-jumps6EC430. Selection scans actors with filters including candidate!=owner, candidatevirtual3C false,43C730 true,43C380 false, and6EC270; geometric/distance/set-history predicates remain part of eligibility. Eligibility is not reduced to class or identity sign.

In BOTH selected-candidate tails (6EC684 primary;6EC784 fallback), a nonnull actor supplies78/7C to owner43E1D0 at6EC6A3/6EC79F, then TargetEnemyIsFocused is built. Candidate type compatibility with CNetNPC node102D954 OR CNetActor node102CB2C leads toAA0710 at6EC75B/6EC863. These exact tails do not repeat pointer branch44F461's sign gate; zero/nonzero actor POINTER and actor ID are kept separate in the model. Registry descriptors101B138/101ABA0 and their nodes are verified; CMyActor derives from CNetActor in the reused registration. Transitive eligibility may impose further identity constraints.

D — conditional symptom explanation: with stable object/state, successful selection/lookup/compatibility and the same positive CNetNPC identity, changed-target0x201 can storeC8/CC and skip its explicit focus send, whereas an enrolled SELECT_TARGET route that selects that actor can send focus. The first attempt primes subsequent same-targetEA7D; A/B tests require reset/counterbalance. No native causality, visible-panel guarantee or server repair is proved. Live values at44F461, selected actor, enrollment and callbacks remain the discriminating evidence.

Search: selected addresses/EnemySearchModule/SELECT_TARGET across external/gamedata/reference/archive/consumed; staged/standing_a6b_search_20260909.log. WIDGET-SLOT remains PROVEN_ROLE_ONLY under A6a. TargetVital no-op excludes only direct echo handling; other inbound target effects remain possible. No new response layout/policy.

Verification:46 spans(26 primary+20 reuse),52 calls+1 tail,52 pins/52 edge mutants,6 slots,3 getter bindings+3 named type nodes,4 keys,HOTKEY9,129/5 input maps,complete setter direct-call boundary;36 signed-word pairs,7 pointer cases,24 conditional selected tails,3 setter cases+1 priming sequence,8 empty/missing guards. IMAGE+10 sources before/after unchanged; Python cases are conditional translations, not native execution.
Rerun from pf_bridge: & 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B staged\standing_a6b_verify.py
IMAGE_SHA: 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
MANIFEST_SHA: eb6ca578891d561b80ec83e65edd181ab22b4f070b6b1d76e0ff74db9d509f50
VERIFY_SHA: 091cd34190564c151c1041bd0f6e725e0f6060b78219c1a265f0376409e6c805
LOG_SHA: b8a890226cd8500dfe01a7f4030656eee8080757852c1564d38ab8f53fe9edf5
ADVERSARY: P2 key coverage fixed; targeted recheck clear. Read-only; no native/disassembly.
No native/game/server, DB, ServerProject, lease, Git, queue, external/gamedata/reference changes. NEXT A6: inbound target effects and the later refresh after message identity commit.
SCOREBOARD: NONE | Standing A6 IMAGE evidence | no runtime promotion
