import io

import easyocr
import numpy
from PIL import Image

class OCRProvider:
    def __init__(self):
        self.reader = easyocr.Reader(["pl", "en"], gpu=False)

    def extract_text(self, image_bytes: bytes) -> str:
        img = numpy.array(Image.open(io.BytesIO(image_bytes)))
        results = self.reader.readtext(img, detail=0, paragraph=True)
        return "\n".join(results)
