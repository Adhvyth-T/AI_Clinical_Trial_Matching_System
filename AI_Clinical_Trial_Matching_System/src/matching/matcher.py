# src/matching/matcher.py
import json
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from src.llm.summarizer import call_openrouter


def load_embeddings(path: str):
    with open(path, "r") as f:
        return json.load(f)


def find_best_matches(patient_embedding: np.ndarray, trials_data: list, top_k: int = 5):
    scores = []
    for trial in trials_data:
        sim = cosine_similarity([patient_embedding], [trial["embedding"]])[0][0]
        scores.append((trial, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def validate_with_llm(patient_summary: str, trial: dict) -> dict:
    prompt = f"""
    A patient has the following summary:
    {patient_summary}

    The trial has this eligibility criteria:
    Title: {trial['title']}
    NCT ID: {trial['nct_id']}
    Inclusion + Exclusion Summary: {trial.get('summary', '[no summary available]')}"

    Determine if the patient is eligible or not, and explain why.
    Respond with a JSON:
    {{"eligible": true/false, "reason": "..."}}
    """
    try:
        result = call_openrouter(prompt)
        parsed = json.loads(result.strip())
        return {
            "nct_id": trial["nct_id"],
            "title": trial["title"],
            "eligible": parsed.get("eligible", False),
            "reason": parsed.get("reason", "No explanation returned")
        }
    except Exception as e:
        return {
            "nct_id": trial["nct_id"],
            "title": trial["title"],
            "eligible": False,
            "reason": f"Error during LLM validation: {str(e)}"
        }


def match_patient_to_trials(patient_id: str, patient_summary: str, patient_embedding: np.ndarray, trial_embedding_path: str, output_dir: str):
    trials = load_embeddings(trial_embedding_path)
    top_matches = find_best_matches(patient_embedding, trials)

    results = []
    for trial, _ in top_matches:
        validated = validate_with_llm(patient_summary, trial)
        results.append(validated)

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{patient_id}_matches.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {patient_id}_matches.json")
