import base64
import io
import subprocess
from utils.DocumentTrimmer import DocumentTrimmer
from pdf2image import convert_from_bytes
import numpy as np
import cv2
from PIL import Image


def get_poppler_path():
    try:
        # Run the `which` command to find the path of Poppler's `pdfinfo`
        poppler_path = subprocess.check_output(["which", "pdfinfo"]).decode().strip()
        return poppler_path
    except subprocess.CalledProcessError:
        return None


class FileToBase64:
    def __init__(self, file=None):
        if file is not None:
            self.file = file

    @classmethod
    def get_text_from_pdf(cls,file):
        pass
        
    @classmethod
    def get_base64(cls, file):
        file_content = file.read()
        filename = file.name
        img_png = None
        poppler_path = get_poppler_path()
        print(poppler_path)
        if poppler_path:
            poppler_path = poppler_path.rsplit("/", 1)[0]
        # Process the file based on its type
        processed_content = None
        if filename.lower().endswith(".pdf"):
            # Convert PDF to PNG
            images = convert_from_bytes(
                file_content, poppler_path=poppler_path, grayscale=True, dpi=120
            )
            if len(images) == 1:
                image = images[0]
                image_cv = np.array(image)
                output = DocumentTrimmer.crop_image(image_cv)
                _, buffer = cv2.imencode(".png", output)

                processed_content = buffer.tobytes()

            else:
                all_images = []
                for i, image in enumerate(images):
                    image_cv = np.array(image)

                    output = DocumentTrimmer.crop_image(image_cv)
                    all_images.append(output)
                combined_image = np.vstack(all_images)
                # Convert the combined image to bytes

                _, buffer = cv2.imencode(".png", combined_image)

                processed_content = buffer.tobytes()

        elif filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            # Convert the file content to a numpy array
            file_bytes = np.frombuffer(file_content, np.uint8)
            # Decode the numpy array to an image
            image_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            # Convert the image to grayscale
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            # Process the image using DocumentTrimmer
            output = DocumentTrimmer.crop_image(image_cv)
            # Convert the processed image back to bytes
            _, buffer = cv2.imencode(".png", output )

            processed_content = buffer.tobytes()
            # processed_content = buffer

        # Encode the processed content to base64
        base64_content = base64.b64encode(processed_content).decode("utf-8")
        img_png = FileToBase64.base64_to_png(base64_content)
        return base64_content, img_png

    @classmethod
    def base64_to_png(cls, base64_string):
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        with open("output.png", "wb") as image_file:
            image_file.write(image_data)
        return image
