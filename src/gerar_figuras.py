"""Gera as figuras estáticas usadas no README.

Grava em img/:

- iv_por_variavel.png ........ Information Value de cada variável categórica,
                               com as faixas de referência de poder preditivo
- taxa_por_matricula.png ..... % procurando trocar de emprego por tipo de
                               matrícula universitária (variável de maior IV)
- correlacao_spearman.png .... correlação de Spearman entre as numéricas
- balanceamento_target.png ... distribuição da variável alvo

Uso: python -m src.gerar_figuras
"""

import os

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

from src import eda, etl
from src.exportar_bi import COLUNAS_CATEGORICAS_IV

# Paleta: uma cor para as barras, tinta neutra para texto, grade discreta
AZUL = '#2a78d6'
AZUL_CLARO = '#9ec5f4'
VERMELHO = '#e34948'
CINZA_NEUTRO = '#f0efec'
FUNDO = '#fcfcfb'
TEXTO = '#0b0b0b'
TEXTO_2 = '#52514e'
MUTED = '#898781'
GRADE = '#e1e0d9'

NOMES = {
    'gender': 'Gênero',
    'relevent_experience': 'Experiência relevante',
    'enrolled_university': 'Matrícula universitária',
    'education_level': 'Nível educacional',
    'major_discipline': 'Área de formação',
    'company_type': 'Tipo de empresa',
    'city_development_index': 'Índice de desenv. da cidade',
    'experience': 'Experiência (anos)',
    'last_new_job': 'Anos desde último emprego',
    'training_hours': 'Horas de treinamento',
    'target': 'Procura novo emprego (alvo)',
}

plt.rcParams.update({
    'figure.facecolor': FUNDO,
    'axes.facecolor': FUNDO,
    'axes.edgecolor': GRADE,
    'axes.labelcolor': TEXTO_2,
    'text.color': TEXTO,
    'xtick.color': MUTED,
    'ytick.color': TEXTO_2,
    'font.size': 11,
    'axes.titlesize': 15,
    'axes.titleweight': 'bold',
    'axes.titlelocation': 'left',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

TAMANHO = (10, 5.625)  # 16:9
DPI = 160


def _br(valor, casas=1):
    """Formata número no padrão brasileiro (vírgula decimal, ponto de milhar)."""
    texto = f'{valor:,.{casas}f}'
    return texto.replace(',', '_').replace('.', ',').replace('_', '.')


def _eixo_br(ax, eixo, casas):
    formato = FuncFormatter(lambda valor, _: _br(valor, casas))
    (ax.xaxis if eixo == 'x' else ax.yaxis).set_major_formatter(formato)


def _salvar(fig, pasta, nome):
    caminho = os.path.join(pasta, nome)
    fig.savefig(caminho, dpi=DPI, facecolor=FUNDO)
    plt.close(fig)
    return caminho


def _subtitulo(ax, texto):
    ax.text(0, 1.02, texto, transform=ax.transAxes, color=MUTED,
            fontsize=10.5, va='bottom')


def _grade(ax, eixo):
    ax.grid(axis=eixo, color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)


def figura_iv(df_bruto, pasta):
    df_iv = eda.calcular_iv_features(df_bruto, COLUNAS_CATEGORICAS_IV)
    rotulos = [NOMES[c] for c in df_iv.index]

    fig, ax = plt.subplots(figsize=TAMANHO, layout='constrained')
    ax.barh(rotulos, df_iv['iv'], color=AZUL, height=0.55)
    for y, valor in enumerate(df_iv['iv']):
        ax.text(valor + 0.0015, y, _br(valor, 3), va='center',
                color=TEXTO_2, fontsize=10.5,
                bbox=dict(facecolor=FUNDO, edgecolor='none', pad=1.5))

    for limite in (0.02, 0.1):
        ax.axvline(limite, color=MUTED, linestyle=(0, (3, 3)), linewidth=1)
    for inicio, fim, nome in [(0.0, 0.02, 'sem poder'), (0.02, 0.1, 'fraco'),
                              (0.1, 0.14, 'médio')]:
        ax.text((inicio + fim) / 2, len(df_iv) - 0.4, nome, ha='center',
                color=MUTED, fontsize=10)

    ax.set_xlim(0, 0.14)
    ax.set_ylim(-0.6, len(df_iv) - 0.2)
    ax.set_xlabel('Information Value (IV)')
    _eixo_br(ax, 'x', 2)
    ax.tick_params(axis='y', length=0)
    _grade(ax, 'x')
    ax.set_title('Nenhuma variável categórica é forte preditora', pad=26)
    _subtitulo(ax, 'IV em relação ao alvo · faixas de referência: '
                   '<0,02 sem poder · 0,02–0,1 fraco · 0,1–0,3 médio')
    return _salvar(fig, pasta, 'iv_por_variavel.png')


def figura_taxa_matricula(df_bruto, pasta):
    rotulos = {
        'Full time course': 'Curso integral',
        'Part time course': 'Curso parcial',
        'no_enrollment': 'Não matriculado',
    }
    grupo = (df_bruto.dropna(subset=['enrolled_university'])
             .groupby('enrolled_university')['target']
             .agg(['mean', 'count'])
             .sort_values('mean'))
    media_geral = df_bruto['target'].mean()

    fig, ax = plt.subplots(figsize=TAMANHO, layout='constrained')
    nomes = [f'{rotulos[i]}\nn = {_br(n, 0)}' for i, n in zip(grupo.index, grupo['count'])]
    ax.barh(nomes, grupo['mean'] * 100, color=AZUL, height=0.5)
    for y, taxa in enumerate(grupo['mean']):
        ax.text(taxa * 100 - 0.8, y, f'{_br(taxa * 100)}%', ha='right',
                va='center', color='white', fontsize=12, fontweight='bold')

    ax.axvline(media_geral * 100, color=MUTED, linestyle=(0, (3, 3)), linewidth=1)
    ax.text(media_geral * 100 + 0.4, len(grupo) - 0.5,
            f'média geral {_br(media_geral * 100)}%', color=MUTED, fontsize=10)

    ax.set_xlim(0, 50)
    ax.set_ylim(-0.6, len(grupo) - 0.3)
    ax.set_xlabel('% procurando trocar de emprego')
    ax.tick_params(axis='y', length=0)
    _grade(ax, 'x')
    ax.set_title('Quem faz curso integral procura mais trocar de emprego', pad=26)
    _subtitulo(ax, 'Matrícula universitária, a variável de maior IV (0,119) · '
                   f'{_br(grupo["count"].sum(), 0)} candidatos com o campo preenchido')
    return _salvar(fig, pasta, 'taxa_por_matricula.png')


def figura_correlacao(df_bruto, pasta):
    df_num = etl.converter_variaveis_numericas(df_bruto)
    ordem = ['city_development_index', 'experience', 'last_new_job',
             'training_hours', 'target']
    corr = df_num[ordem].corr(method='spearman').iloc[1:, :-1]
    mascara = np.triu(np.ones_like(corr, dtype=bool), k=1)

    cmap = LinearSegmentedColormap.from_list('divergente', [VERMELHO, CINZA_NEUTRO, AZUL])
    fig, ax = plt.subplots(figsize=TAMANHO, layout='constrained')
    im = ax.imshow(np.ma.masked_where(mascara, corr.values), cmap=cmap, vmin=-1, vmax=1)
    for i in range(corr.shape[0]):
        for j in range(i + 1):
            valor = corr.values[i, j]
            ax.text(j, i, _br(valor, 2), ha='center', va='center',
                    color='white' if abs(valor) > 0.6 else TEXTO, fontsize=10.5)

    ax.set_xticks(range(corr.shape[1]), [NOMES[c] for c in corr.columns],
                  rotation=25, ha='right')
    ax.set_yticks(range(corr.shape[0]), [NOMES[c] for c in corr.index])
    ax.tick_params(length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    barra = fig.colorbar(im, ax=ax, shrink=0.8, ticks=[-1, 0, 1])
    barra.ax.set_yticklabels(['−1', '0', '1'])
    barra.outline.set_visible(False)
    fig.get_layout_engine().set(rect=(0, 0, 1, 0.88))
    fig.text(0.02, 0.965, 'Correlação de Spearman: associações fracas com o alvo',
             fontsize=15, fontweight='bold', va='top')
    fig.text(0.02, 0.905, 'Mais forte com o alvo: índice de desenvolvimento da cidade '
             f'({_br(corr.loc["target", "city_development_index"], 2)})',
             color=MUTED, fontsize=10.5, va='top')
    return _salvar(fig, pasta, 'correlacao_spearman.png')


def figura_balanceamento(df_bruto, pasta):
    contagem = df_bruto['target'].value_counts().sort_index()
    total = contagem.sum()

    fig, ax = plt.subplots(figsize=TAMANHO, layout='constrained')
    ax.bar(['Não procura', 'Procura trocar'], contagem.values,
           color=[AZUL_CLARO, AZUL], width=0.5)
    for x, n in enumerate(contagem.values):
        ax.text(x, n + total * 0.01, f'{_br(n / total * 100)}%\n{_br(n, 0)}',
                ha='center', va='bottom', color=TEXTO_2, fontsize=11)
    ax.set_ylim(0, contagem.max() * 1.22)
    ax.set_ylabel('Candidatos')
    _eixo_br(ax, 'y', 0)
    ax.tick_params(axis='x', length=0, labelsize=12)
    _grade(ax, 'y')
    ax.set_title('Alvo desbalanceado: 1 em cada 4 procura trocar de emprego', pad=26)
    _subtitulo(ax, f'aug_train.csv · {_br(total, 0)} candidatos')
    return _salvar(fig, pasta, 'balanceamento_target.png')


def gerar_figuras(caminho_entrada='dataset/raw/aug_train.csv', pasta_saida='img'):
    """Gera todas as figuras e retorna os caminhos gravados."""
    os.makedirs(pasta_saida, exist_ok=True)
    df_bruto = etl.carregar_dados(caminho_entrada)
    return [
        figura_iv(df_bruto, pasta_saida),
        figura_taxa_matricula(df_bruto, pasta_saida),
        figura_correlacao(df_bruto, pasta_saida),
        figura_balanceamento(df_bruto, pasta_saida),
    ]


if __name__ == '__main__':
    for arquivo in gerar_figuras():
        print('Gerado:', arquivo)
