# main_controller.py
from views.analyzing_popup import AnalyzingPopup
from views.result_popup import ResultPopup

class MainController:
    """
    Main controller for managing the application's core logic and view transitions.

    This class coordinates user interactions, view switching, OCR and detection operations,
    and handles displaying results or errors. It acts as the central hub connecting the UI,
    OCR, detection, and settings controllers.
    """
    def __init__(self, main_window, app_state, ocr_controller, detection_controller, settings_controller):
        """
        Initializes the MainController with references to the main window, app state,
        OCR controller, detection controller, and settings controller.

        Sets up view references, connects signals, and loads initial settings.
        """
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
        self.wired = False

        self.connect_views()
        self.settings_controller.load_settings()  # Apply initial theme

    def connect_views(self):
        """
        Connects UI signals to their respective slots and controller methods.

        Handles navigation between views and connects OCR/detection signals to result handlers.
        """
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
        """
        Applies and saves the selected settings, such as background color and theme.
        """
        self.settings_controller.save_settings(bg_color)
        self.settings_controller.apply_styles()

    def on_analyze_click(self):
        """
        Handles the analyze button click event.

        Determines whether to analyze text or image, runs OCR if needed, and starts detection.
        Shows appropriate popups for missing input.
        """
        print("[analyze] clicked")
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
        """
        Handles direct text submission for analysis.

        Updates app state and triggers detection if text is provided.
        """
        self.app_state.message_text = text or ""
        self.app_state.image_path = None
        if text:
            self.run_detection(text)

    def handle_image_submission(self, path: str):
        """
        Handles image submission for OCR and analysis.

        Updates app state, shows analyzing popup, and starts OCR process.
        """
        self.app_state.image_path = path
        self._last_image_path = path
        self.app_state.message_text = ""
        self.show_analyzing_popup()
        self.ocr_controller.run_ocr(path)

    def on_ocr_completed(self, extracted_text: str):
        """
        Handles completion of OCR process.

        If text is extracted, runs detection; otherwise, shows an error popup.
        """
        if not extracted_text.strip():
            self._close_analyzing()
            self.show_result_popup("Couldn’t read any text from the image.")
            return
        self.app_state.message_text = extracted_text
        self.run_detection(extracted_text)

    def run_detection(self, text: str):
        """
        Initiates the detection process on the provided text.

        Shows analyzing popup if not already visible and starts detection.
        """
        if not getattr(self, "_analyzing", None):  # keep spinner if already shown by OCR
            self.show_analyzing_popup()
        self.detection_controller.analyze_text(text)

    def on_detection_result(self, label, score, phrases):
        """
        Handles the result of the detection process.

        Interprets the result, applies intensity filter, and displays a summary popup.
        """
        print("[detect] clicked")
        REASONS = {
            "ask_send_pic":     "Requested personal images",
            "ask_nudes_short":  "Requested NSFW explicit images",
            "explicit_terms":   "Use of NSFW explicit terms",
            "coercion":         "Coercive or pressuring language",
            "over_persistence": "Excessive persistence",
            "flirt":            "Unsolicited advances",
        }

        self._close_analyzing()

        if not self.detection_controller.apply_intensity_filter(label, score, phrases):
            self.show_result_popup("No issues detected under current filter.")
            return

        thresh = self.detection_controller._threshold_for_intensity()
        display_label = "Inappropriate/Unsafe message" if score >= thresh else "Normal"

        human = [REASONS.get(p, p) for p in (phrases or [])]
        summary = f"Label: {display_label}\nScore: {score:.2f}\n"
        if human:
            summary += "Matched: " + ", ".join(human)
        self.show_result_popup(summary)


        # Gate on intensity threshold
        if not self.detection_controller.apply_intensity_filter(label, score, phrases):
            self.show_result_popup("No issues detected under current filter.")
            return

        # Compute the label to DISPLAY using the active intensity’s threshold
        thresh = self.detection_controller._threshold_for_intensity()
        display_label = "Creepy" if score >= thresh else "Normal"

        summary = f"Label: {display_label}\nScore: {score:.2f}\n"
        if phrases:
            summary += "Matched: " + ", ".join(phrases)
        self.show_result_popup(summary)

    def on_error(self, message: str):
        """
        Handles errors from OCR or detection processes.

        Closes analyzing popup and displays an error message.
        """
        self._close_analyzing()
        self.show_result_popup(f"Error: {message}")

    def show_analyzing_popup(self):
        """
        Displays the analyzing popup to indicate processing is in progress.
        """
        self._analyzing = AnalyzingPopup(self.main_window)
        self._analyzing.show()

    def _close_analyzing(self):
        """
        Closes the analyzing popup if it is currently shown.
        """
        if getattr(self, "_analyzing", None):
            try:
                self._analyzing.reject()
            except Exception:
                pass
            self._analyzing = None

    def show_result_popup(self, result_text, score=None, phrases=None):
        """
        Displays the result popup with the provided result text and optional details.
        """
        dlg = ResultPopup(result_text, self.main_window)
        dlg.exec()

    def _on_filter_back(self):
        """
        Handles returning from the filter view.

        Updates the app state's intensity setting and navigates back to the main view.
        """
        chosen = (self.filter_view.get_selected_intensity() or "easy").strip().lower()
        self.app_state.intensity = chosen
        self.stacked_widget.setCurrentWidget(self.main_window.main_view)
