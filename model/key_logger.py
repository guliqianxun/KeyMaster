from pynput import keyboard
from datetime import datetime
from collections import deque

class KeyLogger:
    def __init__(self, config):
        self.config = config
        self.keys = deque(maxlen=self.config.buffer_size)
        self.current_keys = set()
        self.listener = None

    def start_logging(self):
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()

    def _on_press(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        
        self.current_keys.add(key_char)
        
        timestamp = datetime.now()
        key_combination = '+'.join(sorted(self.current_keys))
        self.keys.append({'time': timestamp, 'key': key_combination})

    def _on_release(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        
        if key_char in self.current_keys:
            self.current_keys.remove(key_char)

    def get_data(self):
        return list(self.keys)

    def clear_data(self):
        self.keys.clear()