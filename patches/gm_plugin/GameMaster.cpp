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
 * 🔴 COMPILE-UNVERIFIED on cloud -- this file has never been compiled by MSVC
 * and cannot be, here: the cloud clone has no Windows SDK and no VC9.  THE
 * FIRST VC9 BUILD MUST RUN plugin_image_check ON THE BUILT DLL BEFORE INSTALL:
 *     set PYTHONPATH=src
 *     py -3 -m pirateforce_foundation.gm.plugin_image_check \
 *            --dll <build>\GameMaster.dll --client-dir "<client folder>"
 * (pirate-force-server, landed 2026-09-02.  It names which of eleven file-level
 * failures you have, all of them at once, instead of one per boot.)
 *
 * REVISION 4 -- revision 3 was reviewed by pf-adversary in the same round and
 * NEVER LEFT THE WORKING TREE.  Two of its findings were CRITICAL and both
 * were revision 3's own doing:
 *   - the CRT lookup passed dllName = NULL, so the first descriptor importing
 *     ??3@YAXPAX@Z won -- and MFC90, a proxy CRT, or an injected anti-cheat
 *     module import that name too.  Measured on a synthetic import table: it
 *     returned MFC90.  That is the cross-heap free of GM-IMG-010 with a green
 *     "located" line printed over it.  Both lookups now filter on the
 *     descriptor's DLL name as well as the symbol.
 *   - H1 was not actually achieved: the wstring ctor's decorated name is
 *     byte-identical in MSVCP80/90/100, so a symbol-only match could bind
 *     MSVCP80 while announcing "exact instance".
 * Also from that pass: resolution moved out of DllMain entirely (GetProcAddress
 * on a forwarded export re-enters the loader, which is forbidden under the
 * loader lock, and its symptom -- client does not start -- is indistinguishable
 * on screen from "never loaded"); `loaded` is now the first thing DllMain
 * prints; Announce emits one OutputDebugStringW per line (three calls could be
 * split across DebugView rows, and the token is what the whole test order
 * greps for); the self-pin result is checked and reported; slot +0x08 returns
 * the destination rather than NULL (see the comment there); the descriptor-name
 * search verifies the candidate really exports what we need; and an
 * unattributable binding no longer abandons the rest of the table.
 *
 * REVISION 3 -- two HIGH findings from this lane's own pf-adversary pass,
 * ordered fixed by COO-DECISION 20260902_0648 (which also moved this folder
 * into LANE-GM's write zone).  Both were self-inflicted by revision 2:
 *   - H1: DllMain resolved MSVCP90 with GetModuleHandleW(L"msvcp90.dll") --
 *     the exact base-name lookup revision 2 removed for MSVCR90 four lines
 *     earlier, reintroduced for the OTHER side-by-side assembly.  Worse there
 *     than for the CRT: an empty _SECURE_SCL=1 basic_string still takes a
 *     _Container_proxy from its allocator, so a proxy allocated through
 *     instance A and released through the client's pinned instance B is a
 *     cross-heap free.  The import walk is now generic and used for both.
 *   - H2: PF_GM_SLOT0_TOUCH_PLUS4 defaulted to 1, i.e. the default build
 *     constructed an object of a size we are still GUESSING (28 bytes with
 *     _SECURE_SCL=1) over first+4..first+31 inside client memory.  GM-IMG-012
 *     does not name the +4 type.  The default now writes only the -1 that row
 *     states verbatim; touching +4 is the third A/B cell, opt-in.
 *   - and the refusal in CreateGameMaster is now tied to the macro that
 *     actually needs the constructor, not to the constructor itself; see the
 *     comment there for why slot +0x08 is not a reason to refuse the job.
 *
 * REVISION 2 -- rewritten after a pf-adversary pass rejected revision 1.
 * What changed and why (each was a real defect, not a style note):
 *   - r1 inlined a std::wstring constructor from this compiler's headers.  The
 *     TSV's own span lengths refute that: GM-IMG-014's whole body is 29 bytes
 *     and GM-IMG-012's is 35, against a 3-byte control (GM-IMG-003 =
 *     xor eax,eax; ret).  Neither fits an inlined _SECURE_SCL=1 string ctor,
 *     which alone needs a proxy allocation, _Tidy and a _Myproxy store.  And
 *     GM-IMG-014 says so in words: "default-constructs that destination
 *     through the pinned MSVCP90 import".  We therefore call an MSVCP90
 *     export instead of inlining one.  [PROPOSED] the row names no symbol --
 *     it pins a 29-byte span and a vtable cell -- so WHICH export is our
 *     reading of that sentence, not the row's content.  Given that reading it
 *     is layout-exact by construction, so the build no longer depends on VC9 or
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
 *   Therefore: allocate from that exact CRT instance (see FindClientImport), never
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
 * The row does not name the +4 type -- not its size, not its class.  Two
 * things point at a wstring: the sibling slot +0x08 default-constructs one,
 * and the 35-byte body length fits prologue + the -1 store + one import call +
 * epilogue and little else.  That is corroboration, not proof.
 *
 * 🔴 Be exact about what the default costs, because the row cuts both ways:
 * GM-IMG-012 states in ONE clause that the proven fallback "writes -1 to its
 * first dword, INITIALIZES ITS +4 SUBOBJECT, and does not use the second
 * pointer", and slot +0x00 is a slot with a PINNED call route (GM-IMG-011
 * call_counts=1,4; GM-IMG-015 mechanical_slot_+0x00_calls=1).  So the default
 * build is a DELIBERATE DIVERGENCE from the proven fallback on a reachable
 * slot: it writes the -1 and leaves +4 exactly as the caller left it.  Do not
 * describe it as "only what the row states" -- the row states the +4 init just
 * as plainly.  It is a choice between two ways of being wrong, ordered by
 * COO-DECISION 20260902_0648 and taken with eyes open:
 *   =0 leaves a subobject uninitialised that the caller may destroy;
 *   =1 writes 24 or 28 bytes of OUR guess over a subobject whose size and
 *      type nobody has measured, possibly past its end, possibly over a
 *      caller's stack frame.
 * =0 is the smaller blast radius (it writes nothing we cannot cite), not the
 * faithful reproduction.  If the client dies at the click in cell 1 or 2, this
 * is the first suspect, not "a different cause entirely".
 *
 * So the DEFAULT IS 0 (revision 3, H2).  Constructing a wstring at first+4
 * writes 24 or 28 bytes -- the size depends on _SECURE_SCL, which is exactly
 * the kind of thing we do not know about the client's build -- into memory
 * whose extent we have never measured.  If the real subobject is smaller, or
 * if `first` is a caller stack temporary, that is an overwrite in client
 * memory (return address included) produced by our own guess, at the click.
 * A default of 1 spent the first attended round on the riskiest cell.
 *
 * The default therefore writes only what GM-IMG-012 states verbatim.  Turning
 * the +4 initialisation on is the THIRD cell of the A/B in README.md:
 *   set EXTRA_DEFS=/D PF_GM_SLOT0_TOUCH_PLUS4=1
 * and COMPARE THE PRINTED SHA256 to be sure you really got a different DLL.
 */
#ifndef PF_GM_SLOT0_TOUCH_PLUS4
#  define PF_GM_SLOT0_TOUCH_PLUS4 0
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

typedef void* (__cdecl *operator_new_t)(size_t);

wstring_ctor_t g_wstringCtor = NULL;
HMODULE        g_clientCrt   = NULL;
operator_new_t g_clientNew   = NULL;
bool           g_resolved    = false;

/*
 * Names we look for in the CLIENT's import table.  All three are decorated
 * exactly as MSVC emits them; llvm-undname round-trips all three (README,
 * "why revision 2 stopped depending on VS2008").
 */
const char kOperatorDelete[] = "??3@YAXPAX@Z";
const char kOperatorNew[]    = "??2@YAPAXI@Z";
const char kWstringCtor[]    =
    "??0?$basic_string@_WU?$char_traits@_W@std@@V?$allocator@_W@2@@std@@QAE@XZ";
const char kMsvcp90[]        = "msvcp90.dll";
const char kMsvcr90[]        = "msvcr90.dll";

/* [GM-IMG-013] the value slot +0x04 hands to the GUI model resolver.
 *
 * Writable with headroom rather than a tight literal: GM-IMG-017's blocker is
 * DOWNSTREAM_RETENTION_AND_ORIGINAL_OWNERSHIP_UNPROVEN, so a consumer that
 * transforms the key in place is not excluded.  A tight 7-wchar buffer would
 * let such a write run into whatever follows in .data and corrupt the key for
 * the next click; the slack absorbs it instead.  The module is pinned in
 * DllMain so this storage outlives any pointer a consumer retained. */
wchar_t g_modelBasename[64] = PF_GM_KEY;

/*
 * One OutputDebugStringW call per line, assembled here.
 *
 * Revision 3 emitted the prefix, the text and the newline as three separate
 * calls.  DebugView renders one row per call and DLL_PROCESS_ATTACH runs with
 * the client's other threads live, so the token `[GM_PLUGIN] loaded` -- the
 * single indicator the whole three-cell test order hangs on -- could be split
 * across rows or interleaved with another emitter, and a literal search for it
 * would find nothing.  No CRT is used here: this file must not depend on a
 * string function from a heap we do not own.
 */
void Announce(const wchar_t* text) {
    wchar_t line[640];
    const wchar_t prefix[] = L"[GM_PLUGIN] ";
    int i = 0;
    for (int p = 0; prefix[p] != L'\0' && i < 637; ++p) {
        line[i++] = prefix[p];
    }
    for (int t = 0; text[t] != L'\0' && i < 637; ++t) {
        line[i++] = text[t];
    }
    line[i++] = L'\n';
    line[i] = L'\0';
    OutputDebugStringW(line);
}

/* Set by FindClientImport when the client's PE headers themselves do not
 * parse, so a structural failure is never reported as "the symbol is not
 * imported" (revision 3 collapsed thirteen give-up paths into one message). */
const wchar_t* g_walkFailure = NULL;

/*
 * The one lookup primitive in this file: walk the CLIENT's own import table and
 * report the module (and, when matched by symbol, the bound address) that the
 * client itself is wired to.
 *
 * Why this and never GetModuleHandleW(base name).  MSVCR90 and MSVCP90 both
 * ship as side-by-side assemblies: an app-local copy under Microsoft.VC90.CRT
 * and a WinSxS copy can be mapped at the same time, they share a base name,
 * and each carries its own heap.  A base-name handle is whichever the loader
 * lists first, which is a coin toss we would lose only at shutdown, with
 * dumpbin /dependents reporting success the whole time.
 *   - For the CRT this decides who owns our object: GM-IMG-010 proves the
 *     client frees us through its own imported operator delete.
 *   - For MSVCP90 it decides who owns the _Container_proxy an empty
 *     _SECURE_SCL=1 basic_string takes from its allocator (revision 3, H1).
 * Anchoring on a thunk the client has already bound gives the right instance
 * by construction instead of by name.
 *
 * dllName  NULL = any module; otherwise the import descriptor's DLL name,
 *          compared case-insensitively.  🔴 NEVER pass NULL when the answer
 *          decides who owns memory.  The mangled names we look for are NOT
 *          unique to one library: ??3@YAXPAX@Z is imported by MFC90 and by
 *          any injected/anti-cheat module, and the wstring ctor's decorated
 *          name is byte-identical across MSVCP80/90/100.  Matching the first
 *          descriptor that happens to import the name would hand back the
 *          wrong module and reinstate exactly the cross-heap free this file
 *          exists to prevent -- with a green "located" line over it.
 * symbol   NULL = match the descriptor itself (first bound thunk, ordinal
 *          imports included, so a stripped INT is still usable); otherwise the
 *          exact imported-by-name symbol, and out->bound is that binding.
 * requireExport  descriptor mode only (symbol == NULL): accept a candidate
 *          module only if it exports this name, and return that address in
 *          out->bound.  Without it the first bound thunk decides, and one
 *          forwarded or hooked IAT slot at the head of the descriptor points
 *          at a different module entirely.
 *
 * NOT called from DllMain any more (see ResolveOnce): GetProcAddress on a
 * forwarded export can re-enter the loader, which is forbidden while holding
 * the loader lock.  Every loop is still bounded and nothing is dereferenced
 * that the table did not describe as a name.
 */
enum {
    kMaxDescriptors = 1024,        /* a VC9 exe imports tens, not thousands */
    kMaxThunksPerDescriptor = 16384
};

struct ClientImport {
    HMODULE module;
    FARPROC bound;
};

bool FindClientImport(const char* dllName,
                      const char* symbol,
                      const char* requireExport,
                      ClientImport* out) {
    out->module = NULL;
    out->bound  = NULL;
    BYTE* base = reinterpret_cast<BYTE*>(GetModuleHandleW(NULL));
    if (base == NULL) {
        g_walkFailure = L"client image: GetModuleHandleW(NULL) returned NULL";
        return false;
    }

    IMAGE_DOS_HEADER* dos = reinterpret_cast<IMAGE_DOS_HEADER*>(base);
    if (dos->e_magic != IMAGE_DOS_SIGNATURE) {
        g_walkFailure = L"client image: no MZ header";
        return false;
    }

    IMAGE_NT_HEADERS* nt =
        reinterpret_cast<IMAGE_NT_HEADERS*>(base + dos->e_lfanew);
    if (nt->Signature != IMAGE_NT_SIGNATURE) {
        g_walkFailure = L"client image: no PE header";
        return false;
    }

    IMAGE_DATA_DIRECTORY* dir =
        &nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT];
    if (dir->VirtualAddress == 0 || dir->Size == 0) {
        g_walkFailure = L"client image: no import directory";
        return false;
    }

    IMAGE_IMPORT_DESCRIPTOR* imp =
        reinterpret_cast<IMAGE_IMPORT_DESCRIPTOR*>(base + dir->VirtualAddress);

    for (int d = 0; d < kMaxDescriptors && imp->Name != 0; ++d, ++imp) {
        if (dllName != NULL &&
            lstrcmpiA(reinterpret_cast<const char*>(base + imp->Name),
                      dllName) != 0) {
            continue;
        }

        if (imp->FirstThunk == 0) {
            continue;
        }
        IMAGE_THUNK_DATA* bound =
            reinterpret_cast<IMAGE_THUNK_DATA*>(base + imp->FirstThunk);

        if (symbol == NULL) {
            /*
             * Descriptor match only: we want the module this descriptor is
             * bound to -- including through an ordinal import, since no name
             * is read on this path.  We do NOT stop at the first binding
             * unless it satisfies requireExport: one forwarded or hooked slot
             * at the head of the table would otherwise pick a module that
             * merely sits next to the one we asked for.
             */
            for (int t = 0; t < kMaxThunksPerDescriptor &&
                            bound->u1.Function != 0; ++t, ++bound) {
                HMODULE candidate = NULL;
                if (!GetModuleHandleExW(
                        GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                            GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                        reinterpret_cast<LPCWSTR>(bound->u1.Function),
                        &candidate)) {
                    continue;
                }
                if (requireExport != NULL) {
                    FARPROC proc = GetProcAddress(candidate, requireExport);
                    if (proc == NULL) {
                        continue;
                    }
                    out->bound = proc;
                }
                out->module = candidate;
                return true;
            }
            continue;
        }

        /*
         * Never fall back to FirstThunk for the NAME table.  After the loader
         * has run, FirstThunk holds resolved absolute addresses, not RVAs to
         * IMAGE_IMPORT_BY_NAME -- reading it as the name table computes
         * base + <absolute VA>, a wild pointer, and the lstrcmpA below would
         * fault inside DllMain under the loader lock: a hard crash at client
         * start-up.  A descriptor with no INT simply cannot be searched by
         * name, so skip it.  (A normally linked VC9 executable gives every
         * descriptor an INT; this is the branch, not the expected path, and
         * the symbol == NULL mode above still works without one.)
         */
        if (imp->OriginalFirstThunk == 0) {
            continue;
        }

        IMAGE_THUNK_DATA* names =
            reinterpret_cast<IMAGE_THUNK_DATA*>(base + imp->OriginalFirstThunk);

        for (int t = 0; t < kMaxThunksPerDescriptor &&
                        names->u1.AddressOfData != 0; ++t, ++names, ++bound) {
            if (IMAGE_SNAP_BY_ORDINAL(names->u1.Ordinal)) {
                continue;
            }

            IMAGE_IMPORT_BY_NAME* byName =
                reinterpret_cast<IMAGE_IMPORT_BY_NAME*>(
                    base + names->u1.AddressOfData);

            if (lstrcmpA(reinterpret_cast<const char*>(byName->Name),
                         symbol) != 0) {
                continue;
            }
            if (bound->u1.Function == 0) {
                continue;
            }

            if (GetModuleHandleExW(
                    GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                        GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                    reinterpret_cast<LPCWSTR>(bound->u1.Function),
                    &out->module)) {
                out->bound =
                    reinterpret_cast<FARPROC>(bound->u1.Function);
                return true;
            }
            /* Unattributable binding: keep looking.  Revision 3 gave up on
             * the whole table here, so a first descriptor with an
             * unattributable thunk hid a perfectly good MSVCR90 descriptor
             * two entries later. */
            continue;
        }
    }
    return false;
}

void* AllocateFromClientCrt(size_t size) {
    /* Resolved once in DllMain so the load-time report is about the function
     * we will actually call, not about the module that might export it
     * (revision 2 printed "client CRT: located" before anyone had asked
     * MSVCR90 for operator new). */
    if (g_clientNew == NULL) {
        return NULL;
    }
    return g_clientNew(size);
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
    if (g_wstringCtor == NULL) {
        /*
         * We cannot construct.  We still return the destination, because
         * returning NULL does not avoid the damage and adds damage of its own:
         * GM-IMG-014's required_interface_fact flags possible_hidden_sret, and
         * in that shape the CALLER owns the buffer and runs ~basic_string on
         * it at scope exit whatever we leave in EAX -- so the wild free
         * happens either way, while a NULL in EAX additionally gets used as
         * the object (mov ecx,eax) for a NULL dereference on top.  The row's
         * own required_next_evidence says to keep the exact fallback
         * behaviour, and the fallback returns the same pointer in EAX.
         *
         * The evidence is the announce below, not the return value; the two
         * are independent.  If this line ever appears it is NEW EVIDENCE and
         * belongs in the test report: GM-IMG-014 records blocker
         * NO_PINNED_CALL_ROUTE_FOR_SLOT8 -- none of the five pinned
         * application+0x7C8 routes reaches slot +0x08 and no rel32 branch
         * targets it -- so a call here means a route nobody has observed
         * (split address or an external alias, which that row's nonclaim
         * explicitly leaves open).
         */
        Announce(L"slot +0x08 called with no MSVCP90 ctor -- destination left "
                 L"UNCONSTRUCTED, pointer returned unchanged.  REPORT THIS "
                 L"LINE: GM-IMG-014 has no pinned call route, so a call here "
                 L"is new evidence.");
        return destination;
    }
    if (destination != NULL) {
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
/*
 * Everything that can re-enter the loader happens here, on the client's own
 * thread, AFTER DllMain has returned -- never under the loader lock.
 * GetProcAddress on a forwarded export calls LdrpLoadDll; doing that from
 * DLL_PROCESS_ATTACH is a documented deadlock/corruption, and the symptom
 * would be "the client does not start", which on screen is indistinguishable
 * from "the DLL was never loaded" -- the one state the three-cell stop rule
 * cannot get out of.  [GM-IMG-001] has the client call this export from
 * ordinary code, so we are out of the lock by then.
 *
 * Single-threaded by construction: GM-IMG-001 pins one LoadLibrary ->
 * GetProcAddress -> call sequence at start-up.
 */
void ResolveOnce() {
    if (g_resolved) {
        return;
    }
    g_resolved = true;

    /*
     * Pin ourselves.  GM-IMG-017's blocker leaves downstream retention of the
     * slot +0x04 string unproven, and GM-IMG-010 has the client FreeLibrary us
     * at shutdown.  If a panel kept the raw pointer, unmapping this module
     * would fault while reading it -- a crash on exit whose README triage
     * would send the tester to the CRT, which would look fine.  The result is
     * checked and reported: revision 3 discarded it, so the whole argument
     * rested on a call nobody could confirm had worked.
     */
    HMODULE self = NULL;
    BOOL pinned = GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                                         GET_MODULE_HANDLE_EX_FLAG_PIN,
                                     reinterpret_cast<LPCWSTR>(&g_modelBasename),
                                     &self);

    ClientImport crt;
    const wchar_t* crtLine =
        L"client CRT: NOT FOUND -- no import descriptor named msvcr90.dll "
        L"binds ??3@YAXPAX@Z; CreateGameMaster will return NULL";
    if (FindClientImport(kMsvcr90, kOperatorDelete, NULL, &crt)) {
        g_clientCrt = crt.module;
        g_clientNew = reinterpret_cast<operator_new_t>(
            GetProcAddress(g_clientCrt, kOperatorNew));
        crtLine = g_clientNew
            ? L"client CRT: msvcr90.dll instance taken from the client's own "
              L"operator delete import, and ??2@YAPAXI@Z resolved in it"
            : L"client CRT: msvcr90.dll instance located, but it does not "
              L"export ??2@YAPAXI@Z -- CreateGameMaster will return NULL";
    } else if (FindClientImport(NULL, kOperatorDelete, NULL, &crt)) {
        /*
         * Diagnostic only -- deliberately NOT used.  Somebody else in the
         * process imports operator delete under that name (MFC90, an injected
         * anti-cheat module, a proxy CRT).  Allocating from it would be the
         * cross-heap free GM-IMG-010's required_interface_fact forbids
         * (returned_object_memory_must_be_safe_for_application_MSVCR90_delete),
         * so we refuse and print who it was, because that is the fact the
         * attended round needs.
         */
        wchar_t path[MAX_PATH];
        path[0] = L'\0';
        GetModuleFileNameW(crt.module, path, MAX_PATH);
        Announce(L"client CRT: ??3@YAXPAX@Z is imported, but NOT from a "
                 L"descriptor named msvcr90.dll.  REFUSING it.  Owner:");
        Announce(path);
    }

    /*
     * MSVCP90.  Both anchors are inside the client's own import table AND
     * filtered by descriptor name, because the decorated ctor name is
     * byte-identical in MSVCP80/90/100 -- a symbol-only match can bind the
     * wrong library and reinstate the cross-heap free (H1's whole point).
     *   1. the client's own binding for the constructor -- then we call the
     *      exact address it calls;
     *   2. failing that, a module the msvcp90.dll descriptor is bound to that
     *      actually exports the name.
     *
     * [PROPOSED] the decorated name is not verified against this machine's
     * msvcp90.dll.  If it is wrong we resolve NULL, say so on the line below,
     * and degrade as described in CreateGameMaster -- we never fall back to an
     * inlined constructor, because the whole point of calling the export is
     * that our own layout may differ.
     */
    ClientImport cpp;
    ClientImport probe;
    const wchar_t* cppLine =
        L"msvcp90 wstring ctor: NOT RESOLVED -- the client binds nothing from "
        L"a descriptor named msvcp90.dll; slot +0x00 (+4 init) and +0x08 skip "
        L"construction";
    if (FindClientImport(kMsvcp90, kWstringCtor, NULL, &cpp)) {
        g_wstringCtor = reinterpret_cast<wstring_ctor_t>(cpp.bound);
        cppLine = L"msvcp90 wstring ctor: resolved from the client's own "
                  L"msvcp90.dll import binding (that exact instance)";
    } else if (FindClientImport(kMsvcp90, NULL, kWstringCtor, &cpp)) {
        g_wstringCtor = reinterpret_cast<wstring_ctor_t>(cpp.bound);
        cppLine = L"msvcp90 wstring ctor: the client does not import it, but "
                  L"the msvcp90.dll instance it is bound to exports it";
    } else if (FindClientImport(kMsvcp90, NULL, NULL, &probe)) {
        cppLine = L"msvcp90 wstring ctor: NOT RESOLVED -- the client's "
                  L"msvcp90.dll instance does not export that decorated name. "
                  L"Run dumpbin /exports msvcp90.dll and report what it does "
                  L"export";
    }

    if (g_walkFailure != NULL) {
        Announce(g_walkFailure);
    }
    Announce(pinned ? L"self-pin: ok (FreeLibrary cannot unmap us)"
                    : L"self-pin: FAILED -- a retained slot +0x04 pointer "
                      L"would dangle after FreeLibrary; report a crash on "
                      L"exit as THIS, not as a heap mismatch");
    Announce(crtLine);
    Announce(cppLine);
    Announce(L"key=" PF_GM_KEY);
#if PF_GM_SLOT0_TOUCH_PLUS4
    Announce(L"slot +0x00 +4 init: ON  (cell 3 -- the guessed subobject)");
#else
    Announce(L"slot +0x00 +4 init: off (cell 1/2 default -- writes the -1 and "
             L"leaves +4 as the caller left it)");
#endif
}

extern "C" void* __cdecl CreateGameMaster(void) {
    try {
        ResolveOnce();
#if PF_GM_SLOT0_TOUCH_PLUS4
        /*
         * Refuse rather than hand back a half-built object -- but only in the
         * build that promises to build one.
         *
         * With PF_GM_SLOT0_TOUCH_PLUS4=1 and no constructor, slot +0x00 would
         * write its -1 and leave the +4 subobject UNINITIALISED, diverging
         * from the proven fallback which initialises it [GM-IMG-012].  That is
         * a NEW failure, strictly worse than the dead button we already have,
         * so we decline the job and say why.  DllMain has already printed
         * which lookup failed.
         */
        if (g_wstringCtor == NULL) {
            Announce(L"FAIL: msvcp90 wstring ctor unresolved and "
                     L"PF_GM_SLOT0_TOUCH_PLUS4=1; returning NULL rather than a "
                     L"half-constructed object.  Rebuild with =0 to test the "
                     L"key path without the constructor.");
            return NULL;
        }
#else
        /*
         * Default build (revision 3): the constructor is NOT required to do
         * this job, so its absence must not cost the attended round.
         *
         * Note what this branch does NOT claim: with the macro off, +4 is
         * left uninitialised on EVERY call, resolved constructor or not, so
         * the divergence from GM-IMG-012's fallback that the =1 branch above
         * refuses to ship is shipped here unconditionally.  That is the
         * ordered trade (see the PF_GM_SLOT0_TOUCH_PLUS4 block at the top),
         * not something this guard prevents.
         *
         * Slot +0x00 writes only the -1 that GM-IMG-012 states verbatim, and
         * slot +0x04 -- the only slot on the click route that decides anything
         * [GM-IMG-006, -007] -- returns a static string and needs no heap and
         * no CRT at all.  Slot +0x08 has no pinned call route whatsoever
         * (GM-IMG-014, blocker NO_PINNED_CALL_ROUTE_FOR_SLOT8) and now refuses
         * loudly instead of lying.  Refusing the whole interface here would
         * trade the one question we can answer this round -- does a non-empty
         * key open the window -- against a slot nobody has observed being
         * called.
         *
         * [LANE-GM assumption, awaiting COO confirmation] this is narrower
         * than the "tie the guard to the macro" wording in the lane's 0559
         * letter, which asserted that nothing uses the constructor when the
         * macro is 0.  That is not true -- slot +0x08 uses it unconditionally
         * -- so the guard moved and slot +0x08 was made safe, rather than the
         * claim being taken at face value.
         */
        if (g_wstringCtor == NULL) {
            Announce(L"degraded: no MSVCP90 wstring ctor.  Proceeding: slot "
                     L"+0x00 writes only the -1 and slot +0x08 will refuse "
                     L"(GM-IMG-014 has no pinned call route).");
        }
#endif

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

    /*
     * Everything here must be safe under the loader lock, and the load proof
     * must come FIRST.
     *
     * Revision 3 walked the import table and called GetProcAddress twice
     * before announcing anything, so if any of that had faulted or re-entered
     * the loader, the client would have failed to start with no [GM_PLUGIN]
     * line at all -- which the three-cell stop rule reads as "the DLL was
     * never loaded" and answers by running plugin_image_check, a tool that
     * inspects bytes in a file and would report image_ok.  That is a state the
     * plan can enter and cannot leave, on the one attended round it is
     * budgeted for.  So: announce first, resolve later (see ResolveOnce,
     * called from CreateGameMaster on the client's own thread).
     *
     * DisableThreadLibraryCalls and OutputDebugStringW are both safe here.
     */
    DisableThreadLibraryCalls(module);
    Announce(L"loaded build=" PF_GM_WIDE(__DATE__) L" " PF_GM_WIDE(__TIME__));
    Announce(L"key=" PF_GM_KEY);
#if PF_GM_SLOT0_TOUCH_PLUS4
    Announce(L"slot +0x00 +4 init: ON  (cell 3 -- the guessed subobject)");
#else
    Announce(L"slot +0x00 +4 init: off (cell 1/2 default)");
#endif
    Announce(L"CRT / msvcp90 lookups are deferred to the first "
             L"CreateGameMaster call, off the loader lock -- their result "
             L"lines appear then, not now");

    return TRUE;
}
