
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db_models import Transacao
from app.models import ResumoFinanceiroSaida


def calcular_resumo_financeiro(
    db: Session
) -> ResumoFinanceiroSaida:

    consulta_receitas = select(
        func.sum(Transacao.valor)
    ).where(
        Transacao.tipo == "receita"
    )

    consulta_despesas = select(
        func.sum(Transacao.valor)
    ).where(
        Transacao.tipo == "despesa"
    )

    total_receitas = db.scalar(consulta_receitas)
    total_despesas = db.scalar(consulta_despesas)

    if total_receitas is None:
        total_receitas = Decimal("0.00")

    if total_despesas is None:
        total_despesas = Decimal("0.00")

    saldo = total_receitas - total_despesas

    return ResumoFinanceiroSaida(
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo
    )
