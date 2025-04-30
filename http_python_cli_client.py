import subprocess
import os
import sys
from datetime import datetime

def print_cr(message=""):
    """Print message with carriage return and newline"""
    sys.stdout.write(message + "\r\n")
    sys.stdout.flush()

def main_menu():
    while True:
        print_cr("\r\nWelcome to the Python HTTP CURL File Uploader (CLI Edition)")
        print_cr("-------------------------------------------------------------")
        print_cr("1. Upload Files")
        print_cr("2. Exit")
        choice = input("\r\nSelect an option (1-2): ")

        if choice == "1":
            get_server_info()
        elif choice == "2":
            sys.exit(0)
        else:
            print_cr("Invalid choice. Please select 1 or 2.")

def get_server_info():
    print_cr("\r\nServer Connection Setup")
    print_cr("-------------------------")
    ip = input("Enter Server IP (e.g., 192.168.1.100): ").strip()
    port = input("Enter Port (e.g., 8080): ").strip()

    if not ip or not port.isdigit():
        print_cr("Invalid input. IP and numeric port are required.")
        return main_menu()

    print_cr("Example (Windows: C:\\SharedFiles )")
    remote_path = input("Waiting for remote server path: ").strip()

    if not remote_path:
        print_cr("Upload path is required.")
        return main_menu()

    normalized_path = remote_path.replace("\\", "/")
    if not normalized_path.startswith("/"):
        normalized_path = "/" + normalized_path

    upload_files(ip, port, normalized_path)

def upload_files(server_ip, port, remote_path):
    current_dir = os.getcwd()
    print_cr(f"\r\nListing all files in local directory: {current_dir}")
    print_cr("-----------------------------------------------------")

    files_in_pwd = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]

    if not files_in_pwd:
        print_cr("No files found in the current directory.")
        return main_menu()

    for f in files_in_pwd:
        print_cr(f" - {f}")

    print_cr("\r\nYou can now copy and paste one or more filenames (with spaces).")
    filenames_input = input("Enter filenames to upload: ").strip()
    filenames = filenames_input.split()

    selected_files = []
    for fname in filenames:
        full_path = os.path.join(current_dir, fname)
        if os.path.isfile(full_path):
            selected_files.append(full_path)
        else:
            print_cr(f" ⚠️ File not found: {fname}")

    if not selected_files:
        print_cr("\r\nNo valid files selected. Returning to main menu.")
        return main_menu()

    print_cr("\r\nYou have selected the following valid files:\r\n---------------------------------------------")
    for f in selected_files:
        print_cr(f" - {f}")

    confirm = input("\r\nProceed with upload? (y/n): ").strip().lower()
    if confirm != "y":
        return main_menu()

    print_cr(f"\r\n--- Upload Started at {datetime.now().isoformat()} ---\r\n")

    upload_results = ""
    for file_path in selected_files:
        filename = os.path.basename(file_path)
        url = f"http://{server_ip}:{port}{remote_path}"

        print_cr(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Uploading: {filename}")
        print_cr(f" → URL: {url}")
        print_cr(f" → curl --data-binary @{file_path}")

        curl_command = [
            "curl", "-X", "POST",
            "-H", f"X-Filename: {filename}",
            "--data-binary", f"@{file_path}",
            url
        ]

        result = subprocess.run(curl_command, capture_output=True, text=True)

        if result.returncode == 0:
            print_cr(f" ✅ {filename} uploaded successfully\r\n")
            upload_results += f"{filename}: ✅ Uploaded successfully\r\n"
        else:
            print_cr(f" ❌ Failed to upload {filename}")
            print_cr(f" STDERR: {result.stderr.strip()}\r\n")
            upload_results += f"{filename}: ❌ Upload failed\r\nError: {result.stderr.strip()}\r\n"

    log_file = os.path.join(os.getenv("TEMP") if os.name == "nt" else "/tmp", "upload_summary.log")
    with open(log_file, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(upload_results)

    print_cr("\r\nUpload Summary:\r\n----------------")
    print_cr(upload_results)
    print_cr(f"Full log saved to: {log_file}")

    next_action = input("\r\nWhat next? [1=Upload More, 2=Main Menu, 3=Exit]: ").strip()
    if next_action == "1":
        upload_files(server_ip, port, remote_path)
    elif next_action == "2":
        main_menu()
    else:
        sys.exit(0)

if __name__ == "__main__":
    main_menu()
