# src/data/web_scraper_trials.py
import aiohttp
import asyncio

TRIALS_API = "https://clinicaltrials.gov/api/query/full_studies?expr=diabetes&min_rnk=1&max_rnk=5&fmt=json"

async def fetch_trials(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            print(f"Error fetching trials: {response.status}")
            return []
        return await response.json()

async def get_clinical_trials():
    async with aiohttp.ClientSession() as session:
        print("Fetching trials from ClinicalTrials.gov...")
        result = await fetch_trials(session, TRIALS_API)
        if not result:
            return []

        trials = []
        studies = result.get("FullStudiesResponse", {}).get("FullStudies", [])
        for study in studies:
            record = study.get("Study", {})
            trial_info = {
                "nct_id": record.get("ProtocolSection", {}).get("IdentificationModule", {}).get("NCTId", ""),
                "title": record.get("ProtocolSection", {}).get("IdentificationModule", {}).get("BriefTitle", ""),
                "inclusion": record.get("ProtocolSection", {}).get("EligibilityModule", {}).get("InclusionCriteria", ""),
                "exclusion": record.get("ProtocolSection", {}).get("EligibilityModule", {}).get("ExclusionCriteria", "")
            }
            if trial_info["nct_id"]:
                trials.append(trial_info)
        return trials
