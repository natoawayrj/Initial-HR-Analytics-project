# 📊 HR Analytics - Turnover Analysis

> ⚠️ Este projeto representa a versão inicial (v1) e será evoluído com melhorias estruturais e analíticas.

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

## ⚠️ Limitações da versão atual (v1)

* Código ainda não modularizado (funções)
* Repetição em algumas análises e visualizações
* ETL e EDA ainda não totalmente separados
* Pipeline de dados ainda não estruturado

---

## 🚀 Próximos passos (v2)

* Refatorar o código em funções reutilizáveis
* Separar pipeline de ETL e análise
* Melhorar organização do notebook
* Aprofundar análise orientada a negócio
* Evoluir para um modelo preditivo de turnover

---

## 📁 Estrutura do projeto

* `ProjetoRH.ipynb` → notebook principal com ETL e análise
* `dataset/` → dados utilizados no projeto

---

## 👨‍💻 Autor

Renato Lázaro Santos Batista
🔗 [LinkedIn](https://www.linkedin.com/in/renato-santos1978/)
