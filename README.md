# Sobre

Projeto criado para atividade de Ciência de Dados, disciplina ministrada pelo professor Dr. Edison Camilo, no curso Bacharelado em Sistemas de Informação, no Instituto Federal de Alagoas.

Dupla:

* Eike Fabrício
* Luiz Vinícius

## Requisitos:

* Chave de API da Sefaz-AL
* UV (https://docs.astral.sh/uv/getting-started/installation/)

### Como executar: 

Criar arquivo `.env`, sendo cópia de `.env.example`, preenchendo o campo `SEFAZ_TOKEN`.

Instalar as bibliotecas e executar os comandos:

```bash
uv sync
uv run main.py
```

O pipeline cria a pasta `output` automaticamente na raiz do projeto. Por lá, teremos os arquivos:

* bronze.csv`
    * Arquivo contém os dados brutos obtidos pela API.
* silver.csv
    * Arquivo contém as tintas classificadas nos grupos `tinta_branca`, `tinta_acrilica_branca`, `tinta_acrilica`, `tinta_spray` e `tinta_metalica`, independentemente da unidade de medida.
    * Um registro pode aparecer mais de uma vez quando corresponde a mais de um grupo. O grupo de cada linha é informado na coluna `grupo`.
* charts/
    * Pasta contendo os gráficos plotados:
        * Um boxplot comparando tintas brancas e acrílicas
        * Um boxplot comparando tintas spray e metálicas em uma escala própria
        * Um histograma com curva KDE dos preços de venda para cada grupo
