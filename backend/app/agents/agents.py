from crewai import Agent
from loguru import logger

from app.core.config import get_settings


def create_agents(faiss_tool) -> tuple:
    settings = get_settings()

    eligibility_analyst = Agent(
        role="Clinical Trial Eligibility Expert",
        goal=(
            "Systematically check if a patient meets inclusion and exclusion "
            "criteria for each retrieved trial. For every criterion, explicitly "
            "state MET or NOT MET with the patient data that supports your decision."
        ),
        backstory=(
            "You are a clinical research coordinator with 15 years of experience "
            "reviewing patient eligibility for Phase II and III trials at Apollo Hospitals. "
            "You are methodical, precise, and never make assumptions about missing data. "
            "When data is missing from the patient profile, you flag it as UNKNOWN — "
            "you never assume eligibility without evidence."
        ),
        tools=[faiss_tool],
        llm=settings.openai_model,
        verbose=True,
        allow_delegation=False,
    )

    trial_matcher = Agent(
        role="Clinical Trial Matching Specialist",
        goal=(
            "Rank the top 3 matching trials for the patient profile based on the "
            "eligibility analysis. Assign a match_score from 0–100 for each trial. "
            "Provide clear reasoning for each score."
        ),
        backstory=(
            "You are a specialist in patient-trial matching who understands both "
            "the clinical requirements of trials and the practical factors that affect "
            "patient participation — travel burden, trial duration, prior treatment requirements. "
            "You weigh MET criteria more heavily than UNKNOWN criteria, and always "
            "disqualify trials where any HARD exclusion criterion is NOT MET."
        ),
        tools=[faiss_tool],
        llm=settings.openai_model,
        verbose=True,
        allow_delegation=False,
    )

    report_writer = Agent(
        role="Medical Report Writer",
        goal=(
            "Generate a structured, physician-ready clinical recommendation report "
            "summarizing the top 3 trial matches with clear eligibility reasoning. "
            "Output must be valid JSON matching the required schema exactly."
        ),
        backstory=(
            "You write precise medical reports that physicians use directly for patient "
            "counseling at oncology and endocrinology departments. Your reports are factual, "
            "well-structured, and always include a medical disclaimer. You never add trial "
            "information that was not provided to you — you only report what the TrialMatcher found."
        ),
        tools=[],  # No retrieval — works only from Task 2 context
        llm=settings.openai_model,
        verbose=True,
        allow_delegation=False,
    )

    logger.info("All 3 CrewAI agents initialized")
    return eligibility_analyst, trial_matcher, report_writer