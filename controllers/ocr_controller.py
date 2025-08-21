# controllers/ocr_controller.py
from __future__ import annotations

import os
import traceback
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal, QThread

# === use utils ===
from utils.image_utils import is_valid_image, cleanup_ocr_text

# Hard dependencies (installed in your venv): Pillow, pytesseract
try:
    from PIL import Image, UnidentifiedImageError
except Exception:
    Image = None  # type: ignore
    UnidentifiedImageError = Exception  # type: ignore

try:
    import pytesseract
    from pytesseract import TesseractNotFoundError, TesseractError
except Exception:
    pytesseract = None  # type: ignore
    class TesseractNotFoundError(Exception): ...
    class TesseractError(Exception): ...


class OCRWorker(QThread):
    """
    QThread that runs pytesseract on a given image path.

    This worker thread performs OCR on an image file using pytesseract.
    It emits signals when OCR is complete or if an error occurs, allowing the main UI to remain responsive.
    Handles image validation, Tesseract configuration, and interruption requests.
    """
    ocr_done = pyqtSignal(str)
    ocr_error = pyqtSignal(str)

    def __init__(self, image_path: str, tesseract_path: Optional[str] = None, lang: str = "eng", parent: Optional[QObject] = None):
        """
        Initializes the OCRWorker with the image path, optional Tesseract binary path, and language.

        Sets up the worker for asynchronous OCR processing.
        """
        super().__init__(parent)
        self.image_path = image_path
        self.tesseract_path = tesseract_path
        self.lang = lang

    def run(self):
        """
        Executes the OCR process in a separate thread.

        Validates the image, configures Tesseract, performs OCR, and emits the result or error.
        Handles interruption requests and various error scenarios gracefully.
        """
        # Library presence checks (clear messages instead of stack traces)
        if pytesseract is None:
            self.ocr_error.emit("pytesseract is not installed. Run: pip install pytesseract Pillow")
            return
        if Image is None:
            self.ocr_error.emit("Pillow (PIL) is not installed. Run: pip install Pillow")
            return

        try:
            # Fast validation using utils (file exists + allowed extension)
            if not is_valid_image(self.image_path):
                # Provide a precise reason if possible
                if not isinstance(self.image_path, str) or not self.image_path:
                    self.ocr_error.emit("No image path provided.")
                elif not os.path.exists(self.image_path):
                    self.ocr_error.emit(f"Image not found: {self.image_path}")
                else:
                    self.ocr_error.emit(f"Unsupported image type (allowed: .png, .jpg, .jpeg, .bmp): {self.image_path}")
                return

            # Configure Tesseract binary if provided
            if self.tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

            # Open image safely
            with Image.open(self.image_path) as img:
                # Convert to RGB to avoid mode issues
                img = img.convert("RGB")

                if self.isInterruptionRequested():
                    return

                # OCR (add config if you like: config='--psm 6')
                text = pytesseract.image_to_string(img, lang=self.lang)

            if self.isInterruptionRequested():
                return

            # Clean OCR text via utils
            cleaned = cleanup_ocr_text(text or "")
            self.ocr_done.emit(cleaned)

        except TesseractNotFoundError:
            self.ocr_error.emit(
                "Tesseract executable not found. "
                "Install Tesseract OCR and/or set the correct path in main.py "
                "(e.g. tesseract_path=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')."
            )
        except TesseractError as e:
            # Common when language data is missing/invalid config
            self.ocr_error.emit(f"Tesseract error (language/config): {e}")
        except (UnidentifiedImageError, OSError) as e:
            self.ocr_error.emit(f"Invalid or unreadable image: {e}")
        except Exception:
            self.ocr_error.emit(traceback.format_exc())


class OCRController(QObject):
    """
    Orchestrates OCRWorker lifecycle.

    This controller manages the creation, execution, and cleanup of OCRWorker threads.
    It provides a simple interface for running OCR and emits signals when OCR is complete or fails.
    """
    ocr_completed = pyqtSignal(str)
    ocr_failed = pyqtSignal(str)

    def __init__(self, tesseract_path: Optional[str] = None, lang: str = "eng", parent: Optional[QObject] = None):
        """
        Initializes the OCRController with optional Tesseract path and language.

        Preconfigures Tesseract if a path is provided and prepares for OCR operations.
        """
        super().__init__(parent)
        self.tesseract_path = tesseract_path
        self.lang = lang
        self.worker: Optional[OCRWorker] = None

        # Preconfigure tesseract path if provided
        if pytesseract and self.tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

    def run_ocr(self, image_path: str):
        """
        Starts OCR on the given image path in a worker thread.

        Ensures only one OCR operation runs at a time and connects signals for result and error handling.
        """
        # Avoid parallel runs
        if self.worker and self.worker.isRunning():
            return

        self.worker = OCRWorker(image_path=image_path, tesseract_path=self.tesseract_path, lang=self.lang)
        self.worker.ocr_done.connect(self._on_done)
        self.worker.ocr_error.connect(self._on_error)
        self.worker.finished.connect(self._cleanup)
        self.worker.start()

    def cancel(self):
        """
        Cancels any ongoing OCR operation.

        Requests interruption and termination of the worker thread if running, then cleans up resources.
        """
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.quit()
            self.worker.wait(1500)
            if self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait()
        self._cleanup()

    # --- internal slots ---
    def _on_done(self, cleaned_text: str):
        """
        Internal slot: emits the ocr_completed signal with the cleaned OCR text.
        """
        self.ocr_completed.emit(cleaned_text)

    def _on_error(self, message: str):
        """
        Internal slot: emits the ocr_failed signal with the error message.
        """
        self.ocr_failed.emit(message)

    def _cleanup(self):
        """
        Cleans up the worker thread and disconnects all signals.

        Ensures resources are released and the worker is properly deleted after completion.
        """
        if self.worker:
            try:
                self.worker.ocr_done.disconnect(self._on_done)
                self.worker.ocr_error.disconnect(self._on_error)
                self.worker.finished.disconnect(self._cleanup)
            except Exception:
                pass
            self.worker.deleteLater()
            self.worker = None
