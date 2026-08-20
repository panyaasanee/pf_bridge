# LANE D — the rescue / downed / revive machinery

Binary: `GameClient.local.bin` (v134 staging)
SHA-256 asserted at analysis time: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623` — **MATCH**
Image base `0x400000`. All VAs are virtual addresses in this image.
Static reverse engineering only. No server booted, no UI opened, nothing written outside `/tmp/re/`.

Peers read first, not redone: `/tmp/re/LANE_B_COMBAT_FAMILY.md`, `/tmp/re/LANE_C_CLIENT_COMPUTATION.md`.

---

## 0. VERDICT ON THE OWNER TESTIMONY (provenance `owner_testimony`)

| # | Her account | Verdict | Anchor |
|---|---|---|---|
| 1 | HP 0 -> character **falls down / lies on ground panting ("downed", not dead)** | **CONFIRMED IN BINARY** | Two distinct predicates exist. `IsDying()` = actor vtable **`+0x40`** (`0x454AC0` CMyActor / `0x43BDA0` CNetActor) = `HP==0 && dyingTimer > 0.0f`. While it holds, the idle task picks the wide literal **`L"_F_STRUGGLE_000"`** `0xF0F008` (pushed at `0x4726B1`). "Struggle", not "die". |
| 2 | A **countdown (~15 or 20 s)** appears **on the character** | **SPLIT: the 20 s timer is CONFIRMED, the on-screen countdown is NOT FOUND** | The duration is a named image constant `DURATION_DYING` = **20** at data `0x102249C` (registered `0x483475`, read at **`0x44A576`**). But **no widget anywhere reads the dying timer** — see section 4. Whole-image proof of the negative in 4.2. |
| 3 | A **round button with a cross/plus** appears **to the right of the character**, labelled *"cancel the help request"* | **CONFIRMED IN BINARY, as a one-control window** | Window **`L"Main_Dead"`** `0xF0D738` is opened by `0x44A597` while the local player is *dying*. Its handler `MainDeadEventHandler` (ctor `0x5183A0`, vtable `0xF1F550`) binds exactly **one** child: **`L"BUTTON_DIE"`** `0xF1F5CC` (`0x5183D2` -> stored at `handler+0x14`, `0x518404`). Clicking it sends `ActionVital` with action id **`0xEA7C`** (`mov dword [eax+0x30], 0xEA7C` @ `0x518493`) and closes the window (`0x5184AB`). |
| 3b | going down **auto-broadcasts** a help request | **NOT FOUND on the wire; CONFIRMED as a client-local broadcast** | On the rising edge of `IsDying()` the client itself emits a **system chat line** naming the actor: `0x4437C0` latches `[actor+0x70] |= 0x200` (`0x44385D`) then calls `0x5CB9A0(actor.id_lo, actor.id_hi)` (`0x4438E1`). Inside, string id **`0x192`** if the downed actor is me (`0x5CBA1A`), else **`0x19D`** / **`0x32D`** (`0x5CBA02`/`0x5CBA09`). **No Vital is sent when a player goes down** — see 6.3. |
| 4 | countdown reaches 0 -> the character **actually dies** | **CONFIRMED IN BINARY, but the client only *observes* it** | `IsDead()` = actor vtable **`+0x3C`** (`0x454A70` / `0x43BD70`) = `HP==0 && dyingTimer <= 0.0f` (`comiss xmm0(0.0), [attr+0x58]` @ `0x454A7D`, `jb` -> false). The client never writes the timer (4.2), so the transition is entirely server-driven; the client just re-evaluates the two predicates every frame. |
| 5 | -> a **revive-at-town screen** appears | **CONFIRMED IN BINARY** | `CMyActor::Update` `0x44E4E0` calls `IsDead()` at `0x44E594`; if true and the window is not already open, it opens **`L"Common_Death"`** `0xF0D860` (`0x44E5C7`). `Common_Death` -> `ReliveConfirmEventHandler` (name->ctor chain `0x5D8013`/`0x5D8067`, ctor `0x5D5840`, vtable `0xF2E6A8`). Its controls: **`BUTTON_RELIVE`** `0xF1A704`, **`BUTTON_SPAWN`** `0xF1A6E8`, **`BUTTON_RELIVE_TEXT`** `0xF1A6C0` (`0x4E43A0`). |

**Where the binary corrects her memory, plainly:**

* The window that carries the round button during the downed phase is **`Main_Dead`**, and it is *not* the death screen. The death screen is **`Common_Death`**. Two different windows, two different handlers. `Main_Dead` is **closed** the moment `IsDying()` goes false (`0x44A5A8`..`0x44A5C6`).
* **`ReliveVital 0x1AD4` is never sent from `Main_Dead`.** All three of its producers live in `Common_Death`'s handler (6.2).
* There is **no countdown number rendered from the dying timer** in this build. Nothing reads `BasicAttr+0x58` except four predicates and one window gate (4.2).
* Going down does **not** put a "help request" on the wire. What she remembers as a broadcast is reproduced locally by every client that can see the actor, from the same mirrored attributes.

---

## 1. The two predicates that define "downed" vs "dead" (PROVEN)

Actor vtables (`CMyActor` base `0xF0D7A8`; `CNetActor` base `0xF0D3A0`; the pair also appears in `0xF0DD08`, `0xF0E670`, `0xF0DF58`, `0xF0DFF8`, `0xF0E0C8`):

| slot | CMyActor | CNetActor | meaning |
|---|---|---|---|
| `+0x3C` | `0x454A70` (@`0xF0D7E4`) | `0x43BD70` (@`0xF0D3DC`) | **`IsDead()`** |
| `+0x40` | `0x454AC0` (@`0xF0D7E8`) | `0x43BDA0` (@`0xF0D3E0`) | **`IsDying()` / downed** |
| `+0x74` | `0x44C630` = `return this->[+0x348]` | — | `GetBasicAttr()` |

`0x454A70` (`IsDead`):

```
0x00454A73  mov  eax,[esi]          ; vtable
0x00454A75  mov  edx,[eax+0x74]     ; GetBasicAttr
0x00454A78  call edx
0x00454A7A  xorps xmm0,xmm0
0x00454A7D  comiss xmm0, dword [eax+0x58]   ; 0.0 vs dyingTimer
0x00454A81  jb   0x454AB1                   ; timer > 0  -> NOT dead (return false)
0x00454A8D  cmp  byte [esi+0x358], 0
0x00454A94  je   0x454AA5
0x00454A98  cmp  dword [eax+0x1A8], 0 ; sete   ; vehicle/ship HP
0x00454AA7  cmp  dword [eax+0x44],  0 ; sete   ; normal HP
```

`0x454AC0` (`IsDying`) is byte-identical except the timer test:

```
0x00454ACA  movss  xmm0, dword [eax+0x58]
0x00454ACF  comiss xmm0, dword [0xF0989C]   ; 0xF0989C = 0.0f
0x00454AD6  jbe    0x454B06                 ; timer <= 0 -> NOT dying
```

`CNetActor` twins: `0x43BD7A`/`0x43BD8C` and `0x43BDAA`/`0x43BDB9`, HP tested as `[attr+0x44]==0`.

So, exactly:

* **downed** iff `HP == 0` **and** `BasicAttr.f32[+0x58] > 0.0`
* **dead** iff `HP == 0` **and** `BasicAttr.f32[+0x58] <= 0.0`

`BasicAttr+0x58` is server-copied only, mask bit `0x800` in the attribute-apply loop (LANE C 2.4, `0x464436`..`0x4644E0`).

---

## 2. The dying duration — debt closed

| fact | value | anchor |
|---|---|---|
| config name | `L"DURATION_DYING"` | `0xF118FC` |
| registered into global | **`0x102249C`** | `push 0x102249C ; push 0xF118FC ; push esi ; call 0x482640` at `0x483475`..`0x483480` |
| registrar type | `0x482640` = **integer** config (`0x4826F0` is the float twin, e.g. `RESURRECT_TOWN` at `0x483E19`) | — |
| image default | **20** (`dword [0x102249C] == 20`) | data |
| the **only** reader in the whole image | **`0x44A572`** | `cvtsi2sd xmm1, dword [0x102249C]` |

Used exactly once, in the `Main_Dead` gate:

```
0x0044A567  mov   eax,[esi+0x348]                 ; BasicAttr
0x0044A56D  movss xmm0, dword [eax+0x58]          ; dying timer
0x0044A572  cvtsi2sd xmm1, dword [0x102249C]      ; (double)DURATION_DYING = 20
0x0044A57A  subsd  xmm1, qword [0xF092D0]         ; 0xF092D0 = 0.5  ->  19.5
0x0044A582  cvtps2pd xmm0, xmm0
0x0044A585  comisd xmm1, xmm0
0x0044A589  ja    0x44A5A6                        ; 19.5 > timer -> do NOT open
0x0044A597  push 0xF0D738 ; ... call 0xAA0710      ; OpenWindow(L"Main_Dead")
```

**Units:** seconds, and the value is a *remaining* time counting **down** from `DURATION_DYING` to `0`.
Proof chain: `IsDead` requires `timer <= 0` and `IsDying` requires `timer > 0` (section 1), so `0` is the death end of the range; `Main_Dead` opens only when `timer >= DURATION_DYING - 0.5`, i.e. only while the timer is still essentially full, which is the *start* of the downed phase; and `Main_Dead` is closed again as soon as `IsDying()` is false (`0x44A54C` -> `0x44A5A8`). A count-up reading would make `Main_Dead` a window that opens for the last 0.5 s and closes at death, which contradicts it being the only home of `BUTTON_DIE`. The `-0.5` is a freshness guard so the window is not opened for an actor first observed mid-phase.

> **Bounded unknown:** `20` is the *image default*. `0x482640` binds the name to the global so an external config file can override it at load; whatever the deployed server shipped in that file is not in this binary. What is certain is the units (seconds), the direction (down), and that the client reads it from exactly one place.

---

## 3. `L"Main_Dead"` — the downed-phase window (the round button)

* Name->handler binding (from the client's window-factory string chain):
  `0x5DA111 mov eax, 0xF0D738 (L"Main_Dead")` ... match -> `push 0x18 ; call operator new ; call 0x5183A0` (`0x5DA162`..`0x5DA182`).
  `0x5183A0` sets vtable **`0xF1F550`**; `vtable[0] = 0x5183C0` returns **`0x107CD8C`**, which is the registrar global written by the RTTI registration of **`.?AVMainDeadEventHandler@@`** (`0xBE2525 mov ecx, 0x1023E60` ... `0xBE2545 mov dword [0x107CD8C], 0xF36384`). Class identified.
* Object size **0x18** — one member.
* `OnCreate` = `0x5183D0`: looks up **exactly one** child, `L"BUTTON_DIE"` `0xF1F5CC`, casts it with the button cast `0xAB73C0`, stores at `handler+0x14`.
* `vtable+0x18` = `0x5184C0` binds the click callback **`0x518450`** to that button (`push 0x518450` @ `0x5184E1`, `call 0x57A090`).
* Click handler `0x518450`:

```
0x0051846E  call 0x44AF00              ; recycle-pool alloc, ctor 0x74E620
0x0051848E  mov  word [eax+0x4A], cx   ; current scene id ([0x1093198]+0x2C0 -> +0xC -> +0x30)
0x00518493  mov  dword [eax+0x30], 0xEA7C
0x005184A1  call 0x5DD800              ; send
0x005184AB  call [window vtable+0x20C] ; close Main_Dead
```

`0x74E620` sets vtable **`0xF489EC`**; `vtable+0x10 = 0x74E680` returns `word [0x108A2D8]`, the id global filled at `0xC0C120` from the ASCII name **`"ActionVital"`** `0xF48AF8`. So the button sends **`ActionVital`**, field `+0x30` (the `tag 0x14` u32 action id, emitted at `0x74E6EA`) = **`0xEA7C` (60028)**.

`ActionVital` full tagged field list (serializer `0x74E6A0`, walked):

| # | tag | size | member | emit VA |
|---|---|---|---|---|
| 1 | `0x32` | 8 | `+0x18` | `0x74E6BD` |
| 2 | `0x32` | 8 | `+0x20` | `0x74E6CC` |
| 3 | `0x32` | 8 | `+0x28` | `0x74E6DB` |
| 4 | `0x14` u32 | 4 | **`+0x30` = action id** | `0x74E6EA` |
| 5 | `0x19` | 4 | `+0x34` | `0x74E6F9` |
| 6 | `0x2A` f32 | 4 | `+0x38` | `0x74E708` |
| 7 | VEC3 (3x `0x2A`) | 12 | `+0x3C` | `0x74E712` |
| 8 | `0x0B` u8 | 1 | `+0x48` | `0x74E724` |
| 9 | `0x12` u16 | 2 | **`+0x4A` = scene id** | `0x74E733` |
| 10 | `0x0B` u8 | 1 | tail | `0x74E742` |

> **Bounded unknown:** the *label text* on `BUTTON_DIE` and its *texture*. `MainDeadEventHandler` never calls the string-table getters (`0x482400` / `0x482280` / `0x4824C0`), so the caption comes from the layout / string table on disk. The Thai string is **not present in the binary**. Method: whole-file regex for UTF-16LE Thai runs `(?:[\x01-\xff]\x0e){2,}` -> 39 hits, every one inspected and every one is incidental byte noise inside `.text`/`.rdata`/`.rsrc` (mostly unassigned code points such as `U+0E75 U+0E8B`); whole-file regex for UTF-8 Thai `(?:\xe0[\xb8\xb9][\x80-\xbf]){2,}` -> **0 hits**. **There is no Thai text of any kind in this image.** All UI captions are external. "Round, with a cross" is therefore unverifiable from bytes.

---

## 4. The countdown — stated as a flat negative

### 4.1 Who reads the dying timer

Whole-`.text` linear sweep (393,711 instructions decoded) for any operand `[reg+0x58]`, `reg` not `esp`/`ebp`, no index; then filtered to sites whose base register provably came from `GetBasicAttr()` (`[x+0x348]` or `call [vtable+0x74]` within the preceding 8 instructions). **Result: 5 sites, all reads, zero writes.**

| VA | instruction | function |
|---|---|---|
| `0x43BD8C` | `comiss xmm0, [eax+0x58]` | `CNetActor::IsDead` |
| `0x43BDB9` | `movss xmm0, [eax+0x58]` | `CNetActor::IsDying` |
| `0x44A56D` | `movss xmm0, [eax+0x58]` | `Main_Dead` gate |
| `0x454A7D` | `comiss xmm0, [eax+0x58]` | `CMyActor::IsDead` |
| `0x454ACA` | `movss xmm0, [eax+0x58]` | `CMyActor::IsDying` |

### 4.2 The negatives

* **The client never ticks the dying timer.** All 48 raw `[reg+0x58]` float sites in `.text` were inspected; the 43 that are not in the table above are `+0x54/+0x58/+0x5C` **position triples** (e.g. `0x4533AF`/`0x4533BE`/`0x4533C3`, `0x455D96`/`0x455DAA`, `0x4ABD6D`/`0x4ABD72`/`0x4ABD77`, `0x4AC924`/`0x4AC929`/`0x4AC92E`, `0x4447E9`/`0x4447F2`/`0x4447FA`), or the `f_HITRATE` table store (`0x4A3E88`, LANE C 3.1), or verbatim struct copies (`0x464BAD`/`0x464BB0`, `0x4656A7`/`0x4656AA`, `0x4B19B9`/`0x4B19BC`). **No decrement, no dt subtraction, no store of any kind to `BasicAttr+0x58`.**
* **The client does not escalate downed -> dead.** There is no path that zeroes the timer, none that clears HP, and no local "now dead" latch independent of the two predicates. `0x4437C0` and `0x44E4E0` only *observe* them each frame. The escalation is the server's, delivered as an ordinary attribute update (mask bit `0x800` for `+0x58`, bit `0x40` for `+0x44`).
* **No countdown widget is bound to the dying timer.** Every "countdown" widget literal in the image was located and its referencing function checked; none is in the death/rescue code:
  `PROGRESSBAR_COUNTDOWN` `0xF24DD8` (`0x553A2B`, `0x555DC2`), `NUMLABEL_COUNTDOWN` `0xF2B460` (`0x593FBC`), `TIME_COUNTDOWN` `0xF2B440` (`0x594016` ...), `TIMEINFO_COUNTDOWN` `0xF27044` (`0x563439`, `0x65D9A0` ...), `COUNTDOWNBAR` `0xF1EBCC` / `COUNTDOWNSEC` `0xF1EBB0` (`0x512C3B`/`0x512C74` and `0x6325E3`/`0x63261C`, a panel whose siblings are `ITEMLIST_CHECKLIST`, `BUTTON_READY`, `BUTTON_CANCEL` — a ready-check dialog).
  `PANEL_DEAD` `0xF35234` (`0x63321B`) is likewise **not** the death UI: its siblings are `NUMBERLABEL_PIRATE` `0xF35280` and `TIMEINFO_RECIPROCAL_MINS` `0xF3524C` — a PvP scoreboard.
* `Main_Dead` has one control and it is a button (section 3). No label, no bar.

**Conclusion for question 3: the dying timer is `BasicAttr+0x58`, in seconds, counting down, server-authored, and in this build the client uses it only as a boolean threshold. Any number she saw on screen is not produced by this binary from that field.**

---

## 5. The rescue mini-game (`Main_Panel_Rescue`) — client-random

* Name->handler: `0x5D9AE4 mov eax, 0xF0D52C (L"Main_Panel_Rescue")` ... match -> `push 0x38 ; new ; call 0x51D8F0` (`0x5D9B32`..`0x5D9B52`). Ctor sets vtable **`0xF1FC48`**.
* `OnCreate` `0x51D830` binds:
  `L"PANEL_REVIVE_ACTION"` `0xF1FD10` -> `+0x14`; `L"ReviveAction_Btns"` `0xF1FCEC` -> `+0x18` (item-list cast `0xAB76D0`); `L"Common_ProgressBar"` `0xF1FCC4` -> `+0x1C` (progress-bar cast `0xAB2520`).
  Other members: `+0x28`/`+0x2C` = target actor 64-bit id, `+0x30` = f32 start time, `+0x20` = u8.
* `Update` `0x51D980`:
  * `if (id64 == 0) -> CloseWindow` (`0x51D991`)
  * resolve actor (`0x402A20` make key -> `0x446170` resolve), class check against `0x102CE88`
  * `if (!(actor->byte[+0x10] & 0x80))` **and** `!actor->IsDying()` (`call [vtable+0x40]` @ `0x51D9EA`) -> `CloseWindow` (`0x51D9FB`)
  * `if (actor->byte[+0x10] & 0x80)` -> drive the progress bar: `elapsed = now - start`, clamped to `[0xF0D43C] = 5.0f` (`0x51DA3F`), `pct = elapsed / 5.0 * 100.0` (`0x51DA5B`/`0x51DA63`; constants `0xF0F398 = 5.0`, `0xF0AF90 = 100.0`), capped at 100, `SetPercent` `0x472430` (`0x51DA7D`); also cached to global `0x107CED4` (`0x51DA42`).
* Event handler `0x51DA90` reacts to `L"ReviveAction_Update_String"` `0xF1FDEC` and `L"ReviveAction_KeyDown"` `0xF1FD60`. For each entry of the incoming string vector it takes the first wide char, maps `'A'..'W'` through the jump table at `0x51DE30`/`0x51DE38`, and **only `A`, `D`, `S`, `W`** take the live case; it then formats **`L"%sbt_saveurlife_%c.tga"`** `0xF1FDBC` with `L".\Data\GUI\Main\"` `0xF1B5B4` (`0x51DB91`) onto `L"Revive_Char"` `0xF1FDA4` / `L"Char_img"` `0xF1FD90` at alpha `0.66f` (`0xF1FD8C`). The same logic is duplicated in the party-frame handler at `0x629CD1` / `0x629E28` / `0x629E30`.
* **Where the key sequence comes from — the client's own RNG:**

```
0x004722F3  cmp  dword [0x10223C8], esi      ; KEYS_REVIVE
0x00472307  call dword [0xC3B55C]            ; rand()
0x00472309  and  eax, 0x80000003
0x00472315  mov  ecx, dword [0x10220DC]      ; -> ASCII "ADSW" at 0xF0EFAC
0x0047231B  movzx edx, byte [ecx+eax]
0x00472322  call dword [0xC3B454]            ; push_back
```

  `KEYS_REVIVE` = config name `0xF11FB8` -> global **`0x10223C8`**, registered at `0x4830FA`, **image default 5**.
* The generator is called from `0x478BBD`, inside the update of **`CActorTask_FirstAidEvent`** — identified positively: vtable `0xF0EF94` (set at `0x4722BB`), `vtable[0] = 0x4722E0` returns class-descriptor global **`0x102EC84`**, which is the descriptor written by the RTTI registration of `.?AVCActorTask_FirstAidEvent@@` (`0xBD1675 mov ecx, 0x101D164` ... `0xBD1695 mov dword [0x102EC84], 0xF36384`).
  Same technique identified `CActorTask_Dead` -> `0x102ED98` (used at `0x4439AB`, ctor `0x472810`), `CActorTask_Knockdown` -> `0x102EDC8`, `CActorTask_Stalled` -> `0x102EC48`.
* The task posts client module message **`0x27`** to the actor's module list (`0x478C4A mov dword [esp+0x44], 0x27` ; `0x478C71 call 0x5F9C70`) carrying the generated string vector and the 64-bit actor id. `PartyModule_Client`'s handler `0x62C840` case `0x27` (`0x62CD4D`) opens `Main_Panel_Rescue` (`0x62CD89`) and forwards `ReviveAction_Update_String` (`0x62CDC4`). The key-down side is module message **`0x26`** (`0x452F82` / `0x452F8E`), forwarded at `0x62CCCA`..`0x62CD05`.

**Consequence: the WASD "save your life" prompt is generated locally by the client, not sent by the server.**

---

## 6. `ReliveVital 0x1AD4` and the actual revive screen

### 6.1 The class

* Name hash: ASCII `"ReliveVital"` `0xF3096C` -> `0x89C080`/`0x89BD00` -> `word [0x1082038]` (`0xBEE640`..`0xBEE651`). `ReliveMarkerVital` `0xF30978` -> `word [0x108203C]` (`0xBEE660`).
* Registrar ctor `0x422620`, object size **`0x1C`** (`mov dword [edi+0x0C], 0x1C` @ `0x422689`). `ReliveMarkerVital` registrar `0x4226B0`, size **`0x18`** (`0x422719`).
* Class ctor `0x5E5F30`, **vtable `0xF30404`**:

| slot | value | role |
|---|---|---|
| `+0x00` | `0x5E5F60` (returns `0x1081E40`) | class descriptor |
| `+0x10` | `0x5E5F70` (`mov ax, word [0x1082038]`) | **GetVitalId -> `0x1AD4`** |
| `+0x14` | `0x5EB110` | pool clone |
| `+0x18` | `0x5E5F80` | **serializer** |
| `+0x1C` | **`0x710440`** | inbound slot — **shared no-op** |
| `+0x20` | **`0x710440`** | inbound slot — **shared no-op** |

**Confirms the earlier milestone: `ReliveVital` is request-only; the client decodes it and does nothing.**

`ReliveMarkerVital` for contrast: vtable base `0xF305D8`, `+0x10 = 0x5E7440` (`word [0x108203C]`), `+0x18 = 0x5EB6D0` (serializer), `+0x1C = 0x5F0410` (a real handler), `+0x20 = 0x710440`.

### 6.2 `ReliveVital` field list and its three producers

Serializer `0x5E5F80` (write branch `0x5E5F91`..`0x5E5FB0`, read branch `0x5E5FBA`..`0x5E5FDF`):

| # | tag | size | member | write VA | read-back VA |
|---|---|---|---|---|---|
| 1 | `0x08` (i8) | 1 | `+0x14` — **mode** | `0x5E5FA1` | `0x5E5FD2` (`movsx`) |
| 2 | `0x05` | 1 | `+0x18` | `0x5E5FB0` | `0x5E5FDF` |

Ctor zeroes both (`0x5E5F4C`, `0x5E5F4F`). `+0x18` is never written by any producer.

Pool allocator for the class: `0x4E45B0` (`new 0x1C` @ `0x4E45FC`, ctor `0x4E4614`). Its call sites are the **three producers**, all inside `ReliveConfirmEventHandler`, i.e. the `Common_Death` window:

| producer | VA | mode byte written | condition |
|---|---|---|---|
| **P1** — `BUTTON_RELIVE` click, `0x4E46C0` | `0x4E4731` | `mov dword [eax+0x14], 1` @ `0x4E4737` | gated on `0x44A200(0x10, 0)` returning true (`0x4E471C`/`0x4E4721`) — a client-module query (module message code `0x13`, `0x44A265`/`0x44A286`). If false, the handler instead opens `L"Common_Purchase"` `0xF19F24` offering buff/item `0x12D` (`0x4E4881`), or shows a `Common_MessageBox` with string id `0x27B` (`0x4E47B6`). |
| **P2** — `BUTTON_SPAWN` click, `0x4E4B20` | `0x4E4B84` | `mov dword [eax+0x14], 0` @ `0x4E4B8A` | taken when `0x432510(0)` is true; otherwise it builds a confirm dialog first (below). |
| **P3** — the confirm-dialog callback `0x4E4A90` | `0x4E4AE4` | `mov dword [eax+0x14], 0` @ `0x4E4AEA` | fires when the user accepts the death-penalty confirm (`cmp dword [eax+0x94], 1` @ `0x4E4AC3`). Registered at `0x4E4D25` (`push 0x4E4A90`). |

All three then `call 0x4011A0 ; call 0x5DD800` (the send path), e.g. `0x4E473E`/`0x4E4745`.

So **`ReliveVital.mode = 1` = revive on the spot (needs item/buff `0x12D`); `mode = 0` = respawn at town.** The town path first shows the destination scene name (`L"SCENE_NAME_TIP"` `0xF0C59C` -> `L"s_SCENE_NAME"` `0xF0C3C4`, `0x4E4BE2`/`0x4E4BFF`) and the loss value `L"n_DEADLOSS"` `0xF14BC8` from `L"STANDARD_STATUS"` `0xF152AC` (`0x4E4C69` and `0x4E4CB7`), formatted into dialog id `0x11` (`0x4E4CF6`, `call 0x5AB5F0`).

`BUTTON_RELIVE_TEXT` caption is a string id chosen by the same scene predicate: **`0x5F4`** if `0x432510(0)`, else **`0x270`** (`0x4E4471` / `0x4E4478`, `call 0x482400`).
`0x432510(0)` reads `n_SCENE_TYPE` `0xF0C48C` from the `SCENE_NAME` table `0xF0C4A8` for the current scene and returns `(type & 0x24) || (type & 0x300)` (`0x43255C`..`0x43256A`) — a scene-class test, not a death concept.

### 6.3 Negative: nothing is sent when you go down

Method: enumerated every Vital-id global via the `0x89C080`/`0x89BD00` name-hash registration idiom, then walked every send site (`0x5DD800`) reachable from the death/dying code (`0x4437C0`, `0x44A540`, `0x44E4E0`, `0x454A70`, `0x454AC0`, `0x472630`, `0x472850`, `0x478B40`, `0x51D980`).
The only Vitals sent anywhere in that reachable set are:

* `ActionVital` (id global `word [0x108A2D8]`) from `BUTTON_DIE` (`0x5184A1`);
* `ReliveVital 0x1AD4` from the three `Common_Death` buttons (6.2);
* `PartyCmdVital 0x2466` from the party menu (opcodes `0x0B` leave `0x62CA5D`, `0x0C` kick `0x62CB2A`, `0x0D` changeleader `0x62CBA4`).

**No message is emitted at the moment `IsDying()` becomes true.** The "help request" is a purely local consequence of attribute state that every nearby client already receives.

---

## 7. What the server actually controls (answer to question 2)

**Client-derived, not a server flag.** Precisely:

* The **only** inputs from the server are two ordinary `BasicAttr` fields: `+0x44` (HP; alternate `+0x1A8` when `actor.u8[+0x358] != 0`) and `+0x58` (dying timer, mask bit `0x800`). Both are `mov`-copied verbatim (LANE C 2.4).
* Everything downstream is computed locally:
  * `IsDying()` / `IsDead()` — section 1.
  * The **round-button window** `Main_Dead` — opened by `0x44A540` from `IsDying()` plus a threshold on the timer. **No server message opens it**: xrefs of `L"Main_Dead"` give exactly four `.text` sites — `0x44A555` (probe), `0x44A597` (open), `0x44A5A8` (probe for close), `0x5DA111` (the name->handler factory). None is in a Vital handler.
  * The **prone/panting animation** `_F_STRUGGLE_000` — chosen at `0x4726A7`/`0x4726B1` purely from `IsDying()` and `actor+0x10 & 0x80`.
  * The **help-request chat line** — `0x4438E1`, local.
  * The **WASD rescue prompt** — client `rand()`, section 5.
  * The **death screen** `Common_Death` — opened by `0x44E5C7` from `IsDead()`.
* The one flag-looking input, `actor+0x10` bit `0x80` ("being rescued"), is itself **derived**, not received. `0x4437C0` mirrors it from the actor's motion state every frame:

```
0x004437E8  mov  eax,[esi+0x244]        ; motion object
0x004437EE  mov  ecx,[eax+0x3C]
0x004437F1  and  cl, 0x80
0x004437F4  cmp  cl, 0x80 ; sete al
0x00443801  or   eax, 0x80   /  0x00443808  and eax, 0xFFFFFF7F
0x0044380D  mov  [esi+0x10], eax
```

  Whole-image scan for any other write to that bit: **none**. It is only tested, at `0x44A54E`, `0x44FA44`, `0x47269C`, `0x51D9DD`, `0x51D9FD`.

**One line: the server sends HP and a float timer; the client alone decides that this means "downed", plays the struggle animation, opens the one-button window, prints the help-request line, and later decides it means "dead" and opens the revive screen.**

---

## 8. Other proven artefacts of the downed/dead path

* **`0x4437C0` — per-frame death/dying state sync** (`this` = actor):
  * mirrors the motion bit into `actor+0x10` bit `0x80` (`0x44380D`);
  * `bl = IsDying()` (`0x443836`), `[esp+0x13] = IsDead()` (`0x443841`);
  * on the `IsDying()` rising edge: latch `[actor+0x70] |= 0x200` (`0x44385D`), `0x43E930(this,1)` (`0x443864`), stop sound channels 4 and 5 (`0x443877`, `0x443886`), spawn attached effect id **`0x232B`** (`push 0x232B` @ `0x44389B`, `call 0x4162A0` -> `0x48D270` -> `0x4843C0`), emit the chat notice `0x5CB9A0(id_lo,id_hi)` (`0x4438E1`);
  * on the falling edge, or when the rescue bit is set: flips latch `0x400` / clears `0x200` (`0x4438FF`, `0x443942`) and restores the sounds (`0x44397C`, `0x44398B`);
  * on `IsDead()`: allocates and pushes **`CActorTask_Dead`** (descriptor `0x102ED98` @ `0x4439AB`, ctor `0x472810` @ `0x4439E9`, push `0x4843C0` @ `0x4439FC`) and, if the dead actor is my current target, fires UI event **`L"TargetIsDead"`** `0xF0D470` to `Main_Panel_Target_Enemy_New` (`0x443A57`..`0x443A78`).
* **`CActorTask_Dead::Update` `0x472850`** — plays the wide literal at `0xF0F060` (`push 0xF0F060` @ `0x4728AF`, guarded by `[actor+0x70] & 0x40` and a once-latch `[task+0x20]`), then advances the animation (`0x484610`, `0x485B90`).
* **Idle-task animation selector `0x472630`** — the `_F_STRUGGLE_000` (`0xF0F008`, `0x4726B1`) / `_F_RESCURED_000` (`0xF0F028`, `0x4726A7`) choice, gated on `IsDying()` at `0x472691` and the rescue bit at `0x47269C`.
* **Party-frame rescue indicator** (`Party_Main` `0xF348C4`, handler vtable `0xF34894`, member update `0x62C2A0`): for each party member it resolves the actor, **skips the local player** (`cmp [0x1032EC4], eax ; je` @ `0x62C382`), calls `IsDying()` (`0x62C449`) and posts `L"ReviveNotify_Show"` `0xF345E0` with arg byte `1` when dying (`mov byte [esp+0xC0], 1` @ `0x62C491`) or `0` plus `L"ReviveAction_Show"` `0xF345BC` when not (`0x62C4FB`, `0x62C53D`). The receiving handler `0x629A5F` toggles `PANEL_REVIVE_NOTIFY` `0xF343AC` visibility (`0x629A87`) and shows `BUTTON_REVIVE` `0xF34390` (`0x629A74`). Again purely from the client-side predicate. That handler's `OnCreate` is `0x6283E0`: `ICON_DEAD` `0xF343F0` -> `+0x48`, `ICON_OFFLINE` `0xF343D4` -> `+0x4C`, `PANEL_REVIVE_NOTIFY` -> `+0x50`, `BUTTON_REVIVE` -> `+0x54`, `Common_ProgressBar` -> `+0x58`, `PANEL_REVIVE_ACTION` -> `+0x5C`, `ReviveAction_Btns` -> `+0x64`, `ICON_SELECT` `0xF34378` -> `+0x68`, `IMAGEBAR_HP_NEW`/`IMAGEBAR_MP_NEW`/`LABEL_HP_NEW`/`LABEL_MP_NEW` -> `+0xAC`..`+0xB8`.
* **Cursor**: `L"CURSOR_RESCUE"` `0xF0CA7C` is loaded as `%s%s.ani` at `0x437C5E` — a dedicated mouse cursor for rescuing, i.e. downed players are click-targetable.
* **ESC closes the rescue panel**: `0x448180` tests `[msg+4]==0x100 && [msg+8]==0x1B` (`0x44819A`/`0x4481A3`) and closes `Main_Panel_Rescue` (`0x4481C6`).
* **`SetDying`** — ASCII `0xF0E4A4`, bound as a script/exported function at `0x462150` to implementation **`0x45FA00`**, which is `xor eax,eax ; ret 4`. **A stub. It does nothing in this client.**
* Related literals located but not on the death path: `.\Data\FXS\S_DYING1.fxs` `0xF0D2E8`, `.\Data\FXS\SOUND_DYING` `0xF42C68`, `.\Data\FXS\U_RESURRECT` `0xF42BB8`, `.\Data\FXS\U_REVIVED` `0xF42AB0`, `M079_000_000_RESCUE.avt` `0xF0DDC8`, `Equipment_Ship_Dying` `0xF2CB68` (ship UI), `SCORE_SEA_RELIVE` `0xF1278C` (a naval scoring config, global `0x10222D4`, default 2).

---

## 9. Bounded unknowns (explicit)

1. **The deployed value of `DURATION_DYING`.** Image default 20, registered as an overridable int at `0x483475`. The external config file is not in this binary.
2. **The caption and texture of `BUTTON_DIE`.** Both live in the layout / string table on disk; no Thai text of any kind exists in the image (see section 3). "Round, with a cross/plus" is unverifiable from bytes.
3. **The meaning of `ActionVital` action id `0xEA7C` (60028).** The client only sends the number; nothing in the image names it. "Stop asking for help / die now" is an inference from `BUTTON_DIE`'s name and its window's dying-only lifetime, not proof.
4. **What `0x44A200(0x10, 0)` actually asks** (the gate on `BUTTON_RELIVE`). It posts client-module message `0x13` with a 64-bit argument (`0x44A265`..`0x44A286`); the answering module was not traced. The fallback offers item/buff `0x12D`, so "do I hold the revive item?" is the natural reading — unproven.
5. **Effect id `0x232B`** spawned on going down (`0x44389B`) — the effect table is external.
6. **`0x43E930(actor, bool)`**, called on both edges of the downed latch (`0x443864`, `0x443906`, `0x44392B`, `0x443969`) — body not analysed.
7. **What creates `CActorTask_FirstAidEvent`.** Its factory is `0x47C9A0`, reached only through a function-pointer table entry at `0xF0F7D0`; the table base could not be tied to a concrete `mov [reg], imm` site, so the caller chain — and therefore whether a wire message triggers first aid on *another* player — is not proven. The task's *content* (client `rand()` over "ADSW") is proven.
8. **`ReliveVital` field `+0x18`** (tag `0x05`, 1 byte): serialized in both directions, written by no producer, left `0` by the ctor. Purpose unknown.
9. **The `PartyModule_Client` message-code enum** (`0x25`, `0x26`, `0x27`, `0x39`, `0x49`). Only `0x26` and `0x27` were traced to producers (`0x452F82`, `0x478C4A`); the rest were not.
10. **Direction of `BasicAttr+0x58` is an inference**, not a byte-level fact: nothing in the client writes it, so "counts down" rests on the threshold logic argued in section 2. The thresholds themselves are proven.
11. **Tension with the attended test.** If the timer really is set to `DURATION_DYING` at down-time, `0x44A597` should have opened `Main_Dead` immediately; that is consistent with her seeing a button within 6 s, but the same reasoning predicts `Common_Death` at ~20 s, which was outside the observed window. Nothing here settles what the current server actually sends in `+0x58`; that needs a wire/DB observation, not the binary.

---

## 10. Files touched

Read-only:

* `/sessions/hopeful-stoic-euler/mnt/Pirate Force/Pirate Force ServerProject/packages/.v134_staging_20260815_0355/GameClient.local.bin`
* `/sessions/hopeful-stoic-euler/mnt/Pirate Force/pf_bridge/VITAL_REGISTRY_FROM_CLIENT_BINARY_20260817.tsv`
* `/tmp/re/LANE_B_COMBAT_FAMILY.md`, `/tmp/re/LANE_C_CLIENT_COMPUTATION.md`, `/tmp/re/pe.py`, `/tmp/re/walk.py`, `/tmp/re/fn.py`

Created (all inside `/tmp/re/`, none in the repo, none in any mounted folder):

* `/tmp/re/sx.py` — string extractor (ASCII + UTF-16LE incl. the Thai plane)
* `/tmp/re/sx.pkl` — cached string index (97,981 ASCII / 7,683 wide)
* `/tmp/re/rt.py` — RTTI / vtable helpers
* `/tmp/re/ann.py` — annotating disassembler (`ann`, `afn`, `fstart`, `fend`)
* `/tmp/re/LANE_D_RESCUE_DOWNED_REVIVE.md` — this document

Nothing under `src/`, `current/`, `tests/`, `tools/` was read or written. `pf_bridge/LOCK.txt`, `pf_bridge/GAME_TEST_QUEUE.md`, `pf_bridge/CHIEF_CONTINUATION.md` were not touched. No git operation, no server, no UI. **No rule violations to report.**
