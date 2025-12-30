from docx import Document

def load_docx(path):
    doc = Document(path)
    paragraphs = []

    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            paragraphs.append(text)

    return paragraphs

