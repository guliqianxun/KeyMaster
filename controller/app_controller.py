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
        self.key_logger = KeyLogger(self.config)
        self.data_storage = DataStorage(self.config)
        self.stats_analyzer = StatsAnalyzer()
        self.main_window = None
        self.stats_view = None
        self.auto_save_thread = None
        self.running = True

    def run(self):
        self.main_window = MainWindow(self)
        self.key_logger.start_logging()
        self.start_auto_save()
        self.main_window.mainloop()

    def start_auto_save(self):
        def auto_save():
            while self.running:
                time.sleep(self.config.save_interval)
                if self.running:
                    self.save_data()

        self.auto_save_thread = threading.Thread(target=auto_save)
        self.auto_save_thread.start()

    def save_data(self):
        data = self.key_logger.get_data()
        self.data_storage.save_data(data)
        self.key_logger.clear_data()
        if self.main_window:
            self.main_window.update_status("数据已保存")

    def show_statistics(self):
        if not self.stats_view:
            self.stats_view = StatisticsView(self.main_window, self)
        
        data = self.data_storage.load_data()
        stats = self.stats_analyzer.analyze_data(data)
        self.stats_view.update_charts(stats)
        self.stats_view.deiconify()  # 如果窗口被最小化，重新显示

    def stop_logging(self):
        self.running = False
        self.key_logger.stop_logging()
        self.save_data()  # 保存最后的数据
        if self.auto_save_thread:
            self.auto_save_thread.join()
        if self.stats_view:
            self.stats_view.destroy()