# models/detection_model.py
from __future__ import annotations
import re
from typing import List, Tuple, Dict

from utils.text_utils import normalize_text, fold_unicode_homoglyphs  # keep using your shared normalizer

def _despace_and_deleet(s: str) -> str:
    if not s:
        return s
    # remove . _ - inside words only (keep spaces!)
    s = re.sub(r'(?<=\w)[\.\-_]+(?=\w)', '', s)

    # leetspeak mapping — IMPORTANT: no '!' -> 'i' here
    s = s.translate(str.maketrans({
        '0':'o','3':'e','4':'a','1':'i','5':'s','7':'t','@':'a','$':'s'
    }))

    # collapse 3+ repeats to 2 (plzzzz -> plzz)
    s = re.sub(r'(.)\1{2,}', r'\1\1', s)

    # strip trailing punctuation that can break word boundaries after media words
    # e.g., "pic!!!" -> "pic", "photo??" -> "photo"
    s = re.sub(r'([a-z])([!?.,;:]+)(?=\s|$)', r'\1', s, flags=re.IGNORECASE)

    # --- lightweight typo fixes (additions) ---
    # 'nakd' / 'nakde' -> 'naked'
    s = re.sub(r"\bnakd[e]?\b", "naked", s, flags=re.IGNORECASE)
    # common OCR: 'snow you' -> 'now you'
    s = re.sub(r"\bsnow\s+you\b", "now you", s, flags=re.IGNORECASE)

    return s


# Canonical name -> (compiled regex, weight)
RX: Dict[str, Tuple[re.Pattern, float]] = {}

def fuzzy_letters(word: str, gap: str = r'[\W_]*', case_insensitive: bool = True) -> str:
    parts = list(word)
    return gap.join(map(re.escape, parts))


def _compile_patterns() -> None:
    """Build regex library with flexible gaps."""
    global RX
    flags = re.IGNORECASE | re.DOTALL | re.VERBOSE

    def C(p: str) -> re.Pattern:
        return re.compile(p, flags)

    critical_terms = ['nude', 'nudes', 'pic', 'pics', 'pussy', 'cock', 'boobs', 'tits']
    fuzzy_alts = "|".join(fuzzy_letters(w) for w in critical_terms)


    # Up to 3 filler tokens between verb and media word: (?:\s+\w+){0,3}?
    RX = {
        # --- existing patterns (keep) ---
        "ask_send_pic": (C(r"""
            \b(?:send|share|show)\b
            (?:.{0,40}?)
            \b(?:pic|pics|picture|pictures|photo|photos|image|images|selfie|selfies|nude|nudes)\b
        """), 0.55),

        "ask_nudes_short": (C(r"""
            \bsend(?:\s+\w+){0,3}?\s+\b(nude|nudes|naked|nakde|nakd)\b
        """), 0.55),

        "fuzzy_critical": (C(fr"\b(?:{fuzzy_alts})\b"), 0.40),


        # Expanded explicit vocabulary (fires per-occur; see step 2)
        "explicit_terms": (C(r"""
            \b(
                boobs?|bobs|b00bs|tits?|t1ts|t!ts|nipple[s]?|nipples|
                pussy|pusy|pussi|p\*ssy|vagina|vegana|clit|
                cock|c0ck|dick|d1ck|penis|
                horny|hard|sexy|moan(?:s|ing)?|
                suck|lick|finger(?:ing)?|cum|c\*m|
                blowjob|bl0wjob|bj|anal|fuck(?:ing)?
            )\b
        """), 0.45),


        # NEW: sexual size inquiry
        "size_inquiry": (C(r"""
            \bhow\s+big\s+is\s+(?:your|ur)\s+(?:pussy|boobs?|tits?|dick|cock)\b
        """), 0.45),

        # NEW: abuse/insults
        "abuse_terms": (C(r"""
            \b(bitch|slut|whore|cunt)\b
        """), 0.30),

        # Keep your existing coercion/over_persistence/flirt
        "coercion": (C(r"""
            \b(please\s+don'?t\s+ignore\s+me|you\s+don'?t\s+love\s+me\??|just\s+one\s+picture\s+please)\b
        """), 0.35),

        "over_persistence": (C(r"""
            \b(i\s*(?:am|'?m)\s*lonely|please\s*talk\s*to\s*me|can\s*i\s*be\s*your\s*friend)\b
        """), 0.35),

        "flirt": (C(r"""
            \b(hi\s*dear|hi\s*beautiful|hey\s*(?:baby|babe))\b
        """), 0.25),

        "harassment_threats": (C(r"""
            \b(
                kill \s* yourself   |  # "kill yourself", "killyourself", "k y s" handled below
                k \s* y \s* s       |  # "kys" with optional spaces
                i'?m \s+ going \s+ to \s+ kill \s+ you |
                i \s* '?\s* ll \s+ (?:find|hunt) \s+ you |
                rape \s+ you
            )\b
        """), 0.60),

        "harassment_dox_stalk": (C(r"""
            \b(
                i \s+ know \s+ where \s+ you \s+ live |
                (?:send|share) \s+ (?:your\s+)? (?:address|location) |
                what \s+ is \s+ your \s+ address
            )\b
        """), 0.45),

        "harassment_insults": (C(r"""
            \b(bitch|slut|whore|cunt|skank|hoe|bastard|scum|trash)\b
        """), 0.0),  # keep 0.0 so only COUNTED applies

        "grooming_age": (C(r"""
            \b(how\s+old\s+are\s+you|age\??|are\s+you\s+(?:mature|legal)|what'?s\s+your\s+age)\b
        """), 0.45),

        "grooming_parents": (C(r"""
            \b(parents?\s+(?:home|there)|are\s+you\s+(?:alone|by\s+yourself))\b
        """), 0.45),

        "grooming_move_dm": (C(r"""
            \b(add\s+me\s+on\s+(?:snap|snapchat|telegram|whatsapp)|dm\s+me\s+privately|private\s+chat)\b
        """), 0.30),

        "grooming_show_face": (C(r"""
            \b(show\s+(?:your|ur)\s+face|face\s+reveal|turn\s+on\s+camera|cam\s+on)\b
        """), 0.35),

    }

# compile at import
_compile_patterns()

COUNTED = {
    # pattern_name: (per_hit_weight, cap_for_this_pattern)
    "explicit_terms": (0.12, 0.84),   # ~7 explicit terms to reach 0.84
    "abuse_terms":    (0.20, 0.40),   # two insults max out at 0.40
}

class DetectionModel:
    def __init__(self, confidence_threshold: float = 0.45):
        self.confidence_threshold = float(confidence_threshold)

    def _preprocess(self, text: str) -> str:
        t0 = text
        t = fold_unicode_homoglyphs(text)
        t = normalize_text(t)          # step 1: lowercase, collapse whitespace, keep spaces
        t = _despace_and_deleet(t)         # step 2: de-leet, remove separators inside tokens
        print("PRE:", repr(t0), "\nPOST:", repr(t))  # <-- add this debug here
        return t

    def _score_text(self, t: str) -> Tuple[float, List[str]]:
        score = 0.0
        matched: List[str] = []
        for name, (pat, weight) in RX.items():
            if name in COUNTED:
                per_hit, cap = COUNTED[name]
                hits = pat.findall(t)
                if hits:
                    matched.append(name)
                    inc = min(cap, per_hit * len(hits))
                    print(f"[COUNTED] {name}: hits={len(hits)} per={per_hit} cap={cap} +{inc:.2f}")
                    score += inc
            else:
                if pat.search(t):
                    matched.append(name)
                    print(f"[FIXED]   {name}: +{weight:.2f}")
                    score += weight
        print(f"[TOTAL] score={score:.2f} matches={matched}")
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

        label = "Creepy message. Immediately block!" if best_score >= self.confidence_threshold else "Normal"
        return label, best_score, best_matches
