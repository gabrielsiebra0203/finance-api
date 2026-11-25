
from datetime import date


def dados_transacao(**alteracoes):
    dados = {
        "descricao": "Compra de teste",
        "valor": "150.50",
        "tipo": "despesa",
        "categoria": "Testes",
    }

    dados.update(alteracoes)
    return dados


def test_criar_transacao_com_data(client):
    resposta = client.post(
        "/transacoes",
        json=dados_transacao(
            data_transacao="2026-11-10"
        )
    )

    assert resposta.status_code == 201
    assert resposta.json()["data_transacao"] == "2026-11-10"


def test_criar_transacao_sem_data(client):
    antes = date.today()

    resposta = client.post(
        "/transacoes",
        json=dados_transacao()
    )

    depois = date.today()

    assert resposta.status_code == 201

    data_retornada = date.fromisoformat(
        resposta.json()["data_transacao"]
    )

    assert antes <= data_retornada <= depois


def test_buscar_transacao_retorna_data(client):
    criacao = client.post(
        "/transacoes",
        json=dados_transacao(
            data_transacao="2026-10-15"
        )
    )

    assert criacao.status_code == 201

    transacao_id = criacao.json()["id"]

    resposta = client.get(
        f"/transacoes/{transacao_id}"
    )

    assert resposta.status_code == 200
    assert resposta.json()["data_transacao"] == "2026-10-15"


def test_atualizar_data_transacao(client):
    criacao = client.post(
        "/transacoes",
        json=dados_transacao(
            data_transacao="2026-10-01"
        )
    )

    assert criacao.status_code == 201

    transacao_id = criacao.json()["id"]

    resposta = client.put(
        f"/transacoes/{transacao_id}",
        json=dados_transacao(
            descricao="Compra atualizada",
            data_transacao="2026-11-20"
        )
    )

    assert resposta.status_code == 200
    assert resposta.json()["data_transacao"] == "2026-11-20"


def test_atualizar_sem_data_preserva_original(client):
    criacao = client.post(
        "/transacoes",
        json=dados_transacao(
            data_transacao="2026-09-05"
        )
    )

    assert criacao.status_code == 201

    transacao_id = criacao.json()["id"]

    resposta = client.put(
        f"/transacoes/{transacao_id}",
        json=dados_transacao(
            descricao="Descrição modificada"
        )
    )

    assert resposta.status_code == 200
    assert resposta.json()["data_transacao"] == "2026-09-05"


def test_data_invalida_retorna_422(client):
    resposta = client.post(
        "/transacoes",
        json=dados_transacao(
            data_transacao="data-invalida"
        )
    )

    assert resposta.status_code == 422
