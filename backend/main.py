from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "ml")
    )
)

from hybrid_diagnosis import hybrid_diagnosis
from backend.database import SessionLocal
from backend.models import DiagnosticRecord


app = FastAPI(
    title="PCB-Diag API",
    description="Intelligent PCB Fault Diagnosis API",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PCBMeasurements(BaseModel):

    supply_voltage: float
    input_current: float
    regulator_output: float
    mcu_voltage: float
    temperature: float
    ripple_voltage: float
    signal_frequency: float
    continuity: int


class RepairVerification(BaseModel):

    supply_voltage: float
    input_current: float
    regulator_output: float
    mcu_voltage: float
    temperature: float
    ripple_voltage: float
    signal_frequency: float
    continuity: int
    original_diagnosis: str | None = None


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "PCB-Diag API is running!"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "PCB-Diag API"
    }


# --------------------------------------------------
# DIAGNOSE PCB
# --------------------------------------------------

@app.post("/diagnose")
def diagnose(
    measurements: PCBMeasurements,
    db: Session = Depends(get_db)
):

    try:

        measurement_data = measurements.model_dump()

        result = hybrid_diagnosis(
            measurement_data
        )

        record = DiagnosticRecord(

            created_at=datetime.now(),

            supply_voltage=measurements.supply_voltage,
            input_current=measurements.input_current,
            regulator_output=measurements.regulator_output,
            mcu_voltage=measurements.mcu_voltage,
            temperature=measurements.temperature,
            ripple_voltage=measurements.ripple_voltage,
            signal_frequency=measurements.signal_frequency,
            continuity=measurements.continuity,

            diagnosis=result["diagnosis"],
            ml_prediction=result["ml_prediction"],
            rule_prediction=result["rule_prediction"],
            confidence=float(result["confidence"]),
            severity=result["severity"],
            suspected_area=result["suspected_area"],
            evidence=result["evidence"],
            recommendation=result["recommendation"]
        )

        db.add(record)

        db.commit()

        db.refresh(record)

        return result

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Diagnosis failed: {str(e)}"
        )


# --------------------------------------------------
# DIAGNOSIS HISTORY
# --------------------------------------------------

@app.get("/history")
def get_history(
    db: Session = Depends(get_db)
):

    try:

        records = (
            db.query(DiagnosticRecord)
            .order_by(DiagnosticRecord.id.asc())
            .all()
        )

        return [

            {
                "id": record.id,
                "created_at": record.created_at,

                "supply_voltage": record.supply_voltage,
                "input_current": record.input_current,
                "regulator_output": record.regulator_output,
                "mcu_voltage": record.mcu_voltage,
                "temperature": record.temperature,
                "ripple_voltage": record.ripple_voltage,
                "signal_frequency": record.signal_frequency,
                "continuity": record.continuity,

                "diagnosis": record.diagnosis,
                "ml_prediction": record.ml_prediction,
                "rule_prediction": record.rule_prediction,

                "confidence": record.confidence,
                "severity": record.severity,
                "suspected_area": record.suspected_area,

                "evidence": record.evidence,
                "recommendation": record.recommendation
            }

            for record in records
        ]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not load history: {str(e)}"
        )

@app.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db)
):

    try:

        records = (
            db.query(DiagnosticRecord)
            .all()
        )

        total = len(records)

        healthy = 0
        faulty = 0
        critical = 0

        diagnosis_counts = {}
        area_counts = {}

        for record in records:

            diagnosis = record.diagnosis

            if diagnosis == "Normal":
                healthy += 1
            else:
                faulty += 1

            if record.severity == "Critical":
                critical += 1

            diagnosis_counts[diagnosis] = (
                diagnosis_counts.get(diagnosis, 0) + 1
            )

            if diagnosis != "Normal":

                area = record.suspected_area

                if area:
                    area_counts[area] = (
                        area_counts.get(area, 0) + 1
                    )

        most_common_fault = None

        faulty_diagnoses = {
            key: value
            for key, value in diagnosis_counts.items()
            if key != "Normal"
        }

        if faulty_diagnoses:

            most_common_fault = max(
                faulty_diagnoses,
                key=faulty_diagnoses.get
            )

        most_common_area = None

        if area_counts:

            most_common_area = max(
                area_counts,
                key=area_counts.get
            )

        return {

            "total_diagnoses": total,

            "healthy_boards": healthy,

            "faulty_boards": faulty,

            "critical_faults": critical,

            "most_common_fault":
                most_common_fault,

            "most_common_area":
                most_common_area,

            "diagnosis_distribution":
                diagnosis_counts,

            "area_distribution":
                area_counts
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not generate analytics: {str(e)}"
        )


# --------------------------------------------------
# POST-REPAIR VERIFICATION
# --------------------------------------------------

@app.post("/verify-repair")
def verify_repair(
    measurements: RepairVerification
):

    try:

        measurement_data = {
            "supply_voltage": measurements.supply_voltage,
            "input_current": measurements.input_current,
            "regulator_output": measurements.regulator_output,
            "mcu_voltage": measurements.mcu_voltage,
            "temperature": measurements.temperature,
            "ripple_voltage": measurements.ripple_voltage,
            "signal_frequency": measurements.signal_frequency,
            "continuity": measurements.continuity
        }

        result = hybrid_diagnosis(measurement_data)

        if result["diagnosis"] == "Normal":

            repair_status = "Repair Successful"

            recommendation = (
                "PCB parameters are within normal "
                "operating limits. Repair appears successful."
            )

        else:

            repair_status = "Repair Required"

            recommendation = (
                "The PCB still shows abnormal parameters. "
                "Further troubleshooting is recommended."
            )

        return {
            "repair_status": repair_status,

            "original_diagnosis":
                measurements.original_diagnosis
                if measurements.original_diagnosis
                else "Not Provided",

            "diagnosis":
                result["diagnosis"],

            "confidence":
                result["confidence"],

            "recommendation":
                recommendation
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Repair verification failed: {str(e)}"
        )