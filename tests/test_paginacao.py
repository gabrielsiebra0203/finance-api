
def test_paginacao_com_limit_e_offset(client):
    for numero in range(1, 6):
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": f"Transação {numero}",
                "valor": "100.00",
                "tipo": "despesa",
                "categoria": "Teste"
            }
        )
        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "limit": 2,
            "offset": 2
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 5
    assert len(dados["transacoes"]) == 2

    assert dados["transacoes"][0]["descricao"] == "Transação 3"
    assert dados["transacoes"][1]["descricao"] == "Transação 4"


def test_paginacao_com_filtros_combinados(client):
    transacoes = [
        ("Salário", "3000.00", "receita", "Trabalho"),
        ("Mercado", "150.00", "despesa", "Alimentação"),
        ("Restaurante", "80.00", "despesa", "Alimentação"),
        ("Transporte", "50.00", "despesa", "Transporte"),
        ("Padaria", "30.00", "despesa", "Alimentação"),
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
            "valor_min": "20",
            "valor_max": "200",
            "limit": 2,
            "offset": 1
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 3
    assert dados["limit"] == 2
    assert dados["offset"] == 1
    assert dados["tem_proxima"] is False

    assert len(dados["transacoes"]) == 2
    assert dados["transacoes"][0]["descricao"] == "Restaurante"
    assert dados["transacoes"][1]["descricao"] == "Padaria"


def test_parametros_invalidos_de_paginacao(client):
    parametros_invalidos = [
        {"limit": 0},
        {"limit": 101},
        {"limit": -5},
        {"offset": -1},
        {"offset": "abc"},
        {"limit": "texto"},
    ]

    for parametros in parametros_invalidos:
        resposta = client.get(
            "/transacoes",
            params=parametros
        )

        assert resposta.status_code == 422


def test_offset_maior_que_total(client):
    resposta_criacao = client.post(
        "/transacoes",
        json={
            "descricao": "Compra de teste",
            "valor": "75.00",
            "tipo": "despesa",
            "categoria": "Compras"
        }
    )

    assert resposta_criacao.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "limit": 5,
            "offset": 100
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 1
    assert dados["limit"] == 5
    assert dados["offset"] == 100
    assert dados["tem_proxima"] is False
    assert dados["transacoes"] == []


def test_metadados_de_paginacao(client):
    for numero in range(1, 4):
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": f"Compra {numero}",
                "valor": "100.00",
                "tipo": "despesa",
                "categoria": "Compras"
            }
        )
        assert resposta.status_code == 201

    primeira_pagina = client.get(
        "/transacoes",
        params={"limit": 2, "offset": 0}
    )

    assert primeira_pagina.status_code == 200

    dados = primeira_pagina.json()

    assert dados["total"] == 3
    assert dados["limit"] == 2
    assert dados["offset"] == 0
    assert dados["tem_proxima"] is True
    assert len(dados["transacoes"]) == 2

    segunda_pagina = client.get(
        "/transacoes",
        params={"limit": 2, "offset": 2}
    )

    assert segunda_pagina.status_code == 200

    dados = segunda_pagina.json()

    assert dados["total"] == 3
    assert dados["limit"] == 2
    assert dados["offset"] == 2
    assert dados["tem_proxima"] is False
    assert len(dados["transacoes"]) == 1
