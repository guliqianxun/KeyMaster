import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("KeyMaster")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self, text="KeyMaster 正在运行...", font=("Arial", 12))
        self.status_label.pack(pady=20)

        self.save_button = ttk.Button(self, text="手动保存", command=self.controller.save_data)
        self.save_button.pack(pady=10)

        self.stats_button = ttk.Button(self, text="查看统计", command=self.controller.show_statistics)
        self.stats_button.pack(pady=10)

        self.quit_button = ttk.Button(self, text="退出", command=self.quit)
        self.quit_button.pack(pady=10)

    def update_status(self, message):
        self.status_label.config(text=message)

    def quit(self):
        self.controller.on_closing()
        super().quit()