from PyQt6.QtCore import QSettings  # <- use this backend
from PyQt6.QtGui import QColor

class SettingsModel:
    # # Encapsulates persistent app settings via QSettings

    # ---- constants ----
    _ORG = "OrgName: SP2023LAB"          # shown in OS registry/plist
    _APP = "CreepyMessageDetector"
    KEY_BG_COLOR = "ui/bg_color"
    DEFAULT_BG_COLOR = "#121212"

    def __init__(self):
        # # Create QSettings store (Format.Native by default)
        self._settings = QSettings(self._ORG, self._APP)
        # # Optionally seed defaults if missing
        self._ensure_defaults()

    # --------- public API ----------
    def get_bg_color(self) -> str:
        return self._get(self.KEY_BG_COLOR, self.DEFAULT_BG_COLOR)

    def set_bg_color(self, color: str) -> None:
        if self._is_valid_color(color):
            self._set(self.KEY_BG_COLOR, color.strip().lower())
        else:
            raise ValueError("Invalid color format. Use hex code or named colors.")

    def reset_to_defaults(self) -> None:
        self._settings.clear()
        # # Reset all settings to their defaults
        self._ensure_defaults()

    def export_all(self) -> dict:
        # # Return all settings as a dict
        return {
            self.KEY_BG_COLOR: self.get_bg_color(),
            # Add other keys as needed
        }

    def import_all(self, data: dict) -> None:
        # # Import settings from a dict
        if self.KEY_BG_COLOR in data:
            self.set_bg_color(data[self.KEY_BG_COLOR])
        # Handle other keys as needed

    # --------- private helpers ----------
    def _get(self, key: str, default):
        # # thin wrapper around self._settings.value(key, defaultValue)
        value = self._settings.value(key, default, type=str)
        return value if value is not None else default

    def _set(self, key: str, value):
        # # thin wrapper around self._settings.setValue(key, value)
        self._settings.setValue(key, value)

    def _ensure_defaults(self):
        # # if KEY_BG_COLOR not set, set to DEFAULT_BG_COLOR
        if not self._settings.contains(self.KEY_BG_COLOR):
            self._set(self.KEY_BG_COLOR, self.DEFAULT_BG_COLOR)

    def _is_valid_color(self, color: str) -> bool:
        # # Check if the color is a valid hex code or a named color
        return isinstance(color, str) and bool(color) and QColor(color).isValid()