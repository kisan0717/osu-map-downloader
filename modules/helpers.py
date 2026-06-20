import subprocess
import os
import platform
from modules.credentials import getClient
from modules.constants import BROWSER

def openInBrowser(url: str):
	subprocess.Popen([
		BROWSER,
		url
	])

def openFile(path: str):
	system = platform.system()

	if system == "Windows":
		os.startfile(path)

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
