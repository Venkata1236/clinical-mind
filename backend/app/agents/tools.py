from crewai.tools import BaseTool
from pydantic import Field
from loguru import logger


class FAISSRetrieverTool(BaseTool):
    """
    LangChain-compatible Tool that wraps FAISSRetriever.
    Given to EligibilityAnalyst and TrialMatcher only.

    Why NOT ReportWriter:
    ReportWriter's job is to format and narrate — it receives
    fully structured data from Task 2. Giving it retrieval access
    wastes tokens and risks it injecting new, unverified trial data
    into the final report.
    """

    name: str = "clinical_trial_retriever"
    description: str = (
        "Search the clinical trials database for relevant eligibility criteria. "
        "Input: a patient profile summary or specific condition/medication query. "
        "Output: top 5 most relevant trial criteria chunks from the FAISS index."
    )
    retriever: object = Field(default=None, exclude=True)

    def _run(self, query: str) -> str:
        logger.info(f"FAISSRetrieverTool called | query: {query[:80]}...")
        result = self.retriever.search_as_text(query, k=5)
        return result