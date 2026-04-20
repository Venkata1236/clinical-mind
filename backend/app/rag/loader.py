from pathlib import Path
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger


def load_trial_documents(trials_dir: str = "data/trials/") -> list[Document]:
    """
    Load all .txt trial documents from the trials directory.
    Each file = one clinical trial.
    """
    trials_path = Path(trials_dir)
    documents = []

    for file_path in trials_path.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        doc = Document(
            page_content=text,
            metadata={
                "source": file_path.name,
                "trial_id": file_path.stem,
            }
        )
        documents.append(doc)
        logger.info(f"Loaded trial document: {file_path.name}")

    logger.info(f"Total trial documents loaded: {len(documents)}")
    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    Criteria-aware chunking strategy.

    Why NOT arbitrary character splitting:
    - A chunk like "...age > 18\nNo prior insulin\nExclu" has no context.
    - A chunk aligned to "Inclusion Criteria:" gives the agent a complete,
      actionable block it can check against the patient profile.

    separators priority:
    1. Double newline  → paragraph boundary
    2. "Inclusion"     → start of inclusion criteria block
    3. "Exclusion"     → start of exclusion criteria block
    4. Single newline  → line boundary fallback
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "Inclusion", "Exclusion", "\n"],
    )

    chunks = splitter.split_documents(documents)
    logger.info(f"Total chunks after splitting: {len(chunks)}")
    return chunks