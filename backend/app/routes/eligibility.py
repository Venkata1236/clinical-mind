import uuid
import time
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.models.schemas import PatientProfile, EligibilityResponse, ReportSection, TrialMatch
from app.database.connection import get_db
from app.database.models import EligibilityCheck

router = APIRouter()

# Crew instance injected at startup via app state
def get_crew(request):
    return request.app.state.crew


@router.post("/check-eligibility", response_model=EligibilityResponse)
async def check_eligibility(
    patient: PatientProfile,
    db: AsyncSession = Depends(get_db),
    request=None,
):
    from fastapi import Request
    session_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"Eligibility check started | session={session_id} | patient={patient.patient_id}")

    try:
        crew = request.app.state.crew
        patient_dict = patient.model_dump()
        patient_dict["lab_values"] = patient_dict["lab_values"] if isinstance(patient_dict["lab_values"], dict) else patient.lab_values.model_dump()

        crew_output = crew.run(patient_dict)

        top_trials = [TrialMatch(**t) for t in crew_output["top_trials"]]
        report_data = crew_output["report"]
        report = ReportSection(
            summary=report_data["summary"],
            recommendation=report_data["recommendation"],
            disclaimer=report_data["disclaimer"],
        )

        processing_time = round(time.time() - start_time, 2)

        response = EligibilityResponse(
            session_id=session_id,
            status="completed",
            top_trials=top_trials,
            report=report,
            processing_time_seconds=processing_time,
        )

        # Persist to PostgreSQL
        top_trial = top_trials[0] if top_trials else None
        db_record = EligibilityCheck(
            session_id=session_id,
            patient_id=patient.patient_id,
            patient_name=patient.name,
            diagnosis=patient.diagnosis,
            top_trial_id=top_trial.trial_id if top_trial else None,
            top_trial_score=top_trial.match_score if top_trial else None,
            eligibility_status=top_trial.eligibility_status if top_trial else None,
            full_response=response.model_dump(mode="json"),
            processing_time_seconds=processing_time,
        )
        db.add(db_record)
        await db.commit()

        logger.info(f"Eligibility check completed | session={session_id} | time={processing_time}s")
        return response

    except Exception as e:
        logger.error(f"Eligibility check failed | session={session_id} | error={e}")
        raise HTTPException(status_code=500, detail=str(e))