import pandas as pd
import numpy as np

def calculate_copras(df_alternatives, weights, benefit_criteria, cost_criteria):
    
    # Pisahkan nama alternatif dari data kriteria
    alternatives = df_alternatives.iloc[:, 0].tolist()
    criteria_data = df_alternatives.iloc[:, 1:].values
    criteria_names = df_alternatives.columns[1:].tolist()

    # Pastikan jumlah bobot sama dengan jumlah kriteria
    if len(weights) != len(criteria_names):
        raise ValueError("Jumlah bobot tidak sesuai dengan jumlah kriteria.")

    # Ubah bobot ke dalam array numpy sesuai urutan kriteria_names
    weights_array = np.array([weights[c] for c in criteria_names])

    # --- Langkah 1: Normalisasi Matriks Keputusan ---
    normalized_matrix = np.zeros_like(criteria_data, dtype=float)
    for j in range(criteria_data.shape[1]):
        col_sum = np.sum(criteria_data[:, j])
        normalized_matrix[:, j] = criteria_data[:, j] / col_sum

    # --- Langkah 2: Pembobotan Matriks Normalisasi ---
    weighted_normalized_matrix = normalized_matrix * weights_array

    # --- Langkah 3: Perhitungan Jumlah Terbobot Kriteria Keuntungan (Si+) dan Biaya (Si-) ---
    Si_plus = np.zeros(weighted_normalized_matrix.shape[0])
    Si_minus = np.zeros(weighted_normalized_matrix.shape[0])

    for i in range(weighted_normalized_matrix.shape[0]):
        for j, crit_name in enumerate(criteria_names):
            if crit_name in benefit_criteria:
                Si_plus[i] += weighted_normalized_matrix[i, j]
            elif crit_name in cost_criteria:
                Si_minus[i] += weighted_normalized_matrix[i, j]
            else:
                raise ValueError(f"Kriteria '{crit_name}' tidak didefinisikan sebagai benefit atau cost.")

    # --- Langkah 4: Perhitungan Prioritas Relatif (Qi) ---
    epsilon = 1e-9
    Q_i = Si_plus + (np.sum(Si_minus) / (Si_minus + epsilon))

    # --- Langkah 5: Perhitungan Utilitas Relatif (Ni) ---
    Q_max = np.max(Q_i)
    N_i = (Q_i / Q_max) * 100

    # --- Langkah 6: Perangkingan Alternatif ---
    df_results = pd.DataFrame({
        'Alternatif': alternatives,
        'Si+': Si_plus,
        'Si-': Si_minus,
        'Qi': Q_i,
        'Ni (%)': N_i
    })

    df_ranked = df_results.sort_values(by='Ni (%)', ascending=False).reset_index(drop=True)
    df_ranked['Ranking'] = df_ranked.index + 1

    return df_ranked, df_results