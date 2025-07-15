#!/bin/bash

echo "=== Whisper Functionality Test ==="
echo

# Check if Whisper is installed
if ! command -v whisper &> /dev/null; then
    echo "✗ Whisper is not installed. Please run check-whisper.sh first."
    exit 1
fi

# Create a test directory
TEST_DIR="whisper-test-$(date +%s)"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "Creating a test audio file..."

# Check if ffmpeg is available for generating test audio
if command -v ffmpeg &> /dev/null; then
    # Generate a simple test audio file with speech synthesis
    echo "Generating test audio with tone..."
    ffmpeg -f lavfi -i "sine=frequency=440:duration=3" -ac 1 -ar 16000 test_audio.wav -y 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✓ Test audio file created: test_audio.wav"
        
        echo
        echo "Running Whisper transcription test..."
        echo "Command: whisper test_audio.wav --model tiny --language en"
        
        # Run whisper on the test file
        whisper test_audio.wav --model tiny --language en 2>&1 | while IFS= read -r line; do
            echo "  $line"
        done
        
        # Check if output files were created
        echo
        echo "Checking output files..."
        if ls test_audio.* 2>/dev/null | grep -E '\.(txt|json|vtt|srt|tsv)$' > /dev/null; then
            echo "✓ Transcription files created:"
            ls test_audio.* | grep -E '\.(txt|json|vtt|srt|tsv)$' | while read file; do
                echo "  - $file"
            done
            echo
            echo "✓ Whisper is working correctly!"
        else
            echo "✗ No transcription files were created."
            echo "  This might indicate an issue with Whisper."
        fi
    else
        echo "✗ Failed to create test audio file"
    fi
else
    echo "⚠ ffmpeg not found. Cannot generate test audio."
    echo "  To test Whisper, place an audio file in the application and try transcribing it."
fi

# Cleanup
cd ..
rm -rf "$TEST_DIR"

echo
echo "Test completed."