#!/bin/bash
# Migration script to move project from /mnt/ to native Linux home

WINDOWS_VERSION_PATH="/mnt/d/Users/wpoga/Documents/Python Scripts/antigravity-agent-factory"
LINUX_TARGET_DIR="$HOME/projects/antigravity-agent-factory"

echo "=== Project Migration: Windows Mount -> Linux Native ==="

if [ ! -d "$WINDOWS_VERSION_PATH" ]; then
    echo "Error: Project not found at $WINDOWS_VERSION_PATH"
    echo "Please ensure your D: drive is mounted under /mnt/d/"
    exit 1
fi

echo "Creating target directory: $LINUX_TARGET_DIR"
mkdir -p "$HOME/projects"

echo "Copying files (this may take a moment)..."
cp -r "$WINDOWS_VERSION_PATH" "$HOME/projects/"

echo "Fixing permissions..."
sudo chown -R $USER:$USER "$LINUX_TARGET_DIR"
chmod -R 755 "$LINUX_TARGET_DIR"

echo "=== Migration Complete ==="
echo "Project is now available at: $LINUX_TARGET_DIR"
echo "Next step: Run 'bash ops/setup_linux.sh' inside the new directory."
