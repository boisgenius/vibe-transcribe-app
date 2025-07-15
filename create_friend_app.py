#!/usr/bin/env python3
"""
Create a friend-friendly version of the app that hides localhost completely
"""
import os
import shutil

def create_friend_app():
    app_name = "Vibe Transcribe"
    app_dir = f"{app_name} - Friend Edition.app"
    
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
    <string>vibe-transcribe-friend</string>
    <key>CFBundleIdentifier</key>
    <string>com.vibe.transcribe.friend</string>
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
</plist>'''
    
    with open(f"{app_dir}/Contents/Info.plist", 'w') as f:
        f.write(info_plist)
    
    # Create the friend-friendly launcher script
    launcher_script = f'''#!/bin/bash

# Vibe Transcribe - Friend Edition
# Hides all technical details from user

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
    show_error "Required components are missing. Please contact the app developer."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    show_error "App files not found. Please reinstall the application."
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    osascript -e "display dialog \\"Setting up Vibe Transcribe...\\\\nThis may take a few minutes on first run.\\" with title \\"Vibe Transcribe\\" buttons {{\\"OK\\"}} default button \\"OK\\" with icon note"
    npm install >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        show_error "Setup failed. Please check your internet connection and try again."
        exit 1
    fi
fi

# Check if Whisper is installed
if ! command_exists whisper; then
    show_error "Audio processing components are missing. Please contact the app developer."
    exit 1
fi

# Kill any existing server on port 3000
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Show friendly startup message
osascript -e "display dialog \\"🌈 Starting Vibe Transcribe...\\\\n\\\\nYour audio transcription app is loading!\\" with title \\"Vibe Transcribe\\" buttons {{\\"OK\\"}} default button \\"OK\\" with icon note giving up after 2"

# Start the server in background
npm start >/dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to start
if wait_for_server; then
    # Check if Chrome is available for app mode
    if command_exists "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; then
        # Open in Chrome app mode (no address bar, looks like native app)
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \\
            --app=http://localhost:3000 \\
            --disable-web-security \\
            --disable-features=TranslateUI \\
            --disable-extensions \\
            --disable-plugins \\
            --disable-default-apps \\
            --no-first-run \\
            --no-default-browser-check \\
            --window-size=1200,800 \\
            --window-position=100,100 \\
            >/dev/null 2>&1 &
    else
        # Fallback to Safari without toolbar
        osascript -e '
        tell application "Safari"
            activate
            make new document with properties {{URL:"http://localhost:3000"}}
            tell window 1
                set toolbar visible to false
                set current tab to tab 1
                do JavaScript "
                    document.addEventListener(\\"DOMContentLoaded\\", function() {{
                        document.title = \\"🌈 Vibe Transcribe\\";
                        // Remove any localhost references from UI
                        setTimeout(() => {{
                            var elements = document.querySelectorAll(\\"*\\");
                            elements.forEach(el => {{
                                if (el.textContent && el.textContent.includes(\\"localhost\\")) {{
                                    el.textContent = el.textContent.replace(/localhost:3000/g, \\"Vibe Transcribe\\");
                                }}
                            }});
                        }}, 1000);
                    }});
                " in current tab
            end tell
        end tell'
    fi
else
    show_error "Failed to start the application. Please try again."
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Keep the server running
wait $SERVER_PID
'''
    
    with open(f"{app_dir}/Contents/MacOS/vibe-transcribe-friend", 'w') as f:
        f.write(launcher_script)
    
    # Make the launcher executable
    os.chmod(f"{app_dir}/Contents/MacOS/vibe-transcribe-friend", 0o755)
    
    # Copy the icon
    icon_source = "vibe_icon.svg.png"
    if os.path.exists(icon_source):
        shutil.copy2(icon_source, f"{app_dir}/Contents/Resources/AppIcon.png")
    
    print(f"✅ Friend-friendly app created: {app_dir}")
    print("🎯 This version hides all technical details from users!")
    print("📱 Your friend will see a clean native-looking app")
    print("🚫 No localhost, no browser UI, no technical messages")

if __name__ == "__main__":
    create_friend_app()