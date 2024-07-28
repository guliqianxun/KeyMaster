import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import font_manager

import matplotlib
import platform
plt.rcParams['font.family'] = 'SimHei'
class StatisticsView(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("KeyMaster 统计")
        self.geometry("800x600")
        self.set_global_font()
        self.create_widgets()

    def set_global_font(self):
        # 根据操作系统选择合适的字体
        if platform.system() == 'Windows':
            font_name = 'Microsoft YaHei'
        elif platform.system() == 'Darwin':  # macOS
            font_name = 'Arial Unicode MS'
        else:  # Linux and others
            font_name = 'DejaVu Sans'

        # 设置matplotlib的全局字体
        matplotlib.rc('font', family=font_name)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.key_freq_frame = ttk.Frame(self.notebook)
        self.hourly_dist_frame = ttk.Frame(self.notebook)
        self.summary_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.key_freq_frame, text='按键频率')
        self.notebook.add(self.hourly_dist_frame, text='每小时分布')
        self.notebook.add(self.summary_frame, text='摘要')

        self.create_key_freq_chart()
        self.create_hourly_dist_chart()
        self.create_summary()

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
        self.update_key_freq_chart(stats['key_counts'])
        self.update_hourly_dist_chart(stats['hourly_counts'])
        self.update_summary(stats)

    def update_key_freq_chart(self, key_counts):
        self.key_freq_plot.clear()
        keys = list(key_counts.keys())
        counts = list(key_counts.values())
        
        # 处理特殊按键名称
        keys = [self.format_key_name(key) for key in keys]
        
        self.key_freq_plot.bar(keys, counts)
        self.key_freq_plot.set_title("按键频率")
        self.key_freq_plot.set_xlabel("按键")
        self.key_freq_plot.set_ylabel("频率")
        plt.setp(self.key_freq_plot.get_xticklabels(), rotation=45, ha='right')
        self.key_freq_figure.tight_layout()
        self.key_freq_canvas.draw()
    
    def format_key_name(self, key):
        # 处理特殊按键名称
        special_keys = {
            'Key.space': '空格',
            'Key.enter': '回车',
            'Key.backspace': '退格',
            'Key.shift': 'Shift',
            'Key.ctrl': 'Ctrl',
            'Key.alt': 'Alt',
            # 添加更多特殊按键的映射
        }
        return special_keys.get(key, key)

    def update_hourly_dist_chart(self, hourly_counts):
        self.hourly_dist_plot.clear()
        hours = list(hourly_counts.keys())
        counts = list(hourly_counts.values())
        self.hourly_dist_plot.bar(hours, counts)
        self.hourly_dist_plot.set_title("每小时按键分布")
        self.hourly_dist_plot.set_xlabel("小时")
        self.hourly_dist_plot.set_ylabel("按键次数")
        self.hourly_dist_figure.tight_layout()
        self.hourly_dist_canvas.draw()

    def update_summary(self, stats):
        summary = f"""
            总按键次数: {stats['total_keystrokes']}
            记录开始时间: {stats['start_time']}
            记录结束时间: {stats['end_time']}
            总时长: {stats['total_duration']}
            每分钟按键次数: {stats['keystrokes_per_minute']:.2f}
        """
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)