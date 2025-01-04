import os
import json
from utils.run_path import resource_path

class Config:
    CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".keymaster_config.json")

    def __init__(self):
        self.title = "KeyMaster v0.50"
        self.csv_folder = resource_path("CSV")
        self.log_folder = resource_path("Logs")
        self.icon_path = resource_path("Resources/keyboard.ico")
        self.sponser_path = resource_path("Resources/支付宝收款码.jpg")
        self.buffer_size = 50
        self.save_interval = 60
        self.keyboard_mapping = self.default_keyboard_mapping()
        self.keyboard_layout = self.default_keyboard_layout()

        # 初始化时加载配置文件
        self.load_config()

        # 如果 CSV 文件夹不存在，创建它
        for folder in [self.csv_folder, self.log_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def load_config(self):
        """ 从配置文件加载用户设置 """
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as file:
                    data = json.load(file)
                    self.csv_folder = data.get("csv_folder", self.csv_folder)
                    self.log_folder = data.get("log_folder", self.log_folder)
                    self.buffer_size = data.get("buffer_size", self.buffer_size)
                    self.save_interval = data.get("save_interval", self.save_interval)
            except Exception as e:
                print(f"加载配置失败：{e}")

    def save_config(self):
        """ 保存用户设置到配置文件 """
        data = {
            "csv_folder": self.csv_folder,
            "log_folder": self.log_folder,
            "buffer_size": self.buffer_size,
            "save_interval": self.save_interval,
        }
        try:
            with open(self.CONFIG_FILE, "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"保存配置失败：{e}")

    @staticmethod
    def default_keyboard_mapping():
        # 返回默认键盘映射字典
        return {
        # Function keys
        'esc': 'Esc',
        'f1': 'F1', 'f2': 'F2', 'f3': 'F3', 'f4': 'F4',
        'f5': 'F5', 'f6': 'F6', 'f7': 'F7', 'f8': 'F8',
        'f9': 'F9', 'f10': 'F10', 'f11': 'F11', 'f12': 'F12',
        'print_screen': 'PrtSc', 'scroll_lock': 'ScrLk', 'pause': 'Pause',

        # Number row (both shifted and unshifted)
        '`': '`', '~': '`', '1': '!\n1', '!': '!\n1', '2': '@\n2', '@': '@\n2', '3': '#\n3', '#': '#\n3',
        '4': '$\n4', '$': '$\n4', '5': '%\n5', '%': '%\n5', '6': '^\n6', '^': '^\n6', '7': '&\n7', '&': '&\n7',
        '8': '*\n8', '*': '*\n8', '9': '(\n9', '(': '(\n9', '0': ')\n0', ')': ')\n0', '-': '_\n-', '_': '_\n-',
        '=': '+\n=', '+': '+\n=', 'backspace': 'Backspace',

        # Insert, Home, Page Up
        'insert': 'Insert', 'home': 'Home', 'page_up': 'PgUp',

        # Tab and main letter keys
        'tab': 'Tab',
        'Q': 'Q', 'W': 'W', 'E': 'E', 'R': 'R', 'T': 'T', 'Y': 'Y', 'U': 'U',
        'I': 'I', 'O': 'O', 'P': 'P', '[': '[', '{': '[', ']': ']', '}': ']',
        '\\': '\\', '|': '\\',

        # Caps and main letter keys
        'caps_lock': 'Caps',
        'A': 'A', 'S': 'S', 'D': 'D', 'F': 'F', 'G': 'G', 'H': 'H', 'J': 'J',
        'K': 'K', 'L': 'L', ';': ';', ':': ';', "'": "'", '"': "'",
        'enter': 'Enter',

        # Shift and remaining letter keys
        'shift_l': 'Shift', 'shift_r': 'Shift',
        'Z': 'Z', 'X': 'X', 'C': 'C', 'V': 'V', 'B': 'B', 'N': 'N', 'M': 'M',
        ',': ',', '<': ',', '.': '.', '>': '.', '/': '/', '?': '/',

        # Bottom row
        'ctrl_l': 'Ctrl', 'ctrl_r': 'Ctrl',
        'cmd': 'Win', 'alt_l': 'Alt', 'alt_r': 'Alt',
        'menu': 'Menu', 'space': 'Space',

        # Arrow keys
        'up': '↑', 'down': '↓', 'left': '←', 'right': '→',

        # numpad
        'num_lock': 'Num',
        'numpad /': '/', 'numpad *': '*', 'numpad -': '-', 'numpad +': '+',
        'numpad 7': '7', 'numpad 8': '8', 'numpad 9': '9',
        'numpad 4': '4', 'numpad 5': '5', 'numpad 6': '6',
        'numpad 1': '1', 'numpad 2': '2', 'numpad 3': '3',
        'numpad 0': '0', 'numpad .': '.',

        # Delete, End, Page Down
        'delete': 'Delete', 'end': 'End', 'page_down': 'PgDn',

        # Ensure lowercase letters are also mapped
        'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H',
        'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P',
        'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X',
        'y': 'Y', 'z': 'Z',
        }

    @staticmethod
    def default_keyboard_layout():
        # 返回默认键盘布局
        return [
            ["esc",{"x":1},"f1","f2","f3","f4",{"x":0.5},"f5","f6","f7","f8",{"x":0.5},"f9","f10","f11","f12",{"x":0.25},"print_screen","scroll_lock","pause"],
            [{"y":0.5},"`","1","2","3","4","5","6","7","8","9","0","-","=",{"w":2},"backspace",{"x":0.25},"insert","home","page_up",{"x":0.25},"num_lock","numpad /","numpad *","numpad -"],
            [{"w":1.5},"tab","q","w","e","r","t","y","u","i","o","p","[","]",{"w":1.5},"\\",{"x":0.25},"delete","end","page_down",{"x":0.25},"numpad 7","numpad 8","numpad 9",{"h":2},"numpad +"],
            [{"w":1.75},"caps_lock","a","s","d","f","g","h","j","k","l",";","'",{"w":2.25},"enter",{"x":3.5},"numpad 4","numpad 5","numpad 6"],
            [{"w":2.25},"shift_l","z","x","c","v","b","n","m",",",".","/",{"w":2.75},"shift_r",{"x":1.25},"up",{"x":1.25},"numpad 1","numpad 2","numpad 3",{"h":2},"enter"],
            [{"w":1.25},"ctrl_l",{"w":1.25},"cmd",{"w":1.25},"alt_l",{"w":6.25},"space",{"w":1.25},"alt_r",{"w":1.25},"cmd",{"w":1.25},"menu",{"w":1.25},"ctrl_r",{"x":0.25},"left","down","right",{"x":0.25,"w":2},"numpad 0","numpad ."]
        ]
