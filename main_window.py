"""
Main application window for ChatShield.

This class sets up the main window, manages all top-level views using a QStackedWidget,
and initializes the settings controller and model. It handles basic navigation between
views, applies the current theme, and delegates business logic to the MainController.
"""

# main_window.py
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import pyqtSignal

# Import your top-level files directly (no packages)
from views.homepage_view import HomepageView
from views.settings_view import SettingsView
from views.main_view import MainView
from views.filter_view import FilterView
from controllers.settings_controller import SettingsController
from models.settings_model import SettingsModel

class MainWindow(QMainWindow):
    """
    Main application window for ChatShield.

    Manages the stacked views, initializes controllers and models, and handles navigation.
    """
    go_another_view = pyqtSignal()  # (unused; keep or remove)

    def __init__(self):
        """
        Initializes the MainWindow.

        Sets up the stacked widget, all views, the settings controller, and basic navigation.
        Applies the current theme and sets the initial screen.
        """
        super().__init__()
        self.setWindowTitle("ChatShieldNLP")
        self.resize(800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Views
        self.homepage_view = HomepageView()
        self.settings_view = SettingsView()
        self.main_view = MainView()
        self.filter_view = FilterView()

        # Add to stack
        self.stacked_widget.addWidget(self.homepage_view)
        self.stacked_widget.addWidget(self.settings_view)
        self.stacked_widget.addWidget(self.main_view)
        self.stacked_widget.addWidget(self.filter_view)

        # Settings
        self.settings_model = SettingsModel()
        self.settings_controller = SettingsController(
            self.settings_model,
            self,
            [self.homepage_view, self.main_view, self.filter_view],
        )
        # Let MainController handle apply_settings; don't double-wire here.
        # self.settings_view.apply_settings.connect(self._on_apply_bg_color)

        # Apply current theme + reflect selected color in the UI
        self.settings_controller.apply_styles()
        self.settings_view.set_initial_bg_color(self.settings_controller.get_bg_color())

        # Initial screen
        self.stacked_widget.setCurrentWidget(self.homepage_view)

        # Basic navigation (business logic is in MainController)
        self.homepage_view.go_settings.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.settings_view)
        )
        self.homepage_view.go_main.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.main_view)
        )

        self.settings_view.go_homepage.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.homepage_view)
        )

        self.main_view.go_homepage.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.homepage_view)
        )
        self.main_view.go_filter.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.filter_view)
        )
        # IMPORTANT: Do NOT connect go_analyze here — MainController owns analysis.
        # self.main_view.go_analyze.connect(self.start_analysis)  # REMOVE

        self.filter_view.go_main.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.main_view)
        )

    # If you want to keep a window-level hook for manual apply (not recommended),
    # you can re-enable this method and wire it — but MainController already handles it.
    def _on_apply_bg_color(self, color: str):
        """
        Applies the selected background color using the settings controller.

        Handles errors if the color is invalid.
        """
        try:
            self.settings_controller.save_settings(color)
            # Optionally reflect immediately in settings view buttons:
            self.settings_view.apply_customization(self.settings_controller.get_bg_color())
        except ValueError as e:
            print(f"Error applying background color: {e}")
