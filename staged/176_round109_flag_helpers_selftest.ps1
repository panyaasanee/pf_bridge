# Job 176 - chief round 109.  Run the flag-helper self-test and watch it decide.
#
# WHY.  Round 109 found that every gate/commit job from 160 to 175 wrote
# LOCK_GIT.txt with Out-File -Encoding utf8, which on Windows PowerShell 5.1
# prepends a BOM, while the acquire check in those same jobs tests '^HELD:',
# which a BOM'd line does not match.  The check therefore reported "free"
# EXACTLY WHEN THE FLAG WAS HELD.  Round 108 had already written that warning
# into the flag file's own warn block and it was inherited anyway, which is the
# real lesson: a rule that lives only in prose gets re-learned by the next reader.
#
# staged\TEMPLATE_lock_flag_helpers.ps1 fixes it in two independent places (the
# writer emits no BOM; the checker tolerates one) and carries a self-test with
# four cases.  T4 is the one that matters: a BOM'd HELD file, byte-for-byte what
# jobs 160-175 produced, which the OLD check called free.
#
# A rule nobody has watched reject something is not a rule.  This job watches.
# Read-only: no git, no index, no commit, no server, no client, no database, no
# flag taken (the template writes only to %TEMP% and deletes what it wrote).
# ASCII ONLY.

$ErrorActionPreference = 'Continue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$tpl    = Join-Path $bridge 'staged\TEMPLATE_lock_flag_helpers.ps1'

Write-Host '=== job 176 : flag-helper self-test (BOM trap) ==='
Write-Host ("time : " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))

$out  = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $tpl 2>&1
$code = $LASTEXITCODE
foreach ($l in $out) { Write-Host ('  | ' + $l) }
Write-Host ('  exit = ' + $code)

$joined = ($out | Out-String)
$ok = $true
foreach ($t in @('T1 Write-Flag emits no BOM : PASS',
                 'T2 held is seen as held    : PASS',
                 'T3 released is seen as free: PASS',
                 "T4 BOM'd held is seen held : PASS")) {
    if ($joined -cmatch [regex]::Escape($t)) { Write-Host ("CHECK " + $t) }
    else { Write-Host ("CHECK MISSING> " + $t); $ok = $false }
}
if ($code -ne 0) { Write-Host 'CHECK exit-zero: FAIL'; $ok = $false } else { Write-Host 'CHECK exit-zero: PASS' }

# The live flag must ALSO be clean now - round 109 stripped the BOM job 175 left.
$lockGit = Join-Path $bridge 'LOCK_GIT.txt'
$b = [System.IO.File]::ReadAllBytes($lockGit)
$hasBom = ($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF)
Write-Host ('CHECK LOCK_GIT-has-no-BOM: ' + $(if (-not $hasBom) { 'PASS' } else { 'FAIL' }))
if ($hasBom) { $ok = $false }

Write-Host ''
if (-not $ok) { Write-Host 'JOB176_VERDICT=FAIL'; exit 44 }
Write-Host 'JOB176_VERDICT=PASS'
exit 0
