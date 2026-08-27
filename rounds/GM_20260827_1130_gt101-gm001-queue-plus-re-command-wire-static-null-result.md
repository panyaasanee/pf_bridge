# LANE-GM round -- GT-101 (GM-001 attended probe queued) + static-RE dig closed negative

Session: rw9ovu (2026-08-27, +07:00)

## What this round did

1. **Verified no [LANE-GM] PR was left open** in either repo at round start (protocol step). Checked
   the previous round's PRs by `pull_request_read` (`method: get`, not `list_pull_requests` -- that
   endpoint's `merged` field reads `false` for PRs that are in fact merged; this repeats R191's own
   lesson about re-deriving state from the tool that actually tells the truth):
   `pf_bridge#182` and `pirate-force-server#106` (say-wire round) both show `"merged": true`,
   `"merged_by": "github-actions[bot]"`. Confirmed on `main` directly: `pf_bridge@e34bfde` (Merge PR
   #182) and `pirate-force-server@93856bf` (Merge PR #106) are both present in `git log origin/main`.
   No recovery needed this round.

2. **GT-101 queued** (`pf_bridge/GAME_TEST_QUEUE.md`): the GM-001 login-state attended probe that the
   1630 order letter proposed has never actually been queued, even though its precondition
   (`CORE-REQUEST-006` wiring `state_wire.make_gm_update_state_frame` into the real login path) landed
   rounds ago. `docs/GM_LANE.md` and `RE-089-RESULT` both say the remaining question here --
   whether anything visible happens when a GM-listed account logs in -- is attended-capture
   territory, not more static reading, and RE-089 names this exact matrix as its own recommended next
   step without opening it. This round opens it as `GT-101`, written to this repo's exact house format
   (source citations demanding re-derivation not trust, a stage-0/1/2 boot gate including a
   "confirm the GM account allowlist without inventing a name" stage since this lane has no authority
   to add or guess a real account name, wire/DB pass criteria separate from client-observable pass
   criteria, and a nonclaim block making explicit that this is a GM-tool observation, not proof of any
   feature, and that the three payload fields stay unnamed regardless of what the screen does).
   `pf-queue-author` drafted the entry against the live file (source citations, house format, numbering
   check against both `GAME_TEST_QUEUE.md` and `CLIENT_RE_QUEUE.md`'s shared counter -- confirmed
   `GT-101`/`RE-101` both unused); this session performed the actual file write since that subagent's
   tools are read-only in this environment.

3. **Static-RE re-dig on `GM_RunGMCommandVital`'s two wide-string / two-u32 / one-u8 field semantics,
   closed negative.** `CORE-REQUEST-011`/`012` stay blocked (per `CHIEF_CONTINUATION.md` rows 011-012)
   because no command source exists that can turn a real inbound 0x51E9 frame into a `GmCommand` --
   `RE-088` pinned the byte shape but explicitly declined to name field meaning. Before opening a new
   RE ticket for the physical binary, this round dispatched a `pf-static-re` pass over everything
   already committed to both clones (RTTI/class census, `PF_SERIALIZER_FIELDS.tsv` neighbourhood,
   `PF_RUNTIME_CLASSMAP`/`PF_DATA_EVIDENCE`/`PF_TAG_CENSUS`, all of `gamedata/tables`+`gamedata/lua`) to
   check whether anything beyond RE-088/089/090/091 was sitting unread. Result: negative on all four
   angles checked (GM editor widget/command-list RTTI, command-syntax strings, a GM command catalog
   table, missed adjacent registry rows) -- everything found reproduces facts already cited in
   `docs/GM_LANE.md`, and the `GMCommandArg` "kind 0x20" field RE-091 found on the editor-side object is
   confirmed still unconnected to the wire object's `field_0x10`/`field_0x14`/`field_0x18` by anything
   committed to this clone. This is a useful negative: it forecloses re-spending a round's static-RE
   budget on this same question and confirms `docs/GM_LANE.md`'s own conclusion (the semantic gap needs
   a real captured frame or an attended live session, not more reading) rather than assuming it without
   checking. No new RE ticket opened -- the existing open item in `docs/GM_LANE.md`'s "RE requests
   open" section already says this correctly; a fresh ticket would just restate it. Recorded in a
   status letter to chief so R191/future rounds don't re-run this same static search.

## What this round did NOT do

- No new code in `pirate-force-server`'s `gm/` write zone this round -- the productive work available
  (queueing GT-101, closing the static-RE question negative) was documentation/queue-only. This is
  consistent with GM-003's own scope note: command execution stays blocked on either a real capture
  (GT-101 does not produce one -- it observes login state, not 0x51E9 traffic) or a COO decision on a
  console/debug command source, neither of which this round can manufacture.
- Did not open a COO-ASK about a console/debug command source this round -- `docs/GM_LANE.md` names
  this as one of two ways `CORE-REQUEST-011`/`012` could unblock, but GT-101 was the more concrete,
  immediately actionable gap (a probe the order letter itself asked for, whose precondition has quietly
  been met for several rounds with nobody noticing). Flagging the console/debug question as still open
  for a future round rather than opening it half-considered this round.

ผู้เทสจะทำอะไรได้ที่เมื่อวานทำไม่ได้: มีใบเทส `GT-101` ในคิวให้ทำได้ทันที (เมื่อวานไม่มีใบนี้เลยแม้
precondition จะพร้อมมาหลายรอบแล้ว) -- ยังไม่มีโค้ดใหม่ให้รันเกตในรอบนี้

nonclaim: รอบนี้ไม่ได้พิสูจน์หรือหักล้างอะไรเกี่ยวกับพฤติกรรม GM บนจอ -- แค่เปิดใบเทสให้คนไปดูจริง และ
ยืนยันว่าการอ่านสถิตต่อไม่ให้คำตอบเพิ่มเกี่ยวกับความหมายฟิลด์ของ `GM_RunGMCommandVital`

## Round-end status (Addendum v6.2 §C)

push แล้ว รอ merge PR #187 (pf_bridge) และ PR #110 (pirate-force-server, no-code-change/merge-forward
only). ยังไม่ถือว่าอยู่บน main จนกว่ารอบถัดไปจะยืนยัน merged=true ด้วย pull_request_read.
