
def test_documentacao_openapi_disponivel(client):
    resposta = client.get("/openapi.json")

    assert resposta.status_code == 200

    documentacao = resposta.json()

    assert "openapi" in documentacao
    assert "/transacoes" in documentacao["paths"]
    assert "/transacoes/{transacao_id}" in documentacao["paths"]


def test_schemas_documentados(client):
    resposta = client.get("/openapi.json")

    assert resposta.status_code == 200

    schemas = resposta.json()["components"]["schemas"]

    assert "TransacaoEntrada" in schemas
    assert "TransacaoSaida" in schemas
    assert "ListaTransacoesSaida" in schemas


def test_post_documenta_resposta_201(client):
    documentacao = client.get("/openapi.json").json()

    respostas = documentacao["paths"]["/transacoes"]["post"]["responses"]

    assert "201" in respostas

    schema = respostas["201"]["content"]["application/json"]["schema"]

    assert schema["$ref"] == "#/components/schemas/TransacaoSaida"


def test_get_lista_documenta_schema(client):
    documentacao = client.get("/openapi.json").json()

    respostas = documentacao["paths"]["/transacoes"]["get"]["responses"]

    schema = respostas["200"]["content"]["application/json"]["schema"]

    assert schema["$ref"] == "#/components/schemas/ListaTransacoesSaida"


def test_get_e_put_documentam_schema(client):
    documentacao = client.get("/openapi.json").json()

    caminho = documentacao["paths"]["/transacoes/{transacao_id}"]

    for metodo in ("get", "put"):
        schema = caminho[metodo]["responses"]["200"]["content"][
            "application/json"
        ]["schema"]

        assert schema["$ref"] == "#/components/schemas/TransacaoSaida"
