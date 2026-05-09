from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain import MemoryType
from models import Memory


class MemoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: UUID,
        memory_type: MemoryType,
        content: str,
        summary: str | None = None,
        confidence: float = 1.0,
        source: str | None = None,
        source_message_id: str | None = None,
        embedding: list[float] | None = None,
    ) -> Memory:
        memory = Memory(
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            summary=summary,
            confidence=confidence,
            source=source,
            source_message_id=source_message_id,
            embedding=embedding,
        )
        self.db.add(memory)
        self.db.flush()
        return memory

    def list_active_for_user(self, user_id: UUID) -> list[Memory]:
        stmt = (
            select(Memory)
            .where(Memory.user_id == user_id)
            .where(Memory.is_active.is_(True))
            .order_by(Memory.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def list_active_for_user_by_type(
        self,
        user_id: UUID,
        memory_type: MemoryType,
    ) -> list[Memory]:
        stmt = (
            select(Memory)
            .where(Memory.user_id == user_id)
            .where(Memory.memory_type == memory_type)
            .where(Memory.is_active.is_(True))
            .order_by(Memory.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def deactivate(self, memory: Memory) -> Memory:
        memory.is_active = False
        self.db.add(memory)
        self.db.flush()
        return memory
