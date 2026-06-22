import os

# Service name used to store credentials and settings
SERVICE = 'osuMapDownloader'

AVAILABLE_BROWSERS: list[str] = [
	'firefox',
	'google-chrome-stable',
	'microsoft-edge-stable',
	'brave-browser',
	'opera',
	'operagx',
	'vivaldi',
]

# File extensions browsers use when downloading files
DOWNLOAD_FILE_EXTENSIONS: dict[str, str] = {
	'firefox': '.part',
	'google-chrome-stable': '.crdownload',
	'microsoft-edge-stable': '.crdownload',
	'brave-browser': '.crdownload',
	'opera': '.crdownload',
	'operagx': '.crdownload',
	'vivaldi': '.crdownload',
}

# Flags to use when opening a url in browser
BROWSER_URL_FLAG: dict[str, str] = {
	'firefox': '-url',
}

# Executable name registered under the Windows 'App Paths' registry key
BROWSER_EXE_NAMES: dict[str, str] = {
	'firefox': 'firefox.exe',
	'google-chrome-stable': 'chrome.exe',
	'microsoft-edge-stable': 'msedge.exe',
	'brave-browser': 'brave.exe',
	'opera': 'opera.exe',
	'operagx': 'opera.exe',
	'vivaldi': 'vivaldi.exe',
}

# Common install locations, checked if PATH and registry lookups fail
BROWSER_FALLBACK_PATHS: dict[str, list[str]] = {
	'firefox': [
		r'C:\Program Files\Mozilla Firefox\firefox.exe',
		r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
	],
	'google-chrome-stable': [
		r'C:\Program Files\Google\Chrome\Application\chrome.exe',
		r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
		os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
	],
	'microsoft-edge-stable': [
		r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
		r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
	],
	'brave-browser': [
		r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
		r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe',
		os.path.expandvars(
			r'%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe'
		),
	],
	'opera': [
		os.path.expandvars(r'%LOCALAPPDATA%\Programs\Opera\opera.exe'),
		r'C:\Program Files\Opera\opera.exe',
		r'C:\Program Files (x86)\Opera\opera.exe',
	],
	'operagx': [
		os.path.expandvars(r'%LOCALAPPDATA%\Programs\Opera GX\opera.exe'),
		r'C:\Program Files\Opera GX\opera.exe',
		r'C:\Program Files (x86)\Opera GX\opera.exe',
	],
	'vivaldi': [
		os.path.expandvars(r'%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe'),
		r'C:\Program Files\Vivaldi\Application\vivaldi.exe',
	],
}
