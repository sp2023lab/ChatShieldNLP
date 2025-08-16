# models/detection_model.py
from __future__ import annotations
import re
from typing import List, Tuple, Dict

from utils.text_utils import normalize_text  # keep using your shared normalizer

def _despace_and_deleet(s: str) -> str:
    if not s:
        return s
    # IMPORTANT: do NOT include \s here; we only remove . _ - between letters
    s = re.sub(r'(?<=\w)[\.\-_]+(?=\w)', '', s)

    # leetspeak mapping
    s = s.translate(str.maketrans({
        '0':'o','3':'e','4':'a','1':'i','5':'s','7':'t','!':'i','@':'a','$':'s'
    }))

    # collapse 3+ repeats to 2 (plzzzz -> plzz)
    s = re.sub(r'(.)\1{2,}', r'\1\1', s)

    return s

# Canonical name -> (compiled regex, weight)
RX: Dict[str, Tuple[re.Pattern, float]] = {}

def _compile_patterns() -> None:
    """Build regex library with flexible gaps."""
    global RX
    flags = re.IGNORECASE | re.DOTALL | re.VERBOSE

    def C(p: str) -> re.Pattern:
        return re.compile(p, flags)

    # Up to 3 filler tokens between verb and media word: (?:\s+\w+){0,3}?
    RX = {
        # Sexual requests (high)
        "ask_send_pic": (C(r"""
            \b(?:send|share|show)\b
            (?:.{0,40}?)                             # allow up to ~40 chars of anything (incl. 'me ur', emojis, punctuation)
            \b(?:pic|pics|picture|pictures|photo|photos|image|images|selfie|selfies|nude|nudes)\b
        """), 0.55),

        "ask_nudes_short": (C(r"""
            \bsend(?:\s+\w+){0,2}?\s+\b(nude|nudes)\b
        """), 0.55),

        # Explicit sexual terms (med-high)
        "explicit_terms": (C(r"""
            \b(boobs?|bobs|tits?|nipple|vegana|vagina|horny|hard|sexy)\b
        """), 0.45),

        # Coercion / persistence (medium)
        "coercion": (C(r"""
            \b(please\s+don'?t\s+ignore\s+me|you\s+don'?t\s+love\s+me\??|just\s+one\s+picture\s+please)\b
        """), 0.35),

        "over_persistence": (C(r"""
            \b(i\s*(?:am|'?m)\s*lonely|please\s*talk\s*to\s*me|can\s*i\s*be\s*your\s*friend)\b
        """), 0.35),

        # Flirt / romantic openers (lower)
        "flirt": (C(r"""
            \b(hi\s*dear|hi\s*beautiful|hey\s*(?:baby|babe))\b
        """), 0.25),
    }

# compile at import
_compile_patterns()

class DetectionModel:
    def __init__(self, confidence_threshold: float = 0.70):
        self.confidence_threshold = float(confidence_threshold)

    def _preprocess(self, text: str) -> str:
        t0 = text
        t = normalize_text(text)          # step 1: lowercase, collapse whitespace, keep spaces
        t = _despace_and_deleet(t)         # step 2: de-leet, remove separators inside tokens
        print("PRE:", repr(t0), "\nPOST:", repr(t))  # <-- add this debug here
        return t

    def _score_text(self, t: str) -> Tuple[float, List[str]]:
        print("RX size:", len(RX), "text:", t)
        score = 0.0
        matched: List[str] = []
        for name, (pat, weight) in RX.items():
            if pat.search(t):
                print(f"Matched: {name} with weight {weight} in text: {t}")
                matched.append(name)
                score += weight
        print(f"Score for '{t}': {score}, matched: {matched}")
        return min(1.0, score), matched

    def get_result(self, text: str):
        if not text or not text.strip():
            return "Normal", 0.0, []

        lines = [ln.strip() for ln in text.splitlines() if ln.strip()] or [text]
        best_score = 0.0
        best_matches: List[str] = []

        for ln in lines:
            t = self._preprocess(ln)
            sc, names = self._score_text(t)
            if sc > best_score:
                best_score, best_matches = sc, names

        label = "Creepy" if best_score >= self.confidence_threshold else "Normal"
        return label, best_score, best_matches
