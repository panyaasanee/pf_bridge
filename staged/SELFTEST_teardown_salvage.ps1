# ============================================================================
# SELFTEST_teardown_salvage.ps1 - drive TEMPLATE_teardown_generic.ps1 through
# all four salvage cases and watch each one decide. ASCII ONLY.
#
# WHY THIS FILE EXISTS
# --------------------
# Round 109: "a template shipped without ever being executed explodes on the
# day it matters most". The flag-helper parse error sat in a function that is
# only reached when a flag is actually held, so it would have fired for the
# first time during a real contended commit. Job 176 caught it by RUNNING the
# file. The salvage path has exactly the same shape: it only runs on the worst
# day of a round, when the evidence is already half gone and nobody is in the
# mood to debug a job. So it gets a self-test, and the self-test runs the real
# template - not a copy of its logic.
#
# WHAT IT COVERS
#   T1  fresh round, no -Salvage   -> normal receipt, exit 0, NO salvage file
#   T2  stale round, no -Salvage   -> exit 12, refusal, NO salvage file
#       (the default must NOT be weakened by the new switch)
#   T3  stale round WITH -Salvage  -> salvage receipt exists, SALVAGE marker in
#       the filename AND on the first line, non-empty MISSING list, boot stamp
#       and real age in the header, and the run-copy DB provably not modified
#   T4  -Salvage with NO console log -> still writes a receipt, and that receipt
#       lists the console log as MISSING instead of failing
#
# SAFETY - what this self-test can and cannot touch
#   - Everything happens in a throwaway sandbox under %TEMP%. The real
#     pf_bridge outbox, the real capture roots and the real canonical DB are
#     never read or written: the template takes -BridgeRoot/-MainRoot/
#     -ClientRoot for exactly this reason.
#   - It watches ports 59188/59189, NOT 10188/10189, and refuses to run if
#     anything is listening on them.
#   - The three pids in the fixture info file are this self-test's OWN pid.
#     That pid certainly exists (so the probe path is exercised) but its
#     process name is 'powershell', so the template's identity guards
#     (console must be 'py', client must be 'GameClient*') can never pass and
#     nothing can ever be signalled or stopped. -ForceKillIfPortsStuck is not
#     passed, so the force-kill branch is unreachable too.
#   - T1's fixture deliberately omits the 'rundb' key so the normal path does
#     not shell out to `py -3` against a fake database. A self-test that needs
#     the python toolchain to be healthy is testing the wrong thing.
#
# RUN IT
#   powershell -NoProfile -ExecutionPolicy Bypass -File staged\SELFTEST_teardown_salvage.ps1
# Last line is SELFTEST_TEARDOWN_SALVAGE_VERDICT=PASS or =FAIL; exit 1 on FAIL.
# ============================================================================

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$here   = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($here)) { $here = Join-Path $bridge 'staged' }
$tpl     = Join-Path $here 'TEMPLATE_teardown_generic.ps1'
$helpers = Join-Path $here 'TEMPLATE_lock_flag_helpers.ps1'
if (-not (Test-Path -LiteralPath $tpl)) { $tpl = Join-Path $bridge 'staged\TEMPLATE_teardown_generic.ps1' }
if (-not (Test-Path -LiteralPath $helpers)) { $helpers = Join-Path $bridge 'staged\TEMPLATE_lock_flag_helpers.ps1' }

$TESTPORTS = @(59188, 59189)
$STALE_MIN = 600     # well past the 420 min limit
$FRESH_MIN = 5

$fail = 0
function Check($label, $ok, $detail) {
    $verdict = 'FAIL'
    if ($ok) { $verdict = 'PASS' } else { $script:fail = 1 }
    $line = ('{0,-58} : {1}' -f $label, $verdict)
    if (-not $ok -and $detail) { $line = $line + '   <- ' + $detail }
    Write-Host $line
}

Write-Host '=== SELFTEST teardown -Salvage ==='
Write-Host ('time     : ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
Write-Host ('template : ' + $tpl)

if (-not (Test-Path -LiteralPath $tpl)) {
    Write-Host 'ABORT: teardown template not found - nothing to test'
    Write-Host 'SELFTEST_TEARDOWN_SALVAGE_VERDICT=FAIL'
    exit 1
}
$busy = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
          Where-Object { $TESTPORTS -contains [int]$_.LocalPort })
if ($busy.Count -gt 0) {
    Write-Host ("ABORT: something is listening on the self-test ports " + ($TESTPORTS -join ',') + " - refusing to run")
    Write-Host 'SELFTEST_TEARDOWN_SALVAGE_VERDICT=FAIL'
    exit 1
}

$sand = Join-Path $env:TEMP ('pf_salvage_selftest_' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $sand -Force | Out-Null
Write-Host ('sandbox  : ' + $sand)
Write-Host ''

# ---------------------------------------------------------------------------
# fixture builder
# ---------------------------------------------------------------------------
# $BootAgeMinutes and $InfoAgeMinutes are separate on purpose. The template has
# TWO stale checks - the mtime of the info file, and the boot stamp inside it -
# and they fire on different lines with different messages. The round that broke
# on 2026-08-20 tripped the SECOND one ("boot stamp is 185.7 min old"), so the
# self-test must be able to reach it, which means being able to hand it an info
# file whose mtime is younger than its own boot stamp.
function New-RoundFixture($Name, $BootAgeMinutes, $InfoAgeMinutes, $WithConsoleLog, $WithRunDbKey) {
    $root   = Join-Path $sand $Name
    $b      = Join-Path $root 'bridge'
    $ob     = Join-Path $b 'outbox'
    $st     = Join-Path $b 'staged'
    $m      = Join-Path $root 'main'
    $ms     = Join-Path $m 'state'
    $c      = Join-Path $root 'client'
    New-Item -ItemType Directory -Path $ob, $st, $ms, $c -Force | Out-Null

    # The template dot-sources staged\TEMPLATE_lock_flag_helpers.ps1 relative to
    # -BridgeRoot, so the sandbox gets a copy: the self-test must exercise the
    # SAME writer the real machine uses, not the inline fallback.
    if (Test-Path -LiteralPath $helpers) {
        Copy-Item -LiteralPath $helpers -Destination (Join-Path $st 'TEMPLATE_lock_flag_helpers.ps1') -Force
    }

    $bootTime = (Get-Date).AddMinutes(-1 * [double]$BootAgeMinutes)
    $stamp    = $bootTime.ToString('yyyyMMdd_HHmmss')

    $canon = Join-Path $ms 'pirateforce.sqlite3'
    Set-Content -LiteralPath $canon -Value 'selftest fixture - not a real database' -Encoding ascii
    $csha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash.ToUpper()
    Set-Content -LiteralPath (Join-Path $b 'CANON_SHA.txt') -Value $csha -Encoding ascii

    $runDb = Join-Path $ms ('pirateforce_selftest_' + $stamp + '.sqlite3')
    Copy-Item -LiteralPath $canon -Destination $runDb -Force

    $cap = Join-Path $c ('capture_selftest_' + $stamp)
    New-Item -ItemType Directory -Path $cap -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $cap 'GAME_LIVE.txt') -Value 'selftest wire log line' -Encoding ascii
    if ($WithConsoleLog) {
        Set-Content -LiteralPath (Join-Path $cap 'server_console_live.out.txt') -Encoding ascii -Value @(
            '[FOUNDATION] listener ready',
            'Traceback (most recent call last):',
            '  File "selftest.py", line 1, in <module>',
            'ValueError: selftest traceback number one',
            'Traceback (most recent call last):',
            '  File "selftest.py", line 2, in <module>',
            'ValueError: selftest traceback number two',
            '[FOUNDATION] stopped'
        )
    }

    $keys = @(
        ('clientpid=' + $PID),
        ('console=' + $PID),
        ('server=' + $PID),
        ('stamp=' + $stamp)
    )
    if ($WithRunDbKey) { $keys += ('rundb=' + $runDb) }
    $keys += 'title=selftest fixture window'
    $info = Join-Path $ob ('900_client_info_' + $stamp + '.txt')
    $keys | Out-File -FilePath $info -Encoding ascii
    (Get-Item -LiteralPath $info).LastWriteTime = (Get-Date).AddMinutes(-1 * [double]$InfoAgeMinutes)

    return New-Object PSObject -Property @{
        Root = $root; Bridge = $b; Outbox = $ob; Main = $m; Client = $c
        Stamp = $stamp; RunDb = $runDb; Info = $info; Capture = $cap
    }
}

# ---------------------------------------------------------------------------
# run the REAL template against a fixture
#
# -Command and not -File: with -File, PowerShell hands each argument to the
# binder as a plain string, and "59188,59189" does not convert to [int[]].
# -Command parses real PowerShell, so the array binds. Every literal below is
# single-quoted, so paths with spaces survive and no double quote ever enters
# the command line.
# ---------------------------------------------------------------------------
function Invoke-Template($Fx, $UseSalvage) {
    function Q($s) { "'" + ([string]$s).Replace("'", "''") + "'" }
    $cmd = '& ' + (Q $tpl) +
           ' -BridgeRoot '    + (Q $Fx.Bridge) +
           ' -MainRoot '      + (Q $Fx.Main) +
           ' -ClientRoot '    + (Q $Fx.Client) +
           ' -Ports ' + ($TESTPORTS -join ',') +
           ' -CaptureFilter ' + (Q 'capture_selftest_*') +
           ' -JobTag '        + (Q 'SELFTEST_teardown')
    if ($UseSalvage) { $cmd = $cmd + ' -Salvage' }
    $cmd = $cmd + '; if ($LASTEXITCODE -eq $null) { exit 0 }; exit $LASTEXITCODE'
    $out  = & powershell.exe -NoProfile -ExecutionPolicy Bypass -Command $cmd 2>&1
    $code = $LASTEXITCODE
    return New-Object PSObject -Property @{ Out = ($out | Out-String); Code = $code }
}

function Get-SalvageReceipt($Fx) {
    return @(Get-ChildItem -LiteralPath $Fx.Outbox -Filter 'SALVAGE_*' -File -ErrorAction SilentlyContinue |
             Where-Object { $_.Name -notlike '*_console_tail_*' })
}
function Get-SalvageTail($Fx) {
    return @(Get-ChildItem -LiteralPath $Fx.Outbox -Filter 'SALVAGE_*_console_tail_*' -File -ErrorAction SilentlyContinue)
}

# ===========================================================================
# T1 - fresh round, no -Salvage -> the normal path, untouched
# ===========================================================================
Write-Host '--- T1: fresh round, no -Salvage (default behaviour must be unchanged) ---'
$f1 = New-RoundFixture 'T1' $FRESH_MIN 1 $true $false
$r1 = Invoke-Template $f1 $false
$log1 = Join-Path $f1.Outbox 'SELFTEST_teardown.utf8.txt'
$txt1 = ''
if (Test-Path -LiteralPath $log1) { $txt1 = Get-Content -Raw -LiteralPath $log1 }
Check 'T1 exit code is 0'                       ($r1.Code -eq 0) ("exit=" + $r1.Code)
Check 'T1 normal receipt written'               (Test-Path -LiteralPath $log1) 'no job log in outbox'
Check 'T1 receipt says TEARDOWN DONE'           ($txt1 -match 'TEARDOWN DONE') 'log has no DONE line'
Check 'T1 wrote NO salvage file'                ((Get-SalvageReceipt $f1).Count -eq 0) 'a salvage receipt appeared without -Salvage'
Check 'T1 did not claim SALVAGE mode'           ($txt1 -notmatch 'MODE = SALVAGE') ''
Write-Host ''

# ===========================================================================
# T2 - stale round, no -Salvage -> exit 12 and nothing else
# ===========================================================================
Write-Host '--- T2: stale round, no -Salvage (the refusal must survive this change) ---'
# T2a: the info FILE itself is old - the first of the two stale checks.
$f2 = New-RoundFixture 'T2a' $STALE_MIN $STALE_MIN $true $true
$r2 = Invoke-Template $f2 $false
$log2 = Join-Path $f2.Outbox 'SELFTEST_teardown.utf8.txt'
$txt2 = ''
if (Test-Path -LiteralPath $log2) { $txt2 = Get-Content -Raw -LiteralPath $log2 }
Check 'T2a exit code is 12'                     ($r2.Code -eq 12) ("exit=" + $r2.Code)
Check 'T2a refusal is loud (ABORT 12)'          ($txt2 -match 'ABORT\(12\)') ''
Check 'T2a refusal states the age and the limit' ($txt2 -match 'min old \(> 420\)') ''
Check 'T2a no normal receipt (no DONE line)'    ($txt2 -notmatch 'TEARDOWN DONE') 'a stale round produced a normal receipt'
Check 'T2a wrote NO salvage file'               ((Get-SalvageReceipt $f2).Count -eq 0) ''
Check 'T2a points the operator at -Salvage'     ($txt2 -match '-Salvage') 'refusal does not mention the recovery path'

# T2b: the info file was touched recently but the BOOT STAMP is old - this is
# the exact refusal that ate the round of 2026-08-20 ("boot stamp is 185.7 min
# old (> 180) - stale round"). It must still refuse, just later than it used to.
$f2b = New-RoundFixture 'T2b' $STALE_MIN 1 $true $true
$r2b = Invoke-Template $f2b $false
$log2b = Join-Path $f2b.Outbox 'SELFTEST_teardown.utf8.txt'
$txt2b = ''
if (Test-Path -LiteralPath $log2b) { $txt2b = Get-Content -Raw -LiteralPath $log2b }
Check 'T2b exit code is 12'                     ($r2b.Code -eq 12) ("exit=" + $r2b.Code)
Check 'T2b refusal names the stale round'       ($txt2b -match 'stale round') ''
Check 'T2b no normal receipt (no DONE line)'    ($txt2b -notmatch 'TEARDOWN DONE') ''
Check 'T2b wrote NO salvage file'               ((Get-SalvageReceipt $f2b).Count -eq 0) ''

# T2c: the same round at 200 minutes - inside the NEW limit, outside the old
# one. This is the case the old 180 min limit refused for no good reason: a
# normal attended round that simply ran long. It must now go through.
$f2c = New-RoundFixture 'T2c' 200 200 $true $false
$r2c = Invoke-Template $f2c $false
$log2c = Join-Path $f2c.Outbox 'SELFTEST_teardown.utf8.txt'
$txt2c = ''
if (Test-Path -LiteralPath $log2c) { $txt2c = Get-Content -Raw -LiteralPath $log2c }
Check 'T2c a 200-minute round is NOT refused'   ($r2c.Code -eq 0) ("exit=" + $r2c.Code)
Check 'T2c 200-minute round gets a normal receipt' ($txt2c -match 'TEARDOWN DONE') ''
Write-Host ''

# ===========================================================================
# T3 - stale round WITH -Salvage -> a receipt that admits what it is
# ===========================================================================
Write-Host '--- T3: stale round WITH -Salvage (collect, do not refuse) ---'
$f3 = New-RoundFixture 'T3' $STALE_MIN $STALE_MIN $true $true
$dbShaBefore = (Get-FileHash -LiteralPath $f3.RunDb -Algorithm SHA256).Hash.ToUpper()
$dbTimeBefore = (Get-Item -LiteralPath $f3.RunDb).LastWriteTime
$canon3 = Join-Path $f3.Main 'state\pirateforce.sqlite3'
$canonShaBefore = (Get-FileHash -LiteralPath $canon3 -Algorithm SHA256).Hash.ToUpper()
$r3 = Invoke-Template $f3 $true
$rc3 = Get-SalvageReceipt $f3
Check 'T3 exit code is 20 (degraded, not green)' ($r3.Code -eq 20) ("exit=" + $r3.Code)
Check 'T3 exactly one salvage receipt'           ($rc3.Count -eq 1) ("count=" + $rc3.Count)

$body3 = ''
$first3 = ''
$missCount3 = 0
$hasBom3 = $false
if ($rc3.Count -eq 1) {
    $body3  = Get-Content -Raw -LiteralPath $rc3[0].FullName
    $first3 = (Get-Content -LiteralPath $rc3[0].FullName -TotalCount 1)
    $missCount3 = @(Get-Content -LiteralPath $rc3[0].FullName | Where-Object { $_ -like 'MISSING:*' }).Count
    $bytes3 = [System.IO.File]::ReadAllBytes($rc3[0].FullName)
    $hasBom3 = ($bytes3.Length -ge 3 -and $bytes3[0] -eq 0xEF -and $bytes3[1] -eq 0xBB -and $bytes3[2] -eq 0xBF)
}
# ${bom} and not $bom: PowerShell reads "^$bom?SALVAGE" as a drive-qualified
# variable reference and dies at parse time. Round 109, job 176.
$bom = [char]0xFEFF
Check 'T3 SALVAGE marker in the filename'        ($rc3.Count -eq 1 -and $rc3[0].Name -clike 'SALVAGE_*') ''
Check 'T3 SALVAGE marker on the first line'      ([bool]($first3 -cmatch "^${bom}?SALVAGE")) ("first line was: " + $first3)
Check 'T3 receipt is BOM-free'                   (-not $hasBom3) 'Write-Flag emitted a BOM'
Check 'T3 MISSING list is non-empty'             ($missCount3 -ge 1) ("MISSING lines=" + $missCount3)
Check 'T3 missing_items header agrees'           ($body3 -match ('missing_items\s+:\s+' + $missCount3)) ''
Check 'T3 header carries the boot stamp'         ($body3 -match [regex]::Escape($f3.Stamp)) ''
Check 'T3 header carries the real age in minutes' ($body3 -match 'boot_age_at_salvage\s+:\s+\d+') ''
Check 'T3 header says no teardown ever ran'      ($body3 -cmatch 'NO TEARDOWN EVER RAN') ''
Check 'T3 header says evidence is incomplete'    ($body3 -cmatch 'INCOMPLETE') ''
Check 'T3 header says recovered after the fact'  ($body3 -cmatch 'RECOVERED AFTER THE FACT') ''
Check 'T3 receipt is not mistakable for a normal one' ($body3 -notmatch 'TEARDOWN DONE') ''
Check 'T3 console tail was copied out'           ((Get-SalvageTail $f3).Count -eq 1) ''
Check 'T3 traceback count was recovered'         ($body3 -match 'traceback markers = 2') ''
Check 'T3 run-copy DB sha recorded'              ($body3 -match 'sha256 = [0-9A-F]{64}') ''
Check 'T3 salvage did NOT modify the run DB'     (((Get-FileHash -LiteralPath $f3.RunDb -Algorithm SHA256).Hash.ToUpper() -eq $dbShaBefore) -and ((Get-Item -LiteralPath $f3.RunDb).LastWriteTime -eq $dbTimeBefore)) 'the run DB changed'
Check 'T3 salvage did NOT modify the canonical DB' ((Get-FileHash -LiteralPath $canon3 -Algorithm SHA256).Hash.ToUpper() -eq $canonShaBefore) 'canonical fixture changed'
Check 'T3 log says SALVAGE DONE'                 ($r3.Out -match 'SALVAGE DONE') ''
# The template dot-sources TEMPLATE_lock_flag_helpers.ps1 on the salvage path.
# That file ends with a self-test whose last statement is `exit`, guarded by
# `if ($MyInvocation.InvocationName -ne '.')`. If that guard ever stopped
# holding, the salvage would die silently mid-run. Watch the guard hold:
Check 'T3 dot-source ran no self-test of its own' ($r3.Out -notmatch 'FLAG_HELPERS_VERDICT') 'the flag-helper self-test executed during a salvage'
Write-Host ''

# ===========================================================================
# T4 - -Salvage with no console log: degrade, do not fail
# ===========================================================================
Write-Host '--- T4: -Salvage with NO server console log on disk ---'
$f4 = New-RoundFixture 'T4' $STALE_MIN $STALE_MIN $false $true
$r4 = Invoke-Template $f4 $true
$rc4 = Get-SalvageReceipt $f4
$body4 = ''
$missCount4 = 0
if ($rc4.Count -eq 1) {
    $body4 = Get-Content -Raw -LiteralPath $rc4[0].FullName
    $missCount4 = @(Get-Content -LiteralPath $rc4[0].FullName | Where-Object { $_ -like 'MISSING:*' }).Count
}
Check 'T4 exit code is 20 (still produced a receipt)' ($r4.Code -eq 20) ("exit=" + $r4.Code)
Check 'T4 receipt exists despite the missing log'     ($rc4.Count -eq 1) ("count=" + $rc4.Count)
Check 'T4 console log is listed as MISSING'           ($body4 -match 'MISSING: the server console log') ''
Check 'T4 MISSING list is non-empty'                  ($missCount4 -ge 1) ("MISSING lines=" + $missCount4)
Check 'T4 no console tail was invented'               ((Get-SalvageTail $f4).Count -eq 0) 'a tail file appeared with no source log'
Check 'T4 did not abort'                              ($r4.Out -notmatch 'SALVAGE FAILED') ''
Write-Host ''

# ---------------------------------------------------------------------------
# cleanup - only ever inside %TEMP%
# ---------------------------------------------------------------------------
if ($sand.StartsWith($env:TEMP, [System.StringComparison]::OrdinalIgnoreCase)) {
    Remove-Item -LiteralPath $sand -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ('sandbox removed: ' + $sand)
} else {
    Write-Host ('sandbox NOT removed (outside TEMP): ' + $sand)
}

Write-Host ''
if ($fail -ne 0) {
    Write-Host 'SELFTEST_TEARDOWN_SALVAGE_VERDICT=FAIL'
    exit 1
}
Write-Host 'SELFTEST_TEARDOWN_SALVAGE_VERDICT=PASS'
exit 0
