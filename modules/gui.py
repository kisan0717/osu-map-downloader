import tkinter as tk
import keyring
from modules.constants import SERVICE
from modules.settings import getAutoDownload, toggleAutoDownload

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

	autoDownloadVar = tk.BooleanVar(
		value=getAutoDownload() == '1'
	)

	tk.Checkbutton(
		root,
		text="Automatically download beatmaps",
		variable=autoDownloadVar,
		command=toggleAutoDownload
	).pack(
		pady=(10, 10)
	)

	root.protocol(
		"WM_DELETE_WINDOW",
		cancel
	)

	root.mainloop()

	return result

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

def createIdleWindow():
	root = tk.Tk()
	root.title("osu! Map Downloader")
	root.resizable(False, False)

	tk.Label(
		root,
		text="What would you like to do?"
	).pack(
		padx=20,
		pady=(15, 10)
	)

	tk.Button(
		root,
		text="Edit Credentials",
		command=editCredentials
	).pack(
		pady=(0, 10)
	)

	autoDownloadVar = tk.BooleanVar(
		value=getAutoDownload() == '1'
	)

	tk.Checkbutton(
		root,
		text="Automatically download beatmaps",
		variable=autoDownloadVar,
		command=toggleAutoDownload
	).pack(
		pady=(0, 15)
	)

	root.mainloop()
