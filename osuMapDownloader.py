#!/home/saurabh26/.local/bin/.venv/bin/python

import sys
import subprocess
from urllib.parse import urlparse
import tkinter as tk
import keyring

SERVICE = 'osuMapDownloader'

browser = 'firefox' # 'google-chrome-stable'
downloadFileExtension = '.osz.part' # '.crdownload'

# ask user for credentials via tk gui and store them with keyring
def getCredentials():
	clientID = keyring.get_password(
		SERVICE,
		'client_id'
	)

	clientSecret = keyring.get_password(
		SERVICE,
		'client_secret'
	)

	if not clientID or not clientSecret:
		editCredentials()

		clientID = keyring.get_password(
			SERVICE,
			'client_id'
		)

		clientSecret = keyring.get_password(
			SERVICE,
			'client_secret'
		)

	return clientID, clientSecret

# tk gui for editing credentials
def editCredentials():
	root = tk.Tk()
	root.title("osu! API Credentials")
	root.resizable(False, False)

	tk.Label(root, text="Client ID").grid(
		row=0,
		column=0,
		padx=10,
		pady=(10, 5),
		sticky='w'
	)

	clientIDEntry = tk.Entry(root, width=40)
	clientIDEntry.grid(
		row=0,
		column=1,
		padx=10,
		pady=(10, 5)
	)

	tk.Label(root, text="Client Secret").grid(
		row=1,
		column=0,
		padx=10,
		pady=5,
		sticky='w'
	)

	clientSecretEntry = tk.Entry(
		root,
		width=40,
		show='*'
	)

	clientSecretEntry.grid(
		row=1,
		column=1,
		padx=10,
		pady=5
	)

	clientID = keyring.get_password(
		SERVICE,
		'client_id'
	)

	clientSecret = keyring.get_password(
		SERVICE,
		'client_secret'
	)

	if clientID:
		clientIDEntry.insert(0, clientID)

	if clientSecret:
		clientSecretEntry.insert(0, clientSecret)

	# save the new credentials
	def save():
		keyring.set_password(
			SERVICE,
			'client_id',
			clientIDEntry.get().strip()
		)

		keyring.set_password(
			SERVICE,
			'client_secret',
			clientSecretEntry.get().strip()
		)

		root.destroy()

	tk.Button(
		root,
		text="Save",
		command=save
	).grid(
		row=2,
		column=0,
		columnspan=2,
		pady=10
	)

	root.mainloop()

# get osu client from credentials
def getClient():
	import osu

	clientID, clientSecret = getCredentials()

	client = osu.Client.from_credentials(
		clientID,
		clientSecret,
		None
	)

	return client

# get a beatmapset id from beatmap id via osu api v2
def resolveBeatmapsetID(beatmpID: int) -> int | None:
	client = getClient()

	try:
		return client.get_beatmap(
			beatmpID
		).beatmapset_id
	except:
		return None

# tk gui for asking 1. download beatmap, 2. open url in browser, 3, edit credentials
def askBeatmapAction() -> bool | None:
	root = tk.Tk()
	root.title("osu! Map Downloader")
	root.resizable(False, False)

	result = None

	def download():
		nonlocal result
		result = True
		root.destroy()

	def openPage():
		nonlocal result
		result = False
		root.destroy()

	def cancel():
		root.destroy()

	tk.Label(
		root,
		text="Beatmap detected. What would you like to do?"
	).pack(
		padx=20,
		pady=(15, 10)
	)

	frame = tk.Frame(root)
	frame.pack(pady=(0, 5))

	tk.Button(
		frame,
		text="Open Page",
		command=openPage,
		width=12
	).pack(
		side=tk.LEFT,
		padx=5
	)

	tk.Button(
		frame,
		text="Download",
		command=download,
		width=12
	).pack(
		side=tk.LEFT,
		padx=5
	)

	tk.Button(
		frame,
		text="Edit Credentials",
		command=editCredentials,
		width=12
	).pack(
		side=tk.LEFT,
		padx=5
	)

	root.protocol(
		"WM_DELETE_WINDOW",
		cancel
	)

	root.mainloop()

	return result

def openInBrowser(url: str):
	subprocess.Popen([
		browser,
		url
	])

def getDownloadURL(beatmapsetID: int, service: str) -> str:
	if service == 'beatconnect':
		return f'https://beatconnect.io/b/{beatmapsetID}'

	if service == 'nerinyan': # application/x-osu-beatmap-archive
		return f'http://dl.nerinyan.moe/v2/d/{beatmapsetID}?nv=1'

	if service == 'catboy': # application/x-osu-beatmap-archive
		return f'https://catboy.best/d/{beatmapsetID}'

	if service == 'sayobot': # application/octet-stream
		return f'https://dl.sayobot.cn/beatmaps/download/novideo/{beatmapsetID}'

def getDownloadFilePath(path, downloads, preDownloadFiles):
	global browser
	downloaded = ''

	if browser == 'firefox':
		# split path by '.'
		pathSplit = str(path).split('.')

		# remove the random string firefox adds after first '.'
		pathSplit.pop(1)

		# remove part extension
		pathSplit.pop(-1)

		# return joined path by '.'
		downloaded = '.'.join(pathSplit)

	else:
		# list .osz files after download
		postDownloadFiles = set(downloads.glob("*.osz"))

		# get the new .osz files
		newFiles = postDownloadFiles - preDownloadFiles

		# if there's more than one or 0 new .osz files, return False
		if len(newFiles) != 1:
			return False

		# return singular downloaded file path
		downloaded = str(next(iter(newFiles)))

	return downloaded

def downloadBeatmapset(url: str, service: str):
	if service == 'beatconnect':
		return beatconnectProcess(url)

	if service in {'nerinyan', 'catboy', 'sayobot'}:
		return directDownloadProcess(url)

def beatconnectProcess(downloadURL: str):
	from pathlib import Path
	import time

	# get default Downloads path
	downloads = Path.home() / "Downloads"

	# list any .osz files in the Downloads folder before starting download
	preDownloadFiles = set(downloads.glob("*.osz"))

	# open the download link in browser
	openInBrowser(downloadURL)

	partFile = None

	waitDownloadStart = 150 # wait 15s to start download
	waitDownloadFinish = 400 # wait 40s to finish download

	# wait a certain ammount of time for the download to start
	for _ in range(waitDownloadStart):
		files = list(downloads.glob(f'*{downloadFileExtension}'))

		# if new .osz download files are found, list the first one and exit loop
		if files:

			partFile = files[0]
			break

		time.sleep(0.1)

	# if no files are being downloaded, return False
	if not partFile:
		print('No download detected, opening original url in browser')
		return False

	partFileExists = True

	# wait a certain ammount of time for the download to finish
	for _ in range(waitDownloadFinish):
		# if the part file has disappeared, assume the download has finished and exit loop
		if not partFile.exists():
			partFileExists = False
			break

		time.sleep(0.1)

	# if part file hasn't disappeared in time, assume something went wrong and return False
	if partFileExists:
		print('Download did not complete in time, opening original url in browser')
		return False

	# file path for the downloaded .osz file
	downloaded = getDownloadFilePath(partFile, downloads, preDownloadFiles)

	if downloaded is False:
		print('Could not resolve downloaded files path, opening original url in browser')
		return False

	# open the downloaded .osz file
	subprocess.Popen([
		"xdg-open",
		downloaded
	])

	return True

def directDownloadProcess(downloadURL: str):
	from pathlib import Path
	import requests
	import zipfile

	downloads = Path.home() / "Downloads"

	response = requests.get(
		downloadURL,
		headers={
			"User-Agent": (
				"Mozilla/5.0 (X11; Linux x86_64; rv:149.0) "
				"Gecko/20100101 Firefox/149.0"
			)
		},
		allow_redirects=True,
		stream=True
	)

	response.raise_for_status()

	contentType = (
		response.headers
		.get("Content-Type", "")
		.split(";")[0]
	)

	if contentType not in {
		"application/x-osu-beatmap-archive",
		"application/octet-stream",
		"application/zip"
	}:
		print(f"Unexpected content type: {contentType}")
		return False

	filename = "beatmap.osz"

	contentDisposition = response.headers.get(
		"Content-Disposition"
	)

	if (contentDisposition and ("filename=" in contentDisposition)):
		filename = (
			contentDisposition
			.split("filename=")[1]
			.strip('"')
		)

	filePath = downloads / filename

	with open(filePath, "wb") as f:
		for chunk in response.iter_content(
			chunk_size=8192
		):
			if chunk:
				f.write(chunk)

	try:
		with zipfile.ZipFile(filePath) as z:
			hasOSU = any(
				name.endswith(".osu")
				for name in z.namelist()
			)

		if not hasOSU:
			print("Downloaded archive contains no .osu files")
			filePath.unlink(missing_ok=True)
			return False

	except zipfile.BadZipFile:
		print("Downloaded file is not a valid zip")
		filePath.unlink(missing_ok=True)
		return False

	subprocess.Popen([
		"xdg-open",
		str(filePath)
	])

	return True

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

	return False

def main(url):
	path = urlparse(url).path
	parts = path.strip('/').split('/')

	# check if it's a beatmap / beatmapset url
	is_beatmapset = (
		len(parts) >= 2
		and (parts[0] == 'beatmapsets' or parts[0] == 'beatmaps')
		and parts[1].isdigit()
	)

	# if not, open it in the browser and return
	if not is_beatmapset:
		print("not beatmapset url")
		openInBrowser(url)
		return None

	# ask to either 1. download the beatmapset, 2. open the page in browser, 3. edit api credentials
	action = askBeatmapAction()

	if action is False:
		print("opening in browser")
		openInBrowser(url)
		return None

	if action is None:
		return None

	URLType = parts[0]
	beatmapsetID = int(parts[1])

	# it it's a beatmap url, get the beatmapset id via osu api v2
	if URLType == 'beatmaps':
		print('resolving beatmapset id')
		beatmapsetID = resolveBeatmapsetID(beatmapsetID)
		print('done.')

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

# check if we got any arguments, if so run the main function and pass the argument to it
if len(sys.argv) > 1:
	main(sys.argv[1])
