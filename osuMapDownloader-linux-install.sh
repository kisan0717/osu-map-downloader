#!/usr/bin/env bash
# osuMapDownloader-linux-install.sh
# Installs the osuMapDownloader bundle system-wide into /opt/osuMapDownloader,
# symlinks the executable into /usr/bin, and registers it as the default
# HTTP/HTTPS handler on Linux (via xdg-utils).
#
# Run this from your project root after building with PyInstaller
# (it looks for dist/osuMapDownloader relative to this script, falling
# back to a copy sitting next to the script itself).
#
# Installing into /opt requires root, so this script will re-invoke
# itself with sudo for the copy step if it isn't already running as root.
#
# Run with:
#   chmod +x osuMapDownloader-linux-install.sh
#   ./osuMapDownloader-linux-install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXE_NAME="osuMapDownloader"
OPT_DIR="/opt/$EXE_NAME"
SYMLINK="/usr/bin/$EXE_NAME"

DIST_DIR="$SCRIPT_DIR/dist/$EXE_NAME"
LOCAL_DIR="$SCRIPT_DIR/$EXE_NAME"

if [ -d "$DIST_DIR" ]; then
	SOURCE_DIR="$DIST_DIR"
elif [ -d "$LOCAL_DIR" ]; then
	SOURCE_DIR="$LOCAL_DIR"
else
	echo "Error: Could not find $EXE_NAME directory in ./dist/ or next to this script." >&2
	echo "Build it with PyInstaller first:" >&2
	echo "  pyinstaller --clean --paths=. --onedir --noconsole --name osuMapDownloader Main.py" >&2
	exit 1
fi

DESKTOP_NAME="osuMapDownloader.desktop"
SOURCE_DESKTOP="$SCRIPT_DIR/$DESKTOP_NAME"

if [ ! -f "$SOURCE_DESKTOP" ]; then
	echo "Error: Could not find $DESKTOP_NAME next to this script." >&2
	exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
	rm -rf "$OPT_DIR"
	cp -r "$SOURCE_DIR" "$OPT_DIR"
	chmod +x "$OPT_DIR/$EXE_NAME"
	ln -sf "$OPT_DIR/$EXE_NAME" "$SYMLINK"
elif command -v sudo >/dev/null 2>&1; then
	echo "Installing to $OPT_DIR requires root privileges, requesting sudo..."
	sudo rm -rf "$OPT_DIR"
	sudo cp -r "$SOURCE_DIR" "$OPT_DIR"
	sudo chmod +x "$OPT_DIR/$EXE_NAME"
	sudo ln -sf "$OPT_DIR/$EXE_NAME" "$SYMLINK"
else
	echo "Error: Installing to $OPT_DIR requires root and sudo was not found." >&2
	echo "Re-run this script as root, e.g.: su -c '$0'" >&2
	exit 1
fi

echo "Installed to $OPT_DIR (symlinked from $SYMLINK)"

# --- .desktop file -----------------------------------------------------

DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/$DESKTOP_NAME"

mkdir -p "$DESKTOP_DIR"
cp -f "$SOURCE_DESKTOP" "$DESKTOP_FILE"

echo "Installed desktop entry to $DESKTOP_FILE"

# --- Refresh desktop database -------------------------------------------

if command -v update-desktop-database >/dev/null 2>&1; then
	update-desktop-database "$DESKTOP_DIR"
else
	echo "Warning: update-desktop-database not found, skipping refresh." >&2
fi

# --- Register as default HTTP/HTTPS handler ------------------------------

if command -v xdg-mime >/dev/null 2>&1; then
	xdg-mime default "$DESKTOP_NAME" x-scheme-handler/http
	xdg-mime default "$DESKTOP_NAME" x-scheme-handler/https
else
	echo "Warning: xdg-mime not found, could not register URL handler." >&2
fi

if command -v xdg-settings >/dev/null 2>&1; then
	xdg-settings set default-url-scheme-handler http "$DESKTOP_NAME" || true
	xdg-settings set default-url-scheme-handler https "$DESKTOP_NAME" || true
else
	echo "Warning: xdg-settings not found, could not set default URL scheme handler." >&2
fi

echo ""
echo "Registration complete."
echo "If your desktop environment does not pick up the new default automatically,"
echo "open your system's Default Applications settings and set"
echo "'osu! Map Downloader' as your default Web browser / URL handler."
