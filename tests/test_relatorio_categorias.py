
from decimal import Decimal


def criar_transacao(
    client,
    descricao,
    valor,
    tipo,
    categoria,
    data
):
    resposta = client.post(
        "/transacoes",
        json={
            "descricao": descricao,
            "valor": valor,
            "tipo": tipo,
            "categoria": categoria,
            "data_transacao": data
        }
    )

    assert resposta.status_code == 201
    return resposta.json()


def preparar_transacoes(client):
    criar_transacao(
        client, "Supermercado", "350.00",
        "despesa", "Alimentação", "2026-10-10"
    )

    criar_transacao(
        client, "Restaurante", "120.00",
        "despesa", "Alimentação", "2026-10-15"
    )

    criar_transacao(
        client, "Aluguel", "1500.00",
        "despesa", "Moradia", "2026-10-20"
    )

    criar_transacao(
        client, "Uber", "80.00",
        "despesa", "Transporte", "2026-11-05"
    )

    criar_transacao(
        client, "Salário", "4000.00",
        "receita", "Trabalho", "2026-10-10"
    )


def categorias_por_nome(resposta):
    return {
        item["categoria"]: Decimal(item["total"])
        for item in resposta.json()["categorias"]
    }


def test_relatorio_agrupa_despesas(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/categorias"
    )

    assert resposta.status_code == 200

    categorias = categorias_por_nome(resposta)

    assert len(categorias) == 3
    assert categorias["Alimentação"] == Decimal("470.00")
    assert categorias["Moradia"] == Decimal("1500.00")
    assert categorias["Transporte"] == Decimal("80.00")


def test_relatorio_ignora_receitas(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/categorias"
    )

    assert resposta.status_code == 200

    categorias = categorias_por_nome(resposta)

    assert "Trabalho" not in categorias


def test_relatorio_ordena_por_maior_valor(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/categorias"
    )

    assert resposta.status_code == 200

    categorias = resposta.json()["categorias"]

    assert categorias[0]["categoria"] == "Moradia"
    assert categorias[1]["categoria"] == "Alimentação"
    assert categorias[2]["categoria"] == "Transporte"


def test_relatorio_filtra_data_inicio(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/categorias",
        params={
            "data_inicio": "2026-11-01"
        }
    )

    assert resposta.status_code == 200

    categorias = categorias_por_nome(resposta)

    assert categorias == {
        "Transporte": Decimal("80.00")
    }


def test_relatorio_filtra_data_fim(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/categorias",
        params={
            "data_fim": "2026-10-31"
        }
    )

    assert resposta.status_code == 200

    categorias = categorias_por_nome(resposta)

    assert categorias == {
        "Moradia": Decimal("1500.00"),
        "Alimentação": Decimal("470.00")
    }


def test_relatorio_filtra_intervalo(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/categorias",
        params={
            "data_inicio": "2026-10-01",
            "data_fim": "2026-10-31"
        }
    )

    assert resposta.status_code == 200

    categorias = categorias_por_nome(resposta)

    assert len(categorias) == 2
    assert categorias["Moradia"] == Decimal("1500.00")
    assert categorias["Alimentação"] == Decimal("470.00")


def test_relatorio_periodo_sem_despesas(client):
    preparar_transacoes(client)

    resposta = client.get(
        "/transacoes/relatorio/categorias",
        params={
            "data_inicio": "2026-09-01",
            "data_fim": "2026-09-30"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json() == {"categorias": []}


def test_relatorio_intervalo_invalido(client):
    resposta = client.get(
        "/transacoes/relatorio/categorias",
        params={
            "data_inicio": "2026-12-01",
            "data_fim": "2026-11-01"
        }
    )

    assert resposta.status_code == 422

    assert resposta.json()["detail"] == (
        "A data inicial não pode ser maior que a data final"
    )
