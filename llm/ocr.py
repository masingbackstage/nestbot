import logging

import ollama


from config import settings
from prompts import VISION_PROMPT

logger = logging.getLogger(__name__)


class OCRProvider:
    def __init__(self):
        self.model = settings.llm_vision_model
        self.client = ollama.Client(host=settings.llm_base_url)

    def extract_text(self, image_bytes: bytes) -> str:
        logger.info(f"Image size: {len(image_bytes)} bytes")

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": VISION_PROMPT,
                    "images": [image_bytes],
                }
            ],
        )

        content = response.message.content
        logger.info(f"OCR raw response: {repr(content)}")
        return content
