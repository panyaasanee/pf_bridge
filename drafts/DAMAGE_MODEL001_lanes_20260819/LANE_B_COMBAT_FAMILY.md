# LANE B — Combat Vital family (static RE, byte-exact)

Binary: `GameClient.local.bin` (v134 staging)
SHA-256 asserted at analysis time: `9627211412AC60D50AD189CE5A629443CE928EC23A9F8D219DFB2B157028B623` — **MATCH**
Image base `0x400000`. Sections: `.text` VA `0x401000` (0x838A2C), `.rdata` VA `0xC3B000`, `.data` VA `0x101A000`.

All VAs below are **virtual addresses in this image**. Every numeric claim carries the instruction/data VA it was read from.

---

## 0. Identification method (proved, not guessed)

Two independent chains were used; **both agree for all 9 classes**.

### Chain A — name string -> ID thunk -> ID global -> `GetVitalID` vtable method -> vtable base

1. ASCII class-name string located in `.rdata`.
2. Exactly one CRT once-init thunk pushes that string:
   `push <str> ; call 0x89C080 ; mov ecx,eax ; call 0x89BD00 ; mov word ptr [<ID global>], ax ; ret`
3. Exactly one `.text` site reads that ID global. It is always a 2-instruction leaf
   `mov ax, word ptr [<ID global>] ; ret` = **`GetVitalID()`**.
4. That leaf's address appears exactly once in `.rdata`, at `vtable + 0x10`. -> vtable base = refVA - 0x10.
5. Sanity gate: `dw(vtable+0x08) == 0x401B20` for every one of them (the chief's known marker). **All 9 pass.**

| class | name string VA | ID thunk VA | ID global VA | GetVitalID VA | vtable VA |
|---|---|---|---|---|---|
| CFightMsgVital | `0xF48AE8` | `0xC0C100` | `0x0108A2D4` | `0x74E600` | **`0xF489C8`** |
| ActionVital | `0xF48AF8` | `0xC0C120` | `0x0108A2D8` | `0x74E680` | **`0xF489EC`** |
| ActionPickVital | `0xF48B04` | `0xC0C140` | `0x0108A2DC` | `0x74E860` | `0xF48A10` |
| ActionItemVital | `0xF48B14` | `0xC0C160` | `0x0108A2E0` | `0x74E960` | `0xF48A34` |
| CShotMissileVital | `0xF48B24` | `0xC0C1C0` | `0x0108A2EC` | `0x74EA50` | **`0xF48A58`** |
| CKnockdownVital | `0xF48B38` | `0xC0C1E0` | `0x0108A2F0` | `0x74EBD0` | **`0xF48A7C`** |
| CHitResult | `0xF0B5F8` | `0xC0C180` | `0x0108A2E4` | `0x74F9C0` | `0xF48AA0` (chief, re-confirmed) |
| CMissileHitResult | `0xF0B5E4` | `0xC0C1A0` | `0x0108A2E8` | `0x74FA80` | **`0xF48AC4`** |
| TargetVital | `0xF30B0C` | `0xBEE940` | `0x01082098` | `0x51DF10` | **`0xF1FEBC`** |

> ### CORRECTION to the briefing
> The briefing stated the vtable at `0xF48AC4` (serializer `0x750110`, handler `0x750EC0`) is `CFightMsgVital`,
> inferred from the adjacent string `CFightMsgVital` at `0xF48AE8`.
> **That is wrong.** `0xF48AC4` is **`CMissileHitResult`** — proven at `0xF48AD4` holding `0x74FA80`,
> and `0x74FA80` = `mov ax,[0x0108A2E8] ; ret` (`0x74FA80`..`0x74FA86`), and `0x0108A2E8` is written only by
> the thunk at `0xC0C1A0` which pushes `0xF0B5E4` = `"CMissileHitResult"`.
> Independently confirmed by the ctor at `0x74F9E0`: `mov dword ptr [esi], 0xF48AC4` at `0x74FA2C`,
> that ctor is called at `0x755069` immediately after `push 0x58 ; call 0x88D020` (`0x75504D`/`0x75504F`),
> and `dw(0xF48AC4+0x0C) = 0x5F29D0` = `mov eax, 0x58 ; ret`.
> **The name-string block in `.rdata` is a separate literal pool from the vtable block — adjacency is NOT a valid identifier here.** `CFightMsgVital`'s real vtable is `0xF489C8`, several slot-groups earlier.

### Chain B — the ID hash, reimplemented and verified

`0x89BD00` -> `0x89B220` is the name hash (`0x89B220`..`0x89B27C`):

```
h : uint16 = 0
for i in 0..len-1:
    di : int16 = (int8)s[i] * (int16)(i+1)      ; 0x89B260 movsx di,[ecx+esi] / 0x89B268 imul di,bx
    h = (h + di) & 0xFFFF                        ; 0x89B26D add dx,di
return (uint16)h                                 ; 0x89B276 mov ax,dx
```

Reimplemented in Python and evaluated — **every ID in the task brief reproduces exactly**:

| name | computed | brief |
|---|---|---|
| CFightMsgVital | `0x29DC` | `0x29DC` OK |
| CKnockdownVital | `0x3123` | `0x3123` OK |
| CShotMissileVital | `0x3E0F` | `0x3E0F` OK |
| CMissileHitResult | `0x3EE5` | `0x3EE5` OK |
| TargetVital | `0x1ADD` | `0x1ADD` OK |
| ActionVital | `0x1AEA` | `0x1AEA` OK |
| CHitResult | `0x16F7` | `0x16F7` OK (chief's value) |
| ActionPickVital | `0x300B` | (not in brief) |
| ActionItemVital | `0x3058` | (not in brief) |

---

## 1. Vtable slot meanings (refined)

Confirmed 9-slot layout, spacing `0x24`:

| slot | meaning | evidence |
|---|---|---|
| +0x00 | `GetPool()` — returns a static pool object ptr | `0x74E610`: `mov eax,0x108A2C8 ; ret` |
| +0x04 | scalar-deleting dtor + pool free-list return | `0x74EED0`..`0x74EF2D` |
| +0x08 | constant `0x401B20` for the whole family | all 9 |
| +0x0C | **`GetSize()`** — `mov eax,<sizeof> ; ret` | see section 2 |
| +0x10 | **`GetVitalID()`** — `mov ax,[ID global] ; ret` | see section 0 |
| +0x14 | (unnamed; 1 call inside) | e.g. `0x74F4A0` |
| +0x18 | **SERIALIZER** `void __thiscall (CStream* s, bool bWrite)` | calls `0x89A600`/`0x89A640` |
| +0x1C | **INBOUND HANDLER** `bool __thiscall (arg)` , `ret 4` | see section 4 |
| +0x20 | `0x710440` for all 8 in the `0xF48xxx` block; TargetVital has `0xA106C0` | data |

Serializer prologue is identical in all of them:
`cmp byte ptr [esp+8],0` -> **flag==0 takes the READ branch (`0x89A640`), flag!=0 takes the WRITE branch (`0x89A600`)**.
Example: `0x74E6A0` / `je 0x74E74C` at `0x74E6B7`. Both branches emit an identical tag sequence (verified for CShotMissileVital: write `0x74EA89..0x74EAF2` vs read `0x74EB04..0x74EB6D`).

---

## 2. Per-class header table

| class | vtable | serializer (+0x18) | handler (+0x1C) | handler is `0x710440`? | ctor | sizeof | # wire fields |
|---|---|---|---|---|---|---|---|
| CFightMsgVital | `0xF489C8` | `0x5F28D0` | `0x750270` | **no — real** | `0x74E5D0` | `0x1C` (28) | 2 |
| ActionVital | `0xF489EC` | `0x74E6A0` | `0x7516C0` | **no — real** | `0x74E620` | `0x50` (80) | 10 |
| CShotMissileVital | `0xF48A58` | `0x74EA70` | `0x750630` | **no — real** | `0x74EA00` | `0x38` (56) | 8 |
| CKnockdownVital | `0xF48A7C` | `0x74EBF0` | `0x750700` | **no — real** | `0x74EB80` | `0x38` (56) | 5 |
| CMissileHitResult | `0xF48AC4` | `0x750110` | `0x750EC0` | **no — real** | `0x74F9E0` | `0x58` (88) | 8 + array |
| TargetVital | `0xF1FEBC` | `0x72A4D0` | `0xA106C0` | **no — a *different* stub, `xor al,al ; ret 4` (returns FALSE)** | inlined only (see below) | `0x28` (40) | 2 |
| *(CHitResult, ref)* | `0xF48AA0` | `0x750040` | `0x750770` | no — real | `0x74F940` | `0x48` (72) | 5 + array |

**sizeof proven twice, independently:**
* (a) `push <N> ; call 0x88D020` (operator new) immediately before the ctor call, inside the prototype-registration function `0x754F51`:
  `0x754F62`=0x1C->ctor `0x74E5D0`; `0x754F91`=0x50->`0x74E620`; `0x754FC0`=0x60->`0x74E7E0`; `0x754FEF`=0x70->`0x74E8E0`; `0x75501E`=0x48->`0x74F940`; `0x75504D`=0x58->`0x74F9E0`; `0x75507C`=0x38->`0x74EA00`; `0x7550AB`=0x38->`0x74EB80`. TargetVital: `0x51E62F` `push 0x28 ; call 0x88D020`.
* (b) vtable slot `+0x0C`: `0x716010`=0x1C, `0x63B130`=0x50, `0x73DE00`=0x60, `0x7318A0`=0x70, `0x63A6E0`=0x38 (shared by CShotMissileVital **and** CKnockdownVital), `0x5E6230`=0x48, `0x5F29D0`=0x58, `0x51DF20`=0x28.

The registration function `0x754F51` also assigns a sequential slot index at `[esp+0x14]`:
`3`=CFightMsgVital (`0x754F70`), `4`=ActionVital (`0x754F9F`), `5`=ActionPickVital (`0x754FCE`), `6`=ActionItemVital (`0x754FFD`), `7`=CHitResult (`0x75502C`), `8`=CMissileHitResult (`0x75505B`), `9`=CShotMissileVital (`0x75508A`), `10`=CKnockdownVital (`0x7550B9`).

**Common base object layout** (set by every ctor before the derived vtable store), e.g. `0x74E5D4`..`0x74E5E6`:
`+0x00` vtable (base = `0xF86D6C`), `+0x04` byte, `+0x08` dword, `+0x0C` dword, `+0x10` byte, `+0x11` byte.
Derived wire payload starts at `+0x14` (CFightMsgVital only) or `+0x18` (all others). **None of `+0x00..+0x13` is serialized.**

**TargetVital has no standalone constructor.** It is constructed inline in two pool-growth routines:
`0x51E63F`..`0x51E664` (vtable store `0x51E65A`, `mov byte [esi+0x11],1` at `0x51E660`) and `0x5EEB7D`..`0x5EEB9E` (vtable store `0x5EEB8F`). Both allocate `0x28` bytes.

---

## 3. Wire field lists (byte-exact, WRITE branch order)

### 3.0 Tag table — empirical census of the whole `.text`

Every `push <size> ... push <tag> ; call 0x89A600|0x89A640` site was tabulated (393,711 instructions swept). Observed `(tag,size)` pairs are 1:1 — **no tag is ever used with two different sizes**:

| tag | size | count | proven meaning |
|---|---|---|---|
| `0x05` | 1 | 2 | *unknown* (size 1) |
| `0x08` | 1 | 8 | *unknown* (size 1) — used by TargetVital `+0x20` |
| `0x0B` | 1 | 50 | `u8` (from server source) |
| `0x0F` | 2 | 18 | **`i16` (signed)** — see 4.2 (`movsx` at `0x750695`) |
| `0x12` | 2 | 44 | `u16` (from server source) |
| `0x14` | 4 | 53 | `u32` (from server source); **read as signed in places, see section 5** |
| `0x19` | 4 | 8 | *unknown* (size 4) |
| `0x26` | 4 | 7 | *unknown* (size 4) |
| `0x2A` | 4 | 14 | `f32` (from server source) |
| `0x32` | 8 | 31 | `qword` (from server source) |

Vec3 sub-serializer `0x5F3490` (write) / `0x5F34D0` (read) = 3 x tag `0x2A`, 12 bytes.

---

### 3.1 `CFightMsgVital` — ID `0x29DC`, sizeof `0x1C`, serializer `0x5F28D0`

| # | tag | type | size | obj offset | write VA | read VA |
|---|---|---|---|---|---|---|
| 1 | `0x14` | u32 | 4 | `+0x14` | `0x5F28E9` | `0x5F290A` |
| 2 | `0x14` | u32 | 4 | `+0x18` | `0x5F28F8` | `0x5F2919` |

Wire = **8 bytes payload + 2 tag bytes**. Field 2 (`+0x18`) is the **message code**; field 1 (`+0x14`) is its parameter (see 4.1).

### 3.2 `ActionVital` — ID `0x1AEA`, sizeof `0x50`, serializer `0x74E6A0`

| # | tag | type | size | obj offset | write VA |
|---|---|---|---|---|---|
| 1 | `0x32` | qword | 8 | `+0x18` | `0x74E6BD` |
| 2 | `0x32` | qword | 8 | `+0x20` | `0x74E6CC` |
| 3 | `0x32` | qword | 8 | `+0x28` | `0x74E6DB` |
| 4 | `0x14` | u32 | 4 | `+0x30` | `0x74E6EA` |
| 5 | `0x19` | ?32 | 4 | `+0x34` | `0x74E6F9` |
| 6 | `0x2A` | f32 | 4 | `+0x38` | `0x74E708` |
| 7 | Vec3 | 3x`0x2A` | 12 | `+0x3C..+0x47` | `0x74E712` (`call 0x5F3490`) |
| 8 | `0x0B` | u8 | 1 | `+0x48` | `0x74E724` |
| 9 | `0x12` | u16 | 2 | `+0x4A` | `0x74E733` |
| 10 | `0x0B` | u8 | 1 | `+0x4C` | `0x74E742` |

Read branch mirrors exactly at `0x74E74C`..`0x74E7D1`. Ctor zero-inits `+0x18..+0x4C` (`0x74E651`..`0x74E674`).
Fields 1 and 2 form the actor 64-bit ID: the handler loads `[esi+0x18]`/`[esi+0x1C]` as the lo/hi halves (`0x7516E7`/`0x7516EA`). Field 3 (`+0x28`) is read as two dwords `+0x28`/`+0x2C` in the handler (`0x7517F7`/`0x7517F3`).

### 3.3 `CShotMissileVital` — ID `0x3E0F`, sizeof `0x38`, serializer `0x74EA70`

| # | tag | type | size | obj offset | write VA | read VA |
|---|---|---|---|---|---|---|
| 1 | `0x32` | qword | 8 | `+0x18` | `0x74EA89` | `0x74EB04` |
| 2 | `0x32` | qword | 8 | `+0x20` | `0x74EA98` | `0x74EB13` |
| 3 | `0x14` | u32 | 4 | `+0x28` | `0x74EAA7` | `0x74EB22` |
| 4 | `0x0F` | **i16** | 2 | `+0x2C` | `0x74EAB6` | `0x74EB31` |
| 5 | `0x0F` | **i16** | 2 | `+0x2E` | `0x74EAC5` | `0x74EB40` |
| 6 | `0x0F` | **i16** | 2 | `+0x30` | `0x74EAD4` | `0x74EB4F` |
| 7 | `0x0F` | **i16** | 2 | `+0x32` | `0x74EAE3` | `0x74EB5E` |
| 8 | `0x2A` | f32 | 4 | `+0x34` | `0x74EAF2` | `0x74EB6D` |

Ctor zero-inits `+0x18..+0x34` (`0x74EA24`..`0x74EA43`), with `+0x2C/+0x2E/+0x30/+0x32` stored as `word` (`0x74EA33`..`0x74EA3F`) — matching 4x 2-byte fields. **`+0x2E/+0x30/+0x32` are a direction/target triple**: the handler sign-extends each (`movsx eax,word [esi+0x2E]` `0x750695`, `[esi+0x30]` `0x750699`, `[esi+0x32]` `0x75069D`) then `cvtsi2ss` (`0x7506A1`,`0x7506AB`,`0x7506B9`) into a float3 at `[esp+0xC..0x14]`.

### 3.4 `CKnockdownVital` — ID `0x3123`, sizeof `0x38`, serializer `0x74EBF0`

| # | tag | type | size | obj offset | write VA | read VA |
|---|---|---|---|---|---|---|
| 1 | `0x32` | qword | 8 | `+0x18` | `0x74EC09` | `0x74EC55` |
| 2 | `0x14` | u32 | 4 | `+0x20` | `0x74EC18` | `0x74EC64` |
| 3 | `0x14` | u32 | 4 | `+0x24` | `0x74EC27` | `0x74EC73` |
| 4 | Vec3 | 3x`0x2A` | 12 | `+0x28..+0x33` | `0x74EC31` (`call 0x5F3490`) | `0x74EC7D` |
| 5 | `0x2A` | f32 | 4 | `+0x34` | `0x74EC43` | `0x74EC8F` |

Ctor `0x74EB80` zero-inits `+0x18/+0x1C/+0x20/+0x24` as dwords (`0x74EBA2`..`0x74EBAB`) and `+0x28/+0x2C/+0x30/+0x34` as floats (`0x74EBAE`..`0x74EBBD`) — confirming the Vec3 at `+0x28` and the f32 at `+0x34`.

### 3.5 `CMissileHitResult` — ID `0x3EE5`, sizeof `0x58`, serializer `0x750110`

| # | tag | type | size | obj offset | write VA | read VA |
|---|---|---|---|---|---|---|
| 1 | `0x32` | qword | 8 | `+0x18` | `0x75012D` | `0x7501B1` |
| 2 | `0x14` | u32 | 4 | `+0x20` | `0x75013C` | `0x7501C0` |
| 3 | `0x12` | u16 | 2 | `+0x24` | `0x75014B` | `0x7501CF` |
| 4 | `0x12` | u16 | 2 | `+0x26` | `0x75015A` | `0x7501DE` |
| 5 | `0x12` | u16 | 2 | `+0x28` | `0x750169` | `0x7501ED` |
| 6 | Vec3 | 3x`0x2A` | 12 | `+0x2C..+0x37` | `0x750173` (`call 0x5F3490`) | `0x7501F7` |
| 7 | `0x2A` | f32 | 4 | `+0x38` | `0x750185` | `0x750209` |
| 8 | `0x14` | u32 | 4 | `+0x3C` | `0x750194` | `0x750218` |
| 9 | **ARRAY** | — | var | `+0x40` (container) | `0x75019E` (`call 0x74F5A0`) | `0x750222` (`call 0x74FF60`) |

Container at `+0x40` is a 3-word vector-like object: `+0x40` = base/first-block ptr, `+0x4C` = begin, `+0x50` = end
(handler reads `[ebp+0x4C]`/`[ebp+0x50]` at `0x750F6D`/`0x750F70`; sub-serializer reads `[esi+0xC]`/`[esi+0x10]` with `esi = this+0x40`, `0x74F5A8`/`0x74F5AB`).

### 3.6 `TargetVital` — ID `0x1ADD`, sizeof `0x28`, serializer `0x72A4D0`

| # | tag | type | size | obj offset | write VA | read VA |
|---|---|---|---|---|---|---|
| 1 | `0x32` | qword | 8 | `+0x18` | `0x72A4E9` | `0x72A50A` |
| 2 | `0x08` | ?8 | 1 | `+0x20` | `0x72A4F8` | `0x72A519` |

Inline ctor sets `+0x18`,`+0x1C` dword-0 and `+0x20` byte-0 (`0x51E651`..`0x51E657`) — matching qword `+0x18` and byte `+0x20`.

---

### 3.7 The shared hit-entry ARRAY — write `0x74F5A0`, read `0x74FF60`

Used by **CHitResult** (`+0x2C`, call at `0x75009F` / `0x7500F8`) and **CMissileHitResult** (`+0x40`, call at `0x75019E` / `0x750222`). Signature is `__cdecl (container*, CStream*)`.

**Count**: `mov eax,[esi+0x10] ; sub eax,[esi+0xC]` (`0x74F5A8`/`0x74F5AB`), `sar eax,5` (`0x74F5B3`) -> **element stride = `1<<5` = 32 bytes (`0x20`)**, `movzx ecx,ax` (`0x74F5B6`), written with **tag `0x12` (u16, 2 bytes)** at `0x74F5C8`. Read side reads the count with tag `0x12` at `0x74FF75` and loops `cmp di,word [esp+0x10] ; jb` (`0x75001F`/`0x750024`).

**Per element (stride 0x20):**

| # | tag | type | size | element offset | write VA | read VA |
|---|---|---|---|---|---|---|
| 1 | `0x32` | qword | 8 | `+0x00` | `0x74F62C` | `0x74FFCF` |
| 2 | `0x14` | u32 (**used signed**) | 4 | `+0x08` | `0x74F63E` | `0x74FFDF` |
| 3 | Vec3 | 3x`0x2A` | 12 | `+0x0C..+0x17` | `0x74F645` | `0x74FFEA` |
| 4 | `0x2A` | f32 | 4 | `+0x18` | `0x74F657` | `0x74FFFD` |
| 5 | `0x12` | u16 (**bitfield**) | 2 | `+0x1C` | `0x74F666` | `0x75000D` |

(`+0x1E..+0x1F` = 2 bytes padding to reach stride 32.)

---

## 4. Inbound handlers

**None** of the six target classes uses the shared no-op `0x710440`. All six have real bodies.
(`0x710440` does appear at vtable slot `+0x20` for all eight `0xF48xxx` classes — a *different* slot from the inbound handler.)

Common preamble in 4 of them: build a 64-bit actor key from `[this+0x18]`/`[this+0x1C]` via `0x402A20`, then resolve to an actor object via `0x446170`; NULL -> early-out returning `1`.
(`0x7516E7`/`0x7516EF`/`0x7516F6` ActionVital; `0x750637`/`0x75063F`/`0x750646` CShotMissileVital; `0x750703`/`0x75070C`/`0x750713` CKnockdownVital; `0x750F12`/`0x750F2A`/`0x750F31` CMissileHitResult.)

### 4.1 `CFightMsgVital` handler `0x750270` — pure client-side message dispatcher

* Reads **only** `[esi+0x18]` (`0x750295`) and `[esi+0x14]`. Writes no actor field directly.
* `lea edx,[ecx-0x186A0]` (`0x750298`) then `cmp edx,0x1C ; ja 0x7503F0` (`0x7502A2`/`0x7502A5`) ->
  **switch over codes `100000 .. 100028`** (`0x186A0` = 100000).
* Jump machinery: byte index table at **`0x750478`** (0x1D bytes), dword target table at **`0x75043C`** (15 entries), dispatch `jmp dword ptr [edx*4+0x75043C]` (`0x7502B2`).

Decoded switch (code -> target VA):

| code | target | what it does (VA of the decisive instruction) |
|---|---|---|
| 100000 | `0x7502B9` | show system msg with ID = `[esi+0x14]` (`0x7502B9`, call `0x5CBC00` @`0x7502C9`) |
| 100001-100003 | `0x750311` | fixed msg `0x149` (`0x750311`) |
| 100005 | `0x750325` | fixed msg `0x14B` (`0x750325`) |
| 100006 | `0x750307` | fixed msg `0x148` (`0x750307`) |
| 100007 | `0x75032F` | fixed msg `0x14C` (`0x75032F`) |
| 100008 | `0x7502DD` | if `[[0x1032EC4]+0x248]` non-null and `byte [..+0xA4] > 0` -> suppress; else msg `0x294` (`0x7502FD`) |
| 100009 | `0x7502D3` | fixed msg `0x147` (`0x7502D3`) |
| 100010 | `0x75031B` | fixed msg `0x14A` (`0x75031B`) |
| 100011 | `0x750339` | fixed msg `0x317`, no trailer (`0x750339`, jmps to `0x7503FC`) |
| 100016 | `0x7503B6` | msg `0x29D` with param `[esi+0x14]` (`0x7503B6`) |
| 100022, 100023 | `0x7503C0` | different UI channel: `[0x1093198]+0x550`, `call 0x5D39C0` (`0x7503CD`) |
| 100024 | `0x750343` | name lookup on `[esi+0x14]` (`0x4A1530` @`0x75034C`), msg `0x1B9` (`0x750376`), then `call 0x43FBB0(2, [esi+0x14])` (`0x7503AF`) |
| 100025 | `0x750412` | `call 0x4729E0(localPlayer)` (`0x75041C`) |
| 100028 | `0x7503D4` | `0x449240([[0x1032EC4]+0x50])` then **`mov byte ptr [eax+0x3C], 1`** (`0x7503EA`) |
| 100004, 100012-100015, 100017-100021, 100026, 100027 | `0x7503F0` | default |

Default path `0x7503F0`: `cmp ecx,0x186A0 ; jge 0x7503FC` (`0x7503F0`/`0x7503F6`) — **if the code is < 100000 it is used directly as a system-message string ID** (`mov eax,ecx` `0x7503F8`) and `bl=1` (`0x7503FA`) triggers a follow-up `0x4729E0(localPlayer)` (`0x75041C`). Codes >= 100000 outside the table fall through with `eax = 0` (from `xor eax,eax` at `0x7502A0`).
Always returns `al = 1` (`0x750424`).

### 4.2 `CShotMissileVital` handler `0x750630` — spawns a projectile

* Actor lookup from qword `+0x18`; NULL -> `mov al,1 ; ret 4` (`0x750651`..`0x750658`).
* Builds a projectile: pushes `[esi+0x24]`, `[esi+0x20]`, `[esi+0x28]`, `movsx edx,word [esi+0x2C]` (`0x750668`), plus literals `1`,`0`,`0`,`0` -> `call 0x402A90` (`0x750678`) -> `call 0x495DC0` (`0x75067F`). NULL result -> returns `al = 0` (`0x75068C`).
* Sets projectile direction/target from the **signed** i16 triple `+0x2E/+0x30/+0x32` (`0x750695`/`0x750699`/`0x75069D`, `cvtsi2ss` `0x7506A1`/`0x7506AB`/`0x7506B9`) -> `call 0x491E40` (`0x7506C6`).
* Sets the f32 at `+0x34` -> `call 0x491E90` (`0x7506D1`).
* Attaches to the owner list at `[actor+0x60]` -> `call 0x494470` (`0x7506DC`).
* `test byte ptr [edi+0x14], 1` (`0x7506E1`) -> if set, `call 0x4948F0` with `0.0f` (`0x7506EF`).

**Fields consumed:** `+0x18` (qword actor), `+0x20`,`+0x24`,`+0x28` (u32 x 3 -> projectile params), `+0x2C` (i16), `+0x2E/+0x30/+0x32` (i16 direction), `+0x34` (f32).

### 4.3 `CKnockdownVital` handler `0x750700` — knockback impulse

* Actor lookup from qword `+0x18`; requires `[actor+0x14]` non-null (`0x75071E`/`0x750721`).
* `fld [esi+0x2C]` (`0x750725`) and `fld [esi+0x28]` (`0x75072F`) -> pushed as two floats -> `call 0x4845A0` (`0x750735`).
  => **Vec3 components X (`+0x28`) and Z (`+0x2C`) are the horizontal knockback direction.**
* `fld [esi+0x30]` (`0x75073D`) -> `fstp dword ptr [edx+0x18]` (`0x750740`) where `edx = [actor+0x14]`.
  => **Vec3 component `+0x30` is stored verbatim into the actor's motion sub-object at `+0x18`.** This is the only direct actor-field WRITE in this handler.
* Then `0x4162A0` singleton -> indirect `call [vtbl+0x0C]` (`0x75075F`) with (`actor`, f32 `[esi+0x34]`, `[esi+0x20]`, `[esi+0x24]`) -> result fed to `call 0x4843F0` (`0x750764`).
* Always returns `al = 1` (`0x75076A`).

### 4.4 `ActionVital` handler `0x7516C0` — the action/state-change driver

* Actor lookup from qword `+0x18`; NULL -> return 1 (`0x7516FF`).
* **`cmp dword ptr [esi+0x30], 0xEA80` (`0x751705`)** — special-cased action code `0xEA80` (60032):
  requires an RTTI-ish type check via vtable slot 0 + `0x88F2B0` against `0x102CB04` (`0x751714`..`0x75171C`),
  then `test al,0x10` on `[actor+0x10]` (`0x751736`) **and** `test eax,0x100000` (`0x75173E`), then `call 0x4A0970([actor+0x40])` (`0x75174C`).
* `cmp eax, 0xEA82` (`0x751818`) -> path pushing literal `1`; `cmp eax, 0xEA83` (`0x751847`) -> same path with literal `0` (`0x75184E`). Both go through `0x48E5D0` (`0x751829`) and then **`or dword ptr [eax+0x10], 1`** (`0x751836`) followed by `0x4843C0` (`0x75183D`).
* Predicate `0x4889D0([esi+0x30])` (`0x75175F`) classifies the code; `0x4889E0` (`0x751853`) and `0x4889C0` (`0x751932`) are two more classifiers on the same field.
* Big branch at `0x7517DA`: passes `f32 [esi+0x38]`, `u8 [esi+0x48]`, `[esi+0x24]`, `lea [esi+0x3C]` (Vec3), `[esi+0x20]`, `[esi+0x2C]`, `[esi+0x28]`, `[esi+0x34]` (the tag-`0x19` field), `[esi+0x30]` -> `call 0x47AB30` (`0x751809`).
* Position path at `0x751870`: **`movq xmm0, qword ptr [esi+0x3C]` -> `movq [eax], xmm0` and `mov ecx,[esi+0x44] ; mov [eax+8], ecx`** where `eax = [actor+0x14] + 0x50` (`0x751875`) — i.e. **the Vec3 at `+0x3C` is written straight into the actor's motion object at `+0x50`** when `byte [esi+0x48] != 0` (`0x75186A`). Otherwise it goes through `0x43B6A0` (`0x75188A`) + `0x4845D0` (`0x7518A8`).
* `movzx edx, byte ptr [esi+0x48]` -> `call 0x4542D0` (`0x7518B5`); `movss` `[esi+0x38]` -> `[actor+0x14]+0x30` (`0x7518C6`), then `0x484450` / `0x484610`.
* **Bit test:** `mov cl, byte ptr [esi+0x4C] ; and cl,1 ; cmp cl,1 ; sete dl ; mov byte ptr [ebx+0x75], dl`
  (`0x75193E`,`0x751941`,`0x751944`,`0x751947`,`0x75194A`) — **bit 0 of the u8 at `+0x4C` becomes a boolean on the spawned action object at `+0x75`.**
* `test byte ptr [ebp+0x28], 0x80` (`0x751951`) is on an *animation* object, not on wire data.
* Tail `0x7519A9`: re-broadcasts `[esi+0x18]`,`[esi+0x1C]`,`[esi+0x28]`,`[esi+0x2C]`,`[esi+0x20]`,`[esi+0x24]`,`[esi+0x30]` to the UI/message system `[0x1093198]+0x728` -> `call 0x5CAF80` (`0x7519D1`).
* Always returns `al = 1` (`0x7519D6`).

### 4.5 `CMissileHitResult` handler `0x750EC0` (len 2046 bytes) — the damage applicator

1. `[ebp+0x20]` (u32) -> `0x402A90` (`0x750F06`) -> `0x47D720` (`0x750F0D`) = resolve the **missile instance**.
2. `[ebp+0x18]`/`[ebp+0x1C]` (qword) -> `0x402A20`/`0x446170` (`0x750F2A`/`0x750F31`) = resolve the **attacker**.
3. **`mov ecx,[ebp+0x50] ; sub ecx,[ebp+0x4C] ; test ecx, 0xFFFFFFE0 ; jne 0x75112D`** (`0x750F6D`,`0x750F70`,`0x750F73`,`0x750F79`)
   -> byte-length of the target array; `& ~0x1F != 0` means **count >= 2** and takes the multi-target loop at `0x75112D`.
   Count <= 1 takes the "missile impact only" path at `0x750F7F`.
4. Single/zero path: `or dword ptr [eax+0x14], 1` on the missile (`0x750F85`);
   **`movq xmm0, qword ptr [ebp+0x2C]` -> `movq qword ptr [eax+0x3C], xmm0`** and `mov edx,[ebp+0x34] ; mov [eax+0x44],edx` (`0x750F9A`,`0x750FA1`,`0x750FA6`,`0x750FA9`)
   => **the Vec3 at `+0x2C` is the impact position, copied verbatim into the effect object at `+0x3C`.**
   `fld [ebp+0x38]` (`0x750FAC`) -> `0x49C8B0` (`0x750FB7`).
5. Multi-target loop `0x751160`..`0x751128`: per element `ebx`, resolves the target from element `+0x00`/`+0x04` (`0x7511AD`/`0x7511B4`), then section 5 semantics.
6. Tail `0x7515C4`: if the **local player** (`[0x1032EC4]`) is the attacker (`cmp [eax+0x78],[ebp+0x18]` `0x7515D6`, `cmp [eax+0x7C],[ebp+0x1C]` `0x7515DD`) and `[ebp+0x3C] != 0` (`0x7515E4`) -> UI call `0x5CB190` (`0x7515F7`) and `0x43FDE0` with literal `0x20` (`0x751603`/`0x751608`).
7. `movzx eax, word ptr [ebp+0x28]` -> `0x5CADD0` (`0x751624`/`0x751635`) is a *suppression filter* — if it returns true, all remaining UI is skipped (`0x75163C`).
   Then `test ax,ax` on `[ebp+0x24]` (`0x751645`) and on `[ebp+0x26]` (`0x75164E`): **both zero -> `0x5CC640`** (`0x75166D`), otherwise `0x5CE010` (`0x75168D`).
8. Always returns `al = 1`.

### 4.6 `TargetVital` handler `0xA106C0`

```
0x00A106C0  xor al, al
0x00A106C2  ret 4
```
**Not** the shared `0x710440` (which is `mov al,1 ; ret 4`). This one returns **FALSE**, and it occupies *both* slot `+0x1C` and slot `+0x20` (`0xF1FED8`, `0xF1FEDC`). TargetVital is decode-capable and inert on the client, but its "false" return is a different code path from the ordinary decode-only stub.

---

## 5. Hit / miss / critical / damage / knockback semantics — instruction-level

### 5.1 The per-target hit entry (array element, stride `0x20`)

The **u16 at element `+0x1C`** is a **result-flags bitfield**. Every one of these tests is on `[ebx+0x1C]` where `ebx` is the current element (loaded `movzx eax, word ptr [ebx+0x1c]` at `0x7511E7` and `0x751318`):

| bit | mask | test VA(s) | behaviour if SET |
|---|---|---|---|
| 0 | `0x01` | `0x7511EB`, `0x7512D6` (`test byte ptr [ebx+0x1c],1`), CHitResult `0x7509D6` | **gates the entire "apply result" block.** Clear => jump to `0x751562` (from `0x7512DA`). |
| 1 | `0x02` | `0x7511EF`, `0x75137D` | at `0x7511EF` (with bit0 set) => **skip** the vtable `+0x34` call; at `0x75137D` => `or dword ptr [eax+0x14], 1` on the missile (`0x75138B`) |
| 3 | `0x08` | `0x75131C` | required to enter the damage-display block; clear => jump `0x751462` |
| 4 | `0x10` | `0x751324` | play effect by **name string `0xF48B4C` = wide `"_F_KNOCKED_002"`** via vtable slot `+0x28` (`0x751333`, `0x75133A`); clear => fall to the numeric-damage path `0x75133E` |
| 5,6 | `0x60` | `0x751204` (`test al,0x60`) | invoke target vtable slot `+0x34` with (`0`, attacker, `word [ebp+0x28]`) (`0x751208`..`0x751217`) |
| 7 | `0x80` | `0x75138F`, CHitResult `0x750A84` | conditional on `test byte ptr [eax+0x24],1` (`0x75139D`) -> `0x469700` (`0x7513A4`) -> indirect vtable `+0x38` (`0x7513B7`) |

**Bounded**: the *labels* hit / miss / block / critical are NOT proven. What IS proven is the gating structure: `0x01` = "this entry is live / apply it", `0x02` = a mutually-exclusive alternative to the `0x60` path, `0x08`+`0x10` select **named-effect** vs **numeric-damage** presentation.

### 5.2 Damage magnitude

* **`cmp dword ptr [ebx+8], 0 ; jge`** at `0x751219` (->`0x7512D6`) and `0x7512E0` (->`0x751318`);
  same pattern in the CHitResult handler at `0x750919` and `0x7509E0`.
  => the wire field at element `+0x08` (tag `0x14`, 4 bytes) is treated as a **signed int32**; **negative takes the "took damage" branch**. Non-negative skips the impact reaction entirely.
* **`fld dword ptr [ebx+0x18]`** at `0x751342` — the element f32 at `+0x18` is pushed together with `movzx ecx, word ptr [ebp+0x28]` (`0x75133E`) and the target into `0x4162A0`->`0x48DBA0` (`0x75134B`/`0x751352`) which returns an object; on success `0x43BC70` is called with `lea edx,[ebx+0xC]` (`0x75135F`/`0x751365`) = **the element's Vec3 (hit position)**, then `or dword ptr [edi+0x10], 0x40000000` (`0x75136A`) and `0x4843F0` (`0x751374`).
  => element `+0x18` (f32) is the magnitude fed to the floating damage-number / effect spawner, positioned at element `+0x0C` (Vec3).
* **Camera shake** (`0x75129A`..`0x7512D1`), reached only when element `+0x08 < 0` and one of the participants is local:
  `fld dword ptr [0xF48B6C]` = **`0.17f`**, `movss xmm0, dword ptr [0xF48B70]` = **`0.7f`** written into `[esp+0x40]`,`[esp+0x44]`,`[esp+0x48]` (`0x7512B3`,`0x7512B9`,`0x7512BF`) -> `call 0x43D220` (`0x7512C5`), then `0x443E80` with `0xF0D5EC` (`0x7512D1`).
  Locality gate: `mov eax,[0x1032EC4]` (`0x751223`), `cmp edi,eax ; je` (`0x751228`/`0x75122A`), `cmp esi,eax ; je` (`0x75122C`/`0x75122E`), plus predicates `0x7504A0` (`0x751238`,`0x75124C`), `0x750590` (`0x751260`,`0x751274`), `0x7505D0` (`0x751281`,`0x75128E`) — all party/group-membership tests against `[0x1032EC4]` (`0x7504E7`, `0x75059E`).
* **Actor flags written by the handler:**
  `or dword ptr [esi+0x70], 0x100` (`0x7511E0`) on the target, gated by `test dword ptr [esi+0x10], 0x10000` (`0x7511C3`) and the 64-bit `element+0 > 0` test (`0x7511CC`,`0x7511D0`,`0x7511D2`,`0x7511D4`,`0x7511D7`).
  `test dword ptr [esi+0x10], 0x400` (`0x751462`) -> also plays `"_F_KNOCKED_002"` (`0x75147A`).
  `test dword ptr [edx+0x24], 0x40000` (`0x7513DE`).

### 5.3 Knockback (CKnockdownVital)

Proven in 4.3: the Vec3 at `+0x28` is split — `X (+0x28)` and `Z (+0x2C)` go to `0x4845A0` as a pair (`0x750725`/`0x75072F`/`0x750735`), and `+0x30` is stored raw into `[actor->motion + 0x18]` (`0x75073D`/`0x750740`). The f32 at `+0x34` is the scalar passed to the indirect `call [vtbl+0x0C]` (`0x75074B`/`0x75075F`).

### 5.4 Action-code constants (ActionVital)

`0xEA80` = 60032 (`0x751705`), `0xEA82` = 60034 (`0x751818`), `0xEA83` = 60035 (`0x751847`). All compared against the u32 at `+0x30`.
Bit extraction: `+0x4C` bit 0 -> boolean at `[actionObj+0x75]` (`0x75193E`..`0x75194A`).

### 5.5 Message-code constants (CFightMsgVital)

Base `0x186A0` = 100000, table span 29 entries (`0x7502A2`). Full decode in 4.1.

---

## Bounded unknowns

Everything below is **NOT proven from bytes** and must not be treated as fact.

1. **Tag `0x19` (size 4)** — used by `ActionVital +0x34` (`0x74E6F9`). Only 8 sites image-wide. Size is proven (4). Signedness/semantic (i32? enum? handle?) is **unknown**. The handler pushes it as a plain dword (`0x7517FB`) into `0x47AB30` without sign-extension or FP conversion, so it is not a float and not a sub-32-bit quantity — but that is all.
2. **Tag `0x08` (size 1)** — used by `TargetVital +0x20` (`0x72A4F8`). 8 sites image-wide. Size proven; type **unknown**. Plausibly `i8` paired with `0x0B`=`u8`, by analogy with `0x0F`(2)/`0x12`(2) and `0x14`(4)/`0x19`(4) — **this is an inference, not a proof.**
3. **Tags `0x05` (size 1) and `0x26` (size 4)** — appear elsewhere in the image, not in this family. Sizes proven; types unknown.
4. **Semantic labels for the element `+0x1C` bits.** The gating *structure* is proven (5.1) but the words "hit", "miss", "block", "critical", "dodge" are **not** in the binary for these bits. Do not name them in the server without a runtime capture.
5. **Whether `+0x08 < 0` means "damage" vs "heal is >= 0".** Proven: `jge` skips the impact reaction. The non-negative branch's meaning (heal? no-op? absorb?) is not tied to any constant I could find.
6. **Meaning of `CMissileHitResult +0x24` and `+0x26` (u16 each).** Only proven use: both-zero vs not-both-zero selects `0x5CC640` vs `0x5CE010` (`0x751645`,`0x75164E`,`0x75166D`,`0x75168D`). Their content is opaque.
7. **Meaning of `CMissileHitResult +0x3C` (u32).** Only proven use: non-zero gate + parameter to `0x5CB190` and `0x43FDE0` on the local-attacker path (`0x7515E1`,`0x7515FC`).
8. **`CFightMsgVital +0x14`** is only *sometimes* read — for codes 100001-100011 it is never read. Whether the server must still send a meaningful value is unknown (it is always written; only the value's meaning is conditional).
9. **`TargetVital`'s role.** It is a registered Vital with an ID (`0x1ADD`) and a 2-field wire form, but its handler returns FALSE (`0xA106C0`) and it is pool-allocated from two inlined sites (`0x51E600`, `0x5EE7D1`) rather than from the prototype table at `0x754F51`. **Whether it is ever sent on the wire as a top-level message, or only used as an internal container, is not determined.**
10. **`ActionPickVital` (`0x300B`, vtable `0xF48A10`, sizeof `0x60`) and `ActionItemVital` (`0x3058`, vtable `0xF48A34`, sizeof `0x70`)** were identified in passing (same registration block) but **their field lists were not walked** — out of scope for this lane.
11. **The exact container type at `CMissileHitResult+0x40` / `CHitResult+0x2C`.** The three observed words (`+0x00` block ptr, `+0x0C` begin, `+0x10` end) and the guard calls to `[0xC3B4C0]` (`0x74F5D5`, `0x74F5EC`, ...) are consistent with an MSVC iterator-checked container, but the full header layout is not derived. **Only the count encoding (u16, tag `0x12`) and stride (32) matter for the wire, and both are proven.**
12. `0x402A20`, `0x402A90`, `0x446170`, `0x47D720` are named "make 64-bit key", "make handle", "resolve actor", "resolve missile" **by usage pattern only**; their bodies were not analysed.

---

## Files touched by this lane

* `/tmp/re/LANE_B_COMBAT_FAMILY.md` (this file — created)
* `/tmp/re/fn.py` (created — small helper adding `fdump()`/`fnend()`/`fstart()` on top of the existing `pe.py`)
* `/tmp/re/pe.py`, `/tmp/re/walk.py` — **read only, not modified**
* The binary — **read only**

No repo file was written. No `src/`, `current/`, `tests/`, `tools/`, `pf_bridge/` path was touched. No git operation, no DB, no server, no UI.
