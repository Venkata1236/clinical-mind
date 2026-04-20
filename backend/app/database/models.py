from sqlalchemy import Column, String, Float, DateTime, JSON, Text
from sqlalchemy.sql import func

from app.database.connection import Base


class EligibilityCheck(Base):
    __tablename__ = "eligibility_checks"

    session_id = Column(String, primary_key=True)
    patient_id = Column(String, nullable=False, index=True)
    patient_name = Column(String)
    diagnosis = Column(String)
    top_trial_id = Column(String)
    top_trial_score = Column(Float)
    eligibility_status = Column(String)
    full_response = Column(JSON)
    processing_time_seconds = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())