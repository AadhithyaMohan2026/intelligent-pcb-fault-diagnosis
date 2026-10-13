import pandas as pd
import numpy as np

np.random.seed(42)

print("Generating realistic PCB dataset...")

n = 1000

# -----------------------------
# 1. NORMAL PCB
# -----------------------------
normal_data = pd.DataFrame({
    "supply_voltage": np.clip(np.random.normal(12, 0.25, n), 11, 13),
    "input_current": np.clip(np.random.normal(0.6, 0.12, n), 0.1, 1.2),
    "regulator_output": np.clip(np.random.normal(5.0, 0.08, n), 4.7, 5.3),
    "mcu_voltage": np.clip(np.random.normal(3.3, 0.05, n), 3.1, 3.5),
    "temperature": np.clip(np.random.normal(35, 5, n), 20, 50),
    "ripple_voltage": np.clip(np.random.normal(0.04, 0.015, n), 0.005, 0.10),
    "signal_frequency": np.clip(np.random.normal(10, 0.3, n), 9, 11),
    "continuity": 1,
    "diagnosis": "Normal"
})


# -----------------------------
# 2. SHORT CIRCUIT
# -----------------------------
short_data = pd.DataFrame({
    "supply_voltage": np.clip(np.random.normal(11.8, 0.4, n), 10.5, 12.8),
    "input_current": np.clip(np.random.normal(3.0, 0.6, n), 1.5, 5.0),
    "regulator_output": np.clip(np.random.normal(3.4, 0.5, n), 2.0, 4.5),
    "mcu_voltage": np.clip(np.random.normal(2.9, 0.25, n), 2.2, 3.4),
    "temperature": np.clip(np.random.normal(70, 12, n), 40, 110),
    "ripple_voltage": np.clip(np.random.normal(0.6, 0.2, n), 0.2, 1.2),
    "signal_frequency": np.clip(np.random.normal(9, 1, n), 5, 11),
    "continuity": 1,
    "diagnosis": "Short Circuit"
})


# -----------------------------
# 3. OPEN CIRCUIT
# -----------------------------
open_data = pd.DataFrame({
    "supply_voltage": np.clip(np.random.normal(12, 0.3, n), 11, 13),
    "input_current": np.clip(np.random.normal(0.15, 0.06, n), 0.01, 0.4),
    "regulator_output": np.clip(np.random.normal(5.0, 0.1, n), 4.6, 5.4),
    "mcu_voltage": np.clip(np.random.normal(3.3, 0.08, n), 3.0, 3.5),
    "temperature": np.clip(np.random.normal(32, 5, n), 20, 50),
    "ripple_voltage": np.clip(np.random.normal(0.04, 0.02, n), 0.005, 0.12),
    "signal_frequency": np.clip(np.random.normal(3, 1.2, n), 0, 8),
    "continuity": 0,
    "diagnosis": "Open Circuit"
})


# -----------------------------
# 4. REGULATOR FAILURE
# -----------------------------
regulator_data = pd.DataFrame({
    "supply_voltage": np.clip(np.random.normal(12, 0.3, n), 11, 13),
    "input_current": np.clip(np.random.normal(1.3, 0.3, n), 0.5, 2.2),
    "regulator_output": np.clip(np.random.normal(4.2, 0.3, n), 3.4, 4.8),
    "mcu_voltage": np.clip(np.random.normal(3.0, 0.2, n), 2.5, 3.4),
    "temperature": np.clip(np.random.normal(60, 10, n), 35, 90),
    "ripple_voltage": np.clip(np.random.normal(0.35, 0.12, n), 0.1, 0.7),
    "signal_frequency": np.clip(np.random.normal(8.5, 1, n), 5, 11),
    "continuity": 1,
    "diagnosis": "Regulator Failure"
})


# -----------------------------
# 5. OVERHEATING
# -----------------------------
overheat_data = pd.DataFrame({
    "supply_voltage": np.clip(np.random.normal(12, 0.3, n), 11, 13),
    "input_current": np.clip(np.random.normal(1.1, 0.3, n), 0.4, 2.0),
    "regulator_output": np.clip(np.random.normal(4.8, 0.2, n), 4.3, 5.2),
    "mcu_voltage": np.clip(np.random.normal(3.2, 0.1, n), 2.9, 3.5),
    "temperature": np.clip(np.random.normal(85, 12, n), 55, 120),
    "ripple_voltage": np.clip(np.random.normal(0.15, 0.05, n), 0.05, 0.35),
    "signal_frequency": np.clip(np.random.normal(9.5, 0.6, n), 7, 11),
    "continuity": 1,
    "diagnosis": "Overheating"
})


# -----------------------------
# 6. SENSOR FAILURE
# -----------------------------
sensor_data = pd.DataFrame({
    "supply_voltage": np.clip(np.random.normal(12, 0.3, n), 11, 13),
    "input_current": np.clip(np.random.normal(0.7, 0.15, n), 0.2, 1.2),
    "regulator_output": np.clip(np.random.normal(5.0, 0.1, n), 4.7, 5.3),
    "mcu_voltage": np.clip(np.random.normal(3.3, 0.05, n), 3.1, 3.5),
    "temperature": np.clip(np.random.normal(40, 7, n), 20, 60),
    "ripple_voltage": np.clip(np.random.normal(0.05, 0.02, n), 0.005, 0.15),
    "signal_frequency": np.clip(np.random.normal(4, 1.5, n), 0, 8),
    "continuity": 1,
    "diagnosis": "Sensor Failure"
})


# -----------------------------
# COMBINE ALL DATA
# -----------------------------
df = pd.concat([
    normal_data,
    short_data,
    open_data,
    regulator_data,
    overheat_data,
    sensor_data
], ignore_index=True)

# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save dataset
df.to_csv(
    "data/raw/pcb_measurements.csv",
    index=False
)

print("Dataset generated successfully!")
print("Shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nDiagnosis distribution:")
print(df["diagnosis"].value_counts())