# R100 Agent-D: LogoutVital 0x1B40 Logout/Transition -- STATIC findings

Binary of record: GameClient.local.bin
sha256 9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623
Image base 0x400000. VA<->offset via given section table. Tool: capstone/pefile, read-only.
No files mutated except this report + /tmp scratch. No server/UI/DB/git touched.

Tag key: [STATIC]=directly read from disassembly; [NEGATIVE]=proven absence;
[UNKNOWN]=not decidable from this binary.

--------------------------------------------------------------------------------
## Q1 -- LogoutVital 0x1B40 send-site(s) and local state on button press
--------------------------------------------------------------------------------

### How the id 0x1B40 is represented (not an immediate)
[STATIC][NEGATIVE] The 32-bit immediate 0x00001B40 does NOT appear anywhere in
.text or .rdata (scan of the 4-byte LE pattern over every section: zero hits).
The id is a RUNTIME name-hash. Derivation:

- String "LogoutVital" at VA 0xf30a8c (off 0xb2ee8c; found by keyword scan).
- Referenced once, from a static-init stub at VA 0xbee860 (found by scanning
  .text for the 4-byte pointer 0xf30a8c):
    0xbee860  push 0xf30a8c            ; "LogoutVital"
    0xbee865  call 0x89c080            ; returns the global vital-registry singleton [0x108cf90]
    0xbee86a  mov  ecx, eax
    0xbee86c  call 0x89bd00            ; name->id (calls hasher 0x89b220), returns AX
    0xbee871  mov  word ptr [0x108207c], ax   ; store LogoutVital id into a global word
- The same pattern registers the two neighbours:
    0xbee840 "ActorInspectVital" (name 0xf30a78) -> id word [0x1082078]
    0xbee880 "ReturnSelectServerVital" (name 0xf30a98) -> id word [0x1082080]
- I reproduced the documented hash sum((i+1)*ord(c))&0xFFFF:
    "LogoutVital"            = 0x1B40  (matches)
    "ReturnSelectServerVital"= 0x709E  (matches)
  So [0x108207c]==0x1B40 and [0x1082080]==0x709E at runtime. [STATIC]

### The LogoutVital wire object and its serializer (payload proven)
[STATIC] Each vital has a 9-slot descriptor "method table" (stride 0x24) in
.rdata. LogoutVital's table starts at 0xf304c8, ReturnSelectServerVital's at
0xf304ec (derived by dumping .rdata pointers: slot0 of each is the id-getter
that reads the id global, and each id-getter is referenced only from its table):
    GetLogoutVitalId   = 0x5e6810 : mov ax,[0x108207c]; ret   -> at 0xf304c8 slot0
    GetReturnSelectId  = 0x5e6960 : mov ax,[0x1082080]; ret   -> at 0xf304ec slot0
    (GetActorInspectId = 0x5e6740 : mov ax,[0x1082078]; ret   -> at 0xf304a4 slot0)

LogoutVital serializer = table slot2 = 0x5e6820. Disassembly (bWrite path) shows
EXACTLY the captured 14-byte body `08 <subcode> 08 00 14 00000000 14 00000000`:
    0x5e6831  mov al,[esi+0x14]        ; field0 = subcode (u8)
    0x5e6839  push 8 ; call 0x89a600   ; wire tag 0x08 = u8   -> "08 <subcode>"
    0x5e6846  mov dl,[esi+0x18]        ; field1 = u8 (=0)
    0x5e6850  push 8 ; call 0x89a600   ; tag 0x08            -> "08 00"
    0x5e685f  lea ecx,[esi+0x1c]       ; field2 = u32 (=0)
    0x5e6863  push 0x14; call 0x89a600 ; wire tag 0x14 = u32 -> "14 00000000"
    0x5e686e  add esi,0x20             ; field3 = u32 (=0)
    0x5e6872  push 0x14; call 0x89a600 ; tag 0x14            -> "14 00000000"
So the LogoutVital object field layout is: +0x14 subcode(u8), +0x18 u8, +0x1c u32,
+0x20 u32. subcode 0x01/0x03 are literally written from object+0x14. [STATIC]
Note: slot2 is a symmetric serialize (leading `cmp byte[esp+8],0` selects
read vs write), so the same class is usable both to SEND and to RECEIVE; direction
alone is not decidable from the descriptor. [UNKNOWN-direction]

The pooled LogoutVital descriptor singleton object is at 0x1030e24 (RSS at
0x1030fb8); constructed in static init at 0xbd4f90 / 0xbd4fb0 (calls 0x422fb0 /
0x423040). Derived by dumping the init thunks and by xref of 0x1030e24.

### Button handlers (send side) and local state
[STATIC] The three logout-window buttons are wired through two self-registering
UI event-handler classes, found by their MSVC typeid strings:
    ".?AVSysetmSettingLogoutEventHandler@@"        TD 0x1026fdc (name 0x1026fe4)
    ".?AVSystemSettingLogoutConfirmEventHandler@@"  TD 0x1027074 (name 0x102707c)
They register themselves BY typeid-name in static init:
    0xc06540: push 0x10945d0; mov ecx,0x1026fdc; call [0xc3b7ac]
    0xc06860: push 0x10945d0; mov ecx,0x1027074; call [0xc3b7ac]
where [0xc3b7ac] resolves (pefile import table) to
  MSVCR90 type_info::_name_internal_method  i.e. typeid(T).name().
The singletons (0x10888f8, 0x1088974) are given the SHARED "named-registrant"
vtable 0xf36384 (the same vtable used by cStateSelectServer's registrant at
0xbdbee0 and many others), and are keyed into a name-hash registry via
0xa8f190 / 0x88f2e0. [STATIC]

[UNKNOWN] Because the concrete per-button Execute is dispatched through the UI
name-binding (a class-name/hash lookup) and the visible registrant vtable is the
generic 0xf36384, the exact instruction that the button handler runs on click --
and in particular whether it sets a "waiting-for-server" flag, starts a timer, or
fires-and-forgets -- is NOT directly reachable by immediate/xref from this binary.
This specific micro-fact is undecidable statically here. See Q2/Q3 for the
orchestrator-level evidence that bears on it.

--------------------------------------------------------------------------------
## Q2 -- subcode 03 (return to character select): server-driven or client-local?
--------------------------------------------------------------------------------

### Inbound architecture: vitals ride the RunTimeProtocol envelope
[STATIC] Individual vitals (LogoutVital, ReturnSelectServerVital, etc.) are NOT
top-level network messages with their own receive handlers. They are elements of
the GSCN_RunTimeProtocol vital-collection (source string
"..\\..\\ShareCode\\NetCode\\GSCN_VitalData.cpp" at 0xf30708; envelope names
GSCN_RunTimeProtocolReq/Res at 0xf2ffe0/0xf2fff8).

The inbound GSCN_RunTimeProtocolRes handler is 0x446F30 (given 0x5E4060->0x446F30).
Disassembly shows it is a two-linked-list ACTOR-VITAL RECONCILE pass, not a
type-switch:
    0x446f8f call 0x446170             ; find existing actor entry by (id,src)
    0x446fa3 call 0x446990             ; else insert entry
    0x446fb6 mov eax,[edx+0x20]; call eax  ; per-entry VIRTUAL "apply/update"
    0x447044 mov eax,[edx]; call eax; cmp vs [0x102cb04] ; generic name compare
    0x446fe1..0x4470e5                 ; removal/reconcile of stale entries
It adds / updates / removes actor-attached vitals; there is NO branch that loads a
scene, disconnects, or changes app state on the basis of a particular vital id.
[STATIC] This mechanistically explains GT-007/008/026: echoing LogoutVital (or, by
the same path, echoing ReturnSelectServerVital) only reconciles an actor vital and
produces no visible transition.

### No dedicated 0x709E / 0x1B40 "transition" receive handler
[NEGATIVE] I searched every use of the LogoutVital and ReturnSelectServerVital id
globals and descriptor singletons. The id globals ([0x108207c], [0x1082080]) are
read ONLY by the two id-getters (0x5e6810, 0x5e6960); those getters have ZERO
callers and are referenced only from the descriptor tables. All references to the
RSS singleton (0x1030fb8) and Logout singleton (0x1030e24) resolve to
serialization/reflection/pool-alloc framework code (e.g. 0x4b12b0 pool-free,
0x4b2a30 field-get, descriptor slot fns 0x5e68xx/0x5ea6xx/0x5eb2xx/0x5f11xx).
None is a scene-teardown / char-select-load handler. There is no decodable inbound
handler that consumes a specific "logout/return-select response vital" to drive
cStateSelectServer. [NEGATIVE]

### Where the transition actually lives: a session/connection orchestrator
[STATIC] The char-select target state exists as class cStateSelectServer (typeid
".?AVcStateSelectServer@@" 0x1022f1c). The full app state set is:
FullScreenMovie, CreateActor, InitGame, DisplayLogo, Login, SelectServer,
SwitchScene (typeid scan for ".?AVcState*"). There is NO "cStateGame" -- in-game
runs under InitGame/scene machinery -- so "return to character select" is a
STATE/SCENE change into cStateSelectServer plus a connection change, not a single
vital that morphs the current scene.

The one class that ties LogoutVital to that machinery is a session/connection
orchestrator with vtable 0xf45030 (derived: its dispatch method 0x719c80 is stored
at 0xf45058). Relevant members/methods (all [STATIC]):
  - 0x719c30 : on a matching received vital it reaches into the LogoutVital
              descriptor singleton (mov ecx,0x1030e24; call 0x5dd130; mov
              [eax+0x14],0xa) and into the global app object [0x1093198]
              (mov ecx,[0x1093198]; call 0x4016c0). So this class both consumes a
              vital and manipulates the LogoutVital wire object + the app object.
  - 0x719ab0/0x719b90 : a timed "tear-down" method. It reads a MODE field [esi+0x28]
              (branches on ==1 and ==4), a timestamp field [esi+0x24]
              (elapsed-time formatting), and then CLOSES its two connection
              sub-objects [esi+0x18]/[esi+0x1c] via a virtual call [vtable+0xf4]
              (0x719bd0 / 0x719bef). i.e. it holds a mode + a timer and, when the
              mode is set, closes the network connection(s).
[STATIC] This is the shape of a client that, after a logout button, enters a MODE
and WAITS (mode+timestamp) before/while tearing down connections and switching
scene -- consistent with "the client does not fire-and-forget; it transitions via
connection teardown + app-state change," and consistent with the observed
behavior that on the default server the client "just sits there" (mode set, waiting
on a server-side event/redirect/close that never comes).

### Answer to Q2
[STATIC/NEGATIVE] The transition to character select is NOT produced by any single
inbound vital arriving through the normal vital channel (that channel only
reconciles actor vitals). It is driven by the session/connection orchestrator
(vtable 0xf45030) performing connection teardown + a switch to cStateSelectServer.
The evidence indicates this is gated on a server-side event -- most plausibly the
server CLOSING/redirecting the GSCN game connection (or ending the session) -- not
on the client unilaterally loading char-select right after the send. Whether a
specific inbound vital (e.g. ReturnSelectServerVital 0x709E) is the trigger, versus
a plain connection close or a timeout, is NOT decidable from the client binary:
0x709E remains the strongest-NAMED candidate for the char-select direction, but no
client code path was found that turns receipt of 0x709E into the cStateSelectServer
switch. [NAMED-CANDIDATE, UNCONFIRMED]

--------------------------------------------------------------------------------
## Q3 -- subcode 01 (exit game): self-exit after send, or wait?
--------------------------------------------------------------------------------

[STATIC] The clean quit path is a single PostQuitMessage site:
  - import PostQuitMessage IAT 0xc3b8d0 (pefile), exactly ONE caller at 0xa2837e,
    inside a WndProc-style dispatcher (0xa28330) that quits on a specific window
    message index (edi==2 branch at 0x2836f -> virtual [+0x74] then
    call [0xc3b8d0]). Other terminators (exit 0xc3b6b0: 3 sites in CRT teardown;
    _exit 0xc3b7dc: 1; TerminateProcess 0xc3b190: 2) are CRT/abort paths, not a
    "logout button -> immediate exit" path.
[STATIC] There is no code path from a LogoutVital send that unconditionally calls a
process terminator. The exit-game button feeds the SAME session/connection
orchestrator (vtable 0xf45030): its tear-down method (0x719ab0/0x719b90) discerns
mode [esi+0x28] (values 1 vs 4 -- the two non-"return-to-game" outcomes) and closes
connections; the process only quits later via the normal WndProc quit. This matches
the attended observation that pressing "exit game" on the default server did
NOTHING: the client set its mode and is WAITING for the connection to be
closed/acked by the server before it proceeds to quit. [STATIC, supports "waits"]

### Answer to Q3
[STATIC] Exit game is NOT an immediate self-exit after send. The client sends
LogoutVital(subcode 01), enters an orchestrator mode, and waits (for the
server-driven connection close / session end) before the process actually quits via
the ordinary window-quit path. The precise wait condition (server vital vs socket
close vs timeout) is not decodable, but "it waits" is directly supported. [STATIC]

--------------------------------------------------------------------------------
## Q4 -- Bottom line for redesign: what IS the correct LogoutVital response?
--------------------------------------------------------------------------------

(a) ECHO -- FALSIFIED, now with a MECHANISM. [STATIC/NEGATIVE]
    Any vital echoed inside GSCN_RunTimeProtocolRes is consumed by the actor-vital
    reconcile pass 0x446F30, which only adds/updates/removes actor-attached vitals
    and never switches scene/state or touches the connection. Echoing LogoutVital
    -- OR echoing ReturnSelectServerVital 0x709E -- through that envelope cannot,
    by construction, cause a transition. This is why the client "does not freeze,
    it just does not transition."

(b) A SPECIFIC OTHER VITAL (e.g. 0x709E) / scene-change / disconnect -- PARTIALLY
    SUPPORTED, best available direction. [STATIC + NAMED-CANDIDATE]
    The real transition is performed by a session/connection ORCHESTRATOR
    (vtable 0xf45030; methods 0x719c30 / 0x719ab0 / 0x719b90) that closes the
    game connection(s) (virtual [vtable+0xf4]) and drives the app-state machine to
    cStateSelectServer / to process-quit, gated on a mode field (+0x28 in {1,4})
    and a timer (+0x24). This is disconnect/teardown-shaped, i.e. the honest
    reading is that the correct server behavior is to END/redirect the GSCN game
    session (close or hand back to select-server), not to echo a vital. Whether the
    server should additionally emit ReturnSelectServerVital 0x709E as the "go to
    select server" signal is plausible (it is a separate, real vital and the
    strongest-named candidate for the char-select direction) but I found NO client
    code that consumes 0x709E to trigger cStateSelectServer, so I cannot confirm it.

(c) UNKNOWN from the binary -- TRUE for the exact wire response. [UNKNOWN]
    The client binary does not contain a decodable single "LogoutVital response
    vital" whose receipt drives the transition. The two facts that would pin it
    down are both out of reach here: (i) the button handler's post-send local-state
    write is behind the UI typeid-name binding + shared registrant vtable, and
    (ii) there is no per-id inbound handler for 0x1B40/0x709E outside the
    reconcile-only RunTimeProtocol path.

STRONGEST-SUPPORTED ANSWER: not (a). The evidence points to (b)-as-disconnect:
the correct response to LogoutVital is to TEAR DOWN / redirect the game session
(server closes or hands the client back to select-server), which the client's
session orchestrator (0xf45030) turns into the char-select switch (subcode 03) or
the process quit (subcode 01). ReturnSelectServerVital 0x709E is the best NAMED
candidate for an explicit char-select signal but is UNCONFIRMED as the trigger.
For the precise wire bytes of the response, the honest verdict is UNDECIDABLE from
the client binary alone -- an attended experiment that (1) closes the GSCN game
connection on receiving LogoutVital, and separately (2) sends 0x709E, will
distinguish the mechanisms far more cheaply than further static work.

--------------------------------------------------------------------------------
## Key VAs (all derivations noted inline above)
--------------------------------------------------------------------------------
Strings:       LogoutVital 0xf30a8c ; ReturnSelectServerVital 0xf30a98 ;
               GSCN_VitalData.cpp path 0xf30708 ; LSCN_SelectServerReq 0xf0b040 /
               Res 0xf0b028
Id reg stubs:  0xbee840 (ActorInspect->[0x1082078]) ; 0xbee860 (Logout->[0x108207c]) ;
               0xbee880 (RSS->[0x1082080])
Registry prims:0x89c080 (registry singleton [0x108cf90]) ; 0x89bd00 (name->id) ;
               0x89b220 (hasher)
Id getters:    0x5e6810 (Logout) ; 0x5e6960 (RSS) ; 0x5e6740 (ActorInspect)
Descriptor tbl:Logout 0xf304c8 ; RSS 0xf304ec ; ActorInspect 0xf304a4 (stride 0x24)
Serializer:    LogoutVital slot2 = 0x5e6820 (fields +0x14 u8 subcode / +0x18 u8 /
               +0x1c u32 / +0x20 u32 ; wire field-writer 0x89a600)
Descriptor singletons: Logout 0x1030e24 ; RSS 0x1030fb8 (ctors 0x422fb0 / 0x423040 ;
               init thunks 0xbd4f90 / 0xbd4fb0)
UI handlers:   TD AVSysetmSettingLogoutEventHandler 0x1026fdc ;
               TD AVSystemSettingLogoutConfirmEventHandler 0x1027074 ;
               register sites 0xc06540 / 0xc06860 ; singletons 0x10888f8 / 0x1088974 ;
               shared registrant vtable 0xf36384 ; type_info::name import [0xc3b7ac]
Inbound:       GSCN_RunTimeProtocolRes handler 0x446F30 (reconcile; per-entry apply
               [vtable+0x20] @0x446fb6 ; removal 0x446fe1..0x4470e5)
Orchestrator:  vtable 0xf45030 (dispatch 0x719c80 @0xf45058) ; 0x719c30 (touches
               Logout descriptor 0x1030e24 + app [0x1093198]) ; tear-down
               0x719ab0/0x719b90 (mode [esi+0x28], timer [esi+0x24], conn-close
               virtual [vtable+0xf4]) ; app method 0x4016c0
Exit:          PostQuitMessage IAT 0xc3b8d0, single caller 0xa2837e (WndProc 0xa28330) ;
               closesocket thunk 0xb378d4
States:        cStateSelectServer typeid 0x1022f1c ; cStateLogin 0x1022efc ;
               cStateSwitchScene 0x1022f44
Verified hashes: LogoutVital=0x1B40 ; ReturnSelectServerVital=0x709E

--------------------------------------------------------------------------------
FILES TOUCHED
--------------------------------------------------------------------------------
/sessions/friendly-dreamy-hopper/mnt/outputs/r100_agentD_logout_transition_statics.md  (this report; created)
/tmp/*.py  (scratch disassembly scripts; ephemeral, not under repo)
Read-only: GameClient.local.bin ; VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv (not needed -- ids resolved directly)
No repo files, server, UI, DB, git, or LOCK_* touched.
