from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout, QTextEdit, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

class MainView(QWidget):
    go_homepage = pyqtSignal()
    go_filter = pyqtSignal()
    go_analyze = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_buttons()
        self.current_image_path = None  # To store the path of the uploaded image

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        logo = QLabel("ChatShield")
        logo.setStyleSheet("font-size: 32px; font-family: Inter; font-weight: 600; color: White; letter-spacing: 0.5px;")

        self.homepage_button = QPushButton("<")
        self.homepage_button.setStyleSheet("""
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
        self.one_liner_1.addWidget(self.homepage_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.one_liner_1.addStretch(1)
        self.one_liner_1.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.one_liner_1.addStretch(1)

        self.title = QLabel("Main")
        self.title.setStyleSheet("font-size: 24px; font-family: Inter; color: White; letter-spacing: 0.5px;")

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setStyleSheet("background-color: white; height: 1px; border: none;")

        #We need to add taking in text

        self.textbox = QVBoxLayout()
        
        self.textbox_label = QLabel("Enter the conversation here.")
        self.textbox_label.setStyleSheet("color: white; font-family: Inter; font-size: 16px; letter-spacing: 0.5px;")
        
        self.textbox_box = QTextEdit()
        self.textbox_box.textChanged.connect(self.handle_text_change)
        self.textbox_box.setPlaceholderText("Enter here...")
        self.textbox_box.setStyleSheet("background-color: white; color: black; font-size: 16px; font-family: Inter; padding: 10px; border-radius: 8px;")
        self.textbox_box.setFixedHeight(150)
        
        self.textbox.addWidget(self.textbox_label)
        self.textbox.addStretch(1)
        self.textbox.addWidget(self.textbox_box)
        self.textbox.addStretch(1)

        self.textbox_wrapper = QWidget()
        self.textbox_wrapper.setLayout(self.textbox)
        
        #We need to add in taking in images

        self.imagebox = QVBoxLayout()
        
        self.imagebox_label = QLabel("Upload screenshots of the conversation here.")
        self.imagebox_label.setStyleSheet("color: white; font-family: Inter; font-size: 16px; letter-spacing: 0.5px;")
        
        self.imagebox_line2 = QHBoxLayout()
        
        self.imagebox_upload = QPushButton("Upload Image")
        self.imagebox_upload.setStyleSheet("""
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
        self.imagebox_upload.clicked.connect(self.upload_image) 
        
        self.imagebox_preview = QLabel("No image uploaded")

        self.imagebox_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imagebox_preview.setStyleSheet("color: white; font-family: Inter; font-size: 16px; letter-spacing: 0.5px;")
        self.imagebox_upload.setFixedSize(200, 50)

        self.image_remove = QPushButton("X")
        self.image_remove.setFixedSize(30, 30)
        self.image_remove.setStyleSheet("""
                                            QPushButton {
                                                background-color: red;
                                                color: white;
                                                font-size: 16px;
                                                padding: 5px;
                                                border-radius: 15px;
                                            }
                                            QPushButton:hover {
                                                background-color: darkred;
                                            }
                                            QPushButton:pressed {
                                                background-color: maroon;
                                            }
                                        """)
        self.image_remove.clicked.connect(self.clear_image)
        self.image_remove.hide()
        
        self.imagebox_line2.addWidget(self.imagebox_upload)
        self.imagebox_line2.addStretch(1)
        self.imagebox_line2.addWidget(self.imagebox_preview)
        self.imagebox_line2.addStretch(1)
        self.imagebox_line2.addWidget(self.image_remove)
        self.imagebox_line2.addStretch(1)

        self.imagebox.addWidget(self.imagebox_label)
        self.imagebox.addSpacing(10)
        self.imagebox.addLayout(self.imagebox_line2)
        self.imagebox.addStretch(1)

        self.imagebox_wrapper = QWidget()
        self.imagebox_wrapper.setLayout(self.imagebox)

        #We need to add buttons for filter and analyze

        self.filter_analyze_buttons = QHBoxLayout()
        self.filter_button = QPushButton("Filter")
        self.analyze_button = QPushButton("Analyze")
        for btn in (self.filter_button, self.analyze_button):
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
        self.filter_analyze_buttons.addWidget(self.filter_button)
        self.filter_analyze_buttons.addWidget(self.analyze_button)

        #We need to structure the page

        layout.addLayout(self.one_liner_1)
        layout.addStretch(1)
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.line)
        layout.addSpacing(20)
        layout.addWidget(self.textbox_wrapper)
        layout.addSpacing(20)
        layout.addWidget(self.imagebox_wrapper)
        layout.addSpacing(20)
        layout.addLayout(self.filter_analyze_buttons)
        layout.addStretch(1)
        self.setLayout(layout)

    def upload_image(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if filepath:
            # Handle the image upload logic here
            self.current_image_path = filepath  # Store the path for later use
            print(f"Image uploaded: {filepath}")
            pixmap = QPixmap(filepath)
            scaled_pixmap = pixmap.scaled(
                self.imagebox_upload.size(),
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.imagebox_preview.setPixmap(scaled_pixmap)
            self.imagebox_preview.setText("")

            self.image_remove.show()
            self.imagebox_upload.hide()

            self.handle_image()
            self.handle_text_change()
           
    def handle_text_change(self):
        text = self.textbox_box.toPlainText().strip()
        if text:
            self.imagebox_wrapper.hide()
        else:
            self.imagebox_wrapper.show()

    def handle_image(self):
        pix = self.imagebox_preview.pixmap()
        if pix and not pix.isNull():
            self.textbox_wrapper.hide()
            self.image_remove.show()
            self.imagebox_upload.hide()
        else:
            self.textbox_wrapper.show()
            self.image_remove.hide()
            self.imagebox_upload.show()

    def clear_image(self):
        self.imagebox_preview.clear()
        self.imagebox_preview.setText("No image uploaded")
        self.image_remove.hide()
        self.imagebox_upload.show()
        self.current_image_path = None
        self.handle_image()

    def connect_buttons(self):
        self.homepage_button.clicked.connect(self.go_homepage.emit)
        self.filter_button.clicked.connect(self.go_filter.emit)
        self.analyze_button.clicked.connect(self.go_analyze.emit)