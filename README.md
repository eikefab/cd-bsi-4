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
    * Arquivo contém os dados tratados
* charts/
    * Pasta contendo os gráficos plotados:
        * Boxplot dos 10 itens que mais aparecem
        * Histograma dos preços das tintas
        * Evolução de preços
        * Dispersão dos valores
