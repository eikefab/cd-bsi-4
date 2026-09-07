class Product:
    def __init__(self, json_object):
        self.codigo = json_object.get("codigo")
        self.descricao = json_object.get("descricao")
        self.descricao_sefaz = json_object.get("descricaoSefaz")
        self.gtin = json_object.get("gtin")
        self.ncm = json_object.get("ncm")
        self.gpc = json_object.get("gpc")
        self.unidade_medida = json_object.get("unidadeMedida")

        venda = json_object.get("venda")

        self.data_venda = venda.get("dataVenda")
        self.valor_declarado = venda.get("valorDeclarado")
        self.valor_venda = venda.get("valorVenda")

    @staticmethod
    def headers():
        return (
            "codigo",
            "descricao",
            "descricao_sefaz",
            "gtin",
            "ncm",
            "gpc",
            "unidade_medida",
            "data_venda",
            "valor_declarado",
            "valor_venda"
        )

class SefazResponse:
    def __init__(self, http_response):
        self.status_code = http_response.status_code
        self.json_data = http_response.json()

        self.total_registros = self.json_data.get("totalRegistros")
        self.total_paginas = self.json_data.get("totalPaginas")
        self.pagina_atual = self.json_data.get("pagina")
        self.registros_por_pagina = self.json_data.get("registrosPorPagina")
        self.registros_pagina = self.json_data.get("registrosPagina")
        self.primeira_pagina = self.json_data.get("primeiraPagina")
        self.ultima_pagina = self.json_data.get("ultimaPagina")
        self.produtos = list(self._parse_products(self.json_data))

    def _parse_products(self, json_object):
        conteudo = json_object.get("conteudo", [])

        for item in conteudo:
            produto = item.get("produto")

            if not produto:
                continue

            yield Product(produto)

    def to_csv(self, file):
        import csv
        from pathlib import Path

        Path(file).parent.mkdir(parents=True, exist_ok=True)

        with open(file, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=Product.headers())
            writer.writeheader()

            for produto in self.produtos:
                writer.writerow(produto.__dict__)

        return file
