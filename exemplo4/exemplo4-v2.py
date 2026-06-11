from flask import Flask, jsonify, request
from operacoesbd import *

app = Flask(__name__)

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_SENHA = "Unifacisa12!"
DB_NOME = "loja_cauca"


def get_connection():
    return criarConexao(DB_HOST, DB_USER, DB_SENHA, DB_NOME)


def produto_para_dict(row):
    """Converte uma linha do banco (tupla) em dicionário."""
    return {
        "id": row[0],
        "nome": row[1],
        "preco": float(row[2]),
        "quantidade": row[3],
    }


# GET /produtos — lista todos os produtos
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    conn = get_connection()
    if conn is None:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    sql = "SELECT id, nome, preco, quantidade FROM produtos"
    rows = listarBancoDados(conn, sql)
    encerrarConexao(conn)

    return jsonify([produto_para_dict(r) for r in rows]), 200


# GET /produtos/<id> — busca um produto pelo ID
@app.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    conn = get_connection()
    if conn is None:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    sql = "SELECT id, nome, preco, quantidade FROM produtos WHERE id = %s"
    dados = [id]
    rows = listarBancoDados(conn, sql, dados)
    encerrarConexao(conn)

    if not rows:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify(produto_para_dict(rows[0])), 200


# POST /produtos — cria um novo produto
@app.route("/produtos", methods=["POST"])
def criar_produto():
    dados = request.get_json()

    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    campos_obrigatorios = ["nome", "preco", "quantidade"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo obrigatório ausente: {campo}"}), 400

    conn = get_connection()
    if conn is None:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    sql = "INSERT INTO produtos (nome, preco, quantidade) VALUES (%s, %s, %s)"
    valores = (dados["nome"], dados["preco"], dados["quantidade"])
    novo_id = insertNoBancoDados(conn, sql, valores)
    encerrarConexao(conn)

    if novo_id is None:
        return jsonify({"erro": "Erro ao inserir produto"}), 500

    return jsonify({"id": novo_id, "nome": dados["nome"], "preco": dados["preco"], "quantidade": dados["quantidade"]}), 201


# PUT /produtos/<id> — atualiza um produto existente
@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    campos = []
    valores = []

    if "nome" in dados:
        campos.append("nome = %s")
        valores.append(dados["nome"])
    if "preco" in dados:
        campos.append("preco = %s")
        valores.append(dados["preco"])
    if "quantidade" in dados:
        campos.append("quantidade = %s")
        valores.append(dados["quantidade"])

    if not campos:
        return jsonify({"erro": "Nenhum campo para atualizar"}), 400

    valores.append(id)

    conn = get_connection()
    if conn is None:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    sql = f"UPDATE produtos SET {', '.join(campos)} WHERE id = %s"
    linhas = atualizarBancoDados(conn, sql, tuple(valores))
    encerrarConexao(conn)

    if linhas == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify({"mensagem": f"Produto {id} atualizado com sucesso"}), 200


# DELETE /produtos/<id> — remove um produto
@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    conn = get_connection()
    if conn is None:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    sql = "DELETE FROM produtos WHERE id = %s"
    linhas = excluirBancoDados(conn, sql, (id,))
    encerrarConexao(conn)

    if linhas == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify({"mensagem": f"Produto {id} removido com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
