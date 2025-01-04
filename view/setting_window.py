import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class SettingWindow(tk.Toplevel):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("设置")
        self.geometry("400x300")
        self.configure(bg="#F0F0F0")

        self.create_widgets()

    def create_widgets(self):
        # 创建日志路径配置
        log_label = tk.Label(self, text="日志路径：", bg="#F0F0F0")
        log_label.pack(pady=5)
        self.log_entry = tk.Entry(
            self, textvariable=tk.StringVar(value=self.controller.config.log_folder), width=40
        )
        self.log_entry.pack(pady=5)
        log_browse_button = tk.Button(self, text="浏览", command=self.browse_log_folder)
        log_browse_button.pack(pady=5)

        # 创建 CSV 文件路径配置
        csv_label = tk.Label(self, text="CSV 文件路径：", bg="#F0F0F0")
        csv_label.pack(pady=5)
        self.csv_entry = tk.Entry(
            self, textvariable=tk.StringVar(value=self.controller.config.csv_folder), width=40
        )
        self.csv_entry.pack(pady=5)
        csv_browse_button = tk.Button(self, text="浏览", command=self.browse_csv_folder)
        csv_browse_button.pack(pady=5)

        # 保存按钮
        save_button = tk.Button(self, text="保存", command=self.save_settings)
        save_button.pack(pady=20)

    def browse_log_folder(self):
        """浏览日志文件夹"""
        folder = filedialog.askdirectory()
        if folder:
            self.log_entry.delete(0, tk.END)
            self.log_entry.insert(0, folder)

    def browse_csv_folder(self):
        """浏览 CSV 文件夹"""
        folder = filedialog.askdirectory()
        if folder:
            self.csv_entry.delete(0, tk.END)
            self.csv_entry.insert(0, folder)

    def save_settings(self):
        """保存用户修改的设置"""
        self.controller.config.log_folder = self.log_entry.get()
        self.controller.config.csv_folder = self.csv_entry.get()
        self.controller.config.save_config()
        messagebox.showinfo("成功", "设置已保存！")
