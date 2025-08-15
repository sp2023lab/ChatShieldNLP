# main.py
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from models.app_state import AppState
from controllers.main_controller import MainController
from controllers.ocr_controller import OCRController
from controllers.detection_controller import DetectionController
from models.detection_model import DetectionModel 
from assets.tesseract_path_config import detect_tesseract_path

# For github do the following:
# 1. git add .
# 2. git commit -m "your message"
# 3. git push origin main

tesseract_path = detect_tesseract_path()
print(f"Detected Tesseract path: {tesseract_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()                 # creates SettingsController internally
    app_state = AppState()

    ocr = OCRController(
        tesseract_path=tesseract_path
    )

    detection_model = DetectionModel()
    detection = DetectionController(
        detection_model=detection_model,
        app_state=app_state,
    )

    controller = MainController(
        main_window=window,
        app_state=app_state,
        ocr_controller=ocr,
        detection_controller=detection,
        settings_controller=window.settings_controller,   # <-- reuse the one in MainWindow
    )

    window.show()
    sys.exit(app.exec())