import pandas as pd
import joblib

from rule_engine import diagnose_with_rules


# --------------------------------------------------
# LOAD ML MODEL
# --------------------------------------------------

model = joblib.load("ml/pcb_fault_model.pkl")


# --------------------------------------------------
# NORMAL MEASUREMENT CHECK
# --------------------------------------------------

def is_normal_measurement(measurements):

    supply = float(measurements["supply_voltage"])
    current = float(measurements["input_current"])
    regulator = float(measurements["regulator_output"])
    mcu = float(measurements["mcu_voltage"])
    temperature = float(measurements["temperature"])
    ripple = float(measurements["ripple_voltage"])
    frequency = float(measurements["signal_frequency"])
    continuity = int(measurements["continuity"])

    return (
        11.0 <= supply <= 13.0
        and 0.1 <= current <= 1.2
        and 4.7 <= regulator <= 5.3
        and 3.1 <= mcu <= 3.5
        and 20 <= temperature < 70
        and 0.005 <= ripple <= 0.10
        and 9 <= frequency <= 11
        and continuity == 1
    )


# --------------------------------------------------
# DIAGNOSIS DETAILS
# --------------------------------------------------

def get_diagnosis_details(diagnosis, measurements):

    if diagnosis == "Normal":

        return {
            "severity": "None",
            "suspected_area": "PCB - No Fault Detected",
            "evidence": (
                "All measured parameters are within the "
                "expected operating conditions."
            ),
            "recommendation": (
                "PCB appears healthy. No immediate action required."
            )
        }

    elif diagnosis == "Short Circuit":

        return {
            "severity": "Critical",
            "suspected_area": "Power / Supply Section",
            "evidence": (
                "Input current is abnormally high, with "
                "elevated temperature and ripple voltage."
            ),
            "recommendation": (
                "Power off the PCB and inspect the power rail "
                "for shorted components, solder bridges, or PCB traces."
            )
        }

    elif diagnosis == "Open Circuit":

        return {
            "severity": "Medium",
            "suspected_area": "PCB Trace / Interconnect",
            "evidence": (
                "Continuity testing indicates an open connection."
            ),
            "recommendation": (
                "Inspect PCB traces, connectors, solder joints, "
                "and other interconnections for discontinuity."
            )
        }

    elif diagnosis == "Regulator Failure":

        return {
            "severity": "High",
            "suspected_area": "Voltage Regulator",
            "evidence": (
                "Regulator output and/or MCU voltage are below "
                "their expected operating levels."
            ),
            "recommendation": (
                "Check the regulator input/output voltages and "
                "inspect the regulator and surrounding capacitors."
            )
        }

    elif diagnosis == "Overheating":

        return {
            "severity": "High",
            "suspected_area": "Thermal / Power Section",
            "evidence": (
                "Measured PCB temperature is significantly "
                "above the normal operating range."
            ),
            "recommendation": (
                "Inspect the regulator and power components for "
                "excessive current draw, poor thermal dissipation, "
                "or component failure."
            )
        }

    elif diagnosis == "Sensor Failure":

        return {
            "severity": "Medium",
            "suspected_area": "Sensor / Signal Section",
            "evidence": (
                "Signal frequency is significantly below the "
                "expected operating frequency while the main "
                "power measurements remain normal."
            ),
            "recommendation": (
                "Inspect the sensor, signal connections, sensor "
                "supply, and associated signal-conditioning circuitry."
            )
        }

    return {
        "severity": "Unknown",
        "suspected_area": "Unknown",
        "evidence": (
            "The diagnostic engine could not determine the fault details."
        ),
        "recommendation": (
            "Repeat the measurements and inspect the PCB."
        )
    }


# --------------------------------------------------
# HYBRID DIAGNOSIS
# --------------------------------------------------

def hybrid_diagnosis(measurements):

    # Make a copy so the original object is not modified
    measurements = measurements.copy()

    # VERY IMPORTANT:
    # Always normalize continuity to integer 0 or 1
    measurements["continuity"] = int(
        measurements["continuity"]
    )

    print("\n===============================================")
    print("PCB DIAGNOSIS")
    print("===============================================")

    print("Supply Voltage   :", measurements["supply_voltage"])
    print("Input Current    :", measurements["input_current"])
    print("Regulator Output :", measurements["regulator_output"])
    print("MCU Voltage      :", measurements["mcu_voltage"])
    print("Temperature      :", measurements["temperature"])
    print("Ripple Voltage   :", measurements["ripple_voltage"])
    print("Signal Frequency :", measurements["signal_frequency"])
    print("Continuity       :", measurements["continuity"])

    # --------------------------------------------------
    # FIRST CHECK: ENGINEERING NORMAL CONDITION
    # --------------------------------------------------

    if is_normal_measurement(measurements):

        print("Engineering Check: NORMAL")
        print("Final Diagnosis: NORMAL")
        print("===============================================\n")

        return {
            "diagnosis": "Normal",
            "ml_prediction": "Normal",
            "rule_prediction": "Normal",
            "confidence": 1.0,
            "severity": "None",
            "suspected_area": "PCB - No Fault Detected",
            "evidence": (
                "All measured parameters are within the "
                "expected operating conditions."
            ),
            "recommendation": (
                "PCB appears healthy. No immediate action required."
            )
        }

    # --------------------------------------------------
    # ML PREDICTION
    # --------------------------------------------------

    input_data = pd.DataFrame([measurements])

    ml_prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    ml_confidence = float(max(probabilities))

    # --------------------------------------------------
    # RULE ENGINE
    # --------------------------------------------------

    rule_prediction = diagnose_with_rules(measurements)

    # --------------------------------------------------
    # FINAL DIAGNOSIS
    # --------------------------------------------------

    if rule_prediction != "Unknown Fault":
        final_diagnosis = rule_prediction
    else:
        final_diagnosis = ml_prediction

    confidence = ml_confidence

    # --------------------------------------------------
    # GET DETAILS
    # --------------------------------------------------

    details = get_diagnosis_details(
        final_diagnosis,
        measurements
    )

    print("ML Prediction    :", ml_prediction)
    print("Rule Prediction  :", rule_prediction)
    print("Final Diagnosis  :", final_diagnosis)
    print("Confidence       :", confidence)

    print("===============================================\n")

    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {
        "diagnosis": final_diagnosis,
        "ml_prediction": ml_prediction,
        "rule_prediction": rule_prediction,
        "confidence": confidence,
        "severity": details["severity"],
        "suspected_area": details["suspected_area"],
        "evidence": details["evidence"],
        "recommendation": details["recommendation"]
    }