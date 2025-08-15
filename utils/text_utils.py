import re

def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = " ".join(text.split())
    text = text.strip()
    print(f"Here is the text {text}")
    return text

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