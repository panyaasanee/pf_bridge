งานเป้าหมายยืน — ยังไม่มีเลขใบ ขอให้ LANE-K ตั้งเลขและผูกจดหมายนี้

# A5 PARTIAL — EA7D skips the 1.0 task; the other clock follows COnLandVital

ADDRESSEE: chief, LANE-B, COO; cc LANE-K
START: 2026-09-09T00:24:07.0019074+07:00
STATUS: PARTIAL / new static findings; autonomous repetition remains UNKNOWN.
MODE: local IMAGE read-only. No runtime, source/queue/DB/lease/Git changes.

**ผลหลัก:** EA7D ข้าม task รอ1.0; อีกนาฬิกาถูกตั้งหลัง COnLandVital จึงยังแทน600msไม่ได้ ผู้ส่งคำสั่งตีซ้ำยังไม่พิสูจน์

## New exact IMAGE findings (grade A)

1. **Input-triggered attack is not itself a repeat loop.** In event handler `44F0B0`, accepted event `+4=0x201`, event `+8` mask0x8 clear, resolved picked actor, failed relation predicate and picked-actor vslot3C false reach `44F36A`. Both words of picked identity `+78/+7C` must equal CMyActor's retained target `+C8/+CC`; with local byte `+358=0`, `44F393` pushes EA7D and `44F39A -> 44EBF0`. This command has its own actor-state/death predicates. Configuration index13 can redirect it through `44EC88 -> 44E890` and the geometric gate; otherwise `44ED85 -> 44D260`. These are conditional paths for another input event, not proof of a second command after input stops. Target identity and an active attack intent must not be treated as synonymous.

2. **The queue call precedes the wait-task checks.** In the admitted network path, `44D3B7` copies the requested action to ActionVital `+30`, `44D400..44D40F` copies CMyActor `+C8/+CC` to vital `+20/+24`, and `44D42C -> 5DD800` submits it. Only afterward come existing-task/actor checks and `44D500 -> 47C5D0`. Failure there jumps from `44D507` to exit `44D5DD`; it does not undo the preceding submit. Thus these later checks cannot throttle that already-submitted request. No claim that all preceding calls or every input route lack other gates.

3. **EA7D is explicitly excluded from task472900 creation here.** `47C5D0 -> 4889C0` recognizes the signed reserved domain >=EA60. Within that domain, comparisons at `47C5E8/47C5F0` make **EA7D, EA7E and EA7F return false**; adjacent EA7C/EA80 return true from this helper. A true helper result is only one prerequisite for allocation, not sufficient. The later constructor at `44D54D -> 472900` installs vtable F0F078, flags `+10=60000000`, and float `+18=1.0` from F092A4. EA7D's false return skips this constructor. Neither this constant nor the helper's true cases establish an attack interval, elapsed wall-clock units, or all possible origins of this task.

4. **A concrete response can mark that task for termination, without proving repeat.** Named CFightMsgVital binds codec `5F28D0`, handler `750270`, vtable F489C8. Codec transfers two tag14/len4 fields at object `+14` and `+18`. For `+18=100025`, selector `75029A` subtracts 100000, byte-table index25 gives12, and target-table entry12 gives `750412`. With the local singleton present, `75041C -> 4729E0` looks at local actor `+50`, type-checks against the same token 102ED8C returned by `472930`, and ORs that task's `+10` with8. This does not demonstrate a following attack, an ACK contract, original rejection policy, or that EA7D instantiated the task. This cancellation branch uses the local singleton, without a qword actor lookup.

5. **Correction to an old timer attribution.** `PF_RESCUE_AND_DEATH_ESCALATION_STATIC_20260819.md:328` calls the vital submitted at425095 ActionVital. Exact chain: `425063 -> pool424D20 -> ctor5E6E50`; both new/recycled pool paths call that ctor (`424D84/424E02`). Ctor sets vtable **F30548**, whose getter5E6EA0 reads the ID global10820A8 written by named **COnLandVital** registrationBEE9C0; codec/handler slots are5E6EB0/710440. Thus this submit is COnLandVital. `42509A..4250A2` sets global1031790 to1.0, and `44E53F..44E578` subtracts the frame argument and clamps at0. The numeric clock is real; the old ActionVital attribution is wrong. This does not establish its complete role or prove it can never indirectly affect an attack.

## Evidence and reproduction

Pinned GameClient.local.bin: 14,759,424 bytes; SHA256
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.
All nine source SHA values, 32 unique VA/file spans and their full SHA256 are in `staged/standing_a5_manifest.json`; repeated reference ranges are aliases, not new evidence rows.

Key spans (end exclusive):

| Claim | VA span | File offset | SHA256 |
|---|---|---|---|
| EA7D exclusion |47C5D0..47C60C|7B9D0|6b3a79ba8d57a008cb5cd2846d956084c63822990affdd42e07324c757d52aa0|
| COnLand constructor |5E6E50..5E6E8B|1E6250|2d335c79891fa75124531a6b0093c5cf34a122795368f300b20ff0a5be3c38b8|
| Land submit/clock |425057..4250AA|24457|fe1184856cb1a5cf408f494134bd84763d37d3abf30fa077511a5194befa9986|

ค้นชุดส่งมอบแล้ว: เจอ ActionVital, CFightMsgVital and COnLandVital registry/codec anchors in external; reused CL-IMG-003/004/005 from reference_codex_attr/PF_COMBAT_LIFECYCLE.tsv, checking every selected primary/support span (100%). Their old UseBehavior no-direct-edge result remains narrowly bounded; it is not reissued as a new absence proof.

ค้น gamedata แล้ว: เจอ EQUIP_VALUE.n_ATTACK_SKILL and BEHAVIOR.n_MOB_CD, plus the columns index; these supply no new provenance for replacing provisional600ms. No animation suffix or zero MOB_CD is interpreted as time here. Current read-only runtime.py contains check_attack_cadence at5769; the historical "unwired" request is not current status.

Run from any directory (PowerShell):
```powershell
& 'C:\Users\Panya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\standing_a5_verify.py'
```
PASS:32 spans,3 reused rows,20 calls,10 branches,32 instruction pins,8 bounded analytical eligibility cases,2 named bindings,94 in-memory mutations +2 empty-coverage traps rejected. Model cases are not native execution. Source/image SHA checked before/after.
Verifier SHA `296cfa53c02c4203e662256c329abc8a358d4d28d03d68b0a01b51f86838ab41`.
Manifest SHA `22175b7b9d7eb2ae1a8d13cb3ab6bedf85e663e2c842894ca2e4dbc741d2a43d`.
Log `staged/standing_a5_verify_20260909.log` SHA `ec4214f6cde523f2fe1fdcdf50c5070e1c65d518c1cc315bb8b942fa2eab5a3a`.

## Remaining work and build impact

This is a checkpoint, not a whole-client static ceiling. Exact next seam: CMyActor `+3DC` retains an input controller; `44E76A..44E784` invokes its vslot+4 each frame. `449110` replaces/deletes it; command paths44ED28/44E978 clear it. Still needed: concrete controller producer/vtable reachability from the attack gesture, any retained state that re-enters attack submission after input ceases, its stop predicates, and its timing/response dependency. Do not re-scan UseBehavior as a substitute. No claim of universal repeat absence, authentic cadence, click timing, rendered attacks or gameplay completion.

BUILD_PROPOSED: complete single-gesture repeated attack and explicit stop behavior after the remaining sender/intent seam is resolved, preserving server admission checks | LANE-B via chief, existing GT-224 scope | ONE_GESTURE_REPEAT_STOP: one recorded gesture; >=3 separately timestamped attack submissions/results; stop on cancel, target loss and death, with no extra clicks; distinguish a server-driven sequence if that is what evidence shows
BUILD_IMPACT: keep600ms labelled provisional; neither identified1.0 value replaces it. Do not synthesize CFightMsg100025 as an auto-repeat trigger from this result.

SCOREBOARD: NONE | ผู้เล่นยังไม่ได้รับการยืนยันว่าคลิกครั้งเดียวตีต่อเนื่อง | IMAGE exclusions/correction only; no client runtime this round
