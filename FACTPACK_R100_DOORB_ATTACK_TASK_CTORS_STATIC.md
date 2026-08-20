# R100 Agent A - Door B statics (the other half)

Binary of record: GameClient/GameClient.local.bin
sha256 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
Image base 0x400000.

## Format + VA<->file-offset mapping [STATIC]

- File is a normal on-disk PE (starts with 'MZ', pefile parses it). It is NOT a
  raw dumped image: section RawPtr != VirtualAddress, so mapping must go through
  the section table, not `off = VA - base`.
- Sections (VA / VSize / RawPtr / RawSize):
  - .text  0x401000 / 0x838a2c / 0x400    / 0x838c00
  - .rdata 0xc3b000 / 0x3de38e / 0x839400 / 0x3de400
  - .data  0x101a000/ 0x81f70  / 0xc17800 / 0x11e00
  - .rsrc  0x109c000/ 0x58998  / 0xc29600 / 0x58a00
  - .reloc 0x10f5000/ 0x1915f0 / 0xc82000 / 0x191600
- Mapping used everywhere below: file_off = RawPtr + (VA - ImageBase - SectVA),
  bounded by RawSize. Verified: VA 0xF0F060 -> "_F_DIE_000" stored as UTF-16LE
  ("_\0F\0_\0D\0I\0E\0..."), matching the known anchor. All animation literals
  in this image are wide (UTF-16LE) strings.
- Tooling: capstone (CS_MODE_32) + pefile. Helper scripts copied read-only to
  /tmp/pf and adapted (Windows paths replaced); originals untouched.

Key generic mechanism discovered (used by Q1 and Q2):
Every game class registered by the two RTTI registrars carries an MSVC-format
type-descriptor (".?AV<Name>@@" in .data) plus a per-type "token record" object
in .data (record vtable 0xf36384, shared). A class's virtual method slot-0
("GetType") is a 5-byte thunk `mov eax, <token>; ret`. Because each ctor/GetType
references its own token, class name <-> vtable <-> ctor CAN be bound statically
even though there are no MSVC Complete-Object-Locators (COLs) wiring vtable->name.
Derivation of the token->name table: scan for the registrar stub
`... mov ecx,<TD>; call [0xc3b7ac]; push eax; push <token> ...` and read the name
at TD+8. This reproduced the known Dead=0xF0F048 anchor exactly.

=====================================================================
## Q1 - CActorTask_UseBehavior and CActorTask_PlayActionEvent
=====================================================================

### Ctor cluster enumeration (KIND writes) [STATIC]
Byte-scan of 0x472000-0x476000 for `mov dword [esi+0x10], 0x800000XX`
(C7 46 10 XX 00 00 80). 11 genuine ctor KIND stores (others in a raw imm scan
were decode-misalignment: `and/or/test/call`). Each paired with the vtable the
same function installs via `mov [esi], <vt>` (C7 06):

  KIND store VA   vtable     KIND        (vtable install VA)
  0x472558        0xf0eec8   0x80000004  (0x47250c)
  0x472827        0xf0f048   0x80000005  (0x47281d)  <- CActorTask_Dead (anchor)
  0x472ab6        0xf0f090   0x80000006  (0x472a61)
  0x472d94        0xf0eee0   0x80000006  (0x472d80)
  0x473341        0xf0f334   0x80000002  (0x473311)  <- CActorTask_TracePath*
  0x474487        0xf0f420   0x80000005  (0x474461)
  0x474b23        0xf0f444   0x80000005  (0x474b1d)  <- CActorTask_Stun*
  0x475704        0xf0f530   0x80000006  (0x4756d4)
  0x475863        0xf0f548   0x80000006  (0x475825)
  0x475f54        0xf0f578   0x80000006  (0x475f24)
  0x475ff3        0xf0f590   0x80000005  (0x475fed)
Counts match the anchor: KIND 5 -> 4 vtables, KIND 6 -> 5 vtables.
(*names via the token-binding method below.)

IMPORTANT: UseBehavior and PlayActionEvent are NOT in this 0x800000XX group and
their ctors are at 0x471xxx / 0x47axxx (below/outside the 0x472000 window). They
use [task+0x10] as a small flags word, not a 0x800000XX prototype code (see the
UseBehavior ctor writing [task+0x10]=8 at 0x47abea).

### Name -> ctor -> vtable binding [STATIC]
Type name strings live in .data: ".?AVCActorTask_UseBehavior@@" @ 0x101cec0
(TD 0x101ceb8), ".?AVCActorTask_PlayActionEvent@@" @ 0x101cfc0 (TD 0x101cfb8).
No MSVC COL references either TD (searched; 0 hits) -> confirms the anchor
"vtable->name NOT statically resolvable" via MSVC RTTI. BUT each TD is referenced
once by the actor-task registrar (UseBehavior TD ref @ 0xbd1236, PlayActionEvent
TD ref @ 0xbd13f6), and each registrar stub binds the name to a per-type token:
  - UseBehavior token record = 0x102ed50 (registrar stub @ 0xbd1230)
  - PlayActionEvent token record = 0x102ecfc (registrar stub @ 0xbd13f0)
Then the token is referenced from the class's own GetType thunk:
  - 0x471dc0: `mov eax, 0x102ed50; ret`  -> UseBehavior GetType
  - 0x471f50: `mov eax, 0x102ecfc; ret`  -> PlayActionEvent GetType
These thunks are vtable slots, giving the final binding:

CActorTask_UseBehavior [STATIC]
  - vtable      0xf0ef10   (installed by dtor @ 0x471d20 [mov [esi],0xf0ef10 @
                            0x471d48] and by the real ctor @ 0x47ab30
                            [mov [esi],0xf0ef10 @ 0x47ab96])
  - ctor        0x47ab30   (thiscall, `ret 0x30` = 12 dword stack args)
  - dtor        0x471d20
  - GetType     0x471dc0 (vtable slot 0) -> token 0x102ed50
  - KIND/flags  [task+0x10] = 8  (0x47abea: mov dword [esi+0x10], 8)

CActorTask_PlayActionEvent [STATIC / partial NEGATIVE]
  - vtable      0xf0ef28
  - dtor        function @ ~0x471e90 (installs 0xf0ef28 @ 0x471ef0)
  - GetType     0x471f50 (vtable slot 0) -> token 0x102ecfc
  - ctor        NOT FOUND as a standalone function. A whole-file scan for the
    4-byte value 0xf0ef28 finds it referenced ONLY at 0x471ef0 (its own dtor).
    Interpretation: PlayActionEvent is the BASE task; concrete instances observed
    are the derived UseBehavior, whose ctor writes the derived vtable 0xf0ef10
    directly. UseBehavior vtable 0xf0ef10 slots [6..13] == PlayActionEvent vtable
    0xf0ef28 slots [0..7] (identical function pointers 0x471f50,0x47b350,
    0x475170,0x475290,0x475320,0x4a0880,0x472050,0x47b800), i.e. UseBehavior
    embeds/derives-from PlayActionEvent. [STATIC]

### Consumer chain walk [STATIC]
The audited chain 0x47CAD0 / 0x48D270 / 0x48D870 does NOT call any task ctor
directly. Instead:
  - 0x48D870 (CHitResult reaction factory): gets a behavior row via 0x702A10
    (fallback 0x48AE40 @ 0x48d8cc), then builds VISUAL hit-reaction effects from
    the row's sub-arrays (row+0xe4/0xf0/0xf4), driving effect keys via the effect
    pool ctor 0x442d50 with pool 0x102dca4 (strings 0xf13e14 / 0xf13df4 /
    0xf13dd4 pushed at 0x48dac5/0x48daf5/0x48db10). This is the on-hit visual
    path, not the task-construction path.
  - 0x48D270: iterates the behavior row's sub-arrays (row+0x90,0xc0,0xd8,0xf0,
    0x108) and dispatches construction through VIRTUAL methods of its `this`
    (ebx): [ebx]+8 builds a root, [ebx]+0x18/0x1c/0x20/0x24/0x34 build sub-parts.
    The concrete task type therefore depends on ebx's runtime vtable, not a
    static call target. 0x47CAD0 just wraps 0x48D270's result in the flags
    wrapper (vtable 0xF0F7DC installed @ 0x47cb47), matching the anchor.
So the "builder" indirection means the audited chain alone cannot name the task
ctors -> that is why the token-binding method above was needed. [NEGATIVE on the
direct-call approach; the token method is the resolution.]

### Who actually constructs UseBehavior, and the actor gates [STATIC]
Direct CALL xrefs (E8 rel32) to ctor 0x47ab30:
  0x42514f 0x42b815 0x42c0c4 0x44d1fc 0x44d5c4 0x453d82 0x47b989 0x47ba83
  0x751809 0x751aa1
The clean, behavior-vital path is 0x751809, inside the vital consumer 0x7516c0:

  0x7516e5  mov esi, ecx                  ; esi = the vital
  0x7516e7  mov eax,[esi+0x1c]            ; actor handle hi
  0x7516ea  mov ecx,[esi+0x18]            ; actor handle lo
  0x7516ef  call 0x402a20                 ; handle -> raw
  0x7516f6  call 0x446170                 ; -> resolved actor object
  0x7516fb  mov edi, eax                  ; edi = TARGET actor
  0x7516ff  je 0x7519d6                   ; bail only if actor not resolvable
  0x751705  cmp dword [esi+0x30], 0xea80  ; behavior/action id switch
  ...default path (id != 0xea80/0xea82/0xea83)...
  0x751756  call 0x4162a0 ; 0x75175f call 0x4889d0 (is-known-action? test al)
  0x75176f  mov eax,[0x1032ec4]           ; localplayer singleton (see Q4)
  0x751778..0x75179f: if this actor == localplayer AND a match, SKIP (0x7519d6)
  0x7517b0  call 0x702a10                 ; BEHAVIOR row lookup
  0x7517c1  call 0x442d50 (pool 0x102dca4, size 0x78) ; alloc task object
  0x7517da..0x751806 push args from the vital (esi+0x20,0x24,0x28,0x2c,0x30,
             0x34,0x38,0x3c,0x48) + push 0 + push edi (the actor)
  0x751807  mov ecx, eax                  ; this = new task
  0x751809  call 0x47ab30                 ; <-- UseBehavior ctor

Argument shape passed to the ctor: (actor `edi`, 0, and ~9 fields copied out of
the vital object: two int params +0x20/+0x24, a byte +0x48/selector, a vec3 pack
+0x38.., a float +0x48, etc.). The behavior ROW pointer itself is consumed by
0x702a10 earlier; the ctor receives the ACTOR and the vital's scalar params, not
the row pointer. No animation-string pointer is passed at this call site (the
default anim fallback 0xf0da12 is chosen inside the ctor @ 0x47abd3 when a param
is 0).

Actor-type gates on the construct path:
  1. On the caller (0x7516c0) DEFAULT path: NONE that exclude NPCs. The only
     skip is the localplayer-identity special case at 0x75176f-0x75179f (skips
     construction when the actor IS the tracked/local actor under a match). The
     0xea80 branch (0x751705) has a `not CMyActor` check (0x751717 push
     0x102cb04=CMyActor; call is-a 0x88f2b0) but that is a different, special
     branch, not the default UseBehavior path.
  2. INSIDE ctor 0x47ab30:
     - base ctor 0x485d40 stores the actor arg into [task+0x1c]
       (0x485d4c: mov [esi+0x1c], eax) and installs CActorTask base vtable
       0xf13784.
     - vtable 0xf0ef10 and [task+0x10]=8 are written FIRST (0x47ab96, 0x47abea).
     - Gate A @ 0x47ac01-0x47ac22: virtual GetType on [task+0x1c] (the actor),
       then `push 0x102ce88; call 0x88f2b0` (is-a). Token 0x102ce88 =
       ".?AVCActorBaseClient@@" -- the ROOT client-actor base. Every client
       actor (CMyActor, CNetActor, and a server-projected CNetNPC) derives from
       it, so this gate PASSES for a projection. On failure it `je 0x47ae91`.
     - Gate B @ 0x47ac28: `mov eax,[esi+0x1c]; mov eax,[eax+0x14]; cmp eax,0;
       je 0x47ae91`. So it also needs [actor+0x14] != 0 (an actor
       render/animation sub-component; the same +0x14 field is read by the
       knockdown consumer 0x750700 @ 0x75071e and by the PlayActionEvent dtor @
       0x471ea0).
     - BAIL target 0x47ae91 simply does `mov eax, esi; ...; ret 0x30` -- it
       RETURNS THE FULLY-ALLOCATED TASK. The gates only skip the optional
       animation-model wiring (setting [task+0x50], calling 0x484450/0x484850);
       they do NOT prevent the task object, its vtable, or its KIND from
       existing.

### Q1 answer to the key question [STATIC]
YES -- a behavior-id-bearing vital CAN construct a UseBehavior/PlayActionEvent
task for a projected CNetNPC. Evidence:
  - The target actor is resolved purely from a handle in the vital via
    0x402a20->0x446170; a projected NPC that is visible/registered in the client
    actor table resolves normally.
  - The construct path has NO actor-type gate that excludes NPCs. The only
    in-ctor type gate is an is-a check against CActorBaseClient (the universal
    client-actor base) which every projection satisfies.
  - Task existence (vtable 0xf0ef10 + [task+0x10]=8) is committed BEFORE any
    gate; even when the inner gates fail the ctor still returns a valid task
    (bail path 0x47ae91). The only thing a bare projection can lose is the
    optional animation-model init, which is skipped if the projection lacks the
    [actor+0x14] render/anim sub-component.
  - No branch requires "is local player", any server-authority flag, or a
    specific NPC subtype.
Driving vital: the consumer 0x7516c0 sits in a vital vtable in .rdata
(pointer @ 0xf48a08); its neighbouring GetType thunks resolve to
".?AVCFightMsgVital@@" (token 0x108a2bc) -- i.e. this is the combat/fight-message
vital, consistent with "attack task". (Vital naming is [STATIC] via the adjacent
GetType thunk but the exact MI sub-object owning slot 0xf48a08 was not
disassembled to byte precision -> treat CFightMsgVital as high-confidence, not
proven-to-the-adjustor.) The knockdown consumer 0x750700 sits at the sibling
slot 0xf48abc.

=====================================================================
## Q2 - CAIStateCombatProxy / AI FSM server-authority
=====================================================================

### AI type descriptors: xrefs [STATIC]
AI type-name TDs and their ONLY pointer references (whole-file dword scan):
  .?AVCAIControler@@   TD 0x102284c -> ref 0xbda306 (registrar) ONLY
  .?AVCAICondition@@   TD 0x1022868 -> ref 0xbda346 (registrar) ONLY
  .?AVCAIBehavior@@    TD 0x1022884 -> ref 0xbda386 (registrar) ONLY
  .?AVCAIState@@       TD 0x10228a0 -> ref 0xbda3c6 (registrar) ONLY
  .?AVCAIState_Dead@@  TD 0x10228b8 -> ref 0xbda406 (registrar) ONLY
  .?AVCAIStateRamble@@ TD 0x10228d4 -> ref 0xbda446 (registrar) ONLY
  .?AVCAIStateCombat@@ TD 0x102293c -> ref 0xbda506 (registrar) ONLY
  .?AVCAIStateCombatProxy@CAIStateCombat@@ TD 0x1022960 -> ZERO refs anywhere
  .?AVMobLuaProxy_Client@@ TD 0x1021ea8 -> ref 0xbd8636 (registrar) ONLY
  .?AVPatrolPath@@     TD 0x1021748 -> refs 0xbd7b76 (registrar) AND 0x4388dc
CONFIRMS the anchor "zero live xrefs outside the registrar" for the AI-control /
AI-state / combat descriptors. Only exception in the family: PatrolPath has one
non-registrar ref (0x4388dc) -- pathing is live, combat-FSM typing is not.

### AI vtables and virtual methods [STATIC]
Token records: CAIState = 0x102d090, CAIStateCombatProxy = 0x102d100,
CAIStateCombat = 0x1079fb8.
  - CAIState: vtable 0xf14a70 exists (GetType 0x4a0740 `mov eax,0x102d090;ret`;
    ctor/deleting-dtor 0x4a08a0 installs 0xf14a70). It has ~9 real virtual method
    slots (0x4a0740,0x4a08a0,0xa9a560,0x73d360,0xa9a560,0x4a0880,0x4a0c70,
    0x4a0f80,0x4a12c0). The BASE AI-state machinery is present.
  - CAIStateCombatProxy: vtable 0xf14958, but only TWO real slots -- GetType
    0x49c210 (`mov eax,0x102d100;ret`) and a deleting-destructor 0x49c230; the
    rest of the "array" is ASCII string data (a stub). Its ctor 0x49c220 is
    trivial: `mov [eax],0xf14958; ret` (installs vtable, no field init). ALL
    references to vtable 0xf14958 are confined to the 0x49c200-0x49c250 stub
    cluster (0x49c202/0x49c224/0x49c23a) -- nothing else in the image constructs
    it or calls its methods.
  - CAIStateCombat (the non-proxy): token 0x1079fb8 has NO GetType thunk
    (`mov eax,0x1079fb8;ret` does not exist in the image) and NO vtable install;
    its only .text refs are the registrar stub (0xbda517/0xbda527) plus one
    atexit thunk (0xc29d01). It is a NAME-ONLY registration -- completely inert
    client-side.

### Q2 deliverable [STATIC]
CONFIRM: combat is not driven by a client-side CAIStateCombat FSM. The
CAIStateCombat node is a name-only RTTI registration with no vtable, no ctor,
and no instances; CAIStateCombatProxy is an inert stub whose only methods are
GetType and a deleting-destructor -- there are NO tick/enter/update virtual
methods and therefore NO reads of any field (server/wire OR local state) for
combat decisions on this FSM. Because the client's combat-state class carries no
behavioral logic, combat state is not decided by this client FSM (consistent with
server-authoritative combat and/or the CActorTask/behavior projection of Door B).
An honest boundary: the base CAIState (0xf14a70) IS a live class with real
virtual methods; I did not disassemble those to prove they carry no combat logic
-- the claim above is scoped specifically to the CAIStateCombat / *Proxy nodes
named in the anchor, which are provably inert.

=====================================================================
## Q4 - singletons [0x10339B0] and [localplayer+0x420]
=====================================================================

### [0x10339B0] [STATIC]
Class: this global holds a pointer to a CMacroActionFactory instance
(vtable 0xf140e8, GetType 0x491ca0 -> token 0x102ee9c = ".?AVCMacroActionFactory@@").
Writers (dword scan for A3/89-05 stores): 0x491c65 and 0x491d0c.
  - 0x491c65 is inside the factory DESTRUCTOR (0x491c20): `cmp [0x10339b0],esi;
    jne; mov [0x10339b0], eax(=0)` -> clears the singleton when the active
    factory is destroyed.
  - 0x491d0c sets it (`mov [0x10339b0], esi`) when a factory registers.
Readers (5 genuine, others misaligned): 0x47b220, 0x491c5d, 0x5cae00, 0x5cdf40,
0x753cf0. All are NULL-gates for the macro-action record/playback feature, e.g.:
  - 0x47b220: only after `[0x1032ec4]==[task+0x1c]` (localplayer's own task);
    `mov ecx,[0x10339b0]; test ecx; je skip` -> macro interception is
    local-player only.
  - 0x5cdf40 / 0x753cf0: `cmp [0x10339b0],0; jne ...; <default true/false>` --
    if null, macro interception is off and the default action is taken.
What it gates: macro-action (user action macro) recording/playback interception,
local-player scope. It is NOT on the damage-number / HUD path. The primary
damage-number sprites go through the CHitResult factory 0x48D870 using pool
0x102dca4 and are gated only by the behavior row / reaction flags, not by
[0x10339B0]. => [0x10339B0] canNOT silently suppress damage-number/HUD draw.

### [localplayer+0x420] [STATIC]
localplayer global = [0x1032ec4] (2013 reads, 3 writes; the writer 0x44c4ea
clears it to null when the CMyActor is destroyed -- classic singleton). It is the
local CMyActor pointer.
[localplayer+0x420] is a single BYTE flag:
  - Init: 0x44cac2 `mov byte [esi+0x420], 1` (in the CMyActor construction region
    0x44cxxx) -> defaults ON.
  - Toggle: command handler at 0x42c674 does
    `mov eax,[0x1032ec4]; cmp byte [eax+0x420],bl(0); sete cl;
     mov byte [eax+0x420], cl` -> flips 0<->1 (a client keybind/command case;
    dispatched in a switch, sibling case 0x42c695 tests id 0x29).
  - Gate: 0x43fe25 `mov eax,[0x1032ec4]; test eax; je out; cmp byte
    [eax+0x420],0; je out` -> the whole body of function 0x43fde0 runs ONLY when
    the flag is set. 0x43fde0 is CALLED from the fight-vital consumer (0x75161f).
    Its body does friend/foe relation checks (same predicates 0x7504a0 /
    0x750590 / 0x7505d0 as the knockdown consumer) and calls text/UI helpers in
    the 0xa7xxxx range (0xa78f30/0xa79cf0/0xa7b6c0). It does NOT touch the
    damage-number pool 0x102dca4 (0 references in its 0x400-byte body).
What it gates: a per-hit combat-feedback / floating combat-text routine (the
0x43fde0 path invoked during fight-vital processing), toggled by a local
command. Setting it to 0 WOULD silently suppress THAT combat-text/feedback draw
(no error path -- both readers just fall through to `ret`). It does NOT gate the
primary damage-number sprites (those are ungated by this flag), so it cannot
silently blank the core damage numbers, only the secondary combat-text feature.

### Q4 short answer [STATIC]
Neither singleton can silently suppress the CORE damage-number/HUD draw:
  - [0x10339B0] gates macro-action interception (CMacroActionFactory), not HUD.
  - [localplayer+0x420] is a local, default-on, user-toggleable boolean that
    gates a secondary combat-text/feedback routine (0x43fde0) during fight-vital
    processing; toggling it off silently drops that feedback but not the damage
    numbers themselves (pool 0x102dca4 path is not gated by it).

=====================================================================
## FILES TOUCHED
=====================================================================
- outputs/r100_agentA_doorb_statics.md  (this file - the only deliverable
  written; path as requested:
  /sessions/friendly-dreamy-hopper/mnt/outputs/r100_agentA_doorb_statics.md)
- /tmp/pf/*  (scratch only: pfmap.py, func.py, rtti.py, tokrefs.txt, and
  read-only copies of the original helper scripts msvc_rtti.py / list_vtables.py
  / string_xrefs.py etc.; originals in the backups tree were NOT modified)
No git operations. No server/UI/LOCK files. The sqlite state file was not touched.
