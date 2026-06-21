# osuMapDownloader-win-install.ps1
# Installs osuMapDownloader.exe into a per-user location and registers it
# as a candidate HTTP/HTTPS handler in Windows.
#
# Run this from your project root after building with PyInstaller
# (it looks for dist\osuMapDownloader.exe relative to this script, falling
# back to a copy sitting next to the script itself).
#
# Run with:
#   powershell -ExecutionPolicy Bypass -File .\osuMapDownloader-win-install.ps1

$ErrorActionPreference = "Stop"

$installDir = Join-Path $env:LOCALAPPDATA "Programs\osuMapDownloader"
$exeName    = "osuMapDownloader.exe"
$targetExe  = Join-Path $installDir $exeName

$distExe   = Join-Path $PSScriptRoot "dist\$exeName"
$localExe  = Join-Path $PSScriptRoot $exeName

if (Test-Path $distExe) {
	$sourceExe = $distExe
} elseif (Test-Path $localExe) {
	$sourceExe = $localExe
} else {
	Write-Error "Could not find $exeName in .\dist\ or next to this script. Build it with PyInstaller first (pyinstaller --clean --paths=. --onefile --noconsole --name osuMapDownloader Main.py)."
}

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Copy-Item -Path $sourceExe -Destination $targetExe -Force

Write-Host "Installed to $targetExe"

$commandValue = '"' + $targetExe + '" "%1"'

New-Item -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader" -Force | Out-Null
Set-Item -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader" -Value "osu! Map Downloader"

New-Item -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities" -Name "ApplicationName" -Value "osu! Map Downloader"
Set-ItemProperty -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities" -Name "ApplicationDescription" -Value "Download osu! beatmaps directly from osu! beatmap links"

New-Item -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities\URLAssociations" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities\URLAssociations" -Name "http" -Value "osuMapDownloaderURL"
Set-ItemProperty -Path "HKCU:\Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities\URLAssociations" -Name "https" -Value "osuMapDownloaderURL"

New-Item -Path "HKCU:\Software\Classes\osuMapDownloaderURL\shell\open\command" -Force | Out-Null
Set-Item -Path "HKCU:\Software\Classes\osuMapDownloaderURL\shell\open\command" -Value $commandValue

New-Item -Path "HKCU:\Software\RegisteredApplications" -Force | Out-Null
Set-ItemProperty -Path "HKCU:\Software\RegisteredApplications" -Name "osuMapDownloader" -Value "Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities"

Write-Host ""
Write-Host "Registration complete."
Write-Host "Now open Settings > Apps > Default Apps, search for 'osu! Map Downloader', and set it as your Web browser."
