#!/usr/bin/env bash
# ------------------------------------------------------------
# Quick start script for the Florence‑2‑base‑ft demo repository
# ------------------------------------------------------------
# This script performs the following steps:
#   1. Clone the repository (you can provide a custom URL).
#   2. Create and activate a Python virtual environment.
#   3. Install required dependencies.
#   4. Run the demo script (yolo.py) on a sample image.
# ------------------------------------------------------------

# ----------- Configuration -----------------------------------
# Repository URL – change if you fork/host elsewhere
REPO_URL="https://github.com/yourusername/yolo.git"
# Destination directory (default: current directory "yolo-demo")
DEST_DIR="yolo-demo"
# Sample image – ensure it exists in the repo or provide your own path
IMAGE="yolo2.png"
# ------------------------------------------------------------

set -e

echo "=== Cloning repository ==="
if [ -d "$DEST_DIR" ]; then
  echo "Directory $DEST_DIR already exists. Removing..."
  rm -rf "$DEST_DIR"
fi

git clone "$REPO_URL" "$DEST_DIR"
cd "$DEST_DIR"

echo "=== Setting up virtual environment ==="
python3 -m venv .venv
source .venv/bin/activate

echo "=== Installing dependencies ==="
# If requirements.txt exists, use it; otherwise install minimal deps
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  pip install torch transformers Pillow
fi

echo "=== Running demo ==="
python yolo.py --image "$IMAGE"

echo "=== Done ==="
