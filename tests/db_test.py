
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_TEST_NAME = os.getenv("DB_TEST_NAME")

if DB_TEST_NAME != "finance_test_db":
    raise RuntimeError(
        "Banco de testes não configurado corretamente."
    )

TEST_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5433")),
    database=DB_TEST_NAME
)

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False
)


def verificar_banco_teste():
    with test_engine.connect() as conexao:
        nome_banco = conexao.execute(
            text("SELECT current_database()")
        ).scalar_one()

        if nome_banco != "finance_test_db":
            raise RuntimeError(
                "Conexão não está usando o banco de testes!"
            )

        return nome_banco
