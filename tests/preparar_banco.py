
from tests.db_test import test_engine, verificar_banco_teste
from app.db_models import Base


def preparar_banco_teste():
    nome_banco = verificar_banco_teste()

    print(f"Banco confirmado: {nome_banco}")

    Base.metadata.create_all(bind=test_engine)

    print("Tabelas de teste criadas com sucesso!")


if __name__ == "__main__":
    preparar_banco_teste()
