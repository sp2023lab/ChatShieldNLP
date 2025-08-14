import os
import platform

# Constants
DEFAULT_TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows default

def detect_tesseract_path() -> str | None:
    """
    Tries to find the tesseract executable based on OS.
    Returns full path if found, else None.
    """
    system = platform.system()

    candidates = []

    if system == "Windows":
        candidates = [
            DEFAULT_TESSERACT_PATH,
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe"
        ]
    elif system == "Darwin":  # macOS
        candidates = [
            "/opt/homebrew/bin/tesseract",
            "/usr/local/bin/tesseract"
        ]
    elif system == "Linux":
        candidates = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract"
        ]

    for path in candidates:
        if is_valid_tesseract_path(path):
            return path

    return None


def is_valid_tesseract_path(path: str) -> bool:
    """
    Checks if given path exists and is executable.
    """
    return isinstance(path, str) and os.path.isfile(path) and os.access(path, os.X_OK)
