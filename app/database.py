
from decimal import Decimal

# Banco de dados temporário em memória
transacoes = [
    {
        "id": 1,
        "descricao": "Salário",
        "valor": Decimal("3000.00"),
        "tipo": "receita"
    },
    {
        "id": 2,
        "descricao": "Supermercado",
        "valor": Decimal("250.00"),
        "tipo": "despesa"
    }
]
