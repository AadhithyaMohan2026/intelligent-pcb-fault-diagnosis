from sqlalchemy import Column, Integer, Float, String, Text, DateTime
from backend.database import Base


class DiagnosticRecord(Base):

    __tablename__ = "diagnostic_records"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)

    supply_voltage = Column(Float)
    input_current = Column(Float)
    regulator_output = Column(Float)
    mcu_voltage = Column(Float)
    temperature = Column(Float)
    ripple_voltage = Column(Float)
    signal_frequency = Column(Float)
    continuity = Column(Integer)

    diagnosis = Column(String(50))
    ml_prediction = Column(String(50))
    rule_prediction = Column(String(50))
    confidence = Column(Float)

    severity = Column(String(20))
    suspected_area = Column(String(100))
    evidence = Column(Text)
    recommendation = Column(Text)