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
