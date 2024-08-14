import sys
import os

def resource_path(relative_path):
    """ 获取资源绝对路径 """
    try:
        # PyInstaller 创建临时文件夹 sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)