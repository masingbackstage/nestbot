import logging
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from config import settings
from prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class LLMProvider:
    def __init__(self) -> None:
        self.model = init_chat_model(
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            temperature=settings.temperature,
            extra_body={"think": False},
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                ("human", "{query}"),
            ]
        )
        self.chain = self.prompt | self.model

    async def chat(self, context: str, query: str) -> str | list[Any]:
        logger.debug(f"LLM context:\n{context}")
        response = await self.chain.ainvoke({"context": context, "query": query})
        return response.content
