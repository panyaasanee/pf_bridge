# ============================================================================
# TEMPLATE_preflight_unattended.ps1 - the first job of an unattended round.
# Enumerate every visible top-level window and ABORT the round if any of them
# is elevated, or if any of them cannot be PROVED not to be. ASCII ONLY.
#
# WHY THIS FILE EXISTS
# --------------------
# 2026-08-21, big round #11, unattended, GT-031. An elevated
# "Administrator: Windows PowerShell" window - Panya's own, left open before
# going to bed - sat across the middle of the screen at L234 T234 R1227 B753
# and stayed on top of everything. The tester could not run the round and,
# crucially, could not FIX it. Windows forbids a normal-integrity process from
# touching an elevated window through every channel there is, and the tester
# measured all three rather than guessing:
#
#   clicking its minimize button with computer use   -> nothing happened (UIPI)
#   job 953: ShowWindow(hWnd, SW_MINIMIZE)           -> callable, NO effect
#   job 954: SetWindowPos to move it out of the way  -> returned False,
#                                                       lastError = 5 (ACCESS DENIED)
#
# Moving the GAME window instead did work (the game is a normal process, jobs
# 955/956), and the game still would not accept a single click - most likely
# the elevated window holding the foreground lock, though that was NOT isolated
# and is not claimed here.
#
# Twenty minutes of an unattended round were spent discovering a condition that
# was visible on screen before the round started and that no amount of cleverness
# could have fixed from inside the round. That is a preflight, not a bug. The
# tester asked for exactly this job, and asked for it to ABORT rather than warn.
#
# WHAT IT DOES
#   - Enumerates every visible top-level window: title, owning pid, process
#     name, rectangle, topmost/minimized state.
#   - For each owning process, tries to determine elevation from its token.
#   - ABORTS with a non-zero exit and a NAMED LIST if any elevated window is
#     visible.
#
# WHAT IT DELIBERATELY DOES NOT DO - AND CANNOT
#   It is READ-ONLY. It never moves, minimizes, restores, closes, hides or
#   focuses a window, and never signals, suspends or kills a process. That is
#   not a promise in prose: the interop class below declares ONLY read
#   functions. There is no ShowWindow, no SetWindowPos, no SetForegroundWindow,
#   no PostMessage, no Stop-Process and no CloseMainWindow anywhere in this
#   file, so there is nothing here that could do any of it even by accident.
#   The one thing it writes is its own log in outbox\ (skip with -NoLog).
#
# "CANNOT DETERMINE" IS A FINDING, NOT AN ALL-CLEAR
#   Reading another process's token requires OpenProcess + OpenProcessToken.
#   From a normal-integrity process those calls are DENIED for exactly the
#   processes we are most worried about - being unable to look IS the usual
#   symptom of elevation, not evidence of innocence. So an undetermined window
#   is reported by name in its own section and, by default, ABORTS the round
#   too (exit 62). Defaulting an unknown to "fine" is the failure shape this
#   project keeps paying for: the BOM'd flag file that read as "free" exactly
#   when it was held (round 109), the stale info file that made a teardown skip
#   its ctrl-c (job 145), the paired teardown that was never executed before it
#   shipped (job 950). Pass -UndeterminedIsWarning to accept the risk out loud;
#   it prints a line saying that somebody chose to.
#
# EXIT CODES
#   0   no visible elevated window, and every window was determined
#   61  at least one VISIBLE ELEVATED window - the round must not start
#   62  at least one window whose elevation could not be determined
#       (suppressed to a loud warning by -UndeterminedIsWarning)
#   63  the enumeration itself failed - nothing was measured, so nothing is
#       proved, so this is a failure and not a pass
#
# USAGE - the two lines a big-round boot sequence adds, FIRST, before it starts
# a server or a client:
#
#     & 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\TEMPLATE_preflight_unattended.ps1'
#     if ($LASTEXITCODE -ne 0) { Write-Host 'PREFLIGHT FAILED - not booting this round'; exit $LASTEXITCODE }
#
# Run it by hand the same way; it takes about a second and touches nothing:
#
#     powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\TEMPLATE_preflight_unattended.ps1"
#
# A NOTE ON TITLES AND cp874
#   Window titles come from other people's programs and can contain anything.
#   The console here is cp874 and one stray character turns the project gate
#   red, so every title is sanitised for printing: any character outside
#   printable ASCII becomes '?', and the line says how many were replaced. The
#   ELEVATION TEST NEVER USES THE PRINTED FORM - it uses the token, and the
#   English "Administrator: " title marker is matched against the RAW title.
#   That marker only exists in English Windows; on any other display language
#   the title check simply never fires and the token probe is what decides.
#   This is a limit of an ASCII-only file, stated rather than hidden.
# ============================================================================

param(
    [string] $BridgeRoot = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge',
    [string] $JobTag     = 'PREFLIGHT_unattended',
    # Downgrade "cannot determine" from an abort to a loud warning. Somebody
    # has to type this; it is never the default.
    [switch] $UndeterminedIsWarning,
    [switch] $NoLog
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

$outbox = Join-Path $BridgeRoot 'outbox'
$log    = ''
if (-not $NoLog -and (Test-Path -LiteralPath $outbox)) {
    $log = Join-Path $outbox ($JobTag + '.utf8.txt')
}
function W($m) {
    $l = [string]$m
    Write-Host $l
    if ($log) { $l | Out-File -FilePath $log -Encoding utf8 -Append }
}
if ($log) {
    ('=== ' + $JobTag + '  ' + (Get-Date -Format 'yyyyMMdd_HHmmss') + ' ===') |
        Out-File -FilePath $log -Encoding utf8
}

W '=== PREFLIGHT: unattended round - visible window survey (READ ONLY) ==='
W ('time       : ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
W ('this pid   : ' + $PID)
W ('bridge     : ' + $BridgeRoot)
W 'read-only  : no window is moved, minimized, closed or focused; no process is signalled'
W ''

# ----------------------------------------------------------------------------
# Interop. READ FUNCTIONS ONLY - see the header. If you ever need to add a
# function to this class, ask first whether this file is still read-only.
# ----------------------------------------------------------------------------
$cs = @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

public class PFPreflightWin
{
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }

    private delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);

    [DllImport("user32.dll")]
    private static extern bool EnumWindows(EnumProc cb, IntPtr lParam);
    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int GetWindowTextLengthW(IntPtr hWnd);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int GetWindowTextW(IntPtr hWnd, StringBuilder buf, int max);
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT r);
    [DllImport("user32.dll")]
    private static extern int GetWindowThreadProcessId(IntPtr hWnd, out int pid);
    [DllImport("user32.dll", EntryPoint = "GetWindowLongW")]
    private static extern int GetWindowLongW(IntPtr hWnd, int index);
    [DllImport("user32.dll")]
    public static extern IntPtr GetShellWindow();
    [DllImport("user32.dll")]
    public static extern int GetSystemMetrics(int index);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern IntPtr OpenProcess(int access, bool inherit, int pid);
    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool CloseHandle(IntPtr h);
    [DllImport("advapi32.dll", SetLastError = true)]
    private static extern bool OpenProcessToken(IntPtr proc, int access, out IntPtr tok);
    [DllImport("advapi32.dll", SetLastError = true)]
    private static extern bool GetTokenInformation(IntPtr tok, int cls, IntPtr buf, int len, out int ret);

    public static List<IntPtr> TopLevelWindows()
    {
        List<IntPtr> r = new List<IntPtr>();
        EnumWindows(delegate(IntPtr h, IntPtr l) { r.Add(h); return true; }, IntPtr.Zero);
        return r;
    }

    public static string TitleOf(IntPtr hWnd)
    {
        int n = GetWindowTextLengthW(hWnd);
        if (n <= 0) { return ""; }
        StringBuilder sb = new StringBuilder(n + 2);
        GetWindowTextW(hWnd, sb, sb.Capacity);
        return sb.ToString();
    }

    public static int PidOf(IntPtr hWnd)
    {
        int pid = 0;
        GetWindowThreadProcessId(hWnd, out pid);
        return pid;
    }

    public static int ExStyleOf(IntPtr hWnd) { return GetWindowLongW(hWnd, -20); }

    // "ELEVATED" | "NORMAL" | "UNDETERMINED:<why>"
    // Never throws. The caller must treat UNDETERMINED as a finding.
    public static string Elevation(int pid)
    {
        int PROCESS_QUERY_LIMITED_INFORMATION = 0x1000;
        int PROCESS_QUERY_INFORMATION         = 0x0400;
        int TOKEN_QUERY                       = 0x0008;
        int TokenElevation                    = 20;

        IntPtr h = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, false, pid);
        int e1 = Marshal.GetLastWin32Error();
        if (h == IntPtr.Zero)
        {
            h = OpenProcess(PROCESS_QUERY_INFORMATION, false, pid);
            int e2 = Marshal.GetLastWin32Error();
            if (h == IntPtr.Zero)
            {
                return "UNDETERMINED:OpenProcess denied (err " + e1 + "/" + e2 + ")";
            }
        }
        try
        {
            IntPtr tok = IntPtr.Zero;
            if (!OpenProcessToken(h, TOKEN_QUERY, out tok))
            {
                return "UNDETERMINED:OpenProcessToken denied (err " + Marshal.GetLastWin32Error() + ")";
            }
            try
            {
                IntPtr buf = Marshal.AllocHGlobal(4);
                try
                {
                    int ret = 0;
                    if (!GetTokenInformation(tok, TokenElevation, buf, 4, out ret))
                    {
                        return "UNDETERMINED:GetTokenInformation failed (err " + Marshal.GetLastWin32Error() + ")";
                    }
                    int v = Marshal.ReadInt32(buf);
                    if (v != 0) { return "ELEVATED"; }
                    return "NORMAL";
                }
                finally { Marshal.FreeHGlobal(buf); }
            }
            finally { CloseHandle(tok); }
        }
        finally { CloseHandle(h); }
    }
}
'@

$typeOk = $true
try {
    if (-not ([System.Management.Automation.PSTypeName]'PFPreflightWin').Type) {
        Add-Type -TypeDefinition $cs -Language CSharp -ErrorAction Stop
    }
} catch {
    $typeOk = $false
    W ('ABORT(63): could not compile the window-survey interop: ' + $_.Exception.Message)
}
if (-not $typeOk) {
    W 'Nothing was measured, so nothing is proved. This is a FAIL, not a pass.'
    W 'PREFLIGHT_UNATTENDED_VERDICT=FAIL'
    exit 63
}

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
# Titles come from other people's programs. Sanitise for the cp874 console; the
# elevation decision never uses this form.
function SafeTitle($s) {
    $t   = [string]$s
    $sb  = New-Object System.Text.StringBuilder
    $bad = 0
    foreach ($ch in $t.ToCharArray()) {
        $i = [int]$ch
        if ($i -ge 32 -and $i -le 126) { $null = $sb.Append($ch) }
        else { $null = $sb.Append('?'); $bad++ }
    }
    return New-Object PSObject -Property @{ Text = $sb.ToString(); Replaced = $bad }
}

$WS_EX_TOOLWINDOW = 0x00000080
$WS_EX_TOPMOST    = 0x00000008
$SM_CXSCREEN      = 0
$SM_CYSCREEN      = 1

$scrW = 0
$scrH = 0
try {
    $scrW = [PFPreflightWin]::GetSystemMetrics($SM_CXSCREEN)
    $scrH = [PFPreflightWin]::GetSystemMetrics($SM_CYSCREEN)
} catch { $scrW = 0; $scrH = 0 }
$cx = [int]($scrW / 2)
$cy = [int]($scrH / 2)
W ('primary screen : ' + $scrW + ' x ' + $scrH + '  (centre point ' + $cx + ',' + $cy + ')')
W ''

$handles = @()
try { $handles = @([PFPreflightWin]::TopLevelWindows()) }
catch {
    W ('ABORT(63): EnumWindows failed: ' + $_.Exception.Message)
    W 'PREFLIGHT_UNATTENDED_VERDICT=FAIL'
    exit 63
}
W ('top-level windows returned by EnumWindows : ' + $handles.Count)
if ($handles.Count -eq 0) {
    W 'ABORT(63): EnumWindows returned nothing. A live desktop always has windows,'
    W 'so this measured nothing at all - and nothing measured is not an all-clear.'
    W 'PREFLIGHT_UNATTENDED_VERDICT=FAIL'
    exit 63
}

$shell = [IntPtr]::Zero
try { $shell = [PFPreflightWin]::GetShellWindow() } catch { $shell = [IntPtr]::Zero }

$rows = New-Object System.Collections.ArrayList
foreach ($h in $handles) {
    if (-not [PFPreflightWin]::IsWindowVisible($h)) { continue }
    if ($h -eq $shell) { continue }

    $raw = ''
    try { $raw = [PFPreflightWin]::TitleOf($h) } catch { $raw = '' }
    if ([string]::IsNullOrEmpty($raw)) { continue }

    $ex = 0
    try { $ex = [PFPreflightWin]::ExStyleOf($h) } catch { $ex = 0 }
    # Tool windows are palettes and tooltips; they are not what blocks a round.
    if (($ex -band $WS_EX_TOOLWINDOW) -ne 0) { continue }

    $r = New-Object 'PFPreflightWin+RECT'
    $gotRect = $false
    try { $gotRect = [PFPreflightWin]::GetWindowRect($h, [ref] $r) } catch { $gotRect = $false }
    $L = 0; $T = 0; $R = 0; $B = 0
    if ($gotRect) { $L = $r.Left; $T = $r.Top; $R = $r.Right; $B = $r.Bottom }
    if ($gotRect -and ($R - $L) -le 0 -and ($B - $T) -le 0) { continue }

    $wpid = 0
    try { $wpid = [PFPreflightWin]::PidOf($h) } catch { $wpid = 0 }
    $pname = '(process not readable)'
    try {
        $p = Get-Process -Id $wpid -ErrorAction Stop
        $pname = $p.ProcessName
    } catch { $pname = '(process not readable)' }

    $elev = 'UNDETERMINED:no pid'
    if ($wpid -gt 0) {
        try { $elev = [string][PFPreflightWin]::Elevation($wpid) }
        catch { $elev = 'UNDETERMINED:probe threw (' + $_.Exception.Message + ')' }
    }

    # The English title marker. It is a SECOND, independent signal: Windows
    # writes "Administrator: " into the title bar of an elevated console, and
    # that is readable even when the token is not. It can only ever ADD an
    # elevated verdict, never remove one.
    $marker = $false
    if ($raw.StartsWith('Administrator: ') -or $raw -like '*Administrator: *') { $marker = $true }

    $state = 'ELEVATION-UNDETERMINED'
    if ($elev -ceq 'ELEVATED') { $state = 'ELEVATED' }
    elseif ($elev -ceq 'NORMAL') { $state = 'NORMAL' }
    if ($marker -and $state -ne 'ELEVATED') { $state = 'ELEVATED' }

    $st = SafeTitle $raw
    $flags = @()
    if (($ex -band $WS_EX_TOPMOST) -ne 0) { $flags += 'TOPMOST' }
    $min = $false
    try { $min = [PFPreflightWin]::IsIconic($h) } catch { $min = $false }
    if ($min) { $flags += 'MINIMIZED' }
    $coversCentre = $false
    if ($gotRect -and -not $min -and $scrW -gt 0 -and
        $cx -ge $L -and $cx -lt $R -and $cy -ge $T -and $cy -lt $B) {
        $coversCentre = $true
        $flags += 'COVERS-SCREEN-CENTRE'
    }

    $null = $rows.Add((New-Object PSObject -Property @{
        Pid          = $wpid
        Process      = $pname
        Title        = $st.Text
        TitleFixed   = $st.Replaced
        Rect         = ('L' + $L + ' T' + $T + ' R' + $R + ' B' + $B)
        State        = $state
        Elev         = $elev
        Marker       = $marker
        Flags        = ($flags -join ',')
        CoversCentre = $coversCentre
    }))
}

W ('visible top-level windows with a title  : ' + $rows.Count)
W ''
W '--- survey ---'
W ('{0,-22} {1,-8} {2,-22} {3,-26} {4}' -f 'state', 'pid', 'process', 'rect', 'title')
foreach ($row in $rows) {
    W ('{0,-22} {1,-8} {2,-22} {3,-26} {4}' -f $row.State, $row.Pid, $row.Process, $row.Rect, $row.Title)
    $extra = @()
    if ($row.Flags) { $extra += ('flags=' + $row.Flags) }
    if ($row.State -ne 'NORMAL') { $extra += ('probe=' + $row.Elev) }
    if ($row.Marker) { $extra += 'title-marker=Administrator' }
    if ($row.TitleFixed -gt 0) { $extra += ('title had ' + $row.TitleFixed + ' non-ASCII characters replaced with ?') }
    if ($extra.Count -gt 0) { W ('    ' + ($extra -join '  ')) }
}
W ''

$elevated = @($rows | Where-Object { $_.State -ceq 'ELEVATED' })
$unknown  = @($rows | Where-Object { $_.State -ceq 'ELEVATION-UNDETERMINED' })

if ($elevated.Count -gt 0) {
    W '############################################################################'
    W '## PREFLIGHT ABORT: a VISIBLE ELEVATED WINDOW IS ON SCREEN'
    W '##'
    W '## An unattended round cannot run past this. A normal-integrity process is'
    W '## forbidden by Windows (UIPI) from clicking, minimizing or moving an'
    W '## elevated window - measured on 2026-08-21: ShowWindow had no effect and'
    W '## SetWindowPos returned False with lastError=5, ACCESS DENIED. The round'
    W '## cannot fix this from the inside, and the game will not accept clicks'
    W '## while it is there.'
    W '##'
    W '## CLOSE OR MINIMIZE THESE WINDOWS, THEN RE-RUN THE PREFLIGHT:'
    foreach ($row in $elevated) {
        W ('##   * "' + $row.Title + '"')
        W ('##     pid ' + $row.Pid + '  process ' + $row.Process + '  ' + $row.Rect + '  ' + $row.Flags)
        W ('##     evidence: ' + $row.Elev + $(if ($row.Marker) { '  + Administrator title marker' } else { '' }))
    }
    W '############################################################################'
    W ('elevated windows : ' + $elevated.Count)
    W ('undetermined     : ' + $unknown.Count)
    W 'PREFLIGHT_UNATTENDED_VERDICT=FAIL'
    exit 61
}

if ($unknown.Count -gt 0) {
    W '############################################################################'
    W '## PREFLIGHT FINDING: elevation COULD NOT BE DETERMINED for these windows'
    W '##'
    W '## Being unable to read a process token is not evidence that the process is'
    W '## ordinary. It is the usual symptom of the thing being looked for: from a'
    W '## normal-integrity process, OpenProcess/OpenProcessToken are DENIED for'
    W '## exactly the elevated processes this preflight exists to catch. So this'
    W '## is reported as a finding and not quietly rounded down to "fine".'
    foreach ($row in $unknown) {
        W ('##   * "' + $row.Title + '"')
        W ('##     pid ' + $row.Pid + '  process ' + $row.Process + '  ' + $row.Rect + '  ' + $row.Flags)
        W ('##     probe: ' + $row.Elev)
    }
    W '############################################################################'
    if ($UndeterminedIsWarning) {
        W 'ACCEPTED: -UndeterminedIsWarning was passed, so an operator has taken this'
        W 'risk deliberately and on the record. The round may start; if the game stops'
        W 'accepting clicks, THIS IS THE FIRST THING TO SUSPECT.'
        W ('elevated windows : 0   undetermined (accepted) : ' + $unknown.Count)
        W 'PREFLIGHT_UNATTENDED_VERDICT=PASS-WITH-FINDING'
        exit 0
    }
    W ('undetermined windows : ' + $unknown.Count)
    W 'Close them, or re-run with -UndeterminedIsWarning to accept the risk out loud.'
    W 'PREFLIGHT_UNATTENDED_VERDICT=FAIL'
    exit 62
}

W ('elevated windows : 0')
W ('undetermined     : 0')
W ('all ' + $rows.Count + ' visible windows were determined to be normal integrity.')
W 'PREFLIGHT_UNATTENDED_VERDICT=PASS'
exit 0
