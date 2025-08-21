from PyQt6.QtCore import QThread, pyqtSignal

class ThreadWorker(QThread):
    """
    Generic worker thread for running any function asynchronously.

    This class allows you to execute a provided function with arguments in a separate thread.
    It emits a signal with the result when finished, or an error signal if an exception occurs.
    Useful for offloading blocking or long-running tasks from the main UI thread.
    """

    finished_with_result = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, fn=None, args=None, kwargs=None, parent=None):
        """
        Initializes the ThreadWorker with a function, its arguments, and optional parent.

        Stores the function and its arguments for later execution in the thread.
        """
        super().__init__(parent)
        self.fn = fn
        self.args = args or ()
        self.kwargs = kwargs or {}

    def run(self):
        """
        Executes the provided function with its arguments in a separate thread.

        Emits the finished_with_result signal with the result if successful,
        or the failed signal with the error message if an exception occurs.
        """        
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.finished_with_result.emit(result)
        except Exception as e:
            self.failed.emit(str(e))