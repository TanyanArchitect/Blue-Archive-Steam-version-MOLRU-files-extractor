# 📁 Blue Archive (Steam) - Asset Extractor

<div align="center">

![Version](https://img.shields.io/badge/version-v8.3-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/platform-Windows-brightgreen?style=for-the-badge&logo=windows)
![Language](https://img.shields.io/badge/language-English%20%7C%20Vietnamese-orange?style=for-the-badge)
![Downloads](https://img.shields.io/github/downloads/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/total?style=for-the-badge&color=purple)

**A fast, safe, and easy-to-use tool to extract Assets from Blue Archive (Steam Version).**
*Dành cho cộng đồng game thủ Blue Archive Việt Nam và Quốc tế.*

[📥 Download Latest Version](https://github.com/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/releases) • [🐛 Report Bug](https://github.com/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/issues)

</div>

---

## 🖼️ Interface (Giao diện)

<div align="center">
  <img src="https://github.com/user-attachments/assets/9f179237-ebea-42ec-9f52-e28aa517e8bd" alt="Tool Screenshot" width="80%">
  <br>
  <i>Giao diện trực quan, hỗ trợ Đa ngôn ngữ và Chọn file cộng dồn.</i>
</div>

---

## 👋 Introduction

For those playing the Steam version who enjoy digging into game files (for editing, videos, or memes), you noticed that the recent update packaged assets into **`.molru`** files. Manually extracting them via Hex Editor is a nightmare.

This tool automates that process. Just point it to the files, and it handles the rest in seconds.

## 🚀 Key Features (Tính năng)

| Feature | Description |
| :--- | :--- |
| **⚡ Lightning Fast** | Scans and extracts thousands of assets in seconds. |
| **📂 Batch & Cumulative** | **(New in v8.3)** Select files from multiple folders at once. Append new files to your list easily. |
| **🌎 Multi-Language** | Fully supports **English** and **Vietnamese** (Tiếng Việt). |
| **🛡️ Safe Mode** | Runs in **Read-Only** mode. Never modifies your original game files. |
| **📦 Smart Sort** | Automatically sorts files into subfolders by type. |

### 🎵 Supported Formats
The tool automatically detects and categorizes:
* **Images:** `.jpg`, `.png`, `.webp` (Character arts, UI, Icons)
* **Audio:** `.ogg`, `.wav`, `.mp3` (BGM, Voice lines, SFX)
* **Video:** `.webm` (Cutscenes, PVs)

---

## 📥 Installation & Usage

1.  **Download** the `.exe` from [Releases](https://github.com/TanyanArchitect/Blue-Archive-Steam-version-MOLRU-files-extractor/releases).
2.  **Right-click** -> **Run as Administrator** (Recommended).
3.  Click **"Add Files..."** (hoặc "Thêm file...") to select `.molru` or `.bundle` files.
    * *Tip:* You can navigate to different folders and add more files. The list will accumulate.
4.  *(Optional)* Click **"Clear"** if you want to reset your selection.
5.  Click **"START SCAN & EXTRACT"**.
6.  Enjoy! The output folder opens automatically.

### 📂 Output Structure
Extracted files are organized like this:
```text
Source_File_Extracted/
├── jpg/      # Standard images
├── png/      # Transparent icons/UI
├── webp/     # Animations
├── ogg/      # Audio files
└── webm/     # Videos
```

## 📍 Where are the Game Files?
Navigate to your Steam installation folder. The path usually looks like this:

```text
Steam\steamapps\common\BlueArchive\BlueArchive_Data\StreamingAssets\PUB\Resource\
```
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

## 📜 Latest Update (v8.3)
* **Feature:** Select files from multiple folders (Cumulative Selection).
* **UI:** Added "Clear" button to reset selection.
* **Fix:** Config file now saves correctly next to the `.exe` file.

---

<div align="center">
  <b>Made with ❤️ by TanyanArchitect & Gemini AI</b><br>
  <i>Enjoy the game, Sensei!</i>
</div>
