import tkinter as tk
from tkinter import ttk
import keyring
from Modules.Constants import SERVICE, AVAILABLE_BROWSERS
from Modules.Settings import getAutoDownload, toggleAutoDownload, getDefaultBrowser, setDefaultBrowser

# tk gui for asking to either 1. download beatmap, 2. open url in browser
def askBeatmapAction() -> bool | None:
	root = tk.Tk()
	root.title("osu! Map Downloader")
	root.resizable(False, False)

	style = ttk.Style(root)
	style.theme_use("clam")

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

	main = ttk.Frame(root, padding=20)
	main.grid()

	title = ttk.Label(
		main,
		text="Beatmap detected. What would you like to do?",
		font=("Segoe UI", 10, "bold")
	)
	title.grid(row=0, column=0, columnspan=3, pady=(0, 12))

	# buttons row
	btn_frame = ttk.Frame(main)
	btn_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))

	ttk.Button(
		btn_frame,
		text="Open Page",
		command=openPage,
		width=14
	).grid(row=0, column=0, padx=5)

	ttk.Button(
		btn_frame,
		text="Download",
		command=download,
		width=14
	).grid(row=0, column=1, padx=5)

	autoDownloadVar = tk.BooleanVar(value=getAutoDownload() == '1')

	auto_check = ttk.Checkbutton(
		main,
		text="Automatically download beatmaps",
		variable=autoDownloadVar,
		command=toggleAutoDownload
	)

	auto_check.grid(row=2, column=0, columnspan=3, pady=(5, 0))

	root.protocol("WM_DELETE_WINDOW", cancel)

	root.mainloop()
	return result

# tk gui for editing credentials
def editCredentials():
	root = tk.Tk()
	root.title("osu! API Credentials")
	root.resizable(False, False)

	style = ttk.Style(root)
	style.theme_use("clam")

	main = ttk.Frame(root, padding=20)
	main.grid()

	title = ttk.Label(
		main,
		text="API Credentials",
		font=("Segoe UI", 10, "bold")
	)
	title.grid(row=0, column=0, columnspan=2, pady=(0, 12))

	ttk.Label(main, text="Client ID").grid(
		row=1, column=0, sticky="w", pady=5
	)

	clientIDEntry = ttk.Entry(main, width=35)
	clientIDEntry.grid(row=1, column=1, pady=5)

	ttk.Label(main, text="Client Secret").grid(
		row=2, column=0, sticky="w", pady=5
	)

	clientSecretEntry = ttk.Entry(main, width=35, show="*")
	clientSecretEntry.grid(row=2, column=1, pady=5)

	clientID = keyring.get_password(SERVICE, 'client_id')
	clientSecret = keyring.get_password(SERVICE, 'client_secret')

	if clientID:
		clientIDEntry.insert(0, clientID)
	if clientSecret:
		clientSecretEntry.insert(0, clientSecret)

	def save():
		keyring.set_password(SERVICE, 'client_id', clientIDEntry.get().strip())
		keyring.set_password(SERVICE, 'client_secret', clientSecretEntry.get().strip())
		root.destroy()

	ttk.Button(
		main,
		text="Save",
		command=save
	).grid(row=3, column=0, columnspan=2, pady=(15, 0))

	root.mainloop()

def createIdleWindow():
	root = tk.Tk()
	root.title("osu! Map Downloader")
	root.resizable(False, False)

	style = ttk.Style(root)
	style.theme_use("clam")  #"alt", "default", "clam", "vista" (windows)

	main = ttk.Frame(root, padding=20)
	main.grid()

	# Title
	title = ttk.Label(
		main,
		text="What would you like to do?",
		font=("Segoe UI", 11, "bold")
	)
	title.grid(row=0, column=0, columnspan=2, pady=(0, 12))

	# Edit Crerentials Button
	edit_btn = ttk.Button(
		main,
		text="Edit Credentials",
		command=editCredentials
	)
	edit_btn.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

	# Default Browser Dropdown
	ttk.Label(
		main,
		text="Default browser:"
	).grid(row=2, column=0, sticky="w", pady=(0, 5))

	browserVar = tk.StringVar(value=getDefaultBrowser())

	browserDropdown = ttk.Combobox(
		main,
		textvariable=browserVar,
		values=AVAILABLE_BROWSERS,
		state="readonly",
		width=18
	)

	browserDropdown.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

	def onBrowserSelected(_event):
		setDefaultBrowser(browserVar.get())

	browserDropdown.bind("<<ComboboxSelected>>", onBrowserSelected)

	# Auto Download Checkbox
	autoDownloadVar = tk.BooleanVar(value=getAutoDownload() == '1')

	auto_check = ttk.Checkbutton(
		main,
		text="Automatically download beatmaps",
		variable=autoDownloadVar,
		command=toggleAutoDownload
	)
	auto_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 12))

	# small spacing consistency
	for i in range(2):
		main.columnconfigure(i, weight=1)

	root.mainloop()
