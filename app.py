import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from copras_logic import calculate_copras 

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

CRITERIA_WEIGHTS = {
    'Pengalaman': 0.3,
    'Pendidikan': 0.2,
    'Usia': 0.2,
    'Status Perkawinan': 0.15,
    'Alamat': 0.15
}

if not (0.99 <= sum(CRITERIA_WEIGHTS.values()) <= 1.01):
    raise ValueError("Total bobot kriteria harus mendekati 1.0. Saat ini: " + str(sum(CRITERIA_WEIGHTS.values())))

BENEFIT_CRITERIA = [
    'Pengalaman',
    'Pendidikan',
    'Usia'
]

COST_CRITERIA = [
    'Status Perkawinan',
    'Alamat'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'csv_file' not in request.files:
        return render_template('index.html', error='Tidak ada bagian file dalam permintaan.')
    
    file = request.files['csv_file']
    
    if file.filename == '':
        return render_template('index.html', error='Tidak ada file yang dipilih.')
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Baca file CSV
            df_alternatives = pd.read_csv(filepath)

            if df_alternatives.columns[0] != 'Alternatif':
                return render_template('index.html', error='Kolom pertama CSV harus bernama "Alternatif".')

            missing_criteria = [c for c in CRITERIA_WEIGHTS.keys() if c not in df_alternatives.columns]
            if missing_criteria:
                return render_template('index.html', error=f"Kriteria berikut tidak ditemukan di CSV: {', '.join(missing_criteria)}. Harap sesuaikan file CSV atau konfigurasi bobot.")

            ordered_columns = ['Alternatif'] + list(CRITERIA_WEIGHTS.keys())
            df_alternatives = df_alternatives[ordered_columns]

            df_ranked, df_results = calculate_copras(df_alternatives, CRITERIA_WEIGHTS, BENEFIT_CRITERIA, COST_CRITERIA)

            csv_html = df_alternatives.to_html(classes='table table-striped text-center', index=False)
            ranked_html = df_ranked.to_html(classes='table table-striped text-center', index=False)
            results_html = df_results.to_html(classes='table table-striped text-center', index=False)

            os.remove(filepath)

            return render_template('index.html', csv_html=csv_html, ranked_html=ranked_html, results_html=results_html)

        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return render_template('index.html', error=f'Terjadi kesalahan saat memproses file: {e}')
    else:
        return render_template('index.html', error='File yang diunggah bukan CSV.')

if __name__ == '__main__':
    app.run(debug=True)