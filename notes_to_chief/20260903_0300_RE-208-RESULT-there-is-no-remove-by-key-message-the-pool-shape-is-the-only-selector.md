ขอให้ chief กรอก ### result: และปิดหัวใบให้ด้วย

# RE-208 RESULT -- there is no remove-by-key message. The shape of the pool is the only selector.

- ticket: `RE-208 GROUND-POOL-REMOVAL-PATH-FOR-THE-LAST-OBJECT-001`, opened by LANE-B round `9jrsei`
- worked by: **ka1-A (attended)**, at the owner's direct instruction, 2026-09-03 ~02:5x-03:00 (+07:00)
- consumer: **LANE-B** (the ticket says LANE-B consumes its own result)
- method: NOT a fresh disassembly. Per `CLIENT_RE_QUEUE.md` rule 4 the mandatory search of
  `pf_bridge\external\` was run first, it HIT, and the ticket therefore became
  "verify sha -> adversarial re-derive -> use", exactly as that rule prescribes.

## Mandatory search fields

- **ค้นใน `pf_bridge\external\` แล้ว: เจอ** -- `PF_GROUND_DROP_LIFETIME.tsv` (29 rows, 22 IMAGE)
  and `PF_GROUND_DROP_PICKUP_CLOSURE.md/.tsv` already carry this exact question, at VA level.
- **ค้น `gamedata` แล้ว: ไม่เกี่ยว** -- `grep -rl "TerrainThing|DropThingModule" gamedata/`
  returns nothing. The question is in code, not in a shipped table.

## sha verification, before using a single pinned row

| artefact | pinned | measured on disk | verdict |
|---|---|---|---|
| `GameClient\GameClient.local.bin` | `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`, 14,759,424 B | identical, byte size identical | **MATCH** |
| `external\PF_GROUND_DROP_PICKUP_CLOSURE.tsv` | `1cf955edcff6f360735488c8a6e03a91435f1041ba642092f9193fd295348a1c` | identical | **MATCH** |
| `external\PF_GROUND_DROP_LIFETIME.tsv` | (no self-pin in the doc) | `b1703a7f31c42ddebf9702d12a7942577407fc320a9c2ad8411a08f3f017e710` | recorded for the next round to diff against |

---

## LAYER 1 -- the ticket's single question: **NO. There is no remove-by-key / destroy-one path reachable from a distinct message.**

`0x006AF970` is `DropThingModule_Client::reconcile`, and `GDL-IMG-003` binds how anything
reaches it: handler `0x005E40D5` -> bridge `0x005F53A0` -> **its SOLE direct reconcile call
is `0x006AF970`**. There is one door.

Inside that one door, every outcome is chosen by **the shape of the incoming pool**, never by
an opcode of its own. The complete matrix, all IMAGE, all keyed by `TerrainThing+0x10` u32:

| row | pool shape | effect | VAs |
|---|---|---|---|
| `GDL-IMG-007` | pointer **NULL** (bit `0x08` absent) | **REMOVE_ALL** | unregister `0x00B0EE40` -> map erase `0x005E0D40` |
| `GDL-IMG-008` | non-NULL, count `+0x2C` = 0 | **PRESERVE_ALL**, returns through the epilogue without mutating the map | -- |
| `GDL-IMG-009` | non-NULL, count > 0, a live key **omitted** | **REMOVE_OMITTED** | unregister `0x00B0EE40` -> map erase `0x005E0D40` |
| `GDL-IMG-011` | key present in both | **UPDATE_IN_PLACE** | wrapper update `0x005F4C00` |
| `GDL-IMG-006` | incoming key **not** live | **ADD** -- allocates a wrapper, registers it with the world, inserts it | `0x006AF720` -> `0x005F41E0` -> world register `0x00B0E4A0` -> map insert `0x00708E20` |
| `GDL-IMG-010` | distance > 2500 | **REMOVE_OUT_OF_RANGE** (threshold squared = 6,250,000) | -- |
| `GDL-IMG-015` | module event kind `0x0A`, or destructor | CLEAR_EVENT_OR_DESTRUCTOR_RELEASE | wrapper refs `+0x7C/+0x80/+0x84/+0x88/+0x8C` |

**So a keyed erase DOES exist as code -- `0x005E0D40`, keyed by exactly the identity the
ticket cares about -- but nothing outside reconcile can call it.** It is reached only from
NULL, from omission, and from the range predicate. The only way a message removes ONE
object is to send a non-empty pool that omits it. That is `RE-082`'s finding, now with the
VAs of the removal itself rather than of the consumer.

Independent corroboration from tonight's live round R303 (CAPTURE, attended, owner at the
keyboard), which is the first time the removal path was watched end to end on a real wire:

```
MOB_PICKUP_GROUND_REMOVAL_PUBLISHED key=0x100008 rows_left=4  ->  [G>] MOB_PICKUP_GROUND_AFTER (149 bytes)
MOB_PICKUP_GROUND_REMOVAL_PUBLISHED key=0x100007 rows_left=2  ->  [G>] MOB_PICKUP_GROUND_AFTER ( 88 bytes)
```

The frame size scales with the number of rows LEFT, not with the one row removed. That is
the whole-pool republish shape of `GDL-IMG-009`, observed. IMAGE and CAPTURE agree.

## LAYER 2 -- "can a non-empty generation carrying one dummy row retire a real object?" **NO, and it is worse than useless.**

Both halves fire at once:

- `GDL-IMG-009` erases the real key, because it was omitted. That part works.
- `GDL-IMG-006` treats the dummy key as a **new** key: it allocates a wrapper, initialises
  it from TerrainThing, **registers it with the world** and inserts it into the module map,
  retaining render and nameboard resources.

⇒ the dummy does not vanish. **It becomes a real, drawn, nameboarded object on the floor.**
The trick trades one ghost for another and adds a rendered actor. Do not use it.

## What this settles for LANE-B's last-object case -- the reason the ticket was opened

With zero rows remaining there are exactly two shapes available, and both are already in
the matrix:

- **NULL / bit `0x08` absent** -> `REMOVE_ALL`: the whole scene floor is cleared.
- **non-NULL, count 0** -> `PRESERVE_ALL`: nothing is removed, the last object stays as a ghost.

There is no third shape. **LANE-B's current behaviour -- falling back to v141's empty derived
mask when the scene reaches zero rows, so the floor clears in the same frame the item enters
the bag -- is therefore not a workaround or a compromise. It is the only correct option the
client offers.** The `[สมมติของสาย B - รอ COO ยืนยัน]` tag on that branch can come off, and
`test_the_last_object_clears_the_floor_and_says_that_instead` is pinning the right behaviour.

## Two facts LANE-B did not ask for and should have

1. **`GDL-IMG-010`: reconcile removes any ground object farther than 2500 units** (compares
   squared, 6,250,000), unless the audited bypass flag applies. A drop the server still
   believes is live disappears from the client at that distance with no message at all.
   Tonight's drop sat 173-192 units from the player, so it never touched this.
2. **`GDL-IMG-012`: no clock, no time API, no elapsed-time delete predicate** was found in
   any of the named spans -- codec, handler, bridge, reconciler, initialiser, wrapper update,
   destructor. **The client never expires a drop by itself.** That is measured absence in
   hash-pinned spans, not a global proof. It matches exactly what the owner saw tonight: an
   `Energy Cubic Crystal` sat on the floor long past its 120 s server lifetime and only went
   away when something republished. The 120 s in `mob_loot.DROP_LIFETIME_SECONDS` is a
   server-side number the client has never heard of.

## NONCLAIMS

- **I did not disassemble anything this round.** Every VA above is a re-use of a pinned
  Codex IMAGE row whose image sha I verified against the file on disk. If those rows are
  wrong, this letter is wrong in the same way, and nothing here re-derives them
  independently. An adversarial re-derive of the reconcile spans was NOT performed.
- The `ADD` behaviour of an unknown incoming key is `GDL-IMG-006`, an IMAGE row about the
  new-key path. I did **not** find an IMAGE row that states in one sentence "reconcile adds
  unknown incoming keys"; I am composing `GDL-IMG-006` with the reconcile matrix. The
  closure doc's own ADD=13 / ADD+OMIT=10 classification is labelled there as an analytical
  convention over CAPTURE metadata, not as evidence, and I am not leaning on it.
- This says nothing about **server** policy, about who is allowed to issue a removal, or
  about the original server's behaviour. It describes what this client image does with a
  pool it is handed.
- The three pinned unregister/map-delete functions of `GDP-IMG-006` were not re-checked by
  me; I took that row as given.
- `GDL-IMG-012` is a manual static observation in named spans. Absence there is not absence
  in the image.
- Nothing in `src/` was touched, nothing was committed, no header or ledger was edited.
