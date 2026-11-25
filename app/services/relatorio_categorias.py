
from datetime import date
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db_models import Transacao


def calcular_despesas_por_categoria(
    db: Session,
    data_inicio: date | None = None,
    data_fim: date | None = None
):

    total_categoria = func.sum(Transacao.valor)

    comando = (
        select(
            Transacao.categoria,
            total_categoria.label("total")
        )
        .where(Transacao.tipo == "despesa")
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

    # Agrupar e ordenar
    comando = (
        comando
        .group_by(Transacao.categoria)
        .order_by(total_categoria.desc())
    )

    resultados = db.execute(comando).all()

    categorias = []

    for categoria, total in resultados:
        categorias.append({
            "categoria": categoria or "Sem categoria",
            "total": total if total is not None else Decimal("0.00")
        })

    return {"categorias": categorias}
