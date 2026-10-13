import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/pcb_measurements.csv")

print("----- FIRST 5 ROWS -----")
print(df.head())

print("\n----- SHAPE -----")
print(df.shape)

print("\n----- COLUMNS -----")
print(df.columns)

print("\n----- DATA TYPES -----")
print(df.dtypes)

print("\n----- DATASET INFO -----")
print(df.info())

print("\n----- STATISTICS -----")
print(df.describe())

print("\n----- MISSING VALUES -----")
print(df.isnull().sum())

print("\n----- DIAGNOSIS COUNT -----")
print(df["diagnosis"].value_counts())