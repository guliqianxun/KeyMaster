import sys
import os

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    try:
        # 如果是 PyInstaller 打包的临时运行文件夹
        base_path = sys._MEIPASS
    except AttributeError:
        # 否则以主文件（入口文件）的目录为基准
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    return os.path.join(base_path, relative_path)
