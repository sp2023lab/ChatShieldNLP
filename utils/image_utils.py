from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

ALLOWED_EXTS = (".png", ".jpg", ".jpeg", ".bmp")

def scale_pixmap_to_fit(path: str, max_width: int, max_height: int) -> QPixmap:
    print("scale_pixmap_to_fit called with path: {}, max_width: {}, max_height: {}".format(path, max_width, max_height))
    if not isinstance(path, str) or not os.path.exists(path):
        print("Invalid path or file does not exist.")
        return QPixmap()
    if max_width <= 0 or max_height <= 0:
        print("Invalid dimensions: max_width and max_height must be greater than 0.")
        return QPixmap()
    print("All parameters are valid. Proceeding with scaling.")
    pixmap = QPixmap(path)
    if pixmap.isNull():
        print("Failed to load pixmap from path: {}".format(path))
        return QPixmap()
    print("Pixmap loaded successfully. Scaling to fit within max dimensions.")
    return pixmap.scaled(max_width, max_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

def is_valid_image(path: str) -> bool:
    print("is_valid_image called with path: {}".format(path))
    if not isinstance(path, str):
        print("Invalid path type. Expected a string.")
        return False
    if not os.path.exists(path):
        print(f"File does not exist: {path}")
        return False
    print(f"Checking file extension for: {path}")
    return path.lower().endswith(ALLOWED_EXTS)

def cleanup_ocr_text(text: str) -> str:
    text = (text or "")
    text = text.replace("\x0c", " ")
    text = text.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "")
    text = " ".join(text.split())
    print(f"Here is the text: {text.strip()}")
    return text.strip()
