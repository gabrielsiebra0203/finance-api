
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
        "receita", "2025-09-10"
    )

    criar_transacao(
        client, "Aluguel setembro", "1000.00",
        "despesa", "2025-09-15"
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


def meses_por_nome(resposta):
    return {
        item["mes"]: item
        for item in resposta.json()["meses"]
    }


def verificar_valores(mes, receitas, despesas, saldo):
    assert Decimal(mes["total_receitas"]) == Decimal(receitas)
    assert Decimal(mes["total_despesas"]) == Decimal(despesas)
    assert Decimal(mes["saldo"]) == Decimal(saldo)


def test_relatorio_agrupa_por_mes(client):
    preparar_transacoes(client)

    resposta = client.get("/transacoes/relatorio/mensal")

    assert resposta.status_code == 200

    meses = meses_por_nome(resposta)

    assert len(meses) == 3
    assert "2025-09" in meses
    assert "2026-10" in meses
    assert "2026-11" in meses


def test_relatorio_calcula_valores(client):
    preparar_transacoes(client)

    resposta = client.get("/transacoes/relatorio/mensal")

    assert resposta.status_code == 200

    meses = meses_por_nome(resposta)

    verificar_valores(
        meses["2025-09"], "3000.00", "1000.00", "2000.00"
    )

    verificar_valores(
        meses["2026-10"], "3500.00", "500.00", "3000.00"
    )

    verificar_valores(
        meses["2026-11"], "4000.00", "1200.00", "2800.00"
    )


def test_relatorio_ordem_cronologica(client):
    preparar_transacoes(client)

    resposta = client.get("/transacoes/relatorio/mensal")

    assert resposta.status_code == 200

    meses = [
        item["mes"]
        for item in resposta.json()["meses"]
    ]

    assert meses == ["2025-09", "2026-10", "2026-11"]


def test_relatorio_filtra_por_ano(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/mensal",
        params={"ano": 2026}
    )

    assert resposta.status_code == 200

    meses = meses_por_nome(resposta)

    assert set(meses) == {"2026-10", "2026-11"}


def test_relatorio_filtra_data_inicio(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/mensal",
        params={"data_inicio": "2026-11-01"}
    )

    assert resposta.status_code == 200

    meses = meses_por_nome(resposta)

    assert set(meses) == {"2026-11"}


def test_relatorio_filtra_data_fim(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/mensal",
        params={"data_fim": "2026-10-31"}
    )

    assert resposta.status_code == 200

    meses = meses_por_nome(resposta)

    assert set(meses) == {"2025-09", "2026-10"}


def test_relatorio_filtra_intervalo(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/mensal",
        params={
            "data_inicio": "2026-10-01",
            "data_fim": "2026-10-31"
        }
    )

    assert resposta.status_code == 200

    meses = meses_por_nome(resposta)

    assert set(meses) == {"2026-10"}

    verificar_valores(
        meses["2026-10"], "3500.00", "500.00", "3000.00"
    )


def test_relatorio_combina_ano_e_periodo(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/mensal",
        params={
            "ano": 2026,
            "data_inicio": "2026-11-01"
        }
    )

    assert resposta.status_code == 200

    meses = meses_por_nome(resposta)

    assert set(meses) == {"2026-11"}


def test_relatorio_periodo_vazio(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/mensal",
        params={"ano": 2024}
    )

    assert resposta.status_code == 200
    assert resposta.json() == {"meses": []}


def test_relatorio_intervalo_invalido(client):
    resposta = client.get(
        "/transacoes/relatorio/mensal",
        params={
            "data_inicio": "2026-12-01",
            "data_fim": "2026-11-01"
        }
    )

    assert resposta.status_code == 422

    assert resposta.json()["detail"] == (
        "A data inicial não pode ser maior que a data final"
    )
