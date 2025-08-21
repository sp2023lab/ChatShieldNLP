from PyQt6.QtCore import QSettings  # <- use this backend
from PyQt6.QtGui import QColor

class SettingsModel:
    """
    Encapsulates persistent app settings via QSettings.

    This class manages loading, saving, exporting, and importing application settings such as
    background color. It uses QSettings for cross-platform persistence and provides validation
    for color values. Defaults are ensured on initialization.
    """
    # # Encapsulates persistent app settings via QSettings

    # ---- constants ----
    _ORG = "OrgName: SP2023LAB"          # shown in OS registry/plist
    _APP = "CreepyMessageDetector"
    KEY_BG_COLOR = "ui/bg_color"
    DEFAULT_BG_COLOR = "#121212"

    def __init__(self):
        """
        Initializes the SettingsModel and ensures default settings are present.

        Creates the QSettings store and seeds default values if missing.
        """
        # # Create QSettings store (Format.Native by default)
        self._settings = QSettings(self._ORG, self._APP)
        # # Optionally seed defaults if missing
        self._ensure_defaults()

    # --------- public API ----------
    def get_bg_color(self) -> str:
        """
        Retrieves the current background color from persistent settings.

        Returns the stored color or the default if not set.
        """
        return self._get(self.KEY_BG_COLOR, self.DEFAULT_BG_COLOR)

    def set_bg_color(self, color: str) -> None:
        """
        Sets and saves the background color after validating the input.

        Raises ValueError if the color is not a valid hex code or named color.
        """        
        if self._is_valid_color(color):
            self._set(self.KEY_BG_COLOR, color.strip().lower())
        else:
            raise ValueError("Invalid color format. Use hex code or named colors.")

    def reset_to_defaults(self) -> None:
        """
        Resets all settings to their default values.

        Clears the settings store and re-applies defaults.
        """        
        self._settings.clear()
        # # Reset all settings to their defaults
        self._ensure_defaults()

    def export_all(self) -> dict:
        """
        Exports all settings as a dictionary.

        Useful for backup or migration of user preferences.
        """        
        # # Return all settings as a dict
        return {
            self.KEY_BG_COLOR: self.get_bg_color(),
            # Add other keys as needed
        }

    def import_all(self, data: dict) -> None:
        """
        Imports settings from a dictionary.

        Updates settings based on provided data, with validation.
        """        
        # # Import settings from a dict
        if self.KEY_BG_COLOR in data:
            self.set_bg_color(data[self.KEY_BG_COLOR])
        # Handle other keys as needed

    # --------- private helpers ----------
    def _get(self, key: str, default):
        """
        Internal helper to retrieve a value from QSettings with a default fallback.
        """        
        # # thin wrapper around self._settings.value(key, defaultValue)
        value = self._settings.value(key, default, type=str)
        return value if value is not None else default

    def _set(self, key: str, value):
        """
        Internal helper to set a value in QSettings.
        """
        # # thin wrapper around self._settings.setValue(key, value)
        self._settings.setValue(key, value)

    def _ensure_defaults(self):
        """
        Ensures all required default settings are present in QSettings.
        """
        # # if KEY_BG_COLOR not set, set to DEFAULT_BG_COLOR
        if not self._settings.contains(self.KEY_BG_COLOR):
            self._set(self.KEY_BG_COLOR, self.DEFAULT_BG_COLOR)

    def _is_valid_color(self, color: str) -> bool:
        """
        Checks if the color is a valid hex code or named color.

        Returns True if valid, otherwise False.
        """
        # # Check if the color is a valid hex code or a named color
        return isinstance(color, str) and bool(color) and QColor(color).isValid()