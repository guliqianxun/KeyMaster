import pystray
import threading
from PIL import Image

class BackgroundController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.config = app_controller.config
        self.key_logger = app_controller.key_logger
        self.data_storage = app_controller.data_storage
        self.running = True
        self.save_event = app_controller.save_event
        self.auto_save_thread = None
        self.tray_icon = None

    def start(self):
        self.key_logger.start_logging()
        self.start_auto_save()
        self.create_tray_icon()

    def stop(self):
        self.running = False
        self.save_event.set()
        self.key_logger.stop_logging()
        if self.tray_icon:
            self.tray_icon.stop()
        if self.auto_save_thread:
            self.auto_save_thread.join(timeout=2)

    def start_auto_save(self):
        def auto_save():
            while self.running:
                self.save_event.wait(self.config.save_interval)
                if self.running:
                    self.app_controller.save_data()
                self.save_event.clear()

        self.auto_save_thread = threading.Thread(target=auto_save)
        self.auto_save_thread.daemon = True
        self.auto_save_thread.start()

    def trigger_save(self):
        self.save_event.set()

    def create_tray_icon(self):
        image = self.create_tray_image()
        menu = pystray.Menu(
            pystray.MenuItem("显示", self.app_controller.show_window,default=True),
            pystray.MenuItem("退出", self.app_controller.quit_app)
        )
        self.tray_icon = pystray.Icon(f"{self.config.title}", image, f"{self.config.title}", menu)
        self.tray_icon.on_click = self.on_tray_click
        threading.Thread(target=self.tray_icon.run, daemon=True).start() 

    def on_tray_click(self, icon, button):
        if button == pystray.MouseButton.LEFT:
            self.app_controller.show_window()

    def create_tray_image(self):
        #read ico from file
        image = Image.open(self.config.icon_path)
        return image