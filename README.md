# 📊 Exploratory Data Analysis (EDA) Module  

*This module was created by **Igor GTDS***  
*Este módulo foi criado por **Igor GTDS***  

---

## 🚀 What this module does  

Run the module to perform an **exploratory data analysis (EDA)** with the following steps:  

- ✅ Checks **data types** and **sample size**  
- ✅ Counts **null values** and **duplicates**  
- ✅ Computes **descriptive statistics**  
- ✅ Generates **histograms, QQ-plots, boxplots, correlation matrix**  
- ✅ Tests **normality** (D’Agostino / Shapiro)  
- ✅ Detects **outliers** using **IQR**  
- ✅ Summarizes results into a **textual report with next steps**  

---

## 📄 Example of report output  

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

```

# 📌 Normalidade e Outliers (variáveis numéricas)

Quando analisamos colunas numéricas, é importante entender:

- Se os dados seguem uma **distribuição normal** (curva em formato de sino).  
- Se existem valores fora do padrão esperado (**outliers**).  

---

## 🔹 Skew (Assimetria)

Mede o quanto a distribuição é **simétrica ou não**.  

**Valores:**
- `0` → distribuição simétrica (como a normal)  
- `Positivo` → cauda mais longa à direita (ex.: salários, muitos baixos e poucos muito altos)  
- `Negativo` → cauda mais longa à esquerda  

👉 **Exemplo:**  
Se o tempo até falha de um componente tem muitos valores pequenos e poucos casos muito grandes → **skew positivo**.  

---

## 🔹 Kurtosis (Curtose)

Mede o **"achatamento" ou "pontiagudo"** da distribuição.  

**Valores:**
- `0` (na escala *excess kurtosis*) → parecido com normal  
- `> 0` → mais pontuda (dados concentrados no meio e caudas longas → mais outliers)  
- `< 0` → mais achatada (dados mais espalhados)  

👉 **Exemplo:**  
Se uma peça quase sempre falha perto da média, mas às vezes dura MUITO mais → **curtose alta**.  

---

## 🔹 Teste de normalidade

São testes estatísticos que verificam se os dados podem ser considerados **normais**.  

- **Shapiro-Wilk** → bom para amostras pequenas (< 20)  
- **D’Agostino K²** → bom para amostras maiores  

👉 **Interpretação dos resultados:**
- `p-value > 0,05` → não rejeitamos H₀ → distribuição pode ser considerada normal  
- `p-value ≤ 0,05` → rejeitamos H₀ → distribuição **não é normal**  

---

## 🔹 p-value

- Probabilidade de observarmos os dados se a **hipótese nula (H₀)** fosse verdadeira (no caso, que os dados são normais).  
- Quanto **menor o p**, maior a **evidência contra a normalidade**.  

---

## 🔹 Outliers – IQR (Interquartile Range)

Método baseado em **quartis**:  
- `Q1 = 25%`  
- `Q3 = 75%`  
- `IQR = Q3 – Q1`  

**Definição de outliers:**
- Valores `< Q1 – 1,5 × IQR`  
- Valores `> Q3 + 1,5 × IQR`  

👉 **No relatório:**  
- `iqr_low` = limite inferior  
- `iqr_high` = limite superior  
- `n_outliers` = quantidade de pontos fora desses limites  

---

# 📌 Exemplo prático (idade dos funcionários)

- Média = `40 anos`  
- Skew = `0,2` → quase simétrica  
- Kurtosis = `–0,5` → distribuição mais achatada que a normal  
- Teste de normalidade: `p = 0,12 (>0,05)` → pode ser considerada normal  
- Quartis: `Q1 = 30`, `Q3 = 50` → `IQR = 20`  
  - `iqr_low = 30 – 1,5×20 = 0`  
  - `iqr_high = 50 + 1,5×20 = 80`  
- Outliers = idade `< 0` (impossível) ou `> 80`  

---

## ✅ Resumindo

- **Skew/Kurtosis** → descrevem a forma da curva  
- **Teste + p-value** → indicam se pode ser considerada normal  
- **IQR (low/high)** → ajudam a identificar outliers numéricos  

