from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

ALLOWED_EXTS = (".png", ".jpg", ".jpeg", ".bmp")

def scale_pixmap_to_fit(path: str, max_width: int, max_height: int) -> QPixmap:
    if not isinstance(path, str) or not os.path.exists(path):
        return QPixmap()
    if max_width <= 0 or max_height <= 0:
        return QPixmap()
    pixmap = QPixmap(path)
    if pixmap.isNull():
        return QPixmap()
    return pixmap.scaled(max_width, max_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

def is_valid_image(path: str) -> bool:
    if not isinstance(path, str):
        return False
    if not os.path.exists(path):
        return False
    return path.lower().endswith(ALLOWED_EXTS)

def cleanup_ocr_text(text: str) -> str:
    text = (text or "")
    text = text.replace("\x0c", " ")
    text = text.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "")
    text = " ".join(text.split())
    return text.strip()
