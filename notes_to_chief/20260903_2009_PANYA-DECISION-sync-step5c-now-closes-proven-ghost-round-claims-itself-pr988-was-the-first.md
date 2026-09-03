ADDRESSEE: COO - cc chief, LANE-A (owner of the #988 ghost), every lane that opens claim PRs

# PANYA-DECISION: pf_git_sync.ps1 step [5c] now CLOSES a round claim it can PROVE is a ghost - and sees lane-style claims at all

- when: 2026-09-03 ~19:5x+07:00 (approximate; ordered in chat: "ทำ ข+ค")
- channel: chat with ka1-A (attended session); ka1-A wrote the patch, the owner chose the option
- amends: the 2026-08-25 ~09:4x ruling that [5c] "only REPORTS and never closes a PR" - that sentence is now
  "only reports, EXCEPT a claim that meets all three ghost conditions below, which it closes with the reason written on the PR"
- backup of the script before the patch: pf_bridge\agent_kit\pf_git_sync.ps1.pre_patch_ghostclaim_20260903
- checks: parser 0 errors, -SelfCheck exit 0 (job 1483), token via `git credential fill` = yes, first live round closed #988 (20:06:18)

## The case (measured)

pf_bridge#988 `[LANE-A] round 0zoxir: claim` opened 16:22. The round landed its server half (pirate-force-server#662 merged)
and died before pushing the bridge half. The claim stayed OPEN with one three-line stub on the branch. Round h4d51r (17:23)
yielded to it for a full hour. Round omhpqj (18:23) took it over and opened #1001, reported it in letter 20260903_1840,
and - by the house rule that no lane closes another lane's PR - left #988 open. COO's 1945 decisions did not touch it.
Step [5c] never saw it: its subject filter only knew the old chief-style `round claim: <id>` and not `[LANE-A] round <id>: claim`.
At 20:06 the patched step closed it: `age 224 min; branch holds only 1 claim stub(s); server PR for round 0zoxir is closed/merged`
(pf_bridge#988 state=closed at 13:06:18Z, comment on the PR carries the same sentence; notice 20260903_2006_SYNC-NOTICE-pf_bridge-pr988-ghost-round-claim-closed.md).

## The rule now in the script

A claim PR is a GHOST, and [5c] closes it itself, only when ALL of these hold:
1. the bare claim tip is >= 120 minutes old (`CLAIM_GHOST_MIN`, distinct from the 75-minute shout window);
2. `origin/main..origin/<branch>` holds nothing but claim stubs (1-2 commits whose subject is a claim; any real work = not a ghost);
3. the round is finished or replaced elsewhere: a pirate-force-server PR whose branch ends in the same round id is CLOSED or MERGED,
   or an OPEN pf_bridge claim says `takeover of #<this PR>`. A server PR for that round id still OPEN = the round is alive = never a ghost.
On close: comment on the PR with the three facts, close (never delete the branch), write a SYNC-NOTICE to the lane + COO + chief,
mark the branch's cache verdict `none` so the next round is quiet. Anything short of all three is still only reported, with the
reason it was NOT judged a ghost printed beside it. Dry-run / -SelfCheck never close anything.

Also fixed in the same patch: `IsClaimSubject` accepts both claim shapes, so lane rounds' claims are now inside [5c]'s watch at all.

## What this does and does not promise (the owner asked "will it never happen again?")

- A ghost can still be BORN: a round can still die between its server push and its bridge push (that is the lanes' fragility,
  not the sync's). What changed: it can no longer LINGER. Within ~2 h of the death, with the three proofs in hand, the lock is gone
  and the reason is on the PR and in the mailbox - no lane yields an hour to it, no takeover is needed.
- NOT auto-closed on purpose: a claim whose branch carries real commits (dead work, not a ghost - [5d]/recovery rules own it);
  a claim whose round never opened a server PR and was never taken over (not proven dead - shouted for a person); anything while
  GitHub is unreachable or the token is missing (shouted with the reason).
- If a closed claim was in fact alive, the lane reopens the PR and says so in notes_to_chief; ka1-A tightens the rule.

## Ask
COO: fold the amended sentence into wherever the 2026-08-25 ruling is written (NOW.md / the lane addenda) so the lanes stop
treating an open ghost as untouchable; the script already behaves this way.
