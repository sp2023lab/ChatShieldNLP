from PyQt6.QtCore import QObject, pyqtSignal, QThread
import traceback

class DetectionWorker(QThread):
    detection_done = pyqtSignal(object, float, list)
    detection_error = pyqtSignal(str)

    def __init__(self, text: str, model):
        super().__init__()
        self.text = text
        self.model = model

    def run(self):
        try:
            label, score, phrases = self.model.get_result(self.text)
            self.detection_done.emit(label, score, phrases or [])
        except Exception:
            self.detection_error.emit(traceback.format_exc())

class DetectionController(QObject):
    detection_completed = pyqtSignal(object, float, list)
    detection_failed = pyqtSignal(str)

    def __init__(self, detection_model=None, app_state=None):
        super().__init__()
        self.detection_model = detection_model
        self.app_state = app_state
        self.worker = None

    def analyze_text(self, text: str):
        if self.worker and self.worker.isRunning():
            return
        self.worker = DetectionWorker(text, self.detection_model)
        self.worker.detection_done.connect(self._on_done)
        self.worker.detection_error.connect(self._on_error)
        self.worker.finished.connect(self._cleanup)
        self.worker.start()

    def _on_done(self, label, score, phrases):
        self.detection_completed.emit(label, score, phrases)

    def _on_error(self, msg: str):
        self.detection_failed.emit(msg)

    def _cleanup(self):
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
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.quit()
            self.worker.wait(1500)
            if self.worker.isRunning():
                self.worker.terminate()
                self.worker.wait()
        self._cleanup()

    def _threshold_for_intensity(self) -> float:
        intensity = (getattr(self.app_state, "intensity", "easy") or "easy").strip().lower()
        thresholds = {
            "easy":   0.55,
            "medium": 0.30,
        }
        return thresholds.get(intensity, 0.55)

    def apply_intensity_filter(self, label, score, phrases) -> bool:
        thresh = self._threshold_for_intensity()
        print(f"[filter] threshold={thresh:.2f} score={score:.2f}")
        return score >= thresh