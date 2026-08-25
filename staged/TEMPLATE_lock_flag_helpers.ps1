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
#
# 2026-08-25 (COO, 23:50) - THE SECOND DEFECT THIS FILE EXISTS TO KILL.
# LOCK_GAME.txt was found at 920,675,768 bytes.  Not a logic bug - an ENCODING
# LOOP, and the two halves of it live in two different files:
#   Write-Flag writes UTF-8 with NO BOM (correct, and deliberate - see above).
#   Every job then read it back with a bare `Get-Content`, and Windows
#   PowerShell 5.1 with no BOM to go on falls back to the system ANSI code page.
# Thai text - which has no business being in a file this header declares ASCII -
# came back as mojibake and was written out again as UTF-8.  Three bytes became
# nine.  Every lock.  Every release.  Twenty-seven history cycles later the file
# was 920 MB and every single lock operation was reading and rewriting all of it.
#
# THREE INDEPENDENT FIXES, same reasoning as the BOM defect above: the writer,
# the reader, and the content rule are edited by different jobs at different
# times, so no one of them is allowed to be the only guard.
#   1. Write-Flag replaces non-ASCII with '?' and says so in the file itself.
#      It does NOT throw - a job that dies here dies holding a lock, and a
#      readable flag is worth more than a perfect one.
#   2. Read-Flag exists, and reads UTF-8 explicitly.  Use it.  Never bare
#      Get-Content on a flag file.
#   3. A single line over 4000 chars is truncated with a visible marker, and a
#      file over 600 lines spills the tail into archive\ with a pointer line.
#      Either alone stops the growth; together they survive the next surprise.
function Write-Flag {
    param(
        [Parameter(Mandatory = $true)][string]   $Path,
        [Parameter(Mandatory = $true)][string[]] $Lines
    )

    $dirty = $false
    $long  = $false
    $clean = @(foreach ($l in $Lines) {
        $s = [string]$l
        if ($s -match '[^\x00-\x7F]') { $dirty = $true; $s = ($s -replace '[^\x00-\x7F]', '?') }
        if ($s.Length -gt 4000) { $long = $true; $s = $s.Substring(0, 4000) + '  [...truncated by Write-Flag]' }
        $s
    })

    $notes = @()
    if ($dirty) { $notes += 'note: Write-Flag replaced non-ASCII characters with ? - this file is ASCII only.' }
    if ($long)  { $notes += 'note: Write-Flag truncated at least one line over 4000 characters.' }

    # Spill, never drop.  The project rule is that old text is kept as history,
    # so the tail goes to a real file and the flag carries a pointer to it.
    $cap = 600
    if (($clean.Count + $notes.Count) -gt $cap) {
        $head = $clean[0..($cap - 1)]
        $tail = $clean[$cap..($clean.Count - 1)]
        $stamp = (Get-Date).ToString('yyyyMMdd_HHmmss', [System.Globalization.CultureInfo]::InvariantCulture)
        $dir = Join-Path (Split-Path -Parent $Path) 'archive'
        if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        # Two statements on purpose.  Written as one, PowerShell binds the `+` as a
        # THIRD positional argument to Join-Path and dies - the self-test caught
        # exactly that on 2026-08-25, while T7 still reported PASS because it was
        # only checking the message, not the file.  Both are fixed.
        $leaf  = (Split-Path -Leaf $Path) -replace '\.txt$',''
        $spill = Join-Path $dir ($leaf + "_overflow_$stamp.txt")
        $utf8NoBomS = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllLines($spill, $tail, $utf8NoBomS)
        $notes += "note: history past line $cap moved to archive\$(Split-Path -Leaf $spill) - nothing was deleted."
        $clean = $head
    }

    # $clean[1..0] is not an empty slice in PowerShell - it counts DOWN and hands
    # back index 1 (null) then index 0 (a duplicate).  Guard the single-line case.
    if ($notes.Count -gt 0) {
        if ($clean.Count -ge 2) { $clean = @($clean[0]) + $notes + @($clean[1..($clean.Count - 1)]) }
        else                    { $clean = @($clean) + $notes }
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($Path, $clean, $utf8NoBom)
}

# --- 1b. READ ------------------------------------------------------------------
# The missing half of the pair.  A bare Get-Content on a BOM-less UTF-8 file is
# decoded with the system ANSI code page, and on this machine that is CP874.
# That is what turned one Thai line into 920 MB of history.  Read flags with this.
function Read-Flag {
    param([Parameter(Mandatory = $true)][string] $Path)
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    return @([System.IO.File]::ReadAllLines($Path, (New-Object System.Text.UTF8Encoding($false))))
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

    # T5-T7 are the encoding-loop defect.  T6 is the one that matters: the whole
    # 920 MB came from a read that answered with mojibake, so a round trip that
    # comes back byte-identical is the claim worth testing.
    $thai = [string]([char]0x0E01 + [char]0x0E02)   # two Thai characters, built not typed
    Write-Flag -Path $tmp -Lines @('HELD: t5', "BY: $thai")
    $back = Read-Flag -Path $tmp
    $hasNonAscii = ($back -join '') -match '[^\x00-\x7F]'
    Write-Host ("T5 non-ASCII is replaced   : " + $(if (-not $hasNonAscii) { 'PASS' } else { 'FAIL'; $fail = 1 }))
    Write-Host ("T5b and the file says so   : " + $(if (($back -join '|') -match 'replaced non-ASCII') { 'PASS' } else { 'FAIL'; $fail = 1 }))

    Write-Flag -Path $tmp -Lines @('HELD: t6', 'BY: plain ascii line')
    $rt = Read-Flag -Path $tmp
    Write-Host ("T6 ascii round trip exact  : " + $(if ($rt.Count -eq 2 -and $rt[1] -eq 'BY: plain ascii line') { 'PASS' } else { 'FAIL'; $fail = 1 }))

    $big = @('HELD: t7') + (1..700 | ForEach-Object { "history line $_" })
    Write-Flag -Path $tmp -Lines $big
    $cut = Read-Flag -Path $tmp
    Write-Host ("T7 over-long history spills: " + $(if ($cut.Count -le 601 -and ($cut -join '|') -match 'moved to archive') { 'PASS' } else { 'FAIL'; $fail = 1 }))
    Write-Host ("T7b line 1 survives spill  : " + $(if ($cut[0] -eq 'HELD: t7') { 'PASS' } else { 'FAIL'; $fail = 1 }))
    # T7c/T7d exist because T7 alone PASSED on 2026-08-25 while the spill file was
    # never written - it was matching the note text, and the note text is written
    # whether or not the write succeeded.  Assert the artefact, not the sentence.
    $spillDir = Join-Path (Split-Path -Parent $tmp) 'archive'
    $spills = @(Get-ChildItem -Path $spillDir -Filter '*_overflow_*.txt' -File -ErrorAction SilentlyContinue |
                Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-2) })
    Write-Host ("T7c the spill file exists  : " + $(if ($spills.Count -ge 1) { 'PASS' } else { 'FAIL'; $fail = 1 }))
    if ($spills.Count -ge 1) {
        $tailBack = Read-Flag -Path $spills[0].FullName
        $ok = ($tailBack.Count -eq 101 -and $tailBack[-1] -eq 'history line 700')
        Write-Host ("T7d the spill holds the tail: " + $(if ($ok) { 'PASS' } else { "FAIL (count=$($tailBack.Count) last=$($tailBack[-1]))"; $fail = 1 }))
    }

    Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path (Join-Path (Split-Path -Parent $tmp) 'archive') -Filter '*_overflow_*.txt' -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-2) } |
        Remove-Item -Force -ErrorAction SilentlyContinue
    if ($fail -ne 0) { Write-Host 'FLAG_HELPERS_VERDICT=FAIL'; exit 1 }
    Write-Host 'FLAG_HELPERS_VERDICT=PASS'
    exit 0
}
