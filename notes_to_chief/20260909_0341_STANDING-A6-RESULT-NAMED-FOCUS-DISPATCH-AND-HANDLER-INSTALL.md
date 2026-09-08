งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้

TO: chief / LANE-K / LANE-UI / LANE-B
STANDING A6 PARTIAL — named focus delivery, handler installation and pre-notice show request
START 2026-09-09T03:29:44+07:00; no runtime job.
NO_FEATURE_WAITING: IMAGE/DATA dispatch proof; no protocol change proposed.

A — exact IMAGE/DATA. VA hex, spans end-exclusive/file offsets/SHA in manifest. Main result: compiled named-send -> window.v210 -> installed handler.v30 is inline, conditional on the reached object and ordinary callback returns. A nonnull AA0710 result is a window pointer, not delivery acknowledgement. No live enrollment claim.

1. Full AA0710..AA0799 first calls8946C0: null/empty UTF-16 key returns null before lookup (GM-IMG-007 prior proof rechecked, not new). A9EF00 walks the manager list and compares requested name against object+14's string; it returns a matching object or null. Existing object's v1FC is queried. Missing object OR v1FC true callsA9E080(name,1), thenAA05C0(result). A9E080 calls manager+8C.v10(name), checks returned object's v30, and applies additional initialization/cleanup gates; creation can return null. No claim that a name guarantees a valid resource.

For nonnull selected window, AA0710 executes vF4(arg3) atAA0772, A9E020(arg4) atAA077B, THEN v210(message arg2) atAA078F. A9E020 copies four words into window12CC..12D8 with reference handling for the last member. CHitResult750C3E supplies name Main_Panel_Target_Enemy_New, message,1,1090958 on manager1090708. The show request therefore precedes focus-notice processing. Return atAA0791 is the selected window pointer regardless of the ignored callback return value. Ordinary returns/valid memory required.

2. UIWindow constructorAA2010 installsF8A038 and initializes1294 null. v0=40B380 tails toAA1740 ->type node1090900; registrationC1AAF0 names UIWindow at101AC60. Its v210=AA27D0. That full body calls window.v234(message) FIRST, then REREADS window1294; if nonnull, calls that handler's v30(message) atAA27F3 with the same pointer. No queue is introduced in these two bounded call bodies. Transitive scheduling remains open.

BigUIStandardWindow constructor prefixA91E20 callsAA2010 then installsF87928. GetterA918D0/node10903A8, registrationC1A400/descriptor101F15C prove this class; parent10903B4 is BigUIBaseWindow (getterA918C0, registrationC1A3C0, descriptor101AC94), whose registration parent comes fromAA1740. F87928 also binds210=AA27D0, F4=405E30,1FC=402450,234=73D360. For these pinned UIWindow/StandardWindow tables, v234 is exactly RET4, not an unknown callback. Other derived overrides and runtime object selection remain open.

405E30 compares requested low-byte state to vF0 result; on difference it writes window7C then invokes CURRENT1294.v40 if nonnull. A6a Enemy/Friendly handler tables bind40=A8F9A0. Thus handler callbacks can run BEFORE the later notice; their transitive effects were not excluded. 402450 returns window12A0 byte. No claim that setting7C alone proves visible/rendered output.

3. Installation seam A8F4D0..A8F519 releases an old1294 and clears it, writes new_handler10=window (no new-handler-null guard), installs window1294=new_handler and adds its reference. A91070..A91356 resource creation reaches this seam atA912D7 only after resource/window creation gates and a nonnull handler returned by creator+50.v10(requested name). A912DC rejects a still-missing handler by destroying the created window when creator54 is false. Existing/cached/special-resource paths have separate gates; no blanket mandatory-handler assertion for every returned window.

Initializer subpath40859B..408627 constructs handler factory F09C60, passes it as argument2 to59E090(path,factory,0,1), and stores the resulting resource creator at1090794, which is manager1090708+8C.59E090 forwards toA914F0 then installsF2BD94; A914F0 stores argument2 at creator50 and the two flags at54/55. F2BD94+10=A91070; F09C60+10=5D76C0. This proves the compiled installation chain on that initialization path; it does not show the path executed in a particular run.

Full handler factory5D76C0..5DA823 has selected name comparisons: Friendly branch5D846F usesF0D268 Main_Panel_Target_Friendly_New, allocates98 bytes, calls520320 at5D84E5; Enemy branch5D84EF usesF0D2A8 Main_Panel_Target_Enemy_New, allocatesA8 bytes, calls51DE80 at5D8565. Allocation failure returns null; successful selected branches return their constructor result through5DA80D. A6a typed constructors/tables bind v30=51ECC0 for both. No live factory call or claim for other names.

4. DATA exact files GameClient/Data/GUI/Model/Main_Panel_Target_{Enemy,Friendly}_New.model each have one SourceData root of type BigUIBaseWindow with matching ID and unique LABEL_NAME/BUFFERVIEW_ONBUFF/BUFFERVIEW_DEBUFF controls. This establishes declared model identity/type, not that either file loaded or that the loader chose a particular concrete subclass. BigUIStandardWindow is a compiled compatible subtype; its actual model-instantiation choice is not established here.

5. Periodic linkage: UIWindow v34=AA2840 invokes window.v230, then current1294.v2C with the two float arguments, thenAB3D60. BigUIStandardWindow overrides v34=A918E0; it first updates five embedded subobjects then callsAA2840 atA919A6. A6a tables bind v2C to Enemy51E3B0 and Friendly51EBC0, the shared-threshold routines proved in A6c. Actual update enrollment, delta units and frequency remain unmeasured.

D — conditional consequences: with these compiled dispatch tables and the typed handler installed at the final read, CHitResult focus send reaches51ECC0 inline before AA0710 returns. If a callback detaches or replaces1294 first, delivery changes or is skipped. Even a nonnull return can occur with no handler call. On the reached Enemy notice, name validation may fail before its own HP/show/identity-commit steps, but AA0710's earlier vF4(1) request is already issued; there is no automatic undo in that early-return branch. No final-visible-state assertion.

The composed route now extends A6c's conditional CHitResult -> focus -> name-refresh ->51E600/5DD800 attempt. It is a concrete compiled alternative to an unrestricted 'CHitResult subtree cannot send TargetVital' claim. Runtime arrival, factory/resource success, matching identity, name/host gates and queue/transport success remain separate; this does not reinterpret the historical GT-038 HIT_REACTION capture as causal or change its observed number-display result.

Search: external0/gamedata0/reference9/archive23/consumed8 bounded rg hits (standing_a6d_search_20260909.log). Prior GM dispatcher empty-key gate and RE-104/108 scope reused. Direct DATA files inspected separately. No universal absence claim from search counts.
Validation:48 spans34primary14reuse;32 calls+1tail,69 pins,101 mutation traps,20 slots,5 named types,3 keys,2 XML models,6 full call inventories,9 conditional dispatch cases,2 consequence examples,14 guards. Exact executed counts enforced; IMAGE+9 source hashes unchanged. No native emulation/execution.
REVIEW: independent read-only review found no actionable defect in the frozen scope; no native execution or independent disassembly. Live loader subclass/enrollment remains open.
SCOREBOARD: NONE | Standing A6 IMAGE evidence | no runtime promotion
NEXT: remaining inbound target-clear/name invalidation and a finite A6 boundary; then B1 equipment. No game/server/DB/ServerProject/lease/Git/queue/reference/model edits.
Rerun (PowerShell): & 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B '..\pf_bridge\staged\standing_a6d_verify.py'
IMAGE_SHA: 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
MANIFEST_SHA: 82c11ada5138522c74f7aae6a95d8161e426d3846d3186b8254754b31fbaa4a6
VERIFY_SHA: f5a5029275ef06fe7a290d6af4e96b5d45a5d57d0fe2ffbe89a7788b61908130
LOG_SHA: ab36ab7a061f641c63300ea3c118ca5e6c28a94ca7e94a966c518875b4cf0903
