# Job 078 - HYP-PF-012 Windows gate (round 41). STAGED - move to inbox AFTER 077 finishes.
# Full py -3 pytest + both verifiers on the worktree with HYP-PF-012 changes.
# Green criteria: pytest >= 415 passed / 0 failed (405 prior + 10 new logout tests;
# __notes__ failure is sandbox-only, must NOT appear on Windows py -3),
# ledger PASS entries=19, coverage PASS domains=8. ASCII ONLY. Quote all paths.

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$main   = 'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject'
$stamp  = Get-Date -Format 'yyyyMMdd_HHmmss'
$log    = Join-Path $bridge 'outbox\078_hyp012_gate.utf8.txt'
function W($m) { $l = "$(Get-Date -Format 'HH:mm:ss.fff')  $m"; $l | Out-File -FilePath $log -Encoding utf8 -Append; Write-Host $l }
"=== HYP-PF-012 WINDOWS GATE  $stamp ===" | Out-File -FilePath $log -Encoding utf8

Set-Location -LiteralPath $main
W "cwd = $(Get-Location)"

W '--- pytest full suite ---'
py -3 -m pytest tests -q 2>&1 | Select-Object -Last 15 | ForEach-Object { W "  py> $_" }
$pytestExit = $LASTEXITCODE
W "pytest exit = $pytestExit"

W '--- verify_hypothesis_ledger ---'
py -3 (Join-Path $main 'tools\verify_hypothesis_ledger.py') 2>&1 | Select-Object -Last 5 | ForEach-Object { W "  ledger> $_" }
$ledgerExit = $LASTEXITCODE
W "ledger exit = $ledgerExit"

W '--- verify_functional_coverage ---'
py -3 (Join-Path $main 'tools\verify_functional_coverage.py') 2>&1 | Select-Object -Last 12 | ForEach-Object { W "  cov> $_" }
$covExit = $LASTEXITCODE
W "coverage exit = $covExit"

"pytestExit=$pytestExit ledgerExit=$ledgerExit covExit=$covExit stamp=$stamp" | Out-File -FilePath (Join-Path $bridge "outbox\078_gate_summary_$stamp.txt") -Encoding ascii
W "=== 078 DONE pytest=$pytestExit ledger=$ledgerExit cov=$covExit ==="
