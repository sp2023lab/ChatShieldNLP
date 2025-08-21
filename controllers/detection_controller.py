from PyQt6.QtCore import QObject, pyqtSignal, QThread
import traceback

class DetectionWorker(QThread):
    """
    Worker thread for running the detection model asynchronously.

    This class takes input text and a detection model, runs the detection in a separate thread,
    and emits signals when the detection is complete or if an error occurs. This prevents blocking
    the main UI thread during potentially slow detection operations.
    """
    detection_done = pyqtSignal(object, float, list)
    detection_error = pyqtSignal(str)

    def __init__(self, text: str, model):
        super().__init__()
        self.text = text
        self.model = model

    def run(self):
        """
        Executes the detection model on the provided text.

        Emits a signal with the result if successful, or an error signal if an exception occurs.
        """
        try:
            label, score, phrases = self.model.get_result(self.text)
            self.detection_done.emit(label, score, phrases or [])
        except Exception:
            self.detection_error.emit(traceback.format_exc())

class DetectionController(QObject):
    """
    Controller class for managing detection operations and threading.

    This class manages the lifecycle of the DetectionWorker, handles signals for completion and errors,
    and provides methods to start, cancel, and filter detection results based on intensity thresholds.
    """
    detection_completed = pyqtSignal(object, float, list)
    detection_failed = pyqtSignal(str)

    def __init__(self, detection_model=None, app_state=None):
        super().__init__()
        self.detection_model = detection_model
        self.app_state = app_state
        self.worker = None

    def analyze_text(self, text: str):
        """
        Starts a new detection analysis in a worker thread.

        If a worker is already running, this call is ignored. Connects signals for result and error handling.
        """
        if self.worker and self.worker.isRunning():
            return
        self.worker = DetectionWorker(text, self.detection_model)
        self.worker.detection_done.connect(self._on_done)
        self.worker.detection_error.connect(self._on_error)
        self.worker.finished.connect(self._cleanup)
        self.worker.start()

    def _on_done(self, label, score, phrases):
        """
        Handles successful detection completion by emitting the detection_completed signal.
        """
        self.detection_completed.emit(label, score, phrases)

    def _on_error(self, msg: str):
        """
        Handles successful detection completion by emitting the detection_completed signal.
        """
        self.detection_failed.emit(msg)

    def _cleanup(self):
        """
        Cleans up the worker thread and disconnects all signals.

        Ensures that resources are released and the worker is properly deleted after completion.
        """
        if self.worker:
            try:
                self.worker.detection_done.disconnect(self._on_done)
                self.worker.detection_error.disconnect(self._on_error)
                self.worker.finished.disconnect(self._cleanup)
            except Exception:
                pass
            self.worker.deleteLater()
            self.worker = None

    def cancel_analysis(self):
        """
        Cancels any ongoing detection analysis.

        Requests interruption and termination of the worker thread if it is running, then cleans up resources.
        """
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.quit()
            self.worker.wait(1500)
            if self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait()
        self._cleanup()

    def _threshold_for_intensity(self) -> float:
        """
        Returns the detection threshold based on the current intensity setting.

        The threshold determines how sensitive the detection is. Lower thresholds catch more cases.
        """
        intensity = (getattr(self.app_state, "intensity", "easy") or "easy").strip().lower()
        thresholds = {
            "easy":   0.45,
            "medium": 0.30,
        }
        return thresholds.get(intensity, 0.45)

    def apply_intensity_filter(self, label, score, phrases) -> bool:
        """
        Applies the current intensity threshold to the detection score.

        Returns True if the score meets or exceeds the threshold, otherwise False.
        """
        thresh = self._threshold_for_intensity()
        print(f"[filter] threshold={thresh:.2f} score={score:.2f}")
        return score >= thresh