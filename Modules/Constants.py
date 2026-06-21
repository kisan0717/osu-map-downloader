import os

SERVICE = 'osuMapDownloader'

BROWSER = 'firefox'

DOWNLOAD_FILE_EXTENSION = '.osz.part'

BROWSER_URL_FLAG = {
	"firefox": "-url",
}

# Executable name registered under the Windows "App Paths" registry key
BROWSER_EXE_NAMES: dict[str, str] = {
	"firefox": "firefox.exe",
	"chrome": "chrome.exe",
	"edge": "msedge.exe",
	"brave": "brave.exe",
	"opera": "opera.exe",
	"operagx": "opera.exe",
	"vivaldi": "vivaldi.exe",
}

# Common install locations, checked if PATH and registry lookups fail
BROWSER_FALLBACK_PATHS: dict[str, list[str]] = {
	"firefox": [
		r"C:\Program Files\Mozilla Firefox\firefox.exe",
		r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
	],
	"chrome": [
		r"C:\Program Files\Google\Chrome\Application\chrome.exe",
		r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
		os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
	],
	"edge": [
		r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
		r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
	],
	"brave": [
		r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
		r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
		os.path.expandvars(
			r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"
		),
	],
	"opera": [
		os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\opera.exe"),
		r"C:\Program Files\Opera\opera.exe",
		r"C:\Program Files (x86)\Opera\opera.exe",
	],
	"vivaldi": [
		os.path.expandvars(r"%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe"),
		r"C:\Program Files\Vivaldi\Application\vivaldi.exe",
	],
}
