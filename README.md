# 📊 HR Analytics - Turnover Analysis

> ✅ Versão atual: **v2** — código refatorado em módulos reutilizáveis, com pipeline de ETL separado da análise. O notebook da v1 foi mantido para referência histórica.

---

## 🎯 Objetivo

Este projeto tem como objetivo analisar os fatores que influenciam o turnover de funcionários, utilizando técnicas de ETL, análise exploratória de dados (EDA) e métodos estatísticos.

---

## 📌 Problema de negócio

Altas taxas de turnover geram custos significativos para empresas, impactando diretamente produtividade, retenção de talentos e custos operacionais.
Este projeto busca identificar padrões e variáveis associadas à saída de funcionários, auxiliando na tomada de decisão.

---

## 🛠️ Tecnologias utilizadas

* Python
* Pandas
* NumPy
* Seaborn / Matplotlib
* Scipy

---

## 🔄 Etapas do projeto

* Limpeza e tratamento de dados (ETL)
* Análise exploratória de dados (EDA)
* Tratamento de valores ausentes com base em regras de negócio
* Conversão de variáveis categóricas
* Análise de distribuição das variáveis
* Análise de correlação (Spearman)
* Aplicação de WOE (Weight of Evidence) e IV (Information Value)

---

## 📊 Insights

* Funcionários com menor experiência apresentam maior tendência de saída
* Algumas variáveis relacionadas à educação demonstram relação com o turnover
* Nem todas as variáveis analisadas possuem impacto significativo
* Variáveis categóricas apresentaram potencial preditivo relevante (WOE/IV)

---

## 💡 Impacto

Os resultados desta análise podem auxiliar equipes de RH a:

* Identificar grupos com maior risco de saída
* Direcionar estratégias de retenção de talentos
* Melhorar a tomada de decisão baseada em dados

---

## 📈 Técnicas utilizadas

* Correlação de Spearman (adequada para dados não paramétricos)
* Weight of Evidence (WOE)
* Information Value (IV)
* Análise de distribuição e comportamento das variáveis

---

## ✨ O que mudou na v2

* ✅ Código refatorado em funções reutilizáveis (`src/etl.py` e `src/eda.py`)
* ✅ Pipeline de ETL separado da análise — uma única chamada (`etl.pipeline_etl`) executa toda a limpeza e grava o dataset limpo
* ✅ Notebook reorganizado em seções claras: Carga → EDA → ETL → Verificação → Relatório
* ✅ Correção de bug da v1: a imputação de `major_discipline` sobrescrevia linhas inteiras com `Other` em vez de apenas a coluna

---

## 🚀 Próximos passos (v3)

* Aprofundar análise orientada a negócio
* Evoluir para um modelo preditivo de turnover (atenção ao desbalanceamento do target)

---

## 📁 Estrutura do projeto

* `ProjetoRH_v2.ipynb` → notebook principal (v2), usa os módulos de `src/`
* `src/etl.py` → pipeline de ETL em funções reutilizáveis (carga, imputação por regras de negócio, gravação)
* `src/eda.py` → funções de análise exploratória (plots, normalidade, Spearman, WOE/IV)
* `ProjetoRH.ipynb` → notebook da v1 (mantido para referência)
* `Dashboard_ProjetoRH.html` → dashboard interativo com os principais insights
* `Features.txt` → descrição das variáveis do dataset
* `dataset/` → dados utilizados no projeto (inclui `rh_candidatos_limpo.csv` gerado pelo pipeline)

---

## 👨‍💻 Autor

Renato Lázaro Santos Batista
🔗 [LinkedIn](https://www.linkedin.com/in/renato-santos1978/)
