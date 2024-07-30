import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class StatisticsView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title(f"{self.controller.config.title} Statistics")
        self.geometry("800x600")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.create_widgets()
        
    def on_closing(self):
        self.controller.stats_view = None
        self.destroy()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.heatmap_frame = ttk.Frame(self.notebook)
        self.key_freq_frame = ttk.Frame(self.notebook)
        self.hourly_dist_frame = ttk.Frame(self.notebook)
        self.summary_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.heatmap_frame, text='Keyboard Heatmap')
        self.notebook.add(self.key_freq_frame, text='Key Frequency')
        self.notebook.add(self.hourly_dist_frame, text='Hourly Distribution')
        self.notebook.add(self.summary_frame, text='Summary')

        self.create_keyboard_heatmap()
        self.create_key_freq_chart()
        self.create_hourly_dist_chart()
        self.create_summary()

    def create_keyboard_heatmap(self):
        self.heatmap_figure = Figure(figsize=(10, 4), dpi=100)
        self.heatmap_plot = self.heatmap_figure.add_subplot(111)
        self.heatmap_canvas = FigureCanvasTkAgg(self.heatmap_figure, self.heatmap_frame)
        self.heatmap_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_key_freq_chart(self):
        self.key_freq_figure = Figure(figsize=(8, 5), dpi=100)
        self.key_freq_plot = self.key_freq_figure.add_subplot(111)
        self.key_freq_canvas = FigureCanvasTkAgg(self.key_freq_figure, self.key_freq_frame)
        self.key_freq_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_hourly_dist_chart(self):
        self.hourly_dist_figure = Figure(figsize=(8, 5), dpi=100)
        self.hourly_dist_plot = self.hourly_dist_figure.add_subplot(111)
        self.hourly_dist_canvas = FigureCanvasTkAgg(self.hourly_dist_figure, self.hourly_dist_frame)
        self.hourly_dist_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_summary(self):
        self.summary_text = tk.Text(self.summary_frame, wrap=tk.WORD, font=("Arial", 12))
        self.summary_text.pack(expand=True, fill='both')

    def update_charts(self, stats):
        if not self.winfo_exists():
            return
        self.update_keyboard_heatmap(stats['key_counts'])
        self.update_key_freq_chart(stats['key_counts'])
        self.update_hourly_dist_chart(stats['hourly_counts'])
        self.update_summary(stats)
    
    def update_keyboard_heatmap(self, key_counts):
        self.heatmap_plot.clear()
        
        # 定义键盘布局
        keyboard_layout = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
            ['Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Enter', ''],
            ['Shift','', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift',  ''],
            ['Ctrl', 'Win', 'Alt', '','','', 'Space', '','','','Alt', 'Win', 'Menu', 'Ctrl']
        ]
        # 创建热力图数据
        heatmap_data = []
        for row in keyboard_layout:
            heatmap_row = []
            for key in row:
                count = key_counts.get(key.lower(), 0)
                heatmap_row.append(count)
            heatmap_data.append(heatmap_row)

        # 绘制热力图
        im = self.heatmap_plot.imshow(heatmap_data, cmap='YlOrRd')
        self.heatmap_figure.colorbar(im)

        # 添加键盘标签
        for i, row in enumerate(keyboard_layout):
            for j, key in enumerate(row):
                self.heatmap_plot.text(j, i, key, ha='center', va='center')

        self.heatmap_plot.set_title("Keyboard Heatmap")
        self.heatmap_plot.axis('off')
        self.heatmap_figure.tight_layout()
        self.heatmap_canvas.draw()

    def update_key_freq_chart(self, key_counts):
        self.key_freq_plot.clear()
        keys = [self.format_key_name(k) for k in key_counts.keys()]
        counts = list(key_counts.values())
        
        # 限制显示的键数量，例如只显示前20个最常用的键
        if len(keys) > 20:
            sorted_items = sorted(zip(keys, counts), key=lambda x: x[1], reverse=True)
            keys, counts = zip(*sorted_items[:20])
        
        self.key_freq_plot.bar(keys, counts)
        self.key_freq_plot.set_title("Key Frequency (Top 20)")
        self.key_freq_plot.set_xlabel("Keys")
        self.key_freq_plot.set_ylabel("Frequency")
        plt.setp(self.key_freq_plot.get_xticklabels(), rotation=45, ha='right')
        self.key_freq_figure.tight_layout()
        self.key_freq_canvas.draw()

    def update_hourly_dist_chart(self, hourly_counts):
        self.hourly_dist_plot.clear()
        hours = list(hourly_counts.keys())
        counts = list(hourly_counts.values())
        self.hourly_dist_plot.bar(hours, counts)
        self.hourly_dist_plot.set_title("Hourly Key Distribution")
        self.hourly_dist_plot.set_xlabel("Hour")
        self.hourly_dist_plot.set_ylabel("Key Count")
        self.hourly_dist_figure.tight_layout()
        self.hourly_dist_canvas.draw()

    def update_summary(self, stats):
        if not self.winfo_exists():
            return
        summary = f"""
            Total keystrokes: {stats['total_keystrokes']}
            Start time: {stats['start_time']}
            End time: {stats['end_time']}
            Total duration: {stats['total_duration']}
            Keystrokes per minute: {stats['keystrokes_per_minute']:.2f}
        """
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def format_key_name(self, key_combination):
        special_keys = {
            'Key.space': 'Space',
            'Key.enter': 'Enter',
            'Key.backspace': 'Backspace',
            'Key.shift': 'Shift',
            'Key.ctrl': 'Ctrl',
            'Key.alt': 'Alt',
            'Key.cmd': 'Cmd',
            'Key.caps_lock': 'CapsLock',
            'Key.tab': 'Tab',
            'Key.esc': 'Esc',
            # 添加更多特殊键的映射
        }
        
        parts = key_combination.split('+')
        formatted_parts = []
        
        for part in parts:
            if part in special_keys:
                formatted_parts.append(special_keys[part])
            elif part.startswith('Key.'):
                # 对于未在 special_keys 中列出的特殊键，移除 'Key.' 前缀并大写
                formatted_parts.append(part[4:].capitalize())
            elif len(part) == 1:
                # 对于单个字符，直接大写
                formatted_parts.append(part.upper())
            else:
                # 对于其他情况，保持原样
                formatted_parts.append(part)
        
        # 对组合键进行排序，使显示更一致
        formatted_parts.sort(key=lambda x: (x not in special_keys.values(), x))
        
        return ' + '.join(formatted_parts)