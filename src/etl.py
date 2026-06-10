"""Pipeline de ETL do projeto HR Analytics.

Funções de carga, limpeza e tratamento de valores ausentes
com base nas regras de negócio definidas na análise (v1).
"""

import pandas as pd

# Colunas mantidas para a análise (definidas na v1 com base em WOE/IV e correlação)
COLUNAS_MANTER = [
    'city_development_index',
    'experience',
    'enrolled_university',
    'relevent_experience',
    'education_level',
    'company_type',
    'major_discipline',
    'target',
]


def carregar_dados(caminho):
    """Carrega o dataset a partir de um arquivo CSV."""
    return pd.read_csv(caminho)


def converter_variaveis_numericas(df):
    """Converte experience e last_new_job para float, em uma cópia do DataFrame.

    Regras: experience '<1' -> 1 e '>20' -> 21; last_new_job 'never' -> 0 e '>4' -> 5.
    """
    df_num = df.copy()
    df_num['experience'] = df_num['experience'].replace({'<1': 1, '>20': 21}).astype(float)
    df_num['last_new_job'] = df_num['last_new_job'].replace({'never': 0, '>4': 5}).astype(float)
    return df_num


def tratar_major_discipline(df):
    """Imputa major_discipline.

    Regra de negócio: quem tem education_level 'High School', 'Primary School'
    ou ausente não possui graduação, logo recebe 'Non Degree'.
    O restante dos ausentes recebe 'Other' (sem critério na documentação).
    """
    df = df.copy()
    sem_graduacao = df['major_discipline'].isna() & (
        df['education_level'].isin(['High School', 'Primary School'])
        | df['education_level'].isna()
    )
    df.loc[sem_graduacao, 'major_discipline'] = 'Non Degree'
    df['major_discipline'] = df['major_discipline'].fillna('Other')
    return df


def tratar_enrolled_university(df):
    """Imputa enrolled_university.

    Regra de negócio: candidatos com education_level 'Primary School' não estão
    qualificados para a universidade, logo recebem 'Primary Grad'.
    O restante dos ausentes recebe 'Other'. Também padroniza a categoria
    'no_enrollment' para 'No enrollment'.
    """
    df = df.copy()
    primario = df['enrolled_university'].isna() & (df['education_level'] == 'Primary School')
    df.loc[primario, 'enrolled_university'] = 'Primary Grad'
    df['enrolled_university'] = df['enrolled_university'].fillna('Other')
    df['enrolled_university'] = df['enrolled_university'].replace('no_enrollment', 'No enrollment')
    return df


def tratar_company_type(df):
    """Imputa company_type ausente com 'Other' (sem critério na documentação)."""
    df = df.copy()
    df['company_type'] = df['company_type'].fillna('Other')
    return df


def tratar_education_level(df):
    """Imputa education_level ausente com 'Other' (sem critério na documentação)."""
    df = df.copy()
    df['education_level'] = df['education_level'].fillna('Other')
    return df


def pipeline_etl(caminho_entrada, caminho_saida=None):
    """Executa o pipeline completo de ETL e retorna o DataFrame limpo.

    Etapas: carga -> seleção de colunas -> imputação por regras de negócio ->
    remoção dos ausentes restantes (experience, percentual irrisório) ->
    gravação opcional em CSV.

    A ordem importa: major_discipline depende dos NaN de education_level,
    por isso é tratada antes de education_level.
    """
    df = carregar_dados(caminho_entrada)
    df = df[COLUNAS_MANTER]
    df = tratar_major_discipline(df)
    df = tratar_enrolled_university(df)
    df = tratar_company_type(df)
    df = tratar_education_level(df)
    df = df.dropna()
    if caminho_saida:
        df.to_csv(caminho_saida, index=False)
    return df
