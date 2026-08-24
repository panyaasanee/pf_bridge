# TEMPLATE_video_recorder.ps1 - reusable full-round desktop recorder helpers.
# ASCII only. Dot-source this file from a boot job and its paired teardown.
#
# The boot side follows done\1066_gt034_boot_video_retry.ps1: ffmpeg gdigrab
# is created with Win32_Process.Create and Win32_ProcessStartup.ShowWindow=0.
# After the process and output file are proven live, the PID-scoped window
# helper is called. Exit 2 is a warning only: a dirty recording is better than
# no recording. Any other hide-helper error is also a warning while ffmpeg is
# still alive; if ffmpeg died, boot must fail.
#
# BOOT USAGE (the caller writes the returned fields into its info file):
#   . (Join-Path $bridge 'staged\TEMPLATE_video_recorder.ps1')
#   $rec = Start-PfRoundRecorder -BridgeRoot $bridge `
#       -FfmpegPath $ffmpeg -FfprobePath $ffprobe -JobTag '1066_gt034' -FrameRate 30
#
# TEARDOWN USAGE (call after the game/server teardown, then grade ResultCode):
#   . (Join-Path $bridge 'staged\TEMPLATE_video_recorder.ps1')
#   $vr = Stop-PfRoundRecorder -BridgeRoot $bridge -VideoPid $videoPid `
#       -VideoStart $videoStart -VideoPath $videoFile -FfmpegPath $ffmpeg `
#       -FfprobePath $ffprobe -JobTag '1067_gt034_teardown'
#
# Stop-PfRoundRecorder always attempts frame proof after the recorder has
# stopped. It does not exit the teardown process; the caller decides how to
# combine ResultCode with the generic teardown result.

$ErrorActionPreference = 'Continue'

function Write-PfRecorderLog {
    param([Parameter(Mandatory = $true)][string]$Message)
    if (Test-Path Function:\W) { W $Message }
    else { Write-Host $Message }
}

function Start-PfRoundRecorder {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$BridgeRoot,
        [Parameter(Mandatory = $true)][string]$FfmpegPath,
        [Parameter(Mandatory = $true)][string]$FfprobePath,
        [Parameter(Mandatory = $true)][string]$JobTag,
        [ValidateRange(1, 60)][int]$FrameRate = 30,
        [ValidateRange(0, 86400)][int]$DurationSeconds = 0
    )

    foreach ($required in @(
        $FfmpegPath,
        $FfprobePath,
        (Join-Path $BridgeRoot 'agent_kit\pf_recorder_hide_window.ps1')
    )) {
        if (-not (Test-Path -LiteralPath $required)) {
            throw ("recorder dependency missing: {0}" -f $required)
        }
    }
    # Round videos are always local-only. Keep them outside evidence_screens,
    # whose contents are candidates for git sync under AGENTS.md section 5.
    $videoDir = Join-Path $BridgeRoot 'evidence_video'
    if (-not (Test-Path -LiteralPath $videoDir)) {
        New-Item -ItemType Directory -Path $videoDir -Force | Out-Null
    }

    $existing = @(Get-Process -Name 'ffmpeg' -ErrorAction SilentlyContinue)
    if ($existing.Count -ne 0) {
        throw ("recorder preflight found {0} existing ffmpeg process(es)" -f $existing.Count)
    }

    $stamp = (Get-Date).ToString(
        'yyyyMMdd_HHmmss',
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $safeTag = $JobTag -replace '[^A-Za-z0-9._-]', '_'
    $videoFile = Join-Path $videoDir ("{0}_FULLROUND_{1}.mkv" -f $safeTag, $stamp)
    $durationArg = ''
    if ($DurationSeconds -gt 0) { $durationArg = (' -t {0}' -f $DurationSeconds) }
    $videoCmd = (
        '"' + $FfmpegPath + '" -hide_banner -loglevel warning -y' +
        ' -f gdigrab -framerate ' + $FrameRate +
        ' -draw_mouse 1 -video_size 1920x1080 -i desktop' +
        $durationArg +
        ' -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p' +
        ' -f matroska "' + $videoFile + '"'
    )

    $startup = New-CimInstance -ClassName Win32_ProcessStartup `
        -Namespace root/cimv2 -ClientOnly -Property @{ ShowWindow = [uint16]0 }
    $created = Invoke-CimMethod -ClassName Win32_Process -MethodName Create `
        -Arguments @{
            CommandLine = $videoCmd
            CurrentDirectory = $videoDir
            ProcessStartupInformation = $startup
        }
    $videoPid = [int]$created.ProcessId
    Write-PfRecorderLog ("ffmpeg create rv={0} pid={1}" -f $created.ReturnValue, $videoPid)
    if ($created.ReturnValue -ne 0 -or $videoPid -le 0) {
        throw 'detached ffmpeg create failed'
    }

    Start-Sleep -Seconds 3
    $videoProcess = Get-Process -Id $videoPid -ErrorAction SilentlyContinue
    if (-not $videoProcess -or -not (Test-Path -LiteralPath $videoFile)) {
        if ($videoProcess) {
            Stop-Process -Id $videoPid -Force -ErrorAction SilentlyContinue
        }
        throw 'detached ffmpeg did not remain live or create its output file'
    }
    $videoStart = $videoProcess.StartTime.ToString(
        'yyyy-MM-ddTHH:mm:ss.fff',
        [System.Globalization.CultureInfo]::InvariantCulture
    )

    $hideOutput = @(
        & (Join-Path $BridgeRoot 'agent_kit\pf_recorder_hide_window.ps1') `
            -ProcessId $videoPid 2>&1
    )
    $hideRc = $LASTEXITCODE
    foreach ($line in $hideOutput) {
        Write-PfRecorderLog ("HIDE> {0}" -f [string]$line)
    }
    if ($hideRc -eq 2) {
        Write-PfRecorderLog 'VIDEO_WARN: ffmpeg window is still visible; round continues with dirty frames'
    } elseif ($hideRc -ne 0) {
        $stillLive = Get-Process -Id $videoPid -ErrorAction SilentlyContinue
        if (-not $stillLive) {
            throw ("hide helper exit {0} and ffmpeg is no longer alive" -f $hideRc)
        }
        Write-PfRecorderLog ("VIDEO_WARN: hide helper exit {0}; ffmpeg is alive, round continues" -f $hideRc)
    }

    Write-PfRecorderLog (
        "VIDEO START pid={0} start={1} fps={2} path={3}" -f
        $videoPid, $videoStart, $FrameRate, $videoFile
    )
    return [pscustomobject]@{
        VideoPid = $videoPid
        VideoStart = $videoStart
        VideoPath = $videoFile
        FrameRate = $FrameRate
        FfmpegPath = $FfmpegPath
        FfprobePath = $FfprobePath
        HideExitCode = $hideRc
    }
}

function Stop-PfRoundRecorder {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][string]$BridgeRoot,
        [Parameter(Mandatory = $true)][int]$VideoPid,
        [Parameter(Mandatory = $true)][string]$VideoStart,
        [Parameter(Mandatory = $true)][string]$VideoPath,
        [Parameter(Mandatory = $true)][string]$FfmpegPath,
        [Parameter(Mandatory = $true)][string]$FfprobePath,
        [Parameter(Mandatory = $true)][string]$JobTag
    )

    $resultCode = 0
    $process = Get-Process -Id $VideoPid -ErrorAction SilentlyContinue
    if ($process) {
        $actualStart = $process.StartTime.ToString(
            'yyyy-MM-ddTHH:mm:ss.fff',
            [System.Globalization.CultureInfo]::InvariantCulture
        )
        if ($process.ProcessName -ne 'ffmpeg' -or $actualStart -ne $VideoStart) {
            Write-PfRecorderLog (
                "VIDEO_ABORT: PID guard mismatch name={0} start={1} expected={2}" -f
                $process.ProcessName, $actualStart, $VideoStart
            )
            $resultCode = 32
        } else {
            $stamp = (Get-Date).ToString(
                'yyyyMMdd_HHmmss',
                [System.Globalization.CultureInfo]::InvariantCulture
            )
            $receipt = Join-Path $BridgeRoot ("outbox\{0}_ffmpeg_ctrlc_{1}.json" -f $JobTag, $stamp)
            & py -3 (Join-Path $BridgeRoot 'pf_stop_visible_server.py') `
                $VideoPid --json $receipt
            Write-PfRecorderLog ("VIDEO ctrl-c helper exit={0} receipt={1}" -f $LASTEXITCODE, $receipt)
            Start-Sleep -Seconds 4
            if (Get-Process -Id $VideoPid -ErrorAction SilentlyContinue) {
                Write-PfRecorderLog 'VIDEO_WARN: guarded force stop after Ctrl+C timeout'
                Stop-Process -Id $VideoPid -Force -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 2
            }
        }
    } else {
        Write-PfRecorderLog 'VIDEO_WARN: ffmpeg already exited before video stop'
    }

    if (Get-Process -Id $VideoPid -ErrorAction SilentlyContinue) {
        Write-PfRecorderLog ("VIDEO_FAIL: guarded ffmpeg pid remains={0}" -f $VideoPid)
        if ($resultCode -eq 0) { $resultCode = 33 }
    }

    $proofOutput = @()
    $proofRc = 0
    if (-not (Test-Path -LiteralPath $VideoPath)) {
        Write-PfRecorderLog ("VIDEO_FAIL: file missing path={0}" -f $VideoPath)
        $proofRc = 1
        if ($resultCode -eq 0) { $resultCode = 34 }
    } else {
        $oldPath = $env:Path
        try {
            $ffmpegDir = Split-Path -Parent $FfmpegPath
            $ffprobeDir = Split-Path -Parent $FfprobePath
            $env:Path = $ffmpegDir + ';' + $ffprobeDir + ';' + $oldPath
            $proofOutput = @(
                & (Join-Path $BridgeRoot 'agent_kit\pf_recorder_frame_proof.ps1') `
                    -VideoPath $VideoPath -JobTag $JobTag 2>&1
            )
            $proofRc = $LASTEXITCODE
        } finally {
            $env:Path = $oldPath
        }
        foreach ($line in $proofOutput) {
            Write-PfRecorderLog ("PROOF> {0}" -f [string]$line)
        }
        if ($proofRc -ne 0 -and $resultCode -eq 0) { $resultCode = 35 }
    }

    $proofPaths = @()
    foreach ($line in $proofOutput) {
        if ([string]$line -match ' path=(.+) bytes=') { $proofPaths += $matches[1] }
    }
    return [pscustomobject]@{
        ResultCode = $resultCode
        FrameProofExitCode = $proofRc
        VideoPath = $VideoPath
        ProofPaths = $proofPaths
    }
}
