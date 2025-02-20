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
        #store data in year/month/log.csv
        year = current_date.split("-")[0]
        month = current_date.split("-")[1]
        #create folder if not exist
        if not os.path.exists(os.path.join(self.config.csv_folder, year, month)):
            os.makedirs(os.path.join(self.config.csv_folder, year, month))
        csv_file = os.path.join(self.config.csv_folder, f"{year}/{month}/key_log_{current_date}.csv")
        
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['time', 'key', 'action'])
            if not file_exists:
                writer.writeheader()
            for key_event in data:
                writer.writerow({
                    'time' :datetime.strptime(key_event['time'], "%Y-%m-%d %H:%M:%S"),
                    'key': key_event['key'],
                    'action': key_event['action']
                })
    def get_available_dates(self):
        """Get list of available dates from existing CSV files"""
        dates = []
        try:
            # Only scan existing directories
            for year_dir in sorted(os.listdir(self.config.csv_folder)):
                year_path = os.path.join(self.config.csv_folder, year_dir)
                if not os.path.isdir(year_path):
                    continue
                    
                for month_dir in sorted(os.listdir(year_path)):
                    month_path = os.path.join(year_path, month_dir)
                    if not os.path.isdir(month_path):
                        continue
                        
                    # Only look for existing key_log files
                    for file in os.listdir(month_path):
                        if file.startswith('key_log_') and file.endswith('.csv'):
                            date = file.replace('key_log_', '').replace('.csv', '')
                            try:
                                # Verify it's a valid date
                                datetime.strptime(date, "%Y-%m-%d")
                                dates.append(date)
                            except ValueError:
                                continue
        except Exception as e:
            print(f"Error scanning for dates: {e}")
            
        return sorted(dates, reverse=True)  # Most recent dates first

    def load_data(self, date=None):
        """Load data from CSV file for specific date, returns list of dictionaries"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            year, month = date.split("-")[:2]
            csv_file = os.path.join(self.config.csv_folder, year, month, f"key_log_{date}.csv")
            
            if not os.path.isfile(csv_file):
                return []

            with open(csv_file, 'r') as file:
                return [
                    {
                        'time': datetime.strptime(str(row['time']), "%Y-%m-%d %H:%M:%S"),
                        'key': row['key'],
                        'action': row['action']
                    }
                    for row in csv.DictReader(file)
                ]
                
        except Exception as e:
            print(f"Error loading data for date {date}: {e}")
            return []