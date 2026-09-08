งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้

TO: chief / LANE-K / LANE-B / LANE-UI
STANDING A5 PARTIAL — resolve RE-110 input candidates; WIELD service branch
เวลาเริ่ม 2026-09-09T02:52:10+07:00; static ไม่มี runtime job/HEAD ที่บูต
NO_FEATURE_WAITING: คลี่จุดทดลองเก่าของ RE-110 และแยก local dispatch ของ WIELD; ไม่มีค่า attack interval ที่พิสูจน์ใหม่ให้แทนค่าชั่วคราวของเซิร์ฟเวอร์

A — exact IMAGE/DATA joins; hex VAs, end-exclusive spans/file offsets/SHA in manifest:
1. RE-110 archive result20260827_1832:44 listed450D79->450E1E and450F6E->450FE2 as unresolved observe-only producer candidates, explicitly without runtime identification. New normalized input crosswalk:
  HOTKEY5/126 MOVE_JUMP ->450CF7 ->450D79 pool -> selectorEA72/EA74 ->450E1E queue;
  HOTKEY108 GLIDEUP ->450F59 ->450F6E pool -> selectorEA75 ->450FE2 queue;
  HOTKEY71 WIELD ->451026 ->45102844BC70.
These selected literal producers are not EA7D. This narrows candidates, not a contradiction of an established auto-repeat result. It does not exclude attack-related transitive callbacks or alternative producers.

450665 calls5D0CD0 normalization;450B20 reads normalized+8, subtracts1, accepts indices<=128, selects byte4519C4 then pointer451970. Exact selected maps include both MOVE_JUMP IDs5 and126; no ID is silently dropped. DATA CONSTDATA_TH__HOTKEY rows5/126 have s_NAME MOVE_JUMP,n_KEY_2=32/96;108 GLIDEUP,n_KEY_2=88;71 WIELD,n_KEY_2=90; all n_KEY_1=0. TEXTDATA_TH__HOTKEY_TIP labels are กระโดด, เหาะเหิน / กระโดด, บิน(2) / บินขึ้น / เก็บอาวุธ. These are file defaults and normalized-ID bindings, not attained physical key settings, repeat frequency or persisted remapping. EarlierA5f key tree and controller interception can consume events before these branches; no bypass is presumed.

2. MOVE_JUMP branch450CF7 tests455300, existing actor3C0 latch, local permission byte, flags and actor10 bit200.450D39 writes actor3C0=1 BEFORE43B560 and later state/permission/pool gates. In the selected43B560-true route,449A30 andactor10 bit4 must pass;450D79 gets typedActionVital.450DDB writesEA72+2*((actor10&8)!=0 AND (actor10&08000000)==0). Reused typed pool74E620/F489EC/get74E690/node108A2BC/regC0C240/descriptor101AD74 supplies constructor/type proof. Its scalar38 can be overridden through448E30 when actor358!=0; vector3C/40=0,44=99999.0,48=0, with optional4A word.450E1E calls5DD800. Queue receipt/transport remains A5e-limited.

After that enqueue attempt,450E23 reads actor50;449240 checks compatibility with type node102ED38. A surviving pointer reaches471DF0, which writes exact float1.0 to that object's54. This is a local field writer, not an attack interval; no broad task name or callback-effect semantics is assigned here. The alternative43B560-false branch contains the actor3BC/44CC80 path already bounded inA5l; it must not be merged with the direct pool route.

At selected normalized release dispatch451261, IDs5/126 both reach451302.451307 clears actor3C0 BEFORE subsequent permission checks; later451331 may call44CC80(0,1). A stable selected MOVE_JUMP invocation can consume the latch even when later gates/allocation prevent a request, and repeated selected invocations then stop until a writer clears it. This local latch does not prove one request per physical press: key-tree interception, release delivery, other writers and indirect mutations remain open. GLIDEUP branch450F59 separately requires actor10 bit8 and writes literalEA75 at450FB6; it does not use this explicit3C0 gate in its bounded body.

3. WIELD44BC70 branch distinction: existingV128 report already binds HOTKEY71/Z to one capturedEA7E request, no reply. This round reuses that historical ceiling, adding the alternative service branch. Initial gates require global1093198, actor14 and clearactor10 bits14. After4011A0, fieldD0!=0 chooses pool44BCB7; null result returns;44BD0C writesEA7E,44BD79 calls5DD800. Target pairs from actorC8/CC andC0/C4 go to vital20/24 and28/2C. D0 is the tested service byte here; its broader connectivity meaning is not assumed.

WhenD0==0,44BD88 calls454D70, normalizes AL and addsEA7E.44BDA8 obtains a pool object, then stores actor78/7C into vital18/1C,20/24,28/2C and the computedEA7E/EA7F at30.44BE3C reads vslot+1C and44BE45 calls it. Reused ActionVital vtableF489EC+1C=7516C0: this is the same handler that resolves performer18/1C and may construct CActorTask_UseBehavior. It is a direct LOCAL handler invocation on this branch; no direct5DD800 call appears in that selected tail. This does NOT prove absence of outbound effects through handler/task callbacks. A5i's conditional macroStart->oldApproachFinish path remains applicable as a hypothesis, not an attained order.

Unlike the nonzero-D0 branch, the zero-D0 path has no explicit null-result check before dereferencing the pooled object (e.g.44BDD6). Successful allocation is required for the normal local path; allocation failure is not modeled as a clean skip. No native failure/crash was induced.

454D70 returns true immediately when initialflags&10100==0 or any initialflags20000/80000/4000/8 is set. Otherwise it calls actorvirtual3C, then40; a true return from either yields true. After those callbacks it REREADS actor10: bit400 or20000000 yields true, otherwise false. Accordingly zero-D0 selectsEA7F when predicate true,EA7E when false; it does not itself establish a toggle or the EA7F gameplay meaning. Stable-state tests enumerate all256 relevant flag combinations times4 fixed virtual-outcome pairs; separate cases allow before/after flags to differ. Callback identity/lifetime/effects are not assumed stable in the evidence claim.

4. Preserve theA5h role correction when reusing RE-110: its cited47AEE0..47B2BF is CActorTask_UseBehavior START(slot+8), not update. Actual tick is473650(slot+C). Constructor47AB96/F0EF10/get471DC0/node102ED50/regBD1230/descriptor101CEB8 and both slots/spans are reverified here. The old direct-call negative says nothing about actual tick, completion, indirect callbacks or absence of repeat. A5h/i supply the newer role/conditional-flow evidence; no old report is edited.

Search: boundary-delimited450D79/450F6E/44BCB7/44BDA8/454D70 across external,gamedata,reference_codex_attr,archive,consumed(md/py/txt/tsv) found RE-110 archive and its consumed copy only. DATA HOTKEY/HOTKEY_TIP selected rows then checked directly. Reused V128 report is evidence context, not a rerun of its capture. Prior method ceiling is not silently lifted: new dispatch/type crosswalks narrow old candidates, while native repeat/interval remains unproved. Full producer census and native ordering remain open.

Verification:29 spans(9 primary+20 reused),28 calls/28 mutants,42 pins,5 slots,2 named bindings,4 HOTKEY rows,129/128 dispatch maps;8 predicate cases+1024 stable-bit combinations,5 service/pool paths,4 latch cases+3 selected sequences;12 actual empty/missing coverage rejections. IMAGE+9 source hashes before/after. Static Python translations are not native execution.
Rerun from pf_bridge: & 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B staged\standing_a5o_verify.py
IMAGE_SHA: 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
MANIFEST_SHA: 223ef8bd47e2eaf0904faadbdd53ea57b259b4fb79e1636c678648258d38b849
VERIFY_SHA: cba193a727ad1fab5bfbcdd1b107f4088291feb187b6efe5425d9cf411b24002
LOG_SHA: c2310c31877f9b7c0f62b5c50d499ce5064f706f6d06f22f2020e5f55b2e6f02
ADVERSARY: P2 release coverage fixed with exact IDs, executed count and two rejection cases; targeted reread found no residual defect.
NEXT: A6 target panel; A5 cadence remains unproved. Reopen these scans only with a new concrete caller/trace.
No native execution or excluded-path changes.
SCOREBOARD: NONE | Standing A5 IMAGE evidence | no runtime promotion
