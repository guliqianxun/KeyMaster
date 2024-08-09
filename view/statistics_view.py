import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import matplotlib.patches as patches

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
        self.sponser_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.heatmap_frame, text='Keyboard Heatmap')
        self.notebook.add(self.key_freq_frame, text='Key Frequency')
        self.notebook.add(self.hourly_dist_frame, text='Hourly Distribution')
        self.notebook.add(self.summary_frame, text='Summary')
        self.notebook.add(self.sponser_frame, text='赞助')

        self.create_keyboard_heatmap()
        self.create_key_freq_chart()
        self.create_hourly_dist_chart()
        self.create_summary()
        self.create_sponser()

    def create_keyboard_heatmap(self):
        self.heatmap_figure = Figure(figsize=(15, 6), dpi=100)
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
    def create_sponser(self):
        sponser_text = """
            如果你喜欢这个项目，可以通过以下方式支持我：
            - 给项目点个 star https://github.com/guliqianxun/KeyMaster
            - 分享给你的朋友
            - 赞助我一杯咖啡 ☕️
        """
        sponser_label = tk.Label(self.sponser_frame, text=sponser_text, font=("Arial", 12), justify=tk.LEFT)
        sponser_label.pack(expand=True, fill='both')
        # 添加赞助二维码图片
        sponser_image = Image.open(self.controller.config.sponser_path)
        sponser_image = sponser_image.resize((250, 400))
        sponser_photo = ImageTk.PhotoImage(sponser_image)
        sponser_label = tk.Label(self.sponser_frame, image=sponser_photo)
        sponser_label.image = sponser_photo
        sponser_label.pack(expand=True, fill='both')

    def update_charts(self, stats):
        if not self.winfo_exists():
            return
        self.update_keyboard_heatmap(stats['key_release_counts'])
        self.update_key_freq_chart(stats['key_counts'])
        self.update_hourly_dist_chart(stats['hourly_counts'])
        self.update_summary(stats)
    
    def update_keyboard_heatmap(self, key_counts):
        self.heatmap_plot.clear()
        
        # Define the keyboard layout data
        keyboard_data = [
            ["Esc",{"x":1},"F1","F2","F3","F4",{"x":0.5},"F5","F6","F7","F8",{"x":0.5},"F9","F10","F11","F12",{"x":0.25},"PrtSc","ScrLk","Pause"],
            [{"y":0.5},"~\n`","!\n1","@\n2","#\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","_\n-","+\n=",{"w":2},"Backspace",{"x":0.25},"Insert","Home","PgUp",{"x":0.25},"Num","/","*","-"],
            [{"w":1.5},"Tab","Q","W","E","R","T","Y","U","I","O","P","{\n[","}\n]",{"w":1.5},"|\n\\",{"x":0.25},"Delete","End","PgDn",{"x":0.25},"7\nHome","8\n↑","9\nPgUp",{"h":2},"+"],
            [{"w":1.75},"Caps","A","S","D","F","G","H","J","K","L",":\n;","\"\n'",{"w":2.25},"Enter",{"x":3.5},"4\n←","5","6\n→"],
            [{"w":2.25},"Shift","Z","X","C","V","B","N","M","<\n,",">\n.","?\n/",{"w":2.75},"Shift",{"x":1.25},"↑",{"x":1.25},"1\nEnd","2\n↓","3\nPgDn",{"h":2},"Enter"],
            [{"w":1.25},"Ctrl",{"w":1.25},"Win",{"w":1.25},"Alt",{"w":6.25},"",{"w":1.25},"Alt",{"w":1.25},"Win",{"w":1.25},"Menu",{"w":1.25},"Ctrl",{"x":0.25},"←","↓","→",{"x":0.25,"w":2},"0\nIns",".\nDel"]
        ]

        def draw_key(x, y, width, height, text, count):
            if key_counts:
                max_count = max(key_counts.values())
                min_count = min(value for value in key_counts.values() if value > 0)
                if count > 0:
                    log_normalized = (np.log(count) - np.log(min_count)) / (np.log(max_count) - np.log(min_count))
                else:
                    log_normalized = 0
                color = plt.cm.YlOrRd(log_normalized)
            else:
                color = plt.cm.YlOrRd(0)
            
            # Draw shadow
            self.heatmap_plot.add_patch(patches.Rectangle((x+0.05, y-0.05), width, height, facecolor='darkgray', edgecolor='none', zorder=1))
            
            # Draw key background
            self.heatmap_plot.add_patch(patches.Rectangle((x, y), width, height, facecolor=color, edgecolor='black', linewidth=1, zorder=2))
            
            # Draw key top (slightly smaller to create a 3D effect)
            self.heatmap_plot.add_patch(patches.Rectangle((x+0.05, y+0.05), width-0.1, height-0.1, facecolor=color, edgecolor='black', linewidth=0.5, zorder=3))
            
            # Add text
            lines = text.split("\n")
            for i, line in enumerate(lines):
                self.heatmap_plot.text(x + width/2, y + (i+1)/(len(lines)+1) * height, line, ha='center', va='center', fontdict={'size': 8}, color='black', zorder=4)

        y_offset = 0
        for row in keyboard_data:
            x_offset = 0
            width, height = 1, 1
            for item in row:
                if isinstance(item, dict):
                    if 'x' in item:
                        x_offset += float(item['x'])
                    if 'y' in item:
                        y_offset += float(item['y'])
                    if 'w' in item:
                        width = float(item['w'])
                    if 'h' in item:
                        height = float(item['h'])
                    continue
                if isinstance(item, str):
                    key_name = item.split("\n")[-1].lower()
                    count = key_counts.get(key_name, 0)
                    draw_key(x_offset, y_offset, width, height, item, count)
                x_offset += width
                width, height = 1, 1
            y_offset += 1

        self.heatmap_plot.set_xlim(0, 23)
        self.heatmap_plot.set_ylim(0, 6.6)
        self.heatmap_plot.invert_yaxis()
        self.heatmap_plot.set_aspect('equal')
        self.heatmap_plot.axis('off')
        self.heatmap_plot.set_title("Keyboard Heatmap")
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