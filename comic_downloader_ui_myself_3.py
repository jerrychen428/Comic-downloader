import os
import json
from tkinter import *
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog, colorchooser
from ttkbootstrap import Style
import tkinter as tk
import subprocess
import threading
from tkinter.scrolledtext import ScrolledText

class ComicDownloaderUI:
    SETTINGS_FILE = "settings.json"  # 保存用戶設置的文件

    def __init__(self, root):
        self.root = root
        self.root.title("8comic Comic Downloader")
        self.root.geometry("800x600")                
        self.style = Style(theme='darkly')
        
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.current_theme = self.load_theme()
        self.apply_theme(self.current_theme)

        # 設置初始字型大小
        self.default_font_size = 12
        self.update_global_font(self.default_font_size)

        # 菜單欄
        self.create_menu()
        
        # URL entry
        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(fill="x", padx=10, pady=5)
        self.url_label = ttk.Label(self.input_frame, text="Comic URL:")
        self.url_label.pack(side="left", padx=5)
        self.url_entry = ttk.Entry(self.input_frame, width=50)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.analyze_button = ttk.Button(self.input_frame, text="Analyze", command=self.start_analyze)
        self.analyze_button.pack(side="left", padx=5)
        
        # Path selection
        self.path_frame = ttk.Frame(root)
        self.path_frame.pack(fill="x", padx=10, pady=5)
        
        self.path_label = ttk.Label(self.path_frame, text="Save Path:")
        self.path_label.pack(side="left", fill="x", padx=5, pady=5)
        self.path_entry = ttk.Entry(self.path_frame, width=50)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.path_button = ttk.Button(self.path_frame, text="Browse", command=self.browse_save_path)
        self.path_button.pack(side="left", padx=5, pady=5)
        self.open_path_button = ttk.Button(self.path_frame, text="Open Folder", command=self.open_download_folder)
        self.open_path_button.pack(side="left", padx=5, pady=5)

        # Progress bars
        self.progress_frame = ttk.Frame(root)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_Totallabel = ttk.Label(self.progress_frame, text="Total_Progress:")
        self.progress_Totallabel.pack(side="left", padx=5)
        self.Total_progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=300, mode="determinate")
        self.Total_progress.pack(side="left", padx=5)                

        # Progress bar
        self.image_progress_frame = ttk.Frame(root)
        self.image_progress_frame.pack(fill="x", padx=10, pady=5)
        self.progress_imagelabel = ttk.Label(self.image_progress_frame, text="Image_Progress:")
        self.progress_imagelabel.pack(side="left", padx=5)
        self.image_progress = ttk.Progressbar(self.image_progress_frame, orient="horizontal", length=300, mode="determinate")
        self.image_progress.pack(side="left", padx=5)
        
        # ScrolledText area
        self.log_frame = ttk.LabelFrame(root, text="Log Output")
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)        
        self.log = scrolledtext.ScrolledText(self.log_frame, height=5)
        self.log.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.chapter_window = None  # Track the popup window
        
        # 操作按鈕區域
        self.action_frame = ttk.Frame(root)
        self.action_frame.pack(fill="x", padx=10, pady=10)
        self.clear_button = ttk.Button(self.action_frame, text="Clear Log", command=self.clear_log)
        self.clear_button.pack(side="left", padx=5)        

        # 佇列區域
        self.setup_queue_area()

        # 右鍵菜單
        self.setup_context_menu()

        # 操作按鈕區域
        self.setup_action_buttons()
        
        # 初始化變數
        self.save_path = os.path.dirname(os.path.abspath(__file__)) 
        self.queue_data = []  # 保存佇列資料，每個項目是一個字典，包含漫畫名稱、集數和儲存路徑
        self.is_paused = False  # 用於控制是否暫停下載
        self.pause_event = threading.Event()  # 用於暫停與續傳控制
        self.pause_event.set()  # 初始化為非暫停狀態
        self.task_status = []  # 每个任务的状态
        self.progress_bars = {}  # 每个任务的进度条        
        
    def start_analyze(self):
        self.log_message("start analyze")

    def apply_theme(self, theme_name):
        """應用主题，如果無效則使用默認主题"""
        try:
            available_themes = self.style.theme_names()
            if theme_name not in available_themes:
                messagebox.showwarning(
                    "Invalid Theme",
                    f"The theme '{theme_name}' is not available. Falling back to default theme.",
                )
                theme_name = "darkly"  # 回退到默認主题                
            self.style.theme_use(theme_name)
            # 强制更新界面
            self.root.update_idletasks()
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
            
    def create_menu(self):
        """建立功能表單"""
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # 設置子菜單 - 視窗
        settings_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # 設置 - 字型大小
        settings_menu.add_command(label="Set Font Size", command=self.set_font_size)
#         # 設置 - 元件顏色，目前功能未完常
#         settings_menu.add_command(label="Set Widget Color", command=self.set_widget_color)
        # 設置 - 背景顏色
        settings_menu.add_command(label="Set Background Color", command=self.set_background_color)
        # 設置 - 主題製作器
        settings_menu.add_command(label="Open Theme Creator", command=self.open_theme_creator)
        # 設置主題
        settings_menu.add_command(label="Change Theme", command=self.change_theme)

        # 幫助菜單
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Comic Downloader v1.0"))        
        
    # 功能函數
    # File menu functions
    def load_theme(self):
        """重設置文件中加載主题"""
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                return settings.get("theme", "darkly")  # 如果未设置主题，返回默认主题
        return "darkly"

    def save_theme(self, theme):
        """保存主题到設置文件"""
        settings = {"theme": theme}
        with open(self.SETTINGS_FILE, "w") as f:
            json.dump(settings, f)

    def change_theme(self):
        """打開更改主题的窗口"""
        theme_window = Toplevel(self.root)
        theme_window.title("Change Theme")
        theme_window.geometry("300x200")        

        # 獲取所有可用主题
        all_themes = self.style.theme_names()
        selected_theme = StringVar(value=self.current_theme)

        ttk.Label(theme_window, text="Select Theme:", style="TLabel").pack(pady=10)
        theme_dropdown = ttk.Combobox(
            theme_window, values=all_themes, textvariable=selected_theme, state="readonly", style="TCombobox"
        )
        theme_dropdown.pack(pady=10)        

        def apply():
            """应用选定的主题"""
            new_theme = selected_theme.get()
            self.apply_theme(new_theme)
            self.current_theme = new_theme
            self.save_theme(new_theme)
            messagebox.showinfo("Theme Changed", f"Theme changed to '{new_theme}'.")
            theme_window.destroy()

        def cancel():
            """取消主题更改"""
            theme_window.destroy()

        # 按鈕區
        button_frame = ttk.Frame(theme_window)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Apply", command=apply, style="TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel, style="TButton").pack(side="right", padx=5)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get("1.0", tk.END).strip())

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
    
    def open_theme_creator(self):

        """在控制台執行 python -m ttkcreator"""
        try:
            # 執行命令
            result = subprocess.run(
                ["python", "-m", "ttkcreator"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            # 輸出結果到控制台
            print("Output:")
            print(result.stdout)
            print("Errors (if any):")
            print(result.stderr)
        except Exception as e:
            print(f"Error executing command: {e}")
            
#         self.log_message("目前無法開啟,保留code待日後修正")

    def set_font_size(self):
        """改變字型大小"""
        size = simpledialog.askinteger("Font Size", "Enter font size (e.g., 10, 12, 16):", minvalue=8, maxvalue=72)
        if size:
            self.update_global_font(size) # 改變全局字型大小
            self.log_message(f"Font size set to {size}.")

    def update_global_font(self, font_size):
        """更新全局字型大小"""
        font_settings = (f"Helvetica {font_size}")
        self.style.configure('.', font=font_settings)  # 更新 ttk 元件樣式
        self.root.option_add("*Font", font_settings)  # 更新 tkinter 元件樣式

        # 更新視窗大小
        self.root.update_idletasks()  # 刷新元件尺寸
        width = max(self.root.winfo_reqwidth(), 800)  # 最小寬度為 800
        height = max(self.root.winfo_reqheight(), 600)  # 最小高度為 600
        self.root.geometry(f"{width}x{height}")  # 調整視窗大小


#     def set_widget_color(self): # 目前功未完善
#         """改變元件顏色"""
#         color = colorchooser.askcolor(title="Choose Widget Color")[1]
#         if color:
#             self.path_label.config(fg=color)
#             self.log_message(f"Widget color set to {color}.")

    def set_background_color(self):
        """改變背景顏色"""
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.root.config(bg=color)
            self.log_message(f"Background color set to {color}.")
        
    def get_url(self):
        return self.url_entry.get().strip()
    
    def get_save_path(self):
        return self.path_entry.get().strip()
    
    def set_save_path(self, path):
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, path)

    def show_chapter_popup(self):
        self.chapter_window = Toplevel(self.root)
        self.chapter_window.title("Select Chapters")
        self.chapter_window.geometry("600x350")

        # Create a scrollable frame
        canvas = Canvas(self.chapter_window)
        scrollbar = ttk.Scrollbar(self.chapter_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add checkboxes to scrollable frame
        for chapter_id, chapter_text in self.chapters:
            var = IntVar()
            check = ttk.Checkbutton(scrollable_frame, text=chapter_text, variable=var)
            check.pack(anchor="w")
            self.chapter_checks.append((var, chapter_text))
        
        # Confirm button
        confirm_button = ttk.Button(self.chapter_window, text="Confirm Selection", command=self.chapter_window.destroy)
        confirm_button.pack(padx=5)
        
    def clear_log(self):
        self.log.delete("1.0", "end")
        
    def log_message(self, message):
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)

    def update_status(self, message):
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
    
    def reset_progress(self):
        self.chapter_progress["value"] = 0
        self.image_progress["value"] = 0
        
    def open_download_folder(self):
        if self.save_path and os.path.exists(self.save_path):
            # Open the specified folder if it exists
            subprocess.Popen(f'explorer "{self.save_path}"' if os.name == 'nt' else ['open', self.save_path])
        else:
            # Open the default directory (e.g., home folder)
            default_path = os.path.dirname(os.path.abspath(__file__))# 將os.path.expanduser("~")改成當前py檔的路徑
            subprocess.Popen(f'explorer "{default_path}"' if os.name == 'nt' else ['open', default_path])            
            
    def check_chapters(self):
        """檢查章節下載狀況"""
        # 模擬找到的章節和下載狀況
        found_chapters = ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4"]
        downloaded_chapters = []

        if self.download_path:
            # 比對下載路徑中的檔案
            existing_files = os.listdir(self.download_path)
            downloaded_chapters = [ch for ch in found_chapters if f"{ch}.pdf" in existing_files]

        # 未下載的章節
        not_downloaded_chapters = [ch for ch in found_chapters if ch not in downloaded_chapters]

        # 彈出視窗顯示結果
        result_text = "Found Chapters:\n"
        result_text += "\n".join(f"✅ {ch}" for ch in downloaded_chapters) + "\n"
        result_text += "\n".join(f"❌ {ch}" for ch in not_downloaded_chapters)

        messagebox.showinfo("Chapter Check", result_text)

    def setup_queue_area(self):
        """設置佇列表格顯示區域"""
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(fill="x", padx=10, pady=5)
        self.queue_frame = ttk.LabelFrame(self.root, text="Download Queue")
        self.queue_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview表格
        columns = ("Comic Name", "Chapter", "Save Path", "Status", "Progress")
        self.queue_table = ttk.Treeview(
            self.queue_frame, columns=columns, show="headings", height=5
        )
        self.queue_table.pack(side="left", fill="both", expand=True)

        # 設置欄標題
        self.queue_table.heading("Comic Name", text="Comic Name", anchor=tk.W)
        self.queue_table.heading("Chapter", text="Chapter", anchor=tk.W)
        self.queue_table.heading("Save Path", text="Save Path", anchor=tk.W)
        self.queue_table.heading("Status", text="Status", anchor=tk.W)
        self.queue_table.heading("Progress", text="Progress", anchor=tk.W)

        # 設置欄寬
        self.queue_table.column("Comic Name", width=200, anchor=tk.W)
        self.queue_table.column("Chapter", width=15, anchor=tk.W)
        self.queue_table.column("Save Path", width=200, anchor=tk.W)
        self.queue_table.column("Status", width=20, anchor=tk.W)
        self.queue_table.column("Progress", width=15, anchor=tk.W)

        # 滾動條
        queue_scroll = ttk.Scrollbar(
            self.queue_frame, orient="vertical", command=self.queue_table.yview
        )
        queue_scroll.pack(side="right", fill="y")
        self.queue_table.configure(yscrollcommand=queue_scroll.set)

        # 點擊事件綁定（右鍵菜單）
        self.queue_table.bind("<Button-3>", self.show_context_menu)

    def setup_context_menu(self):
        """設置右鍵菜單"""
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Pause Task", command=self.pause_task)
        self.context_menu.add_command(label="Delete Task", command=self.delete_task)
        self.context_menu.add_command(label="Resume Task", command=self.resume_task)

    def setup_action_buttons(self):
        """設置操作按鈕區域"""
        self.action_frame = ttk.Frame(self.root)
        self.action_frame.pack(fill="x", padx=10, pady=5)

        self.add_to_queue_button = ttk.Button(
            self.action_frame, text="Add to Queue", command=self.add_to_queue
        )
        self.add_to_queue_button.pack(side="left", padx=5)

        self.start_download_button = ttk.Button(
            self.action_frame, text="Start Download", command=self.Start_1
        )
        self.start_download_button.pack(side="left", padx=5)

    def show_context_menu(self, event):
        """顯示右鍵菜單"""
        try:
            self.selected_item = self.queue_table.identify_row(event.y)
            if self.selected_item:
                self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def pause_task(self):
        print("Download paused.")

    def delete_task(self):
        print("Delete Task", "Task deleted.")

    def resume_task(self):
        print("resume_task")
        
    def browse_save_path(self):
        path = filedialog.askdirectory()

        if path:  # 如果用戶選擇了路徑            
            self.save_path = os.path.normpath(path) # 標準化路徑, 連結filedialog.askdirectory()與OS不同設定路徑方法
            self.set_save_path(self.save_path) # 顯示選擇路徑於entry中
        else:
            self.log_message("未選擇路徑")

    def add_to_queue(self):
#         [{'task_index': 0, 'Comic Name': '劍聖女的重啟人生', 'Chapter': '2話', 'Save Path': 'C:\\Users\\jerry\\python_myself\\8cmoic_downloader', 'Chapter_id': 'c2', 'progress': '0%', 'status': 'Pending'}, {'task_index': 1, 'Comic Name': '劍聖女的重啟人生', 'Chapter': '3話', 'Save Path': 'C:\\Users\\jerry\\python_myself\\8cmoic_downloader', 'Chapter_id': 'c3', 'progress': '0%', 'status': 'Pending'}, {'task_index': 2, 'Comic Name': '劍聖女的重啟人生', 'Chapter': '第04話', 'Save Path': 'C:\\Users\\jerry\\python_myself\\8cmoic_downloader', 'Chapter_id': 'c4', 'progress': '0%', 'status': 'Pending'}]
        self.log_message("Add to queue")
        
    def Start_1(self):
        self.log_message("Start_1")
        
    def submmit_selected(self):
        self.log_message("Submmit selected")
        
if __name__ == "__main__":
    root = Tk()
    show = ComicDownloaderUI(root)
    root.mainloop()



