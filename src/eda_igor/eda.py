# -*- coding: utf-8 -*-
"""
EDA rápida e padronizada
- Lê CSV (ou use run_eda(df)) e gera um conjunto de análises:
  * nulos, duplicatas, dtypes, estatísticas descritivas
  * histogramas, QQ-plots, boxplots
  * normalidade (D'Agostino/Shapiro) e outliers (IQR)
  * correlação entre variáveis numéricas
  * resumo textual com achados e próximos passos (eda_resumo.txt)
"""

import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def assess_normality(series: pd.Series, alpha=0.05, sample_cap=5000):
    """
    Avalia normalidade:
      - D'Agostino K² (n>=20) ou Shapiro-Wilk (n<20)
      - Retorna skew, kurtosis, p-valor e flag is_normal
    """
    s = series.dropna().astype(float)
    n = len(s)
    result = {"n": n, "skew": float(s.skew()), "kurtosis": float(s.kurtosis())}
    if n < 3:
        result.update({"test": "insufficient_data", "p_value": np.nan, "is_normal": False})
        return result

    x = s.values
    # Cap de tamanho para performance
    if n > sample_cap:
        rng = np.random.default_rng(42)
        x = rng.choice(x, size=sample_cap, replace=False)

    try:
        if len(x) >= 20:
            stat, p = stats.normaltest(x, nan_policy="omit")
            test = "D'Agostino K²"
        else:
            stat, p = stats.shapiro(x)
            test = "Shapiro–Wilk"
        result.update({"test": test, "stat": float(stat), "p_value": float(p), "is_normal": bool(p >= alpha)})
    except Exception as e:
        result.update({"test": "failed", "p_value": np.nan, "is_normal": False, "error": str(e)})
    return result

def outlier_summary(series: pd.Series):
    """Resumo de outliers pelo método IQR (1.5*IQR)."""
    s = series.dropna().astype(float)
    if s.empty:
        return {"iqr_low": np.nan, "iqr_high": np.nan, "n_outliers": 0}
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    n_out = int(((s < low) | (s > high)).sum())
    return {"iqr_low": float(low), "iqr_high": float(high), "n_outliers": n_out}


def sigma_intervals(df, num_cols, mu_sigma_table=True):
    """
    Cria tabela com intervalos de sigma para cada coluna numérica.
    Representatividade: 0.5σ ≈ 38%, 1σ ≈ 68%, 2σ ≈ 95%, 3σ ≈ 99.7%
    """
    perc_map = {0.5: "≈38%", 1: "≈68%", 2: "≈95%", 3: "≈99.7%"}
    rows = []
    for c in num_cols:
        serie = df[c].dropna().astype(float)
        if serie.empty:
            continue
        mu = serie.mean()
        sigma = serie.std()
        for k in [0.5, 1, 2, 3]:
            low, high = mu - k*sigma, mu + k*sigma
            rows.append({
                "coluna": c,
                "σ": f"{k}σ ({perc_map[k]})",
                "intervalo": f"[{low:.2f}, {high:.2f}]"
            })
    return pd.DataFrame(rows)

def run_eda(
    df: pd.DataFrame,
    dataset_name: str = "dataset",
    alpha: float = 0.05,
    max_numeric_plots: int = 12,
    top_k_cat: int = 15,
    save_summary_path: str = "eda_resumo.txt",
    
):
    """Executa a EDA completa em um DataFrame."""
    report_lines = []
    report_lines.append(f"EDA para: {dataset_name}")
    report_lines.append(f"Formato: {df.shape[0]} linhas × {df.shape[1]} colunas")
    report_lines.append("")

    # Dtypes
    dtypes = df.dtypes.astype(str)
    info_df = pd.DataFrame({"column": df.columns, "dtype": dtypes.values})
    print("\n[Tipos de dados]\n", info_df)

    # Nulos
    na_counts = df.isna().sum().sort_values(ascending=False)
    na_pct = (na_counts / len(df) * 100).round(2)
    na_df = pd.DataFrame({"missing_count": na_counts, "missing_pct": na_pct})
    print("\n[Valores ausentes por coluna]\n", na_df.head(20))

    n_missing_cols = int((na_counts > 0).sum())
    report_lines.append(f"Colunas com valores ausentes: {n_missing_cols} de {df.shape[1]}")
    top_missing = na_df[na_df["missing_count"] > 0].head(5)
    if not top_missing.empty:
        report_lines.append("Top colunas com mais ausências:")
        for c, row in top_missing.iterrows():
            report_lines.append(f"  - {c}: {int(row['missing_count'])} ({row['missing_pct']}%)")
    report_lines.append("")

    # Duplicadas
    dup_rows = int(df.duplicated().sum())
    report_lines.append(f"Linhas duplicadas: {dup_rows}")
    report_lines.append("")

    # Split numérico x categórico
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]

    # Estatísticas numéricas
    if num_cols:
        desc = df[num_cols].describe().T
        print("\n[Estatísticas descritivas]\n", desc)
        report_lines.append(f"Colunas numéricas: {len(num_cols)} → {', '.join(num_cols[:8])}{'…' if len(num_cols)>8 else ''}")
    else:
        report_lines.append("Não há colunas numéricas.")
    report_lines.append("")

    # Resumo categóricas
    if cat_cols:
        rows = []
        for c in cat_cols:
            vc = df[c].astype(str).value_counts(dropna=False)
            top = dict(vc.head(top_k_cat))
            rows.append({"coluna": c, "n_categorias": int(vc.nunique()), "n_registros": int(vc.sum()), "top": list(top.items())[:5]})
        cat_df = pd.DataFrame(rows)
        print("\n[Resumo categóricas]\n", cat_df)
        report_lines.append(f"Colunas categóricas: {len(cat_cols)} → {', '.join(cat_cols[:8])}{'…' if len(cat_cols)>8 else ''}")
        report_lines.append("")

    # Normalidade e outliers
    normality_rows = []
    for c in num_cols:
        norm_res = assess_normality(df[c], alpha=alpha)
        out_res = outlier_summary(df[c])
        normality_rows.append({
            "coluna": c, "n": norm_res["n"], "skew": norm_res["skew"],
            "kurtosis": norm_res["kurtosis"], "teste": norm_res.get("test"),
            "p_valor": norm_res.get("p_value"), "aparenta_normal": norm_res.get("is_normal"),
            "iqr_low": out_res["iqr_low"], "iqr_high": out_res["iqr_high"],
            "n_outliers_IQR": out_res["n_outliers"]
        })
    if normality_rows:
        normality_df = pd.DataFrame(normality_rows).set_index("coluna")
        print("\n[Normalidade e Outliers]\n", normality_df)

    # Plots: Histograma
    if num_cols:
        to_plot = num_cols[:max_numeric_plots]
        for c in to_plot:
            data = df[c].dropna().values
            if data.size == 0:
                continue
            plt.figure(figsize=(8, 5))
            plt.hist(data, bins="auto")
            plt.title(f'Histograma - {c}')
            plt.xlabel(c); plt.ylabel('Frequência')
            plt.show()

    # QQ-plot
    if num_cols:
        to_plot = num_cols[: min(6, len(num_cols))]
        for c in to_plot:
            data = df[c].dropna().values
            if data.size < 3:
                continue
            plt.figure(figsize=(8, 5))
            stats.probplot(data, dist="norm", plot=plt)
            plt.title(f'QQ-plot - {c} (Normal teórica)')
            plt.xlabel('Quantis teóricos'); plt.ylabel('Quantis da amostra')
            plt.show()

    # Boxplot
    if num_cols:
        to_plot = num_cols[: min(8, len(num_cols))]
        for c in to_plot:
            data = df[c].dropna().values
            if data.size == 0:
                continue
            plt.figure(figsize=(6, 5))
            plt.boxplot(data, vert=True, showmeans=True)
            plt.title(f'Boxplot - {c}')
            plt.ylabel(c)
            plt.show()

    # Correlação
    if len(num_cols) >= 2:
        corr = df[num_cols].corr(numeric_only=True)
        plt.figure(figsize=(8, 6))
        plt.imshow(corr, interpolation="nearest")
        plt.xticks(range(len(num_cols)), num_cols, rotation=90)
        plt.yticks(range(len(num_cols)), num_cols)
        plt.colorbar()
        plt.title("Matriz de Correlação (numéricas)")
        plt.tight_layout()
        plt.show()
        print("\n[Matriz de Correlação]\n", corr)

    # Resumo e próximos passos
    warnings_list = []
    if dup_rows > 0:
        warnings_list.append(f"{dup_rows} linhas duplicadas")
    if n_missing_cols > 0:
        warnings_list.append(f"{n_missing_cols} colunas com ausências")
    if num_cols:
        non_normal = []
        many_outliers = []
        if normality_rows:
            normality_df = pd.DataFrame(normality_rows).set_index("coluna")
            non_normal = [c for c in num_cols if not bool(normality_df.loc[c, "aparenta_normal"])]
            many_outliers = [c for c in num_cols if int(normality_df.loc[c, "n_outliers_IQR"]) > 0]
        if non_normal:
            warnings_list.append(f"{len(non_normal)}/{len(num_cols)} colunas numéricas não parecem normais (α={alpha})")
        if many_outliers:
            warnings_list.append(f"Outliers pelo IQR em {len(many_outliers)} colunas numéricas")

    if warnings_list:
        report_lines.append("⚠️ Alertas potenciais:")
        for w in warnings_list:
            report_lines.append(f" - {w}")
        report_lines.append("")

    report_lines.append("Sugestões próximas etapas:")
    if n_missing_cols > 0:
        report_lines.append(" - Tratar ausências (imputação por média/mediana/moda ou modelos); avaliar descartar colunas com muita ausência.")
    if dup_rows > 0:
        report_lines.append(" - Remover/justificar duplicatas; investigar chaves primárias.")
    if num_cols:
        report_lines.append(" - Para colunas não normais: transformação (log/Box-Cox) ou métodos não paramétricos.")
        report_lines.append(" - Padronizar/normalizar variáveis para modelos sensíveis à escala.")
    if len(num_cols) >= 2:
        report_lines.append(" - Verificar colinearidade; usar regularização ou redução de dimensionalidade se necessário.")

    report_text = "\n".join(report_lines)

    if num_cols:
        sigma_df = sigma_intervals(df, num_cols)
    
    print("\n[Intervalos de Sigma]\n", sigma_df)
    report_lines.append("\nTabela de intervalos de Sigma adicionada (0,5σ, 1σ, 2σ, 3σ).")

        
    with open(save_summary_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(report_text)

        # Dentro do run_eda, no final:
        
    return report_text

# --------------------- Exemplo de uso -----------------------
if __name__ == "__main__":
    # 1) Rodar em um CSV local:
    # df = pd.read_csv("seu_arquivo.csv")
    # run_eda(df, dataset_name="seu_arquivo.csv")

    # 2) Ou detectar automaticamente o maior CSV do diretório atual:
    path = 'YOUR_PATH + FILE'
    df = pd.read_excel(path)
    
    run_eda(df, dataset_name=os.path.basename(path))