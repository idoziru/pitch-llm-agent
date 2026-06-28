#!/usr/bin/env python3
"""
Simple HTTP server to serve presentation and enable PNG export with CORS support.
Allows html2canvas to capture images properly.
"""

import http.server
import socketserver
import webbrowser
import os
import socket
import subprocess
import sys
from pathlib import Path

PORT = 8000
BASE_DIR = Path(__file__).parent.parent

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Custom logging
        print(f"[{self.log_date_time_string()}] {format % args}")

def port_is_in_use(port):
    """Check if port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return False
        except OSError:
            return True

def kill_existing_process(port):
    """Kill existing process using the port"""
    try:
        # Try lsof (macOS/Linux)
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    subprocess.run(['kill', '-9', pid])
                    print(f"✓ Killed existing process (PID: {pid})")
                except:
                    pass
            return True
    except:
        pass
    
    return False

if __name__ == '__main__':
    os.chdir(BASE_DIR)
    
    # Check if port is in use and kill existing process
    if port_is_in_use(PORT):
        print(f"⚠️  Port {PORT} is already in use")
        if kill_existing_process(PORT):
            print(f"✓ Old process killed, starting new server...\n")
            import time
            time.sleep(1)
        else:
            print(f"❌ Could not kill existing process on port {PORT}")
            print(f"Please run: lsof -ti :{PORT} | xargs kill -9")
            sys.exit(1)
    
    try:
        with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
            url = f"http://localhost:{PORT}/index.html"
            print(f"\n{'='*60}")
            print(f"🚀 Server running at: {url}")
            print(f"{'='*60}\n")
            print("Press Ctrl+C to stop the server\n")
            
            # Open in browser
            try:
                webbrowser.open(url)
                print("✓ Browser should open automatically\n")
            except:
                print(f"⚠️  Please open manually: {url}\n")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n\n✓ Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
