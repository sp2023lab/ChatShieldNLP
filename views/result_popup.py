from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class ResultPopup(QDialog):
    """
    Modal popup dialog for displaying the result of an analysis.

    This class creates a dialog that shows the analysis result text and provides a close button.
    It is used to inform the user of the outcome after processing a conversation or text.
    """
    def __init__(self, result_text: str, parent=None):
        """
        Initializes the ResultPopup dialog.

        Sets up the window title, size, result label, and close button with appropriate styles.
        """
        super().__init__(parent)
        self.setWindowTitle("Analysis Result")
        self.setModal(True)
        self.setFixedSize(420, 220)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(result_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 16px; font-family: Inter; color: White; letter-spacing: 0.5px;")

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setStyleSheet("""
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

        layout.addWidget(self.label)
        layout.addWidget(self.close_btn)
        self.setLayout(layout)