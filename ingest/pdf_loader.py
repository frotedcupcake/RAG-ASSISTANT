from pypdf import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({
            "page": i + 1,
            "text": text.strip()
        })

    return pages
