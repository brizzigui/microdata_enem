# Trabalho 2 de Mineração de Dados

## Informações Relevantes

As pastas `microdados_enem_[ano]` contém os microdados divulgados pelo INEP para aquele ano. A estrutura é similar, porém há algumas diferenças para as quais deve se atentar.

Juntos, todos os dados pesam em torno de 10GB. Então, baixem em uma pasta em que eles caibam: .

Creio que a principal diferença foi uma reestruturação feita em 2024 que separou os dados do questionário socioeconômico do desempenho dos candidatos. Nos demais, isso está intacto. Dessa forma, para análises socioeconômicas, recomendo trabalharmos com o intervalo [2020, 2023].

## O que minerar?

- Quem vai bem na área X, vai bem na área Y? (regressão entre desempenho de cada área)
- Impacto de cada fator socioeconomico no desempenho (regressão?)
- Clustering de questões (agrupamento) e comparação do modelo com análise textual feita por LLMs, para verificação de quanto podemos aferir sobre o conteúdo das questões só com clustering.
- Modelo de redes neurais para previsão da nota final só com o questionário socioeconômico
- Adicionem as suas...