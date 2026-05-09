from langchain_ollama import OllamaEmbeddings


class EmbeddingService:

    def __init__(self, model: str) -> None:
        self.embeddings = OllamaEmbeddings(model=model)

    def embed_text(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)