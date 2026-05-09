from sqlalchemy import select
from sqlalchemy.orm import Session

from config import settings
from domain import MemoryType
from models import Memory
from repositories import UserRepository
from services.embedding import EmbeddingService


class MemoryRetrieverService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(self.db)
        self.embedding_service = EmbeddingService(settings.embedding_model)

    def search(
        self,
        *,
        external_ref: str,
        query: str,
        k: int = 5,
        memory_types: list[MemoryType] | None = None,
    ) -> list[Memory]:
        user = self.user_repository.get_by_external_ref(external_ref)
        if user is None:
            return []

        query_embedding = self.embedding_service.embed_text(query)

        stmt = (
            select(Memory)
            .where(Memory.user_id == user.id)
            .where(Memory.is_active.is_(True))
            .where(Memory.embedding.is_not(None))
        )

        if memory_types:
            stmt = stmt.where(Memory.memory_type.in_(memory_types))

        stmt = stmt.order_by(Memory.embedding.cosine_distance(query_embedding)).limit(k)

        return list(self.db.execute(stmt).scalars().all())
