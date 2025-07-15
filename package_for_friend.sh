#!/bin/bash

# Vibe Transcribe - Package for Friend
# Creates a distributable package for Mac users

echo "🌈 Creating Vibe Transcribe package for your friend..."

# Create package directory
PACKAGE_NAME="Vibe-Transcribe-Mac"
rm -rf "$PACKAGE_NAME"
mkdir "$PACKAGE_NAME"

# Copy essential files (exclude node_modules, logs, uploads, transcriptions)
echo "📦 Packaging files..."

# Core application files
cp -r public "$PACKAGE_NAME/"
cp -r server "$PACKAGE_NAME/"
cp -r scripts "$PACKAGE_NAME/"
cp package.json "$PACKAGE_NAME/"
cp package-lock.json "$PACKAGE_NAME/"
cp README.md "$PACKAGE_NAME/"
cp .gitignore "$PACKAGE_NAME/"
cp transcribe-direct.js "$PACKAGE_NAME/"

# Copy the Mac app bundle
cp -r "Vibe Transcribe.app" "$PACKAGE_NAME/"

# Create a simple installer script
cat > "$PACKAGE_NAME/INSTALL.sh" << 'EOF'
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
EOF

# Create a simple start script
cat > "$PACKAGE_NAME/start.sh" << 'EOF'
#!/bin/bash

echo "🌈 Starting Vibe Transcribe..."

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "Dependencies not found. Running installer first..."
    ./INSTALL.sh
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

# Kill any existing server
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo "Server starting at: http://localhost:3000"
echo "Press Ctrl+C to stop"

# Start the server and open browser
npm start &
sleep 3
open http://localhost:3000

# Wait for the server process
wait
EOF

# Make scripts executable
chmod +x "$PACKAGE_NAME/INSTALL.sh"
chmod +x "$PACKAGE_NAME/start.sh"

# Create a README for your friend
cat > "$PACKAGE_NAME/README_FOR_FRIEND.md" << 'EOF'
# 🌈 Vibe Transcribe App

Welcome to Vibe Transcribe! This is a beautiful audio transcription app that runs locally on your Mac.

## 🚀 Quick Start

### Option 1: Double-click to run (Recommended)
1. Double-click `Vibe Transcribe.app`
2. The app will automatically start and open in your browser
3. Start transcribing! 🎉

### Option 2: Manual installation
1. Open Terminal and navigate to this folder
2. Run: `./INSTALL.sh`
3. Run: `./start.sh` or `npm start`

## ✨ Features

- 🎨 **Beautiful gradient UI** inspired by modern tech brands
- 🎵 **Drag & drop audio files** (MP3, WAV, M4A, FLAC, etc.)
- 🧠 **Multiple AI models** (tiny to large-v3)
- 🌍 **Language detection** or manual selection  
- 📄 **Export to TXT/PDF**
- 🔒 **100% local** - no data sent to cloud
- 🧹 **Auto cleanup** of temporary files

## 📋 Requirements

- macOS 10.13 or later
- Node.js (will guide you to install if missing)
- OpenAI Whisper (auto-installed)

## 🆘 Troubleshooting

**App won't start?**
- Make sure Node.js is installed: https://nodejs.org/
- Run `./INSTALL.sh` in Terminal

**"Whisper not found" error?**
- Run: `pip3 install openai-whisper`

**Port 3000 already in use?**
- Run: `lsof -ti:3000 | xargs kill -9`

## 💝 From Your Friend

This app was built with love and powered by OpenAI Whisper AI. Enjoy transcribing! 

If you have any issues, let me know! 
EOF

# Create a nice package
echo "🎁 Creating final package..."

# Compress everything
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"

echo "✅ Package created successfully!"
echo ""
echo "📦 Your friend can use:"
echo "   ${PACKAGE_NAME}.tar.gz"
echo ""
echo "📋 Instructions for your friend:"
echo "   1. Download and extract ${PACKAGE_NAME}.tar.gz"
echo "   2. Double-click 'Vibe Transcribe.app' to run"
echo "   3. If that doesn't work, open Terminal and run './INSTALL.sh'"
echo ""
echo "🎉 All done! Your friend will love this app!"