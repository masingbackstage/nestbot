import logging
from typing import Any

from sqlalchemy.orm import Session

from domain import MemoryType
from llm import LLMProvider, FactExtractor
from models import Memory
from services import MemoryService, MemoryRetrieverService

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.memory_service = MemoryService(self.db)
        self.retriever_service = MemoryRetrieverService(self.db)
        self.llm_provider = LLMProvider()
        self.extractor = FactExtractor()

    @staticmethod
    def _ref(telegram_id: str) -> str:
        return f"telegram:{telegram_id}"

    async def respond(
        self,
        *,
        telegram_id: str,
        display_name: str,
        query: str,
    ) -> str | list[Any]:
        ref = self._ref(telegram_id)

        facts = self.retriever_service.search(
            external_ref=ref,
            query=query,
            k=5,
            memory_types=[MemoryType.PROFILE],
        )

        docs = self.retriever_service.search(
            external_ref=ref,
            query=query,
            k=10,
            memory_types=[MemoryType.DOCUMENT],
        )

        context_parts = []
        if facts:
            context_parts.append(
                "Fakty o użytkowniku:\n" + "\n".join(f"- {m.content}" for m in facts)
            )
        if docs:
            context_parts.append(
                "Dokumenty:\n" + "\n".join(f"- [{m.source}] {m.content}" for m in docs)
            )

        context = "\n\n".join(context_parts) or "Brak wcześniejszych wspomnień."

        response = await self.llm_provider.chat(context=context, query=query)

        await self._save_facts(
            ref=ref,
            display_name=display_name,
            query=query,
            response=response,
        )

        return response

    async def _save_facts(
        self,
        *,
        ref: str,
        display_name: str,
        query: str,
        response: str,
    ) -> None:
        try:
            facts = await self.extractor.extract(query=query)
            logger.info(f"Facts extracted ({len(facts)}): {facts}")
            for fact in facts:
                self.memory_service.remember(
                    external_ref=ref,
                    display_name=display_name,
                    memory_type=MemoryType.PROFILE,
                    content=fact["content"],
                    summary=fact.get("summary"),
                    confidence=fact.get("confidence", 0.8),
                    source="telegram_chat",
                )
        except Exception as e:
            logger.warning(f"Failed to save facts: {e}")

    def list_memories(self, *, telegram_id: str) -> list[Memory]:
        return self.memory_service.list_memories(external_ref=self._ref(telegram_id))

    def forget_all(self, *, telegram_id: str) -> None:
        ref = self._ref(telegram_id)
        user = self.memory_service.get_user(external_ref=ref)
        if user:
            self.db.query(Memory).filter(Memory.user_id == user.id).delete()
            self.db.commit()
