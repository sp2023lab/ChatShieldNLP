# detection_model.py
import re
from utils.text_utils import normalize_text

LOW = {
    "send nudes","send me your pic","please send","show me your",
    "bobs","vegana", "vagina","boobs","tits","nipple","tight dress",
    "you look sexy","i'm horny","i’m hard","i want to see you",
    "i want to touch you","big bobs","u r sexy","kiss me","wet pic",
    "send nude", "send me pic", "send me your pics", "send me pics",
    "show me"
}

MED = {
    "hi dear","hi beautiful","you are so hot","you are sexy",
    "can i be your friend","i want to talk to you","i’m lonely",
    "please talk to me","please don’t ignore me","you’re my dream girl",
    "just one picture please","you don’t love me?","hey baby"
}

class DetectionModel:
    def __init__(self, confidence_threshold=0.70):
        self.confidence_threshold = confidence_threshold

    def get_result(self, text: str):
        t = normalize_text(text)
        low = [p for p in LOW if p in t]
        med = [p for p in MED if p in t]

        if med:
            return "Creepy", 0.75, med
        if len(low) >= 2:
            return "Creepy", 0.70, low
        return "Normal", 0.30, []
