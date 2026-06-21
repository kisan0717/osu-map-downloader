import subprocess
import platform
from Modules.Constants import BROWSER, BROWSER_URL_FLAG
from Modules.Credentials import getClient
from Modules.WindowsBrowsers import getBrowserPathWindows

def buildBrowserArgs(browser: str, browserPath: str, url: str) -> list[str]:
	flag = BROWSER_URL_FLAG.get(browser.lower())
	if flag:
		return [browserPath, flag, url]
	return [browserPath, url]

def openInBrowser(url: str):
	if platform.system() == "Windows":
		browserPath = getBrowserPathWindows(BROWSER)
		if browserPath:
			subprocess.Popen(buildBrowserArgs(BROWSER, browserPath, url))
			return

	subprocess.Popen(buildBrowserArgs(BROWSER, BROWSER, url))

def openFile(path: str):
	system = platform.system()

	if system == "Windows":
		subprocess.Popen([path], shell=True)

	elif system == "Darwin":
		subprocess.run(["open", path])

	else:
		subprocess.run(["xdg-open", path])

def resolveBeatmapsetID(beatmpID: int) -> int | None:
	client = getClient()

	try:
		return client.get_beatmap(
			beatmpID
		).beatmapset_id
	except:
		return None

def getDownloadURL(beatmapsetID: int, service: str) -> str:
	if service == 'beatconnect':
		return f'https://beatconnect.io/b/{beatmapsetID}'

	if service == 'nerinyan': # application/x-osu-beatmap-archive
		return f'http://dl.nerinyan.moe/v2/d/{beatmapsetID}?nv=1'

	if service == 'catboy': # application/x-osu-beatmap-archive
		return f'https://catboy.best/d/{beatmapsetID}'

	if service == 'sayobot': # application/octet-stream
		return f'https://dl.sayobot.cn/beatmaps/download/novideo/{beatmapsetID}'
