


def test_valor_negativo(client):
    dados = {
        "descricao": "Compra inválida",
        "valor": "-100.00",
        "tipo": "despesa"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422


def test_valor_zero(client):
    dados = {
        "descricao": "Compra inválida",
        "valor": "0.00",
        "tipo": "despesa"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422


def test_valor_com_tres_casas_decimais(client):
    dados = {
        "descricao": "Compra inválida",
        "valor": "99.999",
        "tipo": "despesa"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422


def test_descricao_vazia(client):
    dados = {
        "descricao": "",
        "valor": "100.00",
        "tipo": "despesa"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422


def test_tipo_invalido(client):
    dados = {
        "descricao": "Transferência",
        "valor": "100.00",
        "tipo": "transferencia"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422
