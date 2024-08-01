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
        self.update_keyboard_heatmap(stats['key_release_counts'])
        self.update_key_freq_chart(stats['key_counts'])
        self.update_hourly_dist_chart(stats['hourly_counts'])
        self.update_summary(stats)
    
    def update_keyboard_heatmap(self, key_counts):
        self.heatmap_plot.clear()
        
        # Define the keyboard layout with precise positions and sizes
        keyboard_layout = {
            # Function keys row
            'Esc': (0, 0, 1, 1), 'F1': (0, 2, 1, 1), 'F2': (0, 3, 1, 1), 'F3': (0, 4, 1, 1), 'F4': (0, 5, 1, 1),
            'F5': (0, 6.5, 1, 1), 'F6': (0, 7.5, 1, 1), 'F7': (0, 8.5, 1, 1), 'F8': (0, 9.5, 1, 1),
            'F9': (0, 11, 1, 1), 'F10': (0, 12, 1, 1), 'F11': (0, 13, 1, 1), 'F12': (0, 14, 1, 1),
            'PrtSc': (0, 15.25, 1, 1), 'ScrLk': (0, 16.25, 1, 1), 'Pause': (0, 17.25, 1, 1),

            # Number row
            '`': (1, 0, 1, 1), '1': (1, 1, 1, 1), '2': (1, 2, 1, 1), '3': (1, 3, 1, 1), '4': (1, 4, 1, 1),
            '5': (1, 5, 1, 1), '6': (1, 6, 1, 1), '7': (1, 7, 1, 1), '8': (1, 8, 1, 1), '9': (1, 9, 1, 1),
            '0': (1, 10, 1, 1), '-': (1, 11, 1, 1), '=': (1, 12, 1, 1), 'Backspace': (1, 13, 2, 1),

            # QWERTY row
            'Tab': (2, 0, 1.5, 1), 'Q': (2, 1.5, 1, 1), 'W': (2, 2.5, 1, 1), 'E': (2, 3.5, 1, 1), 'R': (2, 4.5, 1, 1),
            'T': (2, 5.5, 1, 1), 'Y': (2, 6.5, 1, 1), 'U': (2, 7.5, 1, 1), 'I': (2, 8.5, 1, 1), 'O': (2, 9.5, 1, 1),
            'P': (2, 10.5, 1, 1), '[': (2, 11.5, 1, 1), ']': (2, 12.5, 1, 1), '\\': (2, 13.5, 1.5, 1),

            # Home row
            'Caps': (3, 0, 1.75, 1), 'A': (3, 1.75, 1, 1), 'S': (3, 2.75, 1, 1), 'D': (3, 3.75, 1, 1), 'F': (3, 4.75, 1, 1),
            'G': (3, 5.75, 1, 1), 'H': (3, 6.75, 1, 1), 'J': (3, 7.75, 1, 1), 'K': (3, 8.75, 1, 1), 'L': (3, 9.75, 1, 1),
            ';': (3, 10.75, 1, 1), "'": (3, 11.75, 1, 1), 'Enter': (3, 12.75, 2.25, 1),

            # Shift row
            'LShift': (4, 0, 2.25, 1), 'Z': (4, 2.25, 1, 1), 'X': (4, 3.25, 1, 1), 'C': (4, 4.25, 1, 1), 'V': (4, 5.25, 1, 1),
            'B': (4, 6.25, 1, 1), 'N': (4, 7.25, 1, 1), 'M': (4, 8.25, 1, 1), ',': (4, 9.25, 1, 1), '.': (4, 10.25, 1, 1),
            '/': (4, 11.25, 1, 1), 'RShift': (4, 12.25, 2.75, 1),

            # Bottom row
            'LCtrl': (5, 0, 1.25, 1), 'LWin': (5, 1.25, 1.25, 1), 'LAlt': (5, 2.5, 1.25, 1), 'Space': (5, 3.75, 6.25, 1),
            'RAlt': (5, 10, 1.25, 1), 'RWin': (5, 11.25, 1.25, 1), 'Menu': (5, 12.5, 1.25, 1), 'RCtrl': (5, 13.75, 1.25, 1),

            # Arrow keys
            'Up': (4, 16.25, 1, 1), 'Left': (5, 15.25, 1, 1), 'Down': (5, 16.25, 1, 1), 'Right': (5, 17.25, 1, 1),

            # Numpad
            'Num7': (2, 15.5, 1, 1), 'Num8': (2, 16.5, 1, 1), 'Num9': (2, 17.5, 1, 1),
            'Num4': (3, 15.5, 1, 1), 'Num5': (3, 16.5, 1, 1), 'Num6': (3, 17.5, 1, 1),
            'Num1': (4, 15.5, 1, 1), 'Num2': (4, 16.5, 1, 1), 'Num3': (4, 17.5, 1, 1),
            'Num0': (5, 15.5, 2, 1), 'NumDot': (5, 17.5, 1, 1),
        }
        # Define special key mappings
        special_keys = {
            'LShift': ['shift_l'],
            'RShift': ['shift_l'],
            'LCtrl': ['ctrl_l'],
            'RCtrl': [ 'ctrl_r'],
            'LAlt': ['alt_l'],
            'RAlt': ['alt_r'],
            'LWin': ['cmd'],
            'RWin': ['cmd_r']
        }
        # 创建高分辨率网格用于热图
        grid_size = 50
        heatmap_data = np.zeros((6*grid_size, 19*grid_size))

        # 填充热图数据
        for key, (row, col, width, height) in keyboard_layout.items():
            if key in special_keys:
                # 处理特殊键
                count = sum(key_counts.get(special_key, 0) for special_key in special_keys[key])
            else:
                # 常规键处理
                count = key_counts.get(key.lower(), 0)
            
            r_start, r_end = int(row*grid_size), int((row+height)*grid_size)
            c_start, c_end = int(col*grid_size), int((col+width)*grid_size)
            heatmap_data[r_start:r_end, c_start:c_end] = count

        # 绘制热图
        im = self.heatmap_plot.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
        self.heatmap_figure.colorbar(im)

        # 添加键盘标签
        for key, (row, col, width, height) in keyboard_layout.items():
            self.heatmap_plot.text(col*grid_size + width*grid_size/2, row*grid_size + height*grid_size/2, 
                                key, ha='center', va='center', fontsize=6)

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