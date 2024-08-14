from collections import Counter
from datetime import datetime, timedelta

class StatsAnalyzer:
    def analyze_data(self, data):
        if not data:
            return {}

        key_counts = Counter()
        key_release_counts = Counter()
        hourly_counts = {i: 0 for i in range(24)}
        
        start_time = datetime.strptime(str(data[0]['time']), "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(str(data[-1]['time']), "%Y-%m-%d %H:%M:%S")
        
        for event in data:
            time = datetime.strptime(str(event['time']), "%Y-%m-%d %H:%M:%S")
            action = event['action']
            key = event['key']
            key = key.lower()

            if action in ['press', 'hotkey']:
                if action == 'hotkey':
                    key_counts[key] += 1
                else:
                    key_counts[key] += 1
            if action == 'release':
                key_release_counts[key] += 1
                hourly_counts[time.hour] += 1

        total_duration = end_time - start_time
        total_keystrokes = sum(key_counts.values())
        print(dict(key_release_counts))

        return {
            'key_counts': dict(key_counts),
            'key_release_counts': dict(key_release_counts),
            'hourly_counts': hourly_counts,
            'total_duration': total_duration,
            'total_keystrokes': total_keystrokes,
            'keystrokes_per_minute': (total_keystrokes / total_duration.total_seconds()) * 60 if total_duration.total_seconds() > 0 else 0,
            'start_time': start_time,
            'end_time': end_time
        }

    def get_daily_summary(self, data):
        daily_summary = {}
        for event in data:
            time = datetime.strptime(str(event['time']), "%Y-%m-%d %H:%M:%S")
            date = time.date()
            action = event['action']
            key = event['key']

            if date not in daily_summary:
                daily_summary[date] = {'count': 0, 'keys': Counter()}
            
            if action in ['press', 'hotkey']:
                daily_summary[date]['count'] += 1
                daily_summary[date]['keys'][key] += 1
        
        return daily_summary