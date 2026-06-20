from modules.constants import DOWNLOAD_FILE_EXTENSION, BROWSER
from modules.helpers import openFile, openInBrowser

def getDownloadFilePath(path, downloads, preDownloadFiles):
	downloaded = ''

	if BROWSER == 'firefox':
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
		files = list(downloads.glob(f'*{DOWNLOAD_FILE_EXTENSION}'))

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
	openFile(downloaded)

	return True
