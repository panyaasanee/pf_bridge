งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้

ADDRESSEE: LANE-K / chief; LANE-B consumer
STANDING A5 — clearing/replacing an approach task can reach its attack-producing finish. PARTIAL; NEW static progress, no whole-client method ceiling.
SCOREBOARD: NONE | ผู้เล่นหยุดหรือเปลี่ยนการกระทำแล้วไม่ตีเป้าหมายเก่าต่อ | IMAGE only; no runtime pass.
BUILD_PROPOSED: carry explicit stop/replacement semantics into existing autoattack work and GT-224 | LANE-B; LANE-K links existing work | record current actor+30 and pending actor+34, task flags, retained/wire targets and outbound submissions across approach, replacement, clear and target loss; distinguish already queued requests from new producer invocations

A / PROVEN_EXACT, bounded: queue clear does not merely discard the current task. For a non-null current pointer it calls the finish wrapper without requiring task bit8. A fresh approach task can consequently reach its EA7D-producing finish if the finish gates pass. Replacement can also reach finish before a positive frame-time gate. Neither path is proof of sustained automatic attacks.

1. Clear4A0970..4A09BE reads queue+10. If non-null,4A097A calls4A0860. The complete wrapper tests task+10 bit10; if clear, it sets10 and8 BEFORE vslot+10. Thus a current task with initial flags80000006 need not have been marked completed by its tick. Existingbit10 still suppresses dispatch.

   Afterward clear re-reads queue+10, invokes destructor vslot+4 on the current non-null pointer, and zeros the slot. Reentrant replacement can change which pointer is destroyed; this is not a guarantee that the original pointer is destroyed or that a replacement survives.

   Pending queue+14 instead goes directly to destructor vslot+4 at4A09A4. The linked list at queue+4 is drained through4A0930 and the same destructor slot. These shown paths have no explicit4A0860 call; that is not a universal no-output claim. For the exact approach type, destructor47AA70 calls475F80, which includes importC3B488 and base4A0730. Import/allocator effects are not closed here.

2. Queue ownership and concrete callers:4842B0 first clears actor+20 via4842B6, then actor+40 via4842BE. The approach constructor/admission verified in the preceding0100 letter puts its current pointer at actor+30 (=20+10); pending is actor+34. Earlier CFightMsg currentactor+50 is a different queue.

   Another concrete caller4498D0 performs position/movement writes, zeros actor+3A8 at449986, and clears actor+20 at449A10. This is a conditional relocation/clear route, not a proved physical Escape binding. Its finish range must be evaluated AFTER those changes; pre-reset proximity is insufficient. No claim that every clear caller preserves a viable owner/target or emits a request.

3. Replacement need not wait for the next positive frame step. For mode0 admission,4A0C90 stores the new task at queue+14. If new pointer is non-null and queue bytes+1C/+1D permit,4A0D6E invokes4A0B50 with float0. Within that scheduler, a non-null candidate from queue+4 (else+14) is passed to current task vslot+14 at4A0BF7. This check precedes the positive-time comparison at4A0C0C.

   The exact approach vtableF0F548 maps+14 to4A0880. Its complete predicate is candidate non-null AND current flags bit2 set. Initial80000006 satisfies bit2. A true result takes4A0BFB->4A0C4A, calls4A09C0 with0, then4A0A16->4A0860. Thus, subject to scheduler/lifetime gates, admitting a replacement can finish the current approach immediately. This describes an existing candidate, not a proof that a one-click action repeatedly creates new candidates.

4. The retained finish is475B80. It checks owner type, retained target existence/type and4758D0 range, then marker+4C nonzero selects475C31->44D260(EA7D,0); marker0 uses task+48 at475C21. The range-path marker is1. The preceding0100 evidence and all11 selected supporting spans are rechecked, including the full approach constructor/getter/registration/descriptor/vtable chain.

   Target-identity limit remains: finish checks retained task+50/+54, whereas producer44D400 copies CURRENT actor+C8/CC to outgoing+20/+24; actor+C0/C4 goes separately to outgoing+28/+2C. Producer also calls43C310 before constructing output. That helper resolves current C8/CC and zeros both if lookup misses (43C33D). This is a new precise invalidation fact, not reconciliation with retained A: a present B is retained, not replaced with A. Callback/lifetime changes still matter. No claim that a retained range check proves the wire target is in range.

   D / proposed falsification: unfinished current approach retains A; after a relocation or replacement, A passes the finish range gates and taskbit10 remains clear. Clear/preemption invokes finish while current wire target is B. Record whether the producer is invoked and admitted. This is a test candidate, not an observed extra hit or an assertion that physical cancellation reaches this state.

5. A separate input command route is now typed.449440 writesF0D690 and selector+14. Vslot0 getter449470 returns102D45C; registrationBCC8D0 links descriptor101A0D4, whose exact name is SkillCommand. Vslot+10=5BF160. With its earlier local-player/mount gates satisfied, selector+14==99 takes5BF199 pushEA7D and5BF19E->44EBF0. Other selectors use a separate check before5BF1C8. This adds a concrete source of attack invocation, but its invocation frequency and any retained input state remain open. Do not equate selector99 with a physical key or a DATA row merely because the numbers match.

   Two tempting repeat candidates have different selectors: movement task calls477EFF/477F51 selectEA76/EA77 andEA84/EA85 from state transitions.44D875 obtains its selector from475E40, whose explicit returns are0 orEA86..EA8D. Those exact paths therefore do not establish repeated EA7D. This uses the concrete return/control branches, not absence in linear disassembly, and does not exclude transitive callbacks elsewhere.

PER-CLASS: SkillCommand@0x14.4#W/#R selector; CActorTask_ActorAutoMoveToUseSkill@0x10.4#R:b0x2 preempt helper, @0x10.4#W:b0x10 finish guard; CMyActor@0xC8.8#W/#R current attack-target identity. Queue offsets are relative to their own actor+20/actor+40 subobjects; never universal offset meanings.

Search: external/, gamedata/, and reference_codex_attr/ were searched for producer, admission, clear/replacement and command mechanisms. PF_ATTR_ROLE_DISCRIMINATOR and its source script supplied prior caller candidates, not a complete callable-graph proof; relevant edges were independently pinned. Gamedata HOTKEY and SKILL_CONTEXT provide no proved repetition join; numeric99 matches are not crosswalks. Prior UseBehavior bounded negative is not expanded.

Reproduce from pf_bridge:
`& 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B .\staged\standing_a5d_verify.py`
PASS32 spans (21new+11reused),23calls27pins,23 actual in-memory call mutations rejected,2 named bindings,4 analytical preempt cases,2 empty-coverage guards. All7 source files and image checked before/after; no native code executed. Log: staged/standing_a5d_verify_20260909.log.
Image SHA256:9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623.
staged/standing_a5d_manifest.json SHA256:965116abef035c03c84d74009c83837f70a196239ed155174b45b80f35287495; each span includes VA/end/file-offset/SHA.

NEXT: trace what retains attack intent and invokes SkillCommand/another producer again after the first action, including revocation before submission. A5 still lacks a proved repeating cycle and authentic interval. Nonclaims: original-server policy, complete callback/writer census, physical cancel mapping, runtime extra attack, rendered damage, persistence or successful stop behavior.
