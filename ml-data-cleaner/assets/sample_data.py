import pandas as pd
import numpy as np

# DATASET DE PRUEBA PARA ML-DATA-CLEANER
# Contiene: Nulos, Outliers, Tipos incorrectos y Desbalance.

data = {
    'id': range(1, 101),
    'edad': [25, 30, np.nan, 45, 200, 18, 34, 29, 40, np.nan] * 10,
    'ingresos': np.random.normal(50000, 15000, 100).tolist(),
    'fecha_registro': ['2023-01-01', 'error_date', '2023-02-15'] * 33 + ['2023-01-01'],
    'target': [0] * 95 + [1] * 5  # Desbalance extremo
}

df = pd.DataFrame(data)

# Añadir nulos aleatorios en ingresos
df.loc[df.sample(frac=0.1).index, 'ingresos'] = np.nan

df.to_csv("test_dataset.csv", index=False)
print("✅ test_dataset.csv generado para pruebas de limpieza.")
