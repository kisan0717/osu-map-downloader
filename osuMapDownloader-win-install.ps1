# osuMapDownloader-win-install.ps1
# Installs the osuMapDownloader bundle into a per-user location and registers
# it as a candidate HTTP/HTTPS handler in Windows.
#
# Run this from your project root after building with PyInstaller
# (it looks for dist\osuMapDownloader relative to this script, falling
# back to a copy sitting next to the script itself).
#
# Run with:
#   powershell -ExecutionPolicy Bypass -File .\osuMapDownloader-win-install.ps1

$ErrorActionPreference = "Stop"

$exeName    = "osuMapDownloader.exe"
$installDir = Join-Path $env:LOCALAPPDATA "Programs\osuMapDownloader"
$targetExe  = Join-Path $installDir $exeName

$distDir  = Join-Path $PSScriptRoot "dist\osuMapDownloader"
$localDir = Join-Path $PSScriptRoot "osuMapDownloader"

if (Test-Path $distDir -PathType Container) {
	$sourceDir = $distDir
} elseif (Test-Path $localDir -PathType Container) {
	$sourceDir = $localDir
} else {
	Write-Error "Could not find osuMapDownloader directory in .\dist\ or next to this script. Build it with PyInstaller first (pyinstaller --clean --paths=. --onedir --noconsole --name osuMapDownloader Main.py)."
}

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Copy-Item -Path "$sourceDir\*" -Destination $installDir -Recurse -Force

Write-Host "Installed to $installDir"

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

$startMenuDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
$shortcutPath = Join-Path $startMenuDir "osu! Map Downloader.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetExe
$shortcut.WorkingDirectory = $installDir
$shortcut.Description = "Download osu! beatmaps"
$shortcut.Save()

Write-Host "Start Menu shortcut created."

Write-Host ""
Write-Host "Registration complete."
Write-Host "Now open Settings > Apps > Default Apps, search for 'osu! Map Downloader', and set it as your Web browser."
