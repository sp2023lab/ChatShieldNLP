import re

def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = " ".join(text.split())
    text = text.strip()
    return text

def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    tokens = normalized.split()
    return tokens  

def highlight_detected_phrases(text: str, phrases: list[str]) -> str:
    html_string = text
    for phrase in phrases:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        html_string = pattern.sub(lambda m: f"<span style='color:red'>{m.group(0)}</span>", html_string)
    return html_string