import csv
import os
from datetime import datetime

class DataStorage:
    def __init__(self, config):
        self.config = config

    def save_data(self, data):
        if not data:
            return

        current_date = datetime.now().strftime("%Y-%m-%d")
        csv_file = os.path.join(self.config.csv_folder, f"key_log_{current_date}.csv")
        
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['time', 'key'])
            if not file_exists:
                writer.writeheader()
            for key_event in data:
                writer.writerow({
                    'time': key_event['time'].strftime("%Y-%m-%d %H:%M:%S"),
                    'key': key_event['key']
                })

    def load_data(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        csv_file = os.path.join(self.config.csv_folder, f"key_log_{date}.csv")
        
        if not os.path.isfile(csv_file):
            return []

        data = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append({
                    'time': datetime.strptime(row['time'], "%Y-%m-%d %H:%M:%S"),
                    'key': row['key']
                })
        
        return data