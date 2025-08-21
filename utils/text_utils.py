import re
import unicodedata

def normalize_text(text: str) -> str:
    """
    Normalizes input text for consistent processing.

    Converts text to lowercase, applies Unicode NFKC normalization, replaces curly quotes with ASCII,
    removes control characters (except whitespace), and collapses whitespace runs to a single space.
    Returns the cleaned and trimmed string.
    """
    if not text:
        return ""
    # lower + NFKC
    t = unicodedata.normalize("NFKC", text).lower()

    # map curly apostrophes etc. to plain ascii (helps your “don’t” cases)
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')

    # remove control chars except whitespace
    t = re.sub(r"[^\S\r\n\t ]", "", t)  # keep spaces/tabs/newlines

    # collapse any whitespace runs to a single space, keep spaces!
    t = re.sub(r"\s+", " ", t)

    return t.strip()

def tokenize(text: str) -> list[str]:
    """
    Tokenizes normalized text into a list of words.

    Normalizes the input text, splits it by whitespace, and returns the resulting list of tokens.
    """
    normalized = normalize_text(text)
    tokens = normalized.split()
    print(f"Here is the tokens {tokens}")
    return tokens  

def highlight_detected_phrases(text: str, phrases: list[str]) -> str:
    """
    Highlights detected phrases in the input text using HTML span tags.

    Wraps each detected phrase in a red-colored span for display in rich text widgets.
    Returns the resulting HTML string.
    """
    html_string = text
    for phrase in phrases:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        html_string = pattern.sub(lambda m: f"<span style='color:red'>{m.group(0)}</span>", html_string)
    print(f"Here is the HTML string: {html_string}")
    return html_string