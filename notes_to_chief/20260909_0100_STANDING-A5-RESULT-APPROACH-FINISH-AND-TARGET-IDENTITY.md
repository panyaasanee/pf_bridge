งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้

ADDRESSEE: LANE-K / chief; LANE-B consumer
STANDING A5 — approach completion versus repeat. PARTIAL; NEW static progress; no global method ceiling.
SCOREBOARD: NONE | ผู้เล่นคลิกครั้งเดียวแล้วเดินเข้าไปตีและตีต่อเนื่อง | IMAGE only; no runtime or player-visible pass.

BUILD_PROPOSED: incorporate approach-completion versus repeat distinction into existing autoattack/cadence work and GT-224 | LANE-B; LANE-K links existing work | selected target: one gesture from out of range, first submission after approach, >=3 later timed attacks without more input; then cancel, target replacement/loss and death, with retained target versus wire target and client/server causes recorded separately

A / PROVEN_EXACT (bounded). A client task can invoke the EA7D producer after a retained-target range check. The producer uses the actor's CURRENT attack target; same-target continuity is not proved. Its completion wrapper is guarded once per unchanged task instance; this is not yet the sought sustained attack loop or an authentic attack interval.

1. EA7D bypasses the two ground/area-controller creation branches. In44EBF0, helper4889C0 returns signed(selector>=EA60); EA7D follows44ED4E..44ED85 into44D260, not ctor452FF0 at44EE09. Even the helper-false branch explicitly redirects EA7D at44EDB2/44EDB8. In44E890, EA7D comparisons44E98A/44E99E select44E9A6, not the mode4 controller allocation44EA67..44EAA6. This excludes those direct creation sites for this selector, not arbitrary callback/reentrant installations or TriggerCastSkillVital. Prior A5 pins the input/configuration13 route.

2. The actual admitted range path retains a different task. With a selected nonzero target,44E9F9 sets a local marker1, then44EB1D calls4758D0. A true range predicate reaches44EB49->44D260 directly. False reaches allocation44EB5A, ctor44EB9D->4757E0 and admission44EBB4->4843C0. Missing target can instead take44E9EF->44D260; no claim that every click creates an approach task.

   ctor4757E0 stores selector at task+48, target qword at+50/+54, marker at+4C and flags+10=80000006. The task is CActorTask_ActorAutoMoveToUseSkill: ctor writesF0F548; slot0 getter4758C0 returns type node102EC6C; registrationBD16F0 connects descriptor101D1C0. Vslots+8/+C/+10 are479110/479280/475B80.

   PER-CLASS: CActorTask_ActorAutoMoveToUseSkill@0x48.4#W/#R selector; @0x50.8#W/#R target; @0x4C.1#W/#R finish branch; @0x10.4#W/#R task flags.

3. Admission and frame execution are connected. Because80000006 lacks40000000,4843C0 chooses actor+20 and calls4A0C90 with mode0. That places the task in queue+14;4A09C0 promotes it to queue+10 and calls vslot+8. Thus the active pointer is actor+30 on this route, distinct from the actor+50 task used by the earlier CFightMsg study and from retained controller+3DC.

   On admitted player frames,44E53A->455AD0,455B0C->443480,443543->4A0C60 on actor+20, then4A0C68->4A0B50. Existing frame gates remain (including actor movement pointer and global state gates in443480).4A0B50 calls4A07B0, whose task bit4 path calls vslot+C with the frame argument. Since this task starts with bit4 set, its initial zero task+18 is NOT a zero-second attack period or a completion timer.

4. Start479110 and tick479280 resolve the retained target and test4758D0; true marks task+10 bit8 at479183/4792E2. For admitted non-null actors and ordinary finite values,4758D0 returns true only when squared distance is STRICTLY LESS than its computed squared range (475B4D comisd;475B51 jbe rejects equality/unordered). It has earlier rejection/type gates and an EA7D-specific range calculation using local ActorAttr/equipment lookups; the full authentic weapon/range policy is not claimed here.

   Other paths also mark completion: missing owner/target, failed owner type check, owner state/death tests, target no longer matching either actor+C0/C4 or+C8/CC, or485B90 returning nonzero. Completion is therefore not synonymous with successful arrival. No universal stop policy inferred.

5. Completion can submit the deferred attack, under its own gates.4A0B50 observes bit8 and calls4A09C0; that calls4A0860. The entire wrapper tests task+10 bit10: already set -> return; otherwise OR10 then OR8 BEFORE tail-dispatching vslot+10. This guards recursive/repeated finish dispatch while that instance and flag remain unchanged.4A09C0 subsequently re-reads the current task, calls destructor vslot+4 when non-null, and clears queue+10. Reentrant replacement/lifetime effects are not generalized to guaranteed destruction of the original pointer.

   vslot+10=475B80 rechecks owner type, target existence/type and4758D0. If any required check fails it returns without these attack calls. If admitted: task+4C==0 uses retained task+48 at475C21->44D260; nonzero forcesEA7D at475C2C/475C31->44D260. Marker1 selects the latter. Each is an invocation of the producer, still subject to its own admission gates, not proof every invocation reaches the network. Prior A5 proves admitted44D260 queues before its later task checks and does not create wait-task472900 for EA7D.

   Analytical models:80000006 becomes8000001E and suppresses a second finish; existing10 suppresses; pending8 permits one. Not native execution; other instances, direct callbacks, flag resets and server-triggered loops remain open.

6. Resource seam: both area controllers construct8B3360, storing result+20 at4530C9/4537CB. This is NiNode (ctorF5B700, getter8B2CE0 ->108D248, C13FB0/8B5830 nameF5B7BC). Slot60=8B1DA0 traverses children+B0/count+B6;888D50 invokes attached property/controller slots4C/50. ctor452FF0 attaches AreaEffect/AreaEffect2 via47D870 and root slot8C=8B3040. Constructor-empty children do not prove later emptiness or visual-only effects. Two matching local PCZ assets decode in memory; controller-string presence is not an object-graph/effects proof.

TARGET-IDENTITY LIMIT (adversary finding): finish475B80 range-checks task+50/+54, then passes only selector/0 to44D260. The producer44D400 instead copies CURRENT actor+C8/+CC to outgoing+20/+24 before queue44D42C. Tick permits retained target to match actor+C0/C4 OR+C8/CC. D falsification case: retained A remains in+C0, current attack target becomes B; checking A does not prove the submitted target is A. No intervening restoration/equality proof closes this join. Capture both identities; do not advertise same-target approach-and-hit from these static spans alone.

Search: external/reference GDL-IMG-020 in PF_GROUND_DROP_LIFETIME.tsv, evidence_key8d4af86b741a01e24653be3a61da6854edbf09a91225634696315c84ad638799: primary+6 support spans rechecked (100% selected row), original ceilings preserved. external/PF_SERIALIZER_FIELDS.tsv labels display-associated8AC090 calls CALL_UNCLASSIFIED; not effects proof. gamedata/ mechanism/AreaEffect searches had no direct answer. Local assets then fingerprinted; lexical absence is not mechanism absence.

Reproduce from pf_bridge:
`& 'C:\Users\Panya\AppData\Local\Programs\Python\Python314\python.exe' -B .\staged\standing_a5c_verify.py`
PASS50 span checks (43 primary+7 reused),32 direct calls,43 pins,7 branches,2 direct named bindings,3 analytical guard cases,2 empty-collection rejections,2 in-memory PCZ decodes; all8 source inputs/image checked before/after. No native/runtime test.
Image SHA256:9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623.
staged/standing_a5c_manifest.json SHA256:c9d49f420e877264d027649010def6d7d13629e1cf34d7df4de0dc1b3de40de3; every span has VA/end/file-offset/SHA. Log: staged/standing_a5c_verify_20260909.log.

NEXT: prove a second EA7D producer cycle after guarded finish/direct attack, with trigger and stop predicates. Resource callback effects remain open. A5 cadence remains unresolved; no authentic timing, complete writer/callback census, original server policy, runtime damage or persistence claim.
