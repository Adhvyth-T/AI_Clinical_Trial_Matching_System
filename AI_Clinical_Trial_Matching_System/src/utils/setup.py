# src/utils/setup.py
import os
from dotenv import load_dotenv

def setup_environment():
    """
    Loads environment variables and prepares directories.
    """
    load_dotenv()
    print("KEY:", os.getenv("OPENROUTER_API_KEY"))

    required_keys = ["OPENROUTER_API_KEY"]
    for key in required_keys:
        if not os.getenv(key):
            raise EnvironmentError(f"Missing required environment variable: {key}")
        
    os.makedirs("data/clinical_trials", exist_ok=True)

    os.makedirs("data/patient_data", exist_ok=True)
    os.makedirs("output/matched_trials", exist_ok=True)
    print("Environment setup complete.")
