# setup_git_sync_admin.ps1 - needs ELEVATION. Launched by SETUP_GIT_SYNC.bat.
#
# Story: Panya asked (2026-08-20) for a second scheduled task, PF_Git_Sync,
# separate from PF_Bridge_Watchdog, to pull/push git state on its own cadence.
# This script is scope-only: it installs and verifies the Task Scheduler
# entry. It does NOT write, read, or run pf_git_sync.ps1 itself - the chief
# was writing that file in parallel. If it is missing when this runs, the
# task is still installed (it will just fail until the file shows up).
#
# The one deliberate difference from PF_Bridge_Watchdog: WakeToRun is OFF.
# The watchdog wakes the machine because a dead bridge blocks a human waiting
# on it. A git sync has no such urgency - if the machine is asleep overnight,
# nobody is standing by to receive a sync, so waking it every 5 minutes for
# nothing would just burn power and disturb Panya for no reason. Sync only
# runs while the machine is already awake, and catches up immediately at
# logon or unlock instead.
#
# Copied structure from fix_watchdog_admin.ps1 (elevation check, transcript,
# New-ScheduledTaskSettingsSet, Set-ScheduledTask, printed verify receipt) and
# from SETUP_BRIDGE_AUTOSTART.bat (schtasks /Create as a fallback path).
# ASCII only - this console is cp874; a stray non-ASCII byte here has broken
# things before.

$ErrorActionPreference = 'Continue'
$bridge     = 'C:\Users\Panya\Desktop\Pirate Force\pf_bridge'
$task       = 'PF_Git_Sync'
$syncScript = Join-Path $bridge 'pf_git_sync.ps1'
$outboxDir  = Join-Path $bridge 'outbox'
$log        = Join-Path $outboxDir 'SETUP_GIT_SYNC.out.txt'

if (-not (Test-Path $outboxDir)) {
    New-Item -ItemType Directory -Path $outboxDir -Force | Out-Null
}

Start-Transcript -Path $log -Force | Out-Null

Write-Output ("=== SETUP_GIT_SYNC  " + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + " ===")

# --- elevation check ---
$id   = [Security.Principal.WindowsIdentity]::GetCurrent()
$pr   = New-Object Security.Principal.WindowsPrincipal($id)
$elev = $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Output ("ELEVATED=" + $elev)
if (-not $elev) {
    Write-Output 'NOT ELEVATED - right-click SETUP_GIT_SYNC.bat and choose "Run as administrator".'
    Stop-Transcript | Out-Null
    exit 1
}

# --- warn (do not abort) if the sync script does not exist yet ---
Write-Output ''
Write-Output '=== CHECK SYNC SCRIPT ==='
if (Test-Path $syncScript) {
    Write-Output ("SYNC_SCRIPT_FOUND: " + $syncScript)
} else {
    Write-Output ("WARNING: " + $syncScript + " does not exist yet.")
    Write-Output "WARNING: installing the task anyway. It will simply error out on each"
    Write-Output "WARNING: run until the chief finishes writing that file - that is expected."
}

# --- remove any existing task so we install clean ---
Write-Output ''
Write-Output '=== REMOVE EXISTING TASK (IF ANY) ==='
$existing = Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
if ($existing) {
    try {
        Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction Stop
        Write-Output 'UNREGISTERED_OLD_TASK'
    } catch {
        Write-Output ('UNREGISTER_FAILED: ' + $_.Exception.Message)
    }
} else {
    Write-Output 'NO_EXISTING_TASK'
}

# --- action: exactly the command Panya specified ---
$actionArgs = '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "' + $syncScript + '"'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $actionArgs

# --- settings ---
# 5-minute cadence: Panya's number, matches watchdog frequency.
# StartWhenAvailable=True: if the PC was off overnight, fire the missed run
#   the moment it is available instead of waiting for the next 5-minute mark.
# AllowStartIfOnBatteries + DontStopIfGoingOnBatteries: a laptop on battery
#   should not silently stop syncing.
# MultipleInstances=IgnoreNew: if a run is still going (slow network, git
#   lock) the next tick must not stack another instance on top of it.
# ExecutionTimeLimit=0 (TimeSpan.Zero means "no limit" to Task Scheduler):
#   a slow git operation should not get killed mid-way.
# WakeToRun=False on purpose - see header story above. This is the one
# knob that must NOT be copied from PF_Bridge_Watchdog.
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -WakeToRun:$false `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit ([TimeSpan]::Zero)

# --- triggers ---
Write-Output ''
Write-Output '=== BUILD TRIGGERS ==='

# Trigger 1: every 5 minutes, forever.
# First fire is set 5 minutes in the future (not "now") on purpose, so this
# setup script never itself causes an immediate run of pf_git_sync.ps1 - the
# rule for this job is that Panya presses Go, not this installer.
#
# KNOWN PS 5.1 ISSUE: New-ScheduledTaskTrigger -Once -RepetitionDuration
# ([TimeSpan]::MaxValue) throws "The parameter is incorrect" on some PS 5.1
# builds (the underlying XML duration serializer overflows on MaxValue). If
# that happens we fall back to `schtasks /Create /SC MINUTE /MO 5`, which
# does not go through that code path, then re-apply Settings and the other
# triggers with Set-ScheduledTask.
$usedFallback  = $false
$repeatTrigger = $null
$firstRun      = (Get-Date).AddMinutes(5)
try {
    $repeatTrigger = New-ScheduledTaskTrigger -Once -At $firstRun `
        -RepetitionInterval (New-TimeSpan -Minutes 5) `
        -RepetitionDuration ([TimeSpan]::MaxValue) -ErrorAction Stop
    Write-Output 'REPEAT_TRIGGER_BUILT_OK'
} catch {
    Write-Output ('REPEAT_TRIGGER_BUILD_FAILED (will use schtasks fallback): ' + $_.Exception.Message)
    $usedFallback = $true
}

# Trigger 2: at logon of Panya - catches up immediately after boot.
$logonTrigger = New-ScheduledTaskTrigger -AtLogOn -User 'Panya'

Write-Output ''
Write-Output '=== REGISTER TASK ==='
if (-not $usedFallback) {
    try {
        Register-ScheduledTask -TaskName $task -Action $action -Settings $settings `
            -Trigger @($repeatTrigger, $logonTrigger) -User 'Panya' -RunLevel Limited `
            -Force -ErrorAction Stop | Out-Null
        Write-Output 'REGISTERED_VIA_Register-ScheduledTask'
    } catch {
        Write-Output ('Register-ScheduledTask FAILED (will use schtasks fallback): ' + $_.Exception.Message)
        $usedFallback = $true
    }
}

if ($usedFallback) {
    Write-Output ''
    Write-Output '=== FALLBACK: schtasks /Create then Set-ScheduledTask ==='
    Write-Output 'Using an array-splat call to schtasks.exe (not one hand-quoted string)'
    Write-Output 'so PowerShell itself handles the embedded quotes/spaces in -File path.'
    $futureTime   = $firstRun.ToString('HH:mm')
    $trValue      = 'powershell.exe ' + $actionArgs
    $schtasksArgs = @(
        '/Create'
        '/F'
        '/TN'
        $task
        '/SC'
        'MINUTE'
        '/MO'
        '5'
        '/TR'
        $trValue
        '/RU'
        'Panya'
        '/IT'
        '/RL'
        'LIMITED'
        '/ST'
        $futureTime
    )
    & schtasks.exe $schtasksArgs | Out-String | Write-Output
    Write-Output ('SCHTASKS_EXITCODE=' + $LASTEXITCODE)

    try {
        $tExisting     = Get-ScheduledTask -TaskName $task -ErrorAction Stop
        $mergedTrigger = @($tExisting.Triggers) + $logonTrigger
        Set-ScheduledTask -TaskName $task -Settings $settings -Trigger $mergedTrigger -ErrorAction Stop | Out-Null
        Write-Output 'SET_SETTINGS_AND_LOGON_TRIGGER_OK'
    } catch {
        Write-Output ('SET_SETTINGS_FAILED: ' + $_.Exception.Message)
    }
}

# --- add SessionUnlock trigger via CIM (New-ScheduledTaskTrigger has no switch for it) ---
# Non-fatal by design: if this fails, the 5-minute and at-logon triggers
# installed above must still stand. We just print a loud warning and let the
# verdict below reflect the missing trigger honestly.
Write-Output ''
Write-Output '=== ADD SESSION-UNLOCK TRIGGER (CIM) ==='
try {
    $unlockClass = Get-CimClass -Namespace 'Root/Microsoft/Windows/TaskScheduler' `
        -ClassName 'MSFT_TaskSessionStateChangeTrigger' -ErrorAction Stop
    $unlockTrigger = New-CimInstance -CimClass $unlockClass -ClientOnly -Property @{
        StateChange = 8
        UserId      = 'Panya'
    }
    $tCur       = Get-ScheduledTask -TaskName $task -ErrorAction Stop
    $mergedAll  = @($tCur.Triggers) + $unlockTrigger
    Set-ScheduledTask -TaskName $task -Trigger $mergedAll -ErrorAction Stop | Out-Null
    Write-Output 'SESSION_UNLOCK_TRIGGER_ADDED'
} catch {
    Write-Output '*** WARNING: SessionUnlock trigger could NOT be added (non-fatal - the'
    Write-Output '*** other two triggers are still installed). Error was:'
    Write-Output ('*** ' + $_.Exception.Message)
}

# --- verify receipt ---
Write-Output ''
Write-Output '=== VERIFY ==='
$tFinal = Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
if (-not $tFinal) {
    Write-Output 'VERIFY_FAILED: task PF_Git_Sync not found after install.'
    Write-Output 'VERDICT=FAIL'
    Stop-Transcript | Out-Null
    exit 1
}

Write-Output 'TRIGGERS:'
$hasMinute = $false
$hasLogon  = $false
$hasUnlock = $false
foreach ($tr in $tFinal.Triggers) {
    $cls   = $tr.CimClass.CimClassName
    $extra = ''
    if ($cls -eq 'MSFT_TaskTimeTrigger' -and $tr.Repetition -and $tr.Repetition.Interval) {
        $extra     = ' Repetition.Interval=' + $tr.Repetition.Interval
        $hasMinute = $true
    }
    if ($cls -eq 'MSFT_TaskLogonTrigger') {
        $hasLogon = $true
    }
    if ($cls -eq 'MSFT_TaskSessionStateChangeTrigger') {
        $extra     = ' StateChange=' + $tr.StateChange
        $hasUnlock = $true
    }
    Write-Output ('  ' + $cls + $extra)
}

Write-Output ''
Write-Output 'SETTINGS:'
$tFinal.Settings |
    Select-Object StartWhenAvailable, WakeToRun, MultipleInstances, ExecutionTimeLimit, DisallowStartIfOnBatteries, StopIfGoingOnBatteries |
    Format-List | Out-String | Write-Output

Write-Output 'TASK_INFO:'
Get-ScheduledTaskInfo -TaskName $task -ErrorAction SilentlyContinue |
    Select-Object LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns |
    Format-List | Out-String | Write-Output

Write-Output '=== VERDICT CHECKS ==='
$allPass = $true

if ($tFinal.Settings.WakeToRun -eq $false) {
    Write-Output 'PASS: WakeToRun is False'
} else {
    Write-Output 'FAIL: WakeToRun is not False'
    $allPass = $false
}

if ($tFinal.Settings.StartWhenAvailable -eq $true) {
    Write-Output 'PASS: StartWhenAvailable is True'
} else {
    Write-Output 'FAIL: StartWhenAvailable is not True'
    $allPass = $false
}

if ($tFinal.Settings.MultipleInstances -eq 'IgnoreNew') {
    Write-Output 'PASS: MultipleInstances is IgnoreNew'
} else {
    Write-Output ('FAIL: MultipleInstances is ' + $tFinal.Settings.MultipleInstances)
    $allPass = $false
}

if ($hasMinute) {
    Write-Output 'PASS: 5-minute repeating trigger present'
} else {
    Write-Output 'FAIL: 5-minute repeating trigger missing'
    $allPass = $false
}

if ($hasLogon) {
    Write-Output 'PASS: AtLogOn trigger present'
} else {
    Write-Output 'FAIL: AtLogOn trigger missing'
    $allPass = $false
}

if ($hasUnlock) {
    Write-Output 'PASS: SessionUnlock trigger present'
} else {
    Write-Output 'FAIL: SessionUnlock trigger missing'
    $allPass = $false
}

Write-Output ''
if ($allPass) {
    Write-Output 'VERDICT=PASS'
} else {
    Write-Output 'VERDICT=FAIL'
}

Write-Output ''
Write-Output 'This script did NOT run pf_git_sync.ps1 and never calls schtasks /Run.'
Write-Output 'To fire one manual test run yourself:'
Write-Output '  schtasks /Run /TN PF_Git_Sync'
Write-Output ''
Write-Output '=== DONE ==='
Stop-Transcript | Out-Null

if ($allPass) { exit 0 } else { exit 1 }
