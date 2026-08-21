# ============================================================================
# SELFTEST_boot_paired_teardown.ps1 - run the REAL paired-teardown generator
# and watch every one of its gates decide. ASCII ONLY.
#
# WHY THIS FILE EXISTS
# --------------------
# Round 109 wrote the lesson down: "a template shipped without ever being
# executed explodes on the day it matters most". On 2026-08-21 the project paid
# for the same lesson a third time, and this time it was the guard against
# silent round-death that was itself silently dead.
#
# staged\TEMPLATE_boot_writes_paired_teardown.ps1 shipped at 21:59 on 08-20. It
# was used for real about three hours later, in an UNATTENDED round with nobody
# awake to notice (job 949, GT-039). The teardown it generated did not parse:
#
#     At ...\inbox\950_gt039_teardown.ps1:16 char:12
#     + 2026-08-21 02:05:45
#     Unexpected token '02:05:45' in expression or statement.
#     === exit 1 ===
#
# The cause was operator precedence: ',' binds tighter than '+' in PowerShell,
# so every "'# key : ' + $value," element of the emitter's array was ARRAY
# concatenation, not string concatenation, and array concatenation flattens.
# Each key and its value became two elements, so WriteAllLines put them on two
# lines, so the values landed at column 0 with no '#' in front of them.
#
# Nothing in the project would have caught that except running the generator
# once and parsing what came out. That is exactly what T1 below does, and it is
# one line of code. The round survived only because the tester noticed exit 1
# and closed the round by hand with TEMPLATE_teardown_generic.ps1 (job 951).
#
# WHAT IT COVERS
#   T1  a normal boot-job name produces a file that PARSES, asserted with
#       [scriptblock]::Create - the exact check that would have caught it - and
#       the file is BOM-free and pure ASCII
#   T2  the generated teardown carries the right job number, boot stamp,
#       scenario and run-DB path, each on ONE line with its key; no value is on
#       a bare line (the job-950 shape); and the embedded -ExpectBootStamp
#       really does make TEMPLATE_teardown_generic REFUSE (exit 12) an info
#       file from a different round, while accepting the matching one
#   T3  hostile metadata - a value with a space, a colon, a single quote, a
#       double quote, a $(...) and a backtick is ACCEPTED, PARSES, and comes
#       back out byte-identical WITHOUT the injected text ever executing; the
#       same value plus a newline (or a CR) is REFUSED and no file is written
#   T4  the generator writes nothing into inbox\, ever - neither the sandbox
#       inbox nor the real one, and a -TeardownName that tries to path its way
#       into inbox\ is refused by name
#   T5  a deliberately corrupted buffer is REFUSED rather than written:
#       T5a  a MUTANT of the real generator with the job-950 precedence bug
#            put back into the header emitter -> refused, nothing on disk
#       T5b  the same mutant with the header guard knocked out, so the refusal
#            has to come from the D2 PARSE GATE itself -> refused, nothing on
#            disk (this is what proves the parse gate is actually wired in)
#       T5c  Test-PairedTeardownParses called directly: it ACCEPTS the real
#            generated text and REFUSES the job-950 corruption of that same
#            text. A gate that accepts everything is not a gate.
#
# SAFETY - what this self-test can and cannot touch
#   - Everything it writes goes under %TEMP%. The real pf_bridge staged\,
#     inbox\ and outbox\ are never written; inbox\ is only ever COUNTED, and
#     T4 asserts the count did not change.
#   - It never boots a server, never launches a client, never touches the
#     canonical DB and never runs git.
#   - T2 runs the real TEMPLATE_teardown_generic.ps1 against a fixture whose
#     roots are all inside %TEMP% and whose watched ports are 59188/59189, not
#     10188/10189. It refuses to start if anything is listening on those. The
#     three pids in the fixture are this self-test's OWN pid: that pid exists
#     (so the probe path is exercised) but its process name is 'powershell', so
#     the template's identity guards - console must be 'py', client must be
#     'GameClient*' - can never pass and nothing can ever be signalled or
#     stopped. -ForceKillIfPortsStuck is not passed. This is the same harness
#     SELFTEST_teardown_salvage.ps1 already uses.
#   - The fixture deliberately omits the 'rundb' key so the normal path does
#     not shell out to `py -3` against a fake database.
#   - T3 evaluates ONLY the five metadata assignment lines of the generated
#     file, in a child scope, never the whole file. If the injection had
#     escaped its quotes, that is where it would fire, and the test would see
#     the environment marker it sets.
#
# RUN IT
#   powershell -NoProfile -ExecutionPolicy Bypass -File staged\SELFTEST_boot_paired_teardown.ps1
# Last line is SELFTEST_BOOT_PAIRED_TEARDOWN_VERDICT=PASS or =FAIL; exit 1 on FAIL.
# ============================================================================

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$here   = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($here)) { $here = Join-Path $bridge 'staged' }
$gen   = Join-Path $here 'TEMPLATE_boot_writes_paired_teardown.ps1'
$tdTpl = Join-Path $here 'TEMPLATE_teardown_generic.ps1'
$flagH = Join-Path $here 'TEMPLATE_lock_flag_helpers.ps1'
if (-not (Test-Path -LiteralPath $gen))   { $gen   = Join-Path $bridge 'staged\TEMPLATE_boot_writes_paired_teardown.ps1' }
if (-not (Test-Path -LiteralPath $tdTpl)) { $tdTpl = Join-Path $bridge 'staged\TEMPLATE_teardown_generic.ps1' }
if (-not (Test-Path -LiteralPath $flagH)) { $flagH = Join-Path $bridge 'staged\TEMPLATE_lock_flag_helpers.ps1' }

$TESTPORTS = @(59188, 59189)
$STAMP     = '20260821_020540'
$BOOTJOB   = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\done\949_gt039_boot.ps1'
$SCEN      = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\scenarios\npc_hp_link_hypothesis_target_sweep.json'
$RUNDB     = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\state\pirateforce_gt039_20260821_020540.sqlite3'
$INJMARK   = 'PF_PAIRED_SELFTEST_INJECTED'

$fail = 0
function Check($label, $ok, $detail) {
    $verdict = 'FAIL'
    if ($ok) { $verdict = 'PASS' } else { $script:fail = 1 }
    $line = ('{0,-62} : {1}' -f $label, $verdict)
    if (-not $ok -and $detail) { $line = $line + '   <- ' + $detail }
    Write-Host $line
}
function Bail($msg) {
    Write-Host ('ABORT: ' + $msg)
    Write-Host 'SELFTEST_BOOT_PAIRED_TEARDOWN_VERDICT=FAIL'
    exit 1
}
function ParsesOk($text) {
    # The independent copy of the check. T1 must not be able to pass just
    # because the function under test says so.
    try { $null = [scriptblock]::Create([string]$text); return $true }
    catch { return $false }
}
function ParseErr($text) {
    try { $null = [scriptblock]::Create([string]$text); return '' }
    catch { return [string]$_.Exception.Message }
}

Write-Host '=== SELFTEST boot-writes-paired-teardown ==='
Write-Host ('time      : ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
Write-Host ('generator : ' + $gen)
Write-Host ('teardown  : ' + $tdTpl)

if (-not (Test-Path -LiteralPath $gen))   { Bail 'the generator template was not found - nothing to test' }
if (-not (Test-Path -LiteralPath $tdTpl)) { Bail 'TEMPLATE_teardown_generic.ps1 was not found - T2 cannot run' }

$busy = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
          Where-Object { $TESTPORTS -contains [int]$_.LocalPort })
if ($busy.Count -gt 0) { Bail ('something is listening on the self-test ports ' + ($TESTPORTS -join ',') + ' - refusing to run') }

# The real inbox is only ever counted, never written. T4 compares the two.
$realInbox = Join-Path $bridge 'inbox'
$realInboxBefore = -1
if (Test-Path -LiteralPath $realInbox) {
    $realInboxBefore = @(Get-ChildItem -LiteralPath $realInbox -File -ErrorAction SilentlyContinue).Count
}
Write-Host ('real inbox file count (before) : ' + $realInboxBefore)

$sand = Join-Path $env:TEMP ('pf_paired_selftest_' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $sand -Force | Out-Null
Write-Host ('sandbox   : ' + $sand)
Write-Host ''

# A sandbox bridge root: staged\ is where the generator is allowed to write,
# inbox\ exists precisely so that T4 can prove it stays empty.
function New-SandBridge($name) {
    $b  = Join-Path $sand $name
    New-Item -ItemType Directory -Path (Join-Path $b 'staged') -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $b 'inbox')  -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $b 'outbox') -Force | Out-Null
    return $b
}
function StagedPs1($b) {
    return @(Get-ChildItem -LiteralPath (Join-Path $b 'staged') -Filter '*.ps1' -File -ErrorAction SilentlyContinue)
}
function InboxCount($b) {
    return @(Get-ChildItem -LiteralPath (Join-Path $b 'inbox') -File -Recurse -ErrorAction SilentlyContinue).Count
}

# Dot-source the REAL generator. This only defines two functions and one
# variable; it starts nothing and writes nothing.
. $gen
if (-not (Get-Command -Name 'Write-PairedTeardown' -ErrorAction SilentlyContinue)) {
    Bail 'Write-PairedTeardown was not defined by dot-sourcing the template'
}
if (-not (Get-Command -Name 'Test-PairedTeardownParses' -ErrorAction SilentlyContinue)) {
    Bail 'Test-PairedTeardownParses was not defined - the D2 parse gate is missing from the template'
}

# ===========================================================================
# T1 - a normal boot-job name produces a file that PARSES
# ===========================================================================
Write-Host '--- T1: normal boot job name -> the generated teardown must parse ---'
$b1 = New-SandBridge 'T1'
$r1 = Write-PairedTeardown -NoThrow -Stamp $STAMP -Scenario $SCEN -RunDb $RUNDB `
                           -BootScriptPath $BOOTJOB -BridgeRoot $b1
$f1 = ''
if ($r1) { $f1 = [string]$r1 }
$txt1   = ''
$L1     = @()
$bytes1 = @()
if ($f1 -and (Test-Path -LiteralPath $f1)) {
    $txt1   = Get-Content -Raw -LiteralPath $f1
    $L1     = @(Get-Content -LiteralPath $f1)
    $bytes1 = [System.IO.File]::ReadAllBytes($f1)
}
$expName1 = '950_gt039_teardown.ps1'
$leaf1    = '(no file)'
if ($f1) { $leaf1 = [string](Split-Path -Leaf $f1) }
$nonAscii1 = 0
foreach ($by in $bytes1) { if ([int]$by -ge 128) { $nonAscii1++ } }
$hasBom1 = ($bytes1.Count -ge 3 -and $bytes1[0] -eq 0xEF -and $bytes1[1] -eq 0xBB -and $bytes1[2] -eq 0xBF)

Check 'T1 generator returned a path'                    ($f1 -ne '') 'returned null - see the refusal banner above'
Check 'T1 the file exists'                              ($f1 -ne '' -and (Test-Path -LiteralPath $f1)) 'no file on disk'
Check 'T1 named from the boot job number (950_gt039)'   ($leaf1 -ceq $expName1) ('got ' + $leaf1)
Check 'T1 the generated teardown PARSES'                (ParsesOk $txt1) (ParseErr $txt1)
Check 'T1 the generated teardown has no BOM'            (-not $hasBom1) 'BOM at offset 0'
Check 'T1 the generated teardown is pure ASCII'         ($nonAscii1 -eq 0) ('bytes >= 0x80 : ' + $nonAscii1)
Check 'T1 exactly one file was staged'                  ((StagedPs1 $b1).Count -eq 1) ('count=' + (StagedPs1 $b1).Count)
Write-Host ''

# ===========================================================================
# T2 - the right values, on the right lines, and a stamp that really refuses
# ===========================================================================
Write-Host '--- T2: metadata is correct, on ONE line, and the stamp is enforced ---'
Check 'T2 round id on its comment line'      ($L1 -ccontains '# round      : gt039') 'missing or split'
Check 'T2 boot job on its comment line'      ($L1 -ccontains '# boot job   : 949_gt039_boot.ps1') 'missing or split'
Check 'T2 boot stamp on its comment line'    ($L1 -ccontains ('# boot stamp : ' + $STAMP)) 'missing or split'
Check 'T2 scenario on its comment line'      ($L1 -ccontains ('# scenario   : ' + $SCEN)) 'missing or split'
Check 'T2 run-copy DB on its comment line'   ($L1 -ccontains ('# run-copy DB: ' + $RUNDB)) 'missing or split'
Check 'T2 bootStamp assigned as a literal'   ($L1 -ccontains ('$bootStamp = ' + "'" + $STAMP + "'")) 'missing or split'
Check 'T2 runDb assigned as a literal'       ($L1 -ccontains ('$runDb     = ' + "'" + $RUNDB + "'")) 'missing or split'
Check 'T2 scenario assigned as a literal'    ($L1 -ccontains ('$scenario  = ' + "'" + $SCEN + "'")) 'missing or split'
Check 'T2 -ExpectBootStamp carries the stamp' ($L1 -ccontains ("    '-ExpectBootStamp',  '" + $STAMP + "',")) 'missing or split'
Check 'T2 -ExpectInfoPrefix carries 949_'    ($L1 -ccontains "    '-ExpectInfoPrefix', '949_'") 'missing or split'
Check 'T2 -CaptureFilter carries gt039'      ($L1 -ccontains "    '-CaptureFilter',    'capture_gt039_*',") 'missing or split'

# The job-950 shape, stated as an assertion: no metadata value may appear on a
# line of its own. This is the single check that would have failed on 08-21.
$bare = @($L1 | Where-Object { $_.Trim() -ceq $STAMP -or $_.Trim() -ceq $SCEN -or $_.Trim() -ceq $RUNDB -or $_.Trim() -ceq 'gt039' })
Check 'T2 no metadata value sits on a bare line (job-950)' ($bare.Count -eq 0) ('bare value lines: ' + $bare.Count)

# every header line is a comment
$hdrEnd = -1
for ($i = 0; $i -lt $L1.Count; $i++) { if ($L1[$i] -like '# ====*') { $hdrEnd = $i } }
$hdrBad = 0
if ($hdrEnd -gt 0) {
    for ($i = 0; $i -le $hdrEnd; $i++) { if (-not ([string]$L1[$i]).StartsWith('#')) { $hdrBad++ } }
}
Check 'T2 every generated header line is a comment' ($hdrEnd -gt 0 -and $hdrBad -eq 0) ('non-comment header lines: ' + $hdrBad)

# --- and now the part that cannot be faked: run the real teardown template ---
function New-RoundFixture($name, $bootAgeMinutes) {
    $root = Join-Path $sand $name
    $b    = Join-Path $root 'bridge'
    $ob   = Join-Path $b 'outbox'
    $st   = Join-Path $b 'staged'
    $m    = Join-Path $root 'main'
    $ms   = Join-Path $m 'state'
    $c    = Join-Path $root 'client'
    New-Item -ItemType Directory -Path $ob, $st, $ms, $c -Force | Out-Null
    if (Test-Path -LiteralPath $flagH) {
        Copy-Item -LiteralPath $flagH -Destination (Join-Path $st 'TEMPLATE_lock_flag_helpers.ps1') -Force
    }
    $bootTime = (Get-Date).AddMinutes(-1 * [double]$bootAgeMinutes)
    $st2      = $bootTime.ToString('yyyyMMdd_HHmmss')
    $canon    = Join-Path $ms 'pirateforce.sqlite3'
    Set-Content -LiteralPath $canon -Value 'selftest fixture - not a real database' -Encoding ascii
    $csha = (Get-FileHash -LiteralPath $canon -Algorithm SHA256).Hash.ToUpper()
    Set-Content -LiteralPath (Join-Path $b 'CANON_SHA.txt') -Value $csha -Encoding ascii
    $cap = Join-Path $c ('capture_selftest_' + $st2)
    New-Item -ItemType Directory -Path $cap -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $cap 'GAME_LIVE.txt') -Value 'selftest wire log line' -Encoding ascii
    Set-Content -LiteralPath (Join-Path $cap 'server_console_live.out.txt') -Encoding ascii -Value @(
        '[FOUNDATION] listener ready',
        '[FOUNDATION] stopped'
    )
    # No 'rundb' key on purpose: the normal path must not shell out to py -3.
    $keys = @(
        ('clientpid=' + $PID),
        ('console=' + $PID),
        ('server=' + $PID),
        ('stamp=' + $st2),
        'title=selftest fixture window'
    )
    $info = Join-Path $ob ('900_client_info_' + $st2 + '.txt')
    $keys | Out-File -FilePath $info -Encoding ascii
    (Get-Item -LiteralPath $info).LastWriteTime = (Get-Date).AddMinutes(-1)
    return New-Object PSObject -Property @{
        Bridge = $b; Outbox = $ob; Main = $m; Client = $c; Stamp = $st2
    }
}

# -Command and not -File: with -File every argument reaches the binder as a
# plain string and '59188,59189' does not convert to [int[]]. Every literal is
# single-quoted, so paths with spaces survive and no double quote is ever put
# on the command line.
function Invoke-Teardown($fx, $expectStamp) {
    function Q($s) { "'" + ([string]$s).Replace("'", "''") + "'" }
    $cmd = '& ' + (Q $tdTpl) +
           ' -BridgeRoot '        + (Q $fx.Bridge) +
           ' -MainRoot '          + (Q $fx.Main) +
           ' -ClientRoot '        + (Q $fx.Client) +
           ' -Ports ' + ($TESTPORTS -join ',') +
           ' -CaptureFilter '     + (Q 'capture_selftest_*') +
           ' -JobTag '            + (Q 'SELFTEST_paired') +
           ' -ExpectInfoPrefix '  + (Q '900_') +
           ' -ExpectBootStamp '   + (Q $expectStamp)
    $cmd = $cmd + '; if ($LASTEXITCODE -eq $null) { exit 0 }; exit $LASTEXITCODE'
    $out  = & powershell.exe -NoProfile -ExecutionPolicy Bypass -Command $cmd 2>&1
    $code = $LASTEXITCODE
    return New-Object PSObject -Property @{ Out = ($out | Out-String); Code = $code }
}

# the stamp the generated file actually carries, read back out of the file
$embedded = ''
foreach ($l in $L1) {
    if ($l -match "^\s*'-ExpectBootStamp',\s*'([^']*)'") { $embedded = $matches[1] }
}
Check 'T2 the embedded stamp is readable and correct' ($embedded -ceq $STAMP) ('read back: ' + $embedded)

$fxA = New-RoundFixture 'T2A' 5
$rA  = Invoke-Teardown $fxA $embedded      # fixture stamp != embedded stamp
Check 'T2 embedded stamp REFUSES a different round (exit 12)' ($rA.Code -eq 12) ('exit=' + $rA.Code)
Check 'T2 and says so by name'             ($rA.Out -match 'DIFFERENT round') 'no DIFFERENT round message'
Check 'T2 the refusal names both stamps'   (($rA.Out -match [regex]::Escape($embedded)) -and ($rA.Out -match [regex]::Escape($fxA.Stamp))) ''

$fxB = New-RoundFixture 'T2B' 5
$rB  = Invoke-Teardown $fxB $fxB.Stamp     # matching stamp - the control
Check 'T2 the SAME check accepts the matching stamp'  ($rB.Code -ne 12) ('exit=' + $rB.Code)
Check 'T2 control: no DIFFERENT round message'        ($rB.Out -notmatch 'DIFFERENT round') ''
Check 'T2 control: the assertion reported OK'         ($rB.Out -match 'boot stamp assertion OK') ''
Write-Host ''

# ===========================================================================
# T3 - hostile metadata: accepted and inert, or refused; never executed
# ===========================================================================
Write-Host '--- T3: hostile metadata ---'
$q  = [char]39   # '
$dq = [char]34   # "
$bt = [char]96   # `
$hostile = 'C:\Program Files\a b' + $q + 's ' + $dq + 'quoted' + $dq +
           ' $(Set-Item Env:' + $INJMARK + ' 1) ' + $bt + 'n at 02:05:45 tail'
Write-Host ('hostile value : ' + $hostile)

# The marker is read and cleared through [Environment] rather than the Env:
# provider: Set-Item Env:X -Value '' is rejected as an empty argument on 5.1,
# and a self-test whose own cleanup throws is a self-test nobody trusts.
[Environment]::SetEnvironmentVariable($INJMARK, $null, 'Process')

$b3 = New-SandBridge 'T3'
$r3 = Write-PairedTeardown -NoThrow -Stamp $STAMP -Scenario $hostile -RunDb $hostile `
                           -BootScriptPath $BOOTJOB -BridgeRoot $b3
$f3   = ''
if ($r3) { $f3 = [string]$r3 }
$txt3 = ''
$L3   = @()
if ($f3 -and (Test-Path -LiteralPath $f3)) {
    $txt3 = Get-Content -Raw -LiteralPath $f3
    $L3   = @(Get-Content -LiteralPath $f3)
}
$accepted3 = ($f3 -ne '')
# The contract is "parses safely OR is refused" - never "produces a file that
# parses and executes the injected text". So a refusal is a legal outcome here,
# as long as it really wrote nothing. It is reported either way, because a
# silent change from accept to refuse is worth somebody's attention.
if ($accepted3) {
    Write-Host '     (hostile-but-ASCII value was ACCEPTED - it must now be provably inert)'
} else {
    Write-Host '     (hostile-but-ASCII value was REFUSED - legal, but it must have written nothing)'
    Check 'T3a a refusal wrote nothing'            ((StagedPs1 $b3).Count -eq 0) ('files staged: ' + (StagedPs1 $b3).Count)
    Check 'T3a a refusal was loud'                 ($global:PairedTeardownRefusal -ne '') 'refused silently'
}
if ($accepted3) {
    Check 'T3a the generated file PARSES'          (ParsesOk $txt3) (ParseErr $txt3)
    Check 'T3a hostile value is on its comment line' ($L3 -ccontains ('# scenario   : ' + $hostile)) 'value split or altered'
    Check 'T3a no bare line carries the value'     (@($L3 | Where-Object { $_.Trim() -ceq $hostile }).Count -eq 0) 'value escaped onto its own line'

    # Evaluate ONLY the five metadata assignments, in a child scope, and read
    # $scenario back. If the injection had escaped its single quotes it would
    # run here and set the environment marker.
    $asg = @($L3 | Where-Object { $_ -match '^\$(tpl|bootStamp|runDb|scenario|jobTag)\s' })
    Check 'T3a all five assignments are single lines' ($asg.Count -eq 5) ('found ' + $asg.Count)
    $sbTxt  = ($asg -join "`r`n") + "`r`n" + '$scenario'
    $got    = ''
    $threw  = ''
    try { $got = [string](& ([scriptblock]::Create($sbTxt))) }
    catch { $threw = [string]$_.Exception.Message }
    $mark = [string][Environment]::GetEnvironmentVariable($INJMARK, 'Process')
    Check 'T3a the assignments evaluate without throwing' ($threw -eq '') $threw
    Check 'T3a the value round-trips byte-identical'      ($got -ceq $hostile) ('got: ' + $got)
    Check 'T3a the injected subexpression DID NOT execute' ($mark -eq '') ('marker was set to: ' + $mark)
}
[Environment]::SetEnvironmentVariable($INJMARK, $null, 'Process')

# the same value with a real line break must be refused outright
$b3n = New-SandBridge 'T3NL'
$hostileNL = $hostile + [char]10 + 'Write-Host PWNED'
$r3n = Write-PairedTeardown -NoThrow -Stamp $STAMP -Scenario $hostileNL -RunDb $RUNDB `
                            -BootScriptPath $BOOTJOB -BridgeRoot $b3n
Check 'T3b a value containing LF is REFUSED'      ($r3n -eq $null) 'a file was produced from a value with a newline in it'
Check 'T3b nothing was written for the LF value'  ((StagedPs1 $b3n).Count -eq 0) ('files staged: ' + (StagedPs1 $b3n).Count)

$b3c = New-SandBridge 'T3CR'
$hostileCR = $hostile + [char]13 + 'Write-Host PWNED'
$r3c = Write-PairedTeardown -NoThrow -Stamp $STAMP -Scenario $hostileCR -RunDb $RUNDB `
                            -BootScriptPath $BOOTJOB -BridgeRoot $b3c
Check 'T3c a value containing CR is REFUSED'      ($r3c -eq $null) 'a file was produced from a value with a CR in it'
Check 'T3c nothing was written for the CR value'  ((StagedPs1 $b3c).Count -eq 0) ('files staged: ' + (StagedPs1 $b3c).Count)

$b3u = New-SandBridge 'T3NONASCII'
$r3u = Write-PairedTeardown -NoThrow -Stamp $STAMP -Scenario ('scenario ' + [char]0x0E01) -RunDb $RUNDB `
                            -BootScriptPath $BOOTJOB -BridgeRoot $b3u
Check 'T3d a non-ASCII value is REFUSED'          ($r3u -eq $null) 'a non-ASCII value reached the disk'
Check 'T3d nothing was written for it'            ((StagedPs1 $b3u).Count -eq 0) ('files staged: ' + (StagedPs1 $b3u).Count)
Write-Host ''

# ===========================================================================
# T4 - nothing, ever, reaches inbox\
# ===========================================================================
Write-Host '--- T4: inbox stays empty ---'
$b4 = New-SandBridge 'T4'
$r4a = Write-PairedTeardown -NoThrow -Stamp $STAMP -Scenario $SCEN -RunDb $RUNDB `
                            -BootScriptPath $BOOTJOB -BridgeRoot $b4 `
                            -TeardownName '..\..\inbox\evil'
Check 'T4 a path-shaped -TeardownName is REFUSED' ($r4a -eq $null) 'the generator accepted a name that is a path'
Check 'T4 the refusal names TeardownName'         ($global:PairedTeardownRefusal -match 'TeardownName') ('refusal: ' + $global:PairedTeardownRefusal)

$r4b = Write-PairedTeardown -NoThrow -Stamp $STAMP -Scenario $SCEN -RunDb $RUNDB `
                            -BootScriptPath $BOOTJOB -BridgeRoot $b4 `
                            -TeardownName '../../inbox/evil'
Check 'T4 the forward-slash variant is REFUSED'   ($r4b -eq $null) 'the generator accepted a forward-slash path'

foreach ($bx in @($b1, $b3, $b3n, $b3c, $b3u, $b4)) {
    $n = InboxCount $bx
    Check ('T4 sandbox inbox empty: ' + (Split-Path -Leaf $bx)) ($n -eq 0) ('files: ' + $n)
}
$realInboxAfter = -1
if (Test-Path -LiteralPath $realInbox) {
    $realInboxAfter = @(Get-ChildItem -LiteralPath $realInbox -File -ErrorAction SilentlyContinue).Count
}
Check 'T4 the REAL pf_bridge inbox is untouched' ($realInboxAfter -eq $realInboxBefore) ('before=' + $realInboxBefore + ' after=' + $realInboxAfter)
Write-Host ''

# ===========================================================================
# T5 - a corrupted buffer is REFUSED, not written
# ===========================================================================
Write-Host '--- T5: corruption is refused, not written ---'

# Build two MUTANTS of the real generator inside %TEMP%. Mutation testing: if
# the gates are real, putting the 2026-08-21 defect back must make them fire.
$mutDir = Join-Path $sand 'mutants'
New-Item -ItemType Directory -Path $mutDir -Force | Out-Null
$srcLines = @(Get-Content -LiteralPath $gen)
$idxGen   = -1
$idxGuard = -1
for ($i = 0; $i -lt $srcLines.Count; $i++) {
    $t = ([string]$srcLines[$i]).TrimEnd()
    $c = $t.TrimStart()
    if ($idxGen -lt 0 -and $c.StartsWith('(' + $q + '# generated  : ') -and $c.EndsWith('),')) { $idxGen = $i }
    if ($idxGuard -lt 0 -and $c.Contains('$hl.StartsWith(') -and $c.StartsWith('if (')) { $idxGuard = $i }
}
Check 'T5 mutation anchor: the # generated emitter line was found' ($idxGen -ge 0) 'the emitter was restructured - update this self-test'
Check 'T5 mutation anchor: the header guard line was found'        ($idxGuard -ge 0) 'the header guard was restructured - update this self-test'

function Write-Mutant($path, $lines) {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($path, $lines, $enc)
}
function Indent($s) {
    $t = [string]$s
    return $t.Substring(0, $t.Length - $t.TrimStart().Length)
}
function Run-Mutant($mutPath, $bridgeRoot) {
    $drv = Join-Path $mutDir ((Split-Path -Leaf $mutPath) + '.driver.ps1')
    function Q2($s) { "'" + ([string]$s).Replace("'", "''") + "'" }
    $d = @(
        '$ErrorActionPreference = ' + (Q2 'Continue'),
        '. ' + (Q2 $mutPath),
        '$r = Write-PairedTeardown -NoThrow -Stamp ' + (Q2 $STAMP) +
            ' -Scenario ' + (Q2 $SCEN) + ' -RunDb ' + (Q2 $RUNDB) +
            ' -BootScriptPath ' + (Q2 $BOOTJOB) + ' -BridgeRoot ' + (Q2 $bridgeRoot),
        'if ($r -eq $null) { Write-Host ' + (Q2 'DRIVER_RESULT=NULL') + ' }',
        'else { Write-Host (' + (Q2 'DRIVER_RESULT=') + ' + $r) }',
        'Write-Host (' + (Q2 'DRIVER_REFUSAL=') + ' + ((([string]$global:PairedTeardownRefusal) -split ' + (Q2 '[\r\n]+') + ') -join ' + (Q2 ' | ') + '))',
        'exit 0'
    )
    Write-Mutant $drv $d
    $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $drv 2>&1
    return ($out | Out-String)
}

if ($idxGen -ge 0) {
    # T5a - put the job-950 precedence bug back into the header emitter by
    # removing the parentheses around one element. ',' then binds tighter than
    # '+', the timestamp becomes an element of its own, and the header stops
    # being all-comments.
    $mA = @() + $srcLines
    $tA = ([string]$mA[$idxGen]).TrimEnd()
    $cA = $tA.TrimStart()
    $mA[$idxGen] = (Indent $tA) + $cA.Substring(1, $cA.Length - 3) + ','
    $pA = Join-Path $mutDir 'MUTANT_A_precedence.ps1'
    Write-Mutant $pA $mA
    $bA = New-SandBridge 'T5A'
    $oA = Run-Mutant $pA $bA
    Check 'T5a the job-950 mutant is REFUSED'        ($oA -match 'DRIVER_RESULT=NULL') 'the mutant produced a file'
    Check 'T5a the refusal is loud and named'        ($oA -match 'PAIRED TEARDOWN REFUSED') 'no refusal banner'
    Check 'T5a nothing was written to staged'        ((StagedPs1 $bA).Count -eq 0) ('files staged: ' + (StagedPs1 $bA).Count)
    Check 'T5a nothing was written to inbox'         ((InboxCount $bA) -eq 0) 'inbox not empty'

    if ($idxGuard -ge 0) {
        # T5b - same mutation, plus the header guard knocked out, so the ONLY
        # thing that can stop it now is the D2 parse gate. This is the test
        # that proves the parse gate is wired into the writer, not merely
        # present in the file.
        $mB = @() + $mA
        $mB[$idxGuard] = (Indent ([string]$mB[$idxGuard])) + 'if ($false) {'
        $pB = Join-Path $mutDir 'MUTANT_B_parsegate_only.ps1'
        Write-Mutant $pB $mB
        $bB = New-SandBridge 'T5B'
        $oB = Run-Mutant $pB $bB
        Check 'T5b with the header guard removed, the PARSE GATE refuses' ($oB -match 'DRIVER_RESULT=NULL') 'the parse gate let a broken job through'
        Check 'T5b the refusal says the job does not parse'  ($oB -match 'does not parse') ('output: ' + ($oB -replace '[\r\n]+', ' | '))
        Check 'T5b nothing was written to staged'            ((StagedPs1 $bB).Count -eq 0) ('files staged: ' + (StagedPs1 $bB).Count)
        Check 'T5b nothing was written to inbox'             ((InboxCount $bB) -eq 0) 'inbox not empty'
    }
}

# T5c - call the gate directly. It must accept the real text and refuse the
# job-950 corruption of that same text.
$gOk = Test-PairedTeardownParses -Text $txt1
Check 'T5c the gate ACCEPTS the real generated text' ($gOk.Ok) ([string]$gOk.Error)

$corrupt = @()
$split   = $false
foreach ($l in $L1) {
    if (-not $split -and ([string]$l).StartsWith('# generated  : ')) {
        $rest = ([string]$l).Substring('# generated  : '.Length)
        $ts   = $rest
        $tail = ''
        $cut  = $rest.IndexOf(' by ')
        if ($cut -gt 0) { $ts = $rest.Substring(0, $cut); $tail = $rest.Substring($cut) }
        # byte-faithful to what job 950 actually contained
        $corrupt += '# generated  : '
        $corrupt += $ts
        if ($tail) { $corrupt += $tail }
        $split = $true
    } else {
        $corrupt += [string]$l
    }
}
Check 'T5c the corruption was actually applied' $split 'no # generated line to corrupt'
$gBad = Test-PairedTeardownParses -Text (($corrupt -join "`r`n"))
Check 'T5c the gate REFUSES the job-950 corruption' (-not $gBad.Ok) 'a bare timestamp line was accepted as parseable'
if (-not $gBad.Ok) { Write-Host ('     gate said : ' + $gBad.Error) }
Write-Host ''

# ---------------------------------------------------------------------------
# cleanup - only ever inside %TEMP%
# ---------------------------------------------------------------------------
[Environment]::SetEnvironmentVariable($INJMARK, $null, 'Process')
if ($sand.StartsWith($env:TEMP, [System.StringComparison]::OrdinalIgnoreCase)) {
    Remove-Item -LiteralPath $sand -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ('sandbox removed: ' + $sand)
} else {
    Write-Host ('sandbox NOT removed (outside TEMP): ' + $sand)
}

Write-Host ''
if ($fail -ne 0) {
    Write-Host 'SELFTEST_BOOT_PAIRED_TEARDOWN_VERDICT=FAIL'
    exit 1
}
Write-Host 'SELFTEST_BOOT_PAIRED_TEARDOWN_VERDICT=PASS'
exit 0
