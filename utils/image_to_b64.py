import logging

import base64
import io
import json
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_bytes


def image_to_base64(file):
    logging.info("Python HTTP trigger function processed a request.")

    # Get the file from the request

    # Read the file content
    file_content = file.read()
    filename = file.name
    img_png = None
    # Process the file based on its type
    if filename.lower().endswith(".pdf"):
        # Convert PDF to PNG
        images = convert_from_bytes(file_content, poppler_path="poppler-utils\\usr\\bin")
        img_byte_arr = io.BytesIO()
        images[0].save(img_byte_arr, format="PNG")
        img_png = images[0].copy()
        processed_content = img_byte_arr.getvalue()
        filename = filename.rsplit(".", 1)[0] + ".png"
    elif filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        # Resize the image to a maximum of 1024x1024 while maintaining aspect ratio
        with Image.open(io.BytesIO(file_content)) as img:
            # img.thumbnail((1024, 1024))
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
