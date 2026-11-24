
from decimal import Decimal


def criar_transacao(client, descricao, valor, tipo):
    resposta = client.post(
        "/transacoes",
        json={
            "descricao": descricao,
            "valor": str(valor),
            "tipo": tipo,
            "categoria": "Teste"
        }
    )

    assert resposta.status_code == 201
    return resposta.json()


def test_resumo_financeiro_banco_vazio(client):
    resposta = client.get("/transacoes/resumo")

    assert resposta.status_code == 200

    dados = resposta.json()

    assert Decimal(dados["total_receitas"]) == Decimal("0.00")
    assert Decimal(dados["total_despesas"]) == Decimal("0.00")
    assert Decimal(dados["saldo"]) == Decimal("0.00")


def test_resumo_financeiro_apenas_receitas(client):
    criar_transacao(client, "Salario", "3500.00", "receita")
    criar_transacao(client, "Freelance", "800.00", "receita")

    resposta = client.get("/transacoes/resumo")

    assert resposta.status_code == 200

    dados = resposta.json()

    assert Decimal(dados["total_receitas"]) == Decimal("4300.00")
    assert Decimal(dados["total_despesas"]) == Decimal("0.00")
    assert Decimal(dados["saldo"]) == Decimal("4300.00")


def test_resumo_financeiro_apenas_despesas(client):
    criar_transacao(client, "Aluguel", "1200.00", "despesa")
    criar_transacao(client, "Internet", "100.00", "despesa")

    resposta = client.get("/transacoes/resumo")

    assert resposta.status_code == 200

    dados = resposta.json()

    assert Decimal(dados["total_receitas"]) == Decimal("0.00")
    assert Decimal(dados["total_despesas"]) == Decimal("1300.00")
    assert Decimal(dados["saldo"]) == Decimal("-1300.00")


def test_resumo_financeiro_receitas_e_despesas(client):
    criar_transacao(client, "Salario", "3500.00", "receita")
    criar_transacao(client, "Freelance", "800.00", "receita")
    criar_transacao(client, "Aluguel", "1200.00", "despesa")
    criar_transacao(client, "Supermercado", "450.00", "despesa")
    criar_transacao(client, "Internet", "100.00", "despesa")

    resposta = client.get("/transacoes/resumo")

    assert resposta.status_code == 200

    dados = resposta.json()

    assert Decimal(dados["total_receitas"]) == Decimal("4300.00")
    assert Decimal(dados["total_despesas"]) == Decimal("1750.00")
    assert Decimal(dados["saldo"]) == Decimal("2550.00")
