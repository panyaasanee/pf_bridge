# TO CHIEF: RE-208's route tag contradicts its own pass criteria, and half the open RE queue is misrouted right now

- who: ka1-A (attended), raised by **Panya** herself - she read the ticket, spotted the
  contradiction, and told me to bring it to you
- when: 2026-09-02 ~20:50 (+07:00), approximate
- her instruction, verbatim in substance: she is sending **RE-208 and RE-138** to the
  Codex RE runner, and **this must not slip again next round**
- I did not touch a single queue header. Headers are yours.

## 1. The contradiction, in one ticket, in its own words

`RE-208 GROUND-POOL-REMOVAL-PATH-FOR-THE-LAST-OBJECT-001` header says:

    [OPEN -- ... `STATIC-ON-CLOUD`]

Its own pass criteria say:

    ชั้น static: **ในภาพไคลเอนต์** ระบุว่า reconciler ของ TerrainThingPool
    (`0x006AF970` ตามใบ Codex CODEX_URGENT_20260901_0324) มีเส้นทาง
    remove-by-key / destroy-one ที่ถูกเรียกจากข้อความอื่นหรือไม่ ·
    **ถ้ามี: VA + ชื่อ vital/opcode + รูปร่างเพย์โหลด**

"in the client image", a named VA to start from, and an answer that must itself be a VA.
That is disassembly of `GameClient.local.bin`. **The cloud has no image.** The route tag
and the pass criteria cannot both be right.

## 2. Its two nearest neighbours, asking for the same class of thing, are tagged the other way

| ticket | route tag | what it asks for |
|---|---|---|
| **RE-208** | `STATIC-ON-CLOUD` | the reconciler at `0x006AF970` in the client image, answer as a VA |
| **RE-209** | `[STATIC-ON-BRIDGE]` and says so out loud: *"ต้องดิสแอสเซมบลีอิมเมจ ⇒ ทำบนคลาวด์ไม่ได้"* | disassemble `0x0045BC80..0x0045BC8A` |
| **RE-210** (closed PASS) | `[STATIC-ON-BRIDGE]` | answered with handler VA `0x00710440` and its five bytes |

Three tickets, one kind of work, one odd tag out.

Corroborating: `COO-DECISION 20260902_1145` parks the quest-mark line **"until the real
machine"**, which is the same judgement applied to the same constraint.

## 3. It is not one ticket. Half the open queue is misrouted as of tonight

`python tools_bridge/pf_re_queue_taglint.py --list-open` returns 4 open tickets:

    RE-138  line 2294   STATIC-ON-CLOUD          <- CORRECT, see below
    RE-155  line 2533   NEEDS-ATTENDED-CAPTURE   <- correct
    RE-169  line 3209   route=MISSING            <- NO ROUTE TAG AT ALL
    RE-208  line 4343   STATIC-ON-CLOUD          <- contradicts its own body

- **RE-169 has no route tag.** That is precisely the `[B] MISSING ROUTE TAG` failure the
  lint tool was built for, and its own docstring records that this exact fault idled the
  runner for **30 hours** at R276 and **12 hours+** across R287-R292. The lint printed it
  tonight; it is still there.
- **RE-138 is correctly tagged.** I checked its body before saying so: no VA, no image,
  no disassembly - it asks what the reconcile round sends and what the shipped tables
  hold. **Please do not "fix" this one.** The owner is sending it to the runner and it
  will work as tagged.

## 4. What I am asking for - and the second half matters more than the first

**(a) Correct RE-208's route tag** to `STATIC-ON-BRIDGE`, and give RE-169 a route tag.
Header edits are yours; I have not touched either.

**(b) Make it mechanically impossible to slip again, because "be careful next round" has
already failed twice on this exact field.**

`tools_bridge/pf_re_queue_taglint.py` already prints two sections, one per past failure:
`[A]` missing status tag, `[B]` missing route tag. RE-208 is the **third member of the
same family** - a tag that is *present but contradicted by the ticket's own text* - and it
deserves the same treatment the other two got: measured, not noticed by accident.

Concretely, a `[C] ROUTE CONTRADICTS BODY` check: flag any ticket tagged
`STATIC-ON-CLOUD` whose body contains an image-only marker. Cheap, purely textual, no
false-negative risk worth caring about:

    GameClient.local.bin      ในภาพไคลเอนต์      span_sha256
    disassembl / ดิสแอสเซมบล   a bare VA matching  0x00[0-9A-Fa-f]{6}

The owner's words for what she wants out of this are exact: **"next round, do not let it
slip."** A lint rule is what makes that a fact rather than an intention.

## 5. NONCLAIMS

- I do NOT know how the Codex RE runner filters on the route tag, so I cannot say whether
  it would have skipped RE-208, picked it up and hit a wall, or answered it from the TSVs
  alone. All three are bad; which one happens is unmeasured by me.
- I do NOT know whether RE-208's tag was a typo or a deliberate judgement I am
  misreading. I am reporting the contradiction, not a motive. The ticket was opened by
  LANE-B and renumbered 206 -> 208 during a merge in the same round, which is churn, not
  evidence.
- I audited only the **4 open** tickets. Closed and archived tickets were not checked, so
  the true count of contradictory tags in the file may be higher.
- I did not run the proposed `[C]` check - it does not exist yet. Its false-positive rate
  is unmeasured.
- No header, no ledger and no queue file was edited by me tonight.
