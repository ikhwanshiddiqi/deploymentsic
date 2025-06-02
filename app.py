from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error_message = None
    if request.method == 'POST':
        try:
            dataset = request.form['dataset']
            model_name = request.form['model']
            days_ahead = int(request.form['days_ahead'])

            data_file = f"dataset/{dataset}.csv"
            df = pd.read_csv(data_file)
            
            if 'Close' not in df.columns:
                raise ValueError("File dataset tidak memiliki kolom 'Close'")
            
            last_30_prices = df['Close'].tail(30).values
            if len(last_30_prices) < 30:
                raise ValueError("Dataset tidak cukup untuk 30 data harga terakhir.")
            
            scaler = pickle.load(open(f'scaler/scaler_{dataset}.pkl', 'rb'))
            model = load_model(f'model/model_{model_name}_{dataset}.keras')
            
            input_seq_scaled = scaler.transform(last_30_prices.reshape(-1, 1)).reshape(1,30,1)
            preds = []
            for day in range(1, days_ahead+1):
                next_pred_scaled = model.predict(input_seq_scaled, verbose=0)[0][0]
                preds.append(next_pred_scaled)
                # Update window: hapus nilai pertama, tambahkan prediksi
                input_seq_scaled = np.append(input_seq_scaled[0,1:,0], next_pred_scaled).reshape(1,30,1)
            
            preds_inv = scaler.inverse_transform(np.array(preds).reshape(-1,1)).flatten()
            prediction = [(day, round(pred, 5)) for day, pred in zip(range(1, days_ahead+1), preds_inv)]

            historical_data = df['Close'].tail(500).values

            # Buat plot
            fig, ax = plt.subplots()

            x_historical = list(range(len(historical_data)))
            ax.plot(x_historical, historical_data, label='Historis 500 Data Terakhir', color='blue')

            pred_start = len(historical_data)
            x_pred = list(range(pred_start, pred_start + days_ahead))
            pred_values = [pred for day, pred in prediction]
            ax.plot(x_pred, pred_values, linestyle='--', color='red', label='Prediksi')

            ax.set_title(f'Prediksi Harga dengan 500 Data Historis Terakhir')
            ax.set_xlabel('Index Data (urutan waktu)')
            ax.set_ylabel('Harga')
            ax.legend()
            ax.grid(True)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_data = base64.b64encode(buf.getvalue()).decode('utf8')
            buf.close()

            return render_template('index.html', prediction=prediction, 
                       error_message=error_message, 
                       plot_data=plot_data,
                       dataset=dataset,
                       model_name=model_name,
                       days_ahead=days_ahead
                       )

        except Exception as e:
            error_message = str(e)
    return render_template('index.html', prediction=prediction, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)