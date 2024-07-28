from collections import Counter
from datetime import datetime, timedelta

class StatsAnalyzer:
    def analyze_data(self, data):
        if not data:
            return {}

        key_counts = Counter()
        hourly_counts = {i: 0 for i in range(24)}
        
        start_time = data[0]['time']
        end_time = data[-1]['time']
        
        for event in data:
            keys = event['key'].split('+')
            key_counts.update(keys)
            hourly_counts[event['time'].hour] += 1

        total_duration = end_time - start_time
        total_keystrokes = sum(key_counts.values())

        return {
            'key_counts': dict(key_counts),
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
            date = event['time'].date()
            if date not in daily_summary:
                daily_summary[date] = {'count': 0, 'keys': Counter()}
            daily_summary[date]['count'] += 1
            daily_summary[date]['keys'].update(event['key'].split('+'))
        
        return daily_summary