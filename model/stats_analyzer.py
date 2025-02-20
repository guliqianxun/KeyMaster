from collections import Counter
from datetime import datetime, timedelta

class StatsAnalyzer:
    def analyze_data(self, data):
        if not data:
            empty_hourly_counts = {i: 0 for i in range(24)}
            return {
                'key_counts': {},
                'key_release_counts': {},
                'hourly_counts': empty_hourly_counts,
                'total_duration': timedelta(0),
                'total_keystrokes': 0,
                'keystrokes_per_minute': 0,
                'start_time': datetime.now(),
                'end_time': datetime.now()
            }

        key_counts = Counter()
        key_release_counts = Counter()
        hourly_counts = {i: 0 for i in range(24)}
        
        # 使用列表的第一个和最后一个元素获取时间范围
        start_time = data[0]['time']
        end_time = data[-1]['time']
        
        for event in data:
            time = event['time']  # 现在直接是 datetime 对象
            action = event['action']
            key = str(event['key']).lower()

            if action in ['press', 'hotkey']:
                key_counts[key] += 1
            if action == 'release':
                key_release_counts[key] += 1
                hourly_counts[time.hour] += 1

        total_duration = end_time - start_time
        total_keystrokes = sum(key_counts.values())

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