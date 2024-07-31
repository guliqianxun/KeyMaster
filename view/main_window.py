import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title(self.controller.config.title)
        self.geometry("400x450")
        self.configure(bg="#F0F0F0")  # 使用浅灰色背景
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