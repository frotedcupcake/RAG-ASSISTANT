from pipeline.index_documents import index_pdf
import os

DOCS_DIR = "docs"

for f in os.listdir(DOCS_DIR):
    if f.endswith(".pdf"):
        index_pdf(os.path.join(DOCS_DIR, f))
