# LANE C — Does the CLIENT compute damage itself?

Binary: `GameClient.local.bin` (v134 staging)
SHA-256 asserted at analysis time: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623` — **MATCH**
Image base `0x400000`. All VAs are virtual addresses in this image.

Builds on `/tmp/re/LANE_B_COMBAT_FAMILY.md` (peer). Contains **two corrections** to that document (§0).

---

## VERDICT

**NO — the client does not compute damage.**

The damage number drawn on screen is the wire field `element+0x08` (signed i32), passed through
three plain `push`/`mov` hops and rendered as `abs(value)` in decimal. The only arithmetic applied
anywhere on that path is `abs()` (`cdq ; xor eax,edx ; sub eax,edx` at `0xA7EBFF`..`0xA7EC02`).
There is **no** multiply, divide, clamp, scale, round, or table lookup on the value.
The client also **never** writes HP from a hit: across all 393,711 `.text` instructions there is
**not one** arithmetic or read-modify-write store to `attr+0x44`, `attr+0x48`, `attr+0x1A8` or
`attr+0x1AC` (§2).

The client *does* compute **display-only derived stats** (ATK/DEF/hit/dodge/block…) for the
character panel, from a data table plus equipment bonuses (§3). Those accessors are called from
UI code only — never from any combat handler (proven caller list, §3.2).

---

## 0. Corrections to LANE B, up front

### 0.1 `element+0x18` (f32) is **not** the damage magnitude — it is a **yaw angle in radians**

LANE B §5.2 states "element `+0x18` (f32) is the magnitude fed to the floating damage-number /
effect spawner". That is wrong. Proven:

* `fld dword [ebx+0x18]` at `0x751342` (CMissileHitResult) and `0x750A42` (CHitResult) is pushed as
  the **2nd argument** to `0x48DBA0` / `0x48D870` respectively.
* Inside both, that float reaches `0x49C8B0` (`0x48D941`, `0x48DC45`).
  `0x49C8B0(Vec3* out, float a)` is `out[0] = sin(a)` (`call 0x49C7A0` @`0x49C8B9`),
  `out[1] = -cos(a)` (`call 0x49C6F0` @`0x49C8CB`, `fchs` @`0x49C8D3`), `out[2] = 0.0f`
  (`xorps xmm0,xmm0` @`0x49C8D0`, `movss [esi+8],xmm0` @`0x49C8DB`).
  **A float that is fed to sin/cos is an angle.**
* Second, independent confirmation: `0x48DA22`..`0x48DA3F`
  `fld [esp+0x74] ; fadd qword [0xF0D140] ; ... call 0x427630 ; fsubr` where
  `0xF0D140 = 3.14159274` (**pi**, read as double) and `0x427630` returns `[actor->motion + 0x30]`
  = the actor's facing yaw (the same slot `ActionVital` writes at `0x7518C6`).
  `angle + pi - facing` is a heading computation, not a damage computation.

So `element+0x18` is the **knock/hit direction yaw**, consumed by the knockdown/falling reaction
animation spawner. It never reaches any text/number widget.

### 0.2 The result-flag bits DO have proven names now

LANE B bounded unknown #4 said the labels hit/miss/block/critical are not provable. They are —
via texture filenames. See §1.4.

---

## 1. The damage-number-on-screen path (PROVEN, end to end)

### 1.1 There is a floating bitmap-number system: class `FxNumber`

* MSVC type descriptors: `.?AVFxNumber@@` @ `0x0101EAA4`, `.?AVFxNumberCache@@` @ `0x0101EABC`.
* Engine (PcRTTI) name literals (UTF-16): `"FxNumber"` @ `0xF85874`, `"FxNumberCache"` @ `0xF85858`.
* Registration: `0x41DA40` pushes `0x101EA9C` (`0x41DA6B`) and sets object size
  **`0x11C`** (`mov dword [edi+0x0C], 0x11C` @ `0x41DA99`). `FxNumberCache` size `0x2C` (`0x41DB29`).
* `FxNumber` **vtable = `0xF85888`** (`mov dword [esi], 0xF85888` @ `0xA7C05E`, inside the ctor).
* Ctor / init: **`0xA7C010`**, signature `__thiscall (int type, Vec3 pos, int value)`:
  * `mov eax,[esp+0x48] ; mov [esi+0xF8], eax` (`0xA7C042`/`0xA7C046`) -> **`+0xF8` = the numeric value, stored verbatim.**
  * `movq [esi+0x100], xmm0` / `mov [esi+0x108], eax` (`0xA7C0CB`/`0xA7C0D3`) -> `+0x100..+0x10B` = world position.
  * `mov [esi+0x10C], ecx` (`0xA7C0C5`) -> **`+0x10C` = the presentation `type`.**

### 1.2 Who creates it: `0x43FBB0` = `CNetActor::SpawnFxNumber(int type, int value)`

`ret 8` (`0x43FBCD`). `arg0 = type` (`esi` @`0x43FBE3`), `arg1 = value`.
Three `operator new(0x11C)` sites select a construction variant purely by `type`:

| type set | new site | value passed to `0xA7C010` |
|---|---|---|
| 6, 7, 8, 9 | `0x43FC3D` | **literal `0`** (`push 0` @ `0x43FC64`) — icon only, no digits |
| 0, 1, 2, 3 | `0x43FCB6` | `arg1` (`mov ecx,[esp+0x2C] ; push ecx` @ `0x43FCD3`/`0x43FCD7`) |
| 4, 5 | `0x43FCDA` | `arg1` (`mov edx,[esp+0x2C] ; push edx` @ `0x43FCF7`/`0x43FCFB`) |

Then it is attached to the world FX list: `[0x1093198]+0x2C0`, `+0x14`, `call 0xA7B6C0` (`0x43FDB7`).
**No arithmetic is performed on `arg1` anywhere in `0x43FBB0`.**

### 1.3 Who calls `0x43FBB0` with the wire damage: `0x43FDE0`

`0x43FDE0` is `__thiscall`, `ret 0x18` (`0x440161`) = **6 stack args**, `this` = the **target actor**.
Argument mapping proven from the CHitResult call site `0x750D90`..`0x750DAA`:

```
mov ecx,[esi+8]          ; element +0x08  (signed i32)   -> arg5   0x750D90
movzx edx,word [esi+0x1C]; element +0x1C  (result flags) -> arg4   0x750D93
mov eax,[esi+4]          ; element +0x04  target hi      -> arg3   0x750D97
mov ecx,[esi]            ; element +0x00  target lo      -> arg2   0x750D9B
mov edx,[ebp+0x1C]       ; CHitResult +0x1C attacker hi  -> arg1   0x750D9E
mov eax,[ebp+0x18]       ; CHitResult +0x18 attacker lo  -> arg0   0x750DA5
mov ecx,edi              ; this = target actor
call 0x43FDE0                                                      0x750DAA
```

Inside, args sit at `[esp+0x74]`(arg0) … `[esp+0x88]`(arg5).
**`mov esi, dword ptr [esp+0x88]` at `0x43FF11` loads the damage into `esi`, and `esi` is thereafter
only ever `push`ed.** Verified mechanically: the whole range `0x43FDE0`..`0x440164` contains
**zero** `imul/idiv/mul/div/fmul/fdiv/mulss/divss/neg` instructions (§4.1 census).

Two global gates before anything is shown:
* `cmp byte [localPlayer + 0x420], 0 ; je end` (`0x43FE25`/`0x43FE2C`) — a user setting.
* party/guild-visibility predicates `0x7504A0`, `0x750590`, `0x7505D0` (`0x43FE96`..`0x43FEE6`).

`bl` = "the local player is the **attacker**": `cmp [localPlayer+0x78], esi(arg0)` (`0x43FF01`) and
`cmp [localPlayer+0x7C], [esp+0x78](arg1)` (`0x43FF05`), `mov bl,1` (`0x43FF0B`) / `xor bl,bl` (`0x43FF0F`).

### 1.4 flags (`element+0x1C`) -> FxNumber `type` -> texture. **This names the bits.**

| flags bit | test VA | `0x43FBB0` type | resulting glyphs | meaning |
|---|---|---|---|---|
| `0x0002` | `0x43FF1B` | **7** (`0x43FF26`) | `bm_block.tga` | **BLOCK** (also plays `.\Data\FXS\S_H_BLOCK.fxs`, str `0xF0D334`, `0x43FF2F`) |
| `0x0001` + `0x0200` + attacker==me | `0x43FF9F`,`0x43FFAD`,`0x43FFBD` | **4** (`0x43FFC1`) | orange digits | damage I dealt, "special" (plays `C_SKILL02`, str `0xF0D328`) |
| `0x0001` + `0x0200` + not me | as above | **5** (`0x43FFFC`) | orange digits | same, other actors |
| `0x0001`, no `0x0200`, attacker==me | `0x440037`,`0x44003B` | **0** | red digits | ordinary damage I dealt |
| `0x0001`, no `0x0200`, not me | `0x44003F` | **1** | red digits | ordinary damage |
| `0x0100` | `0x440046` | **8** (`0x440054`) | `bm_gored.tga` | gore/bleed marker |
| `0x0400` | `0x44005D` | **9** (`0x44006B`) | `bm_overkill.tga` | **OVERKILL** |
| `0x0001` clear **and** damage==0 | `0x44008E`,`0x440090` | **6** (`0x440093`) | `bm_miss.tga` | **MISS** |
| `0x0020` | `0x4400A1` | **2** (`0x4400DA`) | green digits + `bm_gp` | HP-change readout |
| `0x0040` | `0x4400F2` | **3** (`0x440122`) | blue digits + `bm_bp` | MP-change readout |

This supersedes LANE B bounded unknown #4 for bits 0, 1, 5, 6, 8, 9, 10.
(Bits 3 and 4, used at `0x75131C`/`0x751324` for the animation branch, remain unnamed.)

Bits 5 / 6 additionally drive a client-side **change detector** on the local player, using cached
copies of the attribute values (this is bookkeeping, not damage math):
`mov edx,[player+0x348] ; mov ecx,[edx+0x44] ; mov [player+0x42C],ecx` (`0x44007D`..`0x440086`),
`mov edi,[attr+0x1AC] ; mov ebx,[attr+0x1A8] ; cmp [player+0x42C],edi` (`0x4400B1`..`0x4400D1`),
`mov [player+0x42C],ebx` (`0x4400EC`); MP twin at `0x440110`..`0x44013D` using `attr+0x50`/`+0x4C`
and cache slot `player+0x430`.

### 1.5 Value -> glyphs: the only arithmetic in the entire chain is `abs()`

`FxNumber::SetValue` = **`0xA7EE30`** (`ret 4`), reached from `0xA7F2B1`
(`mov eax,[esi+0xF8] ; push eax ; call 0xA7EE30`). It calls two helpers with the same raw value:

* **`0xA7E940`** — sign glyph + width. `0x896100(buf, value)` (`0xA7E982`) with the **raw signed**
  value; `strlen` (`0xA7E996`) `* 32 / 2` (`0xA7E99C`/`0xA7E9A1`) = half pixel width.
  `test esi,esi ; jle` (`0xA7E9B0`/`0xA7E9B2`): only for **value > 0** is a sign glyph appended —
  glyph `0x28` for type 2 (`push 0x28` @ `0xA7E9CB`), glyph `0x2A` for type 3 (`push 0x2A` @ `0xA7EA65`).
* **`0xA7EBA0`** — the digits:

```
0x00A7EBFB  mov  eax, dword ptr [esp+0x68]   ; the value
0x00A7EBFF  cdq
0x00A7EC00  xor  eax, edx
0x00A7EC02  sub  eax, edx                    ; <-- abs(value).  THE ONLY ARITHMETIC.
0x00A7EC04  push eax
0x00A7EC0A  call 0x896100                    ; -> sprintf(buf, "%d", abs(value))
```
`0x896100` is a thin `sprintf` wrapper: it pushes format string **`0xF14A94 = "%d"`** (ASCII,
at `0x896133`) and calls `0x896040` (`0x896139`).

Then one loop iteration per character (`0xA7EC45`..`0xA7EDF6`): the char is converted to a digit
(`call [0xC3B524]` @ `0xA7EC5B`), rejected if `> 9` (`cmp esi,9 ; ja` @ `0xA7EC66`), and a colour
offset is added based on `[edi+0x10C]` (the type):

| type | offset added | VA | palette |
|---|---|---|---|
| 3 | `+0x14` | `0xA7EC7A` | **blue** |
| 2 | `+0x0A` | `0xA7EC84` | **green** |
| 4 or 5 | `+0x1E` | `0xA7EC93` | **orange** |
| 0 or 1 | `+0` | fallthrough `0xA7EC96` | **red** |

Layout only: `fild <char index> ; fmul qword [0xF85BD0] (= 22.0) ; fisub <half width>`
(`0xA7ED53`, `0xA7ED61`, `0xA7ED74`) -> `[esi+0x54]` = the glyph's X pixel offset.

**Statement of the negative, flatly: the number the server sends is displayed verbatim.
`abs()` is applied so the minus sign is not rendered as a digit; the magnitude is untouched.
No rounding, no scaling, no multiplication, no clamping, no sign flip of the magnitude.**

### 1.6 The glyph-code -> texture table (complete)

Built once by the `FxNumberCache` loader (function spanning approx. `0xA7C880`..`0xA7E6C0`,
entered from `0xA7F63D`). The glyph code is stashed at `[esp+0x23]` / `[esp+0x1B]` immediately
before each cache insert:

| glyph code | texture (ASCII literal VA) |
|---|---|
| `0x00`-`0x09` | `.\Data\CP\bmmsg\bm_r%d.tga` `0xF85A30` (loop end `cmp bl,9` @ `0xA7D713`) |
| `0x0A`-`0x13` | `bm_g%d.tga` `0xF859F8` (`mov bl,0x0A` @ `0xA7D92D`, `cmp bl,0x13` @ `0xA7DAF8`) |
| `0x14`-`0x1D` | `bm_b%d.tga` `0xF85A14` (`mov bl,0x14` @ `0xA7D730`, `cmp bl,0x1D` @ `0xA7D920`) |
| `0x1E`-`0x27` | `bm_o%d.tga` `0xF859DC` (`mov bl,0x1E` @ `0xA7DB0B`, `cmp bl,0x27` @ `0xA7DCC9`) |
| `0x28` | `bm_gp.tga` `0xF859C0` (`0xA7E01E`) — green **+** |
| `0x29` | `bm_gm.tga` `0xF859A4` (`0xA7E17F`) — green **-** |
| `0x2A` | `bm_bp.tga` `0xF85988` (`0xA7E2F8`) — blue **+** |
| `0x2B` | `bm_bm.tga` `0xF8596C` (`0xA7E434`) — blue **-** |
| `0x2C` | `bm_block.tga` `0xF85AD0` (`0xA7CFA1`) |
| `0x2D` | `bm_miss.tga` `0xF85AA8` (`0xA7D10F`) |
| `0x2E` | `bm_boom.tga` `0xF85A8C` (`0xA7D233`) |
| `0x2F` | `bm_gored.tga` `0xF85A4C` (`0xA7D551`) |
| `0x30` | `bm_overkill.tga` `0xF85A6C` (`0xA7D3DA`) |

Icon-only types emit a single glyph: type 7 -> `0x2C` (`0xA7EF22`), type 6 -> `0x2D` (`0xA7F050`),
type 9 -> `0x30` (`0xA7F0F1`), type 8 -> `0x2F` (`0xA7F446`).
Digit path for types 0,1,2,3,4,5: `0xA7EEDA`..`0xA7EF0F` -> `0xA7F2B1`.

### 1.7 The self HP/MP-delta readout is also server-sent verbatim

Two more `0x43FDE0` call sites pass `flags = 0x20` (type 2 = green digits) with `this = localPlayer`:

* CHitResult tail `0x750DE8`..`0x750E43`: gated on the local player being the **attacker**
  (`cmp [localPlayer+0x78],[ebp+0x18]` `0x750DFA`, `cmp [localPlayer+0x7C],[ebp+0x1C]` `0x750E01`) and
  `[ebp+0x24] != 0` (`0x750E05`/`0x750E0A`). Value pushed = **CHitResult `+0x24` (u32)** (`0x750E20`),
  flags literal `0x20` (`0x750E27`).
* CMissileHitResult tail `0x7515C4`..`0x75161F`: same shape, value = **CMissileHitResult `+0x3C` (u32)**
  (`0x7515FC`), flags literal `0x20` (`0x751603`).

=> **`CHitResult+0x24` and `CMissileHitResult+0x3C` carry the local player's own resource delta for
this hit, sent by the server and displayed verbatim** (resolves LANE B bounded unknown #7).

### 1.8 Suppression filters (still server-driven, no math)

* Per-message: `movzx eax, word [ebp+0x20] ; call 0x5CAE00([0x1093198]+0x728, id)` (`0x750D2D`/`0x750D3E`)
  — if true, the whole numeric loop for this CHitResult is skipped. Same pattern in
  CMissileHitResult at `0x751624`/`0x751635` (`0x5CADD0`, on `+0x28`).
* The numeric loop uses a **different** actor registry (`mov ecx,0x102C6C0 ; call 0x446170`, `0x750D19`)
  than the animation loop, i.e. the two passes over the same 32-byte element array are independent
  (animation pass `0x750850`..`0x750C79`; numeric pass `0x750C93`..`0x750DC9`).

---

## 2. Does the client ever mutate HP itself from a hit?

### 2.1 Method (mechanical, whole-image)

Full linear sweep of `.text` (`0x401000`, `0x838A2C` bytes, **393,711 instructions** decoded with
capstone). For every instruction whose **destination operand is memory** with a **register base,
no index, dword size**, and displacement in `{0x44, 0x48, 0x4C, 0x50, 0x58, 0x1A8, 0x1AC}`
(excluding `esp`/`ebp` bases), the mnemonic was tabulated; separately a read-modify-write detector
looked back 10 instructions for `mov REG,[base+disp]` ... arithmetic on `REG` ... `mov [base+disp],REG`.

### 2.2 Result — the negative, stated flatly

**The client never subtracts damage from HP. It only redraws what the server sends.**

* **Arithmetic stores to `+0x44` / `+0x48` / `+0x1A8` / `+0x1AC`: ZERO.**
  No `add`, `sub`, `imul`, `neg`, `inc`, `dec`, `shl`, `sar`, `addss`, `subss`, `mulss` with any of
  those as destination, anywhere in `.text`.
* **Read-modify-write sequences on those offsets: ZERO.**
* Every store is `mov` (or `movss`/`movq` on unrelated float structs). Census of dword stores:
  `+0x44`: 142 `mov`, 15 `movss`; `+0x48`: 120 `mov`, 20 `movss`, 14 `movq`;
  `+0x1A8`: 5 `mov`; `+0x1AC`: 4 `mov`, 1 `movq`.
* The single arithmetic store found anywhere in the cluster was `add dword [esi+0x50], -1` at
  **`0x4C4363`** — inspected: it is a **refcount `Release()`** (`cmp dword [esi+0x50],1 ; jne`
  at `0x4C4353`, virtual destructor at `0x4C4361`, then `call [0xC3B168]` free at `0x4C4375`).
  Not MP, not an attribute block.

### 2.3 All five writers of the alternate HP pair `+0x1A8` / `+0x1AC`

| VA | shape | class |
|---|---|---|
| `0x464E02` / `0x464E0C` | `mov dword [esi+0x1A8], 0xFFFFFFFF` / `mov dword [esi+0x1AC], 1` | ctor init |
| `0x4651DB` / `0x4651E7` | `mov eax,[edi+0x1A8] ; mov [esi+0x1A8],eax` | **verbatim struct copy** (edi -> esi, `+0x1A2`..`+0x1B2`) |
| `0x4661E8` / `0x4661F8` | same, each field guarded by a bit of `[esi+0x1B8]` (`test al,0x40 ; jne` @ `0x4661DE`) | **masked merge**, still verbatim |
| `0x4B263D` / `0x4B2649` | `mov edx,[edi+0x1A8] ; mov [esi+0x1A8],edx` | verbatim struct copy |
| `0x4AD6BD` | `mov [esi+0x1A8], eax` inside a `+0x1A0..+0x1C4` stream unpack | deserializer |

### 2.4 The generic attribute-apply loop (server-driven, no math)

`0x464436`..`0x4644E0` is the canonical shape: one `test <mask>, <bit> ; jne skip ; mov REG,[src+off] ;
mov [dst+off],REG` per field, walking `+0x2C` through `+0x5D` in 4-byte steps, mask read from
`[edi+0x28]` (`0x46443E`). Bit `0x40` guards `+0x44` (`0x46447D`/`0x464481`/`0x464484`), the sign bit
guards `+0x48` (`0x464487`/`0x46448B`/`0x46448E`), `0x100` guards `+0x4C`, `0x200` guards `+0x50`,
`0x800` guards `+0x58`. Pure copy; the client is a mirror.

Other whole-block copies of the HP/MP quartet, all `mov`-only:
`0x41C4D4`..`0x41C4E3` (memberwise copy), `0x41C79E`..`0x41C7A4` (zero-init),
`0x464B02`..`0x464B1C` (ctor init), `0x464B8F`..`0x464BAA` (copy `+0x44`..`+0x54`),
`0x465678` (copy).

---

## 3. ATK / DEF / combat attributes

### 3.1 (b) — the external data-table columns

`STANDARD_STATUS` (UTF-16 literal `0xF152AC`) is opened by the table loader `0x4A2BB0`
(`push 0xF152AC` @ `0x4A2C5A`; sibling tables `STANDARD_MOB` `0xF152CC` @ `0x4A2C45`,
`EQUIP_VALUE` `0xF15294` @ `0x4A2C6D`, `AI_WANDER` `0xF0DF28` @ `0x4A2C08`).

Column literals are looked up with `0x891EE0(&out, L"<col>")`, which returns `{bool found; int/float value}`;
the value is stored only if `found` (`test cl,cl ; je`). **Complete extracted mapping** of the
combat row struct (base register `ebx`):

| column (UTF-16 literal VA) | -> row offset | store VA |
|---|---|---|
| `n_HPMAX` `0xF14F24` | `+0x10` | `0x4A3C36` |
| `n_RECOVER_HP` `0xF14F08` | `+0x14` | `0x4A3C56` |
| `n_STAMINAMAX` `0xF14EEC` | `+0x18` | `0x4A3C76` |
| `n_RECOVER_STAMINA` `0xF14EC8` | `+0x1C` | `0x4A3C96` |
| `n_DAMMIN_PHYSICS` `0xF14EA4` | `+0x20` | `0x4A3CB6` |
| `n_DAMMIN_MAGIC` `0xF14E84` | `+0x24` | `0x4A3CD6` |
| `n_DAMPLUS_PHYSICS` `0xF14E60` | `+0x28` | `0x4A3CF6` |
| `n_DAMPLUS_MAGIC` `0xF14E40` | `+0x2C` | `0x4A3D16` |
| `n_AC_PHYSICS` `0xF14E24` | `+0x30` | `0x4A3D36` |
| `n_AC_MAGIC` `0xF14E0C` | `+0x34` | `0x4A3D56` |
| `n_ABSORB_PHYSICS` `0xF14DE8` | `+0x38` | `0x4A3D76` |
| `n_ABSORB_MAGIC` `0xF14DC8` | `+0x3C` | `0x4A3D96` |
| `n_PENETRATE_PHYSICS` `0xF14DA0` | `+0x40` | `0x4A3DB6` |
| `n_PENETRATE_MAGIC` `0xF14D7C` | `+0x44` | `0x4A3DD6` |
| `f_ANTI_STUN` `0xF14D64` | `+0x48` | `0x4A3DF8` |
| `f_STUN` `0xF14D54` | `+0x4C` | `0x4A3E1C` |
| `f_ANTI_CURSE` `0xF14D38` | `+0x50` | `0x4A3E40` |
| `f_CURSE` `0xF14D28` | `+0x54` | `0x4A3E64` |
| `f_HITRATE` `0xF14D14` | `+0x58` | `0x4A3E88` |
| `f_DODGE` `0xF14D04` | `+0x5C` | `0x4A3EAC` |
| `f_ANTI_POWERHIT` `0xF14CCC` | `+0x60` | `0x4A3EF4` |
| `f_POWERHIT` `0xF14CEC` | `+0x64` | `0x4A3ED0` |
| `f_BYPASS` `0xF14CB8` | `+0x68` | `0x4A3F18` |
| `f_OVERHIT` `0xF14CA4` | `+0x6C` | `0x4A3F3C` |
| `f_MULTIPLY_POWERDAM` `0xF14C7C` | `+0x70` | `0x4A3F60` |
| `f_ABSORB_POWERDAM` `0xF14C58` | `+0x74` | `0x4A3F84` |
| `f_ABSORB_SHIELD` `0xF14C38` | `+0x78` | `0x4A3FA8` |
| `f_BLOCKRATE` `0xF14C20` | `+0x7C` | `0x4A3FCC` |

Plus, on the outer row object (`esi`): `n_ID` `0xF0C958` -> `+0x00` (`0x4A406F`),
`n_EXP_CURRENTLV` `0xF14C00` -> `+0x08` (`0x4A4120`), `n_POINT_ABILITY` `0xF14BE0` -> `+0x0C` (`0x4A4140`),
**`n_DEADLOSS` `0xF14BC8` -> `+0x10`** (`0x4A415D`; also read at `0x4E4C6A` / `0x4E4CB8`).

**Which are actually READ vs. merely named.** Every column above is **read** (parsed into memory),
and 18 of them additionally have a live accessor (§3.2). Names present in the image with
**no `.text` reference at all** (named only, parsed by nothing):

* `YADD_BLOCKRATE` `0xF27C5A` — **0 refs** (appears to be a truncated/typo'd literal: `Y` + `ADD_BLOCKRATE`).

Other combat-name families that ARE referenced, but by the **item-option** subsystem, not the
damage path (each has 3-4 refs in `0x56Bxxx` / `0x5AExxx` / `0x5AFxxx` / `0x654xxx` — affix
name->id tables used for tooltips):
`ADD_HITRATE` `0xF27D74`, `ADD_DODGE` `0xF27D60`, `ADD_POWERHIT` `0xF27D20`,
`ADD_ANTI_POWERHIT` `0xF27D3C`, `ADD_ABSORB_POWERDAM` `0xF27C9C`, `ADD_MULTIPLY_POWERDAM` `0xF27CC4`,
`ADD_ABSORB_SHIELD` `0xF27C78`, `ADD_PENETRATE_PHYSICS` `0xF27E18`, `ADD_PENETRATE_MAGIC` `0xF27DF0`,
`ADD_ABSORB_PHYSICS` `0xF27E68`, `ADD_ABSORB_MAGIC` `0xF27E44`, `ADD_DAMPLUS_PHYSICS` `0xF27EF0`,
`ADD_DAMPLUS_MAGIC` `0xF27ECC`, `ADD_DAMMIPHYSICS` `0xF27F38`, `ADD_DAMMIMAGIC` `0xF27F18`,
`ADD_MUL_DAMAGE` `0xF372A0`, `f_MUL_DAMAGE` `0xF372E8`, plus the `MUL_*` mirror set `0xF2C268`..`0xF2C3D4`.

Growth/config constants (1 ref each, all into the client-config reader `0x4838xx`..`0x483Cxx`):
`STR_BLOCKING` `0xF10ACC`, `STR_PENETRATE_PHYSICS` `0xF10AE8`, `STR_DAMMIN_PHYSICS` `0xF10B14`,
`AGI_DODGE` `0xF10A7C`, `AGI_ANTI_POWERHIT` `0xF10A58`, `AGI_ABSORB_PHYSICS` `0xF10A30`,
`AGI_DAMPLUS_PHYSICS` `0xF10A90`, `INT_PENETRATE_MAGIC` `0xF1090C`, `INT_ABSORB_MAGIC` `0xF108E8`,
`INT_DAMMIN_MAGIC` `0xF10934`, `PER_HITRATE` `0xF109AC`, `PER_POWERHIT` `0xF10990`,
`PER_DAMPLUS_MAGIC` `0xF1096C`, `DAM_POWERHIT` `0xF10850`, `MULTIPLY_BACKSTAB` `0xF1082C`,
`DODGE_CAST_POWER` `0xF110A4`, `DODGE_USE_SENSITIVITY` `0xF11064`, `ACCUMULATE_POWER` `0xF10B3C`,
`ATTACK_BAREHAND` `0xF11CB0`, `ARMOR_SLOT` `0xF12FEC`.
`n_DAMAGE_AREA` `0xF13B3C` is read at `0x48A016` / `0x4917B9` (missile AoE radius).

### 3.2 (a) — the character/stats UI, and the decisive caller list

There is a family of **18 derived-stat accessors** at `0x467E90`..`0x468E30`. Each has the shape:

```
base   = 0x467A60/0x467AF0/0x467B80/0x467C10/0x467CA0(this)     ; primary-stat total (int)
value  = (double)base * <const>                                  ; e.g. mulsd @ 0x46826F
value += (float)equip[+0xFC | +0x128 | +0x160]                   ; equipment bonus, if [this+0x18]
value += tableRow[<column offset>]                               ; if the avatar row exists
return max(0.0f, value)                                          ; comiss/jbe @ 0x468958..0x468963
```

Constants: `[0x1022628] = 0.001f`, `[0x102263C] = 2.0f`, `[0xF0D148] = 0.01` (double, used in the
primary-stat aggregator at `0x467BEE`).

| accessor | column read | offset | callers (complete) |
|---|---|---|---|
| `0x467E90` | `n_DAMMIN_PHYSICS` | `+0x20` | `0x57E814`, `0x57E926`, `0x6CFD78` |
| `0x467F80` | `n_DAMMIN_MAGIC` | `+0x24` | `0x57E7ED`, `0x57E8D8`, `0x6CFD55` |
| `0x468070` | `n_DAMPLUS_PHYSICS` | `+0x28` | `0x57E981`, `0x57EA16`, `0x6CFDC0` |
| `0x468160` | `n_DAMPLUS_MAGIC` | `+0x2C` | `0x57E9C7`, `0x57EAB2`, `0x6CFE06` |
| `0x468250` | `n_AC_PHYSICS` | `+0x30` | `0x57E7CA`, `0x57E88A`, `0x6CFD32` |
| `0x468430` | `n_ABSORB_PHYSICS` | `+0x38` | `0x57EDDD`, `0x57EE2C`, `0x6D006A` |
| `0x468520` | `n_ABSORB_MAGIC` | `+0x3C` | `0x57EE04`, `0x57EE7A`, `0x6D008D` |
| `0x468610` | (base only) | — | `0x57E9A4`, `0x57EA64`, `0x6CFDE3` |
| `0x468700` | `n_PENETRATE_MAGIC` | `+0x44` | `0x57E9EE`, `0x57EB00`, `0x6CFE29` |
| `0x4687F0` | `f_HITRATE` | `+0x58` | `0x57ED6B`, `0x6CFE5A` |
| `0x4688B0` | `f_DODGE` | `+0x5C` | `0x57F090`, `0x6D00BB` |
| `0x468970` | `f_POWERHIT` | `+0x64` | `0x57EBA3`, `0x6CFEC8` |
| `0x468A20` | `f_ANTI_POWERHIT` | `+0x60` | `0x57F01B`, `0x6D0129` |
| `0x468AD0` | `f_MULTIPLY_POWERDAM` | `+0x70` | `0x57EC0C`, `0x6D0007` |
| `0x468B70` | `f_ABSORB_POWERDAM` | `+0x74` | `0x57EFA6`, `0x6D018C` |
| `0x468C10` | `f_ABSORB_SHIELD` | `+0x78` | `0x57EF3D`, `0x6D025D` |
| `0x468CF0` | `f_BLOCKRATE` | `+0x7C` | `0x57EED4`, `0x6D01FA` |
| `0x468D90` | `f_BYPASS` | `+0x68` | `0x57ECF6`, `0x6CFFA4` |
| `0x468E30` | `f_OVERHIT` | `+0x6C` | `0x57EC81`, `0x6CFF36` |

**Every caller is in one of two UI modules** (`0x57Exxx`/`0x57Fxxx` = the stat/tooltip block;
`0x6CFxxx`/`0x6D0xxx` = the character-status panel refresh `0x6CFC90`).
Not one of `0x750770` (CHitResult handler), `0x750EC0` (CMissileHitResult handler), `0x43FBB0`,
`0x43FDE0`, `0x48D870`, `0x48DBA0`, `0x74F5A0`/`0x74FF60` (the array serializers) calls any of them.

The consumer at `0x6CFC90` is literally:
```
0x006CFD30  mov ecx, edi              ; edi = the actor
0x006CFD32  call 0x468250             ; = derived n_AC_PHYSICS
0x006CFD37  mov ecx, [esi+0x144]      ; the number-label widget
0x006CFD3D  mov [ecx+0x220], eax      ; <-- the value slot the earlier milestone pinned
0x006CFD43  mov byte [ecx+0x218], 1   ; dirty flag
```
repeated for `[esi+0x148]` <- `0x467F80`, `[esi+0x14C]` <- `0x467E90`, `[esi+0x1B0]` <- `0x468070`, etc.
Callers of `0x6CFC90`: `0x6D0326`, `0x6D05A0`, `0x6D05FA`, `0x6DC531`, `0x6DCE59` — all panel code.

Widget-name literals for this panel family (all UTF-16): `LABEL_ATK` `0xF29AF4` (ref `0x5849F0`),
`LABEL_MATK` `0xF29B08` (ref `0x5849B4`), `NUMLABEL_ATK` `0xF40034` (ref `0x6D42DF`),
`NUMLABEL_MATK` `0xF40050` (ref `0x6D429D`), `LABEL_ARMOR` `0xF1814C` (22 refs),
`LABEL_DODGE` `0xF297B4` (refs `0x585224`, `0x6D4B49`), `NUMBERLABEL_DODGE` `0xF43E00` (ref `0x71B560`),
`HTRACK_DODGE` `0xF43DE4` (ref `0x71B59C`).
The crew/"Sailor" panel binder `0x6D41B0` is fully decoded and binds, among others,
`NUMLABEL_AC` -> `[esi+0x140]` (`0x6D4267`), `NUMLABEL_MATK` -> `[esi+0x144]` (`0x6D42A3`),
`NUMLABEL_ATK` -> `[esi+0x148]` (`0x6D42DF`), `LABEL_HIT` -> `[esi+0x1BC]`, `LABEL_CRI` -> `[esi+0x1C0]`,
`LABEL_DODGE` -> `[esi+0x1D8]`, `LABEL_PARRY` -> `[esi+0x1E4]`.

---

## 4. Any embedded formula or constant table?

### 4.1 Mechanical search (method shown)

Every `imul / idiv / mul / div / fmul / fdiv / mulss / divss / mulsd / divsd / neg / cdq` in the
eight functions on the damage path was enumerated:

| range | function | hits |
|---|---|---|
| `0x750770`..`0x750EC0` | CHitResult handler | `neg eax` @ `0x7507DE`, `0x7509FF` — both the MSVC `dynamic_cast` idiom `neg eax ; sbb eax,eax ; and eax,REG`. **Nothing else.** |
| `0x750EC0`..`0x7516C0` | CMissileHitResult handler | `neg eax` @ `0x750F59`, `0x7512FF` — same idiom. **Nothing else.** |
| `0x43FDE0`..`0x440164` | hit-reaction FX dispatcher | **none** |
| `0x43FBB0`..`0x43FDD0` | FxNumber spawn | **none** |
| `0x48D870`..`0x48DB91` | knock/fall reaction | `imul esi` @ `0x48D8F8` (magic `0x92492493` + `sar 5` = divide by `0xE0`, an array element count) + 3 `mulsd` @ `0x48D95E/78/92` (scaling a Vec3) — **geometry only** |
| `0x48DBA0`..`0x48DEA9` | missile variant | 3 `mulsd` @ `0x48DC65/7F/99` — same Vec3 scaling |
| `0xA7EBA0`..`0xA7EE30` | glyph builder | `cdq` @ `0xA7EBFF` (the `abs`) + `fmul qword [0xF85BD0] (=22.0)` @ `0xA7ED61` (**glyph pitch in pixels**) |
| `0xA7E940`..`0xA7EBA0` | sign/width | **none** |

### 4.2 Every float constant on the hit path, identified

| VA | value | role | proof VA |
|---|---|---|---|
| `0xF48B6C` | `0.17f` | camera-shake amplitude | `fld` @ `0x7509A2`, `0x7512B3` |
| `0xF48B70` | `0.7f` | camera-shake triple | `movss` @ `0x75099A`, `0x7512B9`..`0x7512BF` |
| `0xF0D140` | `3.14159274` (double) | **pi**, added to the knock yaw | `fadd` @ `0x48DA28`, `0x48DD31` |
| `0xF091C0` | `80000000 x4` | sign-flip mask (`xorps` = negate a Vec3) | `0x48D94B`, `0x48DC52` |
| `0xF0989C` | `0.0f` | comparison zero | `comiss` @ `0x48DAB0`, `0x48DDBC` |
| `0xF0F5E0` | `75.0` (double) | FxNumber random spread offset (with `idiv 0x96` = 150) | `subsd` @ `0xA7F2D7`, `0xA7F31F` |
| `0xF15688` | `120.0` (double) | FxNumber vertical spawn offset | `addsd` @ `0xA7F344` |
| `0xF85BD0` | `22.0` (double) | glyph pitch in pixels | `fmul` @ `0xA7ED61` |
| `0x1022628` | `0.001f` | primary-stat -> derived-stat scalar (UI accessors) | `movss` @ `0x4688B9` |
| `0x102263C` | `2.0f` | same, for `n_AC_PHYSICS` | `movss` @ `0x468259` |
| `0xF0D148` | `0.01` (double) | primary-stat aggregator scalar | `mulsd` @ `0x467BEE` |
| `0xF0D324` | `0.75f` | FxNumber lifetime/alpha param | `fld` @ `0x43FD5C` |

**Flat statement: there is no damage formula in the client.** No level-indexed or type-indexed
lookup table feeds the displayed number; the only tables the combat code indexes are
(a) the effect/animation entry array at `[row+0xE4]`, stride `0xE0`, indexed by `CHitResult+0x28`
(`0x48D8D9`..`0x48D90B`), and (b) the `FxNumberCache` glyph->texture map (§1.6).
The `STANDARD_STATUS` combat columns are parsed and exposed only through the UI accessors of §3.2.

---

## 5. `0x48D870` — identification

**`0x48D870` = `<effect-manager>::SpawnKnockdownReaction(CNetActor* target, float yaw, int /*0*/, u16 effectId, u8 index)`**
— a **thiscall on the effect-manager singleton**, `ret 0x14` (5 stack args, `0x48DB8E`).
It is *not* damage-related; it produces the knock/fall reaction animation clips. It returns the
created effect node in `eax`, or `NULL` (`xor eax,eax` @ `0x48D8B0`).

`this` comes from `0x4162A0`, a one-time-init singleton returning the static object **`0x102DAD8`**
(`mov eax, 0x102DAD8 ; ret` @ `0x4162F2`/`0x416306`, guard flag `[0x102DB1C]`).

Call site in the CHitResult handler (`0x750A3E`..`0x750A62`):
```
movzx eax, byte [ebp+0x28]   ; CHitResult +0x28 (u8)   -> arg4 (index)
fld  dword [ebx+0x18]        ; element +0x18 (f32)     -> arg1 (yaw, radians)
movzx ecx, word [ebp+0x22]   ; CHitResult +0x22 (u16)  -> arg3 (effect id)
push 0                       ;                            arg2
push esi                     ; target actor            -> arg0
call 0x4162A0 ; mov ecx,eax ; call 0x48D870
mov edi,eax ; test edi,edi ; je 0x750A80      <-- the "non-null required" gate
```
On non-null, and only then, the handler positions the effect at the element's Vec3 hit point
(`lea edx,[ebx+0x0C] ; call 0x43BC70` @ `0x750A66`/`0x750A6C`), sets `or [edi+0x10],0x40000000`
(`0x750A71`) and attaches it (`call 0x4843F0` @ `0x750A7B`).

Internals, with every early-NULL return:
1. `arg0 == NULL` -> NULL (`0x48D8AC`/`0x48D8AE`).
2. `row = 0x702A10(arg3)`; if NULL, `row = 0x48AE40(this, arg2)`; still NULL -> NULL
   (`0x48D8BC`, `0x48D8CC`, `0x48D8D7`).
3. `count = ([row+0xF4] - [row+0xF0]) / 0xE0` (`0x48D8D9`..`0x48D904`);
   `if (arg4 >= count) -> NULL` (`0x48D906`/`0x48D908`).
4. `entry = 0x43B860(row+0xE4, arg4)` (`0x48D90B`); `if (0.0f >= entry[+0x10]) -> NULL`
   (`0x48D915`/`0x48D919`) — a duration gate.
5. `node = (*this->vtbl[+0x08])(arg0)` (`0x48D91B`..`0x48D923`); NULL -> NULL (`0x48D929`).
6. Direction: `0x488980(&mat)`, then **`0x49C8B0(&mat.row, arg1)`** (`0x48D941`) = `(sin a, -cos a, 0)`,
   scaled by `-entry[+0x04]` (`0x48D946`/`0x48D94B`), then `entry[+0x0C]`, `entry[+0x10]`.
7. Creates a `0x38`-byte clip from pool `0x102DCA4` (`0x48D9C3`) and binds it (`0x485DB0` @ `0x48D9E9`).
8. If `[row+0x24] & 0x200000` (`0x48DA15`): a second `0x34`-byte clip whose angle is
   `arg1 + pi - facing(arg0)` (`0x48DA22`..`0x48DA4C`; `0x427630` returns `[actor->motion+0x30]`).
9. Animation choice by `entry[+0x0C] > 0.0f` (`0x48DAAB`/`0x48DAB0`):
   * true -> wide `"_C_KNOCKED_001"` (`0xF13E14`, `0x48DAC5`) then `"_F_FALLING_000"` (`0xF13DF4`, `0x48DAF5`)
   * false -> wide `"_C_KNOCKED_000"` (`0xF13DD4`, `0x48DB10`)
10. `or [node+0x10], 1` (`0x48DB42`), two `0x487DD0` toggles, returns `node` (`0x48DB6E`).

**`0x48DBA0` is the missile twin** (`ret 0xC`, 3 args: `target`, `yaw`, `u16`) — the same body minus
the index/array lookup; called from the CMissileHitResult handler at `0x751352`.

---

## Bounded unknowns

Not proven from bytes. Do **not** treat as fact.

1. **Result-flag bits 2, 3, 4, 7, 11-15 of `element+0x1C`.** Bits 3/4 gate the animation branch
   (`0x75131C`, `0x751324`) and bit 7 the `0x469700` path (`0x75138F`), but `0x43FDE0` never tests
   them, so there is no texture name to identify them by. Bit 2 and bits 11-15 are tested nowhere I found.
2. **`bm_boom.tga` (glyph `0x2E`, `0xF85A8C`) is loaded into the cache but I found no emitter.**
   `FxNumber::Build` handles types 0-9 only; type 8 emits `0x2F` (gored) and type 9 emits `0x30`
   (overkill). Whether glyph `0x2E` is reachable at all is undetermined.
3. **The negative sign glyphs `0x29` (green -) and `0x2B` (blue -) have no proven emitter.**
   `0xA7E940` emits a sign only for `value > 0` (`jle` @ `0xA7E9B2`), i.e. only `0x28` / `0x2A`.
   Either negative deltas are shown unsigned, or an emitter exists outside the ranges swept.
4. **`CHitResult+0x24` / `CMissileHitResult+0x3C` being "the local player's HP/MP delta".**
   Proven: they are displayed as green digits with a `+`/no-sign glyph when the local player is the
   attacker. Whether the quantity is HP, MP, or something else is *inferred from the colour class*
   (type 2 vs type 3), not from a literal.
5. **`CHitResult+0x20` (u16).** Only proven use is as the key to the suppression filter
   `0x5CAE00` (`0x750D2D`/`0x750D3E`). Its content is opaque.
6. **The exact widget names bound in the class whose refresh is `0x6CFC90`.** I decoded a
   *different* panel's binder (`0x6D41B0`, the crew/"Sailor" panel) whose slot numbering is shifted
   by 4 from `0x6CFC90`'s, so I will **not** claim e.g. `NUMLABEL_ATK == n_DAMMIN_MAGIC`.
   What **is** proven is the accessor -> `[widget+0x220]` wiring (`0x6CFD3D`, `0x6CFD60`, `0x6CFD83`, ...).
7. **`FightAttr`** (`.?AVFightAttr@@` `0x0101B554`, name literal `0xF0E920`, ID global `0x10334CC`,
   `GetID` leaf `0x467A20`, vtable **`0xF0E8E0`**, sizeof **`0x1C`** from `0x40C609` and from
   vtable`+0x0C = 0x716010`). Its vtable slot `+0x18` is **`0x515EC0 = ret 8`, an empty stub** — so on
   this evidence it carries no wire payload. What its 0x1C bytes hold, and whether ATK/DEF ever
   travel inside it, is **not determined**.
8. **Function names assigned by usage shape only** (bodies not analysed):
   `0x891EE0` ("column fetch, returns {bool found; value}" — from `mov cl,[eax] ; mov eax,[eax+4] ;
   test cl,cl ; je`), `0x702A10` ("effect-row lookup by id"), `0x43B860` ("array element by index"),
   `0x896040` ("sprintf"), `0x467A60`/`0x467AF0`/`0x467B80`/`0x467C10`/`0x467CA0` ("primary-stat totals"),
   `0x49C7A0`/`0x49C6F0` ("sin"/"cos" — identified only by the `(x, -y, 0)` output shape).
9. **Which table the `ebx` row struct of §3.1 belongs to.** `STANDARD_STATUS`, `STANDARD_MOB` and
   `EQUIP_VALUE` are all opened by the same loader `0x4A2BB0`. `n_DEADLOSS` is proven to be
   `STANDARD_STATUS` (its literal `0xF14BC8` is read at `0x4E4C6A`, adjacent to the `STANDARD_STATUS`
   reference at `0x4E4C55`), but the table handle for the `n_HPMAX..f_BLOCKRATE` block specifically
   was not traced.
10. **Upper 16 bits of the `flags` argument at the two `flags = 0x20` call sites** (`0x750E27`,
    `0x751603`) are uninitialised stack (`mov word [esp+..],cx` followed by a dword push). Harmless
    because `0x43FDE0` only tests bits 0-10, but worth knowing if the server is ever made to echo it.

---

## Files touched by this lane

* `/tmp/re/LANE_C_CLIENT_COMPUTATION.md` (this file — created)
* `/tmp/re/strs.pkl` (created — cached ASCII/UTF-16 string index, scratch only)
* `/tmp/re/wr.pkl` (created — cached write-site index, scratch only)
* `/tmp/re/pe.py`, `/tmp/re/walk.py`, `/tmp/re/fn.py`, `/tmp/re/LANE_B_COMBAT_FAMILY.md` — **read only, not modified**
* The binary — **read only**

No repo file was written. No path under `src/`, `current/`, `tests/`, `tools/`, `pf_bridge/` was read
or written. No git operation, no DB access, no server boot, no UI.
