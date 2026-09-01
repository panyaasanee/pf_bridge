# LANE-A round `njkvcc` — real pf-adversary re-verification of the logout dialog-open profile

## NOW.md (read first, per house rule)

Checked before anything else. `รอ Panya ติ๊ก` is empty. P-1/P-2/P-3, UI-A, GM-B, UI-B are all
outside LANE-A's write zone and did not move. GM-A/census latch item explicitly says LANE-A/GM
may run normal queue (code-side is done, only Panya's attended `GT-192` is pending, not a lane
blocker). `PANYA-ORDER 20260901_0215` pauses all numbered milestones -- so this round does **not**
touch M2 (the ADDENDUM's own fallback suggestion for an idle LANE-A round), since NOW.md overrides
the addendum where they conflict.

## Section A -- prior PR fate

`pirate-force-server#490` and `pf_bridge#730` (round `2ahq88`): both `merged: true`, confirmed via
`list_pull_requests(state=closed)` showing `merged_at` set on both. Nothing to recover.

## Mailbox

No unconsumed `ADDRESSEE: LANE-A` letter exists. The most recent one
(`20260901_1605_CHIEF-REPLY-corerequest-logout-dialog-open-push-lane-a-may-edit-once.md`) was
already consumed by round `2ahq88`.

## Why this round did what it did

Milestones paused, mailbox empty, no LANE-A-owned queue item with real surface this round -- rule F
applies. Its own text suggests M2 as the idle-round fallback, but that conflicts with the milestone
pause above, so it does not apply this round. Fell back to rule F item (ง): technical debt.

Two prior LANE-A rounds (`tmizmk` / PR #484, `2ahq88` / PR #490) both stated plainly, in writing,
that their remote session had **no Agent/Task tool available**, so the mandatory pre-commit
pf-adversary pass was done as a manual self-checklist walk instead. Round `2ahq88` flagged this
explicitly to COO as `[สมมติของสาย A -- รอ COO ยืนยัน]`: "Whether manual-checklist review is an
acceptable long-term substitute for a real pf-adversary invocation when no Task/Agent tool exists
in a remote session."

This session's remote environment *does* have a working Agent tool with a real `pf-adversary`
subagent. So instead of leaving that question open or idling, this round used it for real: ran
`pf-adversary` against the exact files those two rounds shipped, already merged on `main`,
read-only (agent worked in its own `git worktree`, confirmed byte-identical to the live checkout
afterward).

## What pf-adversary tried, and what held up

All six genuine break attempts came back clean -- these are re-verified, not re-asserted:

1. **`production_allowed` escalation** -- grepped the whole repo: the flag is assigned `False`
   exactly once at module scope, flipped only inside two tests' `mock.patch.object` context
   managers (auto-restoring), and the `runtime.py` dispatch branch re-reads the module attribute
   live. No production path sets it.
2. **Allowlist bypass** -- four mutation attempts (removed a `nonclaims` entry, reordered
   `nonclaims`, added an unknown top-level key, substituted `production_allowed: 0` for `False`).
   All four rejected with `ValueError`; the `type(actual) is not type(expected)` check catches the
   bool/int substitution specifically.
3. **Hash-pin drift** -- corrupted `RETURN_SELECT_SERVER_RESPONSE_PC_SHA256` by one hex digit in
   the worktree copy; broke 24 tests loudly across three files. Load-bearing, not decorative.
4. **CI silently skipping these tests** -- confirmed via the gate workflow's own dynamic exclusion
   grep (`GameClient|capture_v141`) that neither new test file matches it; they run in the real
   `pytest_subset` step.
5. **Double-counting / routing precedence** -- traced `runtime.py:5484-5570`: the dialog-open
   branch and `WORLDINFO_FIRST` are mutually exclusive (single `response_policy` field); confirmed
   with the existing test that `rx_frames` increments exactly once.
6. **TOCTOU race on the one-shot latch** -- one thread per connection, sequential dispatch loop;
   the only other thread (`heartbeat_worker`) never touches the counter. No race window found.

## The real finding: a genuine evidentiary gap, not a functional bug

`logout_hypothesis.py:193` states: *"EVERY TAG BYTE (0x08 / 0x32 / 0x44) IS READ FROM THE CLIENT'S
OWN SERIALIZER; nothing structural is invented"* -- and the sixth profile's own capability list
repeats the same claim.

But the only externally-checkable static artifact for that exact field,
`pf_bridge/external/PF_SERIALIZER_FIELDS.tsv:1125`, classifies `ReturnSelectServerVital`'s field 3
serializer (`0x5E69F0`) as `UNTAGGED_STRING8_LEN32LE` -- not tag `0x44`. No row in that whole
1128-line table carries tag `0x44` anywhere. `pf_bridge`'s own closed ticket GT-055 explains why:
that classification is a known blind spot of the automated extractor for this string-write helper
family. The "the tag really is `0x44` on the wire" claim is directly confirmed only for a
**different** message (`DeleteActorVital`, via GT-018's raw capture) and then generalized to the
whole helper family -- never independently measured for `ReturnSelectServerVital` itself (whose two
captured frames are `W`-direction only, per the RE-070 erratum already recorded in the file).

The tool cited as independent corroboration, `tools/verify_logout_return_select_encoder.py`, calls
itself an *"independent walker"* but hardcodes the identical `FIELD3_TAG = 0x44` constant it is
supposedly verifying (line 72). It is independent of the composer's **code**, not independent of
the composer's **schema assumption** -- it would "confirm" the composed body identically even if
the real client wire form for this specific message has no leading tag byte at all on field 3.

**Concrete failure scenario**: if `ReturnSelectServerVital`'s real client serializer does not
prefix field 3 with `0x44` (unlike `DeleteActorVital`), then `RETURN_SELECT_SERVER_BODY` contains
one genuinely invented byte that never existed on the client's real wire format for this message --
directly contradicting the "nothing structural is invented" guarantee this profile ships, and
undermining the "well-formed" characterization an attended `GT-184`/`GT-186` run relies on.

**Mitigating context, stated plainly**: this byte layout is *inherited* from the earlier HYP-PF-028
round, not newly introduced by the sixth profile. `production_allowed` is confirmed `False`
everywhere reachable. This exact composed frame was already pushed once in a real attended session
(`GT-033` Variant B) with a negative ("no transition") result, and nobody has attributed that
negative result to this specific byte. pf-adversary could not resolve the question definitively
either way from this clone (no raw capture bytes, no client image) -- this is reported as a
**suspicion**, not a confirmed defect. But it is a real, demonstrable gap between what the code
claims ("read from the client's own serializer") and what the cited artifact for that exact field
actually shows ("UNTAGGED", never tag-captured for this message).

## Answer to the standing COO question

Round `2ahq88` asked: is a manual pf-adversary-checklist walk an acceptable long-term substitute
for the real subagent, when no Task/Agent tool exists in a remote session? Given the **same**
already-merged diff that two manual passes had already looked at, a real `pf-adversary` invocation
found a genuine evidentiary gap that neither manual pass caught. That is direct evidence the answer
is **no** -- manual checklist review is not equivalent, at least not for prose/evidence-chain claims
like this one (as opposed to, say, an obvious logic bug a human eye would also have caught).
Recommendation carried to chief/COO below: whenever a session's environment actually has a working
Agent tool (this one does), the pf-adversary/pf-static-re/pf-builder subagents must be invoked for
real before commit -- manual-checklist substitution should be reserved strictly for sessions that
have genuinely verified the tool is absent.

## Why this round did not self-fix the docstring

`logout_hypothesis.py` and its companion `logout_dialog_open_hypothesis.py` are under chief's
explicit restriction from `20260901_1605_CHIEF-REPLY-corerequest-logout-dialog-open-push-lane-a-may-edit-once.md`:
the one-time permission for the sixth profile was granted, and any further edit "ไม่เปิดเขตเขียนถาวร
งานครั้งถัดไปกลับมาเป็นของ chief". Round `2ahq88` already respected this once (opening a
CORE-REQUEST for RE-189 branches 2/3 instead of self-editing); this round does the same rather than
re-opening that file unilaterally to correct the overclaim. See the CORE-REQUEST letter of this
round for the concrete proposed correction text and the ask to chief.

## What did NOT change

No `src/`, `scenarios/`, or `tests/` diff in either repository this round. `production_allowed`
stays `False` everywhere it already was. No allowlist edit. Companion `pirate-force-server` PR
carries only the round-claim and end-of-round wake-gate empty commits, per protocol -- all
substantive content is in this repository.

## Files touched (pf_bridge only)

- `rounds/A_20260901_1737_njkvcc_real-adversary-reverify-finds-tag-byte-evidentiary-gap.md` -- this file, new
- `notes_to_chief/20260901_1737_LANE-A-CORE-REQUEST-logout-tag-byte-overclaim-found-by-real-adversary.md` -- new

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มีเลย -- รอบนี้เป็นการยืนยันหลักฐาน (re-verification) และเปิดคำถามให้ chief ตัดสินเรื่องคำบรรยาย
ที่อาจกล่าวเกินจริงในไฟล์ที่สายนี้แก้ไม่ได้เองแล้ว ไม่มีพื้นผิวใหม่บนจอเกม
