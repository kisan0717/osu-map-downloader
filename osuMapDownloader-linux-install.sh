#!/usr/bin/env bash
# osuMapDownloader-linux-install.sh
# Installs the osuMapDownloader binary system-wide into /usr/bin and registers
# it as the default HTTP/HTTPS handler on Linux (via xdg-utils).
#
# Run this from your project root after building with PyInstaller
# (it looks for dist/osuMapDownloader relative to this script, falling
# back to a copy sitting next to the script itself).
#
# Installing into /usr/bin requires root, so this script will re-invoke
# itself with sudo for the copy step if it isn't already running as root.
#
# Run with:
#   chmod +x osuMapDownloader-linux-install.sh
#   ./osuMapDownloader-linux-install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXE_NAME="osuMapDownloader"
INSTALL_DIR="/usr/bin"
TARGET_EXE="$INSTALL_DIR/$EXE_NAME"

DIST_EXE="$SCRIPT_DIR/dist/$EXE_NAME"
LOCAL_EXE="$SCRIPT_DIR/$EXE_NAME"

if [ -f "$DIST_EXE" ]; then
	SOURCE_EXE="$DIST_EXE"
elif [ -f "$LOCAL_EXE" ]; then
	SOURCE_EXE="$LOCAL_EXE"
else
	echo "Error: Could not find $EXE_NAME in ./dist/ or next to this script." >&2
	echo "Build it with PyInstaller first:" >&2
	echo "  pyinstaller --clean --paths=. --onefile --noconsole --name osuMapDownloader Main.py" >&2
	exit 1
fi

DESKTOP_NAME="osuMapDownloader.desktop"
SOURCE_DESKTOP="$SCRIPT_DIR/$DESKTOP_NAME"

if [ ! -f "$SOURCE_DESKTOP" ]; then
	echo "Error: Could not find $DESKTOP_NAME next to this script." >&2
	exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
	cp -f "$SOURCE_EXE" "$TARGET_EXE"
	chmod +x "$TARGET_EXE"
elif command -v sudo >/dev/null 2>&1; then
	echo "Installing to $INSTALL_DIR requires root privileges, requesting sudo..."
	sudo cp -f "$SOURCE_EXE" "$TARGET_EXE"
	sudo chmod +x "$TARGET_EXE"
else
	echo "Error: Installing to $INSTALL_DIR requires root and sudo was not found." >&2
	echo "Re-run this script as root, e.g.: su -c '$0'" >&2
	exit 1
fi

echo "Installed to $TARGET_EXE"

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
