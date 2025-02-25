from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QColorDialog, QVBoxLayout, QWidget
import sys
from lib.g203_led import G203LEDController
from gui.widgets.settings_form import SettingsForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cli = G203LEDController()
        self.setWindowTitle("LED Control")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        settingsForm = SettingsForm()
        self.setCentralWidget(settingsForm)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())