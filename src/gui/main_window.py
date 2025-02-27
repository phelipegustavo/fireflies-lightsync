import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow
# from PySide6.QtGui import QIcon
from gui.widgets.settings_form import SettingsForm

APP_TITLE = "Fireflies LightSync"
APP_ICON = "fireflies-light-sync-icon.svg"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 400, 300)
        # self.setWindowIcon(QIcon(self.get_icon_path()))
        self.initUI()

    # def get_icon_path(self):
    #     if getattr(sys, 'frozen', False):
    #         return os.path.join(sys._MEIPASS, "icons", APP_ICON)
    #     else:
    #         return os.path.join(os.path.dirname(__file__), "icons", APP_ICON)

    def initUI(self):
        settingsForm = SettingsForm()
        self.setCentralWidget(settingsForm)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())