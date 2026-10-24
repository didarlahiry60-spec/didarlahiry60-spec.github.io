#!/usr/bin/env bash
cd "/home/didar-lahiry/Antigravity/Target Portfolio 2"

# Check if port 3000 is running, if not start server.py in background
if ! ss -lptn 'sport = :3000' | grep -q '3000'; then
    echo "Starting portfolio server..."
    python3 server.py > /dev/null 2>&1 &
    sleep 1
fi

echo "Opening http://localhost:3000 in your browser..."
xdg-open "http://localhost:3000" > /dev/null 2>&1 || google-chrome "http://localhost:3000" > /dev/null 2>&1
