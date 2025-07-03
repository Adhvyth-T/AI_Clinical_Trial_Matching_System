# src/embedding/embedder.py
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import json

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> np.ndarray:
    return model.encode(text, convert_to_numpy=True)


def embed_and_store_trials(trials_json_path: str, output_path: str):
    """
    Embeds inclusion/exclusion criteria for all trials and saves to file.
    """
    with open(trials_json_path, "r") as f:
        trials = json.load(f)

    embedded_trials = []
    for trial in trials:
        combined_text = f"Inclusion: {trial['inclusion']}\nExclusion: {trial['exclusion']}"
        embedding = embed_text(combined_text).tolist()
        embedded_trials.append({
            "nct_id": trial["nct_id"],
            "title": trial["title"],
            "embedding": embedding
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(embedded_trials, f, indent=2)
    print(f"Stored {len(embedded_trials)} trial embeddings to {output_path}")


def embed_patient_summary(summary: str) -> np.ndarray:
    return embed_text(summary)
