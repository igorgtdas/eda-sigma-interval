*This module was created by Igor GTDS*

Run it to make a esploratory analyses as:

Verifica tipos de dados, tamanho da amostra;
Conta nulos e duplicatas;
Calcula estatísticas descritivas;
Faz histogramas, QQ-plots, boxplots e matriz de correlação;
Testa normalidade (D’Agostino/Shapiro) e identifica outliers (IQR);
Resume tudo em um relatório textual com próximos passos.


*Para 

*The EDA will return a report in texts format as below:*

EDA para: demo_dataset.csv
Formato: 1001 linhas × 6 colunas

Colunas com valores ausentes: 2 de 6
Top colunas com mais ausências:
  - peso_kg: 50 (5.0%)
  - cidade: 25 (2.5%)

Linhas duplicadas: 1

Colunas numéricas: 4 → altura_cm, peso_kg, salario, idade

Colunas categóricas: 2 → sexo, cidade

⚠️ Alertas potenciais:
 - 1 linhas duplicadas
 - 2 colunas com ausências
 - 2/4 colunas numéricas não parecem normais (α=0.05)
 - Outliers detectados via IQR em 3 colunas numéricas

Sugestões próximas etapas:
 - Tratar ausências: imputação (média/mediana/moda) ou model-based; avaliar exclusão de colunas com muita ausência.
 - Remover/justificar duplicatas totais; investigar chaves primárias.
 - Para colunas não normais: considerar transformação (log/Box-Cox) ou métodos não paramétricos.
 - Padronizar/normalizar variáveis se for usar modelos sensíveis à escala.
 - Avaliar colinearidade; reduzir dimensionalidade ou regularização se necessário.
