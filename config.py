import os

class Config:
    def __init__(self):
        self.title = "KeyMaster v0.34"
        self.csv_folder = "key_logs"
        self.icon_path = "./Resources/keyboard.ico"
        self.buffer_size = 50
        self.save_interval = 60
        
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)