/*
 * GameMaster.dll -- compatible re-implementation of the GM plug-in that the
 * game client loads at start-up.
 *
 * The original DLL is not merely missing from our copy of the client: the
 * owner's ruling of 2026-09-01 is that it never existed on our side and cannot
 * be recovered, so it has to be built from scratch.  This file is a clean-room
 * implementation written ONLY against the proven ABI contract in
 *
 *   pf_bridge/notes_to_chief/reference_codex_attr/PF_GM_PLUGIN_GATE.tsv (+ .md)
 *
 * Every structural claim below names the gate_id row that proves it.  Nothing
 * here is derived from the original DLL's code, which nobody has ever seen.
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
 *   With no DLL present the client allocates a 4-byte fallback object whose
 *   vtable slot +0x04 unconditionally returns NULL.  The UI dispatcher treats
 *   NULL-or-empty as "nothing to open" and returns before the factory ever
 *   runs.  That is why the button is visible [GM-IMG-004] but the click is
 *   silent: every gate downstream of this point was already proven correct by
 *   RE-104 / RE-118 / RE-126 / RE-164.  The break is upstream of all of them.
 *
 * WHAT WE MUST RETURN
 *
 *   An object whose vtable carries three slots in exactly this order:
 *
 *     +0x00  [GM-IMG-012]  two stack output pointers, ret 8, returns the first
 *                          pointer in EAX
 *     +0x04  [GM-IMG-006]  no explicit arguments, plain ret, returns a pointer
 *                          to a NUL-terminated UTF-16 string
 *     +0x08  [GM-IMG-014]  one stack destination pointer, ret 4, default-
 *                          constructs an MSVCP90 wstring there, returns the
 *                          same pointer
 *
 *   MSVC x86 gives non-static member functions __thiscall by default: ECX
 *   carries this and the callee cleans the stack arguments.  Declaring the
 *   three methods in this order, in a class with a single vtable and NO
 *   virtual destructor, reproduces the required layout and the required
 *   ret 8 / ret 0 / ret 4 automatically.
 *
 * THE KEY WE RETURN FROM SLOT +0x04
 *
 *   The factory compares our string against the requested key with an exact
 *   UTF-16 comparison [GM-IMG-008]; the GUI resolver then loads
 *   .\Data\GUI\Model\<key>.model [GM-IMG-013].  On disk, GMUI.project declares
 *   the model GMUI_1, and GMUI_1.model is the only file out of 534 models that
 *   contains the GMUI_BASIC tab [GM-DATA-001, GM-DATA-002].  There is no
 *   GMUI_BASIC.model at all.  "GMUI_1" is therefore the only basename that is
 *   consistent with the data actually shipped with the client.
 *
 *   NONCLAIM: that is a reconstructed policy, not a measured original return
 *   value.  Nobody has ever observed what the original DLL returned, and this
 *   file does not claim otherwise.
 *
 * MEMORY RULES -- THE EASIEST WAY TO CRASH THE CLIENT   [GM-IMG-010]
 *
 *   At shutdown the client hands our pointer straight to the MSVCR90
 *   operator delete that it imports, WITHOUT calling a virtual destructor, and
 *   then FreeLibrary's us.  Therefore:
 *
 *     - the object must come from the same CRT heap the client deletes into.
 *       AllocateFromClientCrt below asks the already-loaded msvcr90.dll for its
 *       own operator new, which is the narrow path PF_GM_PLUGIN_GATE.md names
 *       and which holds no matter which CRT this DLL itself links against;
 *     - the object must be heap allocated, never a static or a global;
 *     - the class must NOT declare a virtual destructor.  It would occupy a
 *       vtable slot and shift +0x04 and +0x08, and it would never be called;
 *     - nothing may depend on a destructor running, because none ever does.
 */

#if !defined(_MSC_VER)
#  error "Build with Visual C++ (VC9 / Visual Studio 2008). See build_vs2008.bat."
#endif

#if defined(_WIN64)
#  error "The client is 32-bit. Build x86 (/MACHINE:X86)."
#endif

/*
 * VC9 is required because slot +0x00 and slot +0x08 construct an MSVCP90
 * std::basic_string<wchar_t> inside memory the CLIENT owns.  A newer toolchain
 * lays that type out differently, so a non-VC9 build does not merely warn --
 * it corrupts client memory.
 *
 * PF_GM_ALLOW_NON_VC9 exists for the case where the bridge has no VC9 at all.
 * It does not "turn off the check": it removes every wstring construction from
 * this file, because those are the only reason VC9 is required.  That leaves
 * slot +0x08 violating its stated contract -- acceptable only because
 * GM-IMG-014 measured that none of the five pinned direct call routes reaches
 * slot +0x08.  Treat that build as experimental, and say so in the test report.
 */
#if _MSC_VER != 1500 && !defined(PF_GM_ALLOW_NON_VC9)
#  error "Not VC9 (_MSC_VER 1500). Use VS2008, or read the PF_GM_ALLOW_NON_VC9 note above."
#endif

#if _MSC_VER == 1500 && !defined(PF_GM_ALLOW_NON_VC9)
#  define PF_GM_HAVE_MSVCP90_WSTRING 1
#else
#  define PF_GM_HAVE_MSVCP90_WSTRING 0
#endif

/*
 * Slot +0x00's second effect.
 *
 * GM-IMG-012 states the proven fallback body writes -1 into the first dword of
 * the first output pointer, initialises that output's +4 subobject, ignores the
 * second pointer, and returns the first pointer.  The row's
 * required_interface_fact is "fallback_behavior_reusable", so reproducing the
 * fallback is a sanctioned implementation rather than an invention -- the
 * semantics of these outputs are still UNKNOWN and this file does not guess at
 * them.
 *
 * RESIDUAL UNKNOWN -- READ THIS FIRST IF THE CLIENT CRASHES ON THE GM CLICK.
 * The row says "initialises its +4 subobject" but does not name the type.  Its
 * sibling slot +0x08 default-constructs an MSVCP90 wstring, so a wstring at +4
 * is the reading most consistent with the evidence -- but it is a reading, not
 * a proven fact, and it is the single largest guess in this file.  If the
 * client dies at the click, rebuild with PF_GM_SLOT0_TOUCH_PLUS4=0: that writes
 * only the -1 the row states verbatim and leaves +4 untouched.
 */
#ifndef PF_GM_SLOT0_TOUCH_PLUS4
#  define PF_GM_SLOT0_TOUCH_PLUS4 1
#endif

#include <windows.h>
#include <new>
#if PF_GM_HAVE_MSVCP90_WSTRING
#  include <string>
#endif

namespace {

/*
 * The value slot +0x04 hands to the GUI model resolver [GM-IMG-013].
 *
 * Writable and not const on purpose: PF_GM_PLUGIN_GATE.md's hardened policy
 * points out that IMAGE closes only the immediate reads of this pointer and
 * does not close downstream mutability or retention, so we must not place it in
 * a read-only section.  Static storage is correct here even though the returned
 * OBJECT may not be static: the client only ever reads this buffer, and never
 * frees it.  It outlives every use, because the object is deleted before
 * FreeLibrary [GM-IMG-010].
 */
wchar_t g_modelBasename[] = L"GMUI_1";

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
#if PF_GM_SLOT0_TOUCH_PLUS4 && PF_GM_HAVE_MSVCP90_WSTRING
        void* plus4 = reinterpret_cast<char*>(first) + 4;
        new (plus4) std::wstring();
#endif
    }
    return first;
}

const wchar_t* GameMasterInterface::GetWindowModelBasename() {
    return g_modelBasename;
}

void* GameMasterInterface::MakeEmptyString(void* destination) {
#if PF_GM_HAVE_MSVCP90_WSTRING
    if (destination != NULL) {
        new (destination) std::wstring();
    }
#endif
    return destination;
}

/*
 * Allocate out of the CRT the client will free us with.
 *
 * GM-IMG-010 proves the client calls the MSVCR90 operator delete it imports,
 * directly on our pointer.  Mixing heaps there is an immediate crash at
 * shutdown, so we ask the already-loaded msvcr90.dll for its own operator new
 * (mangled ??2@YAPAXI@Z, the symbol PF_GM_PLUGIN_GATE.md names).
 *
 * GetModuleHandleW rather than LoadLibraryW on purpose: the client has already
 * loaded this CRT, and we neither want a second copy nor an extra reference
 * that would outlive our own unload.
 */
void* AllocateFromClientCrt(size_t size) {
    typedef void* (__cdecl *operator_new_t)(size_t);

    HMODULE crt = GetModuleHandleW(L"msvcr90.dll");
    if (crt == NULL) {
        return NULL;
    }

    operator_new_t crt_new =
        reinterpret_cast<operator_new_t>(GetProcAddress(crt, "??2@YAPAXI@Z"));
    if (crt_new == NULL) {
        return NULL;
    }

    return crt_new(size);
}

}  /* namespace */

/*
 * The export the client resolves by exact undecorated name [GM-IMG-001].
 * GameMaster.def forces the name to "CreateGameMaster" with no leading
 * underscore and no @0 suffix.  With zero arguments there is no stack to clean,
 * so __cdecl cannot disagree with the call site about anything.
 */
extern "C" void* __cdecl CreateGameMaster(void) {
    try {
        void* raw = AllocateFromClientCrt(sizeof(GameMasterInterface));
        if (raw != NULL) {
            return new (raw) GameMasterInterface();
        }

        /*
         * msvcr90 was not resolvable.  Plain new is only heap-compatible with
         * the client when this DLL is itself a /MD VC9 build; that is what
         * build_vs2008.bat produces, so this path stays correct there and is a
         * genuine last resort anywhere else.
         */
        return new GameMasterInterface();
    } catch (...) {
        /*
         * Never let an exception cross back into the client.
         *
         * Returning NULL is a well-defined degradation rather than a new
         * failure mode: GM-IMG-002 enumerates "the returned object is absent"
         * alongside a missing library or export, and in all three cases the
         * loader installs its own 4-byte fallback.  So a NULL here reproduces
         * exactly today's behaviour -- button visible, click inert -- instead
         * of taking the button away.
         */
        return NULL;
    }
}

BOOL APIENTRY DllMain(HMODULE module, DWORD reason, LPVOID reserved) {
    (void)reserved;

    if (reason == DLL_PROCESS_ATTACH) {
        /* No work in DllMain beyond this; loader-lock rules apply. */
        DisableThreadLibraryCalls(module);
    }
    return TRUE;
}
