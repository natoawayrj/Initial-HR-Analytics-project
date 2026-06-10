"""Exporta arquivos CSV prontos para consumo no Power BI.

Gera, na pasta dataset/bi/:

- bi_candidatos.csv ............ tabela fato com os dados limpos (experience
                                 numérica e rótulo legível do target)
- bi_taxa_target_categoria.csv . formato longo: taxa de evasão por categoria
                                 de cada variável categórica
- bi_woe_iv.csv ................ WOE por categoria de cada variável
- bi_iv_resumo.csv ............. IV por variável com classificação do poder preditivo
- bi_correlacao_spearman.csv ... matriz de correlação em formato longo

Uso: python -m src.exportar_bi
"""

import os

import numpy as np
import pandas as pd

from src import eda, etl

# Variáveis categóricas nominais usadas no WOE/IV (mesma lista da EDA)
COLUNAS_CATEGORICAS_IV = [
    'gender',
    'relevent_experience',
    'enrolled_university',
    'education_level',
    'major_discipline',
    'company_type',
]

# Variáveis categóricas presentes no dataset limpo
COLUNAS_CATEGORICAS_LIMPO = [
    'enrolled_university',
    'relevent_experience',
    'education_level',
    'company_type',
    'major_discipline',
]


def classificar_iv(iv):
    """Classifica o poder preditivo segundo a tabela de referência do IV."""
    if iv < 0.02:
        return 'Não usar para previsão'
    if iv < 0.1:
        return 'Preditor fraco'
    if iv < 0.3:
        return 'Preditor médio'
    if iv < 0.5:
        return 'Preditor forte'
    return 'Bom demais para ser verdade'


def exportar_csv_bi(caminho_entrada='dataset/aug_train.csv', pasta_saida='dataset/bi'):
    """Gera todos os CSVs de apoio ao dashboard de BI e retorna os caminhos gravados."""
    os.makedirs(pasta_saida, exist_ok=True)
    gerados = []

    df_bruto = etl.carregar_dados(caminho_entrada)
    df_limpo = etl.pipeline_etl(caminho_entrada)

    # 1. Tabela fato: dados limpos com colunas amigáveis para o BI
    df_bi = df_limpo.copy()
    df_bi['experience'] = df_bi['experience'].replace({'<1': 1, '>20': 21}).astype(float)
    df_bi['target_label'] = np.where(df_bi['target'] == 1,
                                     'Procurando novo emprego',
                                     'Não procurando emprego')
    caminho = os.path.join(pasta_saida, 'bi_candidatos.csv')
    df_bi.to_csv(caminho, index=False)
    gerados.append(caminho)

    # 2. Taxa de evasão por categoria (formato longo, ideal para visuais de barra)
    linhas = []
    for col in COLUNAS_CATEGORICAS_LIMPO:
        grupo = df_bi.groupby(col)['target'].agg(['count', 'sum', 'mean']).reset_index()
        for _, linha in grupo.iterrows():
            linhas.append({
                'variavel': col,
                'categoria': linha[col],
                'total_candidatos': int(linha['count']),
                'procurando_emprego': int(linha['sum']),
                'taxa_evasao': round(linha['mean'], 4),
            })
    df_taxa = pd.DataFrame(linhas)
    caminho = os.path.join(pasta_saida, 'bi_taxa_target_categoria.csv')
    df_taxa.to_csv(caminho, index=False)
    gerados.append(caminho)

    # 3. WOE por categoria de cada variável (calculado sobre os dados brutos, como na EDA)
    woe_frames = []
    for col in COLUNAS_CATEGORICAS_IV:
        df_woe = eda.calcular_woe_iv(df_bruto, col).reset_index()
        df_woe = df_woe.rename(columns={col: 'categoria',
                                        0: 'proporcao_target_0',
                                        1: 'proporcao_target_1'})
        df_woe.insert(0, 'variavel', col)
        woe_frames.append(df_woe)
    df_woe_total = pd.concat(woe_frames, ignore_index=True)
    caminho = os.path.join(pasta_saida, 'bi_woe_iv.csv')
    df_woe_total.to_csv(caminho, index=False)
    gerados.append(caminho)

    # 4. Resumo do IV por variável com classificação
    df_iv = eda.calcular_iv_features(df_bruto, COLUNAS_CATEGORICAS_IV).reset_index()
    df_iv['classificacao'] = df_iv['iv'].apply(classificar_iv)
    df_iv = df_iv.rename(columns={'Features': 'variavel'})
    caminho = os.path.join(pasta_saida, 'bi_iv_resumo.csv')
    df_iv.to_csv(caminho, index=False)
    gerados.append(caminho)

    # 5. Correlação de Spearman em formato longo (variavel_1, variavel_2, correlacao)
    df_num = etl.converter_variaveis_numericas(df_bruto)
    corr = (df_num.drop(columns=['enrollee_id'])
            .corr(method='spearman', numeric_only=True))
    df_corr = (corr.stack().reset_index())
    df_corr.columns = ['variavel_1', 'variavel_2', 'correlacao']
    df_corr['correlacao'] = df_corr['correlacao'].round(4)
    caminho = os.path.join(pasta_saida, 'bi_correlacao_spearman.csv')
    df_corr.to_csv(caminho, index=False)
    gerados.append(caminho)

    return gerados


if __name__ == '__main__':
    for arquivo in exportar_csv_bi():
        print('Gerado:', arquivo)
