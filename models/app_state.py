
from time import time
from collections import deque

class AppState:

    def __init__(self):
        self.intensity = "easy"
        self.message_text = ""
        self.image_path = None
        # NEW: track recent scores for conversation-level accumulation
        self.recent_scores = deque(maxlen=8)  # keep last 8 messages (t, score)

    # NEW:
    def add_score(self, score: float):
        self.recent_scores.append((time(), float(score)))

    # NEW:
    def rolling_score(self, horizon_sec: int = 600) -> float:
        now = time()
        return sum(s for ts, s in self.recent_scores if now - ts <= horizon_sec)