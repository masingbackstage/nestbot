from sqlalchemy.orm import Session

from config import settings
from domain import MemoryType
from models import Memory
from repositories import UserRepository, MemoryRepository
from services.embedding import EmbeddingService


class MemoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(self.db)
        self.memory_repository = MemoryRepository(self.db)
        self.embedding_service = EmbeddingService(settings.embedding_model)

    def remember(
        self,
        *,
        external_ref: str,
        memory_type: str | MemoryType,
        content: str,
        display_name: str | None = None,
        summary: str | None = None,
        confidence: float = 1.0,
        source: str | None = None,
        source_message_id: str | None = None,
    ) -> Memory:
        try:

            user, _ = self.user_repository.get_or_create_by_external_ref(
                external_ref=external_ref,
                display_name=display_name,
            )

            normalized_memory_type = self._normalize_memory_type(memory_type)

            duplicate = self._find_duplicate_memory(
                user_id=user.id,
                memory_type=normalized_memory_type,
                content=content,
            )

            if duplicate is not None:
                return duplicate

            text_for_embedding = summary or content
            embedding = self.embedding_service.embed_text(text_for_embedding)

            memory = self.memory_repository.create(
                user_id=user.id,
                memory_type=normalized_memory_type,
                content=content,
                summary=summary,
                confidence=confidence,
                source=source,
                source_message_id=source_message_id,
                embedding=embedding,
            )

            self.db.commit()
            self.db.refresh(memory)

            return memory
        except Exception:
            self.db.rollback()
            raise

    def list_memories(self, *, external_ref: str) -> list[Memory]:
        user = self.user_repository.get_by_external_ref(external_ref)
        if user is None:
            return []

        return self.memory_repository.list_active_for_user(user.id)

    def _find_duplicate_memory(
        self,
        *,
        user_id,
        memory_type: MemoryType,
        content: str,
    ):
        normalized_new = self._normalize_text(content)
        existing_memories = self.memory_repository.list_active_for_user_by_type(
            user_id=user_id,
            memory_type=memory_type,
        )

        for memory in existing_memories:
            normalized_existing = self._normalize_text(memory.content)
            if normalized_existing == normalized_new:
                return memory

        return None

    @staticmethod
    def _normalize_memory_type(memory_type: str | MemoryType) -> MemoryType:
        if isinstance(memory_type, MemoryType):
            return memory_type
        try:
            return MemoryType(memory_type)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in MemoryType)
            raise ValueError(
                f"Invalid memory_type='{memory_type}'. Allowed values: {allowed}"
            ) from exc

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(text.strip().lower().split())
