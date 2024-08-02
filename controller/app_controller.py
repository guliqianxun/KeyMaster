import threading
import time
from model.key_logger import KeyLogger
from model.data_storage import DataStorage
from model.stats_analyzer import StatsAnalyzer
from view.main_window import MainWindow
from view.statistics_view import StatisticsView
from config import Config
from controller.BackgroundController import BackgroundController

class AppController:
    def __init__(self):
        self.config = Config()
        self.key_logger = KeyLogger(self.config, self.trigger_save)
        self.data_storage = DataStorage(self.config)
        self.stats_analyzer = StatsAnalyzer()
        self.main_window = None
        self.stats_view = None
        self.save_event = threading.Event()
        self.background_controller = BackgroundController(self)

    def run(self):
        self.background_controller.start()
        threading.Thread(target=self.run_tk_mainloop, daemon=True).start()
        while self.background_controller.running:
            time.sleep(0.1)

    def run_tk_mainloop(self):
        if not self.main_window:
            self.main_window = MainWindow(self)
        self.main_window.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.main_window.mainloop()\

    def show_window(self):
        if not self.main_window:
            self.main_window = MainWindow(self)
        self.main_window.deiconify()
        self.main_window.lift()
        self.main_window.focus_force()

    def hide_window(self):
        if self.main_window:
            self.main_window.withdraw()

    def start_auto_save(self):
        def auto_save():
            while self.running:
                self.background_controller.save_event.wait(self.config.save_interval)
                if self.running:
                    self.save_data()
                self.background_controller.save_event.clear()

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
        # Minimize to tray instead of exiting
        self.main_window.withdraw()

    def quit_app(self):
        self.running = False
        self.key_logger.stop_logging()
        
        # Close statistics view if it exists
        if self.stats_view and self.stats_view.winfo_exists():
            self.stats_view.destroy()
        
        # Properly close the main window and stop the application
        if self.main_window:
            self.main_window.destroy()

    def cleanup(self):
        # Save the last bits of data
        self.save_data()
        
        # Wait for the auto-save thread to finish
        if self.auto_save_thread:
            self.auto_save_thread.join(timeout=2)
        
        # Close the statistics view if it exists
        if self.stats_view and self.stats_view.winfo_exists():
            self.stats_view.destroy()

    def show_statistics(self):
        if not self.stats_view or not self.stats_view.winfo_exists():
            self.stats_view = StatisticsView(self.main_window, self)
        
        data = self.data_storage.load_data()
        stats = self.stats_analyzer.analyze_data(data)
        self.stats_view.update_charts(stats)
        self.stats_view.deiconify()
