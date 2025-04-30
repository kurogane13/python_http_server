# 🌐 Python HTTP File Server

## Program developed by Gustavo Wydler Azuaga - 2025-04-30

**Python-based HTTP file server**

- Sharing
- Downloading
- Uploading

---

## 📦 Project Scope

This tool provides a simple way to:

- 🌍 Share files over a network using HTTP.
- 📥 Allow clients to upload files securely using `curl`.
- 📄 Present an HTML-based file listing, including file size and last modification time.
- 🧑‍💻 Run without any external dependencies — just Python 3!
- 🧠 Detect the host operating system and validate IP reachability before server startup.

---

## 🚀 Features

✅ **Fancy web interface** with modern styles  
✅ **Supports GET & POST** requests (file listing, downloading, uploading)  
✅ **Auto-formatted file size display** (KB, MB, GB)  
✅ **Easy-to-use upload with curl command** (auto-generated instructions)  
✅ **Validates user-entered IP and port**  
✅ **Custom server IP and port selection at runtime**  
✅ **Detailed file info table: name, size, modified time**  
✅ **Cross-platform** (Windows, Linux)

---

## 🔧 Requirements

- Python 3.8 (recommended 3.8+)
- No external packages required

---

## 🛠️ How to Use

#### ▶️ Start the Server (Tested with python3.10)

```bash
python3 http_file_server.py
```

#### ▶️ Provide the http server IP address

#### ▶️ Provide the http server PORT number

------------------------------------------------------------------------------------------------------------------------------------------------------

**Python-based HTTP client**

- Upload files to a running http server
- Select multiple files at once
- Windowded gui styled navigation
  
## 🔧 Requirements

- Install tkinter
  ```bash
  sudo apt install python3.10-tk
  ```
- Easygui python library required

#### Install the requirements.txt file

```bash
python3.10 -m pip install -r requirements.txt
```

#### ▶️ Run the client (tested with python3.10)

```bash
python3.8 http_file_client.py
```
#### ▶️ Provide the http server IP address

#### ▶️ Provide the http server PORT number

#### ▶️ Follow the wizard to upload the file/s

