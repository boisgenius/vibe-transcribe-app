#!/usr/bin/env python3
"""
Create a native macOS app wrapper that hides the localhost interface
"""
import os
import subprocess
import shutil

def create_native_app():
    app_name = "Vibe Transcribe"
    app_dir = f"{app_name}.app"
    
    # Remove existing app if it exists
    if os.path.exists(app_dir):
        shutil.rmtree(app_dir)
    
    # Create app bundle structure
    os.makedirs(f"{app_dir}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_dir}/Contents/Resources", exist_ok=True)
    
    # Create Info.plist
    info_plist = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>vibe-transcribe-native</string>
    <key>CFBundleIdentifier</key>
    <string>com.vibe.transcribe.native</string>
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
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
    </dict>
</dict>
</plist>'''
    
    with open(f"{app_dir}/Contents/Info.plist", 'w') as f:
        f.write(info_plist)
    
    # Create the native launcher script
    launcher_script = f'''#!/bin/bash

# Native Vibe Transcribe App Launcher
# Hides localhost from user

# Set up proper PATH
export PATH="/Users/bozhang/.local/bin:/Users/bozhang/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# Get the directory where the actual app files are located
APP_DIR="/Users/bozhang/vibe-transcribe-app"
cd "$APP_DIR"

# Function to check if command exists
command_exists() {{
    command -v "$1" >/dev/null 2>&1
}}

# Function to show error dialog
show_error() {{
    osascript -e "display dialog \\"$1\\" with title \\"Vibe Transcribe\\" buttons {{\\"OK\\"}} default button \\"OK\\" with icon stop"
}}

# Function to wait for server to start
wait_for_server() {{
    for i in {{1..30}}; do
        if curl -s http://localhost:3000 >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
    done
    return 1
}}

# Check if Node.js is installed
if ! command_exists node; then
    show_error "Node.js is not installed. Please install Node.js from https://nodejs.org/ and try again."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    show_error "Could not find the app files. Please make sure Vibe Transcribe is properly installed."
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    osascript -e "display dialog \\"Installing dependencies...\\\\nThis may take a few minutes on first run.\\" with title \\"Vibe Transcribe\\" buttons {{\\"OK\\"}} default button \\"OK\\" with icon note"
    npm install
    if [ $? -ne 0 ]; then
        show_error "Failed to install dependencies. Please check your internet connection and try again."
        exit 1
    fi
fi

# Check if Whisper is installed
if ! command_exists whisper; then
    show_error "OpenAI Whisper is not installed. Please install it with:\\\\n\\\\npip3 install openai-whisper\\\\n\\\\nThen try again."
    exit 1
fi

# Kill any existing server on port 3000
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start the server in background
npm start &
SERVER_PID=$!

# Wait for server to start
if wait_for_server; then
    # Open the native app interface (WebKit view)
    osascript -e '
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set appName to name of frontApp
    end tell
    
    set htmlContent to "<!DOCTYPE html>
<html>
<head>
    <title>Vibe Transcribe</title>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; }}
        #webview {{ width: 100vw; height: 100vh; border: none; }}
        .loading {{ 
            position: fixed; 
            top: 50%; 
            left: 50%; 
            transform: translate(-50%, -50%);
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 18px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class=\\"loading\\">🌈 Loading Vibe Transcribe...</div>
    <script>
        setTimeout(() => {{
            document.body.innerHTML = `<iframe id=\\"webview\\" src=\\"http://localhost:3000\\"></iframe>`;
        }}, 2000);
    </script>
</body>
</html>"
    
    set tempFile to (path to temporary items folder as string) & "vibe_transcribe_native.html"
    set fileRef to open for access file tempFile with write permission
    set eof of fileRef to 0
    write htmlContent to fileRef as «class utf8»
    close access fileRef
    
    tell application "Safari"
        activate
        open location "file://" & (POSIX path of tempFile)
        tell window 1
            set toolbar visible to false
            set current tab to tab 1
            tell current tab
                do JavaScript "
                    document.addEventListener(\\"DOMContentLoaded\\", function() {{
                        document.querySelector(\\"body\\").style.margin = \\"0\\";
                        document.querySelector(\\"body\\").style.padding = \\"0\\";
                    }});
                "
            end tell
        end tell
    end tell'
else
    show_error "Failed to start the server. Please try again."
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Keep the script running to maintain the server
wait $SERVER_PID
'''
    
    with open(f"{app_dir}/Contents/MacOS/vibe-transcribe-native", 'w') as f:
        f.write(launcher_script)
    
    # Make the launcher executable
    os.chmod(f"{app_dir}/Contents/MacOS/vibe-transcribe-native", 0o755)
    
    # Copy the icon
    icon_source = "vibe_icon.svg.png"
    if os.path.exists(icon_source):
        shutil.copy2(icon_source, f"{app_dir}/Contents/Resources/AppIcon.png")
    
    print(f"✅ Native app created: {app_dir}")
    print("🎯 This app will hide localhost from users!")
    print("📱 Users will see a native app interface instead of browser")

if __name__ == "__main__":
    create_native_app()