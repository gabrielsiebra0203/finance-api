
from decimal import Decimal

from app.db_models import Transacao


def test_listar_transacoes_postgresql(client_db, db_session):
    # Criar uma transação no banco de testes
    nova_transacao = Transacao(
        descricao="Pagamento de teste",
        valor=Decimal("250.00"),
        tipo="receita"
    )

    db_session.add(nova_transacao)
    db_session.commit()

    # Consultar o endpoint da API
    resposta = client_db.get("/transacoes")

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["total"] == 1
    assert len(dados["transacoes"]) == 1
    assert dados["transacoes"][0]["descricao"] == "Pagamento de teste"
    assert dados["transacoes"][0]["tipo"] == "receita"



def test_criar_transacao_postgresql(client_db, db_session):
    nova_transacao = {
        "descricao": "Venda de notebook",
        "valor": "2500.00",
        "tipo": "receita"
    }

    resposta = client_db.post(
        "/transacoes",
        json=nova_transacao
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["descricao"] == "Venda de notebook"
    assert Decimal(str(dados["valor"])) == Decimal("2500.00")
    assert dados["tipo"] == "receita"
    assert isinstance(dados["id"], int)

    # Confirmar que o registro foi salvo no banco de testes
    transacao_salva = db_session.get(
        Transacao,
        dados["id"]
    )

    assert transacao_salva is not None
    assert transacao_salva.descricao == "Venda de notebook"


def test_buscar_transacao_por_id(client_db):
    # Criar uma transação usando a API
    resposta_post = client_db.post(
        "/transacoes",
        json={
            "descricao": "Compra de teclado",
            "valor": "180.00",
            "tipo": "despesa"
        }
    )

    assert resposta_post.status_code == 201

    transacao_id = resposta_post.json()["id"]

    # Buscar a transação pelo ID
    resposta_get = client_db.get(
        f"/transacoes/{transacao_id}"
    )

    assert resposta_get.status_code == 200

    dados = resposta_get.json()

    assert dados["id"] == transacao_id
    assert dados["descricao"] == "Compra de teclado"
    assert Decimal(str(dados["valor"])) == Decimal("180.00")
    assert dados["tipo"] == "despesa"


def test_buscar_transacao_inexistente(client_db):
    resposta = client_db.get("/transacoes/999999")

    assert resposta.status_code == 404
    assert resposta.json() == {
        "detail": "Transação não encontrada"
    }


def test_atualizar_transacao_postgresql(client_db):
    resposta_post = client_db.post(
        "/transacoes",
        json={
            "descricao": "Notebook antigo",
            "valor": "1500.00",
            "tipo": "despesa"
        }
    )

    assert resposta_post.status_code == 201

    transacao_id = resposta_post.json()["id"]

    resposta_put = client_db.put(
        f"/transacoes/{transacao_id}",
        json={
            "descricao": "Notebook atualizado",
            "valor": "1800.00",
            "tipo": "despesa"
        }
    )

    assert resposta_put.status_code == 200

    dados = resposta_put.json()

    assert dados["id"] == transacao_id
    assert dados["descricao"] == "Notebook atualizado"
    assert Decimal(str(dados["valor"])) == Decimal("1800.00")
    assert dados["tipo"] == "despesa"

    # Confirmar que o GET retorna os dados atualizados
    resposta_get = client_db.get(
        f"/transacoes/{transacao_id}"
    )

    assert resposta_get.status_code == 200
    assert resposta_get.json()["descricao"] == "Notebook atualizado"


def test_atualizar_transacao_inexistente(client_db):
    resposta = client_db.put(
        "/transacoes/999999",
        json={
            "descricao": "Transação inexistente",
            "valor": "100.00",
            "tipo": "receita"
        }
    )

    assert resposta.status_code == 404
    assert resposta.json() == {
        "detail": "Transação não encontrada"
    }


def test_excluir_transacao_postgresql(client_db):
    # Criar uma transação
    resposta_post = client_db.post(
        "/transacoes",
        json={
            "descricao": "Compra de mouse",
            "valor": "120.00",
            "tipo": "despesa"
        }
    )

    assert resposta_post.status_code == 201

    transacao_id = resposta_post.json()["id"]

    # Excluir a transação
    resposta_delete = client_db.delete(
        f"/transacoes/{transacao_id}"
    )

    assert resposta_delete.status_code == 200
    assert resposta_delete.json() == {
        "mensagem": "Transação excluída com sucesso",
        "id": transacao_id
    }

    # Confirmar que não existe mais
    resposta_get = client_db.get(
        f"/transacoes/{transacao_id}"
    )

    assert resposta_get.status_code == 404


def test_excluir_transacao_inexistente(client_db):
    resposta = client_db.delete(
        "/transacoes/999999"
    )

    assert resposta.status_code == 404
    assert resposta.json() == {
        "detail": "Transação não encontrada"
    }
