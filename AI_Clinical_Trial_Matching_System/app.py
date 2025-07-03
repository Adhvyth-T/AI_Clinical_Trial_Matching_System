# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
from src.pipeline.run_pipeline import run_matching_pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    match_files = []

    if request.method == 'POST':
        # Handle file uploads
        patient_file = request.files.get('patient_csv')
        trial_file = request.files.get('trial_csv')

        os.makedirs('data/patient_data', exist_ok=True)
        os.makedirs('data/clinical_trials', exist_ok=True)

        if patient_file:
            patient_df = pd.read_csv(patient_file)
            patient_df.to_csv('data/patient_data/conditions.csv', index=False)

        if trial_file:
            trial_df = pd.read_csv(trial_file)
            trial_df.to_csv('data/clinical_trials/trials.csv', index=False)

        # Run matching pipeline
        run_matching_pipeline()
        message = "Matching complete. You can now view results."

    match_dir = "output/matched_trials"
    if os.path.exists(match_dir):
        match_files = [f for f in os.listdir(match_dir) if f.endswith("_matches.json")]

    return render_template("index.html", message=message, match_files=match_files)


@app.route('/results/<filename>')
def results(filename):
    match_path = os.path.join("output/matched_trials", filename)
    with open(match_path, "r", encoding="utf-8") as f:
        import json
        results = json.load(f)
    return render_template("results.html", filename=filename, results=results)


if __name__ == '__main__':
    app.run(debug=True)
