"""
exemplo3-v1.py — API REST com Flask + Flasgger
==============================================

Este exemplo reaproveita o CRUD de produtos e adiciona documentação
interativa com Flasgger. O Flasgger lê anotações escritas nas rotas e
gera automaticamente uma interface Swagger no navegador.

Como executar:
  python exemplo3-v1.py

Depois de iniciar o servidor:
  API      → http://127.0.0.1:5000/produtos
  Swagger  → http://127.0.0.1:5000/apidocs/
"""

# ---------------------------------------------------------------------------
# IMPORTAÇÕES
# ---------------------------------------------------------------------------
# Flask     → framework web usado para criar as rotas HTTP.
# jsonify   → converte listas/dicionários Python em respostas JSON.
# request   → fornece acesso ao corpo e aos dados da requisição enviada.
# Swagger   → componente do Flasgger que habilita a interface Swagger UI.
from flask import Flask, jsonify, request
from flasgger import Swagger

# ---------------------------------------------------------------------------
# CRIAÇÃO DA APLICAÇÃO
# ---------------------------------------------------------------------------
# A instância principal do Flask representa nosso servidor web.
app = Flask(__name__)

# Configuração básica exibida na página do Swagger.
# Esse dicionário descreve o título da API, versão e descrição geral.
app.config["SWAGGER"] = {
    "title": "API de Produtos com Flask e Flasgger",
    "uiversion": 3,
}

# Inicializa o Flasgger e conecta a documentação à aplicação Flask.
swagger = Swagger(
    app,
    template={
        "info": {
            "title": "API de Produtos",
            "version": "1.0.0",
            "description": (
                "Exemplo didático de CRUD com Flask documentado com Swagger UI."
            ),
        }
    },
)

# ---------------------------------------------------------------------------
# "BANCO DE DADOS" EM MEMÓRIA
# ---------------------------------------------------------------------------
# Os produtos ficam salvos apenas em memória, em uma lista de dicionários.
# Isso simplifica o exemplo e evita depender de banco de dados externo.
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00, "quantidade": 10},
    {"id": 2, "nome": "Mouse", "preco": 80.00, "quantidade": 50},
    {"id": 3, "nome": "Teclado", "preco": 150.00, "quantidade": 30},
]

# Controla o próximo ID a ser usado ao cadastrar um novo produto.
proximo_id = 4


# ---------------------------------------------------------------------------
# FUNÇÃO AUXILIAR
# ---------------------------------------------------------------------------
def buscar_produto(id):
    """
    Localiza um produto pelo ID dentro da lista em memória.

    Retorna o dicionário do produto quando encontrado.
    Se o ID não existir, retorna None.
    """
    for produto in produtos:
        if produto["id"] == id:
            return produto
    return None


# ---------------------------------------------------------------------------
# ROTAS DA API
# ---------------------------------------------------------------------------
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    """
    Lista todos os produtos cadastrados.
    ---
    tags:
      - Produtos
    responses:
      200:
        description: Lista de produtos retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: Notebook
              preco:
                type: number
                format: float
                example: 3500.0
              quantidade:
                type: integer
                example: 10
    """
    return jsonify(produtos), 200


@app.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    """
    Busca um produto específico pelo ID.
    ---
    tags:
      - Produtos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do produto que será consultado.
        example: 1
    responses:
      200:
        description: Produto encontrado com sucesso.
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: Notebook
            preco:
              type: number
              format: float
              example: 3500.0
            quantidade:
              type: integer
              example: 10
      404:
        description: Produto não encontrado.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Produto não encontrado
    """
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto), 200


@app.route("/produtos", methods=["POST"])
def criar_produto():
    """
    Cria um novo produto.
    ---
    tags:
      - Produtos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
            - preco
            - quantidade
          properties:
            nome:
              type: string
              example: Monitor
            preco:
              type: number
              format: float
              example: 1200.0
            quantidade:
              type: integer
              example: 5
    responses:
      201:
        description: Produto criado com sucesso.
      400:
        description: Corpo inválido ou campo obrigatório ausente.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Campo obrigatório ausente: nome"
    """
    global proximo_id

    # request.get_json() tenta interpretar o corpo enviado como JSON.
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    # Todos esses campos são obrigatórios para criar um produto completo.
    campos_obrigatorios = ["nome", "preco", "quantidade"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo obrigatório ausente: {campo}"}), 400

    novo_produto = {
        "id": proximo_id,
        "nome": dados["nome"],
        "preco": dados["preco"],
        "quantidade": dados["quantidade"],
    }

    produtos.append(novo_produto)
    proximo_id += 1
    return jsonify(novo_produto), 201


@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    """
    Atualiza um produto existente.
    ---
    tags:
      - Produtos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do produto que será atualizado.
        example: 1
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Notebook Gamer
            preco:
              type: number
              format: float
              example: 4200.0
            quantidade:
              type: integer
              example: 8
    responses:
      200:
        description: Produto atualizado com sucesso.
      400:
        description: Corpo da requisição inválido.
      404:
        description: Produto não encontrado.
    """
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    # A atualização é parcial: somente os campos enviados são alterados.
    if "nome" in dados:
        produto["nome"] = dados["nome"]
    if "preco" in dados:
        produto["preco"] = dados["preco"]
    if "quantidade" in dados:
        produto["quantidade"] = dados["quantidade"]

    return jsonify(produto), 200


@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    """
    Remove um produto pelo ID.
    ---
    tags:
      - Produtos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do produto que será removido.
        example: 1
    responses:
      200:
        description: Produto removido com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Produto 1 removido com sucesso
      404:
        description: Produto não encontrado.
    """
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produtos.remove(produto)
    return jsonify({"mensagem": f"Produto {id} removido com sucesso"}), 200


# ---------------------------------------------------------------------------
# PONTO DE ENTRADA
# ---------------------------------------------------------------------------
# Ao executar este arquivo diretamente, o servidor Flask inicia na porta 5000.
if __name__ == "__main__":
    app.run(debug=True, port=5000)
