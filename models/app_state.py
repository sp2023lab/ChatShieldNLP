
from time import time
from collections import deque

class AppState:
    """
    Holds the current application state, including user input, settings, and recent detection scores.

    This class tracks the current detection intensity, message text, image path, and a rolling
    history of recent detection scores for conversation-level analysis. It provides methods to
    add new scores and compute a rolling sum of scores within a specified time horizon.
    """
    def __init__(self):
        """
        Initializes the AppState with default values.

        Sets the default intensity, clears message and image data, and prepares a deque for
        tracking recent detection scores.
        """
        self.intensity = "easy"
        self.message_text = ""
        self.image_path = None
        # NEW: track recent scores for conversation-level accumulation
        self.recent_scores = deque(maxlen=8)  # keep last 8 messages (t, score)

    def add_score(self, score: float):
        """
        Adds a new detection score to the rolling history.

        Stores the current timestamp and score in the recent_scores deque.
        """
        self.recent_scores.append((time(), float(score)))

    def rolling_score(self, horizon_sec: int = 600) -> float:
        """
        Computes the sum of detection scores within the given time horizon (in seconds).

        Returns the total score for all messages detected within the specified recent period.
        """
        now = time()
        return sum(s for ts, s in self.recent_scores if now - ts <= horizon_sec)