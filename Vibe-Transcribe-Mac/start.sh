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
