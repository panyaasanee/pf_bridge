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
# ----------------------------------------------------------------------------
# THE 2026-08-21 REGRESSION - READ THIS BEFORE YOU EDIT THE EMITTER
# ----------------------------------------------------------------------------
# This file shipped on 2026-08-20 21:59 and was used for real for the first
# time about three hours later, in an UNATTENDED round (job 949, GT-039). The
# teardown it generated - staged\950_gt039_teardown.ps1 - DID NOT PARSE:
#
#     At ...\inbox\950_gt039_teardown.ps1:16 char:12
#     + 2026-08-21 02:05:45
#     Unexpected token '02:05:45' in expression or statement.
#     === exit 1 ===
#
# The reported symptom was "the metadata values are on a line of their own with
# no leading #". That was true, but it was the symptom, not the cause. The
# cause was an operator-precedence mistake in the emitter, and it corrupted
# EVERY interpolated element of the generated file, not just the comments:
#
#     $lines = @(
#         '#',
#         '# boot stamp : ' + $Stamp,        <- WRONG
#         '# scenario   : ' + $Scenario,     <- WRONG
#         ...
#         '$tpl       = ' + (Esc $tpl),      <- ALSO WRONG
#     )
#
# In PowerShell the comma operator binds TIGHTER than '+'. The parser did not
# read ('# boot stamp : ' + $Stamp) as one element. It read
#
#     ( ... , '# boot stamp : ' ) + ( $Stamp , '# scenario   : ' ) + ( ... )
#
# which is ARRAY concatenation, and array concatenation FLATTENS. So the key
# and its value became two separate ELEMENTS of $lines, and WriteAllLines - one
# element, one line - put them on two separate LINES. Every '+' in the array
# literal split one line into two; the '# boot job   : ' element, which had two
# '+' in it, split into three. The values landed at column 0 with no '#' in
# front of them, and PowerShell read the generated timestamp as code.
#
# THE RULE, and it is now checked twice at run time as well as stated here:
#   * Every element of the $lines array is either a bare literal or is wrapped
#     in ( ). There is no top-level '+' anywhere inside @( ).
#   * Values that go into a COMMENT are forced onto the comment's own line by
#     Cmt() and cannot contain a line break.
#   * Values that go into CODE go through Esc() and become single-quoted
#     literals, where $ ` $( ) and " are all inert.
#
# WHAT ELSE THIS ROUND OF WORK ADDED
#   * PARSE GATE (D2). The text is handed to [scriptblock]::Create BEFORE it is
#     written. If it does not parse, NOTHING is written and the function is
#     loud and non-zero about it. A generated job that cannot parse must never
#     reach the disk. The guard against a round dying silently must not itself
#     be able to die silently - that is the whole point of the file.
#   * HEADER GUARD. Every line of the generated header block must begin with
#     '#'. That is tonight's exact failure, expressed as an assertion.
#   * NEWLINE GUARD. No element of $lines may contain CR or LF.
#   * NAME GUARD. -TeardownName is restricted to [A-Za-z0-9._-] and the
#     resolved output directory must be staged\. A generated job can never be
#     steered into inbox\ (see below) or anywhere else.
#   * A SELF-TEST THAT RUNS THE REAL GENERATOR:
#     staged\SELFTEST_boot_paired_teardown.ps1. Round 109's lesson, paid for a
#     third time tonight: a guard that has never been executed is not a guard.
#
# WHAT IT DELIBERATELY DOES NOT DO
#   - It NEVER puts anything into inbox\. inbox\ is the execute queue; a boot
#     job that could enqueue its own teardown could tear down its own round
#     mid-flight. Staging is safe; enqueueing is the operator's decision.
#   - It never overwrites an existing file. If the target name is taken it
#     writes <name>_<stamp>.ps1 instead and returns THAT path. Nothing in this
#     project deletes or overwrites a job somebody may have hand-edited.
#   - It refuses to emit a file containing a non-ASCII byte (see ASCII GATE).
#   - It refuses to emit a file that does not parse (see PARSE GATE).
#
# USAGE - the three lines an existing boot job adds, right after it has proved
# the server is up and has written its info file:
#
#     . 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\TEMPLATE_boot_writes_paired_teardown.ps1'
#     $td = Write-PairedTeardown -Stamp $stamp -Scenario $scenario -RunDb $runDb
#     W "paired teardown staged: $td (copy it into inbox\ to close the round)"
#
# A refusal is a TERMINATING error by default: it throws, and it sets
# $global:LASTEXITCODE to 41. That is deliberate. A boot job that carries on
# after being told "this round has no teardown" is the 2026-08-20 failure with
# extra steps. If a boot job really must survive it - because the server is
# already up and the round is worth running by hand - it must say so out loud:
#
#     try   { $td = Write-PairedTeardown -Stamp $stamp -Scenario $scenario -RunDb $runDb }
#     catch { W "NO PAIRED TEARDOWN: $($_.Exception.Message)"
#             W 'CLOSE THIS ROUND BY HAND with staged\TEMPLATE_teardown_generic.ps1' }
#
# Callers that want a value instead of an exception pass -NoThrow; they get
# $null back, $global:LASTEXITCODE = 41 and $global:PairedTeardownRefusal set
# to the reason. -NoThrow exists for the self-test and for tooling. It is not
# for boot jobs.
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

# ============================================================================
# THE PARSE GATE (D2)
# ============================================================================
# Deliberately a named, top-level function rather than four lines inline, for
# one reason: the self-test can call it directly and watch it REFUSE a buffer.
# A gate nobody has watched reject something is not a gate - round 109, and
# then tonight, for the same money.
#
# It only parses. It never runs the text, never dot-sources it and never writes
# it anywhere. [scriptblock]::Create compiles; it does not execute.
function Test-PairedTeardownParses {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyString()][string] $Text
    )
    $res = New-Object PSObject -Property @{ Ok = $false; Error = ''; Lines = @() }
    try {
        $null = [scriptblock]::Create($Text)
        $res.Ok = $true
        return $res
    } catch {
        $ex   = $_.Exception
        $msgs = @()
        $lns  = @()
        $errs = $null
        try { $errs = $ex.Errors } catch { $errs = $null }
        if ($errs) {
            foreach ($e in $errs) {
                $ln = 0
                try { $ln = [int]$e.Extent.StartLineNumber } catch { $ln = 0 }
                $lns  += $ln
                $msgs += ('line ' + $ln + ': ' + $e.Message)
            }
        }
        if ($msgs.Count -eq 0) { $msgs = @([string]$ex.Message) }
        $res.Ok    = $false
        $res.Error = ($msgs -join ' | ')
        $res.Lines = $lns
        return $res
    }
}

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
        [string] $BridgeRoot     = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge',
        # Return $null instead of throwing on a refusal. For the self-test and
        # for tooling - NOT for boot jobs. See the USAGE block above.
        [switch] $NoThrow
    )

    $staged = Join-Path $BridgeRoot 'staged'
    $tpl    = Join-Path $staged 'TEMPLATE_teardown_generic.ps1'
    $now    = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

    $global:PairedTeardownRefusal = ''

    # ---- helpers ----------------------------------------------------------
    # Esc: a value that goes into CODE becomes a single-quoted literal with any
    # embedded quote doubled. Inside a single-quoted PowerShell string, $ ` "
    # and $( ) are all inert, so no input can escape into code. A path with a
    # space or an apostrophe survives verbatim.
    function Esc($s) { "'" + ([string]$s).Replace("'", "''") + "'" }

    # Cmt: a value that goes into a COMMENT is forced onto one line. CR, LF and
    # TAB become a single space. The ASCII gate below already rejects those
    # bytes outright, so this is the second of two locks on the same door: no
    # value can ever start a line of its own again, which is what happened to
    # job 950.
    function Cmt($s) {
        $t = [string]$s
        $t = $t.Replace("`r", ' ')
        $t = $t.Replace("`n", ' ')
        $t = $t.Replace("`t", ' ')
        return $t
    }

    # Deny: one exit for every refusal. Loud, named, and non-zero.
    function Deny($reason) {
        $r = [string]$reason
        Write-Host ''
        Write-Host '############################################################################'
        Write-Host '## PAIRED TEARDOWN REFUSED - NOTHING WAS WRITTEN'
        foreach ($rl in ($r -split "`n")) { Write-Host ('## ' + $rl.TrimEnd()) }
        Write-Host '##'
        Write-Host '## THIS ROUND HAS NO PAIRED TEARDOWN. Close it by hand, before you walk'
        Write-Host '## away, with staged\TEMPLATE_teardown_generic.ps1 - or the round dies'
        Write-Host '## with the server still up, which is the failure this file exists to'
        Write-Host '## prevent.'
        Write-Host '############################################################################'
        $global:LASTEXITCODE = 41
        $global:PairedTeardownRefusal = $r
    }

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

    # ---- 2) NAME GATE -----------------------------------------------------
    # $TeardownName becomes a FILE NAME. A value like '..\..\inbox\evil' would
    # resolve straight into the execute queue, and this function's first
    # promise is that it never writes into inbox\. So the name is restricted to
    # a flat, boring character class before it is ever joined to a path, and
    # the resolved directory is checked again in step 4.
    if ($TeardownName -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$') {
        Deny ("TeardownName '" + $TeardownName + "' is not a plain file name. Allowed: letters, digits, dot, underscore, hyphen; must start with a letter or digit. A teardown name is never a path.")
        if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: illegal TeardownName' }
        return $null
    }

    # ---- 3) ASCII GATE ----------------------------------------------------
    # These scripts run on Windows PowerShell 5.1 with console codepage cp874.
    # One non-cp874 character printed to the console turns the project gate red;
    # it has happened before. A generated job is exactly the kind of file nobody
    # re-reads, so it must never be the thing that carries a stray byte. If any
    # value we would embed is not pure ASCII we write NOTHING and say so: the
    # round can still be closed by hand with TEMPLATE_teardown_generic.ps1,
    # which is a worse day than usual but not a red gate.
    #
    # The list below now includes BootBase, Tpl and Now. The 2026-08-21 review
    # found that $bootBase - which comes from -BootScriptPath or from the call
    # stack, i.e. from outside this function - was interpolated into the header
    # WITHOUT ever being checked. It only lands in a comment, but "it only lands
    # in a comment" is exactly the reasoning that produced job 950.
    #
    # Rejecting CR (13) and LF (10) here is also the FIRST of the two locks that
    # stop a value from starting a line of its own; Cmt() is the second.
    foreach ($pair in @(@('Stamp', $Stamp), @('Scenario', $Scenario), @('RunDb', $RunDb),
                        @('GtId', $GtId), @('InfoPrefix', $InfoPrefix),
                        @('CaptureFilter', $CaptureFilter), @('TeardownName', $TeardownName),
                        @('BridgeRoot', $BridgeRoot), @('BootBase', $bootBase),
                        @('Tpl', $tpl), @('Now', $now))) {
        $v = [string]$pair[1]
        foreach ($ch in $v.ToCharArray()) {
            if ([int]$ch -gt 126 -or ([int]$ch -lt 32 -and [int]$ch -ne 9)) {
                Deny ("parameter " + $pair[0] + " contains a character that is not printable ASCII (U+" + ('{0:X4}' -f [int]$ch) + "). Refusing to generate a job that could print it to a cp874 console, or that could break out of its own line.")
                if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: non-ASCII or control character in a metadata value' }
                return $null
            }
        }
    }

    # ---- 4) target path - never overwrite, never inbox\ --------------------
    if (-not (Test-Path -LiteralPath $staged)) {
        New-Item -ItemType Directory -Path $staged -ErrorAction SilentlyContinue | Out-Null
    }
    $target = Join-Path $staged ($TeardownName + '.ps1')
    if (Test-Path -LiteralPath $target) {
        $target = Join-Path $staged ($TeardownName + '_' + $Stamp + '.ps1')
        Write-Host ("paired teardown: " + $TeardownName + ".ps1 already exists - writing " + (Split-Path -Leaf $target) + " instead (nothing is ever overwritten)")
    }

    # Second lock on the same door as the NAME GATE, this time on the resolved
    # path rather than on the input. Cheap, and it is the one an auditor reads.
    $targetFull = ''
    $targetDir  = ''
    $stagedFull = ''
    try {
        $targetFull = [System.IO.Path]::GetFullPath($target)
        $targetDir  = [System.IO.Path]::GetDirectoryName($targetFull)
        $stagedFull = [System.IO.Path]::GetFullPath($staged)
    } catch {
        Deny ("cannot resolve the output path '" + $target + "': " + $_.Exception.Message)
        if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: unresolvable output path' }
        return $null
    }
    if ($targetDir.TrimEnd('\') -ne $stagedFull.TrimEnd('\')) {
        Deny ("the output path resolves to '" + $targetDir + "' which is not the staged directory '" + $stagedFull + "'. Refusing.")
        if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: output path escapes staged\' }
        return $null
    }
    if ($targetDir -match '(?i)\\inbox\\?$') {
        Deny ("the output path resolves into an inbox directory ('" + $targetDir + "'). This function never enqueues its own teardown. Refusing.")
        if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: output path is inbox\' }
        return $null
    }

    # ---- 5) build the generated job ---------------------------------------
    # READ THE REGRESSION NOTE AT THE TOP OF THIS FILE BEFORE EDITING EITHER
    # ARRAY BELOW. Every element is a bare literal or is wrapped in ( ). There
    # is no top-level '+' inside @( ), because in PowerShell ',' binds tighter
    # than '+' and a top-level '+' concatenates ARRAYS instead of strings.
    $scenTxt  = '(none declared)'
    if ($Scenario) { $scenTxt = $Scenario }
    $runDbTxt = '(none declared)'
    if ($RunDb) { $runDbTxt = $RunDb }

    $hdr = @(
        '# ==========================================================================',
        '# AUTO-GENERATED PAIRED TEARDOWN - do not hand-edit; re-boot to regenerate.',
        '#',
        ('# round      : ' + (Cmt $GtId)),
        ('# boot job   : ' + (Cmt $bootBase) + '.ps1'),
        ('# boot stamp : ' + (Cmt $Stamp)),
        ('# scenario   : ' + (Cmt $scenTxt)),
        ('# run-copy DB: ' + (Cmt $runDbTxt)),
        ('# generated  : ' + (Cmt $now) + ' by TEMPLATE_boot_writes_paired_teardown.ps1'),
        '# parse gate : this text was accepted by [scriptblock]::Create before it',
        '#              was allowed to reach the disk.',
        '#',
        '# TO CLOSE THIS ROUND: copy this file into pf_bridge\inbox\. That is all.',
        '# Nothing to rename, nothing to fill in, nothing to remember.',
        '#',
        '# If the round already went cold and you only want the evidence that is',
        '# still on disk, run this file by hand with -Salvage. It will collect and',
        '# never kill. See HOWTO_SALVAGE_A_DEAD_ROUND.md.',
        '# =========================================================================='
    )

    # The argument list of the generated job, built as pairs so that the last
    # element gets no trailing comma. PowerShell rejects @( 'a', ) outright, and
    # a generated file that does not parse is worse than no generated file.
    # (These are METHOD ARGUMENTS, not array elements, so '+' behaves normally
    # here - but they are parenthesised anyway, for one rule instead of two.)
    $pairs = New-Object System.Collections.ArrayList
    $null = $pairs.Add(("'-JobTag',           " + (Esc $TeardownName)))
    $null = $pairs.Add(("'-ExpectBootStamp',  " + (Esc $Stamp)))
    $null = $pairs.Add(("'-CaptureFilter',    " + (Esc $CaptureFilter)))
    if ($InfoPrefix) { $null = $pairs.Add(("'-ExpectInfoPrefix', " + (Esc $InfoPrefix))) }
    $pargsLines = @()
    for ($i = 0; $i -lt $pairs.Count; $i++) {
        $sep = ','
        if ($i -eq ($pairs.Count - 1)) { $sep = '' }
        $pargsLines += ('    ' + $pairs[$i] + $sep)
    }

    $bodyA = @(
        '',
        'param([switch] $Salvage)',
        '',
        '$ErrorActionPreference = ''Continue''',
        '$ProgressPreference    = ''SilentlyContinue''',
        '',
        ('$tpl       = ' + (Esc $tpl)),
        ('$bootStamp = ' + (Esc $Stamp)),
        ('$runDb     = ' + (Esc $RunDb)),
        ('$scenario  = ' + (Esc $Scenario)),
        ('$jobTag    = ' + (Esc $TeardownName)),
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
    $bodyB = @(
        ')',
        'if ($Salvage) { $pargs += ''-Salvage'' }',
        '',
        '& powershell.exe @pargs',
        '$code = $LASTEXITCODE',
        'Write-Host ("teardown template exit = " + $code)',
        'if ($code -eq 20) { Write-Host ''SALVAGE receipt written - this round is DEGRADED, not green.'' }',
        'exit $code'
    )

    $lines = @()
    $lines += $hdr
    $lines += $bodyA
    $lines += $pargsLines
    $lines += $bodyB

    # ---- 6) HEADER GUARD --------------------------------------------------
    # Tonight's bug, written down as an assertion instead of as a warning: every
    # line of the header block is a comment or is empty. If an interpolated
    # value ever falls onto a line of its own again, this catches it here, by
    # name, before the parse gate and long before the operator.
    for ($i = 0; $i -lt $hdr.Count; $i++) {
        $hl = [string]$hdr[$i]
        if ($hl -ne '' -and -not $hl.StartsWith('#')) {
            Deny ("generated header line " + ($i + 1) + " is not a comment: <<" + $hl + ">>. A metadata value has escaped onto a line of its own - this is the job-950 defect.")
            if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: header line is not a comment' }
            return $null
        }
    }

    # ---- 7) NEWLINE GUARD -------------------------------------------------
    # One element, one line, always. WriteAllLines cannot enforce it; this can.
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $ln = [string]$lines[$i]
        if ($ln.Contains("`r") -or $ln.Contains("`n")) {
            Deny ("generated line " + ($i + 1) + " contains an embedded line break. One element must be exactly one line.")
            if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: embedded line break in a generated line' }
            return $null
        }
    }

    # ---- 8) PARSE GATE (D2) -----------------------------------------------
    # The last thing between a broken generator and an unattended round. The
    # text that is checked is byte-for-byte the text that would be written:
    # same lines, same separator that WriteAllLines uses.
    $text = ($lines -join [Environment]::NewLine)
    $chk  = Test-PairedTeardownParses -Text $text
    if (-not $chk.Ok) {
        $detail = @()
        $detail += ('the generated teardown does not parse: ' + $chk.Error)
        foreach ($bad in @($chk.Lines)) {
            $idx = [int]$bad
            if ($idx -ge 1 -and $idx -le $lines.Count) {
                $detail += ('  >> line ' + $idx + ': ' + [string]$lines[$idx - 1])
            }
        }
        $detail += 'NOT WRITTEN. This is exactly the job-950 failure and it stops here.'
        Deny ($detail -join "`n")
        if (-not $NoThrow) { throw 'PAIRED TEARDOWN REFUSED: generated job does not parse' }
        return $null
    }

    # ---- 9) write it, BOM-free -------------------------------------------
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
    Write-Host ("  parse gate : OK (" + $lines.Count + " lines accepted by [scriptblock]::Create)")
    return $target
}
