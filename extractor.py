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
CURRENT_VERSION = "v7.3"

CHANGELOG_TEXT = """
=== LỊCH SỬ CẬP NHẬT ===

[V7.3 - Online Update] (Phiên bản hiện tại)
- KẾT NỐI: Tự động kiểm tra phiên bản mới từ GitHub khi mở phần mềm.
- Nếu có bản mới, chương trình sẽ thông báo và dẫn link tải về.

[V7.2 - Safety Update]
- AN TOÀN: Tự động phát hiện nếu game Blue Archive đang chạy.
- CẢNH BÁO: Hiện thông báo nhắc nhở người dùng tắt game trước khi giải nén để tránh xung đột file hoặc lỗi game.

[V7.1 - Final Polish]
- GIAO DIỆN: Làm lại giao diện.
- THÔNG TIN: Thêm nút xem "Lịch sử cập nhật" để anh em tiện theo dõi các thay đổi.
- Hoàn thiện các tính năng.

[V7.0 - Quản lý thư mục thông minh]
- TÍNH NĂNG MỚI: Tự động đánh số thư mục.
- Nếu anh em giải nén 2 lần cùng 1 file, lần sau tool sẽ tự tạo folder tên là "TenFile (1)", "TenFile (2)"...
- Tác dụng: Giúp anh em không bao giờ bị ghi đè hay mất file cũ nếu lỡ tay bấm giải nén nhiều lần.

[V6.0 - Cập nhật Đa phương tiện]
- NÂNG CẤP LỚN: Không chỉ lấy ảnh, giờ tool lấy được tất cả mọi thứ.
- Lấy được Âm thanh: Nhạc nền, giọng nói nhân vật (OGG, WAV, MP3).
- Lấy được Video: Các đoạn phim mở đầu, hoạt cảnh (WEBM).
- Lấy được Ảnh động: Các file ảnh WebP.
- Tool tự động nhận diện file nào là ảnh, file nào là nhạc để xếp vào folder riêng.

[V5.0 - Hỗ trợ File lớn]
- HIỆU NĂNG: Sửa lỗi bị treo máy (Not Responding) khi giải nén các file game nặng hàng Gigabyte (GB).
- Anh em nào máy yếu, ít RAM vẫn có thể giải nén file game nặng 5GB - 10GB mà không bị đơ máy.

[V4.0 - Hỗ trợ PNG & Lọc rác]
- ẢNH MỚI: Hỗ trợ lấy thêm định dạng ảnh PNG (thường là các icon, ảnh trong suốt).
- LỌC RÁC: Tool sẽ kiểm tra kỹ hơn để đảm bảo những gì xuất ra là ảnh thật 100%, loại bỏ hoàn toàn các file lỗi (file rác) không mở được.

[V3.0 - Sửa lỗi ảnh mờ]
- SỬA LỖI: Tool hay cắt nhầm mấy ảnh nhỏ (thumbnail) làm ảnh bị mờ.
- GIẢI PHÁP: Dạy tool cách bỏ qua ảnh nhỏ để lấy đúng ảnh gốc sắc nét nhất.

[V2.0 - Có giao diện]
- Bỏ màn hình đen (CMD).
- Thêm cửa sổ, nút bấm và thanh chạy phần trăm.

[V1.0 - Bản đầu tiên]
- Phiên bản sơ khai.
- Tìm và cắt file ảnh JPG.
"""

class UniversalExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Blue Archive Extractor {CURRENT_VERSION} (Auto-Update)")
        self.root.geometry("720x480")
        self.root.resizable(False, False)
        self.file_path = tk.StringVar()
        
        self.setup_icon()
        self.create_widgets()
        
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def setup_icon(self):
        try:
            myappid = 'mycompany.bluearchive.extractor.v7'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            if getattr(sys, 'frozen', False): application_path = sys._MEIPASS
            else: application_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(application_path, "my_icon.ico")
            if os.path.exists(icon_path): self.root.iconbitmap(icon_path)
        except Exception: pass

    def create_widgets(self):
        lbl_title = tk.Label(self.root, text="BLUE ARCHIVE ASSET EXTRACTOR", font=("Segoe UI", 16, "bold"), fg="#0056b3")
        lbl_title.pack(pady=(15, 5))
        
        lbl_ver = tk.Label(self.root, text=f"Version: {CURRENT_VERSION}", font=("Segoe UI", 9, "bold"), fg="gray")
        lbl_ver.pack()

        lbl_warning = tk.Label(self.root, text="⚠️ LƯU Ý: Vui lòng TẮT GAME trước khi giải nén!", font=("Segoe UI", 9, "bold"), fg="#d9534f")
        lbl_warning.pack(pady=(5, 10))

        grp_input = tk.LabelFrame(self.root, text="Chọn file dữ liệu (.molru / .bundle)", padx=10, pady=10)
        grp_input.pack(padx=20, pady=5, fill="x")

        entry_file = tk.Entry(grp_input, textvariable=self.file_path, width=70)
        entry_file.pack(side="left", fill="x", expand=True)
        
        btn_browse = tk.Button(grp_input, text="...", width=5, command=self.browse_file)
        btn_browse.pack(side="right", padx=5)

        frame_actions = tk.Frame(self.root)
        frame_actions.pack(padx=20, pady=10, fill="x")

        self.btn_extract = tk.Button(frame_actions, text="BẮT ĐẦU QUÉT & GIẢI NÉN", bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), height=2, command=self.start_extraction)
        self.btn_extract.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_about = tk.Button(frame_actions, text="Lịch sử cập nhật", bg="#17a2b8", fg="white", font=("Segoe UI", 10), height=2, width=20, command=self.show_changelog)
        btn_about.pack(side="right")

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=100, mode="determinate")
        self.progress.pack(padx=20, pady=(10,5), fill="x")

        self.lbl_status = tk.Label(self.root, text="Đang kiểm tra cập nhật...", fg="gray", font=("Segoe UI", 9))
        self.lbl_status.pack(pady=5)
        
        lbl_credit = tk.Label(self.root, text="Made by Community | Powered by Python", font=("Segoe UI", 8, "italic"), fg="#aaa")
        lbl_credit.pack(side="bottom", pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Unity/Molru", "*.molru;*.bundle")])
        if filename: self.file_path.set(filename)

    def show_changelog(self):
        top = tk.Toplevel(self.root)
        top.title("Lịch sử cập nhật")
        top.geometry("500x400")
        try:
            if getattr(sys, 'frozen', False): app_path = sys._MEIPASS
            else: app_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(app_path, "my_icon.ico")
            if os.path.exists(icon_path): top.iconbitmap(icon_path)
        except: pass
        txt = scrolledtext.ScrolledText(top, wrap=tk.WORD, font=("Consolas", 10))
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert(tk.END, CHANGELOG_TEXT)
        txt.config(state=tk.DISABLED)

    def check_for_updates(self):
        api_url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
        
        try:
            with urllib.request.urlopen(api_url, timeout=3) as response:
                data = json.loads(response.read().decode())
                
                latest_version = data.get("tag_name", "")
                html_url = data.get("html_url", "")
                
                if latest_version and latest_version != CURRENT_VERSION:
                    self.root.after(0, lambda: self.show_update_dialog(latest_version, html_url))
                else:
                    self.root.after(0, lambda: self.lbl_status.config(text=f"Bạn đang dùng phiên bản mới nhất ({CURRENT_VERSION}).", fg="green"))

        except Exception:
            self.root.after(0, lambda: self.lbl_status.config(text="Chế độ Offline (Không thể kiểm tra cập nhật).", fg="orange"))

    def show_update_dialog(self, version, url):
        msg = f"Đã có phiên bản mới: {version}!\n\nBạn đang dùng: {CURRENT_VERSION}\nBạn có muốn tải về ngay không?"
        choice = messagebox.askyesno("Cập nhật phần mềm", msg)
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

    def start_extraction(self):
        src = self.file_path.get()
        if not src or not os.path.exists(src):
            messagebox.showerror("Lỗi", "Vui lòng chọn file hợp lệ!")
            return

        if self.check_game_running():
            msg = "CẢNH BÁO: Game đang chạy! Hãy tắt game để tránh lỗi."
            if not messagebox.askyesno("Cảnh báo", msg + "\nTiếp tục giải nén?", icon='warning'):
                return

        try:
            if getattr(sys, 'frozen', False): app_path = os.path.dirname(sys.executable)
            else: app_path = os.path.dirname(os.path.abspath(__file__))

            file_name = os.path.splitext(os.path.basename(src))[0]
            base_output_dir = os.path.join(app_path, f"{file_name}_Extracted")
            final_output_dir = self.get_unique_output_folder(base_output_dir)
            os.makedirs(final_output_dir)
            
            self.lbl_status.config(text=f"Đang xuất ra: {os.path.basename(final_output_dir)}", fg="blue")
            self.root.update()

            with open(src, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    self.process_mmap(mm, final_output_dir)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi: {str(e)}")
            self.lbl_status.config(text="Thất bại!", fg="red")
    
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
        while pos < file_size:
            if pos % (10*1024*1024) == 0: 
                self.progress["value"] = (pos / file_size) * 100
                self.root.update()
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

            if found_ext and file_len > 128:
                c = stats.get(found_ext, 0) + 1
                stats[found_ext] = c
                out_name = f"file_{c}.{found_ext}"
                sub_dir = os.path.join(output_folder, found_ext)
                if not os.path.exists(sub_dir): os.makedirs(sub_dir)
                with open(os.path.join(sub_dir, out_name), 'wb') as f_out:
                    f_out.write(data[pos : pos + file_len])
                pos += file_len
            else:
                pos += 1
        
        self.progress["value"] = 100
        try: os.startfile(output_folder)
        except: pass
        report = f"HOÀN TẤT!\nFolder: {os.path.basename(output_folder)}\n"
        for k, v in stats.items(): report += f"- {k.upper()}: {v}\n"
        if not stats: report = "Không tìm thấy file."
        self.lbl_status.config(text="Xong.", fg="green")
        messagebox.showinfo("Kết quả", report)

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
            flags = data[p+5]
            n = data[p+26]
            sz = 27 + n + sum(data[p+27 : p+27+n])
            p += sz
            if flags & 0x04: return p - start
        return p - start

    def scan_until_next_header(self, data, start):
        p = start + 4
        limit = min(len(data), start + 50*1024*1024)
        sigs = [b'RIFF', b'OggS', b'\xFF\xD8\xFF', b'\x89PNG']
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