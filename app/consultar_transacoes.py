
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_connection import engine
from app.db_models import Transacao


def consultar_transacoes():
    with Session(engine) as sessao:
        comando = select(Transacao).order_by(Transacao.id)

        transacoes = sessao.scalars(comando).all()

        if not transacoes:
            print("Nenhuma transação cadastrada.")
            return

        print(f"Total de transações: {len(transacoes)}")

        for transacao in transacoes:
            print("---------------------------")
            print(f"ID: {transacao.id}")
            print(f"Descrição: {transacao.descricao}")
            print(f"Valor: R$ {transacao.valor}")
            print(f"Tipo: {transacao.tipo}")


if __name__ == "__main__":
    consultar_transacoes()
