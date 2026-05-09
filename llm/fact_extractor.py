import json
import logging

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from config import settings
from prompts import FACT_EXTRACTION_PROMPT

logger = logging.getLogger(__name__)


class FactExtractor:
    def __init__(self) -> None:
        self.model = init_chat_model(
            model=settings.llm_extractor_model,
            base_url=settings.llm_base_url,
            temperature=0.1,
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", FACT_EXTRACTION_PROMPT),
                ("human", "Wyciągnij fakty (lub zwróć []):"),
            ]
        )
        self.chain = self.prompt | self.model

    async def extract(self, query: str) -> list[dict]:
        result = await self.chain.ainvoke({"query": query})
        logger.info(f"Extractor raw output: {result.content}")
        try:
            facts = json.loads(result.content.strip())
            return facts if isinstance(facts, list) else []
        except (json.JSONDecodeError, ValueError):
            logger.warning(f"Fact extraction non-JSON: {result.content[:200]}")
            return []
