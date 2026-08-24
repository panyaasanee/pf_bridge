# pf_recorder_hide_window.ps1 - hide the console window of a detached recorder
# process (ffmpeg) so it cannot sit on top of the game while the round records.
#
# WHY THIS EXISTS (measured, not a guess):
#   GT-034 round 1066 (2026-08-24 02:23) recorded 165.4 s of 1920x1080 video,
#   and the ffmpeg console covered the middle of the frame for the whole clip.
#   The job launched ffmpeg through Win32_Process.Create with
#   ProcessStartupInformation.ShowWindow = 0.  That flag sets STARTUPINFO
#   wShowWindow, which the child only honours if it calls ShowWindow itself.
#   ffmpeg does not.  WMI gives the child a brand new console, and that console
#   window stays visible.  There is no creation-flag knob on Win32_Process, so
#   the fix has to happen after the process exists: find the window it owns and
#   hide it with the Win32 ShowWindow API.
#
# USAGE
#   .\pf_recorder_hide_window.ps1 -ProcessId 1234
#   .\pf_recorder_hide_window.ps1 -ProcessId 1234 -TimeoutSeconds 10
#
# EXIT CODES
#   0  no visible window remains for that pid (hidden now, or never had one)
#   1  the process is gone
#   2  a visible window is still there after the timeout - report it, the round
#      is still usable but the frame is dirty
#
# SAFE BY DESIGN
#   - only touches windows owned by the pid it is given
#   - never kills anything, never sends input, never writes outside stdout
#   - ASCII only, no characters outside cp874 reach the console
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][int]$ProcessId,
    [int]$TimeoutSeconds = 10
)

$ErrorActionPreference = 'Stop'

if (-not ('PfNative.PfWin32' -as [type])) {
    Add-Type -Namespace 'PfNative' -Name 'PfWin32' -MemberDefinition @'
[DllImport("user32.dll")]
public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, System.IntPtr lParam);
public delegate bool EnumWindowsProc(System.IntPtr hWnd, System.IntPtr lParam);
[DllImport("user32.dll")]
public static extern uint GetWindowThreadProcessId(System.IntPtr hWnd, out uint lpdwProcessId);
[DllImport("user32.dll")]
public static extern bool IsWindowVisible(System.IntPtr hWnd);
[DllImport("user32.dll")]
public static extern bool ShowWindow(System.IntPtr hWnd, int nCmdShow);
'@
}
$api = [PfNative.PfWin32]
$SW_HIDE = 0

function Get-VisibleWindowsForPid {
    param([int]$TargetProcessId)
    $found = New-Object System.Collections.ArrayList
    $cb = [PfNative.PfWin32+EnumWindowsProc] {
        param($hWnd, $lParam)
        $owner = 0
        [void]$api::GetWindowThreadProcessId($hWnd, [ref]$owner)
        if ($owner -eq $TargetProcessId -and $api::IsWindowVisible($hWnd)) {
            [void]$found.Add($hWnd)
        }
        return $true
    }
    [void]$api::EnumWindows($cb, [System.IntPtr]::Zero)
    return $found
}

$proc = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
if (-not $proc) {
    Write-Output ("HIDE_WINDOW=NO_PROCESS pid={0}" -f $ProcessId)
    exit 1
}

# The console window does not exist the instant CreateProcess returns, so poll.
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$hidden = 0
$seen = 0
do {
    $wins = Get-VisibleWindowsForPid -TargetProcessId $ProcessId
    foreach ($h in $wins) {
        $seen++
        [void]$api::ShowWindow($h, $SW_HIDE)
        Start-Sleep -Milliseconds 120
        if (-not $api::IsWindowVisible($h)) { $hidden++ }
    }
    if ($seen -gt 0) { break }
    if (-not (Get-Process -Id $ProcessId -ErrorAction SilentlyContinue)) {
        Write-Output ("HIDE_WINDOW=NO_PROCESS pid={0}" -f $ProcessId)
        exit 1
    }
    Start-Sleep -Milliseconds 250
} while ((Get-Date) -lt $deadline)

$remaining = @(Get-VisibleWindowsForPid -TargetProcessId $ProcessId)
Write-Output ("HIDE_WINDOW pid={0} seen={1} hidden={2} still_visible={3}" -f $ProcessId, $seen, $hidden, $remaining.Count)

if ($remaining.Count -eq 0) {
    Write-Output 'HIDE_WINDOW=OK'
    exit 0
}
Write-Output 'HIDE_WINDOW=STILL_VISIBLE'
exit 2
