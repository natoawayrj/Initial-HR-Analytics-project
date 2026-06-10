"""Funções de análise exploratória (EDA) do projeto HR Analytics.

Cada função encapsula uma visualização ou cálculo que na v1 era
repetido em várias células do notebook.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import normaltest


def _anotar_barras(ax, size=11):
    """Escreve a contagem acima de cada barra do gráfico."""
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'\n{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='baseline', color='black', size=size)


def plotar_categoricas(df, colunas, n_linhas=5, n_colunas=2, figsize=(18, 30)):
    """Countplot de cada variável categórica (NaN exibido como categoria)."""
    plt.figure(figsize=figsize)
    for i, col in enumerate(colunas, start=1):
        plt.subplot(n_linhas, n_colunas, i)
        ax = sns.countplot(data=df.fillna('NaN'), x=col, hue=col,
                           palette='bright', legend=False)
        plt.title(col, fontsize=15)
        _anotar_barras(ax, size=12)
        plt.xticks(rotation=45)
    plt.tight_layout(h_pad=2)
    plt.show()


def plotar_categorica(df, coluna, titulo=None):
    """Countplot de uma única variável categórica (NaN exibido como categoria)."""
    ax = sns.countplot(data=df.fillna('NaN'), x=coluna, hue=coluna,
                       alpha=0.7, edgecolor='black', legend=False)
    sns.despine()
    plt.xticks(rotation=45)
    _anotar_barras(ax, size=10)
    plt.title(titulo or f'{coluna}\n', fontsize=15)
    plt.show()


def plotar_distribuicao(df, colunas, cores=None):
    """Histograma + boxplot para cada variável numérica."""
    cores = cores or ['green', 'magenta', 'blue', 'orange']
    n = len(colunas)
    plt.figure(figsize=(17, 6 * n))
    for i, col in enumerate(colunas):
        cor = cores[i % len(cores)]
        plt.subplot(n, 2, 2 * i + 1)
        sns.histplot(df[col], kde=True, color=cor)
        plt.title(f'Histograma de {col}', fontsize=16)
        plt.subplot(n, 2, 2 * i + 2)
        sns.boxplot(x=df[col], color=cor)
        plt.title(f'Boxplot de {col}', fontsize=16)
    plt.tight_layout()
    plt.show()


def testar_normalidade(df, colunas, alpha=0.05):
    """Teste de normalidade (D'Agostino-Pearson) para cada coluna.

    Retorna um dicionário {coluna: True se distribuição normal}.
    """
    resultados = {}
    for col in colunas:
        _, pval = normaltest(df[col])
        normal = pval > alpha
        resultados[col] = normal
        print(col, ':', 'Distribuição Normal' if normal else 'Distribuição Não Normal')
    return resultados


def plotar_correlacao_spearman(df, drop_cols=('enrollee_id',), figsize=(7, 7)):
    """Heatmap de correlação de Spearman das variáveis numéricas.

    Retorna a matriz de correlação.
    """
    corr = df.drop(columns=list(drop_cols), errors='ignore').corr(
        method='spearman', numeric_only=True)
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=True, cmap='YlGnBu')
    plt.title('Mapa de Correlação das Variáveis Numéricas\n', fontsize=15)
    plt.show()
    return corr


def calcular_woe_iv(df, coluna, target='target'):
    """WOE e IV de uma variável categórica em relação ao target."""
    return (pd.crosstab(df[coluna], df[target], normalize='columns')
            .assign(woe=lambda dfx: np.log(dfx[1] / dfx[0]))
            .assign(iv=lambda dfx: np.sum(dfx['woe'] * (dfx[1] - dfx[0]))))


def calcular_iv_features(df, colunas, target='target'):
    """IV de cada variável categórica, ordenado do menor para o maior."""
    iv = [calcular_woe_iv(df, col, target)['iv'].iloc[0] for col in colunas]
    return (pd.DataFrame({'Features': list(colunas), 'iv': iv})
            .set_index('Features')
            .sort_values(by='iv'))


def plotar_iv(df_iv):
    """Barplot horizontal do Information Value de cada variável."""
    df_iv.plot(kind='barh', title='Information Value das Variáveis Categóricas',
               colormap='Accent', figsize=(10, 8))
    for index, value in enumerate(round(df_iv['iv'], 3)):
        plt.text(value, index, str(value))
    plt.legend(loc='lower right')
    plt.show()


def plotar_valores_ausentes(df, figsize=(15, 5)):
    """Barplot com a contagem de valores ausentes por coluna."""
    null_df = df.isna().sum().reset_index()
    plt.figure(figsize=figsize)
    ax = sns.barplot(x=null_df['index'], y=null_df[0], palette='husl')
    plt.xlabel('Atributos', fontsize=12)
    plt.ylabel('Contagem de Valores Ausentes', fontsize=12)
    plt.xticks(rotation=45)
    plt.title('Plot de Valores Ausentes', fontsize=15)
    _anotar_barras(ax)
    plt.show()


def plotar_mapa_ausentes(df):
    """Matriz missingno apenas das colunas que possuem valores ausentes."""
    import missingno
    contagem = df.isna().sum()
    colunas = contagem[contagem > 0].index
    if len(colunas) > 0:
        missingno.matrix(df[colunas])
        plt.show()
    else:
        print('Nenhum valor ausente no DataFrame.')


def plotar_balanceamento_target(df, target='target'):
    """Pizza + countplot mostrando o balanceamento da variável alvo."""
    plt.figure(figsize=(17, 5))
    plt.subplot(121)
    contagem = df[target].value_counts()
    plt.pie(round(contagem / len(df) * 100, 2), labels=list(contagem.index),
            autopct='%.2f%%', explode=(0, 0.1))
    plt.axis('equal')
    plt.title('Target Imbalance Ratio', size=15)
    plt.subplot(122)
    ax = sns.countplot(data=df, x=target, hue=target, legend=False)
    plt.title('Barplot Target Label', fontsize=15)
    _anotar_barras(ax)
    plt.show()
