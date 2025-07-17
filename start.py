#!/usr/bin/env python3
import subprocess
import sys
import os

def install_requirements():
    """Install requirements.txt packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def start_server():
    """Start the uvicorn server"""
    try:
        port = os.getenv("PORT", "8000")
        subprocess.check_call([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", port
        ])
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Railway deployment...")
    install_requirements()
    start_server()