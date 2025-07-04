# 🧠 AI-Based Clinical Trial Matching System

## 🔍 Project Overview

This system uses AI and semantic similarity to match patients with clinical trials by:

* Extracting structured patient data (conditions, medications, allergies)
* Parsing inclusion/exclusion criteria from clinical trials
* Summarizing both patient profiles and trial criteria using an LLM (OpenRouter API)
* Matching them via vector similarity and LLM-based validation

Supports both:

* Structured trial data (`trials.csv`)
* Web-scraped data (stored as CSV supplementally)

---

## 🧱 System Architecture

```bash
Patient Data (CSV) ──▶ SQLite DB ──▶ LLM Summary
                                │
Trial Data (CSV / Scraped) ─────┘
      │                                
Vector Embedding (SentenceTransformer)
      │
      ▼
  Matching + Scoring
      ▼
  JSON Output (per patient)
      ▼
  Flask UI (upload, trigger, view)
```

---

## 🧰 Technologies Used

* Python
* Flask (frontend)
* SQLite + Pandas
* SentenceTransformer (MiniLM)
* OpenRouter LLM API (deepseek/deepseek-r1-0528-qwen3-8b)
* dotenv, requests, json

---

## 📁 Folder Structure

```bash
AI_Clinical_Trial_Matching_System/
├── app.py                 # Flask app
├── main.py               # CLI-based pipeline entry point
├── templates/             # HTML frontend
│   ├── index.html
│   └── results.html
├── src/
│   ├── data/              # Ingestion logic (CSV, web scraping)
│   ├── llm/               # OpenRouter summarizer
│   ├── embedding/         # Embedding logic
│   ├── matching/          # Trial matcher
│   └── pipeline/          # Pipeline orchestration
├── data/
│   ├── patient_data/      # conditions.csv etc.
│   └── clinical_trials/   # trials.csv
├── output/
│   └── matched_trials/    # JSON results
├── .env                   # API key
├── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone & Create Environment

```bash
git clone <repo_url>
cd AI_Clinical_Trial_Matching_System
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

---

## 🚀 How to Use (Option 1: Flask UI)

### 1. Start the Flask App

```bash
python app.py
```

Go to [http://localhost:5000](http://localhost:5000)

### 2. Upload CSV Files

* Patient CSV: `conditions.csv`
* Trials CSV: `trials.csv`

You can use [this sample patient data](https://mitre.box.com/shared/static/aw9po06ypfb9hrau4jamtvtz0e5ziucz.zip).

### 3. Trigger Matching

* Press "Run Matching"
* This will:

  * Convert patient CSV to SQLite
  * Summarize patient + trial data
  * Match using vector similarity and LLM
  * Output JSON to `output/matched_trials/`

### 4. View Results

* Results are shown in the browser
* LLM will mark `✅ Eligible`, `❌ Not Eligible`, or `⚠️ Uncertain`

---

## 🧪 Option 2: Run Matching Without UI

You can also run the system directly using preloaded data:

### 1. Prepare Data

Place your files like so:

```bash
data/patient_data/conditions.csv
data/clinical_trials/trials.csv
```

> You can also let the system **scrape trials from ClinicalTrials.gov**.(API not available in some regions)

The scraping logic uses default trial URLs from:

```python
src/data/web_scraper_trials.py
```

🔧 **To change the scraping source**, modify the base URL or logic in that file.

---

### 2. Run via Command Line

```bash
python main.py
```

This will:

* Convert patient data to SQLite
* Scrape & load trial data
* Summarize all inputs
* Match and score trials
* Save results to `output/matched_trials/`

---

## 📦 Sample Output Format

```json
[
  {
    "nct_id": "NCT100001",
    "title": "Hypertension Drug Study",
    "eligible": false,
    "reason": "The patient does not meet age requirement."
  }
]
```

---

## 🛠 Troubleshooting

### ❌ 401 Unauthorized

Check your `.env` file contains a valid API key:

```bash
OPENROUTER_API_KEY=your_key
```

### ⚠️ Expecting value: line 1 column 1

This means LLM returned empty or invalid JSON. Common causes:

* Invalid or missing prompts
* API quota exceeded
* Missing patient age or clinical criteria

---

## 🧠 Future Improvements

* Caching for LLM calls
* Custom prompt tuning per disease category
* UI for manual feedback & flagging
* Export to CSV, Excel, Sheets
* Support for multi-patient batch processing

---

## 📜 License

MIT

---

