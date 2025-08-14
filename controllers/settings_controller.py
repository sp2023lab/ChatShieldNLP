from models.settings_model import SettingsModel
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow

class SettingsController:
    # # Manages theme persistence and applying it across views

    def __init__(self, settings_model: SettingsModel,  main_window : QMainWindow, views_to_update):
        self.settings_model = settings_model
        self.main_window = main_window
        self.views_to_update = views_to_update or []
        self.bg_color_selected = None
        self._base_qss = "QWidget { background-color: %s; }"
        self.load_settings() 
        # # store references; views_to_update can be [homepage_view, main_view, ...]
        # # prepare a base stylesheet template


    def get_bg_color(self) -> str:        # # Get the current background color from settings_model
        return self.bg_color_selected or self.settings_model.get_bg_color() or "#121212"


    def _is_valid_color(self, color: str) -> bool:
        return QColor(color).isValid() and bool(color)


    def load_settings(self):
        color = self.settings_model.get_bg_color() or "#121212"
        if not self._is_valid_color(color):
            color = "#121212"
        self.bg_color_selected = self.settings_model.get_bg_color()
        self.apply_styles()
        # # Get saved values from settings_model (bg_color)
        # # Apply them via apply_styles()


    def save_settings(self, bg_color: str):
        bg_color = (bg_color or "").strip().lower()
        self.settings_model.set_bg_color(bg_color)
        self.bg_color_selected = bg_color
        self.apply_styles()
        # # Validate inputs (e.g., hex code for bg_color)
        # # Persist to settings_model        
        # # Call apply_styles()


    def apply_styles(self):
        bg = self.get_bg_color()
        qss = f"""QWidget {{
            background-color: {bg};
        }}"""
        self.main_window.setStyleSheet(qss)
        # # Build a unified QSS string (global theme) using current settings
        # # Apply to main_window.setStyleSheet(...)
        # # If you need per-view tweaks, setStyleSheet on those views too


    def reset_to_default(self):
        default_bg_color = "#121212"
        self.settings_model.set_bg_color(default_bg_color)
        self.bg_color_selected = default_bg_color
        self.apply_styles() 
        # # Write default values in settings_model
        # # Call apply_styles()