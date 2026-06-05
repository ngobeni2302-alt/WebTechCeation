#!/bin/bash

# Configuration
PORT=8080
DIRECTORY=$(dirname "$0")

echo "------------------------------------------------"
echo "  WEBHub Premium: Launching Web Experience...  "
echo "------------------------------------------------"

# Change to the project root directory where this script is located
cd "$DIRECTORY/.."

# Setup and Start the FastAPI Server in the background
echo "Setting up FastAPI backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
(uvicorn main:app --port 8000 > /dev/null 2>&1 &)
cd ..

# Wait a second for the server to start
sleep 2

PORT=8000
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

echo "The server is running at $URL (PID: $!)"
echo "Press Ctrl+C in this terminal when you want to stop the website."

# Trap Ctrl+C to kill the background process on exit
trap "kill $!; exit" INT
wait
