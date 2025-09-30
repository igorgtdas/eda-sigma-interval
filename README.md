# 📊 Exploratory Data Analysis (EDA) Module  
# 📊 Módulo de Análise Exploratória de Dados (EDA)  

*This module was created by **Igor GTDS***  
*Este módulo foi criado por **Igor GTDS***  

---

## 🚀 What this module does  
## 🚀 O que este módulo faz  

Run the module to perform an **exploratory data analysis (EDA)** with the following steps:  
Rode o módulo para executar uma **análise exploratória de dados (EDA)** com as seguintes etapas:  

- ✅ Checks **data types** and **sample size**  
- ✅ Verifica **tipos de dados** e **tamanho da amostra**  

- ✅ Counts **null values** and **duplicates**  
- ✅ Conta **valores nulos** e **duplicatas**  

- ✅ Computes **descriptive statistics**  
- ✅ Calcula **estatísticas descritivas**  

- ✅ Generates **histograms, QQ-plots, boxplots, correlation matrix**  
- ✅ Gera **histogramas, QQ-plots, boxplots e matriz de correlação**  

- ✅ Tests **normality** (D’Agostino / Shapiro)  
- ✅ Testa **normalidade** (D’Agostino / Shapiro)  

- ✅ Detects **outliers** using **IQR**  
- ✅ Identifica **outliers** via **IQR**  

- ✅ Summarizes results into a **textual report with next steps**  
- ✅ Resume tudo em um **relatório textual com próximos passos**  

---

## 📄 Example of report output  
## 📄 Exemplo de saída do relatório  

```text
EDA for: demo_dataset.csv
Format: 1001 rows × 6 columns

Columns with missing values: 2 out of 6
Top columns with most missing:
  - peso_kg: 50 (5.0%)
  - cidade: 25 (2.5%)

Duplicate rows: 1

Numeric columns: 4 → altura_cm, peso_kg, salario, idade
Categorical columns: 2 → sexo, cidade

⚠️ Potential alerts:
 - 1 duplicate row
 - 2 columns with missing values
 - 2/4 numeric columns do not appear normal (α=0.05)
 - Outliers detected via IQR in 3 numeric columns

Suggested next steps:
 - Handle missing values: imputation (mean/median/mode) or model-based; consider dropping columns with too many missing values
 - Remove/justify duplicate rows; investigate primary keys
 - For non-normal columns: consider transformation (log/Box-Cox) or non-parametric methods
 - Standardize/normalize variables if using scale-sensitive models
 - Check for collinearity; use regularization or dimensionality reduction if needed
