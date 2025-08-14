from PyQt6.QtCore import QThread, pyqtSignal

class ThreadWorker(QThread):

    finished_with_result = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, fn=None, args=None, kwargs=None, parent=None):
        super().__init__(parent)
        self.fn = fn
        self.args = args or ()
        self.kwargs = kwargs or {}

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.finished_with_result.emit(result)
        except Exception as e:
            self.failed.emit(str(e))