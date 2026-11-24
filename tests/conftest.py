
import pytest
from copy import deepcopy

from fastapi.testclient import TestClient
from app.main import app
from app.database import transacoes


DADOS_INICIAIS = deepcopy(transacoes)


@pytest.fixture(autouse=True)
def restaurar_transacoes():
    # Garante os mesmos dados antes de cada teste
    transacoes[:] = deepcopy(DADOS_INICIAIS)

    yield

    # Limpa qualquer alteração feita pelo teste
    transacoes[:] = deepcopy(DADOS_INICIAIS)


@pytest.fixture
def client():
    with TestClient(app) as cliente:
        yield cliente
