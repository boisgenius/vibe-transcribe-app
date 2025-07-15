#!/bin/bash

echo "=== Whisper Transcription App Monitor ==="
echo

# Check if Node.js is running
echo "Checking Node.js server..."
if pgrep -f "node.*server/app.js" > /dev/null; then
    echo "✓ Node.js server is running"
    
    # Get the PID and port
    PID=$(pgrep -f "node.*server/app.js")
    echo "  PID: $PID"
    
    # Try to find the port
    if command -v lsof &> /dev/null; then
        PORT=$(lsof -Pan -p $PID -i | grep LISTEN | awk '{print $9}' | cut -d: -f2 | head -1)
        if [ ! -z "$PORT" ]; then
            echo "  Port: $PORT"
            echo "  URL: http://localhost:$PORT"
        fi
    fi
else
    echo "✗ Node.js server is not running"
    echo "  To start the server, run: npm start"
fi

echo

# Check disk space for uploads and transcriptions
echo "Checking disk space..."
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_AVAIL=$(df -h . | awk 'NR==2 {print $4}')

if [ "$DISK_USAGE" -gt 90 ]; then
    echo "⚠ Warning: Disk usage is high ($DISK_USAGE%)"
    echo "  Available space: $DISK_AVAIL"
else
    echo "✓ Disk space available: $DISK_AVAIL ($DISK_USAGE% used)"
fi

echo

# Check upload directory
echo "Checking upload directory..."
UPLOAD_DIR="uploads"
if [ -d "$UPLOAD_DIR" ]; then
    FILE_COUNT=$(find "$UPLOAD_DIR" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [ "$FILE_COUNT" -gt 0 ]; then
        echo "✓ Upload directory exists"
        echo "  Files in upload directory: $FILE_COUNT"
        
        # Check for old files (older than 1 hour)
        OLD_FILES=$(find "$UPLOAD_DIR" -type f -mmin +60 2>/dev/null | wc -l | tr -d ' ')
        if [ "$OLD_FILES" -gt 0 ]; then
            echo "  ⚠ Old files found: $OLD_FILES files older than 1 hour"
        fi
    else
        echo "✓ Upload directory is clean"
    fi
else
    echo "ℹ Upload directory not found (will be created when needed)"
fi

echo

# Check transcription directory
echo "Checking transcription directory..."
TRANS_DIR="transcriptions"
if [ -d "$TRANS_DIR" ]; then
    FILE_COUNT=$(find "$TRANS_DIR" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "✓ Transcription directory exists"
    echo "  Transcription files: $FILE_COUNT"
else
    echo "ℹ Transcription directory not found (will be created when needed)"
fi

echo

# Check Whisper availability
echo "Checking Whisper..."
if command -v whisper &> /dev/null; then
    echo "✓ Whisper is available"
else
    echo "✗ Whisper is not installed"
fi

echo
echo "=== Monitoring complete ==="