import base64
import io
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_bytes
import pymupdf  # PyMuPDF
from PIL import Image
from paddleocr import PaddleOCR
import numpy as np

import subprocess


def get_poppler_path():
    try:
        # Run the `which` command to find the path of Poppler's `pdfinfo`
        poppler_path = subprocess.check_output(["which", "pdfinfo"]).decode().strip()
        return poppler_path
    except subprocess.CalledProcessError:
        return None


def _paddle_ocr(file_content, filename):
    ocr = PaddleOCR(use_angle_cls=True, lang="pt")
    text = []
    if filename.lower().endswith(".pdf"):
        document = pymupdf.open(stream=file_content, filetype="pdf")
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_np = np.array(img)
            result = ocr.ocr(img_np, cls=True)
            for line in result:
                for word in line:
                    text.append(word[1][0])
        document.close()
    elif filename.lower().endswith((".png", ".jpeg", ".jpg")):
        img = Image.open(io.BytesIO(file_content)).convert("RGB")
        img_np = np.array(img)
        result = ocr.ocr(img_np, cls=True)
        print("REsult", result)
        for line in result:
            for word in line:
                text.append(word[1][0])

    return "\n\n".join(text)


def image_to_base64(file):

    # Read the file content
    file_content = file.read()
    # Perform OCR using PaddleOCR

    filename = file.name
    text_paddle_ocr = _paddle_ocr(file_content, filename)

    content_type = (
        "application/pdf" if filename.lower().endswith(".pdf") else "application/jpeg"
    )
    #    text_paddle_ocr = use_paddle_ocr(file_content, content_type)
    img_png = None
    poppler_path = get_poppler_path()
    print(poppler_path)

    if poppler_path:
        poppler_path = poppler_path.rsplit("/", 1)[0]
    # Process the file based on its type
    if content_type == "application/pdf":
        # Convert PDF to PNG
        images = convert_from_bytes(
            file_content, poppler_path=poppler_path, grayscale=True
        )
        widths, heights = zip(*(i.size for i in images))

        total_width = max(widths)
        total_height = sum(heights)

        concatenated_image = Image.new("RGB", (total_width, total_height))

        y_offset = 0
        for img in images:
            concatenated_image.paste(img, (0, y_offset))
            y_offset += img.height

        img_byte_arr = io.BytesIO()
        concatenated_image.save(img_byte_arr, format="PNG")
        img_png = concatenated_image.copy()
        processed_content = img_byte_arr.getvalue()
        filename = filename.rsplit(".", 1)[0] + ".png"
    elif content_type == "application/jpeg":
        with Image.open(io.BytesIO(file_content)) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            img_png = img.copy()
            processed_content = img_byte_arr.getvalue()

    else:
        # Leave other file types as they are
        processed_content = file_content

    # Encode the processed content to base64
    base64_content = base64.b64encode(processed_content).decode("utf-8")

    if text_paddle_ocr:
        with open("text_paddle_ocr.txt", "w") as paddle_ocr_file:
            paddle_ocr_file.write(text_paddle_ocr)
    return base64_content, img_png, text_paddle_ocr


def merge_data(values):
    data = []
    for idx in range(len(values)):
        data.append(values[idx][1][0])
    return data


def base64_to_png(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    with open("output.png", "wb") as image_file:
        image_file.write(image_data)
    return image
