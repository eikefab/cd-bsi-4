from .models import SefazResponse, Product

import requests
import os


API_URL="http://api.sefaz.al.gov.br/sfz-economiza-alagoas-api/api/public/produto/pesquisa"

FILTER_REF_CODE="83000000" # Materiais de Construção
MCZ_REF_CODE=2704302 # Maceió

SEARCH_PARAM="tinta"


def search(page=1, page_size=50, days=7):
    if days > 10 or days < 1:
        raise ValueError("Dias devem estar no intervalo de 1 a 10.")

    payload = {
        "produto": {
            "descricao": SEARCH_PARAM,
            "gpc": FILTER_REF_CODE,
        },
        "estabelecimento": {
            "municipio": {
                "codigoIBGE": MCZ_REF_CODE
            }
        },
        "dias": days,
        "pagina": page,
        "registrosPorPagina": page_size
    }

    headers = {
        "Content-Type": "application/json",
        "AppToken": os.getenv("SEFAZ_TOKEN")
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

    return response

def get_items():
    return SefazResponse(search())

def get_all_items(limit=None):
    response = SefazResponse(search())
    items = []  

    while not response.ultima_pagina:
        print(f"Página {response.pagina_atual} de {response.total_registros // response.registros_por_pagina + 1} (qtd.: {response.total_registros}) [{len(items)}]")

        items.extend(response.produtos)

        if limit is not None and response.pagina_atual == limit:
            break

        query = search(page=response.pagina_atual + 1)
        response = SefazResponse(query)

    print("Processamento finalizado.")

    response.produtos = items

    return response
    