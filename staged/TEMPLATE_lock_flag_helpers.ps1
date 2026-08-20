# TEMPLATE - the two flag-file helpers, written once so nobody copies the broken
# pair out of job 169 again.  Chief round 109, 2026-08-20.  ASCII ONLY.
#
# THE DEFECT THIS EXISTS TO KILL.  Out-File -Encoding utf8 on Windows PowerShell
# 5.1 prepends a UTF-8 BOM (EF BB BF).  Every gate/commit job from 160 to 175
# used it to write LOCK_GIT.txt, so the first line on disk is not "HELD:" but
# BOM + "HELD:".  The acquire check in those same jobs is:
#     if ($firstLine -cmatch '^HELD:')
# which DOES NOT MATCH a BOM'd line.  The failure is perfectly inverted: the
# check is there to stop a second job from stomping a held flag, and it fails
# EXACTLY WHEN THE FLAG IS HELD, silently, reporting the flag as free.  Round 108
# wrote this down in the flag's own warn block; job 175 inherited it anyway,
# because a lesson that lives only in prose gets re-learned by the next reader.
#
# TWO INDEPENDENT FIXES, on purpose.  The writer and the checker are edited by
# different jobs at different times, so neither is allowed to be the only one:
#   1. Write-Flag never emits a BOM.
#   2. Test-FlagHeld tolerates one anyway.
# Either alone would close today's hole.  Both together survive the day somebody
# writes a flag with a tool nobody in this project has thought about yet.

# --- 1. WRITE -----------------------------------------------------------------
# WriteAllLines with a UTF8Encoding($false) - the $false IS the fix; the default
# UTF8Encoding emits the BOM.  These files are ASCII by project rule, so the
# encoding only decides the BOM.  Do NOT "simplify" this back to Out-File.
function Write-Flag {
    param(
        [Parameter(Mandatory = $true)][string]   $Path,
        [Parameter(Mandatory = $true)][string[]] $Lines
    )
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($Path, $Lines, $utf8NoBom)
}

# --- 2. CHECK -----------------------------------------------------------------
# -cmatch, case-sensitive, same as the jobs have always used: a flag file whose
# first line says "held:" in lower case is not a flag this protocol wrote, and
# guessing about it is worse than refusing.
# Once PowerShell has DECODED the file, the BOM is ONE CHARACTER (U+FEFF), not
# three bytes - Get-Content decodes, so the pattern must be written against the
# character.  It is built with [char]0xFEFF rather than typed literally, because
# this file declares itself ASCII-only and a file about a byte-order-mark trap is
# the last file that should contain one.
function Test-FlagHeld {
    param([Parameter(Mandatory = $true)][string] $Path)
    $first = (Get-Content -LiteralPath $Path -TotalCount 1 -ErrorAction SilentlyContinue)
    if ($null -eq $first) { return $false }   # absent file = not held
    # ${bom} and not $bom: PowerShell parses "$bom?HELD:" as a DRIVE-QUALIFIED
    # variable reference and dies with "':' was not followed by a valid variable
    # name character".  Job 176 caught that at 19:33 by running this file, which
    # is the entire argument for the self-test existing at all - the parse error
    # sat in a function that is only reached when a flag is actually held, so a
    # template shipped unrun would have exploded on the day it mattered most.
    $bom = [char]0xFEFF
    return [bool]($first -cmatch "^${bom}?HELD:")
}

# --- 3. HEARTBEAT -------------------------------------------------------------
# Add-Content appends without touching the BOM question at all, so it was never
# part of the defect; kept here only so the three operations live in one place.
function Add-FlagHeartbeat {
    param(
        [Parameter(Mandatory = $true)][string] $Path,
        [Parameter(Mandatory = $true)][string] $Phase
    )
    Add-Content -LiteralPath $Path `
        -Value "HEARTBEAT: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')+07:00  $Phase" `
        -Encoding utf8
}

# --- 4. SELF-TEST -------------------------------------------------------------
# A rule nobody has watched reject something is not a rule.  Run this file
# directly to watch all four cases decide, including the one that was wrong:
#     powershell -NoProfile -ExecutionPolicy Bypass -File TEMPLATE_lock_flag_helpers.ps1
if ($MyInvocation.InvocationName -ne '.') {
    $tmp = Join-Path $env:TEMP ("flagtest_" + [Guid]::NewGuid().ToString('N') + ".txt")
    $fail = 0

    Write-Flag -Path $tmp -Lines @('HELD: now', 'BY: the self-test')
    $bytes = [System.IO.File]::ReadAllBytes($tmp)
    $hasBom = ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
    Write-Host ("T1 Write-Flag emits no BOM : " + $(if (-not $hasBom) { 'PASS' } else { 'FAIL'; $fail = 1 }))
    Write-Host ("T2 held is seen as held    : " + $(if (Test-FlagHeld $tmp) { 'PASS' } else { 'FAIL'; $fail = 1 }))

    Write-Flag -Path $tmp -Lines @('RELEASED: now')
    Write-Host ("T3 released is seen as free: " + $(if (-not (Test-FlagHeld $tmp)) { 'PASS' } else { 'FAIL'; $fail = 1 }))

    # T4 is the whole point: a BOM'd HELD file, exactly what jobs 160-175 wrote.
    # The old check answered "free" here.  This one must answer "held".
    $utf8Bom = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllLines($tmp, @('HELD: now', 'BY: a job with the old writer'), $utf8Bom)
    Write-Host ("T4 BOM'd held is seen held : " + $(if (Test-FlagHeld $tmp) { 'PASS' } else { 'FAIL'; $fail = 1 }))

    Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    if ($fail -ne 0) { Write-Host 'FLAG_HELPERS_VERDICT=FAIL'; exit 1 }
    Write-Host 'FLAG_HELPERS_VERDICT=PASS'
    exit 0
}
