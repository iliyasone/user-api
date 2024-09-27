#!/bin/bash

# Name of the screen session
SESSION_NAME="fastapi_server"

# Stop the screen session running FastAPI
screen -S $SESSION_NAME -X quit

echo "FastAPI server stopped (screen session '$SESSION_NAME')."