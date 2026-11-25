
from datetime import date
from decimal import Decimal

from sqlalchemy import select, func, case
from sqlalchemy.orm import Session

from app.db_models import Transacao


def calcular_relatorio_mensal(
    db: Session,
    ano: int | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None
):

    # Agrupamento por mês
    mes_transacao = func.date_trunc(
        "month",
        Transacao.data_transacao
    )

    # Soma das receitas
    soma_receitas = func.sum(
        case(
            (
                Transacao.tipo == "receita",
                Transacao.valor
            ),
            else_=0
        )
    )

    # Soma das despesas
    soma_despesas = func.sum(
        case(
            (
                Transacao.tipo == "despesa",
                Transacao.valor
            ),
            else_=0
        )
    )

    # Consulta inicial
    comando = select(
        mes_transacao.label("mes"),
        soma_receitas.label("total_receitas"),
        soma_despesas.label("total_despesas")
    )

    # Filtrar por ano
    if ano is not None:
        comando = comando.where(
            Transacao.data_transacao >= date(ano, 1, 1),
            Transacao.data_transacao <= date(ano, 12, 31)
        )

    # Filtrar pela data inicial
    if data_inicio is not None:
        comando = comando.where(
            Transacao.data_transacao >= data_inicio
        )

    # Filtrar pela data final
    if data_fim is not None:
        comando = comando.where(
            Transacao.data_transacao <= data_fim
        )

    # Agrupar e ordenar cronologicamente
    comando = (
        comando
        .group_by(mes_transacao)
        .order_by(mes_transacao)
    )

    resultados = db.execute(comando).all()

    meses = []

    for mes, receitas, despesas in resultados:

        total_receitas = (
            receitas
            if receitas is not None
            else Decimal("0.00")
        )

        total_despesas = (
            despesas
            if despesas is not None
            else Decimal("0.00")
        )

        saldo = total_receitas - total_despesas

        meses.append({
            "mes": mes.strftime("%Y-%m"),
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "saldo": saldo
        })

    return {"meses": meses}
