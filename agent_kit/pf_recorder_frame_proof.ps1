# pf_recorder_frame_proof.ps1 - pull still frames out of a round recording so the
# evidence that matters can travel where the video cannot.
#
# WHY THIS EXISTS
#   Round videos are large (GT-034 round 1066 = 56 MB for 165 s) and AGENTS.md
#   forbids pushing them to git.  Frames are small and evidence_screens\ is one
#   of the two folders pf_git_sync.ps1 is allowed to commit, so a frame reaches
#   the chief and the cloud while the video stays on this disk.
#   It is also the check that the recorder console really was hidden: pull a
#   frame and look at the middle of the picture.
#
# USAGE
#   .\pf_recorder_frame_proof.ps1 -VideoPath "...\GT034_FULLROUND_1066_x.mkv" -JobTag 1066
#   .\pf_recorder_frame_proof.ps1 -VideoPath "..." -JobTag 1066 -At 5,30,120
#   .\pf_recorder_frame_proof.ps1 -VideoPath "..." -JobTag 1066 -EverySeconds 30
#
#   -At            seconds from the start of the clip; default 5, mid, end-3
#   -EverySeconds  overrides -At and samples the whole clip on a fixed step
#   -MaxFrames     hard cap so a long clip cannot flood evidence_screens (default 12)
#
# OUTPUT
#   evidence_screens\FRAME_<JobTag>_<seconds>s_<stamp>.png  plus one manifest
#   line per frame on stdout: path, seconds, bytes, sha256.
#
# EXIT CODES
#   0 every requested frame was written
#   1 ffmpeg or ffprobe missing, or the video does not exist
#   2 at least one frame failed to extract
#
# ASCII only; never writes outside evidence_screens\; never touches the video.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$VideoPath,
    [Parameter(Mandatory = $true)][string]$JobTag,
    [double[]]$At,
    [double]$EverySeconds = 0,
    [int]$MaxFrames = 12,
    [string]$EvidenceDir
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $VideoPath)) {
    Write-Output ("FRAME_PROOF=NO_VIDEO path={0}" -f $VideoPath); exit 1
}
$ff = Get-Command ffmpeg -ErrorAction SilentlyContinue
$fp = Get-Command ffprobe -ErrorAction SilentlyContinue
if (-not $ff -or -not $fp) { Write-Output 'FRAME_PROOF=NO_FFMPEG'; exit 1 }

if (-not $EvidenceDir) {
    $EvidenceDir = Join-Path (Split-Path -Parent (Split-Path -Parent $VideoPath)) 'evidence_screens'
    if (-not (Test-Path -LiteralPath $EvidenceDir)) {
        $EvidenceDir = Split-Path -Parent $VideoPath
    }
}
if (-not (Test-Path -LiteralPath $EvidenceDir)) {
    New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null
}

$durRaw = & $fp.Source -v error -show_entries format=duration -of default=nw=1:nk=1 "$VideoPath" 2>&1
$dur = 0.0
[void][double]::TryParse(([string]$durRaw).Trim(), [ref]$dur)
if ($dur -le 0) { Write-Output ("FRAME_PROOF=NO_DURATION raw={0}" -f $durRaw); exit 1 }
Write-Output ("FRAME_PROOF video={0} duration_s={1:N3}" -f $VideoPath, $dur)

if ($EverySeconds -gt 0) {
    $marks = @()
    for ($t = 0.0; $t -lt $dur; $t += $EverySeconds) { $marks += [math]::Round($t, 3) }
} elseif ($At) {
    $marks = @($At)
} else {
    $marks = @(5.0, [math]::Round($dur / 2.0, 3), [math]::Round([math]::Max($dur - 3.0, 0.0), 3))
}

$marks = @($marks | Where-Object { $_ -ge 0 -and $_ -lt $dur } | Sort-Object -Unique)
if ($marks.Count -gt $MaxFrames) {
    Write-Output ("FRAME_PROOF NOTE requested={0} capped_to={1} - frames beyond the cap were NOT taken" -f $marks.Count, $MaxFrames)
    $marks = @($marks | Select-Object -First $MaxFrames)
}

$stamp = (Get-Date).ToString('yyyyMMdd_HHmmss', [System.Globalization.CultureInfo]::InvariantCulture)
$failed = 0
foreach ($m in $marks) {
    $name = ('FRAME_{0}_{1}s_{2}.png' -f $JobTag, ([string]$m).Replace('.', 'p'), $stamp)
    $out = Join-Path $EvidenceDir $name
    # -ss before -i seeks fast; -frames:v 1 takes exactly one picture.
    $null = & $ff.Source -hide_banner -loglevel error -y -ss $m -i "$VideoPath" -frames:v 1 "$out" 2>&1
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $out)) {
        Write-Output ("FRAME at={0}s STATUS=FAIL" -f $m); $failed++; continue
    }
    $len = (Get-Item -LiteralPath $out).Length
    $sha = (Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash
    Write-Output ("FRAME at={0}s path={1} bytes={2} sha256={3}" -f $m, $out, $len, $sha)
}

Write-Output ("FRAME_PROOF requested={0} failed={1}" -f $marks.Count, $failed)
if ($failed -gt 0) { Write-Output 'FRAME_PROOF=PARTIAL'; exit 2 }
Write-Output 'FRAME_PROOF=OK'
exit 0
