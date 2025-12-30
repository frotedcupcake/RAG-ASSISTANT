import re

def clean_text(text):
    text = text.replace("\u00a0", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
