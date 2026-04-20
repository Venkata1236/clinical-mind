from crewai import Crew, Process
from loguru import logger

from app.agents.agents import create_agents
from app.agents.tasks import create_tasks
from app.agents.tools import FAISSRetrieverTool


class ClinicalMindCrew:
    """
    Stateless crew — a new Crew instance is created per request.
    No shared memory between runs. Each patient gets a clean context.
    """

    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, patient_profile: dict) -> dict:
        logger.info(f"Starting crew for patient: {patient_profile.get('patient_id')}")

        faiss_tool = FAISSRetrieverTool(retriever=self.retriever)

        eligibility_analyst, trial_matcher, report_writer = create_agents(faiss_tool)
        tasks = create_tasks(
            eligibility_analyst,
            trial_matcher,
            report_writer,
            patient_profile,
        )

        crew = Crew(
            agents=[eligibility_analyst, trial_matcher, report_writer],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        logger.info(f"Crew completed for patient: {patient_profile.get('patient_id')}")

        return self._parse_result(result)

    def _parse_result(self, result) -> dict:
        import json

        raw = result.raw if hasattr(result, "raw") else str(result)

        # Strip markdown fences if model adds them despite instructions
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse crew JSON output: {e}")
            logger.error(f"Raw output: {raw[:500]}")
            raise ValueError(f"Crew output was not valid JSON: {e}")