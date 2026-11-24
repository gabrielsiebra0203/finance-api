
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