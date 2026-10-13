import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data/raw/pcb_measurements.csv")

# Input features
X = df.drop("diagnosis", axis=1)

# Target
y = df["diagnosis"]

print("Features:")
print(X.columns)

print("\nTarget:")
print(y.name)

print("\nX shape:", X.shape)
print("y shape:", y.shape)

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)

from sklearn.ensemble import RandomForestClassifier

# Create the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

print("\nModel training completed!")

# Predict diagnoses for unseen test data
y_pred = model.predict(X_test)

print("\nPredictions:")
print(y_pred[:10])

print("\nActual:")
print(y_test.values[:10])

from sklearn.metrics import accuracy_score, classification_report

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

# Detailed evaluation
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

import joblib

# Save trained model
joblib.dump(model, "ml/pcb_fault_model.pkl")

print("\nModel saved successfully!")