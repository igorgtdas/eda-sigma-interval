import os
import pandas as pd
from eda_igor import assess_normality, outlier_summary, sigma_intervals, run_eda

# --------------------- Exemplo de uso -----------------------
if __name__ == "__main__":
    # 1) Rodar em um CSV local:
    # df = pd.read_csv("seu_arquivo.csv")
    # run_eda(df, dataset_name="seu_arquivo.csv")

    # 2) Ou detectar automaticamente o maior CSV do diretório atual:
    path = 'YOURPATH+YOUR_FILE'
    df = pd.read_excel(path)
    
    run_eda(df, dataset_name=os.path.basename(path))
