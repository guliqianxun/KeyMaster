import winreg
import os
import sys
import tkinter as tk 
from tkinter import ttk
import tkinter.font as tkfont

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title(self.controller.config.title)
        self.geometry("400x500")
        self.configure(bg="#F0F0F0") 
        self.startup_var = tk.BooleanVar()
        self.startup_var.set(self.is_in_startup())
        self.create_widgets()

    def create_widgets(self):
        # 创建自定义字体
        title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        button_font = tkfont.Font(family="Helvetica", size=12)

        # 标题框架
        title_frame = tk.Frame(self, bg="#4285F4", height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text=self.controller.config.title, font=title_font, bg="#4285F4", fg="white")
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # 主内容框架
        content_frame = tk.Frame(self, bg="#F0F0F0")
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # 状态标签
        self.status_label = tk.Label(content_frame, text=f"{self.controller.config.title} 正在运行...", 
                                     font=("Helvetica", 12), bg="#F0F0F0", fg="#5F6368")
        self.status_label.pack(pady=20)

        # 创建按钮
        button_styles = [
            {"text": "手动保存", "bg": "#4CAF50", "command": self.controller.save_data},
            {"text": "查看统计", "bg": "#2196F3", "command": self.controller.show_statistics},
            {"text": "退出", "bg": "#F44336", "command": self.quit}
        ]

        for style in button_styles:
            button = tk.Button(content_frame, text=style["text"], font=button_font,
                               bg=style["bg"], fg="white", relief=tk.FLAT,
                               command=style["command"], width=15, height=2)
            button.pack(pady=10)
            button.bind("<Enter>", lambda e, b=button: self.on_hover(e, b))
            button.bind("<Leave>", lambda e, b=button: self.on_leave(e, b))

        # 开机自启动复选框
        startup_frame = tk.Frame(content_frame, bg="#F0F0F0")
        startup_frame.pack(pady=10)

        startup_checkbox = ttk.Checkbutton(startup_frame, text="开机自启动", 
                                           variable=self.startup_var, 
                                           command=self.toggle_startup,
                                           style="TCheckbutton")
        startup_checkbox.pack(side=tk.LEFT)

        # Configure checkbutton style
        style = ttk.Style()
        style.configure("TCheckbutton", background="#F0F0F0", font=("Helvetica", 12))

    def toggle_startup(self):
        if self.startup_var.get():
            self.add_to_startup_registry()
        else:
            self.remove_from_startup_registry()

    def add_to_startup_registry(self):
        file_path = os.path.abspath(sys.argv[0])
        key_path = r"Software\\Microsoft\Windows\\CurrentVersion\\Run"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, self.controller.config.title, 0, winreg.REG_SZ, file_path)
            winreg.CloseKey(key)
            self.update_status("已添加到开机自启动")
        except WindowsError:
            self.update_status("添加到开机自启动失败")

    def remove_from_startup_registry(self):
        key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key, self.controller.config.title)
            winreg.CloseKey(key)
            self.update_status("已从开机自启动中移除")
        except WindowsError:
            self.update_status("从开机自启动中移除失败")

    def is_in_startup(self):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, self.controller.config.title)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False
    def on_hover(self, event, button):
        button.config(bg=self.lighten_color(button.cget("bg")))

    def on_leave(self, event, button):
        button.config(bg=self.darken_color(button.cget("bg")))

    def lighten_color(self, color):
        # 简单的颜色变亮函数
        r, g, b = self.winfo_rgb(color)
        return f"#{min(r+1000, 65535):04x}{min(g+1000, 65535):04x}{min(b+1000, 65535):04x}"

    def darken_color(self, color):
        # 简单的颜色变暗函数
        r, g, b = self.winfo_rgb(color)
        return f"#{max(r-1000, 0):04x}{max(g-1000, 0):04x}{max(b-1000, 0):04x}"

    def update_status(self, message):
        self.status_label.config(text=message)

    def quit(self):
        self.controller.on_closing()
        super().quit()