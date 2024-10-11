import pymupdf
import pymupdf4llm
import io


class PdfTextExtactor:
    @classmethod
    def extract_text_from_pdf(cls, conteudo):
        # Open the PDF file
        pdf_stream = io.BytesIO(conteudo)
        pdf_doc = pymupdf.open(stream=pdf_stream, filetype="pdf")
        pdf_document = pymupdf4llm.to_markdown(pdf_doc)
        # pathlib.Path(f"{pdf_path}.txt").write_bytes(pdf_document.encode())
        return pdf_document
