import easygui
import subprocess
import os
import sys
from datetime import datetime

def main_menu():
    choice = easygui.buttonbox(
        "Welcome to the Python HTTP CURL File Uploader client\n\n\n               Press the 'Upload Files button' to get started",
        title="PYTHON HTTP SERVER Start window",
        choices=["Upload Files", "Exit"]
    )

    if choice == "Upload Files":
        show_intro_and_get_server_info()
    elif choice == "Exit":
        sys.exit(0)

def show_intro_and_get_server_info():
    easygui.msgbox(
        msg=(
            "                          Python HTTP CURL File Uploader\n\n"
            "This tool allows you to upload files to an HTTP server using the `curl` command.\n\n"
            " - Features:\n\n\n"
            "       - Choose and upload one or more files to a remote HTTP server.\n"
            "       - Enter your destination server IP and port.\n"
            "       - Set the upload path on the remote server.\n"
            "       - Get a detailed terminal log and summary of the upload results.\n\n"
            "\n\n                    Let's begin by entering your server details."
        ),
        title="Welcome to the File Uploader"
    )
    get_server_info()

def get_server_info():
    field_names = ["Server IP (e.g., 192.168.1.100)", "Port (e.g., 8080)"]
    default_values = ["", "8080"]
    values = easygui.multenterbox("Enter the server connection details below:", "Server Info", field_names, default_values)

    if not values or any(not val.strip() for val in values):
        easygui.msgbox("Both IP address and port are required.", title="Missing Info")
        return main_menu()

    ip, port = values[0].strip(), values[1].strip()
    if not port.isdigit():
        easygui.msgbox("Port must be a number.", title="Invalid Port")
        return get_server_info()

    path = easygui.enterbox("Enter the upload path where the python http server is running. \n\n\nExample for linux: /home/john/.\n\nExample for windows C:\SharedFiles\n\n", title="Upload Path")
    if not path:
        easygui.msgbox("Upload path is required.", title="Missing Info")
        return main_menu()

    # Normalize and sanitize upload path
    normalized_path = path.replace("\\", "/")
    if not normalized_path.startswith("/"):
        normalized_path = "/" + normalized_path

    upload_files(ip, port, normalized_path)

def upload_files(server_ip, port, upload_path):
    easygui.msgbox("Welcome to the Upload Wizard.\n\n\n                   You will now select the files to upload.", title="Start Upload Wizard")

    files = easygui.fileopenbox(
        msg="Select one or more files to upload",
        title="File Selection",
        multiple=True
    )

    if not files:
        easygui.msgbox("No files selected. Returning to main menu.", title="Info")
        return main_menu()

    # Display selected files for confirmation
    file_list_display = "\n".join(files)
    confirm_msg = (
        "You have selected the following files to upload:\n\n"
        f"{file_list_display}\n\n"
        "Do you want to proceed with uploading these files?"
    )

    choice = easygui.buttonbox(
        msg=confirm_msg,
        title="Confirm Upload",
        choices=["Yes", "No", "Back to Main Menu"]
    )

    if choice == "Back to Main Menu":
        return main_menu()
    elif choice == "No":
        return upload_files(server_ip, port, upload_path)

    # Final instruction before upload starts
    easygui.msgbox(
        "All files are confirmed.\n\nClick OK to start uploading.\n\n"
        "Upload progress and details will be shown in the terminal window.",
        title="Ready to Upload"
    )

    print(f"\n--- Starting Upload at {datetime.now().isoformat()} ---\n")

    upload_results = ""
    for file_path in files:
        if os.path.isfile(file_path):
            filename = os.path.basename(file_path)
            url = f"http://{server_ip}:{port}{upload_path}"

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Uploading: {filename}")
            print(f" → URL: {url}")
            print(f" → curl --data-binary @{file_path}")

            curl_command = [
                "curl", "-X", "POST",
                "-H", f"X-Filename: {filename}",
                "--data-binary", f"@{file_path}",
                url
            ]

            result = subprocess.run(curl_command, capture_output=True, text=True)

            if result.returncode == 0:
                print(f" ✅ {filename} uploaded successfully\n")
                upload_results += f"{filename}: ✅ Uploaded successfully\n"
            else:
                print(f" ❌ Failed to upload {filename}")
                print(f" STDERR: {result.stderr.strip()}\n")
                upload_results += f"{filename}: ❌ Upload failed\nError: {result.stderr.strip()}\n"

    # Save results to a temporary log file
    log_file = os.path.join(os.getenv("TEMP") if os.name == "nt" else "/tmp", "upload_summary.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(upload_results)

    summary_text = upload_results if len(upload_results) <= 4000 else \
        upload_results[:4000] + "\n... (truncated)\n\nFull log saved to:\n" + log_file

    easygui.codebox("Upload Summary", "Results", summary_text)

    next_action = easygui.buttonbox(
        "What would you like to do next?",
        title="Next Step",
        choices=["Upload More Files", "Back to Main Menu", "Exit"]
    )

    if next_action == "Upload More Files":
        upload_files(server_ip, port, upload_path)
    elif next_action == "Back to Main Menu":
        main_menu()
    else:
        sys.exit(0)

if __name__ == "__main__":
    main_menu()
