#!/bin/bash

# Configuration
PORT=8080
DIRECTORY=$(dirname "$0")

echo "------------------------------------------------"
echo "  WEBHub Premium: Launching Web Experience...  "
echo "------------------------------------------------"

# Change to the project root directory where this script is located
cd "$DIRECTORY/.."

# Start the Custom Auth Server in the background
PYTHON_BIN="python3"
if [ -f ".venv/bin/python3" ]; then
    PYTHON_BIN=".venv/bin/python3"
elif [ -f "venv/bin/python3" ]; then
    PYTHON_BIN="venv/bin/python3"
fi

# Check for required dependencies
if ! $PYTHON_BIN -c "import dotenv, jwt, fastapi, uvicorn, slowapi" > /dev/null 2>&1; then
    echo "ERROR: Missing required Python dependencies (python-dotenv, PyJWT, fastapi, uvicorn, slowapi)."
    echo "Please run: $PYTHON_BIN -m pip install python-dotenv PyJWT fastapi uvicorn slowapi"
    exit 1
fi

$PYTHON_BIN -m uvicorn backend.server:app --host 0.0.0.0 --port $PORT --reload > /dev/null 2>&1 &
SERVER_PID=$!

# Wait a second for the server to start
sleep 1

# Get the URL
URL="http://localhost:$PORT"

# Open the default browser
echo "Opening $URL in your default browser..."

if command -v xdg-open > /dev/null; then
    xdg-open "$URL"
elif command -v open > /dev/null; then
    open "$URL"
elif command -v sensible-browser > /dev/null; then
    sensible-browser "$URL"
else
    echo "Could not find a command to open the browser. Please visit: $URL"
fi

echo "The server is running at $URL (PID: $SERVER_PID)"
echo "Press Ctrl+C in this terminal when you want to stop the website."

# Trap Ctrl+C to kill the background process on exit
trap "kill $SERVER_PID; exit" INT
wait
