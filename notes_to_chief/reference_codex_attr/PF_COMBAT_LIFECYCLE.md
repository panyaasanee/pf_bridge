# PF combat lifecycle - source-separated client checkpoint

This report publishes 34 deterministic rows from the pinned original client IMAGE and pinned original DATA only. Each TSV row carries exactly one evidence layer; no server/emulator code is evidence in the lifecycle table, and no raw client bytes are exported.

- Image SHA-256: `9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`
- Rows: 34 (`IMAGE` 26; `DATA` 8)
- Semantic status: exact 27; role-only 5; unknown 2

## Proven ordering and surfaces

- A valid ActionVital `+0x30` value is the behavior-selector surface: lookup `0x00702A10` precedes `CActorTask_UseBehavior` construction at `0x0047AB30`.
- A lethal actor-entry update must target an identity already present in the actor map. The first unknown-identity entry spawns through `+0x10`; only a later same-identity entry can dispatch `+0x20` into dead-state sync.
- CHitResult resolves target identity and consumes signed `+0x08`. Its frozen handler has no direct E8 edge to the pinned HP/death entry points; indirect, virtual, and transitive effects remain open.
- The target panel opens through client-local identity/event/relation/CNetNPC logic. Separate widget functions consume BasicAttr name and HP, but their relative dispatch order versus panel open remains unknown. TargetVital's registry/vtable-bound inbound slot is a no-op.

## Still open

- CHitResult versus HP actor-entry arrival order, original-server cadence, original-server death hold, exact equipment-dependent behavior selection, and original-server acknowledgement remain `UNKNOWN`.
- The pinned DATA maps equipment types `1/2/8/16/32/64` to behavior IDs `280/284/288/282/290/286`; behavior ID `60029` is absent. `n_MOB_CD=0` on those rows does not prove cadence.
- CAPTURE, attended-test, replacement-server, and owner-testimony claims are intentionally excluded from this IMAGE/DATA artifact; consult the separately sourced audit/checkpoint instead.

## Probe gate

[LOCAL TOOLING] This generator revision adds no probe request. The TSV rows retain their exact blockers and required-next-evidence fields; no IMAGE/DATA claim is promoted by a proposed or attended probe here.

## Server-code conflicts

Two current production-code disagreements are recorded separately in `PF_ATTR_CONFLICTS.tsv` and resolve to `PF_COMBAT_LIFECYCLE.tsv`; server code is not copied into or treated as evidence by the lifecycle TSV.
