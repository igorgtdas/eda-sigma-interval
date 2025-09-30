import os
import pandas as pd
from eda_igor import assess_normality, outlier_summary, sigma_intervals, run_eda

# --------------------- Exemplo de uso -----------------------
if __name__ == "__main__":
    # 1) Rodar em um CSV local:
    # df = pd.read_csv("seu_arquivo.csv")
    # run_eda(df, dataset_name="seu_arquivo.csv")

    # 2) Ou detectar automaticamente o maior CSV do diretório atual:
    path = 'C:/Users/igtsilva/OneDrive - GOL Linhas Aéreas S A/Área de Trabalho/Igor - Reliability/Local_data_bases/info_acft.xlsx'
    df = pd.read_excel(path)
    
    run_eda(df, dataset_name=os.path.basename(path))