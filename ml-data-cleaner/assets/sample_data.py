import pandas as pd
import numpy as np

def generate_sample_data(output_path="sample_dataset.csv"):
    """
    Genera un dataset sintético con problemas comunes:
    - Nulos (MCAR/MNAR)
    - Outliers
    - Desbalance de clases
    - Columnas irrelevantes (ID)
    """
    np.random.seed(42)
    n_rows = 1000
    
    data = {
        'id': range(n_rows),
        'age': np.random.normal(35, 10, n_rows),
        'income': np.random.normal(50000, 15000, n_rows),
        'category': np.random.choice(['A', 'B', 'C'], n_rows),
        'target': np.random.choice([0, 1], n_rows, p=[0.95, 0.05]) # Desbalance
    }
    
    df = pd.DataFrame(data)
    
    # Inyectar Nulos
    df.loc[df.sample(frac=0.1).index, 'age'] = np.nan
    df.loc[df.sample(frac=0.05).index, 'income'] = np.nan
    
    # Inyectar Outliers
    df.loc[0:5, 'income'] = 1000000
    
    df.to_csv(output_path, index=False)
    print(f"✓ Dataset de prueba generado en: {output_path}")

if __name__ == "__main__":
    generate_sample_data()
