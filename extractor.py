import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import sys
import struct
import mmap
import ctypes
import subprocess
import threading
import urllib.request
import json
import webbrowser

GITHUB_USER = "TanyanArchitect"
GITHUB_REPO = "Blue-Archive-Steam-version-MOLRU-files-extractor"
CURRENT_VERSION = "v8.3"

def get_app_path():
    """Lấy đường dẫn chứa file .exe (hoặc file .py khi chạy code)"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(get_app_path(), "config.json")

TRANSLATIONS = {
    "VN": {
        "title": f"Blue Archive Extractor {CURRENT_VERSION}",
        "header": "BLUE ARCHIVE ASSET EXTRACTOR",
        "ver_prefix": "Phiên bản:",
        "warning": "⚠️ LƯU Ý: Vui lòng TẮT GAME trước khi giải nén!",
        "grp_input": "Chọn file dữ liệu (.molru / .bundle)",
        "btn_browse": "Thêm file...",
        "btn_clear": "Xóa chọn",
        "btn_extract": "BẮT ĐẦU QUÉT & GIẢI NÉN",
        "btn_history": "Lịch sử cập nhật",
        "status_check": "Đang kiểm tra cập nhật...",
        "status_offline": "Chế độ Offline.",
        "status_latest": "Bạn đang dùng bản mới nhất.",
        "status_ready": "Sẵn sàng.",
        "status_processing": "Đang xử lý file {}/{} : {}",
        "status_done": "Hoàn tất! Đã xử lý {} file.",
        "credit": "Made by Community | Powered by Python",
        "msg_error_title": "Lỗi",
        "msg_select_file": "Vui lòng chọn ít nhất một file!",
        "msg_warn_game_running": "CẢNH BÁO: Game Blue Archive đang chạy!\nHãy tắt game để tránh lỗi file.\nBạn có muốn tiếp tục không?",
        "msg_complete_title": "Hoàn tất",
        "msg_complete_body": "Đã giải nén xong!\nTổng số file: {}\nKiểm tra thư mục chứa file gốc.",
        "update_msg": "Đã có phiên bản mới: {}!\n\nBạn đang dùng: {}\nBạn có muốn tải về ngay không?",
        "changelog_title": "Lịch sử cập nhật",
        "lbl_lang": "Ngôn ngữ / Language:",
        "txt_selected": "Tổng cộng: {} file (Từ nhiều thư mục)",
        "txt_no_select": "Chưa chọn file nào"
    },
    "EN": {
        "title": f"Blue Archive Extractor {CURRENT_VERSION}",
        "header": "BLUE ARCHIVE ASSET EXTRACTOR",
        "ver_prefix": "Version:",
        "warning": "⚠️ WARNING: Please CLOSE THE GAME before extracting!",
        "grp_input": "Select data files (.molru / .bundle)",
        "btn_browse": "Add Files...",
        "btn_clear": "Clear",
        "btn_extract": "START SCAN & EXTRACT",
        "btn_history": "Changelog",
        "status_check": "Checking for updates...",
        "status_offline": "Offline Mode.",
        "status_latest": "You are using the latest version.",
        "status_ready": "Ready.",
        "status_processing": "Processing file {}/{} : {}",
        "status_done": "Done! Processed {} files.",
        "credit": "Made by Community | Powered by Python",
        "msg_error_title": "Error",
        "msg_select_file": "Please select at least one file!",
        "msg_warn_game_running": "WARNING: Blue Archive is running!\nPlease close the game to avoid file corruption.\nDo you want to continue anyway?",
        "msg_complete_title": "Completed",
        "msg_complete_body": "Extraction finished!\nTotal files: {}\nCheck the source file directory.",
        "update_msg": "New version available: {}!\n\nCurrent: {}\nDownload now?",
        "changelog_title": "Changelog",
        "lbl_lang": "Ngôn ngữ / Language:",
        "txt_selected": "Total: {} files (From various folders)",
        "txt_no_select": "No files selected"
    }
}

CHANGELOGS = {
    "VN": """
=== LỊCH SỬ CẬP NHẬT ===

[V8.3 - Chọn cộng dồn]
- TÍNH NĂNG: Cho phép chọn cộng dồn nhiều file từ nhiều thư mục khác nhau (không bị mất danh sách cũ).
- GIAO DIỆN: Thêm nút "Xóa chọn" (Clear) để làm mới danh sách file.
- HỆ THỐNG: Cải thiện vị trí lưu file cấu hình (config.json) luôn nằm cạnh file exe.

[V8.2 - Tách biệt ngôn ngữ]
- GIAO DIỆN: Tách riêng nội dung Changelog cho tiếng Việt và tiếng Anh (không còn hiển thị lẫn lộn).
- Cập nhật đầy đủ lịch sử phiên bản cho cả 2 ngôn ngữ.

[V8.1 - Sửa lỗi & Hoàn thiện]
- CÀI ĐẶT: Tự động lưu ngôn ngữ đã chọn vào file config.json (không cần chọn lại mỗi lần mở).
- GIAO DIỆN: Sửa lỗi hiển thị sai ngôn ngữ khi chuyển đổi qua lại.
- Sửa lỗi cú pháp nhỏ trong cảnh báo.

[V8.0 - Bản Quốc Tế & Hàng Loạt]
- ĐA NGÔN NGỮ: Thêm tùy chọn Tiếng Anh / Tiếng Việt.
- GIẢI NÉN HÀNG LOẠT: Cho phép chọn và giải nén nhiều file cùng lúc.
- TIẾN TRÌNH: Thêm thanh hiển thị tổng tiến độ xử lý.

[V7.3 - Cập nhật Online]
- KẾT NỐI: Tự động kiểm tra phiên bản mới từ GitHub khi mở phần mềm.
- Nếu có bản mới, chương trình sẽ thông báo và dẫn link tải về.

[V7.2 - An toàn là trên hết]
- AN TOÀN: Tự động phát hiện nếu game Blue Archive đang chạy.
- CẢNH BÁO: Hiện thông báo nhắc nhở người dùng tắt game trước khi giải nén để tránh xung đột file hoặc lỗi game.

[V7.1 - Giao diện hoàn thiện]
- GIAO DIỆN: Làm lại giao diện đẹp và gọn gàng hơn.
- THÔNG TIN: Thêm nút xem "Lịch sử cập nhật".

[V7.0 - Quản lý thư mục thông minh]
- TÍNH NĂNG MỚI: Tự động đánh số thư mục (Ví dụ: TenFile (1), TenFile (2)...).
- Giúp không bao giờ bị ghi đè hay mất file cũ nếu lỡ tay giải nén nhiều lần.

[V6.0 - Cập nhật Đa phương tiện]
- NÂNG CẤP LỚN: Hỗ trợ trích xuất toàn diện.
- Âm thanh: Nhạc nền, giọng nói nhân vật (OGG, WAV, MP3).
- Video: Các đoạn phim mở đầu, hoạt cảnh (WEBM).
- Ảnh động: Các file ảnh WebP.
- Tự động phân loại file vào từng folder riêng biệt.

[V5.0 - Hỗ trợ File lớn]
- HIỆU NĂNG: Sửa lỗi treo máy (Not Responding) khi giải nén các file nặng (GB).
- Tối ưu bộ nhớ cho các máy cấu hình thấp.

[V4.0 - Hỗ trợ PNG & Lọc rác]
- ẢNH MỚI: Hỗ trợ lấy thêm định dạng ảnh PNG (icon, ảnh trong suốt).
- LỌC RÁC: Loại bỏ hoàn toàn các file lỗi không mở được.

[V3.0 - Sửa lỗi ảnh mờ]
- SỬA LỖI: Khắc phục tình trạng cắt nhầm thumbnail khiến ảnh bị mờ.
- Tự động bỏ qua ảnh nhỏ để lấy ảnh gốc sắc nét nhất.

[V2.0 - Có giao diện]
- Bỏ màn hình đen (CMD).
- Thêm cửa sổ trực quan và thanh chạy phần trăm.

[V1.0 - Khởi đầu]
- Phiên bản sơ khai.
- Chỉ hỗ trợ tìm và cắt file ảnh JPG.
""",
    "EN": """
=== CHANGELOG ===

[V8.3 - Cumulative Selection]
- FEATURE: Allows selecting files from multiple different folders (files are appended to the list).
- UI: Added "Clear" button to reset the selection.
- SYSTEM: Fixed config.json location (always ensures it is saved next to the exe file).

[V8.2 - Language Separation]
- UI: Separated Changelog content for English and Vietnamese (cleaner view).
- Updated full version history for both languages.

[V8.1 - Final Polish]
- SETTINGS: Automatically saves your preferred language to config.json.
- UI FIX: Fixed text not updating immediately when switching languages.
- BUG FIX: Fixed a syntax error in the warning message.

[V8.0 - International & Batch Update]
- MULTI-LANGUAGE: Added English/Vietnamese toggle.
- BATCH EXTRACT: Now supports selecting and extracting multiple files at once.
- PROGRESS: Added a total progress bar for batch operations.

[V7.3 - Online Update]
- CONNECTION: Auto-check for updates from GitHub on startup.
- Notifies user and provides download link if a new version is available.

[V7.2 - Safety Update]
- SAFETY: Auto-detects if Blue Archive is currently running.
- WARNING: Warns user to close the game to prevent file corruption or conflicts.

[V7.1 - UI Polish]
- UI: Redesigned interface for a cleaner look.
- INFO: Added "Changelog" button.

[V7.0 - Smart Folder Management]
- FEATURE: Auto-increments folder names (e.g., File (1), File (2)...).
- Prevents accidental overwriting of previous extractions.

[V6.0 - Multimedia Support]
- MAJOR UPGRADE: Full asset extraction support.
- Audio: BGM, Voices (OGG, WAV, MP3).
- Video: Opening movies, cutscenes (WEBM).
- Animation: WebP images.
- Auto-sorts files into specific subfolders.

[V5.0 - Large File Support]
- PERFORMANCE: Fixed "Not Responding" freezing issues with large files (GBs).
- Memory optimization for lower-end PCs.

[V4.0 - PNG & Garbage Filtering]
- NEW FORMAT: Added PNG support (Icons, transparent images).
- CLEANUP: Improved filtering to remove invalid/corrupted files.

[V3.0 - Quality Fix]
- BUG FIX: Fixed an issue where the tool extracted thumbnails instead of full-res images.
- Logic updated to prioritize high-quality assets.

[V2.0 - GUI Update]
- Removed Command Line Interface (CMD).
- Added proper Window UI and Progress Bar.

[V1.0 - Initial Release]
- Basic version.
- Only supported JPG extraction.
"""
}

class UniversalExtractorApp:
    def __init__(self, root):
        self.root = root
        self.selected_files = []
        
        self.current_lang = self.load_config()
        
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        self.file_list_display = tk.StringVar()
        
        self.setup_icon()
        self.create_widgets()
        self.apply_language() 
        
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def load_config(self):
        """Đọc file config.json"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get("lang", "VN")
        except:
            pass
        return "VN"

    def save_config(self):
        """Lưu ngôn ngữ vào config.json"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"lang": self.current_lang}, f)
        except:
            pass

    def setup_icon(self):
        try:
            myappid = 'mycompany.bluearchive.extractor.v8'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            if getattr(sys, 'frozen', False): application_path = sys._MEIPASS
            else: application_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(application_path, "my_icon.ico")
            if os.path.exists(icon_path): self.root.iconbitmap(icon_path)
        except Exception: pass

    def create_widgets(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill="x", padx=20, pady=10)
        
        self.lang_var = tk.StringVar(value=self.current_lang)
        self.lbl_lang = tk.Label(frame_top, text="Language:", font=("Segoe UI", 9))
        self.lbl_lang.pack(side="right", padx=5)
        
        cb_lang = ttk.Combobox(frame_top, textvariable=self.lang_var, values=["VN", "EN"], state="readonly", width=5)
        cb_lang.pack(side="right")
        cb_lang.bind("<<ComboboxSelected>>", self.change_language)

        self.lbl_title = tk.Label(self.root, font=("Segoe UI", 16, "bold"), fg="#0056b3")
        self.lbl_title.pack(pady=(0, 5))
        
        self.lbl_ver = tk.Label(self.root, font=("Segoe UI", 9, "bold"), fg="gray")
        self.lbl_ver.pack()

        self.lbl_warning = tk.Label(self.root, font=("Segoe UI", 9, "bold"), fg="#d9534f")
        self.lbl_warning.pack(pady=(5, 10))

        self.grp_input = tk.LabelFrame(self.root, padx=10, pady=10)
        self.grp_input.pack(padx=20, pady=5, fill="x")

        self.entry_file = tk.Entry(self.grp_input, textvariable=self.file_list_display, width=50, state='readonly')
        self.entry_file.pack(side="left", fill="x", expand=True)
        
        self.btn_clear = tk.Button(self.grp_input, width=10, bg="#dc3545", fg="white", command=self.clear_files)
        self.btn_clear.pack(side="right", padx=(5, 0))

        self.btn_browse = tk.Button(self.grp_input, width=12, command=self.browse_files)
        self.btn_browse.pack(side="right", padx=5)

        frame_actions = tk.Frame(self.root)
        frame_actions.pack(padx=20, pady=10, fill="x")

        self.btn_extract = tk.Button(frame_actions, bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), height=2, command=self.start_batch_extraction)
        self.btn_extract.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_about = tk.Button(frame_actions, bg="#17a2b8", fg="white", font=("Segoe UI", 10), height=2, width=20, command=self.show_changelog)
        self.btn_about.pack(side="right")

        lbl_frame = tk.Frame(self.root)
        lbl_frame.pack(fill="x", padx=20, pady=(10, 0))
        self.lbl_current_file = tk.Label(lbl_frame, text="", font=("Segoe UI", 8), fg="blue")
        self.lbl_current_file.pack(side="left")
        
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=100, mode="determinate")
        self.progress.pack(padx=20, pady=(2, 5), fill="x")

        self.progress_total = ttk.Progressbar(self.root, orient="horizontal", length=100, mode="determinate")
        self.progress_total.pack(padx=20, pady=(0, 5), fill="x")

        self.lbl_status = tk.Label(self.root, fg="gray", font=("Segoe UI", 9))
        self.lbl_status.pack(pady=5)
        
        self.lbl_credit = tk.Label(self.root, font=("Segoe UI", 8, "italic"), fg="#aaa")
        self.lbl_credit.pack(side="bottom", pady=5)

    def change_language(self, event=None):
        self.current_lang = self.lang_var.get()
        self.save_config()
        self.apply_language()

    def get_text(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

    def apply_language(self):
        t = lambda k: self.get_text(k)
        self.root.title(t("title"))
        self.lbl_title.config(text=t("header"))
        self.lbl_ver.config(text=f"{t('ver_prefix')} {CURRENT_VERSION}")
        self.lbl_warning.config(text=t("warning"))
        self.grp_input.config(text=t("grp_input"))
        self.btn_browse.config(text=t("btn_browse"))
        self.btn_clear.config(text=t("btn_clear"))
        self.btn_extract.config(text=t("btn_extract"))
        self.btn_about.config(text=t("btn_history"))
        self.lbl_credit.config(text=t("credit"))
        self.lbl_lang.config(text=t("lbl_lang"))
        
        self.update_file_display()

    def update_file_display(self):
        """Cập nhật text hiển thị số lượng file"""
        t = lambda k: self.get_text(k)
        count = len(self.selected_files)
        if count > 0:
            self.file_list_display.set(t("txt_selected").format(count))
            if self.btn_extract['state'] == 'normal':
                self.lbl_status.config(text=t("status_ready"))
        else:
            self.file_list_display.set(t("txt_no_select"))
            if self.btn_extract['state'] == 'normal':
                self.lbl_status.config(text=t("status_ready"))

    def browse_files(self):
        """Chọn file chế độ cộng dồn"""
        files = filedialog.askopenfilenames(filetypes=[("Unity/Molru", "*.molru;*.bundle"), ("All Files", "*.*")])
        if files:
            added_count = 0
            for f in files:
                if f not in self.selected_files:
                    self.selected_files.append(f)
                    added_count += 1
            
            self.update_file_display()

    def clear_files(self):
        """Xóa toàn bộ danh sách đã chọn"""
        self.selected_files = []
        self.update_file_display()

    def show_changelog(self):
        top = tk.Toplevel(self.root)
        top.title(self.get_text("changelog_title"))
        top.geometry("600x450")
        try:
            if getattr(sys, 'frozen', False): app_path = sys._MEIPASS
            else: app_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(app_path, "my_icon.ico")
            if os.path.exists(icon_path): top.iconbitmap(icon_path)
        except: pass
        
        txt = scrolledtext.ScrolledText(top, wrap=tk.WORD, font=("Consolas", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        
        content = CHANGELOGS.get(self.current_lang, CHANGELOGS["VN"])
        
        txt.insert(tk.END, content)
        txt.config(state=tk.DISABLED)

    def check_for_updates(self):
        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
        t = lambda k: self.get_text(k)
        
        if self.btn_extract['state'] == 'normal':
             self.lbl_status.config(text=t("status_check"))

        try:
            with urllib.request.urlopen(api_url, timeout=3) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "")
                html_url = data.get("html_url", "")
                
                if latest_version and latest_version != CURRENT_VERSION:
                    self.root.after(0, lambda: self.show_update_dialog(latest_version, html_url))
                else:
                    self.root.after(0, lambda: self.lbl_status.config(text=t("status_latest"), fg="green"))
        except Exception:
            self.root.after(0, lambda: self.lbl_status.config(text=t("status_offline"), fg="orange"))

    def show_update_dialog(self, version, url):
        msg = self.get_text("update_msg").format(version, CURRENT_VERSION)
        choice = messagebox.askyesno("Update", msg)
        if choice:
            webbrowser.open(url)
            self.root.destroy()

    def check_game_running(self):
        try:
            if os.name == 'nt': creationflags = 0x08000000
            else: creationflags = 0
            output = subprocess.check_output('tasklist', creationflags=creationflags).decode('utf-8', errors='ignore')
            if "BlueArchive.exe" in output: return True
        except Exception: pass
        return False

    def start_batch_extraction(self):
        t = lambda k: self.get_text(k)
        
        if not self.selected_files:
            messagebox.showerror(t("msg_error_title"), t("msg_select_file"))
            return

        if self.check_game_running():
            if not messagebox.askyesno(t("msg_error_title"), t("msg_warn_game_running"), icon='warning'):
                return

        self.btn_extract.config(state="disabled")
        self.btn_browse.config(state="disabled")
        self.btn_clear.config(state="disabled")
        self.progress_total['value'] = 0
        
        threading.Thread(target=self.process_batch, daemon=True).start()

    def process_batch(self):
        t = lambda k: self.get_text(k)
        total_files = len(self.selected_files)
        
        app_path = get_app_path()

        for idx, src in enumerate(self.selected_files):
            file_name = os.path.splitext(os.path.basename(src))[0]
            
            status_msg = t("status_processing").format(idx + 1, total_files, file_name)
            self.root.after(0, lambda m=status_msg: self.lbl_status.config(text=m, fg="blue"))
            self.root.after(0, lambda m=f"Ext: {file_name}": self.lbl_current_file.config(text=m))
            
            total_prog = (idx / total_files) * 100
            self.root.after(0, lambda v=total_prog: self.progress_total.configure(value=v))

            try:
                base_output_dir = os.path.join(app_path, f"{file_name}_Extracted")
                final_output_dir = self.get_unique_output_folder(base_output_dir)
                os.makedirs(final_output_dir)

                with open(src, 'rb') as f:
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        self.process_mmap(mm, final_output_dir)
            except Exception as e:
                print(f"Error extracting {src}: {e}")
        
        self.root.after(0, lambda: self.progress_total.configure(value=100))
        self.root.after(0, lambda: self.lbl_status.config(text=t("status_done").format(total_files), fg="green"))
        self.root.after(0, lambda: self.lbl_current_file.config(text=""))
        self.root.after(0, lambda: messagebox.showinfo(t("msg_complete_title"), t("msg_complete_body").format(total_files)))
        
        self.root.after(0, lambda: self.btn_extract.config(state="normal"))
        self.root.after(0, lambda: self.btn_browse.config(state="normal"))
        self.root.after(0, lambda: self.btn_clear.config(state="normal"))

    def get_unique_output_folder(self, base):
        if not os.path.exists(base): return base
        c = 1
        while True:
            n = f"{base} ({c})"
            if not os.path.exists(n): return n
            c += 1

    def process_mmap(self, data, output_folder):
        file_size = len(data)
        pos = 0
        stats = {} 
        update_ui_step = 10 * 1024 * 1024
        next_ui_update = update_ui_step

        while pos < file_size:
            if pos > next_ui_update: 
                prog = (pos / file_size) * 100
                self.root.after(0, lambda v=prog: self.progress.configure(value=v))
                next_ui_update += update_ui_step
            
            header = data[pos : pos + 16]
            if len(header) < 16: break
            
            found_ext = None
            file_len = 0
            
            if header.startswith(b'RIFF'):
                try:
                    full_len = struct.unpack('<I', header[4:8])[0] + 8
                    t = header[8:12]
                    if t == b'WEBP': found_ext = 'webp'
                    elif t == b'WAVE': found_ext = 'wav'
                    elif t == b'AVI ': found_ext = 'avi'
                    if found_ext: file_len = full_len
                except: pass
            
            elif header.startswith(b'\x89PNG\r\n\x1a\n'):
                iend = data.find(b'IEND', pos)
                if iend != -1:
                    file_len = (iend - pos) + 8
                    found_ext = 'png'
            
            elif header.startswith(b'OggS'):
                found_ext = 'ogg'
                file_len = self.calc_ogg_length(data, pos)
            
            elif header.startswith(b'\xFF\xD8\xFF'):
                found_ext = 'jpg'
                end = self.find_jpeg_end(data, pos)
                if end != -1: file_len = end - pos
            
            elif header.startswith(b'\x1A\x45\xDF\xA3'):
                found_ext = 'webm'
                file_len = self.scan_until_next_header(data, pos)
            
            elif header.startswith(b'ID3'):
                found_ext = 'mp3'
                file_len = self.scan_until_next_header(data, pos)
            
            elif header.startswith(b'UnityFS'):
                 found_ext = 'assets'
                 file_len = self.scan_until_next_header(data, pos)

            if found_ext and file_len > 128:
                c = stats.get(found_ext, 0) + 1
                stats[found_ext] = c
                
                sub_dir = os.path.join(output_folder, found_ext)
                if not os.path.exists(sub_dir): os.makedirs(sub_dir)
                
                with open(os.path.join(sub_dir, f"file_{c}.{found_ext}"), 'wb') as f_out:
                    f_out.write(data[pos : pos + file_len])
                
                pos += file_len
            else:
                pos += 1
        
        self.root.after(0, lambda: self.progress.configure(value=100))

    def find_jpeg_end(self, data, start):
        p = start + 2
        max_scan = min(len(data), start + 20*1024*1024)
        while p < max_scan:
            if data[p] != 0xFF:
                nxt = data.find(b'\xFF', p, max_scan)
                if nxt == -1: return -1
                p = nxt
            if p + 1 >= max_scan: return -1
            m = data[p+1]
            if m == 0xD9: return p + 2
            if m == 0xDA:
                 nxt = data.find(b'\xFF\xD9', p, max_scan)
                 return nxt + 2 if nxt != -1 else -1
            if (0xD0 <= m <= 0xD7) or m == 0x00:
                p += 2; continue
            if p+4 > max_scan: return -1
            try: p += 2 + struct.unpack(">H", data[p+2:p+4])[0]
            except: return -1
        return -1

    def calc_ogg_length(self, data, start):
        p = start
        max_scan = len(data)
        while p < max_scan:
            if data[p:p+4] != b'OggS': break
            try:
                flags = data[p+5]
                n = data[p+26]
                sz = 27 + n + sum(data[p+27 : p+27+n])
                p += sz
                if flags & 0x04: return p - start
            except: break
        return p - start

    def scan_until_next_header(self, data, start):
        p = start + 4
        limit = min(len(data), start + 50*1024*1024)
        sigs = [b'RIFF', b'OggS', b'\xFF\xD8\xFF', b'\x89PNG', b'UnityFS']
        while p < limit:
            check = data[p:p+4]
            for s in sigs:
                if check.startswith(s): return p - start
            p += 1
        return p - start

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalExtractorApp(root)
    root.mainloop()
