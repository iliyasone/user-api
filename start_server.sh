#!/bin/bash

# Name of the screen session
SESSION_NAME="fastapi_server"

# Start a screen session and run Uvicorn in the background
screen -dmS $SESSION_NAME uvicorn main:app --host 0.0.0.0 --port 8000

echo "FastAPI server started in screen session '$SESSION_NAME'."
