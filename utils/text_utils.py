import re
import unicodedata

HOMO_MAP = str.maketrans({
    'А':'A','В':'B','Е':'E','К':'K','М':'M','Н':'H','О':'O','Р':'P','С':'S','Т':'T','Х':'X','Ь':'b',
    'а':'a','е':'e','о':'o','р':'p','с':'s','у':'y','х':'x',
    'Ι':'I','Ο':'O','Ρ':'P','Χ':'X','Υ':'Y','Ζ':'Z','Ν':'N','Κ':'K','Η':'H','Μ':'M',
    'ι':'i','ο':'o','ρ':'p','χ':'x','υ':'y','ν':'v','κ':'k','η':'n','μ':'m',
})

EMOJI_ALIAS = {
    '🍑':'butt','🍆':'cock','👅':'tongue','💦':'cum','😘':'kiss','😈':'horny','🔥':'hot','💋':'kiss',
}

def fold_unicode_homoglyphs(s: str) -> str:
    if not s:
        return s
    s = unicodedata.normalize('NFKC', s)
    s = s.translate(HOMO_MAP)
    for e, alias in EMOJI_ALIAS.items():
        s = s.replace(e, f" {alias} ")
    return re.sub(r"\s+", " ", s).strip()

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