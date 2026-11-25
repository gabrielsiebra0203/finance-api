
from decimal import Decimal


def criar_transacao(client, descricao, valor, tipo, data):
    resposta = client.post(
        "/transacoes",
        json={
            "descricao": descricao,
            "valor": valor,
            "tipo": tipo,
            "categoria": "Testes",
            "data_transacao": data
        }
    )

    assert resposta.status_code == 201
    return resposta.json()


def preparar_transacoes(client):
    criar_transacao(
        client, "Salario setembro", "3000.00",
        "receita", "2026-09-10"
    )
    criar_transacao(
        client, "Aluguel setembro", "1000.00",
        "despesa", "2026-09-15"
    )
    criar_transacao(
        client, "Salario outubro", "3500.00",
        "receita", "2026-10-10"
    )
    criar_transacao(
        client, "Mercado outubro", "500.00",
        "despesa", "2026-10-20"
    )
    criar_transacao(
        client, "Salario novembro", "4000.00",
        "receita", "2026-11-10"
    )
    criar_transacao(
        client, "Aluguel novembro", "1200.00",
        "despesa", "2026-11-15"
    )


def verificar_resumo(dados, receitas, despesas, saldo):
    assert Decimal(dados["total_receitas"]) == Decimal(receitas)
    assert Decimal(dados["total_despesas"]) == Decimal(despesas)
    assert Decimal(dados["saldo"]) == Decimal(saldo)


def test_resumo_sem_filtro(client):
    preparar_transacoes(client)

    resposta = client.get("/transacoes/resumo")

    assert resposta.status_code == 200

    verificar_resumo(
        resposta.json(),
        "10500.00",
        "2700.00",
        "7800.00"
    )


def test_resumo_com_data_inicio(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/resumo",
        params={"data_inicio": "2026-10-01"}
    )

    assert resposta.status_code == 200

    verificar_resumo(
        resposta.json(),
        "7500.00",
        "1700.00",
        "5800.00"
    )


def test_resumo_com_data_fim(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/resumo",
        params={"data_fim": "2026-10-31"}
    )

    assert resposta.status_code == 200

    verificar_resumo(
        resposta.json(),
        "6500.00",
        "1500.00",
        "5000.00"
    )


def test_resumo_intervalo_outubro(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/resumo",
        params={
            "data_inicio": "2026-10-01",
            "data_fim": "2026-10-31"
        }
    )

    assert resposta.status_code == 200

    verificar_resumo(
        resposta.json(),
        "3500.00",
        "500.00",
        "3000.00"
    )


def test_resumo_periodo_sem_transacoes(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/resumo",
        params={
            "data_inicio": "2026-08-01",
            "data_fim": "2026-08-31"
        }
    )

    assert resposta.status_code == 200

    verificar_resumo(
        resposta.json(),
        "0.00",
        "0.00",
        "0.00"
    )


def test_resumo_intervalo_invalido(client):
    resposta = client.get(
        "/transacoes/resumo",
        params={
            "data_inicio": "2026-12-01",
            "data_fim": "2026-11-01"
        }
    )

    assert resposta.status_code == 422

    assert resposta.json()["detail"] == (
        "A data inicial não pode ser maior que a data final"
    )
