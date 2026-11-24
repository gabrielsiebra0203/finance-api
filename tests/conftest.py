
import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db_connection import get_db
from app.db_models import Base
from tests.db_test import test_engine, verificar_banco_teste


@pytest.fixture
def db_session():
    verificar_banco_teste()

    Base.metadata.create_all(bind=test_engine)

    conexao = test_engine.connect()
    transacao = conexao.begin()

    try:
        with Session(
            bind=conexao,
            join_transaction_mode="create_savepoint"
        ) as sessao:
            yield sessao
    finally:
        transacao.rollback()
        conexao.close()


@pytest.fixture
def client_db(db_session):
    def substituir_get_db():
        yield db_session

    app.dependency_overrides[get_db] = substituir_get_db

    try:
        with TestClient(app) as cliente:
            yield cliente
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def client(client_db):
    yield client_db
