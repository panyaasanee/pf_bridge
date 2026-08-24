$ErrorActionPreference = 'Stop'
$root = 'C:\Users\Panya\Desktop\Pirate Force'
$ext = Join-Path $root 'pf_bridge\external'
$game = Join-Path $root 'GameClient'
$tool = Join-Path $ext 'pf_validate_capture_fields.py'
$out = Join-Path $root 'pf_bridge\outbox'
$log = Join-Path $out 'GT047_capture_validate_baseline.log.txt'
$files = @(
  (Join-Path $ext 'PF_PROTOCOL_REGISTRY.tsv'),
  (Join-Path $ext 'PF_SERIALIZER_FIELDS.tsv'),
  (Join-Path $ext 'PF_TAG_CENSUS.tsv'),
  (Join-Path $ext 'PF_INPUT_INVENTORY.tsv'),
  (Join-Path $game 'GameClient.local.bin')
)
Write-Output 'JOB=GT047-CAPTURE-VALIDATE-BASELINE'
foreach ($path in $files) {
  $item = Get-Item -LiteralPath $path
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
  Write-Output ("BEFORE path={0} size={1} sha256={2}" -f $path,$item.Length,$hash)
}
& py -3 $tool --game-client $game --external $ext 2>&1 | Tee-Object -FilePath $log
$rc = $LASTEXITCODE
Write-Output ("VALIDATOR_EXIT={0}" -f $rc)
foreach ($path in $files) {
  $item = Get-Item -LiteralPath $path
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
  Write-Output ("AFTER path={0} size={1} sha256={2}" -f $path,$item.Length,$hash)
}
Write-Output ("LOG={0}" -f $log)
exit $rc
