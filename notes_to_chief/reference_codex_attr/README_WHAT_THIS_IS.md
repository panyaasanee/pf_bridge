# reference_codex_attr - the Codex attr work, on the route that actually travels

Written by ka1-B, 2026-08-31, on Panya's ruling of the same day.

## What is here

Codex (an outside, read-only reverse-engineering worker) writes its attr
deliverables into `pf_bridge/external/`. Nothing in `external/` reached GitHub,
so no cloud lane could read any of it from a clone - the bridge had to paste
excerpts by hand, one letter at a time.

This folder is the fix. It holds:

1. **A mirror of the attr deliverables** - `PF_ATTR_FOR_SERVER.md`,
   `PF_ATTR_FIELD_SEMANTICS.{md,tsv}`, `PF_ATTR_CLASS_CENSUS.*`,
   `PF_ATTR_RUNTIME_FIELDS.tsv`, `PF_ATTR_UI_BINDINGS.tsv`,
   `PF_ATTR_INHERITANCE.tsv`, `PF_A2_ACTOR_CODEC_CORRECTION.tsv`,
   `PF_A2_BASIC_CODEC_CORRECTION.tsv` and the rest of the set.
2. **Decision-grade slices of the two tables that are too big to travel** -
   see the next section.

Generation mirrored here:

    generation_id = 0e9cb92bb01b6b2255dc2284ae582347cd0f97765ac6128675d01e82aad376bd
    image_sha256  = 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623

Check `PF_ATTR_GENERATION_MANIFEST.json` before trusting a row: if the
generation_id there does not match the one in `external/`, this mirror is
stale and someone must re-run the refresh command below.

## Why a mirror and not the real folder

`pf_git_sync.ps1` runs two scans:

| scan | paths | untracked files |
|---|---|---|
| ALLOWLIST | `notes_to_chief`, `evidence_screens`, `rounds`, `tools_bridge` | **carried** (`--untracked-files=all`) |
| SHARED_TRACKED | `AGENTS.md`, `.gitignore`, `external`, `gamedata`, `staged`, ... | **not carried** (`--untracked-files=no`) |

`external/` is in the second list, so a file there travels only once it is
already in the git index - and on top of that `.gitignore` denied everything
under `external/` except nine named members. `notes_to_chief/` is in the first
list, so a new file here travels on the next 2-minute round with no git step.
This is the same route ka1-A used for `reference_adhoc_probe/` on 2026-08-28.

`.gitignore` was also widened on 2026-08-31 to name the attr deliverables, so
they MAY be tracked in `external/` from now on. Until someone stages them from
the Windows side, this mirror is what the lanes actually get.

## The two tables that never travel

| file | size | rows |
|---|---|---|
| `external/PF_ATTR_CONFLICTS.tsv` | ~3.4 MB | 1,274 |
| `external/PF_ATTR_UNRESOLVED.tsv` | ~2.3 MB | 963 |

Both exceed the 2 MB cap in `pf_git_sync.ps1` (`$SIZE_LIMIT_BYTES`). Listing
them in `.gitignore` would only produce a refusal line every round, so they
stay on the bridge disk and these derived slices travel instead:

- **`PF_ATTR_CONFLICTS_HEADLINE.txt`** - the counts, read this first.
- **`PF_ATTR_CONFLICTS_BUCKETS.tsv`** - every `conflict_kind` x
  `resolution_status` pair with its row count and who has to decide it. This
  is the map: 1,274 rows collapse into a handful of policy families.
- **`PF_ATTR_CONFLICTS_OPEN_WIRED.tsv`** - the 68 still-open rows that touch
  `ActorAttr` or `BasicAttr`, the only two classes the live server encodes
  today. Every other open conflict is on a class we do not wire yet, so it is
  a documentation question, not a release blocker. Read this one before any
  attr wiring change.
- **`PF_ATTR_UNRESOLVED_BUCKETS.tsv`** - the unresolved table reduced to
  `unresolved_kind` x `class` x `scope_status` x first clause of `blocker`.

Nothing in these slices re-derives or reinterprets a Codex claim. They only
count and filter rows, and every line keeps its `conflict_key` /
`unresolved_key` so it can be traced back to the full table on the bridge.

## Refreshing after a Codex round

From the `pf_bridge` folder:

    python tools_bridge\pf_attr_conflict_digest.py

That regenerates the four slices and re-copies any mirrored file whose bytes
changed. It writes nothing outside this folder and runs no git command.

## What this folder is NOT

- Not a source of truth. `external/` on the bridge disk is.
- Not evidence at the client-observable layer. Everything here is IMAGE-layer
  (static binary) analysis. Probe results are the other layer and live in
  `reference_adhoc_probe/`. Do not mix a claim from one layer into the other
  without saying which layer it came from.
