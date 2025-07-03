# src/llm/summarizer.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def call_openrouter(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a clinical trial expert AI."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")
    return response.json()["choices"][0]["message"]["content"]

def summarize_patient_profile(profile_text: str) -> str:
    prompt = f"""
    Summarize the following patient profile into key medical conditions, age, medications, and notable exclusions:
    ---
    {profile_text}
    """
    return call_openrouter(prompt)

def summarize_trial_criteria(inclusion: str, exclusion: str) -> str:
    prompt = f"""
    Summarize the following clinical trial eligibility criteria:
    Inclusion:
    {inclusion}
    Exclusion:
    {exclusion}
    Output a concise and clear list.
    """
    return call_openrouter(prompt)
