# scripts/generate_test_data.py
import pandas as pd
import os

os.makedirs("data/patient_data", exist_ok=True)

# Create mock patient conditions
df_conditions = pd.DataFrame([
    {"patient_id": "P001", "condition": "Type 2 Diabetes"},
    {"patient_id": "P002", "condition": "Hypertension"},
    {"patient_id": "P001", "condition": "Obesity"}
])
df_conditions.to_csv("data/patient_data/conditions.csv", index=False)

# Create mock medications
df_medications = pd.DataFrame([
    {"patient_id": "P001", "medication": "Metformin"},
    {"patient_id": "P002", "medication": "Lisinopril"}
])
df_medications.to_csv("data/patient_data/medications.csv", index=False)

# Create mock allergies
df_allergies = pd.DataFrame([
    {"patient_id": "P002", "allergy": "Penicillin"}
])
df_allergies.to_csv("data/patient_data/allergies.csv", index=False)

print("Sample patient data created in data/patient_data/")
