# fix_watchdog_admin.ps1 - needs ELEVATION. Launched by FIX_WATCHDOG_ADMIN.bat.
# Applies the Task Scheduler settings that job 901 could not (Access is denied
# from the non-elevated bridge): replay missed runs after wake, run on battery,
# wake the PC to run, plus an at-logon trigger. ASCII only.

$ErrorActionPreference = 'Continue'
$bridge = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$task   = 'PF_Bridge_Watchdog'
$log    = Join-Path $bridge 'outbox\902_fix_watchdog_admin.out.txt'

Start-Transcript -Path $log -Force | Out-Null

Write-Output "=== 902 admin fix  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="

$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$pr = New-Object Security.Principal.WindowsPrincipal($id)
$elev = $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Output ("ELEVATED=" + $elev)
if (-not $elev) {
    Write-Output 'NOT ELEVATED - right-click FIX_WATCHDOG_ADMIN.bat and choose "Run as administrator".'
    Stop-Transcript | Out-Null
    exit 1
}

Write-Output ''
Write-Output '=== APPLY SETTINGS ==='
try {
    $set = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -WakeToRun `
        -MultipleInstances IgnoreNew `
        -ExecutionTimeLimit ([TimeSpan]::Zero)
    Set-ScheduledTask -TaskName $task -Settings $set -ErrorAction Stop | Out-Null
    Write-Output 'SETTINGS_OK'
} catch {
    Write-Output ('SETTINGS_FAILED: ' + $_.Exception.Message)
}

Write-Output ''
Write-Output '=== ADD LOGON TRIGGER ==='
try {
    $t = Get-ScheduledTask -TaskName $task -ErrorAction Stop
    $has = $false
    foreach ($tr in $t.Triggers) {
        if ($tr.CimClass.CimClassName -eq 'MSFT_TaskLogonTrigger') { $has = $true }
    }
    if ($has) {
        Write-Output 'LOGON_TRIGGER_ALREADY_PRESENT'
    } else {
        $all = @($t.Triggers) + (New-ScheduledTaskTrigger -AtLogOn -User 'Panya')
        Set-ScheduledTask -TaskName $task -Trigger $all -ErrorAction Stop | Out-Null
        Write-Output 'LOGON_TRIGGER_ADDED'
    }
} catch {
    Write-Output ('LOGON_TRIGGER_FAILED: ' + $_.Exception.Message)
}

Write-Output ''
Write-Output '=== VERIFY ==='
$t2 = Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
if ($t2) {
    $t2.Settings | Select-Object StartWhenAvailable, WakeToRun, DisallowStartIfOnBatteries, StopIfGoingOnBatteries |
        Format-List | Out-String | Write-Output
    Write-Output 'TRIGGERS:'
    $t2.Triggers | ForEach-Object { Write-Output ('  ' + $_.CimClass.CimClassName) }
}
Get-ScheduledTaskInfo -TaskName $task -ErrorAction SilentlyContinue |
    Select-Object LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns |
    Format-List | Out-String | Write-Output

$hbf = Join-Path $bridge 'watchdog_last_check.txt'
if (Test-Path $hbf) { Write-Output ('HEARTBEAT_FILE: ' + (Get-Content -Raw $hbf).Trim()) }
else { Write-Output 'HEARTBEAT_FILE: not written yet' }

Write-Output ''
Write-Output '=== DONE 902 ==='
Stop-Transcript | Out-Null
