def diagnose_with_rules(measurements):

    supply = float(measurements["supply_voltage"])
    current = float(measurements["input_current"])
    regulator = float(measurements["regulator_output"])
    mcu = float(measurements["mcu_voltage"])
    temperature = float(measurements["temperature"])
    ripple = float(measurements["ripple_voltage"])
    frequency = float(measurements["signal_frequency"])
    continuity = int(measurements["continuity"])

    # --------------------------------------------------
    # OPEN CIRCUIT
    # --------------------------------------------------
    if continuity == 0:
        return "Open Circuit"

    # --------------------------------------------------
    # SHORT CIRCUIT
    # --------------------------------------------------
    if (
        current > 2.0
        and temperature >= 60
        and ripple > 0.2
    ):
        return "Short Circuit"

    # --------------------------------------------------
    # REGULATOR FAILURE
    # --------------------------------------------------
    if regulator < 4.5 or mcu < 3.1:
        return "Regulator Failure"

    # --------------------------------------------------
    # OVERHEATING
    # --------------------------------------------------
    if temperature >= 70:
        return "Overheating"

    # --------------------------------------------------
    # SENSOR / SIGNAL FAILURE
    # --------------------------------------------------
    if (
        frequency < 7
        and 3.1 <= mcu <= 3.5
        and 4.7 <= regulator <= 5.3
        and continuity == 1
    ):
        return "Sensor Failure"

    # --------------------------------------------------
    # NORMAL
    # --------------------------------------------------
    if (
        11.0 <= supply <= 13.0
        and 0.1 <= current <= 1.2
        and 4.7 <= regulator <= 5.3
        and 3.1 <= mcu <= 3.5
        and 20 <= temperature < 70
        and 0.005 <= ripple <= 0.10
        and 9 <= frequency <= 11
        and continuity == 1
    ):
        return "Normal"

    # --------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------
    return "Unknown Fault"