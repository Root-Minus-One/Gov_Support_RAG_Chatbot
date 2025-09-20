from pypdf import PdfReader
from typing import List





def extract_text(file):
    extract = PdfReader(file)
    text = ''

    for page in extract.pages:
        text = text + page.extract_text() or ''
        return text
    
