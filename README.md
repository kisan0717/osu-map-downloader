# osu-map-downloader

Automatically download osu! beatmaps directly from osu! beatmap links and import them in osu!.

When an osu! beatmap URL is opened, the downloader can:

* Download the beatmap from multiple mirrors.
* Automatically import the downloaded map into osu!.
* Open the beatmap page in a browser instead.

---

> [!IMPORTANT]
> This application is built for players with slow internet and/or low-end hardware who can't really support osu! project to use osu!direct.
> 
> If you can, please consider supporting the osu! project:  
> https://osu.ppy.sh/home/support

## Supported URL Types
- `https://osu.ppy.sh/beatmaps/<id>`
- `https://osu.ppy.sh/b/<id>`
- `https://osu.ppy.sh/beatmapsets/<id>`
- `https://osu.ppy.sh/s/<id>`

## Installation

### Linux

- From Release: (unavailable right now)
  - Download the Linux zip file from the latest release.
  - Extract the contents into a directory.
  - Make the `Install.sh` executable as a program.
  - Run `Install.sh` with terminal.

- From Repo:
  - [Build](#Building) the executable.
  - Make the installation script executable as a program: `chmod +x osuMapDownloader-linux-install.sh`
  - Run the installation script: `./osuMapDownloader-linux-install.sh`

### Windows

- From Release: (unavailable right now)
  - Download the Windows zip file from the latest release.
  - Extract the contents into a directory.
  - Navigate to the directory in command prompt.
  - Run `powershell -ExecutionPolicy Bypass -File .\Install.ps1`
  - Set osu! Map Downloader as your default browser.

- From Repo:
  - [Build](#Building) the executable.
  - Run `powershell -ExecutionPolicy Bypass -File .\osuMapDownloader-win-install.ps1`
  - Set osu! Map Downloader as your default browser.

## Building

Clone the repository:

```bash
git clone https://github.com/Saurabh262004/osu-map-downloader
cd osu-map-downloader
```

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv

source .venv/bin/activate # for linux

.venv\Scripts\activate # for windows

pip install -r requirements.txt
```

Build the executable:

```bash
pyinstaller --clean --paths=. --onedir --noconsole --name osuMapDownloader Entry.py
```

The executable bundle will be created at:

```text
dist/osuMapDownloader/
```

---

## Manual Installation (Linux)

Install the bundle:

```bash
sudo cp -r dist/osuMapDownloader /opt/
sudo ln -sf /opt/osuMapDownloader/osuMapDownloader /usr/bin/osuMapDownloader
```

Install the .desktop file:

```bash
mkdir -p ~/.local/share/applications
cp osuMapDownloader.desktop ~/.local/share/applications/
```

Refresh the desktop database:

```bash
update-desktop-database ~/.local/share/applications
```

Register the application as the default HTTP/HTTPS handler:

```bash
xdg-settings set default-url-scheme-handler http osuMapDownloader
xdg-settings set default-url-scheme-handler https osuMapDownloader
```

---

## Configuration

Run the application without any arguments:

```bash
osuMapDownloader
```

This opens the settings window where you can:

* Enter osu! APIv2 credentials.
* Enable or disable automatic beatmap downloading.
* Set your default browser.

---

## Obtaining osu! API v2 Credentials

This application requires an osu! API v2 Client ID and Client Secret.

1. Sign in to your osu! account.
2. Open your account settings by clicking your profile picture in the top-right corner and selecting **Settings**.
3. Scroll to the bottom of the page until you find **OAuth**.
4. Click **New OAuth Application**.
5. Fill in the application details:

   * **Application Name:** Any name you like (for example, `osuMapDownloader`).
   * **Application Callback URL:** (you can keep this empty)
6. Save the application.
7. Copy the generated **Client ID** and **Client Secret**.
8. Open osuMapDownloader and select **Edit Credentials**.
9. Enter your Client ID and Client Secret.

The osu! API v2 credentials are used to get beatmapset ID from a beatmap ID when needed.
Your credentials will be stored securely using your system's keyring service.

## Usage

After installation, clicking an osu! beatmap link such as:

```text
https://osu.ppy.sh/beatmapsets/123456
```

will launch osuMapDownloader.

Depending on your settings, the application will either:

* Download the beatmap automatically.
* Ask whether to download the beatmap or open the page in a browser.

---

> [!NOTE]
>
> This application registers itself as the default handler for HTTP and HTTPS URLs.
>
> Every URL other than an osu beatmap / beatmapset URL is instantly forwarded to your configured web browser.
