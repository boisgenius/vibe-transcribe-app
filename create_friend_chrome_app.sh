#!/bin/bash

# Create a friend-ready Chrome App Mode version
# This version hides all technical details and localhost references

APP_NAME="Vibe Transcribe"
FRIEND_APP_DIR="$APP_NAME - Share Version.app"

# Remove existing app if it exists
if [ -d "$FRIEND_APP_DIR" ]; then
    rm -rf "$FRIEND_APP_DIR"
fi

# Create app bundle structure
mkdir -p "$FRIEND_APP_DIR/Contents/MacOS"
mkdir -p "$FRIEND_APP_DIR/Contents/Resources"

# Create Info.plist
cat > "$FRIEND_APP_DIR/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>vibe-transcribe-share</string>
    <key>CFBundleIdentifier</key>
    <string>com.vibe.transcribe.share</string>
    <key>CFBundleName</key>
    <string>Vibe Transcribe</string>
    <key>CFBundleDisplayName</key>
    <string>🌈 Vibe Transcribe</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>CFBundleIconFile</key>
    <string>AppIcon.png</string>
</dict>
</plist>
EOF

# Create the friend-friendly launcher script
cat > "$FRIEND_APP_DIR/Contents/MacOS/vibe-transcribe-share" << 'EOF'
#!/bin/bash

# Vibe Transcribe - Share Version
# Optimized for sharing with friends - hides all technical details

# Set up proper PATH
export PATH="/Users/bozhang/.local/bin:/Users/bozhang/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# Get the directory where the actual app files are located
APP_DIR="/Users/bozhang/vibe-transcribe-app"
cd "$APP_DIR"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to show friendly error dialog
show_friendly_error() {
    osascript -e "display dialog \"$1\" with title \"Vibe Transcribe\" buttons {\"OK\"} default button \"OK\" with icon stop"
}

# Function to wait for server to start
wait_for_server() {
    for i in {1..30}; do
        if curl -s http://localhost:3000 >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
    done
    return 1
}

# Check if required components are available
if ! command_exists node; then
    show_friendly_error "Vibe Transcribe needs to be set up first. Please contact the person who shared this app with you."
    exit 1
fi

if ! command_exists whisper; then
    show_friendly_error "Audio processing components are missing. Please contact the person who shared this app with you."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    show_friendly_error "App files not found. Please make sure Vibe Transcribe is properly installed."
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    osascript -e "display dialog \"Setting up Vibe Transcribe for first use...\\nThis will take a moment.\" with title \"Vibe Transcribe\" buttons {\"OK\"} default button \"OK\" with icon note"
    npm install >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        show_friendly_error "Setup failed. Please check your internet connection and try again."
        exit 1
    fi
fi

# Kill any existing server
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Show friendly startup message
osascript -e "display dialog \"🌈 Starting Vibe Transcribe...\\n\\nYour audio transcription app is loading!\" with title \"Vibe Transcribe\" buttons {\"OK\"} default button \"OK\" with icon note giving up after 2"

# Start the server in background
npm start >/dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to be ready
if wait_for_server; then
    # Check if Chrome is available
    if command_exists "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; then
        # Open in Chrome App Mode - looks like a native desktop app
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
            --app=http://localhost:3000 \
            --disable-web-security \
            --disable-features=TranslateUI \
            --disable-extensions \
            --disable-plugins \
            --disable-default-apps \
            --no-first-run \
            --no-default-browser-check \
            --window-size=1200,800 \
            --window-position=100,100 \
            --disable-dev-shm-usage \
            --disable-gpu \
            --no-sandbox \
            --app-auto-launched \
            --disable-background-mode \
            >/dev/null 2>&1 &
    else
        show_friendly_error "Google Chrome is required for the best experience. Please install Chrome and try again."
        kill $SERVER_PID 2>/dev/null || true
        exit 1
    fi
else
    show_friendly_error "Failed to start Vibe Transcribe. Please try again."
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Keep the server running
wait $SERVER_PID
EOF

# Make the launcher executable
chmod +x "$FRIEND_APP_DIR/Contents/MacOS/vibe-transcribe-share"

# Copy the icon if it exists
if [ -f "vibe_icon.svg.png" ]; then
    cp "vibe_icon.svg.png" "$FRIEND_APP_DIR/Contents/Resources/AppIcon.png"
fi

echo "✅ Friend-ready Chrome App Mode created: $FRIEND_APP_DIR"
echo "🎯 Features:"
echo "   - Chrome App Mode (looks like native app)"
echo "   - No localhost visible to user"
echo "   - No browser UI (address bar, bookmarks, etc.)"
echo "   - Friendly error messages"
echo "   - Clean startup experience"
echo ""
echo "📱 Your friend will see a native-looking desktop app!"
echo "🚫 No technical details, no localhost, no browser UI"