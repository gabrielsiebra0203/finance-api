
def test_filtrar_transacoes_por_tipo(client):
    receita = {
        "descricao": "Salário",
        "valor": "3000.00",
        "tipo": "receita",
        "categoria": "Trabalho"
    }

    despesa = {
        "descricao": "Supermercado",
        "valor": "250.00",
        "tipo": "despesa",
        "categoria": "Alimentação"
    }

    resposta_receita = client.post("/transacoes", json=receita)
    resposta_despesa = client.post("/transacoes", json=despesa)

    assert resposta_receita.status_code == 201
    assert resposta_despesa.status_code == 201

    resposta = client.get("/transacoes?tipo=despesa")

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 1
    assert len(dados["transacoes"]) == 1
    assert dados["transacoes"][0]["tipo"] == "despesa"
    assert dados["transacoes"][0]["descricao"] == "Supermercado"


def test_filtrar_transacoes_por_categoria(client):
    transacoes = [
        {
            "descricao": "Supermercado",
            "valor": "250.00",
            "tipo": "despesa",
            "categoria": "Alimentação"
        },
        {
            "descricao": "Internet",
            "valor": "100.00",
            "tipo": "despesa",
            "categoria": "Moradia"
        },
        {
            "descricao": "Restaurante",
            "valor": "80.00",
            "tipo": "despesa",
            "categoria": "Alimentação"
        }
    ]

    for transacao in transacoes:
        resposta = client.post("/transacoes", json=transacao)
        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={"categoria": "Alimentação"}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 2
    assert all(
        transacao["categoria"] == "Alimentação"
        for transacao in dados["transacoes"]
    )


def test_combinar_filtros_tipo_e_categoria(client):
    transacoes = [
        {
            "descricao": "Salário",
            "valor": "3000.00",
            "tipo": "receita",
            "categoria": "Trabalho"
        },
        {
            "descricao": "Supermercado",
            "valor": "250.00",
            "tipo": "despesa",
            "categoria": "Alimentação"
        },
        {
            "descricao": "Reembolso alimentação",
            "valor": "50.00",
            "tipo": "receita",
            "categoria": "Alimentação"
        }
    ]

    for transacao in transacoes:
        resposta = client.post("/transacoes", json=transacao)
        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "tipo": "despesa",
            "categoria": "Alimentação"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 1
    assert dados["transacoes"][0]["descricao"] == "Supermercado"
    assert dados["transacoes"][0]["tipo"] == "despesa"
    assert dados["transacoes"][0]["categoria"] == "Alimentação"


def test_filtrar_transacoes_por_valor_minimo(client):
    valores = ["50.00", "150.00", "500.00"]

    for valor in valores:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": f"Transação de {valor}",
                "valor": valor,
                "tipo": "despesa",
                "categoria": "Teste"
            }
        )
        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={"valor_min": "150.00"}
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 2
    assert [item["valor"] for item in dados["transacoes"]] == [
        "150.00",
        "500.00"
    ]


def test_filtrar_transacoes_por_intervalo_valores(client):
    valores = ["50.00", "100.00", "250.00", "500.00"]

    for valor in valores:
        resposta = client.post(
            "/transacoes",
            json={
                "descricao": f"Transação de {valor}",
                "valor": valor,
                "tipo": "despesa",
                "categoria": "Teste"
            }
        )
        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "valor_min": "100.00",
            "valor_max": "250.00"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 2
    assert [item["valor"] for item in dados["transacoes"]] == [
        "100.00",
        "250.00"
    ]


def test_combinar_todos_os_filtros(client):
    transacoes = [
        {
            "descricao": "Supermercado",
            "valor": "250.00",
            "tipo": "despesa",
            "categoria": "Alimentação"
        },
        {
            "descricao": "Restaurante",
            "valor": "80.00",
            "tipo": "despesa",
            "categoria": "Alimentação"
        },
        {
            "descricao": "Compra mensal",
            "valor": "600.00",
            "tipo": "despesa",
            "categoria": "Alimentação"
        },
        {
            "descricao": "Internet",
            "valor": "150.00",
            "tipo": "despesa",
            "categoria": "Moradia"
        },
        {
            "descricao": "Reembolso",
            "valor": "200.00",
            "tipo": "receita",
            "categoria": "Alimentação"
        }
    ]

    for transacao in transacoes:
        resposta = client.post("/transacoes", json=transacao)
        assert resposta.status_code == 201

    resposta = client.get(
        "/transacoes",
        params={
            "tipo": "despesa",
            "categoria": "Alimentação",
            "valor_min": "100.00",
            "valor_max": "500.00"
        }
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 1
    assert dados["transacoes"][0]["descricao"] == "Supermercado"
    assert dados["transacoes"][0]["valor"] == "250.00"


def test_rejeitar_intervalo_de_valores_invalido(client):
    resposta = client.get(
        "/transacoes",
        params={
            "valor_min": "500.00",
            "valor_max": "100.00"
        }
    )

    assert resposta.status_code == 422

    assert resposta.json()["detail"] == (
        "O valor mínimo não pode ser maior que o valor máximo"
    )


def test_rejeitar_tipo_invalido(client):
    resposta = client.get(
        "/transacoes",
        params={"tipo": "investimento"}
    )

    assert resposta.status_code == 422


def test_rejeitar_valor_minimo_negativo(client):
    resposta = client.get(
        "/transacoes",
        params={"valor_min": "-100.00"}
    )

    assert resposta.status_code == 422


def test_rejeitar_categoria_vazia(client):
    resposta = client.get(
        "/transacoes",
        params={"categoria": ""}
    )

    assert resposta.status_code == 422


def test_filtro_sem_resultados(client):
    resposta = client.get(
        "/transacoes",
        params={"categoria": "CategoriaInexistenteXYZ"}
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
    "total": 0,
    "limit": None,
    "offset": 0,
    "tem_proxima": False,
    "transacoes": []
}
