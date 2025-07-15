#!/bin/bash

echo "=== Generating Test Audio Files ==="
echo

# Create test-audio directory
TEST_AUDIO_DIR="test-audio"
mkdir -p "$TEST_AUDIO_DIR"

# Check if ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "✗ ffmpeg is not installed."
    echo "  To install ffmpeg on macOS, run: brew install ffmpeg"
    echo
    echo "  Without ffmpeg, you'll need to provide your own test audio files."
    exit 1
fi

echo "Using ffmpeg to generate test audio files..."
echo

# Generate different test audio files
echo "1. Generating short tone (3 seconds)..."
ffmpeg -f lavfi -i "sine=frequency=440:duration=3" -ac 1 -ar 16000 "$TEST_AUDIO_DIR/test_tone_3s.wav" -y 2>/dev/null
echo "   ✓ Created: test_tone_3s.wav"

echo "2. Generating medium tone (10 seconds)..."
ffmpeg -f lavfi -i "sine=frequency=880:duration=10" -ac 1 -ar 16000 "$TEST_AUDIO_DIR/test_tone_10s.wav" -y 2>/dev/null
echo "   ✓ Created: test_tone_10s.wav"

echo "3. Generating complex tone pattern (20 seconds)..."
ffmpeg -f lavfi -i "sine=frequency=440:duration=5,sine=frequency=880:duration=5,sine=frequency=1320:duration=5,sine=frequency=440:duration=5" -filter_complex "[0][1][2][3]concat=n=4:v=0:a=1" -ac 1 -ar 16000 "$TEST_AUDIO_DIR/test_pattern_20s.wav" -y 2>/dev/null
echo "   ✓ Created: test_pattern_20s.wav"

echo "4. Generating white noise (5 seconds)..."
ffmpeg -f lavfi -i "anoisesrc=duration=5" -ac 1 -ar 16000 "$TEST_AUDIO_DIR/test_noise_5s.wav" -y 2>/dev/null
echo "   ✓ Created: test_noise_5s.wav"

# Convert one to MP3 format
echo "5. Converting to MP3 format..."
ffmpeg -i "$TEST_AUDIO_DIR/test_tone_3s.wav" -acodec mp3 "$TEST_AUDIO_DIR/test_tone_3s.mp3" -y 2>/dev/null
echo "   ✓ Created: test_tone_3s.mp3"

# Convert one to M4A format
echo "6. Converting to M4A format..."
ffmpeg -i "$TEST_AUDIO_DIR/test_tone_10s.wav" -c:a aac "$TEST_AUDIO_DIR/test_tone_10s.m4a" -y 2>/dev/null
echo "   ✓ Created: test_tone_10s.m4a"

echo
echo "=== Test Audio Files Created ==="
echo "Location: $TEST_AUDIO_DIR/"
ls -lh "$TEST_AUDIO_DIR"

echo
echo "Note: These are synthetic audio files without speech."
echo "For real transcription testing, use actual speech recordings."
echo
echo "To download sample speech files, you can use:"
echo "- LibriVox (public domain audiobooks): https://librivox.org"
echo "- Common Voice dataset: https://commonvoice.mozilla.org"
echo "- Or record your own voice using QuickTime Player or Voice Memos on macOS"