import unittest
from unittest.mock import Mock, patch
from pynput.keyboard import Key, KeyCode
import time
import string
from model.key_logger import KeyLogger
from config import Config

class TestKeyLogger(unittest.TestCase):

    def setUp(self):
        self.config = Mock(spec=Config)
        self.config.buffer_size = 1000  # 增大缓冲区以容纳所有测试按键
        self.config.csv_folder = '/test_reports'
        self.trigger_save = Mock()
        self.keylogger = KeyLogger(self.config, self.trigger_save)
        
        self.all_keys = list(string.ascii_lowercase) + list(string.digits) + [
            Key.space, Key.enter, Key.backspace, Key.tab, Key.esc, 
            Key.shift, Key.ctrl, Key.alt, Key.cmd,
            Key.left, Key.right, Key.up, Key.down,
            Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, 
            Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12
        ]

    def simulate_key_press(self, key):
        if isinstance(key, str):
            key = KeyCode.from_char(key)
        self.keylogger._on_press(key)
        self.keylogger._on_release(key)

    @patch('pynput.keyboard.Listener')
    def test_start_logging(self, mock_listener):
        """测试键盘监听器是否正确启动"""
        self.keylogger.start_logging()
        mock_listener.assert_called_once()
        mock_listener.return_value.start.assert_called_once()
        print("Test start logging pass")

    def test_key_storage_count(self):
        """测试按键存储数量是否正确"""
        for key in self.all_keys:
            self.simulate_key_press(key)
        
        expected_count = len(self.all_keys) * 2  # 每个键有按下和释放两个事件
        actual_count = len(self.keylogger.keys)
        self.assertEqual(actual_count, expected_count)
        print(f"Test key store event pass(store buffer), expected count: {expected_count} actual count:{actual_count}")

    def test_key_press_release_pairing(self):
        """测试按键的按下和释放是否正确配对"""
        for key in self.all_keys:
            self.simulate_key_press(key)
        
        for i in range(0, len(self.all_keys) * 2, 2):
            self.assertEqual(self.keylogger.keys[i]['key'], self.keylogger.keys[i + 1]['key'])
            self.assertEqual(self.keylogger.keys[i]['action'], 'press')
            self.assertEqual(self.keylogger.keys[i + 1]['action'], 'release')
        print("key press and release pairing test pass")

    def test_special_keys_logging(self):
        """测试特殊键是否正确记录"""
        special_keys = [Key.space, Key.enter, Key.backspace, Key.tab, Key.esc, 
                        Key.shift, Key.ctrl, Key.alt, Key.cmd]
        for key in special_keys:
            self.simulate_key_press(key)
        
        logged_special_keys = [event['key'] for event in self.keylogger.keys if event['action'] == 'press']
        expected_special_keys = [key.name for key in special_keys]
        self.assertEqual(logged_special_keys, expected_special_keys)
        print('special keys logging test pass')

    def test_alphanumeric_keys_logging(self):
        """测试字母和数字键是否正确记录"""
        alphanumeric_keys = list(string.ascii_lowercase) + list(string.digits)
        for key in alphanumeric_keys:
            self.simulate_key_press(key)
        
        logged_alphanumeric_keys = [event['key'] for event in self.keylogger.keys if event['action'] == 'press']
        self.assertEqual(logged_alphanumeric_keys, alphanumeric_keys)
        print("alphanumeric keys logging test pass")

