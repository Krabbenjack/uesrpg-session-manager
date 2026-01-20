#!/bin/bash
# UESRPG Session Manager launcher for Mac/Linux
# This script launches the application with Python

cd "$(dirname "$0")"
python3 app.py || python app.py
