# LANE-A round lg1dvz

Opened 2026-08-30T09:22+07:00 (round-lock claim: pirate-force-server#298,
pf_bridge#473). Closed 2026-08-30T09:39+07:00.

## Round-start checks (ADDENDUM v2 §A/§B)

- Last LANE-A round (`n4wj7k`) checked via `pull_request_read` method=get on
  both repos, NOT the `list_pull_requests` listing (that endpoint's `merged`
  field showed `false` for both `pirate-force-server#295` and `pf_bridge#469`
  -- the exact gotcha `pirate-force-server#297`/this repo's
  `20260830_0920_LANE-GM-STATUS-...` just documented). `get` on each PR
  number shows `merged: true`, `merged_by: github-actions[bot]`, both bases
  are ancestors of the fetched `origin/main`. Work is on main. No cherry-pick
  recovery needed.
- Mailbox: grepped `ADDRESSEE: LANE-A` across `notes_to_chief/`. Every hit
  already has a `.CONSUMED.txt` stub except
  `20260830_0830_LANE-A-RE-mob-npc-jungle-tiger-...md`, LANE-A's own reply
  from round `n4wj7k`. **First pass of this round's `.CONSUMED.txt` called
  it pure header noise and closed it unread -- pf-adversary caught that
  before commit: the letter's body has a self-labelled 🔴 open item
  explicitly handed to "the next lane A round"** (an apparent index mismatch
  between `field_mob_tables.py`'s `WITHDRAWN_UNDER_THIS_RULE` row
  `(58, 60, 'Jungle Big Tiger', 741, 'Juliet')` and
  `world_port_royal_identity.py`'s row `(60, 741, ..., 'Juliet', 'Sworn')`).
  Traced it properly on the re-pass: not a bug. `WITHDRAWN_UNDER_THIS_RULE`
  is keyed by `(placement_index, was_template_id, ...)`
  (`field_mob_tables.py:133-142`); `world_port_royal_identity.py`'s
  `_RESOLVED_ROWS` is keyed by **Mob-Set number**, not placement_index, per
  its own header comment (`world_port_royal_identity.py:206-208`). The
  legacy defect this whole project is built around put the raw Mob-Set
  number directly into the template_id/MOBS-n_ID slot, so `was_template_id
  60` in the withdrawn row *is* the placement's Mob-Set number, not a
  coincidence -- looking that Mob-Set number (60) up in the second table
  gives template 741 / Juliet, matching the withdrawn row's
  `now_template_id`/`now_display_name` character-for-character.
  `placement_index 58` and `Mob-Set number 60` simply aren't the same axis
  and were never supposed to match. Rewrote `.CONSUMED.txt` with the full
  trace before this ever left the working tree (never committed, so nothing
  published needed a strike-through) -- but the stub itself says plainly
  that its first pass was wrong and why, per this project's own rule about
  not quietly erasing a mistaken claim.

## What this round investigated

`FROM_CHIEF_R236_TO_ATTENDED_20260830_0855.md` handed lane A/B four
owner-filed polish gaps from the attended `GT-131` PASS session
(`20260830_0030_KA3A-GT131-...md` §③), explicitly "not urgent, fix at your
own pace": (1) NPC names render green, should be yellow; (2) Training Iron
Man (mob 916) should render as a red-named mob; (3) NPC facing direction
wrong despite a real `FACE_PLAYER_POSITION_HEADING` frame; (4) actor attr
completeness generally, per `PANYA-DECISION 20260828_0125`.

Took (1) and (2) first -- concrete, narrowly scoped, no identity dependency.

Traced both to a static evidence ceiling already recorded three times:
`RE-067` (BOUNDED-NEGATIVE, no read of `NPCAttr faction+0x68` / relation
comparator / `FONT_COLOR` loader inside the fully-decoded `NameBoardNPC::
update`), `RE-068` (`board+0x34` is stale character-delete countdown state,
not a colour field; `FONT_COLOR`'s one caller is a resource-init chain, not
actor render), `RE-109` (closed 2026-08-27T18:15, CFG 485/503 instructions,
explicit `BUILD_IMPACT: NONE -- do not hard-code a colour from actor_type /
faction 1-6 / FONT_COLOR ID / n_SKIN_COLOR until an attended one-field
crosswalk exists`).

Re-verified two facts from source this round rather than trusting the old
tickets by citation alone: `population.py:23` (`NPC_STYLE_ACTOR_TYPE = 4`)
confirms every default NPC already ships `actor_type=4`
(`CNetNPC`/`NameBoardNPC`, per `RE-109`), so the green-name bug is not a
misclassified actor type on our side -- the unresolved logic is inside the
client's own `NameBoardNPC` colour choice, exactly where the three RE
tickets hit their ceiling. And `field_mob_tables.py:96-99`
(`TOWN_TARGET_PLACEMENTS`, template 916 x4) is already unioned into
`field_mobs.load_roster()` and gets the hostile faction splice
(`mob_death.full_roster_override`) on every flagless home-scene boot -- the
same splice `GT-032` already sent, which `field_mobs.py`'s own docstring
records as producing *no* red name label because that frame carried no name
bit at all. Sending the identical bytes again has no evidentiary reason to
produce a different result.

## Why nothing was built in `src/` this round

`RE-109`'s `BUILD_IMPACT: NONE` is explicit and still stands: hard-coding a
name-colour source now, with no attended field crosswalk, is exactly the
guess the project's own evidence rules forbid (AGENTS.md "Evidence rules" --
never promote a broad claim from a narrower test, never overstate an
evidence grade). Writing color logic here would not be "the smallest thing
that can be" (charter sentence 1) toward a real fix -- it would be a
fabricated row the client's own tables don't establish.

## What was built instead (rule 2: open a ticket, then keep moving)

`pf_bridge/CLIENT_RE_QUEUE.md`: new ticket `RE-155`
(`ACTOR-NAME-COLOR-NPC-VS-HOSTILE-MOB-ONE-FIELD-CROSSWALK-001`,
`NEEDS-ATTENDED-CAPTURE`), +65 lines. Names the exact one-field A/B capture
an attended session needs to run (NPC: one field at a time against the
already-identity-confirmed `GT-131` placements; Mob: one field at a time
against Training Iron Man's already-shipped hostile bytes), the pass
criteria (client-observable before/after screenshots -- the layer all three
prior tickets stopped short of), and the nonclaim that a negative result
here still stands as the client data ceiling, not a bug to keep chasing in
static.

## ผู้เล่นจะเห็นอะไรต่างจากเมื่อวาน

ไม่มี -- ทั้งสี่ข้อยังไม่มีโค้ดใหม่ในเกม รอบนี้ป้องกันการเขียนสีแบบเดาที่จะขัดกับ `RE-109` เอง
และเปิดทางเดียวที่เหลือ (attended one-field capture) ให้คนหน้าจอทำได้ทันทีที่มีกะถัดไป

## Not touched

`runtime.py`, `app.py`, `current/pf_login_game_server_v141.py`, any scene,
any test file. Zero diff in `pirate-force-server` this round (`git status
--short` empty, confirmed before and after the build sub-task).

## Tests

`pytest tests/test_field_mobs.py tests/test_mob_death.py
tests/test_mob_death_wired_widening.py tests/test_mob_census_hostility.py
tests/test_population.py` (pirate-force-server) -- 184 passed, 1 skipped,
181 subtests passed. Run twice this round, independently, in two different
sandboxes (once by the build sub-task, once again by this round directly
before commit, after pf-adversary flagged it as unconfirmed since its own
sandbox had no `pytest` installed) -- same result both times. Confirms the
modules read during investigation are unmodified and still green; not a
new-behaviour test run because no new behaviour was written.

## pf-adversary review (this round, before commit)

Independently re-derived the RE-067/RE-068/RE-109 citations from the queue
file and its archive (not from this round's own docs), confirmed the two
re-verified source facts and the call graph they sit in
(`field_mob_tables.py:124-127` `SHIPPED_PLACEMENTS` union,
`field_mobs.py:576-647` `load_roster()`, `runtime.py:7536`
`full_roster_override` called unconditionally on the home-scene boot path),
confirmed zero diff under `src/ tools/ current/`, confirmed no `RE-155`/
`GT-155` numbering collision, and confirmed the ticket is self-contained and
under the size bound. Caught the mailbox-consumption defect described above
before commit. No other defect found.

## CORE-REQUEST

none.

## Next round candidates

- Item (3) from the same letter (NPC facing direction) is unexplored --
  chief flagged it as the most interesting of the four, and it looks
  data-driven rather than client-opaque: check whether a per-placement
  facing/heading value already exists in the shipped placement tables and
  is simply not being wired into the spawn/arrival frame (as opposed to the
  click-triggered `FACE_PLAYER_POSITION_HEADING` frame `world_face_frame.py`
  already handles correctly). Not started this round for lack of remaining
  time budget, not because it hit a ceiling.
- `RE-155` needs an attended session; flag it to the next attended shift the
  same way `RE-152`/`RE-149` were flagged.
- M2 (leaving town) fallback per ADDENDUM v2 §F remains available and
  identity-independent per the owner's own note; not picked up this round
  because the polish-item investigation and ticket authoring filled it.
