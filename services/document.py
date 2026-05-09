import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session

from domain import MemoryType
from llm import OCRProvider
from services.memory import MemoryService

logger = logging.getLogger(__name__)


class DocumentService:

    def __init__(self, db: Session) -> None:
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=75)
        self.ocr = OCRProvider()
        self.memory_service = MemoryService(db)

    def ingest_pdf(self, path: str, source: str) -> list[str]:
        loader = PyPDFLoader(path)
        docs = loader.load()
        chunks = self.splitter.split_documents(docs)
        return [c.page_content for c in chunks]

    def ingest_image(self, image_bytes: bytes) -> list[str]:
        text = self.ocr.extract_text(image_bytes)
        logger.info(f"OCR text length: {len(text) if text else 0}")
        chunks = self.splitter.split_text(text)
        logger.info(f"OCR chunks: {len(chunks)}")
        return chunks

    def save_chunks(
        self,
        *,
        external_ref: str,
        chunks: list[str],
        source: str,
        display_name: str | None = None,
    ) -> int:
        saved = 0
        user, _ = self.memory_service.user_repository.get_or_create_by_external_ref(
            external_ref=external_ref,
            display_name=display_name,
        )
        for chunk in chunks:
            self.memory_service.remember(
                external_ref=external_ref,
                memory_type=MemoryType.DOCUMENT,
                content=chunk,
                source=source,
                display_name=display_name,
            )
            saved += 1
        return saved
