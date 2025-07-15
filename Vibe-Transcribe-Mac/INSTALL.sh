#!/bin/bash

echo "🌈 Installing Vibe Transcribe..."

# Check if Node.js is installed
if ! command -v node >/dev/null 2>&1; then
    echo "❌ Node.js is not installed."
    echo "Please install Node.js from: https://nodejs.org/"
    echo "Then run this installer again."
    exit 1
fi

# Check if Python/pip is available for Whisper
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python3 is not installed."
    echo "Please install Python3, then run: pip3 install openai-whisper"
    exit 1
fi

# Check if Whisper is installed
if ! command -v whisper >/dev/null 2>&1; then
    echo "⚠️  OpenAI Whisper is not installed."
    echo "Installing Whisper now..."
    pip3 install openai-whisper
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Whisper. Please run manually:"
        echo "pip3 install openai-whisper"
        exit 1
    fi
fi

# Install Node.js dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Installation complete!"
    echo ""
    echo "🎉 Vibe Transcribe is ready to use!"
    echo ""
    echo "To start the app:"
    echo "  • Double-click 'Vibe Transcribe.app'"
    echo "  OR"
    echo "  • Run: npm start"
    echo "  OR"
    echo "  • Run: ./start.sh"
    echo ""
    echo "The app will open at: http://localhost:3000"
else
    echo "❌ Installation failed. Please check your internet connection and try again."
    exit 1
fi
