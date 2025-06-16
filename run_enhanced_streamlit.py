#!/usr/bin/env python3
"""
Enhanced startup script for Streamlit with Chinese translation support.
"""
import os
import sys
import subprocess

def main():
    # Fix for PyTorch + Streamlit compatibility issue
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Get the directory of this script (project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(project_root, "src", "streamlit_app", "enhanced_app.py")
    
    if not os.path.exists(app_path):
        print("❌ Enhanced Streamlit app not found. Please run this from the project root.")
        print(f"Expected path: {app_path}")
        return
    
    print("🚀 Starting Enhanced Universal Translation Web App...")
    print("🌟 NEW: Chinese (Simplified) support included!")
    print("📱 The app will open in your browser automatically")
    print("🌐 URL: http://localhost:8502")  # Different port to avoid conflicts
    print("⏹️  Press Ctrl+C to stop the server")
    print("🔧 PyTorch compatibility fix applied")
    print("🇨🇳 Chinese translation via OPUS-MT models")
    print("-" * 60)
    
    # Change to project root and run streamlit with fixed config
    os.chdir(project_root)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.address", "0.0.0.0",
            "--server.port", "8502",  # Different port
            "--browser.gatherUsageStats", "false",
            "--server.fileWatcherType", "none",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down the enhanced translation app...")

if __name__ == "__main__":
    main()