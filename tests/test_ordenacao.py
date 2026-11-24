
def test_ordenacao_por_valor_crescente(client):
    transacoes = [
        ("Compra cara", "500.00"),
        ("Compra barata", "50.00"),
        ("Compra intermediaria", "200.00"),
    ]

    for descricao, valor in transacoes:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": descricao,
                "valor": valor,
                "tipo": "despesa",
                "categoria": "Compras"
            }
        )

        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={"ordenar_por": "valor"}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    descricoes = [
        transacao["descricao"]
        for transacao in dados["transacoes"]
    ]

    assert descricoes == [
        "Compra barata",
        "Compra intermediaria",
        "Compra cara"
    ]

def test_ordenacao_por_valor_decrescente(client):
    transacoes = [
        ("Compra barata", "50.00"),
        ("Compra cara", "500.00"),
        ("Compra intermediaria", "200.00"),
    ]

    for descricao, valor in transacoes:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": descricao,
                "valor": valor,
                "tipo": "despesa",
                "categoria": "Compras"
            }
        )

        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "ordenar_por": "valor",
            "ordem": "desc"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    descricoes = [
        transacao["descricao"]
        for transacao in dados["transacoes"]
    ]

    assert descricoes == [
        "Compra cara",
        "Compra intermediaria",
        "Compra barata"
    ]

def test_parametros_invalidos_de_ordenacao(client):
    resposta = client.get(
        "/transacoes",
        params={"ordenar_por": "invalido"}
    )

    assert resposta.status_code == 422

    resposta = client.get(
        "/transacoes",
        params={"ordem": "aleatorio"}
    )

    assert resposta.status_code == 422


def test_ordenacao_padrao_por_id(client):
    descricoes = [
        "Terceira compra",
        "Primeira compra",
        "Segunda compra"
    ]

    ids_criados = []

    for descricao in descricoes:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": descricao,
                "valor": "100.00",
                "tipo": "despesa",
                "categoria": "Compras"
            }
        )

        assert resposta.status_code == 201
        ids_criados.append(resposta.json()["id"])

    resposta = client.get("/transacoes")

    assert resposta.status_code == 200

    ids_retornados = [
        transacao["id"]
        for transacao in resposta.json()["transacoes"]
    ]

    assert ids_retornados == ids_criados


def test_ordenacao_por_descricao(client):
    descricoes = [
        "Transporte",
        "Aluguel",
        "Internet"
    ]

    for descricao in descricoes:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": descricao,
                "valor": "100.00",
                "tipo": "despesa",
                "categoria": "Contas"
            }
        )

        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "ordenar_por": "descricao",
            "ordem": "asc"
        }
    )

    assert resposta.status_code == 200

    descricoes_retornadas = [
        transacao["descricao"]
        for transacao in resposta.json()["transacoes"]
    ]

    assert descricoes_retornadas == [
        "Aluguel",
        "Internet",
        "Transporte"
    ]
