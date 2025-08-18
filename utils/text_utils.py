import re
import unicodedata

def normalize_text(text: str) -> str:
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
    normalized = normalize_text(text)
    tokens = normalized.split()
    print(f"Here is the tokens {tokens}")
    return tokens  

def highlight_detected_phrases(text: str, phrases: list[str]) -> str:
    html_string = text
    for phrase in phrases:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        html_string = pattern.sub(lambda m: f"<span style='color:red'>{m.group(0)}</span>", html_string)
    print(f"Here is the HTML string: {html_string}")
    return html_string