# Dashboard BI — HR Analytics

## Modificações no projeto

### Bug corrigido
Na etapa de tratamento de `major_discipline`, a linha:

```python
new_df[new_df['major_discipline'].isna()] = 'Other'
```

sobrescrevia **todas as colunas** das linhas com `major_discipline` ausente, em vez de só a coluna `major_discipline`. Isso corrompia `target` e `city_development_index` em 28 registros (viravam a string `'Other'`), forçando essas colunas inteiras a ficarem como tipo texto no CSV exportado.

Corrigido para:

```python
new_df.loc[new_df['major_discipline'].isna(), 'major_discipline'] = 'Other'
```

Notebook reexecutado do zero (`jupyter nbconvert --execute`) para regenerar outputs, CSV e PNG com os dados corretos.

### Limpeza de repositório
- Removidos 3 arquivos de checkpoint do Jupyter que estavam versionados por engano (`Projeto2-checkpoint.ipynb`, `ProjetoRH-checkpoint.ipynb`, `Untitled-checkpoint.ipynb`).
- Criado `.gitignore` com `.ipynb_checkpoints/`.
- Removida célula de código duplicada no notebook (reexportava o mesmo CSV com prints extras).

### Arquivos gerados
- `dataset/processed/hr_analytics_tratado.csv` — dataset limpo, 19.093 linhas, 8 colunas, pronto para BI.
- `dashboard_hr_analytics.png` — painel exploratório gerado no notebook (matplotlib), referência visual.

Commit: `a114633` — `fix: corrige bug de imputação e finaliza pipeline de tratamento`.

---

## Estrutura do dataset (`dataset/processed/hr_analytics_tratado.csv`)

| Coluna | Tipo | Observação |
|---|---|---|
| `city_development_index` | float | 0.448 a 0.949 |
| `experience` | texto | `<1`, `1`...`20`, `>20` — precisa tratamento se for usar como número |
| `enrolled_university` | texto | categórica |
| `relevent_experience` | texto | categórica (2 valores) |
| `education_level` | texto | categórica |
| `company_type` | texto | categórica |
| `major_discipline` | texto | categórica |
| `target` | float | 0.0 = não declarou intenção, 1.0 = declarou intenção de mudar de emprego |

---

## Montagem no Power BI (`rh.pbix`)

**Fonte:** `dataset/processed/hr_analytics_tratado.csv`. Ao clonar o repositório, ajuste o caminho em
*Transformar dados → Configurações da fonte de dados* e clique em *Atualizar*.

**Linguagem:** `target = 1` é intenção **declarada** de mudar de emprego, não saída efetiva. Por isso as
medidas usam "Job Change Intent", e não "Exit" ou "Turnover".

### Colunas renomeadas no modelo (o CSV mantém os nomes originais)

| CSV | Modelo |
|---|---|
| `education_level` | Education Level |
| `company_type` | Company Type |
| `enrolled_university` | University Enrollment |
| `relevent_experience` | Relevant Experience |
| `major_discipline` | Major Discipline |

### Medidas (DAX)

```dax
Total Candidates = COUNTROWS(hr_analytics_tratado)
```

```dax
Job Change Intent Rate = AVERAGE(hr_analytics_tratado[target])
```
> Formatar como porcentagem no próprio formato da medida (não multiplicar por 100).

```dax
Candidates Seeking Change = CALCULATE(COUNTROWS(hr_analytics_tratado), hr_analytics_tratado[target] = 1)
```

```dax
% Relevant Experience =
DIVIDE(
    CALCULATE(COUNTROWS(hr_analytics_tratado), hr_analytics_tratado[Relevant Experience] = "Has relevent experience"),
    COUNTROWS(hr_analytics_tratado)
)
```

```dax
Avg City Dev Index = AVERAGE(hr_analytics_tratado[city_development_index])
```

```dax
Avg Experience (years) =
AVERAGEX(
    hr_analytics_tratado,
    SWITCH(
        TRUE(),
        hr_analytics_tratado[experience] = "<1", 0,
        hr_analytics_tratado[experience] = ">20", 21,
        VALUE(hr_analytics_tratado[experience])
    )
)
```

### Medidas de rótulo (pasta "Labels (en-US)")

O Power BI Desktop formata números conforme a configuração regional do Windows (pt-BR mostra 19.093 e 24,9%).
Como o relatório é em inglês, cartões, matriz e tabela usam medidas de texto com formato fixo en-US:

```DAX
Total Candidates Label = VAR v = [Total Candidates] RETURN IF(ISBLANK(v), BLANK(), FORMAT(v, "#,0", "en-US"))
Intent Rate Label = VAR v = [Job Change Intent Rate] RETURN IF(ISBLANK(v), BLANK(), FORMAT(v, "0.0%", "en-US"))
```

Mesmo padrão para Seeking Change, Relevant Experience, Avg City Dev Index e Avg Experience.
O `IF(ISBLANK(...))` evita linhas vazias na tabela. A cor da matriz continua calculada pela medida numérica
(Job Change Intent Rate). O modelo também foi recriado com idioma en-US.

### Colunas calculadas

```dax
City Development Band =
SWITCH(
    TRUE(),
    hr_analytics_tratado[city_development_index] < 0.6, "Low (<0.60)",
    hr_analytics_tratado[city_development_index] < 0.85, "Medium (0.60-0.85)",
    "High (>=0.85)"
)
```

```dax
Experience Range =
SWITCH(
    TRUE(),
    hr_analytics_tratado[experience] = "<1", "<1 year",
    hr_analytics_tratado[experience] = ">20", ">20 years",
    VALUE(hr_analytics_tratado[experience]) <= 5, "1-5 years",
    VALUE(hr_analytics_tratado[experience]) <= 10, "6-10 years",
    "11-20 years"
)
```
> Ordenada por `Faixa Experiencia Ordem` (coluna oculta, 0 a 4).

### Páginas

**Layout comum**
- Fundo em imagem (`hr_bg_overview.png` / `hr_bg_detail.png`, recursos registrados no .pbix): cabeçalho escuro com título,
  subtítulo da base (19.093 candidatos, target = intenção declarada, Kaggle) e molduras brancas atrás de cada visual
- Botões transparentes sobre as pílulas Overview / Detail fazem a navegação entre páginas (Ctrl+clique no Desktop)

**Overview**
- Cards: Total Candidates, Intent Rate, Seeking Change, Relevant Experience
- Painel Filters: Education Level, Company Type
- Barras: Intent Rate por Company Type (subtítulo: "Other" é quase todo "não informado", 6.104 de 6.225),
  Relevant Experience, Education Level e Experience Range; colunas por City Development Band
- Linha tracejada em cada gráfico: taxa geral (24,9%)
- Painel Key findings (texto fixo, base completa; não muda com os filtros)

**Detail**
- Cards: Total Candidates, Intent Rate, Seeking Change, Avg City Development Index, Avg Experience (yrs)
- Matriz Education Level × Company Type colorida pela Job Change Intent Rate
- Tabela Experience Range × University Enrollment × Relevant Experience com Candidates e Intent Rate
- Painel "How to read this page" (como ler matriz e tabela, cuidado com grupos pequenos)
