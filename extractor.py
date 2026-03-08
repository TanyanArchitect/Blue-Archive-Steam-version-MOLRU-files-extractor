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

try:
    from locales import TRANSLATIONS, CHANGELOGS
except ImportError:
    print("Thiếu file locales.py! Vui lòng đặt file này cùng thư mục với extractor.py.")
    sys.exit()

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    print("Thiếu thư viện tkinterdnd2. Vui lòng chạy: pip install tkinterdnd2")
    sys.exit()

GITHUB_USER = "TanyanArchitect"
GITHUB_REPO = "Blue-Archive-Steam-version-MOLRU-files-extractor"
CURRENT_VERSION = "v8.6"

def get_app_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(get_app_path(), "config.json")

class UniversalExtractorApp:
    def __init__(self, root):
        self.root = root
        self.selected_files = []
        
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop_files)

        self.current_lang = self.load_config()
        
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        self.file_list_display = tk.StringVar()
        
        self.setup_icon()
        self.create_widgets()
        self.apply_language() 
        
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def on_drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        added_count = 0
        for f in files:
            if os.path.isfile(f) and f not in self.selected_files:
                self.selected_files.append(f)
                added_count += 1
        if added_count > 0:
            self.update_file_display()

    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get("lang", "EN")
        except: pass
        return "EN"

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"lang": self.current_lang}, f)
        except: pass

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
        
        cb_lang = ttk.Combobox(frame_top, textvariable=self.lang_var, values=["CN", "JP", "KR", "EN", "VN"], state="readonly", width=5)
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
        lang_dict = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["EN"])
        return lang_dict.get(key, key)

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
        files = filedialog.askopenfilenames(filetypes=[("Unity/Molru", "*.molru;*.bundle"), ("All Files", "*.*")])
        if files:
            added = 0
            for f in files:
                if f not in self.selected_files:
                    self.selected_files.append(f)
                    added += 1
            if added > 0: self.update_file_display()

    def clear_files(self):
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
        
        content = CHANGELOGS.get(self.current_lang, CHANGELOGS["EN"])
        txt.insert(tk.END, content)

        url_to_find = "https://github.com/SS3-4001"
        start_idx = '1.0'
        while True:
            start_idx = txt.search(url_to_find, start_idx, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(url_to_find)}c"
            txt.tag_add("github_link", start_idx, end_idx)
            start_idx = end_idx

        txt.tag_config("github_link", foreground="#0056b3", underline=True)
        txt.tag_bind("github_link", "<Enter>", lambda e: txt.config(cursor="hand2"))
        txt.tag_bind("github_link", "<Leave>", lambda e: txt.config(cursor=""))
        txt.tag_bind("github_link", "<Button-1>", lambda e: webbrowser.open(url_to_find))

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
        
        base_output_root = os.path.join(app_path, "BA_Extracted")
        if not os.path.exists(base_output_root): os.makedirs(base_output_root)

        last_opened_folder = base_output_root

        for idx, src in enumerate(self.selected_files):
            file_name = os.path.splitext(os.path.basename(src))[0]
            
            file_output_dir = os.path.join(base_output_root, file_name)
            if not os.path.exists(file_output_dir): os.makedirs(file_output_dir)
            
            last_opened_folder = file_output_dir
            
            status_msg = t("status_processing").format(idx + 1, total_files, file_name)
            self.root.after(0, lambda m=status_msg: self.lbl_status.config(text=m, fg="blue"))
            self.root.after(0, lambda m=f"Ext: {file_name}": self.lbl_current_file.config(text=m))
            total_prog = (idx / total_files) * 100
            self.root.after(0, lambda v=total_prog: self.progress_total.configure(value=v))

            try:
                with open(src, 'rb') as f:
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        self.process_mmap(mm, file_output_dir)
            except Exception as e:
                print(f"Error extracting {src}: {e}")
        
        self.root.after(0, lambda: self.progress_total.configure(value=100))
        self.root.after(0, lambda: self.lbl_status.config(text=t("status_done").format(total_files), fg="green"))
        self.root.after(0, lambda: self.lbl_current_file.config(text=""))
        self.root.after(0, lambda: messagebox.showinfo(t("msg_complete_title"), t("msg_complete_body").format(total_files)))
        
        folder_to_open = base_output_root if total_files > 1 else last_opened_folder
        self.root.after(0, lambda: self.open_folder(folder_to_open))

        self.root.after(0, lambda: self.btn_extract.config(state="normal"))
        self.root.after(0, lambda: self.btn_browse.config(state="normal"))
        self.root.after(0, lambda: self.btn_clear.config(state="normal"))

    def open_folder(self, path):
        try:
            os.startfile(path)
        except Exception: pass

    def get_unique_subfolder(self, base_dir, ext_name):
        target = os.path.join(base_dir, ext_name)
        if not os.path.exists(target):
            return target
        c = 1
        while True:
            n = os.path.join(base_dir, f"{ext_name} ({c})")
            if not os.path.exists(n): return n
            c += 1

    def process_mmap(self, data, output_folder):
        file_size = len(data)
        pos = 0
        stats = {} 
        
        current_session_folders = {}

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
                if iend != -1: file_len = (iend - pos) + 8; found_ext = 'png'
            elif header.startswith(b'OggS'): found_ext = 'ogg'; file_len = self.calc_ogg_length(data, pos)
            elif header.startswith(b'\xFF\xD8\xFF'): found_ext = 'jpg'; end = self.find_jpeg_end(data, pos); file_len = end - pos if end != -1 else 0
            elif header.startswith(b'\x1A\x45\xDF\xA3'): found_ext = 'webm'; file_len = self.scan_until_next_header(data, pos)
            elif header.startswith(b'ID3'): found_ext = 'mp3'; file_len = self.scan_until_next_header(data, pos)
            elif header.startswith(b'UnityFS'): found_ext = 'assets'; file_len = self.scan_until_next_header(data, pos)

            if found_ext and file_len > 128:
                if found_ext not in current_session_folders:
                    unique_sub = self.get_unique_subfolder(output_folder, found_ext)
                    os.makedirs(unique_sub, exist_ok=True)
                    current_session_folders[found_ext] = unique_sub
                
                target_dir = current_session_folders[found_ext]
                
                c = stats.get(found_ext, 0) + 1
                stats[found_ext] = c
                
                with open(os.path.join(target_dir, f"file_{c}.{found_ext}"), 'wb') as f_out: 
                    f_out.write(data[pos : pos + file_len])
                pos += file_len
            else: pos += 1
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
            if (0xD0 <= m <= 0xD7) or m == 0x00: p += 2; continue
            if p+4 > max_scan: return -1
            try: p += 2 + struct.unpack(">H", data[p+2:p+4])[0]
            except: return -1
        return -1
    
    def calc_ogg_length(self, data, start):
        p = start; max_scan = len(data)
        while p < max_scan:
            if data[p:p+4] != b'OggS': break
            try:
                flags = data[p+5]; n = data[p+26]; sz = 27 + n + sum(data[p+27 : p+27+n]); p += sz
                if flags & 0x04: return p - start
            except: break
        return p - start
    
    def scan_until_next_header(self, data, start):
        p = start + 4; limit = min(len(data), start + 50*1024*1024); sigs = [b'RIFF', b'OggS', b'\xFF\xD8\xFF', b'\x89PNG', b'UnityFS']
        while p < limit:
            check = data[p:p+4]
            for s in sigs:
                if check.startswith(s): return p - start
            p += 1
        return p - start

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = UniversalExtractorApp(root)
    root.mainloop()
