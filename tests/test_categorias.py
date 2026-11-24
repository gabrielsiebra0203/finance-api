
def test_criar_transacao_com_categoria(client):
    dados = {
        "descricao": "Supermercado",
        "valor": "250.00",
        "tipo": "despesa",
        "categoria": "Alimentação"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 201

    transacao = resposta.json()

    assert transacao["descricao"] == "Supermercado"
    assert transacao["categoria"] == "Alimentação"


def test_buscar_transacao_com_categoria(client):
    dados = {
        "descricao": "Salário",
        "valor": "3000.00",
        "tipo": "receita",
        "categoria": "Trabalho"
    }

    resposta_criacao = client.post(
        "/transacoes",
        json=dados
    )

    assert resposta_criacao.status_code == 201

    transacao_id = resposta_criacao.json()["id"]

    resposta_busca = client.get(
        f"/transacoes/{transacao_id}"
    )

    assert resposta_busca.status_code == 200
    assert resposta_busca.json()["categoria"] == "Trabalho"


def test_atualizar_categoria_transacao(client):
    dados = {
        "descricao": "Uber",
        "valor": "35.00",
        "tipo": "despesa",
        "categoria": "Transporte"
    }

    resposta_criacao = client.post(
        "/transacoes",
        json=dados
    )

    assert resposta_criacao.status_code == 201

    transacao_id = resposta_criacao.json()["id"]

    novos_dados = {
        "descricao": "Uber",
        "valor": "35.00",
        "tipo": "despesa",
        "categoria": "Mobilidade"
    }

    resposta_atualizacao = client.put(
        f"/transacoes/{transacao_id}",
        json=novos_dados
    )

    assert resposta_atualizacao.status_code == 200
    assert resposta_atualizacao.json()["categoria"] == "Mobilidade"

    resposta_busca = client.get(
        f"/transacoes/{transacao_id}"
    )

    assert resposta_busca.status_code == 200
    assert resposta_busca.json()["categoria"] == "Mobilidade"


def test_rejeitar_categoria_vazia(client):
    dados = {
        "descricao": "Supermercado",
        "valor": "150.00",
        "tipo": "despesa",
        "categoria": ""
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422


def test_rejeitar_categoria_muito_longa(client):
    dados = {
        "descricao": "Supermercado",
        "valor": "150.00",
        "tipo": "despesa",
        "categoria": "A" * 51
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422


def test_criar_transacao_sem_categoria(client):
    dados = {
        "descricao": "Pagamento",
        "valor": "500.00",
        "tipo": "receita"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 201
    assert resposta.json()["categoria"] is None


def test_rejeitar_categoria_tipo_invalido(client):
    dados = {
        "descricao": "Supermercado",
        "valor": "150.00",
        "tipo": "despesa",
        "categoria": 123
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 422
