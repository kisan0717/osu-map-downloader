import sys
from traceback import print_exc
from urllib.parse import urlparse
from Modules.Helpers import openInBrowser, resolveBeatmapsetID, getDownloadURL
from Modules.GUI import askBeatmapAction, createIdleWindow

def downloadBeatmapset(url: str, service: str):
	from Modules.DirectDownload import directDownloadProcess
	from Modules.Beatconnect import beatconnectProcess

	if service == 'beatconnect':
		return beatconnectProcess(url)

	if service in {'nerinyan', 'catboy', 'sayobot'}:
		return directDownloadProcess(url)

def startProcess(beatmapsetID: int):
	services = [
		'nerinyan',
		'catboy',
		'sayobot',
		'beatconnect'
	]

	for service in services:
		print(f'Trying {service}')

		try:
			downloadURL = getDownloadURL(
				beatmapsetID,
				service
			)

			if downloadBeatmapset(
				downloadURL,
				service
			):
				print(f'Success via {service}')
				return True

		except Exception as e:
			print(f'{service} failed:')
			print(e)
			print_exc()

	return False

def main(url):
	from Modules.Settings import getAutoDownload

	parsed = urlparse(url if '://' in url else f'https://{url}')
	path = parsed.path
	parts = path.strip('/').split('/')

	# check if it's a beatmap / beatmapset url
	is_beatmap_or_set = (
		parsed.netloc == 'osu.ppy.sh'
		and len(parts) >= 2
		and parts[0] in ('beatmaps', 'beatmapsets', 'b', 's')
		and parts[1].isdigit()
	)

	# if not, open it in the browser and return
	if not is_beatmap_or_set:
		print("not beatmapset url")
		openInBrowser(url)
		return None

	autoDownload = getAutoDownload() == '1'

	if autoDownload is False:
		# ask to either 1. download the beatmapset, 2. open the page in browser, 3. edit api credentials
		action = askBeatmapAction()

		if action is None:
			return None

		if action is False:
			print("opening in browser")
			openInBrowser(url)
			return None

	URLType = parts[0]
	beatmapsetID = int(parts[1])

	# it it's a beatmap url, get the beatmapset id via osu api v2
	if URLType == 'beatmaps' or URLType == 'b':
		print('resolving beatmapset id')
		beatmapsetID = resolveBeatmapsetID(beatmapsetID)
		print('done.')

	print(f'Beatmapset ID: {beatmapsetID}')

	# if the beatmapset id cannon be resolved, open the url in browser and return
	if beatmapsetID is None:
		print("beatmapset id could not be resolved")
		openInBrowser(url)
		return None

	try:
		downloadSuccess = startProcess(beatmapsetID)

		if not downloadSuccess:
			openInBrowser(url)

	except Exception as e:
		print('Something unexpected happened:')
		print(e)
		print('opening original url in the browser')
		openInBrowser(url)
