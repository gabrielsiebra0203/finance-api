
def test_filtros_ordenacao_e_paginacao(client):
    transacoes = [
        ("Supermercado", "450.00", "despesa", "Alimentação"),
        ("Restaurante", "280.00", "despesa", "Alimentação"),
        ("Delivery", "120.00", "despesa", "Alimentação"),
        ("Cafe", "30.00", "despesa", "Alimentação"),
        ("Transporte", "600.00", "despesa", "Transporte"),
        ("Salario", "3000.00", "receita", "Trabalho"),
    ]

    for descricao, valor, tipo, categoria in transacoes:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": descricao,
                "valor": valor,
                "tipo": tipo,
                "categoria": categoria
            }
        )

        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "tipo": "despesa",
            "categoria": "Alimentação",
            "valor_min": "100",
            "ordenar_por": "valor",
            "ordem": "desc",
            "limit": 2,
            "offset": 0
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 3
    assert dados["limit"] == 2
    assert dados["offset"] == 0
    assert dados["tem_proxima"] is True

    descricoes = [
        item["descricao"]
        for item in dados["transacoes"]
    ]

    assert descricoes == [
        "Supermercado",
        "Restaurante"
    ]


def test_segunda_pagina_com_ordenacao(client):
    valores = ["100.00", "400.00", "200.00", "300.00"]

    for valor in valores:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": f"Despesa {valor}",
                "valor": valor,
                "tipo": "despesa",
                "categoria": "Teste"
            }
        )

        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "tipo": "despesa",
            "categoria": "Teste",
            "ordenar_por": "valor",
            "ordem": "desc",
            "limit": 2,
            "offset": 2
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 4
    assert dados["limit"] == 2
    assert dados["offset"] == 2
    assert dados["tem_proxima"] is False

    valores_retornados = [
        float(item["valor"])
        for item in dados["transacoes"]
    ]

    assert valores_retornados == [200.0, 100.0]
