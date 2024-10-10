import logging

import base64
import io
import json
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_bytes

import subprocess


def get_poppler_path():
    try:
        # Run the `which` command to find the path of Poppler's `pdfinfo`
        poppler_path = subprocess.check_output(["which", "pdfinfo"]).decode().strip()
        return poppler_path
    except subprocess.CalledProcessError:
        return None




def image_to_base64(file):
    # Read the file content
    file_content = file.read()
    filename = file.name
    img_png = None
    poppler_path = get_poppler_path()
    print(poppler_path)
    if poppler_path:
        poppler_path = poppler_path.rsplit("/", 1)[0]
    # Process the file based on its type
    if filename.lower().endswith(".pdf"):
        # Convert PDF to PNG
        images = convert_from_bytes(
            file_content, poppler_path=poppler_path, grayscale=True, dpi=100
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
    elif filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
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

    return base64_content, img_png


def base64_to_png(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    with open("output.png", "wb") as image_file:
        image_file.write(image_data)
    return image
