import os
import platform
from Modules.Constants import BROWSER_EXE_NAMES, BROWSER_FALLBACK_PATHS

try:
	import winreg
except ImportError:
	winreg = None  # Not on Windows

def whichPathOnly(name: str) -> str | None:
	path_env = os.environ.get("PATH", "")
	if platform.system() == "Windows":
		pathext = os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD")
		exts = [e for e in pathext.split(os.pathsep) if e]
	else:
		exts = [""]

	for directory in path_env.split(os.pathsep):
		if not directory:
			continue
		base = os.path.join(directory, name)
		candidates = [base] if os.path.splitext(name)[1] else [base + ext for ext in exts]
		for candidate in candidates:
			if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
				return candidate
	return None


def getBrowserPathWindows(browser: str) -> str | None:
	browser = browser.lower()
	exe_name = BROWSER_EXE_NAMES.get(browser)

	# 1. Check if it's already resolvable on PATH (current directory excluded)
	if exe_name:
		path = whichPathOnly(exe_name)
		if path:
			return path
	path = whichPathOnly(browser)
	if path:
		return path

	# 2. Check the Windows registry "App Paths" key (HKLM, then HKCU)
	if winreg is not None and exe_name:
		for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
			try:
				key = winreg.OpenKey(
					hive,
					r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\%s"
					% exe_name,
				)
				value, _ = winreg.QueryValueEx(key, None)
				if value and os.path.exists(value):
					return value
			except OSError:
				continue

	# 3. Fall back to well-known install locations
	for guess in BROWSER_FALLBACK_PATHS.get(browser, []):
		if guess and os.path.exists(guess):
			return guess

	return None

def findAllBrowsersWindows() -> dict[str, str | None]:
	"""Return {browser_name: path_or_None} for every known browser."""
	return {name: getBrowserPathWindows(name) for name in BROWSER_EXE_NAMES}
