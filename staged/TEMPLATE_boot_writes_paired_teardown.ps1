# ============================================================================
# TEMPLATE_boot_writes_paired_teardown.ps1 - the boot job stages its own
# teardown at the moment it succeeds. ASCII ONLY.
#
# WHY THIS FILE EXISTS
# --------------------
# On 2026-08-20 an attended round ran for more than three hours and then simply
# stopped, because the human driving it walked away. Nobody ran the teardown.
# The whole wire layer of that round has no evidence at all: no server console
# tail, no post-run DB snapshot, no traceback count. The screenshots survived
# only by luck. Panya's reaction was "it was my fault for not closing the
# round". The chief disagrees on the record: a process that depends on a human
# remembering a cleanup step is a process that will fail eventually, and the
# only question is which round it eats. This is a process fix, not a discipline
# fix.
#
# The remembering was never the hard part - the FILLING IN was. Closing a round
# used to mean: copy TEMPLATE_teardown_generic.ps1, rename it to the right job
# number, set the CaptureFilter for this scenario, check it against the boot
# job, then copy it into inbox\. Five decisions at the exact moment when the
# operator is tired and the interesting part of the work is already over.
#
# So the boot job writes the teardown itself, while it still knows everything:
# its own job number, the boot stamp, the scenario, the run-copy DB path and
# the capture filter all go into a ready-to-run file in staged\ at boot time.
# Closing the round is then ONE action with nothing to remember and nothing to
# fill in:
#
#     copy staged\127_gt016_teardown.ps1  ->  inbox\
#
# WHAT IT DELIBERATELY DOES NOT DO
#   - It NEVER puts anything into inbox\. inbox\ is the execute queue; a boot
#     job that could enqueue its own teardown could tear down its own round
#     mid-flight. Staging is safe; enqueueing is the operator's decision.
#   - It never overwrites an existing file. If the target name is taken it
#     writes <name>_<stamp>.ps1 instead and returns THAT path. Nothing in this
#     project deletes or overwrites a job somebody may have hand-edited.
#   - It refuses to emit a file containing a non-ASCII byte (see ASCII GATE).
#
# USAGE - the three lines an existing boot job adds, right after it has proved
# the server is up and has written its info file:
#
#     . 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\TEMPLATE_boot_writes_paired_teardown.ps1'
#     $td = Write-PairedTeardown -Stamp $stamp -Scenario $scenario -RunDb $runDb
#     W "paired teardown staged: $td (copy it into inbox\ to close the round)"
#
# Everything else is derived from the boot job's own filename: 126_gt016_boot
# gives job number 126, round id gt016, teardown 127_gt016_teardown, info-file
# prefix '126_' and capture filter 'capture_gt016_*'. Override any of them with
# the explicit parameters if a round does not follow the convention.
# ============================================================================

# Path of THIS file, captured at dot-source time. Used only to skip our own
# frame when looking up the caller in the call stack.
$PairedTeardownHelperPath = ''
if ($MyInvocation.MyCommand.Path) { $PairedTeardownHelperPath = $MyInvocation.MyCommand.Path }

function Write-PairedTeardown {
    param(
        # Boot stamp, yyyyMMdd_HHmmss - the same $stamp the boot job put in the
        # info file. This is what pairs the teardown to THIS round.
        [Parameter(Mandatory = $true)][string] $Stamp,
        [string] $Scenario       = '',
        [string] $RunDb          = '',
        # All of these are derived from the boot job's filename when left empty.
        [string] $BootScriptPath = '',
        [string] $GtId           = '',
        [string] $InfoPrefix     = '',
        [string] $CaptureFilter  = '',
        [string] $TeardownName   = '',
        [string] $BridgeRoot     = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
    )

    $staged = Join-Path $BridgeRoot 'staged'
    $tpl    = Join-Path $staged 'TEMPLATE_teardown_generic.ps1'

    # ---- 0) who called us -------------------------------------------------
    $bootScript = $BootScriptPath
    if ([string]::IsNullOrWhiteSpace($bootScript)) {
        foreach ($frame in @(Get-PSCallStack)) {
            $sn = $frame.ScriptName
            if ($sn -and $sn -ne $PairedTeardownHelperPath) { $bootScript = $sn; break }
        }
    }
    $bootBase = 'boot'
    if ($bootScript) { $bootBase = [System.IO.Path]::GetFileNameWithoutExtension($bootScript) }

    # ---- 1) derive the names ---------------------------------------------
    # String CONCATENATION, never "$var_suffix": PowerShell would read the
    # underscore as part of the variable name, and "$var:" as a drive-qualified
    # reference. Round 109 lost an evening to exactly that class of parse.
    $numTxt = ''
    $tdNum  = ''
    if ($bootBase -match '^(\d+)_') {
        $numTxt = $matches[1]
        $tdNum  = ([int]$numTxt + 1).ToString('D' + $numTxt.Length)
    }
    if ([string]::IsNullOrWhiteSpace($GtId)) {
        if ($bootBase -match '_(gt\d+)_') { $GtId = $matches[1] }
        elseif ($bootBase -match '_([a-z0-9]+)_boot$') { $GtId = $matches[1] }
        else { $GtId = 'round' }
    }
    if ([string]::IsNullOrWhiteSpace($InfoPrefix) -and $numTxt) { $InfoPrefix = $numTxt + '_' }
    if ([string]::IsNullOrWhiteSpace($CaptureFilter)) { $CaptureFilter = 'capture_' + $GtId + '_*' }
    if ([string]::IsNullOrWhiteSpace($TeardownName)) {
        if ($tdNum) { $TeardownName = $tdNum + '_' + $GtId + '_teardown' }
        else        { $TeardownName = $GtId + '_teardown_' + $Stamp }
    }

    # ---- 2) ASCII GATE ----------------------------------------------------
    # These scripts run on Windows PowerShell 5.1 with console codepage cp874.
    # One non-cp874 character printed to the console turns the project gate red;
    # it has happened before. A generated job is exactly the kind of file nobody
    # re-reads, so it must never be the thing that carries a stray byte. If any
    # value we would embed is not pure ASCII we write NOTHING and say so: the
    # round can still be closed by hand with TEMPLATE_teardown_generic.ps1,
    # which is a worse day than usual but not a red gate.
    foreach ($pair in @(@('Stamp', $Stamp), @('Scenario', $Scenario), @('RunDb', $RunDb),
                        @('GtId', $GtId), @('InfoPrefix', $InfoPrefix),
                        @('CaptureFilter', $CaptureFilter), @('TeardownName', $TeardownName),
                        @('BridgeRoot', $BridgeRoot))) {
        $v = [string]$pair[1]
        foreach ($ch in $v.ToCharArray()) {
            if ([int]$ch -gt 126 -or ([int]$ch -lt 32 -and [int]$ch -ne 9)) {
                Write-Host "PAIRED TEARDOWN NOT WRITTEN: parameter $($pair[0]) contains a non-ASCII character (U+$('{0:X4}' -f [int]$ch)). Refusing to generate a job that could print it to a cp874 console."
                return $null
            }
        }
    }

    # ---- 3) target path - never overwrite ---------------------------------
    if (-not (Test-Path -LiteralPath $staged)) {
        New-Item -ItemType Directory -Path $staged -ErrorAction SilentlyContinue | Out-Null
    }
    $target = Join-Path $staged ($TeardownName + '.ps1')
    if (Test-Path -LiteralPath $target) {
        $target = Join-Path $staged ($TeardownName + '_' + $Stamp + '.ps1')
        Write-Host "paired teardown: $($TeardownName).ps1 already exists - writing $(Split-Path -Leaf $target) instead (nothing is ever overwritten)"
    }

    # ---- 4) the generated job --------------------------------------------
    # Single-quoted literals, with any embedded quote doubled, so a path with
    # spaces or an apostrophe survives verbatim.
    function Esc($s) { "'" + ([string]$s).Replace("'", "''") + "'" }
    $now = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

    # The argument list of the generated job, built as pairs so that the last
    # element gets no trailing comma. PowerShell rejects @( 'a', ) outright, and
    # a generated file that does not parse is worse than no generated file.
    $pairs = New-Object System.Collections.ArrayList
    $null = $pairs.Add("'-JobTag',           " + (Esc $TeardownName))
    $null = $pairs.Add("'-ExpectBootStamp',  " + (Esc $Stamp))
    $null = $pairs.Add("'-CaptureFilter',    " + (Esc $CaptureFilter))
    if ($InfoPrefix) { $null = $pairs.Add("'-ExpectInfoPrefix', " + (Esc $InfoPrefix)) }
    $pargsLines = @()
    for ($i = 0; $i -lt $pairs.Count; $i++) {
        $sep = ','
        if ($i -eq ($pairs.Count - 1)) { $sep = '' }
        $pargsLines += ('    ' + $pairs[$i] + $sep)
    }

    $lines = @(
        '# ==========================================================================',
        '# AUTO-GENERATED PAIRED TEARDOWN - do not hand-edit; re-boot to regenerate.',
        '#',
        '# round      : ' + $GtId,
        '# boot job   : ' + $bootBase + '.ps1',
        '# boot stamp : ' + $Stamp,
        '# scenario   : ' + $(if ($Scenario) { $Scenario } else { '(none declared)' }),
        '# run-copy DB: ' + $(if ($RunDb) { $RunDb } else { '(none declared)' }),
        '# generated  : ' + $now + ' by TEMPLATE_boot_writes_paired_teardown.ps1',
        '#',
        '# TO CLOSE THIS ROUND: copy this file into pf_bridge\inbox\. That is all.',
        '# Nothing to rename, nothing to fill in, nothing to remember.',
        '#',
        '# If the round already went cold and you only want the evidence that is',
        '# still on disk, run this file by hand with -Salvage. It will collect and',
        '# never kill. See HOWTO_SALVAGE_A_DEAD_ROUND.md.',
        '# ==========================================================================',
        '',
        'param([switch] $Salvage)',
        '',
        '$ErrorActionPreference = ''Continue''',
        '$ProgressPreference    = ''SilentlyContinue''',
        '',
        '$tpl       = ' + (Esc $tpl),
        '$bootStamp = ' + (Esc $Stamp),
        '$runDb     = ' + (Esc $RunDb),
        '$scenario  = ' + (Esc $Scenario),
        '$jobTag    = ' + (Esc $TeardownName),
        '',
        'Write-Host ("=== paired teardown " + $jobTag + " ===")',
        'Write-Host ("boot stamp : " + $bootStamp)',
        'Write-Host ("run DB     : " + $runDb)',
        'Write-Host ("scenario   : " + $scenario)',
        'if ($Salvage) { Write-Host ''mode       : SALVAGE (collect only - nothing will be signalled)'' }',
        '',
        'if (-not (Test-Path -LiteralPath $tpl)) {',
        '    Write-Host ("ABORT: teardown template missing: " + $tpl)',
        '    exit 30',
        '}',
        '',
        '# -ExpectBootStamp is the pairing guarantee: this file was written for ONE',
        '# round, and the template refuses (exit 12) if the newest info file in',
        '# outbox belongs to a different one. That is the job-145 failure closed by',
        '# construction rather than by the operator noticing.',
        '$pargs = @(',
        '    ''-NoProfile'', ''-ExecutionPolicy'', ''Bypass'', ''-File'', $tpl,'
    )
    $lines += $pargsLines
    $lines += @(
        ')',
        'if ($Salvage) { $pargs += ''-Salvage'' }',
        '',
        '& powershell.exe @pargs',
        '$code = $LASTEXITCODE',
        'Write-Host ("teardown template exit = " + $code)',
        'if ($code -eq 20) { Write-Host ''SALVAGE receipt written - this round is DEGRADED, not green.'' }',
        'exit $code'
    )

    # ---- 5) write it, BOM-free -------------------------------------------
    # Round 109: Out-File -Encoding utf8 on PowerShell 5.1 prepends a BOM. A BOM
    # at the top of a .ps1 is tolerated by the engine, but this project has been
    # bitten once by a BOM it did not expect, so: WriteAllLines with an explicit
    # UTF8Encoding($false). The $false IS the fix.
    #
    # This is the same body as Write-Flag in staged\TEMPLATE_lock_flag_helpers.ps1
    # and it is written out here rather than dot-sourced ON PURPOSE. Dot-sourcing
    # runs the other file's top-level statements in this scope, and that file
    # ends with a self-test whose last statement is `exit`; it is guarded, but
    # this function is called from a BOOT job with a live server and a live
    # client, and nothing in this project executes that path often enough to
    # notice if the guard ever stopped holding. What round 109 forbids
    # re-deriving is the BOM-tolerant CHECK (Test-FlagHeld), which is subtle and
    # which this file does not use at all. A one-line writer on a critical path
    # is a different trade.
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($target, $lines, $enc)
    Write-Host ("paired teardown staged: " + $target)
    return $target
}
