
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_pagina_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "online"


def test_healthcheck():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_rota_inexistente():
    resposta = client.get("/rota-inexistente")

    assert resposta.status_code == 404
def test_sobre():
    resposta = client.get("/sobre")

    assert resposta.status_code == 200
    assert resposta.json()["projeto"] == "Finance API"

def test_listar_transacoes():
    resposta = client.get("/transacoes")

    assert resposta.status_code == 200
    assert resposta.json()["total"] == 2
    assert len(resposta.json()["transacoes"]) == 2  


def test_criar_transacao():
    dados = {
        "descricao": "Conta de energia",
        "valor": 180.50,
        "tipo": "despesa"
    }

    resposta = client.post("/transacoes", json=dados)

    assert resposta.status_code == 201
    assert resposta.json()["descricao"] == "Conta de energia"
    assert resposta.json()["valor"] == 180.50
    assert resposta.json()["tipo"] == "despesa"
    assert isinstance(resposta.json()["id"], int)


def test_buscar_transacao_existente():
    resposta = client.get("/transacoes/1")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == 1
    assert resposta.json()["descricao"] == "Salário"


def test_buscar_transacao_inexistente():
    resposta = client.get("/transacoes/9999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Transação não encontrada"


def test_atualizar_transacao():
    dados = {
        "descricao": "Supermercado",
        "valor": 280.00,
        "tipo": "despesa"
    }

    resposta = client.put("/transacoes/2", json=dados)

    assert resposta.status_code == 200
    assert resposta.json()["id"] == 2
    assert resposta.json()["valor"] == 280.00

    consulta = client.get("/transacoes/2")
    assert consulta.json()["valor"] == 280.00


def test_atualizar_transacao_inexistente():
    dados = {
        "descricao": "Despesa inexistente",
        "valor": 100.00,
        "tipo": "despesa"
    }

    resposta = client.put("/transacoes/9999", json=dados)

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Transação não encontrada"


def test_excluir_transacao():
    # Primeiro cria uma transação exclusiva para o teste
    dados = {
        "descricao": "Transação para excluir",
        "valor": 50.00,
        "tipo": "despesa"
    }

    criacao = client.post("/transacoes", json=dados)

    assert criacao.status_code == 201

    transacao_id = criacao.json()["id"]

    # Exclui a transação criada
    resposta = client.delete(f"/transacoes/{transacao_id}")

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Transação excluída com sucesso"

    # Verifica se a transação realmente deixou de existir
    consulta = client.get(f"/transacoes/{transacao_id}")

    assert consulta.status_code == 404


def test_excluir_transacao_inexistente():
    resposta = client.delete("/transacoes/9999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Transação não encontrada"
