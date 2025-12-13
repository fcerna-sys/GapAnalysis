$ErrorActionPreference = 'Stop'
$themeDir = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$blocksDir = Join-Path $themeDir 'tools\blocks'
New-Item -ItemType Directory -Force -Path $blocksDir | Out-Null
