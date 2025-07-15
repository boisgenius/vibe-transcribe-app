# Whisper Audio Transcription App

A local web application for audio transcription using OpenAI's Whisper model. Runs completely offline without any cloud API usage.

## Features

- **Drag-and-drop file upload** with support for multiple audio formats (MP3, WAV, M4A, FLAC, OGG, WEBM, MP4, OPUS)
- **Real-time progress tracking** during transcription
- **Multiple Whisper models** to choose from (tiny, base, small, medium, large-v3)
- **Language selection** with auto-detection support
- **Export options** for transcriptions (TXT and PDF)
- **Automatic cleanup** of temporary files
- **File validation** with 100MB size limit
- **Error handling** with user-friendly messages

## Prerequisites

- **macOS** with Node.js (v14+) and Python 3.8+ installed
- **OpenAI Whisper** installed via pip
- **ffmpeg** (optional, for test audio generation)

## Installation

1. **Install Whisper** (if not already installed):
   ```bash
   pip3 install openai-whisper
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Verify Whisper installation**:
   ```bash
   ./scripts/check-whisper.sh
   ```

## Usage

1. **Start the server**:
   ```bash
   npm start
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:3000
   ```

3. **Upload an audio file** by:
   - Dragging and dropping onto the upload area
   - Clicking "Browse Files" to select a file

4. **Select options**:
   - Choose a Whisper model (larger models are more accurate but slower)
   - Select language or use auto-detection

5. **Wait for transcription** - progress will be shown in real-time

6. **Download results** as TXT or PDF when complete

## Scripts

### Check Whisper Installation
```bash
./scripts/check-whisper.sh
```
Verifies that Python, pip, and Whisper are properly installed.

### Test Whisper Functionality
```bash
./scripts/test-whisper.sh
```
Runs a basic test to ensure Whisper is working correctly.

### Monitor Application
```bash
./scripts/monitor-app.sh
```
Checks server status, disk space, and file cleanup.

### Generate Test Audio Files
```bash
./scripts/generate-test-audio.sh
```
Creates synthetic test audio files (requires ffmpeg).

## Model Information

| Model    | Parameters | Speed    | Accuracy | RAM Usage |
|----------|------------|----------|----------|-----------|
| tiny     | 39M        | Fastest  | Lowest   | ~1GB      |
| base     | 74M        | Fast     | Good     | ~1GB      |
| small    | 244M       | Moderate | Better   | ~2GB      |
| medium   | 769M       | Slow     | Great    | ~5GB      |
| large-v3 | 1550M      | Slowest  | Best     | ~10GB     |

## Troubleshooting

### Whisper not found
If you get "whisper: command not found", ensure:
1. Whisper is installed: `pip3 install openai-whisper`
2. Python's bin directory is in your PATH

### Server won't start
1. Check if port 3000 is already in use
2. Ensure all dependencies are installed: `npm install`

### Transcription fails
1. Check available disk space
2. Ensure the audio file is valid and not corrupted
3. Try a smaller model if running out of memory

### No progress updates
Some audio formats may not show real-time progress. The transcription is still running - please wait.

## File Structure

```
whisper-transcription-app/
├── server/
│   └── app.js           # Express server
├── public/
│   ├── index.html       # Frontend HTML
│   ├── styles.css       # Styling
│   └── script.js        # Frontend JavaScript
├── uploads/             # Temporary upload storage
├── transcriptions/      # Generated transcriptions
├── scripts/             # Utility scripts
├── test-audio/          # Test audio files
└── package.json         # Node.js dependencies
```

## Security Notes

- This app runs completely offline
- No data is sent to any external services
- Uploaded files are automatically deleted after processing
- All transcriptions are stored locally

## License

MIT