from PySide6.QtWidgets import QSlider, QLabel, QPushButton, QComboBox, QColorDialog, QVBoxLayout, QFormLayout, QWidget
from PySide6.QtCore import Qt
from controllers.g203_led import G203LEDController
from gui.widgets.color_button import ColorButton

styles = """
#applyButton {
  padding: 8px;
}
"""

class SettingsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = G203LEDController()
        self.setStyleSheet(styles)
        self.setup()

    def setup(self):
        # QWidget to contain the form layout
        self.formContainer = QWidget()
        self.formContainer.setObjectName("formContainer")

        # Form layout inside the container
        self.formLayout = QFormLayout(self.formContainer)
        self.formLayout.setVerticalSpacing(16)

        
        # Effect combobox
        self.effectComboBox = QComboBox()
        self.effectComboBox.addItems(["Off", "Fixed", "Color wave", "Breathing"])
        self.effectComboBox.currentTextChanged.connect(self.on_effect_text_changed)
        self.formLayout.addRow(self.tr("&Effect:"), self.effectComboBox)

        # Color Button
        self.colorButton = ColorButton(color="#00AAE0")
        self.formLayout.addRow(self.tr("&Color:"), self.colorButton)
        
        # Rate Slider
        self.rateSlider = QSlider(Qt.Horizontal)
        self.rateSlider.setMinimum(1000)
        self.rateSlider.setMaximum(60000)
        self.rateSlider.setValue(3000)
        self.formLayout.addRow(self.tr("&Rate:"), self.rateSlider)
        
        # Brightness Slider
        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setMinimum(1)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setValue(100)
        self.formLayout.addRow(self.tr("&Brightness:"), self.brightnessSlider)

        # Apply Button
        self.applyButton = QPushButton("Apply")
        self.applyButton.setObjectName("applyButton")
        self.applyButton.clicked.connect(self.on_apply_clicked)
        self.formLayout.addRow(self.applyButton)

        # Form
        self.hide_form_elements()
        
        # Set main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.formContainer)
        self.setLayout(mainLayout)

        
    def hide_form_elements(self):
        self.formLayout.setRowVisible(self.colorButton, False)
        self.formLayout.setRowVisible(self.rateSlider, False)
        self.formLayout.setRowVisible(self.brightnessSlider, False)

    def on_effect_text_changed(self, text):
        self.hide_form_elements()
        match text:
            case "Fixed": self.formLayout.setRowVisible(self.colorButton, True)
            case "Off": pass
            case "Breathing":
                self.formLayout.setRowVisible(self.colorButton, True)
                self.formLayout.setRowVisible(self.rateSlider, True)
                self.formLayout.setRowVisible(self.brightnessSlider, True)
            case "Color wave":
                self.formLayout.setRowVisible(self.rateSlider, True)
                self.formLayout.setRowVisible(self.brightnessSlider, True)

    def on_apply_clicked(self):
        effect = self.effectComboBox.currentText()
        effects = {
            "Off": self.set_off,
            "Fixed": self.set_fixed_color,
            "Color wave": self.set_color_wave,
            "Breathing": self.set_breathing
        }
        effects.get(effect)()

    def set_off(self):
        self.controller.set_ls_solid(self.controller.process_color('#000000'))
        pass

    def set_fixed_color(self):
        color = self.colorButton.color()
        self.controller.set_ls_solid(self.controller.process_color(color))

    def set_color_wave(self):
        rate = self.rateSlider.value()
        brightness = self.brightnessSlider.value()
        self.controller.set_ls_wave(
            self.controller.process_rate(rate),
            self.controller.process_brightness(brightness),
            self.controller.process_direction("right")
        )

    def set_breathing(self):
        color = self.colorButton.color()
        rate = self.rateSlider.value()
        brightness = self.brightnessSlider.value()
        self.controller.set_ls_breathe(
            self.controller.process_color(color),
            self.controller.process_rate(rate),
            self.controller.process_brightness(brightness),
        )