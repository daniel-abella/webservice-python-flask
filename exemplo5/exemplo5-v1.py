from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de produtos (banco de dados em memória)
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00, "quantidade": 10},
    {"id": 2, "nome": "Mouse",    "preco": 80.00,   "quantidade": 50},
    {"id": 3, "nome": "Teclado",  "preco": 150.00,  "quantidade": 30},
]

proximo_id = 4  # Controle do próximo ID disponível


def buscar_produto(id):
    for produto in produtos:
        if produto["id"] == id:
            return produto
    return None


# GET /produtos — lista todos os produtos
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos), 200


# GET /produtos/<id> — busca um produto pelo ID
@app.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto), 200


# POST /produtos — cria um novo produto
@app.route("/produtos", methods=["POST"])
def criar_produto():
    global proximo_id
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

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


# PUT /produtos/<id> — atualiza um produto existente
@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    if "nome" in dados:
        produto["nome"] = dados["nome"]
    if "preco" in dados:
        produto["preco"] = dados["preco"]
    if "quantidade" in dados:
        produto["quantidade"] = dados["quantidade"]

    return jsonify(produto), 200


# DELETE /produtos/<id> — remove um produto
@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produtos.remove(produto)
    return jsonify({"mensagem": f"Produto {id} removido com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
