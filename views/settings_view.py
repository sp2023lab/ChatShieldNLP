from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class SettingsView(QWidget):
    """
    View for customizing application settings, such as background color.

    This class provides a UI for users to select and apply customization options.
    It includes controls for navigation, color selection, and applying settings,
    and emits signals when actions are taken.
    """
    go_homepage = pyqtSignal()
    apply_settings = pyqtSignal(str)

    def __init__(self):
        """
        Initializes the SettingsView.

        Sets up the UI components, layouts, and connects button signals.
        """
        super().__init__()
        self.setup_ui()
        self.connect_buttons()

    def setup_ui(self):
        """
        Sets up the layout and widgets for the settings view.

        Adds navigation, title, color selection buttons, and an apply button,
        and arranges them with appropriate styles.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.logo = QLabel("ChatShield")
        self.logo.setStyleSheet("font-size: 32px; font-family: Inter; font-weight: 600; color: white; letter-spacing: 0.5px;")

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

        self.top_bar = QHBoxLayout()
        self.top_bar.addWidget(self.homepage_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.top_bar.addStretch(1)
        self.top_bar.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.top_bar.addStretch(1)

        self.title = QLabel("Settings/Customization")
        self.title.setStyleSheet("font-size: 24px; font-family: Inter; color: white; letter-spacing: 0.5px;")

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setStyleSheet("background-color: white; height: 1px; border: none;")

        self.bg_color_selected = None
        self.bg_color_buttons = []
        self.bg_color_row = QHBoxLayout()
        self.bg_label = QLabel("Customize Background Color:")
        self.bg_label.setStyleSheet("color: white; font-size: 16px;")
        self.bg_color_row.addWidget(self.bg_label)
        self.bg_color_row.addStretch(1)
        for color in ["red", "orange", "yellow", "green", "blue", "#121212"]:
            btn = self._create_color_button(color, self.select_bg_color)
            self.bg_color_buttons.append(btn)
            self.bg_color_row.addWidget(btn)

        self.apply_settings_button = QPushButton("Apply Settings")
        self.apply_settings_button.setStyleSheet("""
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
        self.apply_settings_button.clicked.connect(lambda: self.apply_settings.emit(
            self.bg_color_selected or "#121212"
        ))

        #We need to structure the page
        layout.addLayout(self.top_bar)
        layout.addStretch(1)
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.line)
        layout.addSpacing(20)
        layout.addLayout(self.bg_color_row)
        layout.addWidget(self.apply_settings_button)
        layout.addStretch(1)
        self.setLayout(layout)


    def apply_customization(self, bg_color: str):
        """
        Applies the selected background color to the view.

        Updates the stylesheet to reflect the chosen color.
        """
        style = f"QWidget {{ background-color: {bg_color};}}"
        self.setStyleSheet(style)


    #Helper to create a color button
    def _create_color_button(self, color, callback):
        """
        Helper to create a color selection button.

        Configures the button's appearance and connects its click event to the provided callback.
        """        
        btn = QPushButton()
        btn.setCheckable(True)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 2px solid white;
                border-radius: 5px;
            }}
            QPushButton:checked {{
                border: 2px solid black;
            }}
        """)
        btn.clicked.connect(lambda _, b=btn, c=color: callback(b, c))
        btn._color = color
        return btn

    #Select Background Color Handler
    def select_bg_color(self, clicked_button, color):
        """
        Handles background color selection.

        Updates the selected color and button states.
        """
        self.bg_color_selected = color
        for btn in self.bg_color_buttons:
            btn.setChecked(btn == clicked_button)
        print("Background color selected:", color)

    def connect_buttons(self):
        """
        Connects navigation and apply buttons to their respective signals.

        Enables interaction between the view and the rest of the application.
        """
        self.homepage_button.clicked.connect(self.go_homepage.emit)

    def set_initial_bg_color(self, color: str):
        """
        Sets the initial background color selection.

        Updates the button states to reflect the current color.
        """
        self.bg_color_selected = color
        for b in self.bg_color_buttons:
            b.setChecked(getattr(b, '_color', '') == color)