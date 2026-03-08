# 📁 Blue Archive (Steam) - Asset Extractor

<div align="center">

![Version](https://img.shields.io/badge/version-v8.6-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/platform-Windows-brightgreen?style=for-the-badge&logo=windows)
![Language](https://img.shields.io/badge/language-EN%20%7C%20VN%20%7C%20CN%20%7C%20JP%20%7C%20KR-orange?style=for-the-badge)
![Downloads](https://img.shields.io/github/downloads/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/total?style=for-the-badge&color=purple)

**A fast, safe, and easy-to-use tool to extract Assets from Blue Archive (Steam Version).**
*Dành cho cộng đồng game thủ Blue Archive Việt Nam và Quốc tế.*

[📥 Download Latest Version](https://github.com/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/releases) • [🐛 Report Bug](https://github.com/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/issues)

</div>

---

## 🖼️ Interface (Giao diện)

<div align="center">
  <img src="https://github.com/user-attachments/assets/9841d878-06bb-416e-82ad-619c85ad0298" alt="Tool Screenshot" width="80%">
  <br>
  <i>Giao diện trực quan, hỗ trợ Đa ngôn ngữ và Chọn file cộng dồn.</i>
</div>

---

## 👋 Introduction

For those playing the Steam version who enjoy digging into game files (for editing, videos, or memes), you noticed that the recent update packaged assets into **`.molru`** files. Manually extracting them via Hex Editor is a nightmare.

This tool automates that process. Just **Drag & Drop** files into the tool, and it handles the rest in seconds.

## 🚀 Key Features (Tính năng)

| Feature | Description |
| :--- | :--- |
| **⚡ Lightning Fast** | Scans and extracts thousands of assets in seconds. |
| **🌎 Multi-Language** | Fully supports **English**, **Vietnamese**, **Chinese**, **Japanese**, and **Korean**. |
| **🛡️ Safe Mode** | Runs in **Read-Only** mode. Never modifies your original game files. |
| **👋 Drag & Drop** | **(New in v8.4)** Simply drag `.molru` or `.bundle` files from Explorer directly into the tool. |
| **📂 Smart Organization** | **(New in v8.5)** Extracts to `BA_Extracted` folder. Auto-sorts by type and auto-increments folders to prevent overwriting (e.g., `jpg (1)`). |

### 🎵 Supported Formats
The tool automatically detects and categorizes:
* **Images:** `.jpg`, `.png`, `.webp` (Character arts, UI, Icons)
* **Audio:** `.ogg`, `.wav`, `.mp3` (BGM, Voice lines, SFX)
* **Video:** `.webm` (Cutscenes, PVs)

---

## 📥 User Guide

1.  **Download** the `.exe` from [Releases](https://github.com/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/releases).
2.  **Right-click** -> **Run as Administrator** (Recommended).
3.  **Drag & Drop** your `.molru` files into the window OR click **"Add Files..."**.
    * *Tip:* You can navigate to different folders and add more files. The list will accumulate.
4.  *(Optional)* Click **"Clear"** if you want to reset your selection.
5.  Click **"START SCAN & EXTRACT"**.
6.  Enjoy! The output folder opens automatically.

### 📂 Output Structure
Extracted files are organized like this:
```text
[Tool_Location]/BA_Extracted/
└── [File_Name]/
    ├── jpg/      # Standard images
    ├── png/      # Transparent icons/UI
    ├── webp/     # Animations
    ├── ogg/      # Audio files
    └── webm/     # Videos
```

---

## 👨‍💻 For Developers / Build from Source

If you want to modify the source code or build the `.exe` yourself, please follow these steps carefully.

### 1. Prerequisites
* **Python 3.x** installed.
* Download the source code (`extractor.py` and `locales.py`).
* **Important:** Ensure both `locales.py` and the `my_icon.ico` file are present in the same directory as the main script.

### 2. Install Dependencies
This project uses `tkinterdnd2` for the Drag & Drop feature, which is not included in standard Python.
Open your terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 3. Run from Source
To run the script directly without compiling:

```bash
python extractor.py
```

*Note: When running the raw Python script, a console window will appear alongside the GUI. This is normal and used for displaying debug logs.*

### 4. Build .EXE (PyInstaller)
To package the app into a standalone `.exe`, run the command below. **Important:** You must include the `--collect-all tkinterdnd2` argument, otherwise the drag-and-drop feature will cause the app to crash immediately.

```bash
pyinstaller --noconsole --onefile --icon=my_icon.ico --add-data "my_icon.ico;." --collect-all tkinterdnd2 --name="BlueArchiveExtractor_v8.6" extractor.py
```

**Command Flags Explained:**
* `--noconsole`: Launches the app in GUI mode (hides the background command prompt window).
* `--onefile`: Packages the Python interpreter, script, and dependencies into a single portable `.exe` file.
* `--collect-all tkinterdnd2`: **CRITICAL.** Forces PyInstaller to collect all hooks and binaries for the Drag & Drop library. *Without this, the app will crash.*
* `--add-data "my_icon.ico;."`: Embeds the icon file *inside* the executable so the script can access it internally (e.g., for the window title bar).
* `--icon=my_icon.ico`: Sets the file icon for the executable itself (visible in File Explorer).

---

## 📍 Where are the Game Files?
Navigate to your Steam installation folder. The path usually looks like this:

**Base Path:**
```text
Steam\steamapps\common\BlueArchive\BlueArchive_Data\StreamingAssets\PUB\Resource\
```

**Specific Locations:**
* **Prologue Images:** `...\Resource\Preload\MediaResources\UIs\03_Scenario`
* **All Game Images:** `...\Resource\GameData\MediaResources\UIs\03_Scenario`
* **Voices/BGM:** Look for folders named `Audio`.

---

## ⚠️ Important Notes

> [!WARNING]
> **False Positive Virus Warning:**
> Because this tool is compiled with **PyInstaller** and unsigned, Windows Defender might flag it as "Wacatac" or "Trojan". **This is a false positive.** The source code is open-source for you to verify. Please add an exclusion to run it.

> [!NOTE]
> **Repack/Modding:**
> Currently **IMPOSSIBLE**. The `.molru` header is encrypted. We can extract (read) but cannot repack (write) without causing a black screen.

---

## 📜 Latest Update (v8.6 - Global Edition)
* **Multi-Language:** Added support for Chinese (CN), Japanese (JP), and Korean (KR). Now supports 5 languages in total!
* **Open Source:** Huge thanks to [Shiroko (SS3-4001)](https://github.com/SS3-4001) for the translation contributions!
* **Optimization:** Separated language data into `locales.py` for a cleaner and more maintainable code structure.

---

<div align="center">
  <b>Made with ❤️ by TanyanArchitect, Contributors & Gemini AI</b><br>
  <i>Enjoy the game, Sensei!</i>
</div>
