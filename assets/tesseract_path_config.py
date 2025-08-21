# assets/tesseract_path_config.py
import os
import platform

ENV_VAR = "TESSERACT_PATH"

COMMON_WINDOWS = [
    r"C:\Users\shyam\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",  # your install
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Tesseract-OCR\tesseract.exe",
]

COMMON_MAC = [
    "/opt/homebrew/bin/tesseract",
    "/usr/local/bin/tesseract",
    "/usr/bin/tesseract",
]

COMMON_LINUX = [
    "/usr/bin/tesseract",
    "/usr/local/bin/tesseract",
]

def is_valid_tesseract_path(path: str) -> bool:
    """
    Checks if the provided path is a valid Tesseract executable.

    This function verifies that the given path is a string, points to an existing file,
    and that the file is executable. It is used to ensure that the Tesseract binary
    can be run from the specified location.
    """
    return isinstance(path, str) and os.path.isfile(path) and os.access(path, os.X_OK)

def detect_tesseract_path() -> str | None:
    """
    Attempts to automatically locate the Tesseract executable on the system.

    The function first checks if the TESSERACT_PATH environment variable is set and valid.
    If not, it searches through a list of common installation paths based on the current OS
    (Windows, macOS, or Linux). If a valid executable is found, its path is returned.
    If no valid path is found, the function returns None.
    """
    # 1) environment variable wins
    env_path = os.environ.get(ENV_VAR)
    if env_path and is_valid_tesseract_path(env_path):
        return env_path

    # 2) OS-specific candidates
    system = platform.system()
    candidates = COMMON_WINDOWS if system == "Windows" else COMMON_MAC if system == "Darwin" else COMMON_LINUX

    for p in candidates:
        if is_valid_tesseract_path(p):
            return p

    # 3) give up
    return None
