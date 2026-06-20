from pathlib import Path
import requests
import zipfile
from Modules.Helpers import openFile

def directDownloadProcess(downloadURL: str):
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

	# disable openign the file for debugging
	# openFile(str(filePath))

	return True
