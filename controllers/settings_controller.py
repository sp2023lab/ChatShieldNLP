from models.settings_model import SettingsModel
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow

class SettingsController:
    # # Manages theme persistence and applying it across 
    """
    Controller for managing application theme and settings persistence.

    This class handles loading, saving, and applying user settings such as background color.
    It interacts with the SettingsModel for persistence and updates the application's appearance
    by applying stylesheets to the main window and relevant views.
    """

    def __init__(self, settings_model: SettingsModel,  main_window : QMainWindow, views_to_update):
        """
        Initializes the SettingsController with the settings model, main window, and views to update.

        Loads saved settings, prepares the base stylesheet, and stores references to views that need updates.
        """
        self.settings_model = settings_model
        self.main_window = main_window
        self.views_to_update = views_to_update or []
        self.bg_color_selected = None
        self._base_qss = "QWidget { background-color: %s; }"
        self.load_settings() 
        # # store references; views_to_update can be [homepage_view, main_view, ...]
        # # prepare a base stylesheet template


    def get_bg_color(self) -> str:        # # Get the current background color from settings_model
        """
        Retrieves the current background color.

        Returns the selected color if set, otherwise fetches from the settings model or uses a default.
        """
        return self.bg_color_selected or self.settings_model.get_bg_color() or "#121212"


    def _is_valid_color(self, color: str) -> bool:
        """
        Checks if the provided color string is a valid QColor.

        Returns True if valid, otherwise False.
        """
        return QColor(color).isValid() and bool(color)


    def load_settings(self):
        """
        Loads saved settings from the settings model.

        Applies the loaded background color to the application. Falls back to default if invalid.
        """
        color = self.settings_model.get_bg_color() or "#121212"
        if not self._is_valid_color(color):
            color = "#121212"
        self.bg_color_selected = self.settings_model.get_bg_color()
        self.apply_styles()
        # # Get saved values from settings_model (bg_color)
        # # Apply them via apply_styles()


    def save_settings(self, bg_color: str):
        """
        Saves the provided background color to the settings model.

        Updates the selected color, persists it, and reapplies styles to reflect changes.
        """
        bg_color = (bg_color or "").strip().lower()
        self.settings_model.set_bg_color(bg_color)
        self.bg_color_selected = bg_color
        self.apply_styles()
        # # Validate inputs (e.g., hex code for bg_color)
        # # Persist to settings_model        
        # # Call apply_styles()


    def apply_styles(self):
        """
        Applies the current background color as a stylesheet to the main window.

        Constructs a QSS string and updates the application's appearance.
        """
        bg = self.get_bg_color()
        qss = f"""QWidget {{
            background-color: {bg};
        }}"""
        self.main_window.setStyleSheet(qss)
        # # Build a unified QSS string (global theme) using current settings
        # # Apply to main_window.setStyleSheet(...)
        # # If you need per-view tweaks, setStyleSheet on those views too


    def reset_to_default(self):
        """
        Resets all settings to their default values.

        Restores the default background color and reapplies styles.
        """
        default_bg_color = "#121212"
        self.settings_model.set_bg_color(default_bg_color)
        self.bg_color_selected = default_bg_color
        self.apply_styles() 
        # # Write default values in settings_model
        # # Call apply_styles()