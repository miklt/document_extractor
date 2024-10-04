import pymupdf  # PyMuPDF
import itertools
from PIL import Image
import pytesseract
from paddleocr import PaddleOCR


class TextExtractor:
    def __init__(self, file, content_type):
        self.file = file
        self.content_type = content_type

    def use_pymupdf_text_extraction(self):
        if self.content_type != "application/pdf":
            return "Invalid file type. Only PDF files are accepted."
        text = []
        document = pymupdf.open(stream=self.file, filetype="pdf")
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            tabs = page.find_tables(strategy="text")

            if len(tabs.tables) == []:
                break
            for t in tabs.tables:
                text.append(t.to_markdown())
        document.close()

        flattened_text = list(
            itertools.chain.from_iterable(
                item if isinstance(item, list) else [item] for item in text
            )
        )
        return "\n\n".join(flattened_text)

    def use_ocr_text_extraction(self):
        if self.content_type != "application/pdf":
            return "Invalid file type. Only PDF files are accepted."
        text = []
        document = pymupdf.open(stream=self.file, filetype="pdf")
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text.append(pytesseract.image_to_string(img, lang="por"))
        document.close()
        return "\n\n".join(text)

    
