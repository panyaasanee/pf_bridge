# ==========================================================================
# AUTO-GENERATED PAIRED TEARDOWN - do not hand-edit; re-boot to regenerate.
#
# round      : 
gt039
# boot job   : 
949_gt039_boot
.ps1
# boot stamp : 
20260821_020540
# scenario   : 
C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\scenarios\npc_hp_link_hypothesis_target_sweep.json
# run-copy DB: 
C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\state\pirateforce_gt039_20260821_020540.sqlite3
# generated  : 
2026-08-21 02:05:45
 by TEMPLATE_boot_writes_paired_teardown.ps1
#
# TO CLOSE THIS ROUND: copy this file into pf_bridge\inbox\. That is all.
# Nothing to rename, nothing to fill in, nothing to remember.
#
# If the round already went cold and you only want the evidence that is
# still on disk, run this file by hand with -Salvage. It will collect and
# never kill. See HOWTO_SALVAGE_A_DEAD_ROUND.md.
# ==========================================================================

param([switch] $Salvage)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

$tpl       = 
'C:\Users\Panya\Desktop\Pirate Force\pf_bridge\staged\TEMPLATE_teardown_generic.ps1'
$bootStamp = 
'20260821_020540'
$runDb     = 
'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\state\pirateforce_gt039_20260821_020540.sqlite3'
$scenario  = 
'C:\Users\Panya\Desktop\Pirate Force\Pirate Force ServerProject\scenarios\npc_hp_link_hypothesis_target_sweep.json'
$jobTag    = 
'950_gt039_teardown'

Write-Host ("=== paired teardown " + $jobTag + " ===")
Write-Host ("boot stamp : " + $bootStamp)
Write-Host ("run DB     : " + $runDb)
Write-Host ("scenario   : " + $scenario)
if ($Salvage) { Write-Host 'mode       : SALVAGE (collect only - nothing will be signalled)' }

if (-not (Test-Path -LiteralPath $tpl)) {
    Write-Host ("ABORT: teardown template missing: " + $tpl)
    exit 30
}

# -ExpectBootStamp is the pairing guarantee: this file was written for ONE
# round, and the template refuses (exit 12) if the newest info file in
# outbox belongs to a different one. That is the job-145 failure closed by
# construction rather than by the operator noticing.
$pargs = @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $tpl,
    '-JobTag',           '950_gt039_teardown',
    '-ExpectBootStamp',  '20260821_020540',
    '-CaptureFilter',    'capture_gt039_*',
    '-ExpectInfoPrefix', '949_'
)
if ($Salvage) { $pargs += '-Salvage' }

& powershell.exe @pargs
$code = $LASTEXITCODE
Write-Host ("teardown template exit = " + $code)
if ($code -eq 20) { Write-Host 'SALVAGE receipt written - this round is DEGRADED, not green.' }
exit $code
