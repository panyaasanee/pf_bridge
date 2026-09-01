# PF pool 0x0046BAA0 reader-only correction and fail-closed blocker

[MEASURED] `source=IMAGE`. V1 and every existing overlay remain immutable.

## Result

The additive A2 overlay publishes exactly **3 CHANGED reader rows** and no
other row:

| message/member | V1 line | reader call | result |
|---|---:|---:|---|
| `ItemBindingLockVitalRes +0x18` | 963 | `0x005EAC84` | `SUBCALL:0x0046BD30` |
| `TradeItemResultVital +0x1C` | 2587 | `0x00664C98` | `SUBCALL:0x0046BD30` |
| `GCGSSS_GuildStorageResultVital +0x2C` | 3837 | `0x00673ADB` | `SUBCALL:0x0046BD30` |

A2 delta sha256: `5099d8e6f09ac978c938f13d5059c2b735764ef7ed651ace28f9682880e317fa`. Unchanged rows copied: **0**. Writer rows
changed: **0**. Duplicate delta keys: **0**. Duplicate base keys: **0**.
Existing-overlay base-key overlap: **0**. Every emitted row is
`source=IMAGE`.

No Priority delta is emitted. `ItemBindingLockVitalRes`,
`TradeItemResultVital`, and `GCGSSS_GuildStorageResultVital` all remain
**OPEN**. Closed-count change: **0**.

## Why the reader is fixed

- Pool helper `0x0046BAA0..0x0046BBAB`: file offset `0x0006AEA0`,
  267 bytes, 87 reachable instructions, sha256
  `8a996a4e9c1bf3bdfd81d1711fbf99dba817ee21d0a48bc3200978f3ca4d8924`.
- Both helper arms call base constructor `0x0046B410` at `0x0046BB04`
  and `0x0046BB82`.
- Constructor `0x0046B410..0x0046B497`: file offset `0x0006A810`,
  sha256 `5a5d9aba90e35eea8119d252751058561c125ff68e54c3416a8bef6230872ddc`.
  It stores vtable `0x00F0EBB0` at `0x0046B440`.
- Vtable `0x00F0EBB0 +0x34 -> 0x0046BD30`. The serializer span is
  `0x0046BD30..0x0046BEA1`, sha256
  `b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1`.

Each corrected site is after that exact helper result is stored into the same
member and reloaded for a reader-mode-zero call through slot `+0x34`. The
nested serializer is referenced, not flattened.

## Why the messages remain OPEN

Exact blocker: `BLOCKED_WRITE_DYNAMIC_IDENTITY`. The writer sites do not call
the pool helper; they dispatch a pre-existing `ItemAttr*` through slot
`+0x34`. The IMAGE has at least two exact targets:

| candidate | vtable | serializer | serializer sha256 |
|---|---:|---:|---|
| base `ItemAttr` | `0x00F0EBB0` | `0x0046BD30` | `b21137bde28452c08f8fa6a2eda18accf9c2d51b9b7d82a1b6997986feba86c1` |
| derived `ItemAttr` | `0x00F4A188` | `0x00766C90` | `2e530374f093af280c441ae3e23f97eedbd8b7a02d8b0598fe1b5bba2488b771` |

The untouched writer rows are V1 lines 954 (`0x001EA019`), 2576
(`0x0026400B`), and 3818 (`0x00272E01`). No result collapses these candidates.

For Guild Storage, clone `0x00673AF0..0x00673BA2` (sha256
`f9ad87e3c42588f0346590203d22ab2215fe4004f8344250cb19327833b3da56`)
uses fixed pool `0x0046F4D0` for member `+0x28`, but calls generic clone
`0x004636F0` for member `+0x2C`. Generic clone preserves the source dynamic
identity through source-vtable slots `+0x14` and `+0x24`. Thus the fixed
`+0x28` dependency does not close the whole message.

## Pinned roots

| root | exact span | sha256 |
|---|---|---|
| `ItemBindingLockVitalRes` | `0x005EABD0..0x005EAC8C` | `1d0b7c857719202e760b647dd54a20a8d921559ca41bf85cde799c571f26e88a` |
| `TradeItemResultVital` | `0x00664BA0..0x00664D27` | `92cfcdb8536fcbe50c1af4388116bf21a45540284266dceeebf3725736becec9` |
| `GCGSSS_GuildStorageResultVital` | `0x00673970..0x00673AE3` | `15b78afa4b396223471ab19091dd0d6e1f9fa16b05ab0819a1cd212fd3794759` |

Pinned image: size 14,759,424, sha256
`9627211412ac60d50ad189ce5a629443ce928ec23a9f8d219dfb2b157028b623`.

Reproduction:

```powershell
py -3 pf_build_pool_46baa0_reader_delta.py --check
```
