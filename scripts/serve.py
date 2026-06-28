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
import time
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

def processes_on_port(port):
    """Return process IDs using the port, if lsof is available."""
    try:
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        return [pid for pid in result.stdout.strip().split('\n') if pid]
    except Exception:
        return []

def confirm_kill_processes(port, pids):
    """Ask before terminating processes using the port."""
    if not pids:
        return False

    print(f"Processes using port {port}: {', '.join(pids)}")
    if not sys.stdin.isatty():
        print("Non-interactive terminal: not killing processes automatically.")
        return False

    answer = input(f"Kill these processes and start the server on port {port}? [y/N]: ").strip().lower()
    if answer not in ('y', 'yes'):
        return False

    stopped_any = False
    for pid in pids:
        try:
            subprocess.run(['kill', pid], check=False)
            print(f"✓ Sent stop signal to process (PID: {pid})")
            stopped_any = True
        except Exception as exc:
            print(f"⚠️  Could not stop process {pid}: {exc}")

    time.sleep(1)
    return stopped_any

if __name__ == '__main__':
    os.chdir(BASE_DIR)

    # Check if port is in use and ask before stopping the existing process.
    if port_is_in_use(PORT):
        print(f"⚠️  Port {PORT} is already in use")
        pids = processes_on_port(PORT)
        confirm_kill_processes(PORT, pids)

        if port_is_in_use(PORT):
            print(f"❌ Port {PORT} is still in use")
            print(f"Stop the process manually or edit PORT in scripts/serve.py")
            sys.exit(1)

        print(f"✓ Port {PORT} is free, starting server...\n")

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
