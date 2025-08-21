from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

class HomepageView(QWidget):
    go_main = pyqtSignal()
    go_settings = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_buttons()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo = QLabel("ChatShield")
        self.logo.setStyleSheet("font-size: 32px; font-family: Inter; font-weight: 600; color: White; letter-spacing: 0.5px;")

        self.title = QLabel("Homepage")
        self.title.setStyleSheet("font-size: 24px; font-family: Inter; color: White; letter-spacing: 0.5px;")

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setStyleSheet("background-color: white; height: 1px; border: none;")

        self.main_button = QPushButton("Main")
        self.settings_button = QPushButton("Settings/Customization")
        for btn in (self.main_button, self.settings_button):
            btn.setStyleSheet("""
                                QPushButton {
                                    background-color: grey;
                                    color: white;
                                    font-size: 16px;
                                    padding: 10px 20px;
                                    border-radius: 8px;
                                }

                                QPushButton:hover {
                                    background-color: #0056b3;
                                }

                                QPushButton:pressed {
                                    background-color: #004080;
                                }
                            """)

        #We need to structure the page
        layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.line)
        layout.addSpacing(20)
        layout.addWidget(self.main_button)
        layout.addWidget(self.settings_button)
        layout.addStretch(1)
        self.setLayout(layout)

    def connect_buttons(self):
        self.main_button.clicked.connect(self.go_main.emit)
        self.settings_button.clicked.connect(self.go_settings.emit)