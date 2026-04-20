from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from loguru import logger


class FAISSRetriever:
    """
    Thin wrapper around FAISS vectorstore.
    Loaded once at API startup, reused across all requests.
    """

    def __init__(self, vectorstore: FAISS):
        self.vectorstore = vectorstore

    def search(self, query: str, k: int = 5) -> list[Document]:
        """
        Run similarity search. Returns top-k most relevant trial chunks.
        k=5 gives agents enough context without overwhelming the prompt.
        """
        logger.debug(f"FAISS search | k={k} | query: {query[:80]}...")
        results = self.vectorstore.similarity_search(query, k=k)
        logger.debug(f"FAISS returned {len(results)} chunks")
        return results

    def search_as_text(self, query: str, k: int = 5) -> str:
        """
        Returns search results as a single formatted string.
        This is what agents consume — plain text, not Document objects.
        """
        docs = self.search(query, k=k)
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(
                f"[Trial Chunk {i} | Source: {doc.metadata.get('source', 'unknown')}]\n"
                f"{doc.page_content}"
            )
        return "\n\n".join(formatted)