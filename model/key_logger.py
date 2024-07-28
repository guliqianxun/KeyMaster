from pynput import keyboard
from collections import deque
from datetime import datetime

class KeyLogger:
    def __init__(self, config, trigger_save):
        self.config = config
        self.keys = deque(maxlen=self.config.buffer_size)
        self.trigger_save = trigger_save
        self.pressed_keys = set()  # 用于跟踪所有当前按下的键
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
        # 检查这个键是否已经被按下
        key_str = self._key_to_string(key)
        if key_str in self.pressed_keys:
            return  # 如果已经按下，不进行重复记录
        
        self.pressed_keys.add(key_str)
        
        # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # key_combination = self._get_key_combination(key)
        # self.keys.append({'time': timestamp, 'key': key_combination, 'action': 'press'})
        
        # if len(self.keys) >= self.keys.maxlen:
        #     self.trigger_save()

    def _on_release(self, key):
        key_str = self._key_to_string(key)
        if key_str in self.pressed_keys:
            self.pressed_keys.remove(key_str)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            key_combination = self._get_key_combination(key)
            self.keys.append({'time': timestamp, 'key': key_combination, 'action': 'release'})
            
            if len(self.keys) >= self.keys.maxlen:
                self.trigger_save()

    def _key_to_string(self, key):
        if isinstance(key, int):
            # 直接处理整数键码
            return self._vk_to_string(key)
        elif hasattr(key, 'vk'):
            # 处理带有 vk 属性的对象
            return self._vk_to_string(key.vk)
        elif isinstance(key, str):
            # 处理普通字符串
            return key
        else:
            # 处理其他类型的键对象
            try:
                return key.char
            except AttributeError:
                return str(key)
    def _vk_to_string(self, vk):
        if 65 <= vk <= 90:  # A-Z
            return chr(vk)
        elif 48 <= vk <= 57:  # 0-9
            return chr(vk)
        else:
            # 扩展的特殊键映射
            special_keys = {
                0x01: 'Ctrl',
                0x02: 'Alt',
                0x03: 'Break',
                0x08: 'Backspace',
                0x09: 'Tab',
                0x0C: 'Clear',
                0x0D: 'Enter',
                0x10: 'Shift',
                0x11: 'Ctrl',
                0x12: 'Alt',
                0x13: 'Pause',
                0x14: 'Caps Lock',
                0x1B: 'Esc',
                0x20: 'Space',
                0x21: 'Page Up',
                0x22: 'Page Down',
                0x23: 'End',
                0x24: 'Home',
                0x25: 'Left',
                0x26: 'Up',
                0x27: 'Right',
                0x28: 'Down',
                0x2C: 'Print Screen',
                0x2D: 'Insert',
                0x2E: 'Delete',
                0x2F: 'Help',
                0x5B: 'Left Windows',
                0x5C: 'Right Windows',
                0x5D: 'Applications',
                0x5F: 'Sleep',
                0x60: 'Numpad 0',
                0x61: 'Numpad 1',
                0x62: 'Numpad 2',
                0x63: 'Numpad 3',
                0x64: 'Numpad 4',
                0x65: 'Numpad 5',
                0x66: 'Numpad 6',
                0x67: 'Numpad 7',
                0x68: 'Numpad 8',
                0x69: 'Numpad 9',
                0x6A: 'Numpad *',
                0x6B: 'Numpad +',
                0x6C: 'Numpad Separator',
                0x6D: 'Numpad -',
                0x6E: 'Numpad .',
                0x6F: 'Numpad /',
                0x70: 'F1',
                0x71: 'F2',
                0x72: 'F3',
                0x73: 'F4',
                0x74: 'F5',
                0x75: 'F6',
                0x76: 'F7',
                0x77: 'F8',
                0x78: 'F9',
                0x79: 'F10',
                0x7A: 'F11',
                0x7B: 'F12',
                0x7C: 'F13',
                0x7D: 'F14',
                0x7E: 'F15',
                0x7F: 'F16',
                0x80: 'F17',
                0x81: 'F18',
                0x82: 'F19',
                0x83: 'F20',
                0x84: 'F21',
                0x85: 'F22',
                0x86: 'F23',
                0x87: 'F24',
                0x90: 'Num Lock',
                0x91: 'Scroll Lock',
                0xA0: 'Left Shift',
                0xA1: 'Right Shift',
                0xA2: 'Left Ctrl',
                0xA3: 'Right Ctrl',
                0xA4: 'Left Alt',
                0xA5: 'Right Alt',
                0xA6: 'Browser Back',
                0xA7: 'Browser Forward',
                0xA8: 'Browser Refresh',
                0xA9: 'Browser Stop',
                0xAA: 'Browser Search',
                0xAB: 'Browser Favorites',
                0xAC: 'Browser Home',
                0xAD: 'Volume Mute',
                0xAE: 'Volume Down',
                0xAF: 'Volume Up',
                0xB0: 'Next Track',
                0xB1: 'Previous Track',
                0xB2: 'Stop Media',
                0xB3: 'Play/Pause Media',
                0xB4: 'Start Mail',
                0xB5: 'Select Media',
                0xB6: 'Start Application 1',
                0xB7: 'Start Application 2',
                0xBA: ';',
                0xBB: '+',
                0xBC: ',',
                0xBD: '-',
                0xBE: '.',
                0xBF: '/',
                0xC0: '`',
                0xDB: '[',
                0xDC: '\\',
                0xDD: ']',
                0xDE: "'",
            }
            return special_keys.get(vk, f'Key.{hex(vk)}')

    def _get_key_combination(self, new_key):
        # 转换所有按下的键和新键
        all_keys = [self._key_to_string(k) for k in self.pressed_keys] + [self._key_to_string(new_key)]
        # 去重并排序
        unique_keys = sorted(set(all_keys))
        return '+'.join(unique_keys)
    
    def get_data(self):
        return list(self.keys)

    def clear_data(self):
        self.keys.clear()