import tkinter as tk
from tkinter import ttk
import datetime
from PIL import Image, ImageTk

class WorkIdleGame:
    def __init__(self, root):
        # Initialize window
        self.root = root
        self.root.title("下班倒计时与工资增长")
        self.root.geometry("400x400")  # Increased height to accommodate GIF

        # Create canvas for gradient background
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack(fill="both", expand=True)

        # Gradient background colors
        self.create_gradient_background(self.canvas, "lightblue", "lightpink")

        # Set font styles
        self.large_font = ("Helvetica", 24, "bold")
        self.medium_font = ("Helvetica", 16)
        self.small_font = ("Helvetica", 12)

        # Set work times
        self.work_start_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.work_end_time = datetime.datetime.now().replace(hour=0, minute=40, second=0, microsecond=0)

        # Set salary
        self.monthly_salary = 20000
        self.daily_salary = self.monthly_salary / 21.75

        # Initialize work progress and salary growth variables
        self.salary_earned = 0
        self.work_progress = 0

        # Countdown label
        self.time_label = tk.Label(self.canvas, text="已下班，距离下次上班还有", font=self.small_font, bg="#D8BFD8")
        self.time_label.place(x=50, y=50)

        # Work progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", thickness=30, troughcolor="white", background="green")
        self.work_progress_bar = ttk.Progressbar(self.canvas, orient="horizontal", length=300, mode='determinate', style="TProgressbar")
        self.work_progress_bar.place(x=50, y=100)

        # Salary progress bar
        self.salary_progress_bar = ttk.Progressbar(self.canvas, orient="horizontal", length=300, mode='determinate', style="TProgressbar")
        self.salary_progress_bar.place(x=50, y=150)

        # Current salary label
        self.salary_label = tk.Label(self.canvas, text=f"当前工资: {self.salary_earned:.2f} 元", font=self.medium_font, bg="#D8BFD8")
        self.salary_label.place(x=50, y=200)

        # GIF display
        self.gif_label = tk.Label(self.canvas)
        self.gif_label.place(x=50, y=250)

        # Load GIFs
        self.load_gifs()

        # Start update loop
        self.update()


    def create_gradient_background(self, canvas, color1, color2):
        # 创建渐变背景
        steps = 100
        r1, g1, b1 = self.canvas.winfo_rgb(color1)
        r2, g2, b2 = self.canvas.winfo_rgb(color2)

        r_ratio = (r2 - r1) / steps
        g_ratio = (g2 - g1) / steps
        b_ratio = (b2 - b1) / steps

        for i in range(steps):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))

            color = f'#{nr:04x}{ng:04x}{nb:04x}'
            canvas.create_line(0, i * 3, 400, i * 3, fill=color)
    def load_gifs(self):
        self.gifs = {
            "sleeping": self.load_gif("间谍过家家-打瞌睡.gif"),
            "excited": self.load_gif("间谍过家家-期待.gif"),
            "leaving": self.load_gif("间谍过家家.gif")
        }

    def load_gif(self, filename):
        gif = Image.open(f"assets/{filename}")
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames

    def update_gif(self, gif_name):
        if not hasattr(self, 'gif_index'):
            self.gif_index = 0
        self.gif_index += 1
        if self.gif_index >= len(self.gifs[gif_name]):
            self.gif_index = 0
        self.gif_label.configure(image=self.gifs[gif_name][self.gif_index])

    def update(self):
        now = datetime.datetime.now()

        if now < self.work_start_time:
            # Before work
            time_left = self.work_start_time - now
            self.time_label.config(text=f"未上班，距离上班还有: {time_left}")
            self.work_progress_bar['value'] = 0
            self.salary_progress_bar['value'] = 0
            self.gif_label.configure(image='')  # No GIF shown
        elif self.work_start_time <= now <= self.work_end_time:
            # During work
            total_work_seconds = (self.work_end_time - self.work_start_time).total_seconds()
            work_elapsed_seconds = (now - self.work_start_time).total_seconds()
            self.work_progress = work_elapsed_seconds / total_work_seconds * 100
            self.work_progress_bar['value'] = self.work_progress

            # Update salary
            seconds_per_day = total_work_seconds
            salary_per_second = self.daily_salary / seconds_per_day
            self.salary_earned = work_elapsed_seconds * salary_per_second
            self.salary_progress_bar['value'] = (self.salary_earned / self.daily_salary) * 100
            self.salary_label.config(text=f"当前工资: {self.salary_earned:.2f} 元")

            # Update countdown
            time_left = self.work_end_time - now
            self.time_label.config(text=f"距离下班还有: {time_left}")

            # Update GIF
            if time_left <= datetime.timedelta(minutes=5):
                self.update_gif("excited")
            elif time_left <= datetime.timedelta(minutes=1):
                self.update_gif("leaving")
            else:
                self.update_gif("sleeping")
        else:
            # After work
            time_left = datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1) - now
            self.time_label.config(text=f"已下班，距离下次上班还有: {time_left}")
            self.work_progress_bar['value'] = 100
            self.salary_progress_bar['value'] = 100
            self.gif_label.configure(image='')  # No GIF shown

        # Refresh every second
        self.root.after(1000, self.update)

# Create Tkinter window and start the game
root = tk.Tk()
game = WorkIdleGame(root)
root.mainloop()