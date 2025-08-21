from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QButtonGroup, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal

class FilterView(QWidget):
    """
    View for selecting message filter intensity.

    This class provides a UI for users to choose the detection sensitivity (Easy or Medium)
    using radio buttons. It includes navigation controls and emits a signal to return to the main view.
    """
    go_main = pyqtSignal()

    def __init__(self):
        """
        Initializes the FilterView.

        Sets up the UI components, layouts, and connects button signals.
        """
        super().__init__()
        self.setup_ui()
        self.connect_buttons()

    def setup_ui(self):
        """
        Sets up the layout and widgets for the filter selection view.

        Adds logo, navigation button, title, radio buttons for intensity, and styles them appropriately.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.logo = QLabel("ChatShield")
        self.logo.setStyleSheet("font-size: 32px; font-family: Inter; font-weight: 600; color: White; letter-spacing: 0.5px;")

        self.main_button = QPushButton("<")
        self.main_button.setStyleSheet("""
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

        self.one_liner_1 = QHBoxLayout()
        self.one_liner_1.addWidget(self.main_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.one_liner_1.addStretch(1)
        self.one_liner_1.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.one_liner_1.addStretch(1)

        self.title = QLabel("Filter")
        self.title.setStyleSheet("font-size: 24px; font-family: Inter; color: White; letter-spacing: 0.5px;")

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setStyleSheet("background-color: white; height: 1px; border: none;")

        #QRadio buttons
        self.radio_easy = QRadioButton("Easy")
        self.radio_medium = QRadioButton("Medium")
        for btn in (self.radio_easy, self.radio_medium):
            btn.setCheckable(True)
            btn.setStyleSheet("""
                                QRadioButton { color: white; font-size: 16px; }
                                QRadioButton::indicator { width: 18px; height: 18px; }
                                QRadioButton::indicator:checked { background-color: #2ecc71; }
                            """)

        self.difficulty_buttons_group = QButtonGroup(self)
        self.difficulty_buttons_group.setExclusive(True)
        self.difficulty_buttons_group.addButton(self.radio_easy)
        self.difficulty_buttons_group.addButton(self.radio_medium)

        #We need to structure the page
        layout.addLayout(self.one_liner_1)
        layout.addStretch(1)
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.line)
        layout.addSpacing(20)
        layout.addWidget(self.radio_easy)
        layout.addWidget(self.radio_medium)
        layout.addStretch(1)
        self.setLayout(layout)

    def get_selected_intensity(self):
        """
        Returns the currently selected intensity level.

        Returns "easy", "medium", or None if no option is selected.
        """
        if self.radio_easy.isChecked():
            return "easy"
        elif self.radio_medium.isChecked():
            return "medium"
        return None

    def connect_buttons(self):
        """
        Connects the navigation button to emit the go_main signal.

        Allows the user to return to the main view.
        """
        self.main_button.clicked.connect(self.go_main.emit)