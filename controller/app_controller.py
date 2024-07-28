import threading
import time
from model.key_logger import KeyLogger
from model.data_storage import DataStorage
from model.stats_analyzer import StatsAnalyzer
from view.main_window import MainWindow
from view.statistics_view import StatisticsView
from config import Config

class AppController:
    def __init__(self):
        self.config = Config()
        self.key_logger = KeyLogger(self.config, self.trigger_save)
        self.data_storage = DataStorage(self.config)
        self.stats_analyzer = StatsAnalyzer()
        self.main_window = None
        self.stats_view = None
        self.auto_save_thread = None
        self.running = True
        self.save_event = threading.Event()

    def run(self):
        self.main_window = MainWindow(self)
        self.key_logger.start_logging()
        self.start_auto_save()
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_window.mainloop()

    def start_auto_save(self):
        def auto_save():
            while self.running:
                self.save_event.wait(self.config.save_interval)
                if self.running:
                    self.save_data()
                self.save_event.clear()

        self.auto_save_thread = threading.Thread(target=auto_save)
        self.auto_save_thread.daemon = True
        self.auto_save_thread.start()
    def trigger_save(self):
        self.save_event.set()

    def save_data(self):
        data = self.key_logger.get_data()
        if data:
            self.data_storage.save_data(data)
            self.key_logger.clear_data()
            if self.main_window:
                self.main_window.update_status(f"数据已保存 {time.strftime('%H:%M:%S')}")

    def on_closing(self):
        self.running = False
        self.save_event.set()  # 触发最后一次保存
        self.key_logger.stop_logging()
        
        # 使用线程来处理关闭操作，避免UI卡顿
        closing_thread = threading.Thread(target=self.cleanup)
        closing_thread.start()
        
        # 显示正在关闭的消息
        if self.main_window:
            self.main_window.update_status("正在保存数据，请稍候...")
            self.main_window.update()  # 强制更新UI
        
        # 等待清理完成
        closing_thread.join(timeout=5)  # 最多等待5秒
        
        # 关闭主窗口
        if self.main_window:
            self.main_window.destroy()


    def cleanup(self):
        # 保存最后的数据
        self.save_data()
        
        # 等待自动保存线程结束
        if self.auto_save_thread:
            self.auto_save_thread.join(timeout=2)
        
        # 关闭统计视图
        if self.stats_view and self.stats_view.winfo_exists():
            self.stats_view.destroy()

    def show_statistics(self):
        if not self.stats_view or not self.stats_view.winfo_exists():
            self.stats_view = StatisticsView(self.main_window, self)
        
        data = self.data_storage.load_data()
        stats = self.stats_analyzer.analyze_data(data)
        self.stats_view.update_charts(stats)
        self.stats_view.deiconify()

    # def stop_logging(self):
    #     self.running = False
    #     self.key_logger.stop_logging()
    #     self.save_data()  # 保存最后的数据
    #     if self.auto_save_thread:
    #         self.auto_save_thread.join()
    #     if self.stats_view and self.stats_view.winfo_exists():
    #         self.stats_view.destroy()