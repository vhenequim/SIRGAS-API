#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install numpy first to avoid binary compatibility issues
pip install numpy==1.24.3

# Install other dependencies
pip install -r requirements.txt 