#!/bin/bash
# Setup script for Antigravity Agent Factory on Linux/WSL2

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_NAME="cursor-factory"

echo "=== Initializing Linux Environment for Antigravity Agent Factory ==="

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi

# Create and update environment
echo "Creating/Updating conda environment: $ENV_NAME..."
conda create -n $ENV_NAME python=3.10 -y
conda run -n $ENV_NAME pip install -r "$PROJECT_DIR/requirements.txt"
conda run -n $ENV_NAME pip install -r "$PROJECT_DIR/requirements-dev.txt"

echo "=== Environment Setup Complete ==="
echo "To activate:"
echo "conda activate $ENV_NAME"
