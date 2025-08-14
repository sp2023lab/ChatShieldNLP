from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt

class AnalyzingPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Analyzing...")
        self.setModal(True)  # Block interaction with the main window
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Analyzing conversation...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-family: Inter; color: White; letter-spacing: 0.5px;")

        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress.setRange(0, 0) 
        self.progress.setStyleSheet("""
                                        QProgressBar {
                                            background-color: #2c2c2c;
                                            color: white;
                                            font-size: 14px;
                                            border-radius: 10px;
                                        }
                                        QProgressBar::chunk {
                                            background-color: #4caf50;
                                            border-radius: 10px;
                                        }
                                    """)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        # NOTE: Make sure to change this and adjust for the models processing the language - VERY IMPORTANT
