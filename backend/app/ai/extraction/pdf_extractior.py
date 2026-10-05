from pathlib import Path
from pypdf import PdfReader


class PDFExtractor:
    def extract(self, file_path:str) ->str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        reader = PdfReader(path)
        pages_text=[]

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "/n".join(pages_text)        