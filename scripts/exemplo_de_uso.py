import os
import pandas as pd
from eda_igor import assess_normality, outlier_summary, sigma_intervals, run_eda

# --------------------- Exemplo de uso -----------------------
if __name__ == "__main__":
    file = 'your_file.xlsx'    #-- Trocar para o nome do seu arquivo
    df = pd.read_excel(file)
    
    run_eda(df, dataset_name=os.path.basename(path))
