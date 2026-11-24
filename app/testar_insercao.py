
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db_connection import engine
from app.db_models import Transacao


def inserir_transacao():
    with Session(engine) as sessao:
        nova_transacao = Transacao(
            descricao="Primeira transação PostgreSQL",
            valor=Decimal("150.00"),
            tipo="receita"
        )

        sessao.add(nova_transacao)
        sessao.commit()
        sessao.refresh(nova_transacao)

        print("Transação cadastrada com sucesso!")
        print(f"ID: {nova_transacao.id}")
        print(f"Descrição: {nova_transacao.descricao}")
        print(f"Valor: R$ {nova_transacao.valor}")
        print(f"Tipo: {nova_transacao.tipo}")


if __name__ == "__main__":
    inserir_transacao()
