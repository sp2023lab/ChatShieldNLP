# main_controller.py
from views.analyzing_popup import AnalyzingPopup
from views.result_popup import ResultPopup

class MainController:
    def __init__(self, main_window, app_state, ocr_controller, detection_controller, settings_controller):
        self.main_window = main_window
        self.app_state = app_state
        self.ocr_controller = ocr_controller
        self.detection_controller = detection_controller
        self.settings_controller = settings_controller

        self.stacked_widget = main_window.stacked_widget
        self.homepage_view = main_window.homepage_view
        self.settings_view = main_window.settings_view
        self.main_view = main_window.main_view
        self.filter_view = main_window.filter_view

        self._analyzing = None
        self._last_image_path = None

        self.connect_views()
        self.settings_controller.load_settings()  # Apply initial theme

    def connect_views(self):
        w = self.main_window
        # Homepage
        w.homepage_view.go_main.connect(lambda: w.stacked_widget.setCurrentWidget(w.main_view))
        w.homepage_view.go_settings.connect(lambda: w.stacked_widget.setCurrentWidget(w.settings_view))

        # Settings
        w.settings_view.go_homepage.connect(lambda: w.stacked_widget.setCurrentWidget(w.homepage_view))
        w.settings_view.apply_settings.connect(self.on_apply_settings)

        # Main
        w.main_view.go_homepage.connect(lambda: w.stacked_widget.setCurrentWidget(w.homepage_view))
        w.main_view.go_filter.connect(lambda: w.stacked_widget.setCurrentWidget(w.filter_view))
        w.main_view.go_analyze.connect(self.on_analyze_click)

        # Filter
        w.filter_view.go_main.connect(self._on_filter_back)

        # OCR/Detection signals
        self.ocr_controller.ocr_completed.connect(self.on_ocr_completed)
        self.ocr_controller.ocr_failed.connect(self.on_error)
        self.detection_controller.detection_completed.connect(self.on_detection_result)
        self.detection_controller.detection_failed.connect(self.on_error)

    def on_apply_settings(self, bg_color: str):
        self.settings_controller.save_settings(bg_color)
        self.settings_controller.apply_styles()

    def on_analyze_click(self):
        text = self.main_view.textbox_box.toPlainText().strip()
        pix = self.main_view.imagebox_preview.pixmap()
        self.app_state.message_text = text

        if text:
            self.run_detection(text)
            return

        if pix:
            path = getattr(self.main_view, "current_image_path", None) or self.app_state.image_path
            if not path:
                self.show_result_popup("No image path found. Please re-upload.")
                return
            self._last_image_path = path
            self.show_analyzing_popup()     # show spinner during OCR too
            self.ocr_controller.run_ocr(path)
            return

        self.show_result_popup("Please enter text or upload an image first.")

    def handle_text_submission(self, text: str):
        self.app_state.message_text = text or ""
        self.app_state.image_path = None
        if text:
            self.run_detection(text)

    def handle_image_submission(self, path: str):
        self.app_state.image_path = path
        self._last_image_path = path
        self.app_state.message_text = ""
        self.show_analyzing_popup()
        self.ocr_controller.run_ocr(path)

    def on_ocr_completed(self, extracted_text: str):
        if not extracted_text.strip():
            self._close_analyzing()
            self.show_result_popup("Couldn’t read any text from the image.")
            return
        self.app_state.message_text = extracted_text
        self.run_detection(extracted_text)

    def run_detection(self, text: str):
        if not getattr(self, "_analyzing", None):  # keep spinner if already shown by OCR
            self.show_analyzing_popup()
        self.detection_controller.analyze_text(text)

    def on_detection_result(self, label, score, phrases):
        self._close_analyzing()

        # NOTE: pass score here (your old call didn’t)
        if not self.detection_controller.apply_intensity_filter(label, score, phrases):
            self.show_result_popup("No issues detected under current filter.")
            return

        summary = f"Label: {label}\nScore: {score:.2f}\n"
        if phrases:
            summary += "Matched: " + ", ".join(phrases)
        self.show_result_popup(summary)

    def on_error(self, message: str):
        self._close_analyzing()
        self.show_result_popup(f"Error: {message}")

    def show_analyzing_popup(self):
        self._analyzing = AnalyzingPopup(self.main_window)
        self._analyzing.show()

    def _close_analyzing(self):
        if getattr(self, "_analyzing", None):
            try:
                self._analyzing.reject()
            except Exception:
                pass
            self._analyzing = None

    def show_result_popup(self, result_text, score=None, phrases=None):
        dlg = ResultPopup(result_text, self.main_window)
        dlg.exec()

    def _on_filter_back(self):
        chosen = self.filter_view.get_selected_intensity() or "easy"
        self.app_state.intensity = chosen
        self.stacked_widget.setCurrentWidget(self.main_window.main_view)
