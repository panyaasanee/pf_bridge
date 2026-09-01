/*
 * GameMaster.dll -- compatible re-implementation of the GM plug-in the client
 * loads at start-up.
 *
 * Owner ruling, live in session 2026-09-01: the original plug-in never existed
 * on our side and cannot be recovered, so it has to be rebuilt.
 * [UNPINNED -- spoken ruling, no repository artifact records it.  The lane's
 * own most recent pinned note (notes_to_chief/20260901_2132_RE-164-RESULT-...)
 * says only that a bridge inventory did not find the file, and explicitly
 * nonclaims that it is truly absent.  Nothing in this file depends on the
 * distinction, and the installer refuses to overwrite an existing file.]
 *
 * Written ONLY against the proven ABI contract in
 *   pf_bridge/notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv (+ .md)
 * Every structural claim names the gate_id row that proves it.  Nothing here
 * comes from the original DLL's code, which nobody has ever seen.
 *
 * REVISION 2 -- rewritten after a pf-adversary pass rejected revision 1.
 * What changed and why (each was a real defect, not a style note):
 *   - r1 inlined a std::wstring constructor from this compiler's headers.  The
 *     TSV's own span lengths refute that: GM-IMG-014's whole body is 29 bytes
 *     and GM-IMG-012's is 35, against a 3-byte control (GM-IMG-003 =
 *     xor eax,eax; ret).  Neither fits an inlined _SECURE_SCL=1 string ctor,
 *     which alone needs a proxy allocation, _Tidy and a _Myproxy store.  And
 *     GM-IMG-014 says so in words: "default-constructs that destination
 *     through the pinned MSVCP90 import".  We now CALL THAT EXPORT.  This is
 *     layout-exact by construction, so the build no longer depends on VC9 or
 *     on _SECURE_SCL, which r1 rode as an undocumented default.
 *   - r1 picked the CRT with GetModuleHandleW(L"msvcr90.dll").  MSVCR90 is a
 *     side-by-side assembly and two instances can be mapped at once, each with
 *     its own heap; the name lookup returns whichever the loader lists first.
 *     We now walk the client's own import table to the module that actually
 *     backs the operator delete it will free us with.
 *   - r1 emitted no evidence it had ever run, so four different failures all
 *     produced the same silent symptom as the six-day-old bug.  It now
 *     announces itself, and what it resolved, through OutputDebugStringW.
 *   - r1 fell back to plain new when CRT lookup failed.  That path is dead
 *     where it is safe and a guaranteed cross-heap free everywhere else, so it
 *     is gone; failure returns NULL, which is a well-defined degradation.
 *
 * ---------------------------------------------------------------------------
 * WHAT THE CLIENT DOES WITH US   [GM-IMG-001]
 *
 *   LoadLibraryW(L"GameMaster.dll")
 *     -> GetProcAddress(h, "CreateGameMaster")   exact ASCII, undecorated
 *     -> call that export with zero explicit arguments
 *     -> store the returned pointer at application+0x7C8
 *
 * WHY THE GM WINDOW DOES NOT OPEN TODAY   [GM-IMG-002, -003, -007]
 *
 *   With no plug-in the client allocates a 4-byte fallback whose vtable slot
 *   +0x04 returns NULL.  The dispatcher treats NULL-or-empty as "nothing to
 *   open" and returns before the factory runs, so the button is visible
 *   [GM-IMG-004] and the click is silent.
 *
 *   NONCLAIM: PF_GM_PLUGIN_GATE.md:14 puts this no higher than "consistent
 *   with" -- the inventory it rests on is flagged there as possibly stale, and
 *   GM-IMG-005 gives an independent producer of the same silence (the
 *   GMModule_Client+0x19 click gate, which GT-164 probed with 14 variants).
 *   This file does not claim to have found THE cause, only to remove one.
 *
 * THE THREE SLOTS WE MUST PROVIDE
 *
 *   +0x00  [GM-IMG-012]  two stack output pointers, ret 8, returns the first
 *   +0x04  [GM-IMG-006]  no explicit arguments, plain ret, returns a pointer
 *                        to a NUL-terminated UTF-16 string
 *   +0x08  [GM-IMG-014]  one stack destination pointer, ret 4, default-
 *                        constructs an MSVCP90 wstring there, returns it
 *
 *   [PROPOSED -- toolchain fact, no evidence layer, verify with dumpbin]
 *   MSVC x86 lays a single-inheritance class's virtuals out in declaration
 *   order; the /GR object locator sits at vftable[-4], a negative offset, so
 *   it does not shift slot 0.  Non-static member functions are __thiscall by
 *   default (this in ECX, callee cleans), giving ret 8 / ret / ret 4 for 2 / 0
 *   / 1 stack arguments.  build_vs2008.bat disassembles the built DLL and
 *   checks those three epilogues, because nothing else here can.
 *
 * WHAT SLOT +0x04 RETURNS, AND WHY THAT IS STILL THE OPEN QUESTION
 *
 *   GM-IMG-013: the resolver builds .\Data\GUI\Model\<key>.model from it.
 *   GM-DATA-001/002: GMUI.project declares model GMUI_1, and GMUI_1.model is
 *   the only one of 534 models carrying the GMUI_BASIC tab; no GMUI_BASIC.model
 *   exists.  So GMUI_1 is the basename consistent with the shipped data.
 *
 *   But note what does NOT test it.  GM-IMG-006 passes our return to the
 *   dispatcher as the requested key, and GM-IMG-008 has the factory re-read
 *   our getter and compare it against that same requested key -- both sides
 *   come from us, so that comparison is satisfied by any non-empty string and
 *   proves nothing about the value.  The gate that actually decides is the
 *   dispatcher lookup in between (GM-IMG-007), and GM-IMG-008's own blocker is
 *   REQUEST_TO_FACTORY_RUNTIME_BINDING_NOT_OBSERVED.  A wrong key therefore
 *   produces silence at the click, indistinguishable from not loading at all
 *   -- which is why PF_GM_KEY is a build parameter and why the README asks for
 *   an A/B against GMUI_BASIC rather than treating GMUI_1 as settled.
 *
 * MEMORY RULES -- THE EASIEST WAY TO CRASH THE CLIENT   [GM-IMG-010]
 *
 *   At shutdown the client hands our pointer straight to the MSVCR90 operator
 *   delete it imports, with NO virtual destructor call, then FreeLibrary's us.
 *   Therefore: allocate from that exact CRT instance (see FindClientCrt), never
 *   return a static or global, declare no virtual destructor -- it would take a
 *   vtable slot and shift +0x04/+0x08, and would never be called -- and let
 *   nothing depend on a destructor running.
 */

#if defined(_WIN64)
#  error "The client is 32-bit. Build x86 (/MACHINE:X86)."
#endif

/*
 * The key slot +0x04 returns.  Overridable so the A/B the README describes
 * needs a rebuild, not a source edit:  set EXTRA_DEFS=/D PF_GM_KEY=L\"GMUI_BASIC\"
 */
#ifndef PF_GM_KEY
#  define PF_GM_KEY L"GMUI_1"
#endif

/*
 * Slot +0x00's second effect.
 *
 * GM-IMG-012 says the proven fallback writes -1 into the first dword of the
 * first output, initialises that output's +4 subobject, ignores the second
 * pointer, and returns the first.  Its required_interface_fact is
 * "fallback_behavior_reusable", so reproducing it is sanctioned rather than
 * invented -- the MEANING of these outputs is still UNKNOWN
 * (semantic_status: PROVEN_EXACT_ABI_UNKNOWN_SEMANTIC) and is not guessed here.
 *
 * The row does not name the +4 type.  Two things point at a wstring: the
 * sibling slot +0x08 default-constructs one, and the 35-byte body length fits
 * prologue + the -1 store + one import call + epilogue and little else.  That
 * is corroboration, not proof.  If the client dies at the click, rebuild with
 *   set EXTRA_DEFS=/D PF_GM_SLOT0_TOUCH_PLUS4=0
 * which writes only the -1 the row states verbatim, and COMPARE THE PRINTED
 * SHA256 to be sure you really got a different DLL.
 */
#ifndef PF_GM_SLOT0_TOUCH_PLUS4
#  define PF_GM_SLOT0_TOUCH_PLUS4 1
#endif

#include <windows.h>
#include <new>          /* placement new -- the only header dependency, and it
                         * carries no layout: we construct nothing from our own
                         * headers into client memory.  See revision 2 above. */

/* Widen __DATE__/__TIME__ without depending on a CRT-internal macro. */
#define PF_GM_WIDE2(x) L ## x
#define PF_GM_WIDE(x)  PF_GM_WIDE2(x)

namespace {

/*
 * MSVCP90's std::basic_string<wchar_t> default constructor, __thiscall, no
 * arguments.  Resolved at load time; never inlined from our own headers, so
 * our compiler's idea of the layout is irrelevant.
 */
typedef void* (__thiscall *wstring_ctor_t)(void* self);

wstring_ctor_t g_wstringCtor = NULL;
HMODULE        g_clientCrt   = NULL;

/* [GM-IMG-013] the value slot +0x04 hands to the GUI model resolver.
 *
 * Writable with headroom rather than a tight literal: GM-IMG-017's blocker is
 * DOWNSTREAM_RETENTION_AND_ORIGINAL_OWNERSHIP_UNPROVEN, so a consumer that
 * transforms the key in place is not excluded.  A tight 7-wchar buffer would
 * let such a write run into whatever follows in .data and corrupt the key for
 * the next click; the slack absorbs it instead.  The module is pinned in
 * DllMain so this storage outlives any pointer a consumer retained. */
wchar_t g_modelBasename[64] = PF_GM_KEY;

void Announce(const wchar_t* text) {
    OutputDebugStringW(L"[GM_PLUGIN] ");
    OutputDebugStringW(text);
    OutputDebugStringW(L"\n");
}

/*
 * Find the CRT instance that will actually free us.
 *
 * GetModuleHandleW(L"msvcr90.dll") is not good enough: MSVCR90 ships as a
 * side-by-side assembly, an app-local copy and a WinSxS copy can both be
 * mapped, they share a base name, and each has its own _crtheap.  Allocating
 * from one and being freed by the other is a shutdown crash whose only
 * symptom is a crash on exit -- and dumpbin /dependents reports success for it.
 *
 * So we walk the main module's import table for the thunk bound to
 * ??3@YAXPAX@Z (operator delete(void*)) -- the very function GM-IMG-010 proves
 * the client calls on us -- and resolve the module from that bound address.
 * The result is the right instance by construction rather than by name.
 */
HMODULE FindClientCrt() {
    BYTE* base = reinterpret_cast<BYTE*>(GetModuleHandleW(NULL));
    if (base == NULL) {
        return NULL;
    }

    IMAGE_DOS_HEADER* dos = reinterpret_cast<IMAGE_DOS_HEADER*>(base);
    if (dos->e_magic != IMAGE_DOS_SIGNATURE) {
        return NULL;
    }

    IMAGE_NT_HEADERS* nt =
        reinterpret_cast<IMAGE_NT_HEADERS*>(base + dos->e_lfanew);
    if (nt->Signature != IMAGE_NT_SIGNATURE) {
        return NULL;
    }

    IMAGE_DATA_DIRECTORY* dir =
        &nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT];
    if (dir->VirtualAddress == 0 || dir->Size == 0) {
        return NULL;
    }

    IMAGE_IMPORT_DESCRIPTOR* imp =
        reinterpret_cast<IMAGE_IMPORT_DESCRIPTOR*>(base + dir->VirtualAddress);

    for (; imp->Name != 0; ++imp) {
        /*
         * Never fall back to FirstThunk for the NAME table.  After the loader
         * has run, FirstThunk holds resolved absolute addresses, not RVAs to
         * IMAGE_IMPORT_BY_NAME -- reading it as the name table computes
         * base + <absolute VA>, a wild pointer, and the lstrcmpA below would
         * fault inside DllMain under the loader lock: a hard crash at client
         * start-up.  A descriptor with no INT simply cannot be searched by
         * name, so skip it.  (A normally linked VC9 executable gives every
         * descriptor an INT; this is the branch, not the expected path.)
         */
        if (imp->OriginalFirstThunk == 0 || imp->FirstThunk == 0) {
            continue;
        }

        IMAGE_THUNK_DATA* names =
            reinterpret_cast<IMAGE_THUNK_DATA*>(base + imp->OriginalFirstThunk);
        IMAGE_THUNK_DATA* bound =
            reinterpret_cast<IMAGE_THUNK_DATA*>(base + imp->FirstThunk);

        for (; names->u1.AddressOfData != 0; ++names, ++bound) {
            if (IMAGE_SNAP_BY_ORDINAL(names->u1.Ordinal)) {
                continue;
            }

            IMAGE_IMPORT_BY_NAME* byName =
                reinterpret_cast<IMAGE_IMPORT_BY_NAME*>(
                    base + names->u1.AddressOfData);

            if (lstrcmpA(reinterpret_cast<const char*>(byName->Name),
                         "??3@YAXPAX@Z") != 0) {
                continue;
            }

            HMODULE owner = NULL;
            if (GetModuleHandleExW(
                    GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                        GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                    reinterpret_cast<LPCWSTR>(bound->u1.Function),
                    &owner)) {
                return owner;
            }
            return NULL;
        }
    }
    return NULL;
}

void* AllocateFromClientCrt(size_t size) {
    typedef void* (__cdecl *operator_new_t)(size_t);

    if (g_clientCrt == NULL) {
        return NULL;
    }

    operator_new_t crtNew = reinterpret_cast<operator_new_t>(
        GetProcAddress(g_clientCrt, "??2@YAPAXI@Z"));
    if (crtNew == NULL) {
        return NULL;
    }
    return crtNew(size);
}

class GameMasterInterface {
public:
    /* vtable +0x00 [GM-IMG-012] -- two output pointers, ret 8 */
    virtual void* QueryStateOutputs(void* first, void* second);

    /* vtable +0x04 [GM-IMG-006] -- no arguments, plain ret */
    virtual const wchar_t* GetWindowModelBasename();

    /* vtable +0x08 [GM-IMG-014] -- one destination pointer, ret 4 */
    virtual void* MakeEmptyString(void* destination);
};

void* GameMasterInterface::QueryStateOutputs(void* first, void* second) {
    /* [GM-IMG-012] the fallback body does not use the second pointer. */
    (void)second;

    if (first != NULL) {
        *reinterpret_cast<LONG*>(first) = -1;
#if PF_GM_SLOT0_TOUCH_PLUS4
        if (g_wstringCtor != NULL) {
            /* Exceptions must never cross back into a client frame compiled
             * for ret 8 with no unwind data. */
            try {
                g_wstringCtor(reinterpret_cast<char*>(first) + 4);
            } catch (...) {
            }
        }
#endif
    }
    return first;
}

const wchar_t* GameMasterInterface::GetWindowModelBasename() {
    return g_modelBasename;
}

void* GameMasterInterface::MakeEmptyString(void* destination) {
    if (destination != NULL && g_wstringCtor != NULL) {
        try {
            g_wstringCtor(destination);
        } catch (...) {
        }
    }
    return destination;
}

}  /* namespace */

/*
 * The export the client resolves by exact undecorated name [GM-IMG-001].
 * GameMaster.def forces the published name; with zero arguments __cdecl and
 * __stdcall are indistinguishable to the caller, so no convention mismatch is
 * possible here.
 */
extern "C" void* __cdecl CreateGameMaster(void) {
    try {
        /*
         * Refuse rather than hand back a half-built object.
         *
         * Without the MSVCP90 constructor, slot +0x00 would write its -1 and
         * leave the +4 subobject UNINITIALISED -- diverging from the proven
         * fallback, which initialises it [GM-IMG-012] -- and slot +0x08 would
         * return a buffer it never constructed while telling the caller a
         * wstring lives there.  Whoever read or destroyed those would be
         * working on garbage.  That is a NEW failure, strictly worse than the
         * dead button we already have, so we decline the job instead and say
         * why.  DllMain has already printed which lookup failed.
         */
        if (g_wstringCtor == NULL) {
            Announce(L"FAIL: msvcp90 wstring ctor unresolved; returning NULL "
                     L"rather than a half-constructed object");
            return NULL;
        }

        void* raw = AllocateFromClientCrt(sizeof(GameMasterInterface));
        if (raw == NULL) {
            /*
             * No safe heap, so do not invent one.  Plain new here would be
             * freed by the client's CRT at shutdown from a heap that never
             * owned it.  NULL is a well-defined degradation instead:
             * GM-IMG-002 lists "the returned object is absent" beside a missing
             * library or export, and in all three cases the loader installs its
             * own 4-byte fallback -- exactly today's behaviour, button visible
             * and click inert, rather than a new failure.
             */
            Announce(L"FAIL alloc: client CRT operator new unavailable; "
                     L"returning NULL (client keeps its own fallback)");
            return NULL;
        }

        Announce(L"alive, returning interface");
        return new (raw) GameMasterInterface();
    } catch (...) {
        Announce(L"FAIL exception in CreateGameMaster; returning NULL");
        return NULL;
    }
}

BOOL APIENTRY DllMain(HMODULE module, DWORD reason, LPVOID reserved) {
    (void)reserved;

    if (reason != DLL_PROCESS_ATTACH) {
        return TRUE;
    }

    DisableThreadLibraryCalls(module);

    /*
     * Pin ourselves.  GM-IMG-017's blocker leaves downstream retention of the
     * slot +0x04 string unproven, and GM-IMG-010 has the client FreeLibrary us
     * at shutdown.  If a panel kept the raw pointer, unmapping this module
     * would fault while reading it -- a crash on exit whose README triage would
     * send the tester to the CRT, which would look fine.  Pinning removes the
     * whole class for the cost of not unloading.
     */
    HMODULE self = NULL;
    GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                           GET_MODULE_HANDLE_EX_FLAG_PIN,
                       reinterpret_cast<LPCWSTR>(&g_modelBasename),
                       &self);

    g_clientCrt = FindClientCrt();

    HMODULE cpp = GetModuleHandleW(L"msvcp90.dll");
    if (cpp != NULL) {
        /*
         * std::basic_string<wchar_t,char_traits<wchar_t>,allocator<wchar_t> >
         * ::basic_string(void), public __thiscall.
         * [PROPOSED] name not verified against this machine's msvcp90.dll.  If
         * it is wrong we resolve NULL, skip both constructions, and say so
         * below -- we never fall back to an inlined constructor, because the
         * whole point of calling the export is that our own layout may differ.
         */
        g_wstringCtor = reinterpret_cast<wstring_ctor_t>(GetProcAddress(
            cpp,
            "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ"));
    }

    Announce(L"loaded  build=" PF_GM_WIDE(__DATE__) L" " PF_GM_WIDE(__TIME__));
    Announce(g_clientCrt   ? L"client CRT: located via import table"
                           : L"client CRT: NOT FOUND -- CreateGameMaster will return NULL");
    Announce(g_wstringCtor ? L"msvcp90 wstring ctor: resolved"
                           : L"msvcp90 wstring ctor: NOT RESOLVED -- slots +0x00/+0x08 will skip construction");
    Announce(L"key=" PF_GM_KEY);

    return TRUE;
}
