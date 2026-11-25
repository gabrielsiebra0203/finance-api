
def criar_transacao(client, descricao, data, tipo="despesa"):
    resposta = client.post(
        "/transacoes",
        json={
            "descricao": descricao,
            "valor": "100.00",
            "tipo": tipo,
            "categoria": "Testes",
            "data_transacao": data
        }
    )

    assert resposta.status_code == 201
    return resposta.json()


def preparar_transacoes(client):
    criar_transacao(
        client, "Compra setembro", "2026-09-10"
    )
    criar_transacao(
        client, "Compra outubro", "2026-10-15"
    )
    criar_transacao(
        client, "Compra novembro", "2026-11-20"
    )


def test_filtrar_por_data_inicio(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes?data_inicio=2026-10-01"
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 2

    datas = [
        item["data_transacao"]
        for item in dados["transacoes"]
    ]

    assert "2026-09-10" not in datas
    assert "2026-10-15" in datas
    assert "2026-11-20" in datas


def test_filtrar_por_data_fim(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes?data_fim=2026-10-31"
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 2

    datas = [
        item["data_transacao"]
        for item in dados["transacoes"]
    ]

    assert "2026-09-10" in datas
    assert "2026-10-15" in datas
    assert "2026-11-20" not in datas


def test_filtrar_por_intervalo(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes",
        params={
            "data_inicio": "2026-10-01",
            "data_fim": "2026-10-31"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 1
    assert dados["transacoes"][0]["descricao"] == "Compra outubro"


def test_intervalo_invalido_retorna_422(client):
    resposta = client.get(
        "/transacoes",
        params={
            "data_inicio": "2026-12-01",
            "data_fim": "2026-11-01"
        }
    )

    assert resposta.status_code == 422
    assert resposta.json()["detail"] == (
        "A data inicial não pode ser maior que a data final"
    )


def test_formato_data_invalido_retorna_422(client):
    resposta = client.get(
        "/transacoes",
        params={
            "data_inicio": "data-invalida"
        }
    )

    assert resposta.status_code == 422


def test_combinar_data_e_tipo(client):
    criar_transacao(
        client, "Salário outubro", "2026-10-10", "receita"
    )
    criar_transacao(
        client, "Aluguel outubro", "2026-10-15", "despesa"
    )
    criar_transacao(
        client, "Salário novembro", "2026-11-10", "receita"
    )

    resposta = client.get(
        "/transacoes",
        params={
            "tipo": "receita",
            "data_inicio": "2026-10-01",
            "data_fim": "2026-10-31"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 1
    assert dados["transacoes"][0]["descricao"] == "Salário outubro"


def test_filtrar_datas_com_paginacao(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes",
        params={
            "data_inicio": "2026-09-01",
            "data_fim": "2026-11-30",
            "limit": 2,
            "offset": 0
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 3
    assert len(dados["transacoes"]) == 2
    assert dados["tem_proxima"] is True
