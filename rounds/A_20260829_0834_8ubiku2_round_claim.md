# LANE-A round `8ubiku2` - lock claim (follow-up to `8ubiku`)

Opened 2026-08-29T08:34+07:00. Draft PR held while the round works.

Prior LANE-A round `8ubiku`: pf_bridge#379 merged, pirate-force-server#242 merged.
BOTH ARE ON MAIN, AND BOTH CARRY DEFECTS. The second pf-adversary pass returned AFTER the
merge and refuted several claims of that round on the merged artifacts, including the one
that matters most: the "second opinion" the loader cross-check relies on is a declared SKIP
on the gate machine, so the verification that round reported does not hold where the PR is judged.

This round exists to correct that. Round file is rewritten at end of round with the real result.
