# ============================================================================
# fix_git_sync_settings.ps1 - apply the PF_Git_Sync settings that need elevation.
# ASCII ONLY. Run through SETUP_GIT_SYNC_FIXED.bat, not on its own.
#
# PROVENANCE: this is fix_watchdog_admin.ps1 with one value flipped. That script
# ran successfully on this machine on 2026-08-20 ~09:2x and is the only
# Set-ScheduledTask call this project has ever seen succeed. The task is created
# by schtasks in the .bat (the same line that registered PF_Bridge_Watchdog and
# has worked for days); this script only ADJUSTS an existing task. Do not add a
# Register-ScheduledTask call here - that is exactly what failed at 19:14.
#
# THE ONE DELIBERATE DIFFERENCE FROM THE WATCHDOG: WakeToRun is FALSE.
# The watchdog wakes the machine on purpose so chief can run while Panya sleeps.
# The sync must NOT: when the machine is asleep there is no local tester to hand
# anything to, so waking every 5 minutes forever would burn the battery to move
# nothing. StartWhenAvailable + the logon trigger cover the catch-up instead.
# ============================================================================
$ErrorActionPreference = 'Continue'
$task = 'PF_Git_Sync'

Write-Output "=== fix_git_sync_settings  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="

$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$pr = New-Object Security.Principal.WindowsPrincipal($id)
$elev = $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Output ("ELEVATED=" + $elev)
if (-not $elev) {
    Write-Output 'NOT ELEVATED - right-click SETUP_GIT_SYNC_FIXED.bat and Run as administrator.'
    exit 1
}

$t0 = Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
if (-not $t0) {
    Write-Output "TASK_NOT_FOUND: $task was not registered by the .bat step. Stopping."
    Write-Output 'Nothing was changed. Read the schtasks output above this line.'
    exit 2
}
Write-Output 'TASK_FOUND_OK'

Write-Output '=== APPLY SETTINGS ==='
try {
    $set = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -MultipleInstances IgnoreNew `
        -ExecutionTimeLimit ([TimeSpan]::Zero)
    $set.WakeToRun = $false
    Set-ScheduledTask -TaskName $task -Settings $set -ErrorAction Stop | Out-Null
    Write-Output 'SETTINGS_OK'
} catch {
    Write-Output ('SETTINGS_FAILED: ' + $_.Exception.Message)
}

Write-Output '=== ADD LOGON TRIGGER (keep the 5-minute one) ==='
try {
    $t = Get-ScheduledTask -TaskName $task -ErrorAction Stop
    $hasLogon = $false
    foreach ($tr in @($t.Triggers)) {
        if ($tr.CimClass.CimClassName -eq 'MSFT_TaskLogonTrigger') { $hasLogon = $true }
    }
    if ($hasLogon) {
        Write-Output 'LOGON_TRIGGER_ALREADY_PRESENT'
    } else {
        $all = @($t.Triggers) + (New-ScheduledTaskTrigger -AtLogOn -User 'Panya')
        Set-ScheduledTask -TaskName $task -Trigger $all -ErrorAction Stop | Out-Null
        Write-Output 'LOGON_TRIGGER_ADDED'
    }
} catch {
    Write-Output ('LOGON_TRIGGER_FAILED (non-fatal): ' + $_.Exception.Message)
}

Write-Output '=== VERIFY (this is the part that decides, not the exit code above) ==='
$t2 = Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
if (-not $t2) { Write-Output 'VERDICT=FAIL (task vanished)'; exit 3 }

$t2.Settings | Select-Object StartWhenAvailable, WakeToRun, MultipleInstances, DisallowStartIfOnBatteries, StopIfGoingOnBatteries | Format-List | Out-String | Write-Output
Write-Output 'TRIGGERS:'
foreach ($tr in @($t2.Triggers)) { Write-Output ('  ' + $tr.CimClass.CimClassName) }

$ok = $true
if ($t2.Settings.WakeToRun -eq $false) { Write-Output 'PASS: WakeToRun is False' } else { Write-Output 'FAIL: WakeToRun is not False'; $ok = $false }
if ($t2.Settings.StartWhenAvailable -eq $true) { Write-Output 'PASS: StartWhenAvailable is True' } else { Write-Output 'FAIL: StartWhenAvailable is not True'; $ok = $false }

if ($ok) { Write-Output 'VERDICT=PASS' } else { Write-Output 'VERDICT=FAIL' }
