
from decimal import Decimal

from sqlalchemy import select

from app.db_models import Transacao


def test_inserir_transacao_temporaria(db_session):
    nova_transacao = Transacao(
        descricao="Transação temporária",
        valor=Decimal("99.90"),
        tipo="despesa"
    )

    db_session.add(nova_transacao)
    db_session.commit()

    resultado = db_session.scalars(
        select(Transacao)
    ).all()

    assert len(resultado) == 1
    assert resultado[0].descricao == "Transação temporária"
