from pynput import keyboard
from collections import deque
from datetime import datetime
from simple_log_helper import CustomLogger

class KeyLogger:
    def __init__(self, config, trigger_save):
        self.config = config
        self.logger = CustomLogger(__name__,log_filename=f'{self.config.csv_folder}/key_logger.log')
        self.keys = deque(maxlen=self.config.buffer_size)
        self.trigger_save = trigger_save
        self.pressed_keys = set()
        self.listener = None
        self.hotkeys = {
            frozenset(['ctrl_l', 'C']): 'Ctrl+C',
            frozenset(['ctrl_l', 'V']): 'Ctrl+V',
            frozenset(['alt_l', 'f4']): 'Alt+F4',
            frozenset(['ctrl_l', 'shift', 'esc']): 'Ctrl+Shift+Esc',
            frozenset(['ctrl_l', 'S']): 'Ctrl+S',
            frozenset(['ctrl_l', 'A']): 'Ctrl+A',
            frozenset(['cmd', 'D']): 'Win+D',
            frozenset(['cmd', 'R']): 'Win+R',
            frozenset(['cmd', 'E']): 'Win+E',
            frozenset(['ctrl_l', 'F']): 'Ctrl+F',
            frozenset(['ctrl_l', 'Z']): 'Ctrl+Z',
            frozenset(['ctrl_l', 'H']): 'Ctrl+H',
            frozenset(['ctrl_l', 'X']): 'Ctrl+X',
            frozenset(['alt_l', 'tab']): 'Alt+Tab',
            frozenset(['cmd', 'tab']): 'Win+Tab',
            frozenset(['insert','shift']): 'Insert+Shift',
            frozenset(['insert','ctrl_l']): 'Insert+Ctrl',
            frozenset(['enter','shift']): 'Enter+Shift',
            frozenset(['enter','ctrl_l']): 'Enter+Ctrl',
            frozenset(['ctrl_l','/']): 'Ctrl+/',
            frozenset(['ctrl_l','shift','/']): 'Ctrl+Shift+/',
            frozenset(['ctrl_l','shift','N']): 'Ctrl+Shift+N',
            frozenset(['ctrl_l','G']): 'Ctrl+G',
            frozenset(['tab','shift']): 'Tab+Shift',
            frozenset(['ctrl_l','insert']): 'Ctrl+Insert',
            frozenset(['ctrl_l','shift','insert']): 'Ctrl+Shift+Insert',
            frozenset(['shift','insert']): 'Shift+Insert',
        }
    def start_logging(self):
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()

    def _on_press(self, key):
        if key == None:
            return
        key_str = self._key_to_string(key)
        key_str = key_str.replace("Key.", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if key_str not in self.pressed_keys:
            self.pressed_keys.add(key_str)
            hotkey = self._check_hotkey()
            if hotkey:
                self.keys.append({'time': timestamp, 'key': hotkey, 'action': 'hotkey'})
            else:
                self.keys.append({'time': timestamp, 'key': key_str, 'action': 'press'})
            
            if len(self.keys) >= self.keys.maxlen:
                self.trigger_save()

    def _on_release(self, key):
        if key == None:
            return
        key_str = self._key_to_string(key)
        if key_str in self.pressed_keys:
            self.pressed_keys.remove(key_str)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.keys.append({'time': timestamp, 'key': key_str, 'action': 'release'})
        
        if len(self.keys) >= self.keys.maxlen:
            self.trigger_save()

    def _key_to_string(self, key):
        try:
            if hasattr(key, 'name') and key.name:#default key is Enum
                return str(key.name).replace("Key.", "")
            elif hasattr(key, 'vk') and key.vk:#special key
                return self._vk_to_string(key.vk)
            else:
                return str(key)
        except AttributeError:
            return str(key)
            
        
    def _vk_to_string(self, vk):
        if 65 <= vk <= 90:  # A-Z
            return chr(vk)
        elif 48 <= vk <= 57:  # 0-9
            return chr(vk)
        else:
            # Extended special key mapping
            special_keys = {
                0x01: 'Left Mouse',
                0x02: 'Right Mouse',
                0x03: 'Control-break processing',
                0x04: 'Middle Mouse',
                0x05: 'X1 Mouse',
                0x06: 'X2 Mouse',
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
                0x25: 'Left Arrow',
                0x26: 'Up Arrow',
                0x27: 'Right Arrow',
                0x28: 'Down Arrow',
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
                0x6C: 'Separator',
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
                0xBB: '=',
                0xBC: ',',
                0xBD: '-',
                0xBE: '.',
                0xBF: '/',
                0xC0: '`',
                0xDB: '[',
                0xDC: '\\',
                0xDD: ']',
                0xDE: "'",
                0xDF: 'Office Home',
                0xE0: 'Media Select',
            }
            return special_keys.get(vk, f'Unknown ({hex(vk)})')
    
    def _check_hotkey(self):
        current_keys = frozenset(self.pressed_keys)
        if len(current_keys) < 1:
            return
        if len(current_keys) > 1 and current_keys not in self.hotkeys:
            #check if not only contain a~z or 0~9
            for key in current_keys:
                if key in ['shift', 'ctrl_l', 'alt_l', 'cmd']:
                    self.logger.info(f'Hotkey not found: {current_keys}')
                    break
            return None
            
        for hotkey_combo, hotkey_name in self.hotkeys.items():
            if hotkey_combo.issubset(current_keys):
                return hotkey_name
        return None
    
    def get_data(self):
        return list(self.keys)

    def clear_data(self):
        self.keys.clear()