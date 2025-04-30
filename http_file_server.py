import http.server
import socketserver
import os
import urllib.parse
import re
import subprocess
import platform
from datetime import datetime

# === Fancy Console Welcome Title ===
print("=" * 70)
print("🌐  Welcome to the Python HTTP File Server! 🌐".center(70))
print("=" * 70)
print("""
This server allows you to:

🔹 Serve files over HTTP from a shared directory.
🔹 List all available files with size and last-modified details.
🔹 Download files via web browser or CLI.
🔹 Upload files securely using a simple curl command.

💡 Tip: Access the server on your local network by providing the IP address.
""")
print("-" * 70)

# Detect operating system
CURRENT_OS = platform.system().lower()
print(f"\n📟 Detected OS: {CURRENT_OS.capitalize()}")

# Validate IP address format
def is_valid_ip(ip):
    print("\nValidating correct IP v4 format...")
    ip_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(ip_regex, ip):
        return False
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

# Check if the IP is reachable via ping
def is_reachable(ip):
    print(f"\nTesting provided IP {ip} reachability...")
    try:
        if "windows" in CURRENT_OS:
            subprocess.check_output(['ping', '-n', '1', '-w', '1000', ip], stderr=subprocess.DEVNULL)
        else:
            subprocess.check_output(['ping', '-c', '1', '-W', '1', ip], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Prompt for IP address until valid and reachable
while True:
    server_ip = input("\nEnter the server IP address for file uploads (e.g., 192.168.1.10): ").strip()
    if not is_valid_ip(server_ip):
        print("\n❌ Invalid IP format. Please try again.")
        continue
    if not is_reachable(server_ip):
        print("\n❌ IP is not reachable. Please try another reachable address.")
        continue
    break

# Get the current working directory as share directory
SHARE_DIR = os.getcwd()

class UploadAndListHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.list_shared_files()
        else:
            return super().do_GET()

    def list_shared_files(self):
        try:
            file_list = os.listdir(SHARE_DIR)
        except FileNotFoundError:
            os.makedirs(SHARE_DIR)
            file_list = []

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Shared Files in {SHARE_DIR}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to bottom right, #0d0d0d, #1a1a1a);
            color: #f2f2f2;
            margin: 0;
            padding: 0;
        }}
        header {{
            background: linear-gradient(to right, #8e2de2, #4a00e0);
            padding: 30px;
            text-align: center;
            color: white;
            box-shadow: 0 0 15px #4a00e0;
        }}
        header2 {{
            padding: 30px;
            text-align: center;
            color: white;
        }}
        h1 {{
            margin: 0;
            font-size: 30px;
            text-shadow: 1px 1px 2px #000;
        }}
        .container {{
            padding: 40px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            box-shadow: 0 0 18px #00ffd5;
            margin-top: 25px;
            background-color: #10131a;
            border: 1px solid #444;
        }}
        th, td {{
            padding: 16px 20px;
            text-align: left;
            border-bottom: 1px solid #333;
        }}
        th {{
            background-color: #00ffd5;
            color: #10131a;
            font-size: 16px;
        }}
        tr:nth-child(even) {{
            background-color: #1f2233;
        }}
        tr:hover {{
            background-color: #293352;
        }}
        a {{
            color: #ffcc00;
            text-decoration: none;
            font-weight: 600;
            transition: 0.3s;
        }}
        a:hover {{
            color: #ffffff;
            text-shadow: 0 0 8px #ffcc00;
        }}
        .curl-command {{
            padding: 18px;
            border-radius: 10px;
            font-size: 1.2em;
            margin-top: 10px;
            margin-bottom: 20px;
            font-weight: bold;
            background-color: #000000;
            color: #ffffff;
            font-family: monospace;
            white-space: pre-wrap;
            box-shadow: 0 0 15px #00ffaa;
        }}
        .upload-box {{
            border-left: 4px solid #3399ff;
            box-shadow: 0 0 15px #3399ff;
        }}
        .example-box {{
            border-left: 4px solid #00ffaa;
            box-shadow: 0 0 15px #00ffaa;
        }}
        .curl-title {{
            font-size: 20px;
            font-weight: bold;
            color: #00ffff;
            margin: 30px 0 10px 0;
            text-shadow: 0 0 8px #00ffff;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Python HTTP File Server<br><br>Hosting Shared Files in {SHARE_DIR}</h1>
    </header>

    <div class="container">
        <div class="curl-title">Upload a file to this server using:</div>
        <div class="curl-command upload-box">
curl -X POST -H "X-Filename: yourfile.ext" --data-binary @yourfile.ext http://{server_ip}:{PORT}
        </div>

        <div class="curl-title">Upload example:</div>
        <div class="curl-command example-box">
curl -X POST -H "X-Filename: ends_protocol_chart.png" --data-binary @ends_protocol_chart.png http://{server_ip}:{PORT}
        </div>

        <header2>
            <h2>Click on any file to download it</h2>
        </header2>

        <table>
            <tr>
                <th>Filename</th>
                <th>Size (KB)</th>
                <th>Size (MB)</th>
                <th>Size (GB)</th>
                <th>Last Modified</th>
            </tr>
        """

        for f in file_list:
            path = os.path.join(SHARE_DIR, f)
            if os.path.isfile(path):
                size_bytes = os.path.getsize(path)
                size_kb = round(size_bytes / 1024, 2)
                size_mb = round(size_bytes / (1024 ** 2), 2)
                size_gb = round(size_bytes / (1024 ** 3), 2)
                mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
                url = urllib.parse.quote(f)
                html += (
                    f"<tr><td><a href='/{url}' download>{f}</a></td>"
                    f"<td>{size_kb}</td><td>{size_mb}</td><td>{size_gb}</td><td>{mtime}</td></tr>"
                )

        html += """
            </table>
        </div>
    </body>
</html>
"""
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        field_data = self.rfile.read(length)
        filename = self.headers.get('X-Filename', 'upload.file')
        file_path = os.path.join(SHARE_DIR, os.path.basename(filename))
        with open(file_path, 'wb') as f:
            f.write(field_data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Upload received successfully.\n')

# Ensure directory exists
os.makedirs(SHARE_DIR, exist_ok=True)
os.chdir(SHARE_DIR)

# Prompt and retry if port is in use
while True:
    try:
        PORT = int(input("\n🔌 Enter the port to run the server on (default 8080): ") or "8080")
        with socketserver.TCPServer(("", PORT), UploadAndListHandler) as httpd:
            print(f"\n✅ Server started successfully!")
            print(f"📂 Serving directory: {SHARE_DIR}")
            print(f"🌍 Access the server from: http://{server_ip}:{PORT}")
            httpd.serve_forever()
        break
    except OSError as e:
        if e.errno == 98:
            print(f"\n❌ Port {PORT} is already in use.")
            choice = input("\nDo you want to try another port? (y/n): ").strip().lower()
            if choice != 'y':
                print("\n🚪 Exiting the server.")
                break
        else:
            raise
