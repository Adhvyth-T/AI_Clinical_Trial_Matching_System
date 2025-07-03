# src/pipeline/run_pipeline.py
import os
import sqlite3
import pandas as pd
import json
import asyncio
from src.data.csv_to_sqlite import csv_to_sqlite
from src.data.csv_trials_loader import load_trials_from_csv
from src.data.web_scraper_trials import get_clinical_trials
from src.llm.summarizer import summarize_patient_profile, summarize_trial_criteria
from src.embedding.embedder import embed_and_store_trials, embed_patient_summary
from src.matching.matcher import match_patient_to_trials


def get_patient_profiles(db_path: str) -> dict:
    conn = sqlite3.connect(db_path)
    patient_ids = pd.read_sql("SELECT DISTINCT patient_id FROM conditions", conn)["patient_id"].tolist()

    profiles = {}
    for pid in patient_ids:
        patient_info = []
        for table in ["conditions", "medications", "allergies"]:
            try:
                df = pd.read_sql(f"SELECT * FROM {table} WHERE patient_id = ?", conn, params=(pid,))
                if not df.empty:
                    patient_info.append(f"{table.title()}:\n" + df.to_string(index=False))
            except Exception as e:
                continue
        profiles[pid] = "\n\n".join(patient_info)
    return profiles


def run_matching_pipeline():
    db_path = "data/patient_data/patients.db"
    csv_to_sqlite("data/patient_data", db_path)

    os.makedirs("data/clinical_trials", exist_ok=True)

    print("Loading trials from CSV...")
    csv_trials = load_trials_from_csv("data/clinical_trials/trials.csv")

    print("Scraping additional clinical trials...")
    scraped_trials = asyncio.run(get_clinical_trials())

    # Save scraped trials as CSV
    pd.DataFrame(scraped_trials).to_csv("data/clinical_trials/scraped_trials.csv", index=False)

    trials = csv_trials + scraped_trials

    print("Summarizing clinical trial criteria...")
    for trial in trials:
        trial["summary"] = summarize_trial_criteria(trial.get("inclusion", ""), trial.get("exclusion", ""))

    summarized_trials_path = "data/clinical_trials/summarized_trials.json"
    with open(summarized_trials_path, "w") as f:
        json.dump(trials, f, indent=2)

    embed_and_store_trials(summarized_trials_path, "data/clinical_trials/trial_embeddings.json")

    print("Summarizing patients and matching to trials...")
    profiles = get_patient_profiles(db_path)

    for pid, raw_text in profiles.items():
        summary = summarize_patient_profile(raw_text)
        embedding = embed_patient_summary(summary)
        match_patient_to_trials(
            patient_id=pid,
            patient_summary=summary,
            patient_embedding=embedding,
            trial_embedding_path="data/clinical_trials/trial_embeddings.json",
            output_dir="output/matched_trials"
        )
