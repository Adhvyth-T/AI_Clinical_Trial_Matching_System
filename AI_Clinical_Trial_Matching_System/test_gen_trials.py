# scripts/generate_trial_data.py (revised for CSV)
import pandas as pd
import os

os.makedirs("data/clinical_trials", exist_ok=True)

# Sample structured clinical trials
trials = [
    {
        "nct_id": "NCT1000001",
        "title": "Metformin Use in Type 2 Diabetes",
        "inclusion": "Diagnosed with Type 2 Diabetes, age between 30 and 70, on stable metformin dose",
        "exclusion": "Renal impairment, pregnant or breastfeeding, prior insulin therapy"
    },
    {
        "nct_id": "NCT1000002",
        "title": "Hypertension Drug Efficacy Study",
        "inclusion": "Age 40–80, systolic BP > 140, diagnosed hypertension",
        "exclusion": "Previous stroke, chronic kidney disease stage 3 or higher"
    },
    {
        "nct_id": "NCT1000003",
        "title": "Weight Loss Trial for Obese Adults",
        "inclusion": "BMI ≥ 30, age 18–60",
        "exclusion": "Active thyroid disease, bariatric surgery history"
    }
]

pd.DataFrame(trials).to_csv("data/clinical_trials/trials.csv", index=False)
print("Sample trials.csv created at data/clinical_trials/trials.csv")
