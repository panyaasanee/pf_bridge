# TO LANE-GM: `build_vs2008.bat` produces a DLL Windows will not load. One step is missing.

- who: ka1-A (attended), from the GT-207 round R304
- when: 2026-09-02 ~19:20 (+07:00), approximate
- machine: the owner's, VC9 freshly installed today

## The measurement

`build_vs2008.bat`, run exactly as the ticket's cell 1 (no `EXTRA_DEFS`), on a real
VS2008 install, produced:

- `GameMaster.dll`, 13,824 bytes, all three of your own checks `[ok]`
- imports `MSVCR90.dll` (as intended, `/MD`)
- **no `.rsrc` section, no embedded RT_MANIFEST**
- a separate `GameMaster.dll.manifest`, 616 bytes, written by the linker beside it

`plugin_image_check` calls exactly this combination fatal, and it is right:
side-by-side CRT binding with no manifest, the loader answers `LoadLibraryW` with
14001 and nothing in the plug-in ever runs. Your own README and the ticket both predict
it (`build_vs2008.bat` does not call `mt.exe`, `install.bat` copies only the `.dll`).

So as it stands today, **every build this script makes is unloadable**, and the ticket's
own STOP would end every attended round before the game is even started.

## The part your note could not know

**`mt.exe` is on this machine.** Not in `VC\bin`, and not under `Program Files (x86)`:

```
C:\Program Files\Microsoft SDKs\Windows\v6.0A\bin\mt.exe
Microsoft (R) Manifest Tool version 5.2.3790.2075
```

One command turned the same DLL into a loadable one:

```
mt.exe -manifest GameMaster.dll.manifest -outputresource:GameMaster.dll;#2
```

- exit 0, no warnings
- 13,824 -> 14,848 bytes; sha256 `67501F7E...F496` -> `4A0ECB58...D743B`
- `plugin_image_check` then: `embedded_manifest=yes`, `verdict=image_ok`, exit 0
- the embedded manifest is the linker's own, declaring
  `Microsoft.VC90.CRT 9.0.21022.8 x86 publicKeyToken=1fc8b3b9a1e18e3b`
- and the plug-in then **loaded and ran**: `[GM_PLUGIN] loaded`, `client CRT: ...`,
  `msvcp90 wstring ctor: resolved ...`, `alive, returning interface`, and the GM window
  opened. Full evidence in my GT-207 result letter filed 1915 today.

## What I am asking for

Add the `mt.exe` step to `build_vs2008.bat`, in your own file, in your own words. I did
**not** edit anything in `patches/gm_plugin/` - the embed above ran as a separate command
in my own bridge job, with the owner's explicit approval, precisely because that folder
is your write area.

Two details worth building in, since neither is obvious:

1. `mt.exe` is **not** on the VC9 path. `vcvars32.bat` does not add
   `...\Microsoft SDKs\Windows\v6.0A\bin`, so the script has to locate it. Searching
   `Program Files (x86)` alone finds nothing - the SDK sits under `Program Files` here.
2. If `mt.exe` really is absent on some machine, failing loudly at build time is far
   better than shipping a DLL that dies at `LoadLibraryW` with no message at all.

## NONCLAIMS

- I did NOT test whether a `/MT` build would sidestep the manifest question. It probably
  would, but the plug-in's whole design rests on sharing the client's CRT, so I did not
  treat it as an option.
- I did NOT verify `mt.exe` exists on any machine but this one.
- The manifest I embedded is the one **your** link step generated. I did not write,
  edit, or hand-craft a manifest.
- One build, one machine, one round.
