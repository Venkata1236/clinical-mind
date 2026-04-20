from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TrialPhase(str, Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    any = "any"


class EligibilityStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    POTENTIALLY_ELIGIBLE = "POTENTIALLY_ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"


class LabValues(BaseModel):
    HbA1c: Optional[float] = None
    eGFR: Optional[float] = None
    ECOG_score: Optional[int] = None


class PatientProfile(BaseModel):
    patient_id: str
    name: str
    age: int = Field(ge=0, le=120)
    diagnosis: str
    comorbidities: list[str] = []
    current_medications: list[str] = []
    prior_treatments: list[str] = []
    lab_values: LabValues = LabValues()
    trial_phase_preference: TrialPhase = TrialPhase.any


class TrialMatch(BaseModel):
    trial_id: str
    title: str
    condition: str
    phase: str
    match_score: float = Field(ge=0.0, le=100.0)
    eligibility_status: EligibilityStatus
    met_criteria: list[str]
    unmet_criteria: list[str]
    reasoning: str


class ReportSection(BaseModel):
    summary: str
    recommendation: str
    disclaimer: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class EligibilityResponse(BaseModel):
    session_id: str
    status: str = "completed"
    top_trials: list[TrialMatch]
    report: ReportSection
    processing_time_seconds: float


class HealthResponse(BaseModel):
    status: str
    environment: str
    faiss_index_loaded: bool