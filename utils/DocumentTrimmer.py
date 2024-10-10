import numpy as np
import cv2


class DocumentTrimmer:
    def __init__(self, image_path=None, image_as_np_array=None):
        if image_as_np_array is not None:
            self.image = image_as_np_array
        else:
            self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    @classmethod
    def crop_image(cls, image):

        original_height, original_width = image.shape

        # Cortar o rodapé (10% da altura)
        footer_crop_height = int(0.1 * original_height)
        image = image[: original_height - footer_crop_height, :]

        # Inverter a imagem para que o texto fique branco
        inverted_image = cv2.bitwise_not(image)
        _, thresh = cv2.threshold(
            inverted_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # Re-confirmar que há pixels não zero
        assert (
            cv2.countNonZero(thresh) > 0
        ), "A imagem binarizada não contém pixels não zero. Verifique a imagem original."

        # Detectar a área de texto de baixo para cima
        bottom_row = original_height
        for row in range(thresh.shape[0] - 1, -1, -1):
            if cv2.countNonZero(thresh[row, :]) > 0:
                bottom_row = row + 1
                break

        # Detectar a área de texto da direita para a esquerda
        right_col = original_width
        for col in range(thresh.shape[1] - 1, -1, -1):
            if cv2.countNonZero(thresh[:, col]) > 0:
                right_col = col + 1
                break

        # Detectar a área de texto da esquerda para a direita
        left_col = 0
        for col in range(thresh.shape[1]):
            if cv2.countNonZero(thresh[:, col]) > 0:
                left_col = col
                break
        # Detectar a área de texto de cima para baixo
        top_row = 0
        for row in range(thresh.shape[0]):
            if cv2.countNonZero(thresh[row, :]) > 0:
                top_row = row
                break

        # Cortar a imagem mantendo apenas as áreas com texto
        # Adicionar uma margem de 3px em todos os lados
        top_row = max(0, top_row - 3)
        bottom_row = min(original_height, bottom_row + 3)
        left_col = max(0, left_col - 3)
        right_col = min(original_width, right_col + 3)

        cropped_image = image[top_row:bottom_row, left_col:right_col]

        return cropped_image
