<#
.SYNOPSIS
  Windows 打包脚本：生成便携版和 exe 安装版，并用 7z 加密压缩。

.EXAMPLE
  .\build_windows.ps1                       # 打包便携版 + 安装版
  .\build_windows.ps1 -Target portable      # 只打包便携版
  .\build_windows.ps1 -Target installer     # 只打包安装版
  .\build_windows.ps1 -InstallDeps          # 先 pip install -r requirements.txt
  .\build_windows.ps1 -SkipBuild            # 跳过 PyInstaller，直接用现有 dist\文字转音频

  产物在 dist\release\：
    txt2au-<版本>-windows-portable.7z   便携版（解压即用）
    txt2au-<版本>-windows-setup.7z      安装版（内含 setup.exe）

  依赖：Python、7-Zip、Inno Setup 6（仅安装版需要）。
  winget install 7zip.7zip JRSoftware.InnoSetup
#>
param(
    [ValidateSet('all', 'portable', 'installer')]
    [string]$Target = 'all',
    [string]$Version = '',
    [string]$Password = '123',
    [switch]$InstallDeps,
    [switch]$SkipBuild
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$Root = $PSScriptRoot
Set-Location $Root

$AppName = '文字转音频'
$DistApp = Join-Path $Root "dist\$AppName"
$ReleaseDir = Join-Path $Root 'dist\release'

function Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }

function Invoke-Native {
    param([string]$Exe, [string[]]$Arguments)
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Exe 执行失败，退出码 $LASTEXITCODE" }
}

function Find-Tool {
    param([string]$Name, [string[]]$Candidates)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($c in $Candidates) {
        if ($c -and (Test-Path $c)) { return $c }
    }
    return $null
}

# ---------- 版本号 ----------
if (-not $Version) {
    $m = Select-String -Path (Join-Path $Root 'app.py') -Pattern "APP_VERSION\s*=\s*['""]([^'""]+)['""]" | Select-Object -First 1
    if (-not $m) { throw '无法从 app.py 读取 APP_VERSION，请用 -Version 指定' }
    $Version = $m.Matches[0].Groups[1].Value
}
$Version = $Version.TrimStart('v')
Step "版本: $Version  目标: $Target"

# ---------- 工具检查 ----------
$SevenZip = Find-Tool '7z' @(
    "$env:ProgramFiles\7-Zip\7z.exe",
    "${env:ProgramFiles(x86)}\7-Zip\7z.exe"
)
if (-not $SevenZip) { throw '未找到 7-Zip，请先安装: winget install 7zip.7zip' }

$Iscc = $null
if ($Target -in 'all', 'installer') {
    $Iscc = Find-Tool 'ISCC' @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
        "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
    )
    if (-not $Iscc) { throw '未找到 Inno Setup 6 (ISCC.exe)，请先安装: winget install JRSoftware.InnoSetup' }
}

# ---------- PyInstaller ----------
if ($InstallDeps) {
    Step '安装依赖'
    Invoke-Native python @('-m', 'pip', 'install', '--upgrade', 'pip')
    Invoke-Native python @('-m', 'pip', 'install', '-r', 'requirements.txt')
}

if (-not $SkipBuild) {
    Step 'PyInstaller 打包'
    Invoke-Native python @('-m', 'PyInstaller', 'build.spec', '--noconfirm', '--clean')
}
if (-not (Test-Path (Join-Path $DistApp "$AppName.exe"))) {
    throw "未找到 $DistApp\$AppName.exe，PyInstaller 打包可能失败"
}

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null

function New-EncryptedArchive {
    param([string]$Archive, [string]$Source)
    if (Test-Path $Archive) { Remove-Item $Archive -Force }
    # -mhe=on 同时加密文件名
    Invoke-Native $SevenZip @('a', '-t7z', '-mx=9', '-mhe=on', "-p$Password", $Archive, $Source)
}

# ---------- 便携版 ----------
if ($Target -in 'all', 'portable') {
    Step '生成便携版 7z'
    $portable = Join-Path $ReleaseDir "txt2au-$Version-windows-portable.7z"
    New-EncryptedArchive $portable $DistApp
    Write-Host "便携版: $portable" -ForegroundColor Green
}

# ---------- 安装版 ----------
if ($Target -in 'all', 'installer') {
    Step 'Inno Setup 生成安装程序'
    $setupExe = Join-Path $ReleaseDir "txt2au-$Version-windows-setup.exe"
    if (Test-Path $setupExe) { Remove-Item $setupExe -Force }
    Invoke-Native $Iscc @(
        "/DAppVersion=$Version",
        "/DSourceDir=$DistApp",
        "/DOutputDir=$ReleaseDir",
        (Join-Path $Root 'installer\txt2au.iss')
    )

    Step '生成安装版 7z'
    $setupArchive = Join-Path $ReleaseDir "txt2au-$Version-windows-setup.7z"
    New-EncryptedArchive $setupArchive $setupExe
    Remove-Item $setupExe -Force
    Write-Host "安装版: $setupArchive" -ForegroundColor Green
}

Step "完成，产物目录: $ReleaseDir"
Get-ChildItem $ReleaseDir | Format-Table Name, Length -AutoSize
