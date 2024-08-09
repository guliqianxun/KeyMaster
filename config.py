import os

from utils.run_path import resource_path
class Config:
    def __init__(self):
        self.title = "KeyMaster v0.36"
        self.csv_folder = "key_logs"
        self.icon_path = resource_path("Resources/keyboard.ico")
        self.sponser_path = resource_path("Resources/支付宝收款码.jpg")
        self.buffer_size = 50
        self.save_interval = 60
        
        if not os.path.exists(self.csv_folder):
            os.makedirs(self.csv_folder)