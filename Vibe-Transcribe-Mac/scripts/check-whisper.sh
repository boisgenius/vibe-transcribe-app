#!/bin/bash

echo "=== Whisper Installation Check ==="
echo

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1)
    echo "✓ Python installed: $python_version"
else
    echo "✗ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo

# Check if pip is installed
echo "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    pip_version=$(pip3 --version 2>&1)
    echo "✓ pip installed: $pip_version"
else
    echo "✗ pip3 is not installed. Please install pip3."
    exit 1
fi

echo

# Check if Whisper is installed
echo "Checking Whisper installation..."
if command -v whisper &> /dev/null; then
    echo "✓ Whisper is installed"
    
    # Check Whisper version
    echo
    echo "Whisper details:"
    pip3 show openai-whisper 2>/dev/null || echo "Could not retrieve Whisper package details"
else
    echo "✗ Whisper is not installed."
    echo
    echo "To install Whisper, run:"
    echo "pip3 install openai-whisper"
    echo
    echo "Note: The installation may take several minutes and requires ~1-2GB of disk space."
    exit 1
fi

echo
echo "=== Available Whisper Models ==="
echo "tiny    - 39M parameters  (Fastest, least accurate)"
echo "base    - 74M parameters  (Good balance)"
echo "small   - 244M parameters (Better accuracy)"
echo "medium  - 769M parameters (Good accuracy)"
echo "large   - 1550M parameters (Best accuracy, slowest)"
echo "large-v3 - 1550M parameters (Latest version, best accuracy)"

echo
echo "=== System Requirements ==="
echo "RAM Requirements:"
echo "- tiny/base: ~1GB"
echo "- small: ~2GB"
echo "- medium: ~5GB"
echo "- large: ~10GB"

echo
echo "✓ All checks passed! Whisper is ready to use."